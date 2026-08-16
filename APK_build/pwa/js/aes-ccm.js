/**
 * AES-CCM (RFC 3610 / NIST SP800-38C) поверх WebCrypto SubtleCrypto.
 *
 * SubtleCrypto не умеет CCM нативно (только GCM/CBC/CTR) — но CCM собирается
 * из CBC-MAC (для тега) и CTR (для маскирования тега + шифрования данных),
 * оба примитива у SubtleCrypto есть. Собственной реализации AES-блока нет —
 * это снижает риск тонких ошибок по сравнению с ручным AES.
 *
 * Ограничения (достаточны для протокола самоката, см. dreame_auth.py):
 *   - nonce строго 12 байт (=> L=3, поле длины q=3 байта, лимит сообщения 16 МиБ);
 *   - без associated data (Adata=0) — протокол его не использует;
 *   - tagLength параметризуем (протокол использует 4 байта, не дефолтные 16).
 *
 * Совместимость проверена побайтово с Python `cryptography.AESCCM`
 * (см. APK_build/test/ccm_vectors.*).
 */

function concatBytes(...arrs) {
  const len = arrs.reduce((s, a) => s + a.length, 0);
  const out = new Uint8Array(len);
  let off = 0;
  for (const a of arrs) { out.set(a, off); off += a.length; }
  return out;
}

function zeroPad16(data) {
  const rem = data.length % 16;
  if (rem === 0) return data;
  return concatBytes(data, new Uint8Array(16 - rem));
}

async function importKey(subtle, rawKey, name) {
  return subtle.importKey("raw", rawKey, { name }, false, ["encrypt"]);
}

/** B0 (первый блок CBC-MAC) — флаги || nonce || q(длина plaintext, L байт BE). */
function buildB0(nonce, L, M, plaintextLen) {
  const flags = (((M - 2) / 2) << 3) | (L - 1); // Adata=0 => старший бит 0x40 не ставим
  const q = new Uint8Array(L);
  let n = plaintextLen;
  for (let i = L - 1; i >= 0; i--) { q[i] = n & 0xff; n = Math.floor(n / 256); }
  return concatBytes(new Uint8Array([flags]), nonce, q);
}

/** A0 (первый counter-блок CTR) — флаги' || nonce || 0..0 (L байт). */
function buildA0(nonce, L) {
  const flagsA = L - 1;
  return concatBytes(new Uint8Array([flagsA]), nonce, new Uint8Array(L));
}

async function cbcMac(subtle, rawKey, B0, paddedPlaintext) {
  const cbcKey = await importKey(subtle, rawKey, "AES-CBC");
  const macInput = concatBytes(B0, paddedPlaintext);
  const iv0 = new Uint8Array(16);
  const out = new Uint8Array(await subtle.encrypt({ name: "AES-CBC", iv: iv0 }, cbcKey, macInput));
  // WebCrypto's AES-CBC всегда добавляет PKCS7-паддинг (ещё один блок), даже
  // если вход уже кратен 16Б — поэтому настоящий CBC-MAC это ПРЕДпоследний
  // блок вывода, а не последний (CBC-цепочка идёт вперёд, лишний паддинг-блок
   // не влияет на шифртекст уже посчитанных блоков).
  return out.slice(out.length - 32, out.length - 16);
}

async function ctrKeystream(subtle, rawKey, A0, L, totalBytes) {
  const ctrKey = await importKey(subtle, rawKey, "AES-CTR");
  const dummy = new Uint8Array(totalBytes);
  return new Uint8Array(await subtle.encrypt(
    { name: "AES-CTR", counter: A0, length: L * 8 }, ctrKey, dummy));
}

/**
 * CCM-шифрование. Возвращает Uint8Array(ciphertext || tag), как
 * Python `AESCCM(key, tag_length=M).encrypt(nonce, plaintext, None)`.
 */
export async function ccmEncrypt(rawKey, nonce, plaintext, tagLength = 4, subtle = crypto.subtle) {
  if (nonce.length !== 12) throw new Error("ccmEncrypt: nonce должен быть 12 байт");
  const L = 15 - nonce.length; // = 3
  const M = tagLength;

  const B0 = buildB0(nonce, L, M, plaintext.length);
  const macFull = await cbcMac(subtle, rawKey, B0, zeroPad16(plaintext));
  const T = macFull.slice(0, M);

  const A0 = buildA0(nonce, L);
  const ks = await ctrKeystream(subtle, rawKey, A0, L, 16 + zeroPad16(plaintext).length);
  const S0 = ks.slice(0, 16);
  const Srest = ks.slice(16, 16 + plaintext.length);

  const U = new Uint8Array(M);
  for (let i = 0; i < M; i++) U[i] = T[i] ^ S0[i];

  const ct = new Uint8Array(plaintext.length);
  for (let i = 0; i < plaintext.length; i++) ct[i] = plaintext[i] ^ Srest[i];

  return concatBytes(ct, U);
}

/**
 * CCM-расшифровка с проверкой тега. Возвращает Uint8Array(plaintext) либо
 * null при неверном теге (аналог InvalidTag в Python).
 */
export async function ccmDecrypt(rawKey, nonce, ctAndTag, tagLength = 4, subtle = crypto.subtle) {
  if (nonce.length !== 12) throw new Error("ccmDecrypt: nonce должен быть 12 байт");
  const L = 15 - nonce.length;
  const M = tagLength;
  if (ctAndTag.length < M) return null;
  const ct = ctAndTag.slice(0, ctAndTag.length - M);
  const tag = ctAndTag.slice(ctAndTag.length - M);

  const A0 = buildA0(nonce, L);
  const ks = await ctrKeystream(subtle, rawKey, A0, L, 16 + zeroPad16(ct).length);
  const S0 = ks.slice(0, 16);
  const Srest = ks.slice(16, 16 + ct.length);
  const pt = new Uint8Array(ct.length);
  for (let i = 0; i < ct.length; i++) pt[i] = ct[i] ^ Srest[i];

  const B0 = buildB0(nonce, L, M, pt.length);
  const macFull = await cbcMac(subtle, rawKey, B0, zeroPad16(pt));
  const Tcomputed = macFull.slice(0, M);

  let ok = true;
  for (let i = 0; i < M; i++) {
    if ((Tcomputed[i] ^ S0[i]) !== tag[i]) ok = false;
  }
  return ok ? pt : null;
}
