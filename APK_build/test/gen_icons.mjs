// Генератор простых плейсхолдер-иконок (сплошной тёмный фон + акцентный круг)
// без внешних зависимостей — PNG собирается вручную поверх встроенного zlib.
// Заменить на нормальную иконку перед реальным релизом (см. README).
import { deflateSync } from "node:zlib";
import { writeFileSync, mkdirSync } from "node:fs";

function crc32(buf) {
  let c;
  const table = crc32.table || (crc32.table = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      t[n] = c >>> 0;
    }
    return t;
  })());
  c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = table[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function chunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length, 0);
  const typeBuf = Buffer.from(type, "ascii");
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(Buffer.concat([typeBuf, data])), 0);
  return Buffer.concat([len, typeBuf, data, crc]);
}

function genPng(size, { bg = [10, 14, 20], fg = [79, 214, 255] } = {}) {
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 2; // color type RGB
  ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;

  const cx = size / 2, cy = size / 2, r = size * 0.32;
  const raw = Buffer.alloc(size * (1 + size * 3));
  let off = 0;
  for (let y = 0; y < size; y++) {
    raw[off++] = 0; // filter: none
    for (let x = 0; x < size; x++) {
      const d = Math.hypot(x - cx, y - cy);
      const [r8, g8, b8] = d <= r ? fg : bg;
      raw[off++] = r8; raw[off++] = g8; raw[off++] = b8;
    }
  }
  const idat = deflateSync(raw);
  return Buffer.concat([sig, chunk("IHDR", ihdr), chunk("IDAT", idat), chunk("IEND", Buffer.alloc(0))]);
}

mkdirSync(new URL("../pwa/icons", import.meta.url), { recursive: true });
for (const size of [192, 512]) {
  const png = genPng(size);
  writeFileSync(new URL(`../pwa/icons/icon-${size}.png`, import.meta.url), png);
  console.log(`icon-${size}.png: ${png.length} байт`);
}
