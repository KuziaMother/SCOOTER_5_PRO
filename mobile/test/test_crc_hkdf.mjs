import { webcrypto } from "node:crypto";
import { readFileSync } from "node:fs";
import { crc32, hexToBytes, bytesToHex } from "../pwa/js/bin.js";

const subtle = webcrypto.subtle;
let failures = 0;

const crcVecs = JSON.parse(readFileSync(new URL("./crc32_vectors.json", import.meta.url)));
for (const [i, v] of crcVecs.entries()) {
  const got = crc32(hexToBytes(v.data));
  const ok = got === v.crc;
  if (!ok) failures++;
  console.log(`[crc32 ${i}] len=${v.data.length / 2} got=${got} want=${v.crc} ${ok ? "OK" : "FAIL"}`);
}

async function hkdf(keymix, saltStr, infoStr, lengthBytes) {
  const enc = new TextEncoder();
  const ikmKey = await subtle.importKey("raw", keymix, "HKDF", false, ["deriveBits"]);
  const okm = await subtle.deriveBits(
    { name: "HKDF", hash: "SHA-256", salt: enc.encode(saltStr), info: enc.encode(infoStr) },
    ikmKey,
    lengthBytes * 8
  );
  return new Uint8Array(okm);
}

const hkdfVecs = JSON.parse(readFileSync(new URL("./hkdf_vectors.json", import.meta.url)));
for (const [i, v] of hkdfVecs.entries()) {
  const got = await hkdf(hexToBytes(v.keymix), "smartcfg-login-salt", "smartcfg-login-info", 64);
  const ok = bytesToHex(got) === v.out;
  if (!ok) failures++;
  console.log(`[hkdf ${i}] ${ok ? "OK" : `FAIL got=${bytesToHex(got)} want=${v.out}`}`);
}

console.log(failures === 0 ? "\n=== ВСЕ ВЕКТОРЫ СОШЛИСЬ ===" : `\n=== ${failures} ОШИБОК ===`);
process.exit(failures === 0 ? 0 : 1);
