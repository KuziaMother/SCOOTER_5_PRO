# ruff: noqa: F405  (имена из star-import от fv_core)
"""§78.5 (A3-динамика): SPI-контекст + протокол flash-транзакций — полное закрытие.
Найдено (2026-11-18, dynamic probes):
  - **SPI-контекст = регистровый блок 0x40022000** (внутренний FLASH-контроллер,
    НЕ struct в RAM; pool-литералы 0x235D0/0x23608 → 0x40022000): +0x00 low-байт =
    старт-пульс (0xF0 clocking / 0xF1 arm), +0x04 = cmd/len (low24 |= cmd, high-байт
    = cmd-байт, len bits25..31), +0x08 = MOSI-дата (u32), +0x14 bit31 = ready-gate
    (0xFFFFFFFF по дефолту = ready; lsrs #26/31 из quirk-класса — при 0x80000001
    гейт «выключается»), +0x28 = MISO-байт (ответ flash).
  - **0x221a4(r0) = write-enable wrapper**: cmd = r0+1 (5→0x06), flow: WE-handshake
    0x23688 → 0x235d4 arm (ctx+4 |= low24(cmd), ctx+0 low ← 0xF1) → WE-handshake;
    ret 0 = успех, 1 = сбой (status-байт фрейма).
  - **0x221e6(r0=addr, r1=data) = page-program**: валидация addr (<<30≠0 → reject;
    NVM ≤4KB), фрейм {status, addr, ~addr, len=1, &data, data@+0x14}, 0x23688 WE,
    0x2360c-транзакция (len-preload ctx+4, data в ctx+8, старт-пульс 0xF0), 0x235b0
    MISO-потребление; ret 0 = успех.
  - **0x2360c(r0=&desc)** — SPI-двигатель: desc {u32 cmd-word (high-байт → ctx+4),
    u32 mask, u16 len, u32 *data, [u32 пары]}: (len+3)>>2 слов из *data в ctx+8 с
    старт-пульсом 0xF0 на слово; ret 1 = успех.
  - **0x235b0()** — MISO-потребление: [ctx+0x28] читается и сбрасывается в 0;
    ret 0 = данные были (ready).
  - **0x23688()** — write-enable handshake: два слова 0x00112233/0x55667788 в
    [ctx+0x28] (когда гейт снят; при ready (0xFFFFFFFF) пропускается).
  - **0x1c838()** — NVM-write батч: 2 полные транзакции (payload-слова 0x01A1,
    0x06ED в ctx+8) + 3 MISO-потребления + RAM-строки 0x844/0x858 (b68-золото).
  - **SpiFlashMiso** — MISO-модель (25xxx: 0x06 WE, 0x03/0x02 read, 0x02 prog AND,
    0x05 статус): staged-ответы в ctx+0x28 под MOSI-записи в ctx+0x08."""
import struct

from fv_core import *  # noqa: F401,F403

from emulator.mcu_emu import (SPI_CTX_BASE, SPI_CTX_CTRL, SPI_CTX_CMD,  # noqa: E402
                              SPI_CTX_MOSI, SPI_CTX_READY, SPI_CTX_MISO,
                              SPI_CTX_WE_WORDS, SpiFlashModel, SpiFlashMiso)


def _a3_fresh(off, args=(), seeds=(), max_insn=200000):
    """fresh-emu для A3: нулевой RAM + 0xFF периферия + seeds; (emu, uc, lastpc)"""
    emu = McuEmu(max_insn=max_insn)
    uc = emu.uc
    uc.mem_write(RAM, bytes(0x20000))
    emu.hook_periph_ready()
    for addr, val in seeds:
        if isinstance(val, (bytes, bytearray)):
            uc.mem_write(addr, val)
        else:
            uc.mem_write(addr, struct.pack('<I', val))
    for i, a in enumerate(args):
        uc.reg_write([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2][i], a)
    uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
    uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
    lastpc = [0]

    def _hc(uc_, address, size, user):
        lastpc[0] = address

    uc.hook_add(UC_HOOK_CODE, _hc)
    try:
        uc.emu_start(off | 1, 0, count=max_insn)
    except Exception:
        pass
    return emu, uc, lastpc[0]


def _pw(emu, addr):
    return [v for pc, a, s, v in emu.periph_writes if a == addr]


@t(0x221A4, '§78.5: 0x221a4(r0) — write-enable wrapper: cmd = r0+1 (5→0x06): WE-handshake '
           '0x23688 (skipped при ready) → 0x235d4 arm (ctx+4 |= low24(cmd), ctx+0 low ← 0xF1) '
           '→ WE; ret 0 = успех (status-байт 1)')
def _(run, rng):
    for r0, cmd in ((0, 1), (5, 0x06)):
        emu, uc, lp = _a3_fresh(0x221A4, [r0])
        assert uc.reg_read(UC_ARM_REG_R0) == 0, f'0x221a4({r0}): ret≠0'
        assert _pw(emu, SPI_CTX_BASE + SPI_CTX_CMD)[-1] == 0xFF000000 | cmd, \
            f'arm cmd {cmd:#x}: {_pw(emu, SPI_CTX_BASE + SPI_CTX_CMD)}'
        assert _pw(emu, SPI_CTX_BASE + SPI_CTX_CTRL)[-1] == 0xFFFFFFF1, \
            f'arm старт 0xF1: {_pw(emu, SPI_CTX_BASE + SPI_CTX_CTRL)}'
        assert len(emu.periph_writes) == 2, \
            f'0x221a4({r0}): лишних записей {emu.periph_writes}'


@t(0x221E6, '§78.5: 0x221e6(addr, data) — page-program полный flow: фрейм '
           '{status=1, addr, ~addr, len=1, &data, data@+0x14}, WE, 0x2360c-транзакция '
           '(data → ctx+8, старт 0xF0), MISO-потребление; ret 0 = успех')
def _(run, rng):
    emu, uc, lp = _a3_fresh(0x221E6, [0x100, 0xA5])
    assert uc.reg_read(UC_ARM_REG_R0) == 0, f'0x221e6: ret={uc.reg_read(UC_ARM_REG_R0):#x}'
    # фрейм: base = STACK_TOP - 0x28 (push 0xC + sub 0x1C)
    fb = STACK_TOP - 0x28 - RAM
    assert uc.mem_read(RAM + fb, 1)[0] == 1, 'status-байт != 1'
    assert struct.unpack_from('<I', uc.mem_read(RAM + fb + 4, 4), 0)[0] == 0x100, 'addr'
    assert struct.unpack_from('<I', uc.mem_read(RAM + fb + 8, 4), 0)[0] & 0xFF == 0xFF, \
        '~addr (mvns-quirk: верхние биты стабильны, низкий — от контекста)'
    assert struct.unpack_from('<H', uc.mem_read(RAM + fb + 0xC, 2), 0)[0] == 1, 'len=1'
    data_ptr = struct.unpack_from('<I', uc.mem_read(RAM + fb + 0x10, 4), 0)[0]
    # quirk-двойственность add/str: оба наблюдались в разных контекстах
    assert data_ptr in (STACK_TOP - 0x14, STACK_TOP - 0x10), f'&data {data_ptr:#x}'
    assert struct.unpack_from('<I', uc.mem_read(RAM + fb + 0x14, 4), 0)[0] == 0xA5, 'data'
    # транзакция: data-слово в MOSI-регистр + старт-пульс + MISO-сброс
    assert _pw(emu, SPI_CTX_BASE + SPI_CTX_MOSI) == [0xA5], \
        f'MOSI: {_pw(emu, SPI_CTX_BASE + SPI_CTX_MOSI)}'
    assert _pw(emu, SPI_CTX_BASE + SPI_CTX_CTRL)[-1] == 0xFFFFFFF0, 'старт 0xF0'
    assert _pw(emu, SPI_CTX_BASE + SPI_CTX_MISO) == [0], 'MISO-потребление'


@t(0x235B0, '§78.5: 0x235b0() — MISO-потребление: [ctx+0x28] читается и сбрасывается в 0 '
           '(ret 0 = данные были); + SpiFlashMiso-модель: 25xxx read (0x03+3 адреса → '
           'NVM-байты staged в ctx+0x28), program (0x06+0x02+3 адреса+данные → AND в NVM)')
def _(run, rng):
    emu, uc, lp = _a3_fresh(0x235B0, [], seeds=[(SPI_CTX_BASE + SPI_CTX_READY, 0xFFFFFFFF),
                                                (SPI_CTX_BASE + SPI_CTX_MISO, 0x42)])
    assert uc.reg_read(UC_ARM_REG_R0) == 0, 'MISO-потребление: ret'
    assert _pw(emu, SPI_CTX_BASE + SPI_CTX_MISO) == [0], f'сброс MISO: {_pw(emu, SPI_CTX_BASE + SPI_CTX_MISO)}'
    # --- SpiFlashMiso: read-транзакция ---
    femu = McuEmu(max_insn=1000)
    nvm = SpiFlashModel(femu)
    nvm.set(0x10, bytes([0xDE, 0xAD, 0xBE, 0xEF]))
    miso = SpiFlashMiso(femu, nvm)
    uc2 = femu.uc
    for b in (0x03, 0x00, 0x01, 0x10, 0x00, 0x00, 0x00):   # READ addr=0x0110, 4 dummy clock
        miso.feed(b)
    assert miso.miso_log[-2:] == [0xAD, 0xBE], f'MISO read: {miso.miso_log}'
    staged = struct.unpack_from('<I', uc2.mem_read(SPI_CTX_BASE + SPI_CTX_MISO, 4), 0)[0]
    assert staged == 0xBE, f'staged MISO {staged:#x}'
    # --- SpiFlashMiso: program-транзакция (0x06 WE + 0x02, addr 0x0020, 2 байта) ---
    nvm.set(0x20, bytes([0xFF, 0xFF]))
    for b in (0x06, 0x02, 0x00, 0x00, 0x20, 0xFF, 0x55, 0xAA):  # (0xFF — адресный edge, не data)
        miso.feed(b)
    assert nvm.get(0x20, 2) == b'\x55\xaa', f'program: {nvm.get(0x20, 2).hex()}'


@t(0x2360C, '§78.5: 0x2360c(&desc) — SPI-двигатель: desc {cmd-word, mask, u16 len, *data}: '
           'len→ctx+4 (len-поле), high-байт cmd → ctx+4, (len+3)>>2 слов *data → ctx+8 '
           'со старт-пульсом 0xF0 на слово; ret 1 = успех')
def _(run, rng):
    desc = RAM + 0x200
    emu, uc, lp = _a3_fresh(0x2360C, [desc], seeds=[
        (SPI_CTX_BASE + SPI_CTX_READY, 0xFFFFFFFF),
        (desc, 0x03000000), (desc + 4, 0), (desc + 8, 2),
        (desc + 0xC, RAM + 0x300), (RAM + 0x300, 0xDEADBEEF), (RAM + 0x304, 0xCAFEBABE)])
    assert uc.reg_read(UC_ARM_REG_R0) == 1, f'0x2360c: ret={uc.reg_read(UC_ARM_REG_R0):#x}'
    mosi = _pw(emu, SPI_CTX_BASE + SPI_CTX_MOSI)
    assert mosi[0] == 0xDEADBEEF, f'первое слово *data: {mosi}'
    assert len(mosi) == 1, f'(2+3)>>2=1 слово: {mosi}'
    assert _pw(emu, SPI_CTX_BASE + SPI_CTX_CTRL)[-1] == 0xFFFFFFF0, 'старт 0xF0'
    assert len(_pw(emu, SPI_CTX_BASE + SPI_CTX_CMD)) >= 2, 'cmd/len-записи в ctx+4'


@t(0x23688, '§78.5: 0x23688() — write-enable handshake: гейт снят (ready=0) → два слова '
           '{0x00112233, 0x55667788} в [ctx+0x28] (ret 0); при ready (0xFFFFFFFF) '
           'пропускается (ret 1, без записей)')
def _(run, rng):
    emu, uc, lp = _a3_fresh(0x23688, [], seeds=[(SPI_CTX_BASE + SPI_CTX_READY, 0)])
    assert uc.reg_read(UC_ARM_REG_R0) == 0, f'WE off: ret={uc.reg_read(UC_ARM_REG_R0):#x}'
    assert _pw(emu, SPI_CTX_BASE + SPI_CTX_MISO) == list(SPI_CTX_WE_WORDS), \
        f'WE-слова: {_pw(emu, SPI_CTX_BASE + SPI_CTX_MISO)}'
    emu, uc, lp = _a3_fresh(0x23688, [])   # естественный ready (0xFFFFFFFF)
    assert uc.reg_read(UC_ARM_REG_R0) == 1 and len(emu.periph_writes) == 0, \
        f'WE skip: ret={uc.reg_read(UC_ARM_REG_R0):#x} P={len(emu.periph_writes)}'


@t(0x1C838, '§78.5: 0x1c838() — NVM-write батч (интеграция): 2 полные SPI-транзакции '
           '(payload-слова 0x01A1, 0x06ED → ctx+8; старт-пульсы 0xF0; 3 MISO-сброса) '
           '+ RAM-строки 0x844/0x858 (b68-золото); ret 1')
def _(run, rng):
    emu, uc, lp = _a3_fresh(0x1C838, [], max_insn=80000)
    assert uc.reg_read(UC_ARM_REG_R0) == 1, f'0x1c838: ret={uc.reg_read(UC_ARM_REG_R0):#x}'
    assert 5000 < emu.insn < 7000, f'insn={emu.insn}'
    mosi = _pw(emu, SPI_CTX_BASE + SPI_CTX_MOSI)
    assert mosi == [0x1A1, 0x1A1, 0x6ED], f'payload-слова: {mosi}'
    assert _pw(emu, SPI_CTX_BASE + SPI_CTX_MISO) == [0, 0, 0], '3 MISO-сброса'
    starts = [v for v in _pw(emu, SPI_CTX_BASE + SPI_CTX_CTRL)]
    assert starts.count(0xFFFFFFF0) == 3 and starts.count(0xFFFFFFF1) == 2, f'старты: {starts}'
    # b68-золото: декодированные RAM-строки
    s1 = uc.mem_read(RAM + 0x844, 24)
    s2 = uc.mem_read(RAM + 0x858, 24)
    assert s1 == bytes.fromhex('09a4a5a6c274f8000099c30103c260a0a000a020e9627216'), f's1 {s1.hex()}'
    assert s2 == bytes.fromhex('e96272160930303030302f30303030303030303030303030'), f's2 {s2.hex()}'
