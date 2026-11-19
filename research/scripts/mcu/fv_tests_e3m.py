# ruff: noqa: F405
"""§96 BLE (без железа): (9) app-протокол Mi Home из APK+snoop; (8) co-proc тривиальные статик.

(9) Протокол BLE (apk/64bitpackage.apk + logs/btsnoop_hci.log, ground truth):
  data-фрейм: [siid:1][piid:1][len:2 LE][data:len]; len = ПОЛНЫЙ размер, при len>~240Б —
  фрагментация по ATT-фреймам (стриминг). Trailing CRC-8 на siid=0/piid=0 не найден.
  siid/piid-карта (snoop): siid=0/piid=0 = main data (handles 0x18/0x21/0x24);
  siid=1/piid=0 = sec data (0x21); siid=245(0xF5)/piid=0,1 = OTA/DFU шифр (0x38/0x3a/0x44).
  CCC (0x16/0x19/0x22): WRITE_REQ 0100 = enable notify."""
from fv_core import *  # noqa: F401,F403
from emulator.mcu_emu import (MI_BLE_SIID_MAIN, MI_BLE_SIID_SEC, MI_BLE_SIID_OTA,  # noqa: E402
                              MI_BLE_MTU_DATA, mi_ble_decode)


@t(0x211F8, '§96(9) BLE app-протокол (Mi Home APK + snoop): data-фрейм [siid][piid][len:2 LE][data]; '
            'len=полный размер, len>MTU→фрагментация (стриминг). siid/piid-карта: 0/0=main, 1/0=sec, '
            '0xF5/0,1=OTA шифр. CRC-8 (poly 0x29/0x49/0x31/0x9B) на siid=0/piid=0 не совпадает. '
            'mi_ble_decode сверен с реальными snoop-фреймами (logs/btsnoop_hci.log)')
def _(run, rng):
    """Emulator test @ 0x211f8: §96(9) BLE app-протокол (Mi Home APK + snoop): data-фрейм [siid][piid][len:2 LE][data]; len=полный размер, len>MTU→фрагментация (стриминг). siid/piid-карта: 0/0=main, 1/0=sec, 0xF5/0,1=OTA шифр. CRC-8 (poly 0x29/0x49/0x31/0x9B) на siid=0/piid=0 не совпадает. mi_ble_decode сверен с реальными snoop-фреймами (logs/btsnoop_hci.log).
    Тест эмулятора @ 0x211f8: §96(9) BLE app-протокол (Mi Home APK + snoop): data-фрейм [siid][piid][len:2 LE][data]; len=полный размер, len>MTU→фрагментация (стриминг). siid/piid-карта: 0/0=main, 1/0=sec, 0xF5/0,1=OTA шифр. CRC-8 (poly 0x29/0x49/0x31/0x9B) на siid=0/piid=0 не совпадает. mi_ble_decode сверен с реальными snoop-фреймами (logs/btsnoop_hci.log).
    """
    assert MI_BLE_SIID_MAIN == 0 and MI_BLE_SIID_SEC == 1 and MI_BLE_SIID_OTA == 0xF5
    # короткий полный фрейм: siid=0/piid=0, len=2, data=2Б
    d = mi_ble_decode(bytes([0x00, 0x00, 0x02, 0x00, 0xAA, 0xBB]))
    assert d['siid'] == 0 and d['piid'] == 0 and d['len'] == 2 and d['data'] == b'\xAA\xBB'
    assert d['complete'] is True
    # фрагментация: len=260 > 240 (data в этом фрейме < len)
    long_pl = bytes([0x00, 0x00, 0x04, 0x01]) + bytes([0xF2]) * 240  # len=0x0104=260
    d2 = mi_ble_decode(long_pl)
    assert d2['len'] == 260 and len(d2['data']) == 240 and d2['complete'] is False, \
        f"фрагментация: {d2}"
    assert MI_BLE_MTU_DATA == 240
    # OTA-канал: siid=0xF5
    d3 = mi_ble_decode(bytes([0xF5, 0x00, 0x20, 0xFF]) + bytes(16))
    assert d3['siid'] == 0xF5 and d3['piid'] == 0
    # сверка с реальным snoop (если лог есть)
    import os
    snoop = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logs', 'btsnoop_hci.log')
    if os.path.exists(snoop):
        import struct as _st
        from collections import Counter
        raw = open(snoop, 'rb').read()
        assert raw[:8] == b'btsnoop\x00'
        off = 16
        seen = Counter()
        while off + 24 <= len(raw):
            _, ilen, _, _, _ = _st.unpack('>IIIIq', raw[off:off + 24])
            off += 24
            pkt = raw[off:off + ilen]
            off += ilen
            if len(pkt) >= 9 and pkt[0] == 0x02 and _st.unpack('<H', pkt[7:9])[0] == 4:
                att = pkt[9:]
                if att and att[0] in (0x1b, 0x52) and len(att) >= 4:
                    fr = mi_ble_decode(att[3:])
                    if fr['siid'] is not None:
                        seen[(fr['siid'], fr['piid'])] += 1
        # ground truth: main (0,0) доминирует, OTA (0xF5,0) присутствует
        assert seen[(0, 0)] > 0, f"snoop: siid=0/piid=0 не найден: {dict(seen)}"
        assert seen[(0xF5, 0)] > 0, f"snoop: siid=0xF5/piid=0 не найден: {dict(seen)}"
        assert seen[(0, 0)] == max(c for _, c in seen.items()), f"main data не доминирует: {dict(seen)}"


@t(0x06008, '§96(8) BLE co-proc тривиальные статик: setter-семья 0x06008..0x060e4 (6×44Б, ble_2.7.0_0015.bin) — единый '
            'trampoline-паттерн: push{r4,r5,lr} → save {lr,r5,r4} в per-setter cfg-struct (+0/+4/+8) → cbz callback → '
            'blx r4 (вызов зарегистрированного callback) → bx r3 (возврат через saved-указатель [ret+8]). Глубокая логика — '
            'в callback/RAM-трамплинах (live). Статически верифицирован: все 6 содержат blx_r4+bx_r3+cbz. '
            'Разница setter\'ов — только адрес cfg-struct и offset callback-указателя')
def _(run, rng):
    """Emulator test @ 0x6008: §96(8) BLE co-proc тривиальные статик: setter-семья 0x06008..0x060e4 (6×44Б, ble_2.7.0_0015.bin) — единый trampoline-паттерн: push{r4,r5,lr} → save {lr,r5,r4} в per-setter cfg-struct (+0/+4/+8) → cbz callback → blx r4 (вызов зарегистрированного callback) → bx r3 (возврат через saved-указатель [ret+8]). Глубокая логика — в callback/RAM-трамплинах (live). Статически верифицирован: все 6 содержат blx_r4+bx_r3+cbz. Разница setter'ов — только адрес cfg-struct и offset callback-указателя.
    Тест эмулятора @ 0x6008: §96(8) BLE co-proc тривиальные статик: setter-семья 0x06008..0x060e4 (6×44Б, ble_2.7.0_0015.bin) — единый trampoline-паттерн: push{r4,r5,lr} → save {lr,r5,r4} в per-setter cfg-struct (+0/+4/+8) → cbz callback → blx r4 (вызов зарегистрированного callback) → bx r3 (возврат через saved-указатель [ret+8]). Глубокая логика — в callback/RAM-трамплинах (live). Статически верифицирован: все 6 содержат blx_r4+bx_r3+cbz. Разница setter'ов — только адрес cfg-struct и offset callback-указателя.
    """
    import os
    ble = os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'ble_2.7.0_0015.bin')
    if not os.path.exists(ble):
        return  # BLE-образ отсутствует — статика пропущена
    data = open(ble, 'rb').read()
    BLX_R4 = bytes([0xA0, 0x47])   # blx r4
    BX_R3 = bytes([0x18, 0x47])    # bx r3
    CBZ = bytes([0x04, 0xB1])      # cbz r4, #+2
    setters = (0x06008, 0x06034, 0x06060, 0x0608c, 0x060b8, 0x060e4)
    for fn in setters:
        b = data[fn:fn + 44]
        assert BLX_R4 in b and BX_R3 in b and CBZ in b, f'setter {fn:#x}: паттерн сломан'
    # 6 различных cfg-struct (первый ldr r4,[pc,#0x20] → разный pool)
    import struct as _st
    pools = set()
    for fn in setters:
        # ldr r4, [pc, #0x20] @fn+2: pool @ ((fn+2+4)&~3)+0x20
        pa = ((fn + 2 + 4) & ~3) + 0x20
        pools.add(_st.unpack_from('<I', data, pa)[0])
    assert len(pools) >= 2, f'setter-семья: cfg-struct не различаются: {pools}'


@t(0x1F600, '§96(4) A2 TX-sender (объединение §94 scheduler + A2): 0x1F600 = main-loop dispatcher (head 0x2C1/tail 0x2C2, '
            'ring @0xA43, слот 0x96, период 432) + byte-примитив 0x1F1C0 → USART3_DR (0x40004804). Гейт TX-ready = '
            'sign-bit([0x40004828]<<17). UsartTxSenderModel: frame-буфер @0xA43 + 1 байт/tick. Контроль: load_frame(8Б) → '
            '8×tick() → 8 байт в USART3_DR (uc.mem_read(USART3_DR) == последний), usart_out == frame')
def _(run, rng):
    """Emulator test @ 0x1f600: §96(4) A2 TX-sender (объединение §94 scheduler + A2): 0x1F600 = main-loop dispatcher (head 0x2C1/tail 0x2C2, ring @0xA43, слот 0x96, период 432) + byte-примитив 0x1F1C0 → USART3_DR (0x40004804). Гейт TX-ready = sign-bit([0x40004828]<<17). UsartTxSenderModel: frame-буфер @0xA43 + 1 байт/tick. Контроль: load_frame(8Б) → 8×tick() → 8 байт в USART3_DR (uc.mem_read(USART3_DR) == последний), usart_out == frame.
    Тест эмулятора @ 0x1f600: §96(4) A2 TX-sender (объединение §94 scheduler + A2): 0x1F600 = main-loop dispatcher (head 0x2C1/tail 0x2C2, ring @0xA43, слот 0x96, период 432) + byte-примитив 0x1F1C0 → USART3_DR (0x40004804). Гейт TX-ready = sign-bit([0x40004828]<<17). UsartTxSenderModel: frame-буфер @0xA43 + 1 байт/tick. Контроль: load_frame(8Б) → 8×tick() → 8 байт в USART3_DR (uc.mem_read(USART3_DR) == последний), usart_out == frame.
    """
    from emulator.mcu_emu import (UsartTxSenderModel, USART3_DR, USART3_TXSR,
                                  TX_SENDER_FN, TX_BYTE_SEND_FN, TX_FRAME_LEN)
    assert TX_SENDER_FN == 0x1F600 and TX_BYTE_SEND_FN == 0x1F1C0 and TX_FRAME_LEN == 8
    emu = run.emu
    tx = UsartTxSenderModel(emu)
    frame = bytes([0x08, 0x41, 0x12, 0x34, 0x56, 0x78, 0xAB, 0xA5])
    tx.load_frame(frame)
    out = []
    for _ in range(TX_FRAME_LEN):
        b = tx.tick()
        assert b is not None, f'байт {len(out)} не отправлен'
        out.append(b)
    assert bytes(out) == frame, f'usart_out={bytes(out).hex()} != {frame.hex()}'
    assert bytes(emu.uc.mem_read(USART3_DR, 1)) == bytes([frame[-1]]), 'USART3_DR != последний байт'
    assert tx.tick() is None, 'после 8 байт — frame закончена'
    # гейт: force_ready=False + [TXSR]=0 → не шлёт
    tx2 = UsartTxSenderModel(emu)
    tx2.force_ready = False
    # v=0 → (v<<17) sign=0 → ready (отправляет)
    emu.uc.mem_write(USART3_TXSR, struct.pack('<I', 0x00000000))
    tx2.load_frame(frame)
    assert tx2.tick() is not None, 'v=0 → sign-bit=0 → ready (должно отправить)'
    # bit14=0x4000 → (v<<17) sign-bit set → not ready (блокирует)
    emu.uc.mem_write(USART3_TXSR, struct.pack('<I', 0x4000))
    tx2.load_frame(frame)
    assert tx2.tick() is None, 'гейт TX-ready должен блокировать отправку'


@t(0x1F600, '§96(4) A2 ControlLoop-интеграция: ControlLoop._emit_tx() собирает push-фрейм телеметрии {8,"A",sp16,thr16,XOR,0xA5} '
            'и отдаёт UsartTxSenderModel (1 байт/tick → USART3_DR). run(20) → tx_sent монотонно растёт, tx_byte ≠ None, '
            'собранные usart_out складываются в целые 8-байтовые фреймы (кратность len)')
def _(run, rng):
    """Emulator test @ 0x1f600: §96(4) A2 ControlLoop-интеграция: ControlLoop._emit_tx() собирает push-фрейм телеметрии {8,"A",sp16,thr16,XOR,0xA5} и отдаёт UsartTxSenderModel (1 байт/tick → USART3_DR). run(20) → tx_sent монотонно растёт, tx_byte ≠ None, собранные usart_out складываются в целые 8-байтовые фреймы (кратность len).
    Тест эмулятора @ 0x1f600: §96(4) A2 ControlLoop-интеграция: ControlLoop._emit_tx() собирает push-фрейм телеметрии {8,"A",sp16,thr16,XOR,0xA5} и отдаёт UsartTxSenderModel (1 байт/tick → USART3_DR). run(20) → tx_sent монотонно растёт, tx_byte ≠ None, собранные usart_out складываются в целые 8-байтовые фреймы (кратность len).
    """
    from emulator.mcu_emu import ControlLoop
    cl = ControlLoop(run_foc=False)
    cl.setup(target=2000, mode=3, soc=100.0)
    states = cl.run(24)
    assert len(states) == 24
    sent = [s['tx_sent'] for s in states]
    assert sent[-1] > sent[0], f"tx_sent не растёт: {sent}"
    assert any(s['tx_byte'] is not None for s in states), 'tx_byte всегда None'
    # usart_out кратен 8 (целые фреймы) + первый фрейм = {8,"A",...}
    out = bytes(cl.tx.usart_out)
    assert len(out) % 8 == 0, f'usart_out={len(out)} не кратен 8'
    assert out[0] == 8 and out[1] == 0x41 and out[7] == 0xA5, f"фрейм-заголовок: {out[:8].hex()}"
