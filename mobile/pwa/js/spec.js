/**
 * MIoT-spec протокол поверх session-шифрования (AES-CCM) — порт
 * probes/spec_read.py (GET) + webui/ble_worker.py (SET, op=0) +
 * ИСПРАВЛЕННОГО разбора ответа (см. docs/FACTS.md: ошибочная запись
 * объекта — ровно 5 байт, без tl/value; это чинилось в этой же сессии
 * в probes/spec_read.py:parse_reply).
 */
import { concatBytes, u16le, u32le, readU16le, sleep } from "./bin.js";
import { ccmEncrypt, ccmDecrypt } from "./aes-ccm.js";

export const CH_WRITE = 0x001a;
export const CH_NOTIFY = 0x001b;
export const SPEC_CHANNEL = 0; // подтверждено снупом (НЕ 6, как одна из ранних гипотез по дизасму)

/** Кадр spec (GET, если value=null; SET, если value задан). op: 2=GET, 0=SET, 5=ACTION. */
export function buildSpecFrame(objects, { tid = 1, op = 2 } = {}) {
  const parts = objects.map(({ siid, piid, typeCode = 0, value = null }) => {
    const vlen = value ? value.length : 0;
    const tl = (((typeCode & 0xf) << 12) | (vlen & 0xfff)) & 0xffff;
    const head = concatBytes(new Uint8Array([siid & 0xff]), u16le(piid & 0xffff), u16le(tl));
    return value ? concatBytes(head, value) : head;
  });
  const body = concatBytes(...parts);
  const total = 6 + body.length;
  const header = concatBytes(
    u16le((total | 0x2000) & 0xffff),
    u16le(tid & 0xffff),
    new Uint8Array([op & 0xff, objects.length & 0xff])
  );
  return concatBytes(header, body);
}

/** Разбор ответа: [siid][piid u16][status u16] + (если status===0) [tl u16][value]. */
export function parseSpecPayload(pt) {
  if (!pt || pt.length < 6) return { objects: [], op: null };
  const op = pt[4];
  const count = pt[5];
  let off = 6;
  const objects = [];
  for (let i = 0; i < count; i++) {
    if (off + 5 > pt.length) break;
    const siid = pt[off];
    const piid = readU16le(pt, off + 1);
    const status = readU16le(pt, off + 3);
    if (status !== 0) {
      objects.push({ siid, piid, status, tcode: null, value: null });
      off += 5;
      continue;
    }
    if (off + 7 > pt.length) break;
    const tl = readU16le(pt, off + 5);
    const tcode = tl >> 12;
    const vlen = tl & 0x0fff;
    const value = pt.slice(off + 7, off + 7 + vlen);
    off += 7 + vlen;
    objects.push({ siid, piid, status: 0, tcode, value });
  }
  return { objects, op };
}

/**
 * Разбор ОТВЕТА НА SET — отдельно от parseSpecPayload (GET). У SET-ack
 * объект ВСЕГДА ровно 5 байт (siid+piid+status), даже при status===0 —
 * value не эхается обратно (в отличие от GET, где status===0 добавляет
 * ещё tl+value). Смешивать эти два парсера нельзя: на SET-ответе
 * `0b20010001010202000000` (успех, status=0) GET-парсер теряет объект
 * целиком, пытаясь дочитать несуществующие tl/value (проверено тестом).
 */
export function parseSetResponse(pt) {
  if (!pt || pt.length < 6) return { objects: [], op: null };
  const op = pt[4];
  const count = pt[5];
  let off = 6;
  const objects = [];
  for (let i = 0; i < count; i++) {
    if (off + 5 > pt.length) break;
    const siid = pt[off];
    const piid = readU16le(pt, off + 1);
    const status = readU16le(pt, off + 3);
    objects.push({ siid, piid, status });
    off += 5;
  }
  return { objects, op };
}

/** Значение по коду типа (как decode_value в Python). type 9 = FLOAT32. */
export function decodeValue(tcode, val) {
  if (!val || !val.length) return null;
  if (tcode === 9 && val.length === 4) {
    return new DataView(val.buffer, val.byteOffset, 4).getFloat32(0, true);
  }
  if (tcode === 10) return new TextDecoder().decode(val);
  const signed = tcode === 2 || tcode === 4 || tcode === 6 || tcode === 8;
  let n = 0n;
  for (let i = val.length - 1; i >= 0; i--) n = (n << 8n) | BigInt(val[i]);
  if (signed) {
    const bits = BigInt(val.length * 8);
    const max = 1n << (bits - 1n);
    if (n >= max) n -= 1n << bits;
  }
  return Number(n);
}

async function encApp(sk, cnt, frame, subtle) {
  const nonce = concatBytes(sk.slice(36, 40), new Uint8Array(4), u32le(cnt));
  const ct = await ccmEncrypt(sk.slice(16, 32), nonce, frame, 4, subtle);
  return concatBytes(u16le(cnt & 0xffff), ct);
}

async function decDev(sk, cnt, ct, subtle) {
  const nonce = concatBytes(sk.slice(32, 36), new Uint8Array(4), u32le(cnt));
  return ccmDecrypt(sk.slice(0, 16), nonce, ct, 4, subtle); // null при неверном теге
}

/**
 * Единая транспортная петля GET/SET: CTR -> ждём start-ACK(01)/pull(05) ->
 * шлём кадры -> ждём CTR-ответ устройства -> собираем/ACK'аем -> расшифровка.
 * Одна попытка, без повторов (§4 методики проекта — не спамить устройство).
 */
export async function specTxn(transport, sk, frame, appCnt, { timeoutMs = 8000, frameSize = 18, subtle = crypto.subtle } = {}) {
  const payload = await encApp(sk, appCnt, frame, subtle);
  const frames = [];
  for (let i = 0; i < payload.length; i += frameSize) frames.push(payload.slice(i, i + frameSize));
  if (!frames.length) frames.push(new Uint8Array(0));

  transport.rx.clear();
  await transport.write(CH_WRITE, concatBytes(new Uint8Array([0, 0, 0x00, SPEC_CHANNEL]), u16le(frames.length)));

  const sendSeq = async (n) => {
    if (n >= 1 && n <= frames.length) await transport.write(CH_WRITE, concatBytes(u16le(n), frames[n - 1]));
  };

  const deadline = Date.now() + timeoutMs;
  let sentAll = false;
  while (Date.now() < deadline) {
    const item = await transport.rx.get(deadline - Date.now());
    if (item === null) break;
    const [s, b] = item;

    if (b.length >= 3 && b[0] === 0 && b[1] === 0 && b[2] === 0x01) {
      const st = b.length > 3 ? b[3] : null;
      if (st === 0x01 && !sentAll) {
        sentAll = true;
        for (let n = 1; n <= frames.length; n++) {
          await sendSeq(n);
          await sleep(30);
        }
      } else if (st === 0x05) {
        for (let i = 4; i + 1 < b.length; i += 2) {
          await sendSeq(readU16le(b, i));
          await sleep(30);
        }
      }
      continue;
    }

    if (b.length >= 6 && b[0] === 0 && b[1] === 0 && b[2] === 0x00 && s === CH_NOTIFY) {
      const fc = readU16le(b, 4);
      await transport.write(CH_NOTIFY, new Uint8Array([0, 0, 0x01, 0x01])); // готовы принимать
      const parts = new Map();
      const rdl = Date.now() + 6000;
      while (parts.size < fc && Date.now() < rdl) {
        const item2 = await transport.rx.get(rdl - Date.now());
        if (item2 === null) break;
        const [s2, b2] = item2;
        if (s2 === CH_NOTIFY && b2.length >= 2) {
          const seq = readU16le(b2, 0);
          if (seq >= 1 && seq <= fc) parts.set(seq, b2.slice(2));
        }
      }
      await transport.write(CH_NOTIFY, new Uint8Array([0, 0, 0x01, 0x00])); // принято
      if (parts.size !== fc) return null;
      const keys = [...parts.keys()].sort((a, b2) => a - b2);
      const payload2 = concatBytes(...keys.map((k) => parts.get(k)));
      const devCnt = readU16le(payload2, 0);
      const ct = payload2.slice(2);
      try {
        return await decDev(sk, devCnt, ct, subtle);
      } catch (e) {
        return null;
      }
    }
  }
  return null;
}

/** Чтение одного свойства (устройство обслуживает только первый объект в запросе). */
export async function specGet(transport, sk, siid, piid, appCnt, { tid = 1, typeCode = 0, timeoutMs = 8000, subtle = crypto.subtle } = {}) {
  const frame = buildSpecFrame([{ siid, piid, typeCode }], { tid, op: 2 });
  const pt = await specTxn(transport, sk, frame, appCnt, { timeoutMs, subtle });
  if (!pt) return null;
  const { objects } = parseSpecPayload(pt);
  return objects.find((o) => o.siid === siid && o.piid === piid) || objects[0] || null;
}

/** Запись одного свойства (op=0). Возвращает {ok, status}. */
export async function specSet(transport, sk, siid, piid, typeCode, value, appCnt, { tid = 1, timeoutMs = 8000, subtle = crypto.subtle } = {}) {
  const frame = buildSpecFrame([{ siid, piid, typeCode, value }], { tid, op: 0 });
  const pt = await specTxn(transport, sk, frame, appCnt, { timeoutMs, subtle });
  if (!pt) return { ok: false, status: null };
  const { objects } = parseSetResponse(pt);
  const obj = objects.find((o) => o.siid === siid && o.piid === piid) || objects[0];
  if (!obj) return { ok: false, status: null };
  return { ok: obj.status === 0, status: obj.status };
}
