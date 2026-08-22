import { webcrypto } from "node:crypto";
import { readFileSync } from "node:fs";
import { ccmEncrypt, ccmDecrypt } from "../pwa/js/aes-ccm.js";

const subtle = webcrypto.subtle;
const hexToBytes = (h) => new Uint8Array(h.match(/.{1,2}/g)?.map((b) => parseInt(b, 16)) || []);
const bytesToHex = (b) => Array.from(b).map((x) => x.toString(16).padStart(2, "0")).join("");

const vectors = JSON.parse(readFileSync(new URL("./ccm_vectors.json", import.meta.url)));

let failures = 0;
for (const [i, v] of vectors.entries()) {
  const key = hexToBytes(v.key);
  const nonce = hexToBytes(v.nonce);
  const pt = hexToBytes(v.plaintext);
  const expectedCt = v.ciphertext;

  const ct = await ccmEncrypt(key, nonce, pt, v.tag_len, subtle);
  const ctHex = bytesToHex(ct);
  const encOk = ctHex === expectedCt;

  const dec = await ccmDecrypt(key, nonce, hexToBytes(expectedCt), v.tag_len, subtle);
  const decOk = dec !== null && bytesToHex(dec) === v.plaintext;

  const status = encOk && decOk ? "OK" : "FAIL";
  if (status === "FAIL") failures++;
  console.log(
    `[${i}] pt_len=${pt.length} tag=${v.tag_len} enc=${encOk ? "OK" : `FAIL (got ${ctHex}, want ${expectedCt})`} dec=${decOk ? "OK" : "FAIL"}  ${status}`
  );
}

// Проверка неверного тега -> должен вернуть null (аналог InvalidTag)
const v0 = vectors[1];
const tampered = hexToBytes(v0.ciphertext);
tampered[tampered.length - 1] ^= 0xff;
const shouldBeNull = await ccmDecrypt(hexToBytes(v0.key), hexToBytes(v0.nonce), tampered, v0.tag_len, subtle);
const tamperOk = shouldBeNull === null;
console.log(`[tamper-check] испорченный тег отклонён: ${tamperOk ? "OK" : "FAIL"}`);
if (!tamperOk) failures++;

console.log(failures === 0 ? "\n=== ВСЕ ВЕКТОРЫ СОШЛИСЬ ===" : `\n=== ${failures} ОШИБОК ===`);
process.exit(failures === 0 ? 0 : 1);
