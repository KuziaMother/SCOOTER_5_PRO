/** Мелкие бинарные хелперы — замена struct.pack/unpack из Python-версии. */

export function concatBytes(...arrs) {
  const len = arrs.reduce((s, a) => s + a.length, 0);
  const out = new Uint8Array(len);
  let off = 0;
  for (const a of arrs) { out.set(a, off); off += a.length; }
  return out;
}

export function u16le(n) {
  return new Uint8Array([n & 0xff, (n >> 8) & 0xff]);
}

export function u32le(n) {
  return new Uint8Array([n & 0xff, (n >> 8) & 0xff, (n >> 16) & 0xff, (n >> 24) & 0xff]);
}

export function readU16le(bytes, offset) {
  return bytes[offset] | (bytes[offset + 1] << 8);
}

export function readU32le(bytes, offset) {
  return (bytes[offset] | (bytes[offset + 1] << 8) | (bytes[offset + 2] << 16) | (bytes[offset + 3] << 24)) >>> 0;
}

export function bytesToHex(b) {
  return Array.from(b).map((x) => x.toString(16).padStart(2, "0")).join("");
}

export function hexToBytes(h) {
  return new Uint8Array((h.match(/.{1,2}/g) || []).map((b) => parseInt(b, 16)));
}

/** CRC32 (IEEE 802.3, zlib-совместимый) — сверено с zlib.crc32. */
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

export function crc32(bytes) {
  let c = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) {
    c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
  }
  return (c ^ 0xffffffff) >>> 0;
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
