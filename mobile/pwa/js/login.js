/**
 * Security-chip login (ECDH P-256 + HKDF-SHA256 + AES-CCM confirmation) —
 * порт stage_a_pubkey_exchange / derive_session_key / stage_b_confirm
 * из dreame_auth.py. Все использованные примитивы (ECDH shared-secret,
 * HKDF, AES-CCM, CRC32) сверены побайтово с Python — см. mobile/test/.
 */
import { CH_CONTROL, CH_LOGIN } from "./transport.js";
import { concatBytes, crc32, u32le, bytesToHex } from "./bin.js";
import { ccmEncrypt } from "./aes-ccm.js";

const LOGIN_SALT = new TextEncoder().encode("smartcfg-login-salt");
const LOGIN_INFO = new TextEncoder().encode("smartcfg-login-info");
// bytes(range(0x10, 0x1c)) в Python — 12 байт: 10 11 12 ... 1b
const CCM_NONCE = new Uint8Array([0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b]);

export let LAST_SK = null; // sessionKey последнего успешного логина (64Б) — как LAST_SK в Python

async function genEcKeypair(subtle) {
  const kp = await subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]);
  const raw65 = new Uint8Array(await subtle.exportKey("raw", kp.publicKey)); // 0x04 || X(32) || Y(32)
  return { privateKey: kp.privateKey, rawPub: raw65.slice(1) }; // 64Б X||Y, как getRawPublicKey в APK
}

/**
 * ECDH shared secret (X-координата, 32Б) + HKDF-SHA256(shared||ltmk) -> sessionKey 64Б.
 */
export async function deriveSessionKey(subtle, privateKey, devPubRaw64, ltmk32) {
  const devPub65 = concatBytes(new Uint8Array([0x04]), devPubRaw64);
  const devPubKey = await subtle.importKey("raw", devPub65, { name: "ECDH", namedCurve: "P-256" }, false, []);
  const sharedBits = await subtle.deriveBits({ name: "ECDH", public: devPubKey }, privateKey, 256);
  const shared = new Uint8Array(sharedBits);

  const keymix = concatBytes(shared, ltmk32); // 64Б
  const ikmKey = await subtle.importKey("raw", keymix, "HKDF", false, ["deriveBits"]);
  const okm = await subtle.deriveBits(
    { name: "HKDF", hash: "SHA-256", salt: LOGIN_SALT, info: LOGIN_INFO },
    ikmKey,
    64 * 8
  );
  return { shared, sk: new Uint8Array(okm) };
}

/**
 * Обмен публичными ключами: login-start(0x0010) -> наш pubkey потоком
 * (channel=3, 0x0016) -> приём device pubkey (SINGLE/CTR+DATA).
 * Возвращает {priv, devPub} — devPub===null, если устройство не ответило.
 */
export async function stageAPubkeyExchange(transport, subtle = crypto.subtle) {
  const { privateKey, rawPub } = await genEcKeypair(subtle);
  transport._log(`  app pubkey (raw X||Y, ${rawPub.length}B): ${bytesToHex(rawPub)}`);

  transport.rx.clear();
  await transport.write(CH_CONTROL, new Uint8Array([0x20, 0x00, 0x00]));
  transport._log("  >>> 0x0010: 20 00 00 (login-start)");
  await new Promise((r) => setTimeout(r, 200));

  const ok = await transport.sendStream(3, rawPub);
  if (!ok) transport._log("  [!] отправка pubkey (CTR+DATA) не подтверждена");

  const dev = await transport.recvMessageV2(6000, CH_LOGIN);
  if (dev) {
    transport._log(`  [DEVICE PUBKEY] ${dev.length}B: ${bytesToHex(dev)}`);
    return { priv: privateKey, devPub: dev };
  }
  transport._log("  [!] device pubkey не получен");
  return { priv: privateKey, devPub: null };
}

/**
 * Confirmation: sessionKey из ECDH+HKDF, AES-CCM(sk[16:32], CCM_NONCE,
 * CRC32(devPub) LE, tag=4) -> поток на channel=5. Результат читаем из
 * последнего ответа на 0x0010 (0x21=OK, 0x22=отказ).
 * Возвращает true/false/null (null = нет ответа устройства).
 */
export async function stageBConfirm(transport, priv, devPub, ltmk32, { crcBE = false, subtle = crypto.subtle } = {}) {
  const { shared, sk } = await deriveSessionKey(subtle, priv, devPub, ltmk32);
  LAST_SK = sk;
  const aesKey = sk.slice(16, 32);

  const crc = crc32(devPub);
  const plaintext = crcBE
    ? new Uint8Array([(crc >>> 24) & 0xff, (crc >>> 16) & 0xff, (crc >>> 8) & 0xff, crc & 0xff])
    : u32le(crc);

  transport._log(`  shared[:8]=${bytesToHex(shared.slice(0, 8))} sessionKey[:8]=${bytesToHex(sk.slice(0, 8))} aes_key=${bytesToHex(aesKey)}`);

  const enc = await ccmEncrypt(aesKey, CCM_NONCE, plaintext, 4, subtle);
  transport._log(`  confirmation enc (${enc.length}B): ${bytesToHex(enc)}`);

  transport.lastCtrl = null;
  await transport.sendStream(5, enc);
  await transport.drain(3000);

  const res = transport.lastCtrl;
  transport._log(`  --- ответ устройства на 0x0010: ${res ? bytesToHex(res) : "нет"} ---`);
  if (res && res[0] === 0x21) return true;
  if (res && res[0] === 0x22) return false;
  return null;
}

/** Полный логин: connect должен быть уже вызван. Возвращает sk (64Б) или бросает исключение. */
export async function login(transport, ltmk32, { subtle = crypto.subtle } = {}) {
  if (!(await transport.a4Handshake())) {
    throw new Error("транспорт не поднялся (нет MNG)");
  }
  // устройство иногда шлёт MNG повторно — подтвердим ещё раз, как в Python main()
  for (const [s, b] of await transport.drain(1000)) {
    if (s === CH_LOGIN && b.length >= 3 && b[2] === 4 /* PKT_MNG */) {
      await transport.write(
        CH_LOGIN,
        concatBytes(new Uint8Array([0, 0, 5 /* PKT_MNG_ACK */, 0]), new Uint8Array([transport.pkgNum, transport.dmtu]))
      );
    }
  }
  const { priv, devPub } = await stageAPubkeyExchange(transport, subtle);
  if (!devPub || devPub.length < 64) {
    throw new Error("Stage A: не получен pubkey устройства");
  }
  const ok = await stageBConfirm(transport, priv, devPub, ltmk32, { subtle });
  if (!ok) {
    throw new Error(ok === false ? "login отклонён (0x22) — неверный ltmk/пин" : "login: нет ответа устройства");
  }
  return LAST_SK;
}
