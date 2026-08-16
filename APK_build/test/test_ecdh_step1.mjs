import { webcrypto } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { hexToBytes, bytesToHex, concatBytes } from "../pwa/js/bin.js";

const subtle = webcrypto.subtle;
const setup = JSON.parse(readFileSync(new URL("./ecdh_setup.json", import.meta.url)));
const pubARaw = hexToBytes(setup.pub_a_raw); // 64B X||Y
const pubA65 = concatBytes(new Uint8Array([0x04]), pubARaw);

const pubAKey = await subtle.importKey("raw", pubA65, { name: "ECDH", namedCurve: "P-256" }, false, []);

const kpB = await subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]);
const pubB65 = new Uint8Array(await subtle.exportKey("raw", kpB.publicKey));
const pubBRaw = pubB65.slice(1); // 64B X||Y

const sharedBits = await subtle.deriveBits({ name: "ECDH", public: pubAKey }, kpB.privateKey, 256);
const sharedB = new Uint8Array(sharedBits);

writeFileSync(
  new URL("./ecdh_step1.json", import.meta.url),
  JSON.stringify({ pub_b_raw: bytesToHex(pubBRaw), shared_b: bytesToHex(sharedB) })
);
console.log("pubB:", bytesToHex(pubBRaw));
console.log("sharedB:", bytesToHex(sharedB));
