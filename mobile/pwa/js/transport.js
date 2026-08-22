/**
 * BLE-транспорт и канальный протокол поверх Web Bluetooth — порт класса
 * Transport из dreame_auth.py. Структура и имена методов намеренно близки
 * к Python-оригиналу, чтобы дальнейшие правки протокола было легко сверять.
 *
 * Важное отличие от bleak: Web Bluetooth API не позволяет подключаться по
 * MAC-адресу напрямую (приватность браузера) — подключение всегда идёт через
 * системный диалог выбора устройства (`requestDevice`). Один раз выбранное
 * устройство браузер запоминает (getDevices() для уже разрешённых).
 */
import { AsyncQueue } from "./queue.js";
import { concatBytes, u16le, readU16le, bytesToHex, sleep } from "./bin.js";

export const FE95_UUID = "0000fe95-0000-1000-8000-00805f9b34fb";

export const CH_CONTROL = 0x0010;
export const CH_LOGIN = 0x0016;
export const CH_MCU = 0x001c;

export const A4 = 0xa4;
export const PKT_CTR = 0, PKT_ACK = 1, PKT_SINGLE = 2, PKT_SINGLE_ACK = 3, PKT_MNG = 4, PKT_MNG_ACK = 5;

/** Короткий 16-бит sid из полного 128-бит UUID (та же логика, что sid() в Python). */
export function sidOf(uuidStr) {
  const hex = uuidStr.replace(/-/g, "");
  return parseInt(hex.slice(0, 8), 16) & 0xffff;
}

function fullUuid(sid16) {
  return `0000${sid16.toString(16).padStart(4, "0")}-0000-1000-8000-00805f9b34fb`;
}

export class TransportError extends Error {}

export class Transport {
  constructor() {
    this.device = null;
    this.server = null;
    this.chars = new Map(); // sid -> BluetoothRemoteGATTCharacteristic
    this.rx = new AsyncQueue(); // {sid, bytes}
    this.lastCtrl = null; // последний ответ на 0x0010 (login-result)
    this.dmtu = 242;
    this.pkgNum = 6;
    this.onLog = null; // необязательный колбэк(text) для UI-лога
  }

  _log(msg) {
    if (this.onLog) this.onLog(msg);
  }

  /** Открывает системный диалог выбора устройства (нужен клик пользователя). */
  async requestDevice() {
    this.device = await navigator.bluetooth.requestDevice({
      filters: [{ services: [FE95_UUID] }],
      optionalServices: [FE95_UUID],
    });
    return this.device;
  }

  /** Подключиться к уже выбранному через requestDevice() устройству. */
  async connect() {
    if (!this.device) throw new TransportError("сначала requestDevice()");
    this.server = await this.device.gatt.connect();
    const service = await this.server.getPrimaryService(FE95_UUID);
    const chars = await service.getCharacteristics();
    this.chars = new Map();
    for (const c of chars) {
      this.chars.set(sidOf(c.uuid), c);
    }
    this._log(`[+] connected chars=${[...this.chars.keys()].sort((a, b) => a - b).map((k) => "0x" + k.toString(16).padStart(4, "0")).join(",")}`);

    for (const [sidVal, c] of this.chars) {
      const props = c.properties;
      if (props.notify || props.indicate) {
        try {
          await c.startNotifications();
          c.addEventListener("characteristicvaluechanged", (ev) => {
            const bytes = new Uint8Array(ev.target.value.buffer);
            this._onNotify(sidVal, bytes);
          });
        } catch (e) {
          this._log(`    [notify fail 0x${sidVal.toString(16)}] ${e}`);
        }
      }
    }
  }

  _onNotify(sidVal, bytes) {
    if (sidVal === CH_CONTROL) this.lastCtrl = bytes;
    this.rx.put([sidVal, bytes]);
    this._log(`    <<< 0x${sidVal.toString(16).padStart(4, "0")} ${bytesToHex(bytes)}`);
  }

  async write(sidVal, data, { response = false } = {}) {
    const char = this.chars.get(sidVal);
    if (!char) throw new TransportError(`нет характеристики 0x${sidVal.toString(16)}`);
    if (response) {
      if (char.writeValueWithResponse) await char.writeValueWithResponse(data);
      else await char.writeValue(data);
    } else {
      if (char.writeValueWithoutResponse) await char.writeValueWithoutResponse(data);
      else await char.writeValue(data);
    }
  }

  /** Читать GATT-характеристику напрямую (для 0x0004 версии и т.п.). */
  async readGatt(sidVal) {
    const char = this.chars.get(sidVal);
    if (!char) throw new TransportError(`нет характеристики 0x${sidVal.toString(16)}`);
    const dv = await char.readValue();
    return new Uint8Array(dv.buffer);
  }

  /** Собрать все notify в течение окна тишины (timeoutMs). */
  async drain(timeoutMs = 2500) {
    const out = [];
    while (true) {
      const item = await this.rx.get(timeoutMs);
      if (item === null) break;
      out.push(item);
    }
    return out;
  }

  async a4Handshake() {
    this.rx.clear();
    await this.write(CH_CONTROL, new Uint8Array([A4]));
    const got = await this.drain(3000);
    for (const [s, b] of got) {
      if (s === CH_LOGIN && b.length >= 6 && b[0] === 0 && b[1] === 0 && b[2] === PKT_MNG) {
        this.pkgNum = b[4];
        this.dmtu = b[5];
        const ack = concatBytes(new Uint8Array([0, 0, PKT_MNG_ACK, b[3]]), new Uint8Array([this.pkgNum, this.dmtu]));
        await this.write(CH_LOGIN, ack);
        await this.drain(1000);
        return true;
      }
    }
    this._log("    [!] MNG не получен");
    return false;
  }

  async waitAckFull(timeoutMs, charSid = CH_LOGIN) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      const item = await this.rx.get(deadline - Date.now());
      if (item === null) return [null, []];
      const [s, b] = item;
      if (s === charSid && b.length >= 4 && b[0] === 0 && b[1] === 0 && b[2] === PKT_ACK) {
        const status = b[3];
        const seqs = [];
        for (let i = 4; i + 1 < b.length; i += 2) seqs.push(readU16le(b, i));
        return [status, seqs];
      }
    }
    return [null, []];
  }

  async waitAckStatus(timeoutMs, charSid = CH_LOGIN) {
    return (await this.waitAckFull(timeoutMs, charSid))[0];
  }

  /**
   * Надёжная отправка сообщения каналом: CTR -> ждём start-ACK -> DATA*fc ->
   * reliable-цикл (00=готово, 05=resend списка seq). Порт send_stream().
   */
  async sendStream(channel, payload, { timeoutMs = 4000, charSid = CH_LOGIN, chunk = null, respData = false } = {}) {
    const chunkSize = chunk ?? this.dmtu - 2;
    const frames = [];
    for (let i = 0; i < payload.length; i += chunkSize) frames.push(payload.slice(i, i + chunkSize));
    if (frames.length === 0) frames.push(new Uint8Array(0));
    const fc = frames.length;

    this.rx.clear();
    const ctr = concatBytes(new Uint8Array([0, 0, PKT_CTR, channel]), u16le(fc));
    await this.write(charSid, ctr);
    const st0 = await this.waitAckStatus(timeoutMs, charSid);
    if (st0 === null) {
      this._log("    [!] нет start-ACK на CTR");
      return false;
    }

    const sendFrames = async (seqs) => {
      for (const i of seqs) {
        const dp = concatBytes(u16le(i), frames[i - 1]);
        await this.write(charSid, dp, { response: respData });
        if (!respData) await sleep(20);
      }
    };

    const all = [];
    for (let i = 1; i <= fc; i++) all.push(i);
    await sendFrames(all);

    for (let attempt = 0; attempt < 40; attempt++) {
      const [st, seqs] = await this.waitAckFull(timeoutMs, charSid);
      if (st === null) {
        this._log("    [!] нет ACK после DATA");
        return false;
      }
      if (st === 0x00) return true;
      if (st === 0x05 && seqs.length) await sendFrames(seqs);
    }
    this._log("    [!] reliable-цикл не завершился (много resend)");
    return false;
  }

  /** Приём сообщения (SINGLE или CTR+DATA*fc), с ACK. Порт recv_message_v2(). */
  async recvMessageV2(timeoutMs = 6000, charSids = CH_LOGIN) {
    const chars = Array.isArray(charSids) ? charSids : [charSids];
    const ackChar = chars[0];
    const deadline = Date.now() + timeoutMs;
    let fc = null;
    const frames = new Map();
    while (Date.now() < deadline) {
      const item = await this.rx.get(deadline - Date.now());
      if (item === null) break;
      const [s, b] = item;
      if (!chars.includes(s) || b.length < 3) continue;
      const seq = readU16le(b, 0);
      if (seq === 0) {
        const t = b[2];
        if (t === PKT_SINGLE) {
          const data = b.slice(4);
          await this.write(ackChar, new Uint8Array([0, 0, PKT_SINGLE_ACK, 0]));
          return data;
        }
        if (t === PKT_CTR) {
          fc = b.length >= 6 ? readU16le(b, 4) : b[4];
          await this.write(ackChar, new Uint8Array([0, 0, PKT_ACK, 1]));
        }
      } else {
        frames.set(seq, b.slice(2));
        if (fc && frames.size >= fc) {
          await this.write(ackChar, new Uint8Array([0, 0, PKT_ACK, 0]));
          break;
        }
      }
    }
    if (frames.size) {
      const keys = [...frames.keys()].sort((a, b) => a - b);
      return concatBytes(...keys.map((k) => frames.get(k)));
    }
    return null;
  }

  async disconnect() {
    if (this.server && this.server.connected) {
      this.server.disconnect();
    }
  }
}
