#!/usr/bin/env python3
"""
Инструкционный эмулятор прошивки MCU (Unicorn) — исполняет РЕАЛЬНЫЙ код mcu_0007.bin.

В отличие от emulator/ (поведенческая модель протокола), это исполнение настоящих
ARM Thumb-инструкций контроллера. Цель — пробить «стену рантайм-RAM»: запустить код,
дать ему инициализировать свои таблицы в RAM и/или перехватить, что он пишет в USART3
(реальные ID/кадры команд, которых нет в статике).

Границы честно: у нас только APP-регион OTA (нет вектор-таблицы/boot), периферия
заглушена (status-регистры отдают «готов»), поэтому это ФУНКЦИОНАЛЬНАЯ эмуляция
(вызов конкретной функции с поднятым состоянием), а не boot-from-reset.

Запуск:  python emulator/mcu_emu.py --func 0x1f600 [--max 200000] [--trace]
"""
import argparse
import os
import struct

from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE,
                     UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ,
                     UC_HOOK_MEM_UNMAPPED, UcError)
from unicorn.arm_const import (UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
                               UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_R4)

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.join(os.path.dirname(HERE), "research", "images", "mcu_0007.bin")

FLASH0 = 0x00000000          # база 0 (адрес == смещение в файле)
FLASH1 = 0x08000000          # зеркало (некоторые литералы могут ждать эту базу)
RAM = 0x20000000
RAM_SIZE = 0x20000           # 128K
PERIPH = 0x40000000
PERIPH_SIZE = 0x00100000
# §59.3: расширенная область периферии чипа (блоки 0x48000400 DMA-подобный,
# 0x48000C00 GPIO-подобный; используют 0x1D640/0x1BF48/0x1C040)
PERIPH2 = 0x48000000
PERIPH2_SIZE = 0x00020000
SYS = 0xE0000000             # Cortex-M NVIC/SCB
SYS_SIZE = 0x00100000
STACK_TOP = 0x20018000

# A7 (§93): карта регистров периферии — машиночитаемый референс нестандартной раскладки
# (консолидация фактов §48/§49/§50/§76/§78.5/§89/§91). Блок → {offset: смысл}.
PERIPH_REG_MAP = {
    0x40021000: ("RCC", {
        0x00: "CTLR: HSE bit 0x10000, PLLSRC bits[19:18], HSION (0xc518), SW (0xc60c)",
        0x04: "CFGR0: AHB-прескалер bits[1:0] (0xc894), PLL-конфиг (0x11cb4)",
        0x10: "clock I2C1 (bit 1<<21) / 0xc684 set/clear",
        0x14: "0xc624 set/clear",
        0x18: "BDCR: 0xc6a4 set/clear; I2C?",
        0x1c: "0xc664 set/clear; power-стадия bit22 (0x2e0c); 0x11cb4 |= 0x10000000",
        0x24: "0x11cb4 |= 4",
        0x28: "0xc644 set/clear; DMA1/AHB clock bit12 = base>>18 (0x17f4); 0x11cb4 |= 4",
        0x2c: "0x11cb4 = 0",
        0x30: "0x11cb4 = 0x3800",
        0x34: "0x11cb4 = 0",
        0x40: "HSE ready flag (bit0); 0x11cb4 = 0; [0x40007000]&0x400",
        0x60: "set/clear (RCC-семья §49.2)",
    }),
    0x40022000: ("FLASH-контроллер (OTA) + SPI-контекст (A3)", {
        0x00: "KEYR: magic 0x45670123/0xCDEF89AB (0x6378); SPI: start-pulse low (0xF0/0xF1)",
        0x0c: "SR: 0x61d4 |= r0 (сброс флагов)",
        0x10: "CTLR: bit1=erase, bit6(0x40)=start (0x6230); SPI: cmd/len",
        0x14: "ADDR (erase); SPI: ready-gate bit31 (0xFFFFFFFF=ready)",
        0x28: "SPI: MISO (0x235b0 читает/сбрасывает)",
    }),
    0x40012C00: ("TIM1 (advanced) — 3-фазный компл. ШИМ BLDC-мотора", {
        0x1c: "bit31 (timer IRQ 0x1a2a4)",
        0x54: "CCR-подобный (0x1a2a4 &= )",
    }),
    0x40014000: ("timer-кластер (вспом. ШИМ) — 0x40014000/4400/4800/4C00", {}),
    0x40000400: ("TIM3", {}),
    0x40000800: ("TIM4", {}),
    0x40012400: ("ADC1 (токи фаз, АКБ, ручка газа, темп.)", {
        0x18: "биты 3/5: 0x1a5c4 |= 8, 0x1a5d4 |= 0x20",
        0xff: "ch9: wait [base+0xFF]==0x40012450 (0x1c1ac)",
    }),
    0x40013800: ("USART1 (BLE-чип)", {
        0x0c: "RCC-пульс 0x1302c (бит 0x4000)",
        0x3c: "SR (НЕ F1-class)",
        0x40: "ICER (НЕ F1-class)",
    }),
    0x40004800: ("USART3 (BLE-чип; RX-протокол 0x1e9e0)", {
        0x04: "DR: 0x1f1c0 пишет байт команды",
        0x10: "RCC-пульс 0x1302c (бит 0x40000)",
        0x3c: "SR (НЕ F1-class)",
        0x40: "ICER (НЕ F1-class)",
    }),
    0x40004400: ("USART2 (BMS/дисплей)", {
        0x10: "RCC-пульс 0x1302c (бит 0x20000)",
    }),
    0x40015000: ("UART4", {0x0c: "RCC-пульс 0x1302c (бит 0x20000)"}),
    0x40015400: ("UART5", {0x0c: "RCC-пульс 0x1302c (бит 0x40000)"}),
    0x40005400: ("I2C1 (датчики/EEPROM; B1 power-стадия 1)", {}),
    0x40005800: ("I2C2 (внешний чип dev 0x3E; B1 power-стадия 2)", {}),
    0x40013000: ("SPI1 (внешний чип; команда 0xB9; НЕ стандартная база)", {}),
    0x40013C00: ("SPI2", {}),
    0x40020000: ("DMA1 (ADC/USART-потоки)", {
        0x800: "канал-блок (0x40020800)",
        0x84c: "ch1 SR? (struct 0x1670)",
    }),
    0x40002800: ("WWDG (оконный watchdog = таймер событий с BCD-окном)", {
        0x00: "CR (0xccbc-декодер)",
        0x04: "CFR: BCD-время (0xcc1c-декодер)",
        0x08: "RER: refresh-данные (0xcd0c)",
        0x0c: "SR: bit5 (0xcc08 &=~0x80; 0xce70 poll)",
        0x10: "bit2 poll (0xcb40)",
        0x24: "magic 0xCA/0x53 → window (0xce70/0xcd80)",
        0x50: "status >>16 (0xcc68)",
    }),
    0x40003000: ("кастомный блок (свободен в F1/GD32F103 — GD32-ext/нестандартный кристалл)", {
        0x00: "магия 0xAAAA (0x99f0/0x5cc0) / 0xCCCC (0x99e0); r0 (0x9a0c)",
        0x04: "r0 (0x9a00)",
        0x08: "r0 (0x99d4)",
    }),
    0x40010800: ("GPIOA (F1-раскладка: CRL+0/CRH+0xC/IDR+0x10/ODR+0x14/BRR+0x18/BSRR+0x1C/LCKR+0x20)", {
        0x18: "BRR: init 0x10 (0x8348), 4 (0x5b98)",
        0x28: "init 0x10 (0x8348)",
    }),
    0x40010C00: ("GPIOB (F1-раскладка; state machine 0x4344)", {}),
    0x40011000: ("GPIOC (F1-раскладка)", {}),
    0x40011400: ("GPIOD (F1-раскладка)", {}),
    0x40010000: ("AFIO", {
        0x04: "MAPR: remap 0x8588 (idx=arg1>>2, p=arg1&3)",
        0x414: "EXTI line-mapping: 0x5970; 0x5908 (0x80/0x100/0x200); 0x30a6/0x32f4 (=0x80)",
    }),
    0x40007000: ("кастомный handshake/ready-блок (sleep 0xc2a8)", {
        0x00: "режим сна (&~7)|2",
        0x08: "|= r1",
        0x10: "bit9/2 ready (poll &2)",
    }),
    0x40001820: ("clock-switch цель (0x11cb4 хвост)", {}),
    0x48000000: ("кастомный GPIO-блок «портов» (PERIPH2; §76 GpioModel; F4-подобный)", {
        0x00: "IDR: input-data (read-only; бит N = состояние пина N; §96: 0x1BF24 читает [port1+0x00], пины 6-8 = 3-bit iron-вход)",
        0x2c: "MODER: ВСЕ 16 пинов, 2 бита/пин (pin N → биты [2N+1:2N])",
        0x28: "MODER_HI (AF/напр.)",
        0x10: "OUTSEL",
    }),
    0xE000E010: ("SysTick CTRL (0xE000E010/0x14 LOAD/0x18 VAL)", {}),
    0xE000E400: ("NVIC (база ЭТОГО чипа = 0xE000E400, НЕ 0xE000E100!)", {
        0x00: "priority [0xE000E400+irq] (0xc0b4); ISER[0] |= 1<<9 (0x1c1ac)",
    }),
    0xE000ED00: ("SCB", {
        0x0c: "CFSR: bits 0x700 = приоритет-группа (0xc0b4)",
        0x10: "SCR: bit2 SLEEPDEEP (0xc2a8)",
        0x88: "0x11cb4 |= 0xF00000",
    }),
}
# RCC set/clear-семья (0xC6xx): offset → функция (gap 0xC63E..0xC684 = 0xC644/0xC664)
RCC_SETCLEAR_FAMILY = {
    0x00: 0xC60C, 0x14: 0xC624, 0x28: 0xC644, 0x1c: 0xC664, 0x10: 0xC684, 0x18: 0xC6A4,
}
HSE_MHZ = 20  # HSE-кварц: 0x7A1200 = 20 МГц (0xc708)


class PeriphRegMap:
    """A machine-readable view of the PERIPH_REG_MAP register map (A7, section 93).
    `base(name_or_base)` -> the base address; `block(base)` -> (name, {off:desc});
    `rcc_setclear()` -> the set/clear family; cross-check against the emulation's
    peripheral writes.
    A7 (§93): доступ к машиночитаемой карте регистров PERIPH_REG_MAP.
    `base(name_or_base)` → базовый адрес; `block(base)` → (name, {off:desc});
    `rcc_setclear()` → семья set/clear; сверка с periph-записями эмуляции."""

    def __init__(self, emu=None):
        """Bind the view to an optional emulator instance.
        Привязка к необязательному экземпляру эмулятора."""
        self.emu = emu

    @staticmethod
    def block(base):
        """The register block for the base address: (name, {offset: description}).
        Блок регистров по базовому адресу: (name, {offset: description})."""
        return PERIPH_REG_MAP.get(base & ~0xFF)

    @staticmethod
    def base_of(name_sub):
        """The base address by the (partial) block name; None if not found.
        Базовый адрес по (частичному) имени блока; None если не найдено."""
        for base, (nm, _) in PERIPH_REG_MAP.items():
            if name_sub.lower() in nm.lower():
                return base
        return None

    def touched_bases(self):
        """The bases from the emulation's peripheral writes that are present in the map.
        Базы из periph-записей эмуляции, присутствующие в карте."""
        if not self.emu:
            return []
        out = []
        for _, addr, _, _ in self.emu.periph_writes:
            b = addr & ~0xFF
            if b in PERIPH_REG_MAP and b not in out:
                out.append(b)
        return sorted(out)


USART3_DR = 0x40004804       # куда 0x1f1c0 пишет байт команды
USART3_BASE = 0x40004800
USART3_TXSR = 0x40004828     # TX-status/gate: [base+0x28]<<17 sign-bit = TX-ready (гейт отправки, §96)
# §96: TX-sender — ОБЪЕДИНЕНИЕ §94 «scheduler» + A2 TX-отправитель: 0x1F600 = main-loop
# dispatcher (head 0x2C1 / tail 0x2C2, как §94; ring-база @0xA43, слот 0x96, период 432).
# При dispatch слота байты фрейма отправляются по одному через 0x1F1C0 → USART3_DR.
TX_SENDER_FN = 0x1F600       # main-loop dispatcher (== «scheduler» §94; head 0x2C1/tail 0x2C2)
TX_BYTE_SEND_FN = 0x1F1C0    # byte-примитив: str r0,[USART3_BASE+4] → USART3_DR
TX_FRAME_BASE = 0xA43        # frame-база (ring @0xA43 = beacon-таблица; §77 TX-ring)
TX_FRAME_LEN = 8             # длина фрейма в TX-sender (0x1F664: r5=#8)
TX_HEAD_OFF = 0x2C1          # head (producer) — совпадает с §94
TX_TAIL_OFF = 0x2C2          # tail/slot_idx (consumer) — совпадает с §94

# §73: моторный таймер PWM = «TIMER_A» из каталога §60/§60.2 (подфункции FOC
# 0x1be1c/0x1bd88). Обнаружен/подтверждён трассой полного входа FOC 0x1a938
# (блок @0x1bde0-0x1bdfc). Блок регистров 0x40012c00..0x40012c54; данные/статус —
# на sub-base 0x40012c40 (это и есть «TIMER_A» каталога), CTRL — на base+0x30.
MOTOR_TIM_BASE = 0x40012c00
MOTOR_TIM_CTRL = MOTOR_TIM_BASE + 0x30    # FOC: ldr/ands #0xDFFF/str → clear бит 13
MOTOR_TIM_DATA0 = MOTOR_TIM_BASE + 0x44   # = TIMER_A+4;  ← u16[RAM+0x386] (PWM duty)
MOTOR_TIM_DATA1 = MOTOR_TIM_BASE + 0x48   # = TIMER_A+8;  ← u16[RAM+0x384]
MOTOR_TIM_DATA2 = MOTOR_TIM_BASE + 0x4c   # = TIMER_A+0xc;← u16[RAM+0x382]
MOTOR_TIM_STAT = MOTOR_TIM_BASE + 0x54    # = TIMER_A+0x14; read (бит15 low16 = гейт FOC)

# A1: кастомный GPIO-блок «портов» (§39.1): 4 порта × stride, F4-подобный layout.
# Эмпирика _gpio_layout_probe.py + дизасм драйвера 0x22000 (валидация port/pin/mode).
GPIO_PORT_BASE = 0x48000000
GPIO_PORT_STRIDE = 0x400        # порты: 0x48000000/0400/0800/0C00
GPIO_NPORTS = 4
GPIO_MODER = 0x2c               # режимы ВСЕХ 16 пинов, по 2 бита/пин: pin N → биты [2N+1:2N]
                                # (наблюдено: порт0=0x666 [пины 0-5], порт1=0x66660000 [пины 12-15])
GPIO_MODER_HI = 0x28            # вторичное поле (AF/напр.) — в motor-init = 0
GPIO_IDR = 0x00                 # input-data-регистра (read-only; 16 пинов, бит N = состояние пина N; §96: 0x1BF24 читает [port1+0x00] и raw-shift'ом берёт пины 6-8 = 3-bit «iron»-вход)
GPIO_OUTSEL = 0x10              # output/select (большие значения — mask в high-битах)
GPIO_BIT_REGS = (0x14, 0x18, 0x1c, 0x20, 0x24)   # битовые регистры (сброс 0 в init)

# §96: BLE app-протокол Mi Home (apk/64bitpackage.apk + logs/btsnoop_hci.log).
# Формат data-фрейма: [siid:1][piid:1][len:2 LE][data:len] — len = ПОЛНЫЙ размер данных;
# при len > ~240Б данные фрагментируются по нескольким ATT-фреймам (стриминг). Trailing
# CRC-8 на siid=0/piid=0 НЕ найден (poly 0x29/0x49/0x31/0x9B не совпадают).
MI_BLE_SIID_MAIN = 0      # основной data-канал (телеметрия+команды): handles 0x18/0x21/0x24
MI_BLE_SIID_SEC = 1       # второй data-канал: handle 0x21
MI_BLE_SIID_OTA = 0xF5    # шифрованный OTA/DFU-канал: handles 0x38/0x3a/0x44 (ciphertext)
MI_BLE_MTU_DATA = 240     # макс. data-байт в одном ATT-фрейме (наблюдено до 244Б payload)


def mi_ble_decode(payload):
    """Decode the Mi Home BLE data-frame: [siid][piid][len:2 LE][data]. Returns
    dict(siid, piid, len, data, complete). complete=False -> fragmentation (len >
    len(data) — the data continues in the next ATT-frame).

    Декод data-фрейма Mi Home BLE: [siid][piid][len:2 LE][data].
    Возвращает dict(siid, piid, len, data, complete). complete=False → фрагментация
    (len > len(data) — данные продолжатся в следующем ATT-фрейме)."""
    if len(payload) < 4:
        return {'siid': payload[0] if payload else None,
                'piid': payload[1] if len(payload) > 1 else None,
                'len': None, 'data': b'', 'complete': False}
    siid, piid = payload[0], payload[1]
    ln = struct.unpack('<H', payload[2:4])[0]
    data = payload[4:]
    return {'siid': siid, 'piid': piid, 'len': ln, 'data': data,
            'complete': ln <= len(data)}

# §99 (F2): полная таблица siid/piid из плагина Mi Home (modules/10724.js —
# global.SIID_DIC + global.SIID_N). SIID_5 — плоское «model»-зеркало (1..34),
# SIID_6 — журнал поездок. SIID_0 (siid=0 в snoop) = тот же набор что SIID_1+2
# (main data-канал; плагин индексирует SIID_1/2, a BLE-фреймы идут с siid=0 —
# см. MI_BLE_SIID_MAIN/SEC).
MI_SIID_PIID = {
    1: {1: "RIDING_MODE", 2: "BATTERY_LEVEL", 3: "REMAINING_BATTERY", 4: "VOLTAGE",
        5: "CURRENT", 6: "POWER", 7: "REMAINING_MILEAGE", 8: "FAULT",
        9: "CURRENT_MILEAGE"},
    2: {1: "AVERAGE_SPEED", 2: "IS_LOCKED", 3: "CRUISE_IS_ON", 4: "TAIL_LIGHT_IS_ON",
        5: "ENERGY_RECOVERY", 6: "TOTAL_MILEAGE", 7: "IS_RIDING", 8: "RIDING_TIME",
        9: "HIGHEST_SPEED", 10: "ASR_IS_ON", 11: "REMAINING_MILEAGE_ALGORITHM",
        12: "AUTO_LIGHT", 13: "TCS", 14: "INTELLIGENT_DOWNHILL", 15: "HILL_PARKING",
        16: "ATMOSPHERE_LIGHT", 17: "BLUETOOTH_SEARCH_ON", 18: "FAKE_SHUTDOWN_STATUS"},
    3: {1: "BATTERY_STATUS", 2: "BATTERY_TEMPERATURE", 3: "SCOOTER_TEMPERATURE",
        4: "LOCK_WARNING", 5: "MILEAGE_UNIT", 6: "OOB_CODE", 7: "TIRE_MAINTENANCE",
        8: "ACTIVATION_DATE", 9: "RIDING_RECORDS", 10: "IS_CHARGING",
        11: "NUMBER_OF_CYCLES", 12: "SOH"},
    4: {1: "PRODUCTION_DATE", 2: "BATTERY_SN", 3: "BMS_FIRMWARE_VERSION",
        4: "SCOOTER_SN", 5: "FIRMWARE_VERSION", 6: "RESTORE_SCOOTER_SETTINGS",
        7: "MORE_BATTERY_INFO", 8: "MORE_BATTERY_INFO_2", 10: "BLUETOOTH_CAR_SEARCH"},
    5: {1: "RIDING_MODE", 2: "BATTERY_LEVEL", 3: "REMAINING_BATTERY", 4: "VOLTAGE",
        5: "CURRENT", 6: "POWER", 7: "REMAINING_MILEAGE", 8: "FAULT",
        9: "CURRENT_MILEAGE", 10: "AVERAGE_SPEED", 11: "IS_LOCKED",
        12: "CRUISE_IS_ON", 13: "TAIL_LIGHT_IS_ON", 14: "ENERGY_RECOVERY",
        15: "TOTAL_MILEAGE", 16: "IS_RIDING", 17: "RIDING_TIME",
        18: "HIGHEST_SPEED", 19: "BATTERY_STATUS", 20: "BATTERY_TEMPERATURE",
        21: "SCOOTER_TEMPERATURE", 22: "LOCK_WARNING", 23: "REPORT_SWITCH",
        24: "IS_CHARGING", 29: "TCS_SWITCH", 30: "INTELLIGENT_DOWNHILL_SWITCH",
        31: "HILL_PARKING_SWITCH", 32: "ATMOSPHERE_LIGHT_MODEL",
        33: "BLUETOOTH_SEARCH_ON_MODEL", 34: "FAKE_SHUTDOWN_MODEL"},
    6: {1: "LOG_1", 2: "LOG_2", 3: "LOG_3", 4: "LOG_4", 5: "LOG_5"},
}
MI_PROP_VALUE_TYPE = {0: "BOOL", 1: "UINT8", 2: "INT8", 3: "UINT16", 4: "INT16",
                      5: "UINT32", 6: "INT32", 7: "UINT64", 8: "INT64", 9: "FLOAT",
                      10: "STRING"}  # global.PROP_VALUE_TYPE (10724.js)

# §99 (F2): OTA/DFU-канал (siid=0xF5) из logs/btsnoop_hci.log (97 фреймов).
# Handles: 0x38 — app→device (WRITE_CMD), 0x3A — device→app (NOTIFY-ack),
# 0x44 — app→device (редко). Формат фрейма: [0xF5][piid][N][marker:2 LE][sub:4]
# [cls:1][payload:N+1] (total = 11+N; N=0 → переменный payload до ~234Б).
# marker: 0xFFFF — малые фреймы; 0x5300/0x5600/0x5501 — чанк-фреймы 208Б
# (значения похожи на offset/sequence в OTA-потоке); 0x005C/0x00DE/0x00DC/0x005E
# — маркеры 16-32Б фреймов. cls: 0x80/0xA0/0x90 — data-write, 0x00/0x01/0x03 —
# control/ack. Payload — шифртекст (ключ OTA-сессии из native SDK, не в RN-бандле).
MI_OTA_HANDLE_APP2DEV = 0x38
MI_OTA_HANDLE_DEV2APP = 0x3A
MI_OTA_HANDLE_ALT = 0x44


def mi_ota_decode(payload):
    """Decode the siid=0xF5 OTA frame: [0xF5][piid][N][marker:2 LE][sub:4][cls:1]
    [payload:N+1]. Returns dict(siid, piid, n, marker, sub, cls, payload).

    Декод OTA-фрейма siid=0xF5: [0xF5][piid][N][marker:2 LE][sub:4][cls:1]
    [payload:N+1]. Возвращает dict(siid, piid, n, marker, sub, cls, payload)."""
    if len(payload) < 11 or payload[0] != MI_BLE_SIID_OTA:
        return None
    piid = payload[1]
    n = payload[2]
    marker = struct.unpack('<H', payload[3:5])[0]
    sub = payload[5:9]
    cls = payload[9]
    payload_ = payload[10:]
    return {'siid': payload[0], 'piid': piid, 'n': n, 'marker': marker,
            'sub': sub, 'cls': cls, 'payload': payload_,
            'complete': len(payload_) == n + 1}

# дескрипторы планировщика USART3 (из REPORT §MCU)
DESC_BASE = 0x20000A43
STATE_BASE = 0x20000A40


def align(x, a=0x1000):
    """Round up to a multiple of a.
    Округление вверх до кратного a."""
    return (x + a - 1) & ~(a - 1)


class McuEmu:
    """Instruction emulator for the MCU (Unicorn, ARM Thumb): flash0/flash1/RAM/periph mapping,
    hooks (code/write/read/unmapped), running a function with r0..r3 args and a report.
    Инструкционный эмулятор MCU (Unicorn, ARM Thumb): маппинг flash0/flash1/RAM/периферии,
    hooks (code/write/read/unmapped), запуск функции с аргументами r0..r3 и отчёт."""

    def __init__(self, trace=False, max_insn=200000):
        """Create the Uc context + mapping + hooks.
        Создание контекста Uc + маппинг + hooks."""
        self.trace = trace
        self.max_insn = max_insn
        self.insn = 0
        self.usart_out = bytearray()
        self.ram_writes = []          # (pc, addr, size, val) в области дескрипторов
        self.ram_writes_all = []      # (pc, addr, size, val) ВСЕ записи в RAM (§80 RX-контекст)
        # --- периферия: диагностика + точные значения (§73) ---
        self.periph_overrides = {}    # {addr: u32} точные значения регистров (после fill)
        self.periph_writes = []       # [(pc, addr, size, value)] все записи в периферию
        self.periph_reads = {}        # {addr: [pc,...]} трассировка чтений (trace_periph)
        self.trace_periph = False     # включить логирование чтений периферии
        self.stopped = None
        self.uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        self._map()
        self._hooks()

    def _map(self):
        """Load the firmware into flash0/flash1 and map RAM/PERIPH/PERIPH2/SYS.
        Загрузить firmware в flash0/flash1 и маппировать RAM/PERIPH/PERIPH2/SYS."""
        fw = open(FW, "rb").read()
        fsz = align(len(fw))
        for base in (FLASH0, FLASH1):
            self.uc.mem_map(base, fsz)
            self.uc.mem_write(base, fw)
        self.uc.mem_map(RAM, RAM_SIZE)
        self.uc.mem_map(PERIPH, PERIPH_SIZE)
        self.uc.mem_map(PERIPH2, PERIPH2_SIZE)
        self.uc.mem_map(SYS, SYS_SIZE)
        self.fw_len = len(fw)

    def _hooks(self):
        """Register the hooks: code (limit/spin-detect/trace), write, read (periph), unmapped.
        Подключить hooks: code (лимит/spin-детект/trace), write, read (периферия), unmapped."""
        self.uc.hook_add(UC_HOOK_CODE, self._h_code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._h_write)
        self.uc.hook_add(UC_HOOK_MEM_READ, self._h_read, None, PERIPH, PERIPH + PERIPH_SIZE)
        self.uc.hook_add(UC_HOOK_MEM_READ, self._h_read, None, PERIPH2, PERIPH2 + PERIPH2_SIZE)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self._h_unmapped)

    def _h_code(self, uc, address, size, user):
        """Code hook: instruction counter, limit, spin-loop detection (broad mode), first-60 trace.
        Code-hook: счётчик инструкций, лимит, детект spin-loop (broad-режим), trace первых 60."""
        self.insn += 1
        if self.insn > self.max_insn:
            self.stopped = f"лимит инструкций {self.max_insn}"
            uc.emu_stop()
            return
        # детект зависания: один PC исполнен слишком много раз = spin-loop
        if getattr(self, "broad", False):
            c = self.pc_hits.get(address, 0) + 1
            self.pc_hits[address] = c
            if c > self.spin_limit:
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR) or 1)
                self.spins += 1
                # если совсем застряли (много разных спинов) — стоп
                if self.spins > 400:
                    self.stopped = f"слишком много spin-loop'ов (последний @0x{address:05x})"
                    uc.emu_stop()
        if self.trace and self.insn <= 60:
            print(f"    [{self.insn:>5}] pc=0x{address:05x}")

    def _h_write(self, uc, access, address, size, value, user):
        """Write hook: capture USART3_DR, the descriptor region, full-RAM and periph writes.
        Write-hook: захват USART3_DR, области дескрипторов, full-RAM и записей в периферию."""
        if address == USART3_DR or (USART3_BASE <= address < USART3_BASE + 0x20 and size == 1):
            self.usart_out.append(value & 0xFF)
            pc = uc.reg_read(UC_ARM_REG_PC)
            print(f"    >>> USART3 write @pc=0x{pc:05x}: 0x{value & 0xFF:02x}")
        if 0x20000A00 <= address < 0x20000C10:      # область дескрипторов/стейта
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.ram_writes.append((pc, address, size, value))
        if RAM <= address < RAM + RAM_SIZE:         # full-RAM захват (§80)
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.ram_writes_all.append((pc, address, size, value))
        # запись в периферию (TIM/ADC/GPIO) — логируем для анализа моторного контура
        if (PERIPH <= address < PERIPH + PERIPH_SIZE or
                PERIPH2 <= address < PERIPH2 + PERIPH2_SIZE):
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.periph_writes.append((pc, address, size, value))

    def _h_read(self, uc, access, address, size, value, user):
        # периферия: status-регистры отдают «готов» (все биты), чтобы poll-циклы
        # не зависали. Это грубо, но позволяет коду двигаться.
        """Read hook: periph reads as 0xFF (ready bits) so poll-loops can advance; optional read log.
        Read-hook: периферия читается как 0xFF (ready-биты); опциональный лог чтений."""
        if self.trace_periph:
            pc = uc.reg_read(UC_ARM_REG_PC)
            self.periph_reads.setdefault(address, []).append(pc)
        return

    def _h_unmapped(self, uc, access, address, size, value, user):
        """Unmapped hook: broad mode maps a zero page on demand and continues; otherwise stop.
        Unmapped-hook: ШИРОКИЙ режим — маппим нулевую страницу по требованию; иначе стоп."""
        if getattr(self, "broad", False):
            page = address & ~0xFFF
            try:
                uc.mem_map(page, 0x1000)
                self.mapped_pages = getattr(self, "mapped_pages", 0) + 1
                return True
            except UcError:
                return True
        pc = uc.reg_read(UC_ARM_REG_PC)
        self.stopped = f"обращение к незамапленному 0x{address:08x} @pc=0x{pc:05x} (access={access})"
        return False       # остановить

    def hook_periph_ready(self):
        """Периферию читаем как 0xFFFFFFFF (все ready-биты) — через отдельный
        механизм: Unicorn не даёт менять значение в READ-хуке напрямую, поэтому
        предзаполняем регион единицами."""
        self.uc.mem_write(PERIPH, b"\xff" * PERIPH_SIZE)
        self.uc.mem_write(PERIPH2, b"\x00" * PERIPH2_SIZE)
        self.uc.mem_write(SYS, b"\x00" * SYS_SIZE)

    # --- §73: точные значения регистров периферии + отчёт по обращениям ---
    def set_periph(self, addr, value):
        """Задать точное значение 32-битного регистра периферии (вместо blanket
        0xFF/0x00). Применяется после hook_periph_ready/run_broad-заполнения."""
        self.periph_overrides[addr] = value & 0xFFFFFFFF

    def apply_periph_overrides(self):
        """Пропитать periph_overrides в память (вызывать после заполнения fill)."""
        for addr, val in self.periph_overrides.items():
            try:
                self.uc.mem_write(addr, struct.pack('<I', val))
            except Exception:
                pass

    def report_periph(self, max_addrs=40):
        """Отчёт по обращениям к периферии (записи + чтения, сгруппировано по адресу)."""
        addrs = set(a for _, a, _, _ in self.periph_writes) | set(self.periph_reads)
        if not addrs:
            print("[periph] обращений к периферии не было")
            return
        print(f"[periph] регистров затронуто: {len(addrs)} "
              f"(записей {len(self.periph_writes)}, чтений в {len(self.periph_reads)} адр)")
        for a in sorted(addrs)[:max_addrs]:
            ws = [w for _, aa, _, w in self.periph_writes if aa == a]
            rs = self.periph_reads.get(a, [])
            wvals = sorted(set(ws))
            wstr = ('[' + ','.join(hex(v) for v in wvals[:6]) + ']') if ws else ''
            print(f"  0x{a:08x}: W×{len(ws)} {wstr} R×{len(rs)}")

    # --- E2: periph-write-trace facility (захват periph-writes на функцию) ---
    def periph_write_map(self):
        """E2: periph-writes сгруппированы по адресу {addr: [value,...]} (порядок записей).
        Facility для верификации «функция X пишет в регистр Y значение Z» — улучшает все
        модели A (GPIO/USART/SPI/TIM). Источник: self.periph_writes [(pc,addr,size,value)]."""
        m = {}
        for _, addr, size, value in self.periph_writes:
            m.setdefault(addr, []).append(value)
        return m

    def periph_writes_since(self, mark):
        """E2: periph-writes после снимка mark=len(periph_writes) — окно одного вызова."""
        return self.periph_writes[mark:]

    def seed_scheduler(self):
        """Предусловия планировщика 0x1f600 (из литерального пула):
        - [0x200002c2]=0 (слот 0), [0x200002c1]=1 (!= -> не beq);
        - таймер 'сейчас' 0x200001e0 велик, 'послед.' 0x20000198 = 0 (elapsed>432);
        - дескриптор слота 0 (0x20000a43, 150Б) — маркеры, чтобы увидеть путь в USART3."""
        self.uc.mem_write(0x200002c2, b"\x00")            # слот 0
        self.uc.mem_write(0x200002c1, b"\x01")            # != -> не beq
        self.uc.mem_write(0x200001e0, struct.pack("<Q", 0x00100000))  # таймер now
        self.uc.mem_write(0x20000198, struct.pack("<Q", 0))           # таймер last
        # межбайтовый таймер [0x20000170+0x30/+0x34] > 8 (иначе ждёт 8 тиков)
        self.uc.mem_write(0x200001a0, struct.pack("<II", 100, 0))
        # дескриптор слота 0: узнаваемые байты D0 D1 D2 ... (первый = длина кадра)
        self.uc.mem_write(DESC_BASE, bytes((0xD0 + i) & 0xFF for i in range(150)))
        # USART3 SR [0x40004828] бит14 = 0 -> «не занято», путь отправки открыт

    def run_broad(self, addr, budget=2000000, spin_limit=3000):
        """Широкая эмуляция: прогнать init-функцию, дав рантайм-указателям поставиться.
        Маппинг по требованию, детект spin-loop, толерантность к периферии."""
        self.broad = True
        self.max_insn = budget
        self.spin_limit = spin_limit
        self.pc_hits = {}
        self.spins = 0
        self.mapped_pages = 0
        self.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))
        self.uc.mem_write(PERIPH2, bytes(PERIPH2_SIZE))
        self.uc.mem_write(SYS, bytes(SYS_SIZE))
        self.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        self.uc.reg_write(UC_ARM_REG_LR, 1)
        print(f"[broad] запуск init 0x{addr:05x}, бюджет {budget}")
        try:
            self.uc.emu_start(addr | 1, 0, count=budget + 5)
        except UcError as e:
            if self.stopped is None:
                self.stopped = f"UcError {e} @pc=0x{self.uc.reg_read(UC_ARM_REG_PC):05x}"
        print(f"[broad] инструкций: {self.insn}, spin-loop'ов: {self.spins}, "
              f"домапплено страниц: {self.mapped_pages}")
        print(f"[broad] останов: {self.stopped or 'дошёл до конца'}")
        return self

    def dump_ram(self, addr, size, label=""):
        """Dump a RAM region to the console (hex, 16B lines).
        Дамп региона RAM в консоль (hex, по 16Б)."""
        try:
            r = self.uc.mem_read(addr, size)
        except Exception:
            return
        nz = any(r)
        print(f"[ram] 0x{addr:08x}..+0x{size:x} {label} {'(есть данные)' if nz else '(пусто)'}:")
        if nz:
            for i in range(0, len(r), 16):
                print(f"      +{i:03x}: {r[i:i+16].hex(' ')}")

    def run_func(self, addr, args=(), fill_desc=None, seed_sched=False):
        """Run a function: periph prep (ready/seed_scheduler), stack, r0..r3 args,
        LR=ret_magic, execute and report.
        Запуск функции: подготовка периферии (ready/seed_scheduler), стек, аргументы r0..r3,
        LR=ret_magic, исполнение и отчёт."""
        if seed_sched:
            self.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))   # status-биты сброшены
            self.uc.mem_write(PERIPH2, bytes(PERIPH2_SIZE))
            self.uc.mem_write(SYS, bytes(SYS_SIZE))
            self.seed_scheduler()
        else:
            self.hook_periph_ready()
        self.apply_periph_overrides()      # точные значения регистров (§73)
        # опционально засеять дескрипторы маркерами, чтобы увидеть их путь в USART3
        if fill_desc is not None:
            self.uc.mem_write(DESC_BASE, fill_desc)
        # стек
        self.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        # аргументы r0..r3
        regs = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3]
        for r, v in zip(regs, args):
            self.uc.reg_write(r, v)
        # адрес возврата — «магический», ловим его в code-хуке как конец
        ret_magic = 0x00000001                      # BX к нечётному Thumb-адресу 0 -> поймаем
        self.uc.reg_write(UC_ARM_REG_LR, ret_magic)

        start = addr | 1                            # Thumb bit
        print(f"[emu] запуск функции 0x{addr:05x} (Thumb), макс {self.max_insn} инстр.")
        try:
            self.uc.emu_start(start, 0, count=self.max_insn + 5)
        except UcError as e:
            pc = self.uc.reg_read(UC_ARM_REG_PC)
            if self.stopped is None:
                self.stopped = f"UcError {e} @pc=0x{pc:05x}"
        self._report()

    def _report(self):
        """Post-run report: instructions, stop reason, USART3 bytes, RAM writes, state dump.
        Отчёт после прогона: инструкций, останов, USART3-байты, RAM-записи, дамп стейта."""
        print(f"\n[emu] инструкций выполнено: {self.insn}")
        print(f"[emu] останов: {self.stopped or 'дошёл до конца'}")
        print(f"[emu] байт записано в USART3: {len(self.usart_out)}")
        if self.usart_out:
            print(f"      данные: {bytes(self.usart_out).hex(' ')}")
        if self.ram_writes:
            print(f"[emu] записей в область дескрипторов 0x20000A00..0C10: {len(self.ram_writes)}")
            for pc, addr, size, val in self.ram_writes[:20]:
                print(f"      @pc=0x{pc:05x} [0x{addr:08x}] <- 0x{val:0{size*2}x} ({size}B)")
        # дамп RAM-области дескрипторов после прогона
        try:
            region = self.uc.mem_read(STATE_BASE, 0x60)
            print(f"[emu] RAM 0x{STATE_BASE:08x}..+0x60 после прогона:")
            for i in range(0, len(region), 16):
                print(f"      +{i:02x}: {region[i:i+16].hex(' ')}")
        except Exception:
            pass


class TimModel:
    """Timer behavior model (section 73): a scoped view of the region in Uc memory + a write
    registry + named access. Firmware writes already reach memory (the source of truth);
    the model mirrors them for inspection and provides an extension point for clock/status
    flags (tick() is a placeholder for a future tick model).
    §73: поведенческая модель таймера — scoped-вид на регион в памяти Uc + реестр
    записей + named-доступ. Записи firmware уже попадают в память (источник истины);
    модель зеркалирует их для инспекции и даёт точку расширения под clock/status-флаги
    (метод tick() — заглушка под будущую тактовую модель)."""
    def __init__(self, emu, base=MOTOR_TIM_BASE, size=0x100, period=0x8000, step=1):
        """Create the model for a timer region (base/size) + clock model (period/step).
        Создание модели для региона таймера (base/size) + тактовой модели (period/step)."""
        self.emu = emu
        self.base = base
        self.size = size
        self.writes = []      # [(pc, offset, size, value)] записи в этот таймер
        # --- тактовая модель (§73.x): свободно-ходный счётчик + update-событие ---
        self.period = period  # wrap-значение счётчика (ARR)
        self.step = step      # приращение за такт
        self.cnt = 0          # текущее значение счётчика
        self.update = False   # флаг update-события (wrap)
        self.ticks = 0        # число продвинутых тактов
        self._hook = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                     None, base, base + size)

    def _on_w(self, uc, access, address, size, value, user):
        """Record a write to this timer: (pc, offset, size, value).
        Записать запись в этот таймер: (pc, offset, size, value)."""
        self.writes.append((uc.reg_read(UC_ARM_REG_PC) & 0xFFFFF,
                            address - self.base, size, value))

    def read(self, off):
        """Read a u32 register at the offset.
        Прочитать u32-регистр по смещению."""
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(self.base + off, 4)))[0]

    def set(self, off, val):
        """Write a u32 to the register at the offset.
        Записать u32 в регистр по смещению."""
        self.emu.uc.mem_write(self.base + off, struct.pack('<I', val & 0xFFFFFFFF))

    def snapshot(self):
        """Current values of the key registers: {name: u32}.
        Текущие значения ключевых регистров: {имя: u32}."""
        return {
            'ctrl': self.read(0x30),
            'data0': self.read(0x44),
            'data1': self.read(0x48),
            'data2': self.read(0x4c),
            'stat': self.read(0x54),
        }

    def tick(self, n=1):
        """Advance the tick model by n ticks; returns the number of update events.
        Продвинуть тактовую модель на n тактов; вернуть число update-событий.

        Free-running counter cnt += step, wrap by period; on wrap (cnt <= prev)
        self.update is set (analog of the TIM update/capture event). For the motor
        block 0x40012xxx a 'tick' = one control-loop period; the update event matches
        what the firmware sees as the STAT bit 15 (FOC mode gate). The exact hardware
        source and period are not statically defined -> the model is parameterized.

        Свободно-ходный счётчик cnt += step, wrap по period; при wrap (cnt <= prev)
        устанавливается self.update (аналог TIM update-события / события захвата).
        Для моторного блока 0x40012xxx «такт» = один период контура управления;
        update-событие соответствует тому, что firmware видит как STAT бит15 (гейт
        режима FOC). Точный hardware-источник события и период статически не
        определяются → модель параметризована (period/step задаёт вызывающий).
        """
        updates = 0
        for _ in range(n):
            self.ticks += 1
            prev = self.cnt
            self.cnt = (self.cnt + self.step) % self.period
            if self.cnt <= prev:          # wrap (или step=0)
                self.update = True
                updates += 1
        return updates

    def set_status_bits(self, addr, mask):
        """Set the mask bits in the peripheral register addr (RMW, 32-bit).
        Задать биты mask в периферийном регистре addr (RMW, 32-bit)."""
        cur = struct.unpack('<I', self.emu.uc.mem_read(addr, 4))[0]
        self.emu.uc.mem_write(addr, struct.pack('<I', cur | mask))

    def clear_status_bits(self, addr, mask):
        """Clear the mask bits in the peripheral register addr (RMW, 32-bit).
        Сбросить биты mask в периферийном регистре addr (RMW, 32-bit)."""
        cur = struct.unpack('<I', self.emu.uc.mem_read(addr, 4))[0]
        self.emu.uc.mem_write(addr, struct.pack('<I', cur & ~mask))


# §73.x ADC: capture-регистра измерения фазных токов (ADC-inject PWM). 0x1be1c
# читает T28/T2C/T30 и реконструирует токи: фаза = (T−C)<<4, третья фаза = −сумма
# двух измеренных (закон Кирхгофа), финальный clamp [−30000,30000]. Гейт режима —
# STAT бит15 (u32[0x40012c54]): =1 → capture, =0 → skip (только clamp).
ADC_CAP_BASE = 0x40012440
ADC_CAP_T28 = ADC_CAP_BASE + 0x28    # 0x40012468
ADC_CAP_T2C = ADC_CAP_BASE + 0x2c    # 0x4001246c
ADC_CAP_T30 = ADC_CAP_BASE + 0x30    # 0x40012470
# sector → handler (конвенция каталога §60, поведение эмпирически верифицировано §73.x):
# 0→null, 1→B, 2/3→C, 4/5→A, 6→B.
ADC_SECTOR_HANDLER = {0: None, 1: 'B', 2: 'C', 3: 'C', 4: 'A', 5: 'A', 6: 'B'}
# handler → измеренные фазы: (t_reg_off, c_struct_off, out_struct_off).
# C-ссылки (zero-current refs) в struct FOC: C18=+0x18, C1A=+0x1a, C1C=+0x1c;
# выходы: o_c=+0xc, o_10=+0x10, o_14=+0x14.
ADC_HANDLER_MEASURED = {
    'A': [(0x28, 0x18, 0xc), (0x2c, 0x1a, 0x10)],   # T28→o_c, T2C→o_10; o_14=−sum
    'B': [(0x2c, 0x1a, 0x10), (0x30, 0x1c, 0x14)],   # T2C→o_10, T30→o_14; o_c=−sum
    'C': [(0x28, 0x18, 0xc), (0x30, 0x1c, 0x14)],    # T28→o_c, T30→o_14; o_10=−sum
}


class AdcModel:
    """Phase-current ADC/capture channel model (FOC input) (section 73.x).

    Hardware: ADC-inject PWM — the ADC samples the current, the timer captures the
    compare moment; 0x1be1c reads T28/T2C/T30 (periph) and reconstructs the currents.
    The model gives the app access to the T registers (set_captures) and the
    convenience set_currents (inject desired currents against the C refs).
    Current is quantized x16 (scale <<4).
    §73.x: модель ADC/capture-канала фазных токов (вход FOC).

    Hardware: ADC-inject PWM — ADC сэмплирует ток, таймер захватывает момент
    сравнения; 0x1be1c читает T28/T2C/T30 (periph) и реконструирует токи.
    Модель даёт app доступ к T-регистрам (set_captures) и convenience set_currents
    (инжект желаемых токов под C-ссылки). Ток квантуется ×16 (масштаб <<4).
    """
    def __init__(self, emu):
        """Bind the model to the emulator (reads/writes periph directly).
        Привязать модель к эмулятору (чтение/запись periph напрямую)."""
        self.emu = emu

    def _w(self, off, val):
        """Write a u32 to the capture register at the offset.
        Записать u32 в capture-регистр по смещению."""
        self.emu.uc.mem_write(ADC_CAP_BASE + off,
                              struct.pack('<I', val & 0xFFFFFFFF))

    def set_captures(self, t28, t2c, t30):
        """Write the raw capture values T28/T2C/T30 (periph).
        Записать сырые capture-значения T28/T2C/T30 (periph)."""
        self._w(0x28, t28)
        self._w(0x2c, t2c)
        self._w(0x30, t30)

    def get_captures(self):
        """Read the current (T28, T2C, T30) as u32.
        Прочитать текущие (T28, T2C, T30) как u32."""
        return (struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T28, 4))[0],
                struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T2C, 4))[0],
                struct.unpack('<I', self.emu.uc.mem_read(ADC_CAP_T30, 4))[0])

    def set_currents(self, r0, currents, sector):
        """Inject the desired pre-clamp currents by setting the captures against the C refs from r0.

        currents = {0xc: o_c, 0x10: o_10, 0x14: o_14}. For the two measured phases
        (per sector->handler) T = C + (current>>4); the third phase = -sum (automatic).
        Current is quantized x16; the sector determines which 2 phases are measured.
        Инжект желаемых pre-clamp токов, задав capture под C-ссылки из r0.

        currents = {0xc: o_c, 0x10: o_10, 0x14: o_14}. Для двух измеренных фаз
        (по sector→handler) T = C + (ток>>4); третья фаза = −сумма (автоматически).
        Ток квантуется ×16; sector определяет, какие 2 фазы измеряются.
        """
        h = ADC_SECTOR_HANDLER.get(sector & 7)
        if h is None:
            return
        for t_off, c_off, out_off in ADC_HANDLER_MEASURED[h]:
            cref = struct.unpack('<h', self.emu.uc.mem_read(r0 + c_off, 2))[0]
            target = currents[out_off]
            self._w(t_off, (cref + (target >> 4)) & 0xFFFFFFFF)


# §73.x скорость: V=u32[RAM+0x158]=timer-capture период; F=byte[RAM+0x100] гейт;
# val=s16(48000/V) if F!=0 else 0 (0x1d874). val → u16[RAM+0x1768], читается PID 0x1d078.
SPEED_V_OFF = 0x158        # u32 период (RAM+0x158)
SPEED_F_OFF = 0x100        # byte гейт (RAM+0x100): 0 → val=0
SPEED_SP0_OFF = 0x1768     # u16 вычисленный val (RAM+0x1768) — скорость для PID
SPEED_DIV = 48000          # делитель: val = s16(48000/V)


class SpeedModel:
    """Speed measurement model (PID 0x1d078 input), closes the loop (section 73.x).

    Hardware: timer-capture period between encoder pulses -> V; speed proportional to 1/V.
    Firmware: val = s16(48000/V) if F=byte[RAM+0x100]!=0 else 0 (0x1d874),
    val -> u16[RAM+0x1768]. The model sets V/F (set_period / set_speed / stop).
    The exact ISR writer is gated by hardware state (pulse/pending) and does not
    trigger in isolated emulation (writer-sweep: 0 hits) -> the model is
    parameterized (the app supplies the measured speed).
    §73.x: модель замера скорости (вход PID 0x1d078), замыкает контур.

    Hardware: timer-capture период между импульсами энкодера → V; скорость ∝ 1/V.
    Firmware: val = s16(48000/V) if F=byte[RAM+0x100]!=0 else 0 (0x1d874),
    val → u16[RAM+0x1768]. Модель задаёт V/F (set_period / set_speed / stop).
    Точный ISR-писатель гейтится по аппаратному состоянию (импульс/pending) и в
    изолированной эмуляции не триггерится (writer-sweep: 0 хитов) → модель
    параметризована (app даёт измеренную скорость).
    """
    def __init__(self, emu):
        """Bind the model to the emulator.
        Привязать модель к эмулятору."""
        self.emu = emu

    def set_period(self, v):
        """Write the period V (u32[RAM+0x158]) + open the gate F=1.
        Записать период V (u32[RAM+0x158]) + открыть гейт F=1."""
        self.emu.uc.mem_write(RAM + SPEED_V_OFF,
                              struct.pack('<I', v & 0xFFFFFFFF))
        self.emu.uc.mem_write(RAM + SPEED_F_OFF, bytes([1]))

    def set_speed(self, val):
        """Inject the desired measured speed val: V = max(1, 48000//val).

        val<=0 -> stop() (F=0). val>48000 is capped (V=1 -> val=48000).
        Инжект желаемой измеренной скорости val: V = max(1, 48000//val).

        val<=0 → stop() (F=0). val>48000 кэпится (V=1 → val=48000).
        """
        if val <= 0:
            self.stop()
            return
        v = max(1, SPEED_DIV // int(val))
        self.set_period(v)

    def stop(self):
        """Stop: F=0 -> val=0.
        Останов: F=0 → val=0."""
        self.emu.uc.mem_write(RAM + SPEED_F_OFF, bytes([0]))

    def get_val(self):
        """Read the computed val (s16 u16[RAM+0x1768]) after a PID run.
        Прочитать вычисленный val (s16 u16[RAM+0x1768]) после прогона PID."""
        return struct.unpack('<h', self.emu.uc.mem_read(RAM + SPEED_SP0_OFF, 2))[0]


class MotorModel:
    """Motor dynamics model (plant): throttle -> speed over time (section 73.x).

    First-order lag to the terminal speed for the current throttle:
      v_term = v_max * clamp(throttle/throttle_ref, 0, 1)
      speed += (dt/tau) * (v_term - speed)
    Terminal speed at full throttle = v_max; tau is the time constant (inertia +
    resistance). The parameters are NOT defined by the firmware (the physics of a
    specific scooter) -> the model is parameterized. Speed units = internal val
    (section 71): ~20.8 units/(km/h); target 125≈6 km/h, 208≈10 km/h, 522≈25 km/h (EU).
    v_max=522 by default = the maximum target (~25 km/h). Closes the AUTONOMOUS sim:
      target -> PID 0x1d078 -> throttle(u16[RAM+0x42c]) -> [MotorModel] -> speed ->
      SpeedModel.set_speed (V) -> PID ...
    §73.x: модель динамики мотора (plant): throttle → скорость во времени.

    Первый-порядковый lag к терминальной скорости для текущего throttle:
      v_term = v_max * clamp(throttle/throttle_ref, 0, 1)
      speed += (dt/tau) * (v_term - speed)
    Терминальная скорость при full throttle = v_max; tau — постоянная времени
    (инерция + сопротивление). Параметры НЕ определяются firmware (физика
    конкретного самоката) → модель параметризована. Единицы скорости = внутренние
    val (§71): ~20.8 units/(км/ч); target 125≈6 км/ч, 208≈10 км/ч, 522≈25 км/ч (EU).
    v_max=522 по умолчанию = максимальный target (~25 км/ч). Замыкает АВТОНОМНЫЙ симул:
      target → PID 0x1d078 → throttle(u16[RAM+0x42c]) → [MotorModel] → speed →
      SpeedModel.set_speed (V) → PID ...
    """
    def __init__(self, emu, v_max=522.0, tau=15.0, throttle_ref=4000.0, dt=1.0):
        """Create the plant model (v_max, tau, throttle_ref, dt).
        Создание модели plant (v_max, tau, throttle_ref, dt)."""
        self.emu = emu
        self.v_max = float(v_max)
        self.tau = float(tau)
        self.throttle_ref = float(throttle_ref)
        self.dt = float(dt)
        self.speed = 0.0

    def step(self, throttle):
        """One step: throttle (PID output) -> the new speed (val). Returns speed.
        Один шаг: throttle (PID-вывод) → новая скорость (val). Возвращает speed."""
        tnorm = max(0.0, min(1.0, throttle / self.throttle_ref))
        v_term = self.v_max * tnorm
        self.speed += (self.dt / self.tau) * (v_term - self.speed)
        if self.speed < 0.0:
            self.speed = 0.0
        return self.speed

    def reset(self, speed=0.0):
        """Set the speed directly.
        Задать скорость напрямую."""
        self.speed = float(speed)


# §73.x батарея: SoC% = u16[RAM+0x306] (из i16@0x17a0 [415..535]→[0..100]%, §25).
# FOC читает SoC@0x306 с порогами 90/10, clamp 100; гейт byte@0x22e. Защита: 4150
# (max 4.15 В), 3000 (cutoff 3.0 В). Контур: ADC buf[2]→IIR÷256→×410+калибровка(BLE)
# →блок 0x40023c00→i16@0x17a0→[0..100]%→u16@0x306.
BATT_SOC_OFF = 0x306        # u16 SoC % (RAM+0x306)
BATT_RAW_OFF = 0x17A0       # i16 сырое значение [415..535] (RAM+0x17a0)
BATT_RAW_MIN = 415          # → 0%
BATT_RAW_MAX = 535          # → 100%


class BatteryModel:
    """Battery model. SoC% -> u16[RAM+0x306] (+ the raw i16@0x17a0) (section 73.x).

    Loop (section 25): ADC buf[2] -> IIR÷256 (i16@0x272) -> x410 + calibration u16@0x1ec
    (from BLE, raw×41/48) -> block 0x40023c00 -> i16@0x17a0 [415..535] -> [0..100]% ->
    u16[RAM+0x306]. FOC reads SoC@0x306 with thresholds 90/10 (the byte@0x22e gate —
    does not trigger in isolation, verified). The model sets the SoC (set_soc) and
    models discharge (discharge: SoC drops with the load over time). Discharge
    parameters are parameterized.
    §73.x: модель аккумулятора. SoC% → u16[RAM+0x306] (+ сырое i16@0x17a0).

    Контур (§25): ADC buf[2] → IIR÷256 (i16@0x272) → ×410 + калибровка u16@0x1ec
    (из BLE, raw×41/48) → блок 0x40023c00 → i16@0x17a0 [415..535] → [0..100]% →
    u16[RAM+0x306]. FOC читает SoC@0x306 с порогами 90/10 (гейт byte@0x22e — в изоляции
    не срабатывает, проверено). Модель задаёт SoC (set_soc) и моделирует разряд
    (discharge: SoC падает с нагрузкой во времени). Параметры разряда параметризованы.
    """
    def __init__(self, emu, soc=100.0):
        """Create the battery model with an initial SoC.
        Создание модели аккумулятора с начальным SoC."""
        self.emu = emu
        self.soc = float(soc)

    @staticmethod
    def _raw(pct):
        """[0..100]% -> the raw [415..535].
        [0..100]% → сырое [415..535]."""
        return BATT_RAW_MIN + int(round(pct * (BATT_RAW_MAX - BATT_RAW_MIN) / 100.0))

    def set_soc(self, pct):
        """Write the SoC% (u16[RAM+0x306]) + the consistent raw i16@0x17a0.
        Записать SoC% (u16[RAM+0x306]) + согласованное сырое i16@0x17a0."""
        pct = max(0, min(100, int(pct)))
        self.soc = float(pct)
        self.emu.uc.mem_write(RAM + BATT_SOC_OFF, struct.pack('<H', pct))
        self.emu.uc.mem_write(RAM + BATT_RAW_OFF, struct.pack('<h', self._raw(pct)))
        return pct

    def get_soc(self):
        """Read the SoC% (u16[RAM+0x306]).
        Прочитать SoC% (u16[RAM+0x306])."""
        return struct.unpack('<H', self.emu.uc.mem_read(RAM + BATT_SOC_OFF, 2))[0]

    def discharge(self, throttle, dt=1.0, full_throttle=32760.0, rate=0.05):
        """Discharge: the SoC drops proportionally to the load (throttle as a current proxy).

        rate — %/step at full throttle (parameterized; tune against a live measurement).
        Float accumulation in self.soc (section 74: set_soc truncated to int and zeroed
        the fractional part -> discharge was exactly 1%/tick at any load>0); an int is
        written to RAM. Returns the new SoC (int).
        Разряд: SoC падает пропорционально нагрузке (throttle как прокси тока).

        rate — %/шаг при full throttle (параметризовано; подгонять под live-замер).
        Float-накопление в self.soc (§74: set_soc тринкует до int и обнулял дробную
        часть → разряд был ровно 1%/tick при любой нагрузке>0); в RAM пишется int.
        Возвращает новый SoC (int).
        """
        load = max(0.0, min(1.0, throttle / full_throttle))
        self.soc = max(0.0, self.soc - rate * load * dt)
        pct = max(0, min(100, int(self.soc)))
        self.emu.uc.mem_write(RAM + BATT_SOC_OFF, struct.pack('<H', pct))
        self.emu.uc.mem_write(RAM + BATT_RAW_OFF, struct.pack('<h', self._raw(pct)))
        return pct


# §73.x запас хода (0x1d898): читает i16@RAM+0x27A (батарея, ADC-регион §25),
# пишет struct(RAM+0x3C8, общий с PID/FOC): +0x20 = X=(8000·v)>>16;
# +0x40 = 10000·X/(500−X) (делитель 0x19994, div-by-zero→-1, отриц. знаменатель→отриц.).
# Константы: SCALE=8000, REF=500, K=10000 (=scale/100% из §25). Формула вериф. 400/400 (v≥0).
RANGE_VAL_OFF = 0x27A       # i16 вход (батарея)
RANGE_CTX_OFF = 0x3C8       # struct-контекст (общий с PID/FOC)
RANGE_SCALE = 8000          # ×8000>>16
RANGE_REF = 500             # full-scale (div-by-zero при X==500)
RANGE_K = 10000             # масштаб числителя делителя
# аккумулятор 0x1d898 (leaky integrator): new_0x3c=(old_0x3c+delta−prev_0x14)&0xFFFFFFFF;
# new_0x14=asr(new_0x3c,10)[i16]. delta=i16@RAM+0x26E. Вериф. 250/250.
RANGE_ACC_OFF = 0x404       # u32 аккумулятор (struct+0x3c)
RANGE_ACC_SCALED_OFF = 0x3DC  # i16 = acc>>10 (struct+0x14)
RANGE_DELTA_OFF = 0x26E     # i16 delta-вход


class RangeModel:
    """Range-of-remaining-charge estimator (firmware 0x1d898) (section 73.x).

    v = i16@RAM+0x27A (battery) -> X = (8000·v)>>16; R = 10000·X/(500−X).
    The formula is verified by a 400/400 random sweep (v≥0, including div-by-zero->-1
    and a negative denominator) against the firmware. estimate() is closed-form; to
    cross-check, call the firmware directly: run.call(0x1D898, (0,0,0,0), max_insn=300000)
    -> X=u16[RAM+0x3E8], R=i32[RAM+0x408]. The physical unit of R is not statically
    defined (needs a live correlation); at v∈[415..535] (SoC) R≈1111..1494.
    §73.x: оценщик запаса хода (firmware 0x1d898).

    v = i16@RAM+0x27A (батарея) → X = (8000·v)>>16; R = 10000·X/(500−X).
    Формула верифицирована random-sweep 400/400 (v≥0, включая div-by-zero→-1 и
    отрицательный знаменатель) против firmware. estimate() — closed-form; для сверки
    вызывайте firmware напрямую: run.call(0x1D898, (0,0,0,0), max_insn=300000) →
    X=u16[RAM+0x3E8], R=i32[RAM+0x408]. Физическая единица R не определена статически
    (нужна live-корреляция); при v∈[415..535] (SoC) R≈1111..1494.
    """
    def __init__(self, emu):
        """Bind the model to the emulator.
        Привязать модель к эмулятору."""
        self.emu = emu

    def set_value(self, v):
        """Write the input i16@RAM+0x27A. Returns v.
        Записать входной i16@RAM+0x27A. Возвращает v."""
        v = max(-32768, min(32767, int(v)))
        self.emu.uc.mem_write(RAM + RANGE_VAL_OFF, struct.pack('<h', v))
        return v

    def estimate(self, v):
        """Closed-form: (X, R). X=(8000·v)>>16; R=10000·X/(500−X), div-by-zero -> -1.
        Closed-form: (X, R). X=(8000·v)>>16; R=10000·X/(500−X), div-by-zero→-1."""
        X = (RANGE_SCALE * v) >> 16
        denom = RANGE_REF - X
        if denom == 0:
            return X, -1
        num = RANGE_K * X
        q = abs(num) // abs(denom)
        R = -q if (num < 0) != (denom < 0) else q
        return X, R

    def set_delta(self, d):
        """Write the accumulator delta input i16@RAM+0x26E. Returns d.
        Записать delta-вход аккумулятора i16@RAM+0x26E. Возвращает d."""
        d = max(-32768, min(32767, int(d)))
        self.emu.uc.mem_write(RAM + RANGE_DELTA_OFF, struct.pack('<h', d))
        return d

    def acc_step(self, old_acc, old_scaled, delta):
        """Leaky integrator (0x1d898): returns (new_acc u32, new_scaled i16).

        new_acc = (old_acc + delta − old_scaled) & 0xFFFFFFFF
        new_scaled = asr(new_acc, 10) as i16 (low 16 bits of the arithmetic shift).
        Verified by a 250/250 stateful sweep against the firmware.
        Leaky integrator (0x1d898): возвращает (new_acc u32, new_scaled i16).

        new_acc = (old_acc + delta − old_scaled) & 0xFFFFFFFF
        new_scaled = asr(new_acc, 10) как i16 (низкие 16 бит арифметического сдвига).
        Верифицировано stateful-sweep 250/250 против firmware.
        """
        new_acc = (old_acc + delta - old_scaled) & 0xFFFFFFFF
        s = new_acc if new_acc < 0x80000000 else new_acc - 0x100000000
        asr = s >> 10                      # Python arithmetic shift == ARM asr
        ns = asr & 0xFFFF
        new_scaled = ns if ns < 0x8000 else ns - 0x10000
        return new_acc, new_scaled


# §74 Автономный моторный контур (time-driven warm-start control loop).
PID_OFF = 0x1D078          # PID / speed-limit state machine
FOC_OFF = 0x1A938          # FOC routine
THROTTLE_OFF = 0x42C       # s16 PID-вывод (throttle)
CURR_REF_OFF = 0x224       # u16 FOC current-ref (upstream command, §73.15)
FOC_CTX_OFF = 0x040        # R4 контекст FOC
FOC_CCR_OFFS = (0x382, 0x384, 0x386)   # PWM CCR A/B/C (RAM+off)


class GpioModel:
    """Behavioral model of the custom GPIO 'ports' block (A1, section 39.1) — a scoped
    view of the region 0x48000000..+4×0x400 + a write registry + pin-mode decoding
    (2 bits/pin in MODER_LO/HI). Firmware writes already reach memory (the source of
    truth); the model mirrors them for pin-config inspection and provides an
    extension point for the input state. (The input register is read-only, not
    written in init; see input().)"
    A1: поведенческая модель кастомного GPIO-блока «портов» (§39.1) — scoped-вид на
    регион 0x48000000..+4×0x400 + реестр записей + декод режима пинов (2 бита/пин в
    MODER_LO/HI). Записи firmware уже попадают в память (источник истины); модель
    зеркалирует их для инспекции pin-config и даёт точку расширения под input-state.
    (input-регистр — чтение, в init не пишется; см. input().)"""
    def __init__(self, emu, base=GPIO_PORT_BASE, nports=GPIO_NPORTS, stride=GPIO_PORT_STRIDE):
        """Create the GPIO model for the port block (base/nports/stride) + a write hook.
        Создание модели GPIO для блока портов (base/nports/stride) + write-hook."""
        self.emu = emu
        self.base = base
        self.nports = nports
        self.stride = stride
        self.writes = []      # [(pc, port, offset, size, value)]
        self._hook = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                     None, base, base + nports * stride)

    def _on_w(self, uc, access, address, size, value, user):
        """Record a write: (pc, port, offset, size, value).
        Записать запись: (pc, port, offset, size, value)."""
        off = address - self.base
        self.writes.append((uc.reg_read(UC_ARM_REG_PC) & 0xFFFFF,
                            off // self.stride, off % self.stride, size, value))

    def read(self, port, off):
        """Read a u32 register of a port at the offset.
        Прочитать u32-регистр порта по смещению."""
        return struct.unpack('<I',
                             bytes(self.emu.uc.mem_read(self.base + port * self.stride + off, 4)))[0]

    def set(self, port, off, val):
        """Write a u32 to a port register at the offset.
        Записать u32 в регистр порта по смещению."""
        self.emu.uc.mem_write(self.base + port * self.stride + off,
                              struct.pack('<I', val & 0xFFFFFFFF))

    def pin_mode(self, port, pin):
        """Pin mode (2 bits) from MODER (+0x2c): pin N -> bits [2N+1:2N].
        Режим пина (2 бита) из MODER (+0x2c): pin N → биты [2N+1:2N]."""
        return (self.read(port, GPIO_MODER) >> (pin * 2)) & 0x3

    def input(self, port, pin=None):
        """Pin input state from the IDR (+0x00, read-only). pin=None -> the whole u32;
        otherwise the bit `pin`. Section 96: 0x1BF24 reads [port1+0x00] and raw-shifts
        pins 6-8 of port1 (0x48000400) = the 3-bit 'iron' input.
        Input-состояние пина(ов) из IDR (+0x00, read-only). pin=None → весь u32;
        иначе бит `pin`. §96: 0x1BF24 читает [port1+0x00] и raw-shift'ом берёт
        пины 6-8 порта1 (0x48000400) = 3-bit «iron»-вход."""
        v = self.read(port, GPIO_IDR)
        if pin is None:
            return v
        return (v >> pin) & 1

    def output(self, port):
        """The output/select register value (+0x10).
        Значение output/select-регистра +0x10."""
        return self.read(port, GPIO_OUTSEL)

    def config_report(self):
        """{port: {pin: mode}} — only pins with a non-zero mode (the final state).
        {port: {pin: mode}} — только пины с ненулевым режимом (итоговое состояние)."""
        rep = {}
        for p in range(self.nports):
            pins = {pin: self.pin_mode(p, pin) for pin in range(16)
                    if self.pin_mode(p, pin)}
            if pins:
                rep[p] = pins
        return rep


# A2: push-кадры 'a'/'a1' (сборщик 0x211f8 → TX-кольцо @0x10b5, кадр с 0x10b6).
PUSH_RING_OFF = 0x10B5          # база TX-кольца
PUSH_FRAME_HDR = 0x61
PUSH_FRAME_TRAILER = 0x9E


def decode_push_frames(data):
    """Parse a byte stream into valid push frames `61 [sub] [len] data[len] chk 9E`
    (chk=SUM(bytes before chk)&0xFF). Returns [(raw, sub, fields)]. A pure function —
    works for both the emulator and a live capture (moved from probes/mcu_push_decode.py).
    Разобрать поток байтов на валидные push-кадры `61 [sub] [len] data[len] chk 9E`
    (chk=SUM(байты до chk)&0xFF). Возвращает [(raw, sub, fields)]. Чистая функция —
    работает и для эмулятора, и для live-захвата (перенос из probes/mcu_push_decode.py)."""
    out = []
    i, n = 0, len(data)
    while i < n:
        if data[i] != PUSH_FRAME_HDR:
            i += 1
            continue
        if n - i < 3:
            break
        ln = data[i + 2]
        e = i + ln + 5
        if ln > 200 or e > n:
            i += 1
            continue
        if data[e - 1] != PUSH_FRAME_TRAILER or (sum(data[i:e - 2]) & 0xFF) != data[e - 2]:
            i += 1
            continue
        f = bytes(data[i:e])
        sub = f[1]
        if sub == 0x30:      # 'a0' телеметрия (LEN=10)
            fields = {'mode': f[3], 'mask': f[5], 'cur_biased': f[6],
                      'abs_i290': f[7], 'status': f[8], 'pct_0x236': (f[9] << 8) | f[10],
                      'flag': f[11], 'bit3_0x244': f[12]}
        elif sub == 0x31:    # 'a1' батарея (LEN=9)
            fields = {'v_0x2e6': f[3], 'batt_pct': f[4], 'u16_0x308': (f[5] << 8) | f[6],
                      'u16_0x30a': (f[7] << 8) | f[8], 'temp_c': f[9],
                      'range': (f[10] << 8) | f[11]}
        else:
            fields = {}
        out.append((f, sub, fields))
        i = e
    return out


class UsartTxModel:
    """Push-TX pipeline model (the ASSEMBLY stage) (A2). Runs the REAL assembler 0x211f8
    (no arguments — it reads the fixed telemetry RAM fields), reads the TX ring @0x10b5
    and decodes frames via decode_push_frames. Sending to USART3_DR is done by a separate
    TX sender (usart_out) — this model models exactly the frame assembly.
    A2: модель push-TX pipeline (этап СБОРКИ). Прогоняет РЕАЛЬНЫЙ сборщик 0x211f8
    (без аргументов — читает фикс. RAM-поля телеметрии), читает TX-кольцо @0x10b5 и
    декодит кадры через decode_push_frames. Отправку в USART3_DR делает отдельный
    TX-отправитель (usart_out) — эта модель моделирует именно сборку кадров."""
    def __init__(self, emu):
        """Bind the model to the emulator.
        Привязать модель к эмулятору."""
        self.emu = emu

    def assemble(self, run_off=0x211F8, window=(0x10B0, 0x140)):
        """Run the assembler with the current RAM state -> [(raw, sub, fields)].
        Прогнать сборщик с текущим RAM-состоянием → список [(raw, sub, fields)]."""
        uc = self.emu.uc

        def _st(uc_, a, s, u):
            """Stop if the PC leaves the code range (flash0/flash1).
            Стоп если PC выходит за пределы кода (flash0/flash1)."""
            aa = a & ~1
            if not (FLASH0 <= aa < FLASH0 + 0x23680 or
                    FLASH1 <= aa < FLASH1 + 0x23680):
                uc_.emu_stop()
        sh = uc.hook_add(UC_HOOK_CODE, _st)
        try:
            uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
            uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
            self.emu.insn = 0
            try:
                uc.emu_start(run_off | 1, 0, count=300_000)
            except UcError:
                pass
        finally:
            uc.hook_del(sh)
        lo, size = window
        data = bytes(uc.mem_read(RAM + lo, size))
        return decode_push_frames(data)


class UsartTxSenderModel:
    """TX sender — the union of the section 94 'scheduler' 0x1F600 + the byte primitive
    0x1F1C0 (section 96, A2 remainder). 0x1F600 = the main-loop dispatcher (head 0x2C1 /
    tail 0x2C2, ring @0xA43, slot 0x96, period 432): on a slot dispatch the frame bytes
    (len=8) are sent one by one to USART3_DR via 0x1F1C0, with the TX-ready gate =
    sign-bit([USART3_TXSR]<<17). Model: a frame buffer @0xA43 + a byte index + 1 byte/tick
    (emulating the real 0x1F600/0x1F1C0).
    §96 (A2-остаток): TX-отправитель — объединение §94 «scheduler» 0x1F600 + byte-примитив
    0x1F1C0. 0x1F600 = main-loop dispatcher (head 0x2C1/tail 0x2C2, ring @0xA43, слот 0x96,
    период 432): при dispatch слота байты фрейма (len=8) отправляются по одному в USART3_DR
    через 0x1F1C0, с гейтом TX-ready = sign-bit([USART3_TXSR]<<17). Модель: frame-буфер @0xA43
    + byte-индекс + 1 байт/tick (эмуляция реального 0x1F600/0x1F1C0)."""

    def __init__(self, emu):
        """Create the TX sender model (frame buffer @0xA43, byte index, send counter).
        Создание модели TX-отправителя (frame-буфер @0xA43, byte-индекс, счётчик отправок)."""
        self.emu = emu
        self.usart_out = bytearray()   # всё, что ушло в USART3_DR
        self._frame = None
        self._idx = 0
        self.sent = 0

    def load_frame(self, frame):
        """Queue a frame for sending (analog of the 0x1F600 slot dispatch).
        Поставить фрейм в очередь отправки (аналог dispatch слота 0x1F600)."""
        self._frame = bytes(frame)
        self._idx = 0

    def tx_ready(self):
        """The TX-ready gate: sign-bit([USART3_TXSR]<<17). In isolation (0) -> not ready;
        the model allows forcing via force_ready.
        Гейт TX-ready: sign-bit([USART3_TXSR]<<17). В изоляции (0) → not ready;
        модель позволяет форсировать через force_ready."""
        if getattr(self, 'force_ready', True):
            return True
        v = struct.unpack('<I', bytes(self.emu.uc.mem_read(USART3_TXSR, 4)))[0]
        return bool(((v << 17) & 0x80000000) == 0)

    def tick(self):
        """1 byte/tick: send frame[_idx] -> USART3_DR (0x1F1C0). Returns the byte or None.
        1 байт/tick: отправить frame[_idx] → USART3_DR (0x1F1C0). Вернуть байт или None."""
        if self._frame is None or self._idx >= len(self._frame):
            return None
        if not self.tx_ready():
            return None
        b = self._frame[self._idx]
        self.emu.uc.mem_write(USART3_DR, bytes([b]))
        self.usart_out.append(b)
        self._idx += 1
        self.sent += 1
        if self._idx >= len(self._frame):
            self._frame = None
        return b



# A3: внешний SPI-flash (NVM). SPI1 @0x40013000; NVM ≤ 4KB (валидация addr в 0x221e6).
SPI_FLASH_BASE = 0x40013000   # SPI1 (MOSI/MISO к внешнему flash с NVM)
NVM_SIZE = 0x1000             # ≤4KB

# B3: агрегатор MCU→BLE (beacon 0x1F1CC + 24-состоянная машина 0x1F71C, §89)
TX_BCN_TABLE_OFF = 0xA43      # beacon-таблица: 4 слота (counter byte[0x2C1], wrap ≥4→0)
TX_BCN_SLOT = 0x96            # stride beacon-слота (0x1F1CC: 0x96*idx)
TX_BCN_C = bytes([4, 0x63, 0x44, 0xA7, 0x9C])        # beacon 'c' (0x1F1CC): {4,'c','D',0xA7,0x9C}
TX_BCN_C_DATA = bytes([6, 0x63, 0x63, 0, 0, 0x9C])   # beacon 'c' c данными (0x1F548): {6,'c','c',<byte>,Σcrc,0x9C}
TX_AGGR_SLOT_BASE = 0xC05     # слоты агрегатора (stride 0x96): classifier читает [slot+0..+3]
TX_AGGR_HEAD_OFF = 0x2C7      # «обработано» (head)
TX_AGGR_TAIL_OFF = 0x2C8      # «ожидает» (tail); guard: tail ≠ head иначе early-exit (0x2000C)
TX_AGGR_CLASS_OFF = 0x180     # класс агрегации (byte, 0x170+0x10)
TX_AGGR_FRAME_MAGIC = 0xA5    # магический конец фрейма {len,cmd,payload,XOR-crc,0xA5}
TX_RING_OFF = 0x10B5          # TX-ring (фреймы агрегатора строятся здесь, §77)


class TxAggregatorModel:
    """Scoped view of the MCU->BLE aggregator (B3, section 89). Beacon table @0xA43 (4 slots,
    counter byte[0x2C1]): beacon 'c' {4,'c','D',0xA7,0x9C} (0x1F1CC) and with data
    {6,'c','c',<byte>,Σcrc,0x9C} (0x1F548, the u64 'data ready'); beacon 'a'
    {4,<byte>,'a',0xC4,0x9C} (tail 0x211AE, counter wrap >=8->0). Aggregator 0x1F71C:
    a 24-state machine (jump table @0x1F77A) = a classifier over the slot bytes @0xC05
    (stride 0x96): byte[0] 'Q'-'T' -> class 1, 'd' -> 0x0A, 'Z' -> 0x14; byte[3]
    0xA0..0xA6/0xAE -> the frame builders; the class -> byte[0x180]; frames
    {len,cmd,payload,XOR-crc,0xA5} go to the TX ring 0x10B5 (r4 = 0x10B5 in isolation).
    Guard: byte[0x2C8] (tail) != byte[0x2C7] (head), otherwise early-exit; tail++ on
    each processing step.
    B3 (§89): scoped-вид на агрегатор MCU→BLE. Beacon-таблица @0xA43 (4 слота,
    counter byte[0x2C1]): beacon 'c' {4,'c','D',0xA7,0x9C} (0x1F1CC) и c данными
    {6,'c','c',<byte>,Σcrc,0x9C} (0x1F548, u64 «данные готовы»); beacon 'a'
    {4,<byte>,'a',0xC4,0x9C} (tail 0x211AE, counter wrap ≥8→0). Агрегатор 0x1F71C:
    24-состоянная машина (jump-table @0x1F77A) = classifier по байтам слота @0xC05
    (stride 0x96): byte[0] 'Q'-'T'→класс 1, 'd'→0x0A, 'Z'→0x14; byte[3] 0xA0..0xA6/0xAE
    → билдеры фреймов; класс → byte[0x180]; фреймы {len,cmd,payload,XOR-crc,0xA5} в
    TX-ring 0x10B5 (r4 = 0x10B5 в изоляции). Guard: byte[0x2C8] (tail) ≠ byte[0x2C7]
    (head), иначе early-exit; tail++ на каждую обработку."""
    def __init__(self, emu):
        """Bind the model to the emulator.
        Привязать модель к эмулятору."""
        self.emu = emu

    @property
    def beacon_counter(self):
        """The beacon slot counter byte[0x2C1] (wrap >=4->0).
        Счётчик beacon-слотов byte[0x2C1] (wrap ≥4→0)."""
        return self.emu.uc.mem_read(RAM + 0x2C1, 1)[0]

    def beacon_slot(self, i=0):
        """The content of beacon slot i of the table @0xA43 (16B).
        Содержимое beacon-слота i таблицы @0xA43 (16Б)."""
        return bytes(self.emu.uc.mem_read(RAM + TX_BCN_TABLE_OFF + i * TX_BCN_SLOT, 16))

    def set_beacon_counter(self, v):
        """Write the beacon counter byte[0x2C1].
        Записать счётчик beacon byte[0x2C1]."""
        self.emu.uc.mem_write(RAM + 0x2C1, bytes([v & 0xFF]))

    def aggr_slot(self, i=0):
        """The content of the aggregator slot @0xC05+0x96*i (16B).
        Содержимое слота агрегатора @0xC05+0x96*i (16Б)."""
        return bytes(self.emu.uc.mem_read(RAM + TX_AGGR_SLOT_BASE + i * TX_BCN_SLOT, 16))

    def set_aggr_state(self, head, tail):
        """Raise the guard: head=byte[0x2C7], tail=byte[0x2C8] (tail!=head -> the machine runs).
        Поднять guard: head=byte[0x2C7], tail=byte[0x2C8] (tail≠head → машинa идёт)."""
        self.emu.uc.mem_write(RAM + TX_AGGR_HEAD_OFF, bytes([head & 0xFF]))
        self.emu.uc.mem_write(RAM + TX_AGGR_TAIL_OFF, bytes([tail & 0xFF]))

    def aggr_class(self):
        """The aggregation class byte[0x180].
        Класс агрегации byte[0x180]."""
        return self.emu.uc.mem_read(RAM + TX_AGGR_CLASS_OFF, 1)[0]

    def tx_ring(self, n=0x96):
        """The TX ring content (n bytes from 0x10B5).
        Содержимое TX-ring (n байт от 0x10B5)."""
        return bytes(self.emu.uc.mem_read(RAM + TX_RING_OFF, n))

class SpiFlashModel:
    """A virtual buffer of the external SPI flash (NVM) + set/get (A3). The NVM content is
    the device runtime data (config/calibration); without a live dump the values are
    unknown -> the default is 0xFF (erased flash), the buffer is settable. SPI protocol:
    write-enable 0x221a4 (cmd = r0+1, e.g. 5->0x06) + page-program 0x221e6 (addr<0x4000,
    slot step 4B); NVRAM-save 0x21A08 persists 7+18B of config. The SPI context is the
    register block 0x40022000 (the internal FLASH controller, section 78.5): +0x00 low =
    start pulse (0xF0/0xF1), +0x04=cmd/len, +0x08=MOSI data, +0x14 bit31=ready gate
    (0xFFFFFFFF default = ready), +0x28=MISO byte (read/reset by 0x235b0). MISO return:
    SpiFlashMiso (a 25xxx state machine).
    A3: виртуальный буфер внешнего SPI-flash (NVM) + set/get. Содержимое NVM —
    runtime-данные устройства (конфиг/калибровка); без live-дампа значения неизвестны
    → дефолт 0xFF (стёртая flash), буфер settable. SPI-протокол: write-enable 0x221a4
    (cmd = r0+1, напр. 5→0x06) + page-program 0x221e6 (addr<0x4000, шаг слота 4Б);
    NVRAM-save 0x21A08 персистит 7+18Б конфига. **SPI-контекст = регистровый блок
    0x40022000** (внутренний FLASH-контроллер, §78.5): +0x00 low=старт-пульс (0xF0/
    0xF1), +0x04=cmd/len, +0x08=MOSI-дата, +0x14 bit31=ready-gate (0xFFFFFFFF по
    дефолту = ready), +0x28=MISO-байт (читает/сбрасывает 0x235b0). MISO-возврат:
    SpiFlashMiso (состоянийная машина 25xxx)."""
    def __init__(self, emu, size=NVM_SIZE):
        """Create the NVM buffer (erased to 0xFF).
        Создание буфера NVM (стёрт в 0xFF)."""
        self.emu = emu
        self.size = size
        self.flash = bytearray(b'\xff' * size)   # виртуальное содержимое NVM

    def set(self, addr, data):
        """Write data into the NVM at addr (emulating a page-program).
        Записать data в NVM по addr (эмуляция page-program)."""
        if addr < 0 or addr + len(data) > self.size:
            raise ValueError(f'NVM-адрес вне диапазона: {addr}+{len(data)} > {self.size}')
        self.flash[addr:addr + len(data)] = data

    def get(self, addr, n=1):
        """Read n bytes from the NVM at addr (emulating a read).
        Прочитать n байт из NVM по addr (эмуляция read)."""
        return bytes(self.flash[addr:addr + n])

    def seed(self, mapping):
        """Seed the NVM with a dict {addr: int_or_bytes} (for tests/simulation).
        Засеять NVM словарём {addr: int_or_bytes} (для тестов/симуляции)."""
        for addr, val in mapping.items():
            if isinstance(val, (bytes, bytearray)):
                self.set(addr, bytes(val))
            else:
                self.set(addr, val.to_bytes(max(1, (val.bit_length() + 7) // 8), 'little'))


# A3 (§78.5): SPI-контекст = регистровый блок внутреннего FLASH-контроллера @0x40022000
# (pool-литералы 0x235D0/0x23608/0x23612 → 0x40022000; хелперы 0x235b0/0x235d4/0x2360c/0x23688).
SPI_CTX_BASE = 0x40022000
SPI_CTX_CTRL = 0x00      # low-байт = старт-пульс: 0xF0 (clocking данных), 0xF1 (arm/0x235d4)
SPI_CTX_CMD = 0x04       # cmd/len: low24 |= команда (0x235d4), high-байт = cmd-байт (0x2360c),
                         #          len-поле = bits25..31 (0x23670: (len+3)>>2 | 0x7F)
SPI_CTX_MOSI = 0x08      # data-регистр (MOSI, u32; low-байт = байт, уходящий в flash)
SPI_CTX_READY = 0x14     # bit31 = ready/enable-гейт (0xFFFFFFFF по дефолту = ready)
SPI_CTX_MISO = 0x28      # MISO-байт-регистр (ответ flash; читает/сбрасывает 0x235b0)
SPI_CTX_WE_WORDS = (0x00112233, 0x55667788)  # write-enable handshake 0x23688 (два слова в +0x28)


class SpiFlashMiso:
    """SPI transaction model with the MISO return (A3, section 78.5). The SPI context is
    the register block 0x40022000: the MOSI bytes go out as writes to SPI_CTX_MOSI
    (0x40022008, low byte), the flash reply is **staged** by the model into SPI_CTX_MISO
    (0x40022028) — the firmware reads it as usual (0x235b0 — read + reset to 0). 25xxx
    protocol (NVM <=4KB, 16-bit addresses): 0x06 = write-enable (armed), 0x05/status ->
    MISO 0x00, 0x03 or 0x02 (not armed) = read: 3 address bytes -> NVM[addr] (page wrap
    0x100), 0x02 (armed) = page program: 3 addresses + data (AND into the NVM). The model
    is a companion to execution: it watches the MOSI writes (UC_HOOK_MEM_WRITE) and
    stages the MISO; the NVM data live in SpiFlashModel.flash (read-back after the run).
    A3 (§78.5): модель SPI-транзакции с MISO-возвратом. SPI-контекст — регистровый
    блок 0x40022000: MOSI-байты уходят записями в SPI_CTX_MOSI (0x40022008, low-байт),
    ответ flash модель **staged** в SPI_CTX_MISO (0x40022028) — firmware читает его
    как обычно (0x235b0 — чтение+сброс в 0). Протокол 25xxx (NVM ≤4KB, 16-битные
    адреса): 0x06 = write-enable (armed), 0x05/статус → MISO 0x00, 0x03 или 0x02
    (не armed) = read: 3 адреса-байта → NVM[addr] (page-wrap 0x100), 0x02 (armed)
    = page program: 3 адреса + данные (AND в NVM). Модель — companion к исполнению:
    наблюдает MOSI-записи (UC_HOOK_MEM_WRITE), стейджит MISO; данные NVM — в
    SpiFlashModel.flash (read-back после прогона)."""
    def __init__(self, emu, nvm=None):
        """Create the MISO model bound to an NVM buffer (a SpiFlashModel by default).
        Создание модели MISO, привязанной к буферу NVM (по дефолту SpiFlashModel)."""
        self.emu = emu
        self.nvm = nvm if nvm is not None else SpiFlashModel(emu)
        self.state = 'idle'     # idle | read | prog
        self.armed = False
        self.addr = 0
        self.abuf = []
        self.miso_log = []
        emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_write, None,
                        SPI_CTX_BASE + SPI_CTX_MOSI, SPI_CTX_BASE + SPI_CTX_MOSI + 3)

    def _on_write(self, uc, access, address, size, value, user_data):
        """MOSI write hook: feed the low byte into the state machine.
        Write-hook MOSI: передать low-байт в состоянийную машину."""
        self.feed(value & 0xFF)

    def _stage(self, b):
        """Stage a byte into the MISO register (+ log).
        Стейдж байта в MISO-регистр (+ лог)."""
        self.emu.uc.mem_write(SPI_CTX_BASE + SPI_CTX_MISO, struct.pack('<I', b))
        self.miso_log.append(b)

    def feed(self, b):
        """A state-machine step (manual driving; UC_HOOK_MEM_WRITE does not fire on
        manual mem_write). Шаг состоянии-машины (ручное приведение; UC_HOOK_MEM_WRITE не срабатывает
        на ручных mem_write)."""
        self._step(b)

    def _step(self, b):
        """The 25xxx protocol step: write-enable / status / read / page-program (AND).
        Шаг протокола 25xxx: write-enable / статус / read / page-program (AND)."""
        if b == 0x06:                       # WRITE ENABLE (в любом состоянии)
            self.armed = True
            self.state = 'idle'
            self.abuf = None
            return
        if b == 0x05:                       # READ STATUS
            self._stage(0x00)
            return
        if b in (0x02, 0x03):               # старт READ / PAGE PROGRAM
            self.state = 'prog' if self.armed else 'read'
            self.abuf = []
            return
        if self.state == 'idle':
            return                          # stray data
        if self.abuf is not None and len(self.abuf) < 3:
            self.abuf.append(b)
            return
        if self.abuf is not None:  # адрес только что собрался (MSB-first)
            self.addr = ((self.abuf[0] << 16) | (self.abuf[1] << 8) | self.abuf[2]) & 0x3FFF
            self.abuf = None
            if self.state == 'read':  # MISO-поток стартует сразу после адреса
                a = self.addr
                self._stage(self.nvm.get(a % 0x100, 1)[0])
                self.addr = (a + 1) % 0x100
            return
        a = self.addr
        if self.state == 'read':  # dummy-clock → следующий байт MISO
            self._stage(self.nvm.get(a % 0x100, 1)[0])
            self.addr = (a + 1) % 0x100
        else:  # prog: b = data-байт (AND в NVM)
            if a < self.nvm.size:
                self.nvm.set(a, bytes([self.nvm.get(a, 1)[0] & b]))
            self.addr = (a + 1) % 0x100
            self._stage(0x00)


# A4 (§90): SysTick / модель времени
SYST_CSR = 0xE000E010   # CTRL (ENABLE|TICKINT|TICK_REF; 7 = 1kHz с core clock)
SYST_RVR = 0xE000E014   # RELOAD (24 bit)
SYST_CVR = 0xE000E018   # CURRENT (24 bit)
SYST_DEFAULT_RVR = 0x1193F  # ~1 kHz @ 72 MHz (boot-значение §74)


class SysTickModel:
    """SysTick model + an instruction clock (A4, section 90). SysTick counts in the
    emulator's instruction clock (**1 insn = 1 count**): CVR decrements per instruction,
    underflow -> CVR = RVR (default 0x1193F), tick++ — this makes the firmware busy-wait
    delays deterministic: `0x229D4(r0, r1)` (delay r0×u32[0x24] counts, u16 repeats r1;
    CVR reset r4=0x00FFFFFF) and `0x22A0C(r0)` (the same with u32[0x10]; CVR reset via OR
    0x00FFFFFF) run for ~27 + r0×coeff instructions (r1=1; repeats accumulate). The full
    firmware context (0x19968 u32 division, 0x22934 clock-config, 0x1E2CA boot-init,
    0x11C84 TICK_REF, 0x3600 period, 0x11BAC date formatter) is detailed below in RU.
    A4 (§90): SysTick-модель + инструкционный clock. SysTick считает в
    инструкционном clock эмулятора (**1 insn = 1 count**): CVR декрементится на
    каждую инструкцию, underflow → CVR = RVR (default 0x1193F), tick++ — это
    делает firmware-busy-wait задержки детерминированными: `0x229D4(r0, r1)`
    (delay r0×u32[0x24] counts, u16-повторы r1; CVR-reset r4=0x00FFFFFF) и
    `0x22A0C(r0)` (то же с u32[0x10]; CVR-reset via OR 0x00FFFFFF) исполняются
    ≈ 27 + r0×coeff инструкций (r1=1; повторы складываются). Firmware-контекст:
    `0x19968(a, b)` — u32-деление (shift-subtract, verified); `0x22934(&struct{
    u32 rvr, u32 cvr, b flag, b ctrl})` — clock-config: коэффициенты через 0x19968:
    u32[0x1C] = base/0x3E8 (÷1000, ticks/ms), u32[0x20] = base/0x2710 (÷10000),
    u32[0x24] = base/0x186A0 (÷100000) (base = u32[0x08], ÷8 если struct[8]==0;
    пул-значения — константы, НЕ deref) + RVR/CVR/CTRL из struct (CTRL =
    (flag<<2) | ctrl); `0x1E2CA` — boot-init (RVR=r0−1, CVR=0, CTRL=7);
    `0x11C84(r0)` — r0==4 → CTRL |= 4 (TICK_REF on), иначе CTRL &= ~4;
    `0x35EC` — TICKINT off; `0x3600(ticks)` — период: bl 0x11C84 (build-quirk:
    bl ставит r0=4 → TICK_REF on), reload из LUT 0xC708 (data @0x6A00; zero-
    контекст → 0 → skip-путь), r1 = udiv(retval, 1000), RVR = r1−1 (если <
    0x1000000) + tail CVR=0/CTRL=7 (skip-путь их пропускает → CTRL остаётся 0x4);
    `0x11BAC(&out, sec)` — форматтер даты/времени (дивизоры 31104000/2592000/
    86400/3600/60, §61 100/100). Software-tick: u16[0x2BA]++ в периодическом
    task 0x1DFD8 (§59.8) + main u32[0x314]++."""
    def __init__(self, emu, rvr=None):
        """Create the SysTick model (optional RVR seed) + the per-instruction hook.
        Создание модели SysTick (опц. seed RVR) + hook на инструкцию."""
        self.emu = emu
        self._enabled = True
        self.tick_count = 0
        if rvr is not None:
            emu.uc.mem_write(SYST_RVR, struct.pack('<I', rvr & 0x00FFFFFF))
        self._hook = emu.uc.hook_add(UC_HOOK_CODE, self._on_insn)

    def _on_insn(self, uc, address, size, user):
        """Per-instruction tick: CVR -= 1; underflow -> CVR = RVR (or default) + tick++.
        Tick на инструкцию: CVR -= 1; underflow → CVR = RVR (или default) + tick++."""
        if not self._enabled:
            return
        cvr = struct.unpack_from('<I', uc.mem_read(SYST_CVR, 4), 0)[0] & 0x00FFFFFF
        rvr = struct.unpack_from('<I', uc.mem_read(SYST_RVR, 4), 0)[0] & 0x00FFFFFF
        cvr -= 1
        if cvr < 0:
            cvr = rvr if rvr else SYST_DEFAULT_RVR
            self.tick_count += 1
        uc.mem_write(SYST_CVR, struct.pack('<I', cvr))

    @property
    def ctrl(self):
        """The SysTick CTRL register value.
        Значение SysTick-регистра CTRL."""
        return struct.unpack_from('<I', self.emu.uc.mem_read(SYST_CSR, 4), 0)[0]

    @property
    def rvr(self):
        """The SysTick RELOAD register value.
        Значение SysTick-регистра RELOAD."""
        return struct.unpack_from('<I', self.emu.uc.mem_read(SYST_RVR, 4), 0)[0]

    @property
    def cvr(self):
        """The SysTick CURRENT register value.
        Значение SysTick-регистра CURRENT."""
        return struct.unpack_from('<I', self.emu.uc.mem_read(SYST_CVR, 4), 0)[0]

    def close(self):
        """Disable the model and remove the hook.
        Выключить модель и снять hook."""
        self._enabled = False
        self.emu.uc.hook_del(self._hook)


class TimeModel:
    """Reference time model (A4, section 90): SysTick (ticks/ms) + the 0x11BAC formatter
    (total-seconds -> 6 bytes {v//31104000, (v%31104000)//2592000, .../86400, /3600,
    /60, v%60} ~ a 360d year/30d month/day/hour/minute/second). `format_datetime` calls
    the real firmware code 0x11BAC; `ref_datetime` is the reference computation (the same
    contract, section 61 100/100).
    A4 (§90): референс-модель времени: SysTick (ticks/ms) + 0x11BAC-форматтер
    (total-seconds → 6 байт {v//31104000, (v%31104000)//2592000, .../86400, /3600,
    /60, v%60} ≈ 360d-год/30d-месяц/день/час/мин/сек). `format_datetime` вызывает
    реальный firmware-код 0x11BAC; `ref_datetime` — reference-вычисление (тот же
    контракт, §61 100/100)."""
    _FMT_D = (31104000, 2592000, 86400, 3600, 60)

    def __init__(self, emu):
        """Bind the model to the emulator.
        Привязать модель к эмулятору."""
        self.emu = emu

    @staticmethod
    def ref_datetime(v):
        """Reference computation of the 6-byte date format (same contract as 0x11BAC).
        Reference-вычисление 6-байтового формата даты (тот же контракт, что у 0x11BAC)."""
        out = [(v // TimeModel._FMT_D[0]) & 0xFF]
        for i in range(1, len(TimeModel._FMT_D)):
            out.append(((v % TimeModel._FMT_D[i - 1]) // TimeModel._FMT_D[i]) & 0xFF)
        out.append((v % TimeModel._FMT_D[-1]) & 0xFF)
        return out

    def format_datetime(self, total_seconds, buf_off=0x400):
        """Call 0x11BAC(&out, seconds) on the live code -> the 6-byte out.
        Вызов 0x11BAC(&out, seconds) на живом коде → 6-байтовый out."""
        uc = self.emu.uc
        uc.mem_write(RAM + buf_off, bytes(6))
        uc.reg_write(UC_ARM_REG_R0, RAM + buf_off)
        uc.reg_write(UC_ARM_REG_R1, total_seconds & 0x3FFFFFFF)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        try:
            uc.emu_start(0x11BAC | 1, 0, count=80)
        except Exception:
            pass
        return bytes(uc.mem_read(RAM + buf_off, 6))


# A5 (§91): I2C-модель — I2C2-чип (dev 0x3E) + shadow-регистровая семья
I2C2_BASE = 0x40005800   # I2C2-блок (кастомная периферия; dev-чип 0x3E)
I2C1_BASE = 0x40005400   # I2C1-блок (датчики/EEPROM; B1: тот же блок = power-стадия 1)
I2C2_DEV = 0x3E          # адрес устройства на шине
I2C2_SHADOW_BASE = 0x15FA  # RAM-блок «теневых регистров» чипа (0x15FA..0x164C)
I2C2_FP_STRUCT = 0xDD8   # struct-указатель в RAM (field +0x118 = send-примитив blx из 0x8f7c)
I2C2_FP_SEND = 0x118
I2C2_READER_OUT = 0xF95  # u16-результаты reader'ов: +0x1E / +0x20

# 22 setter'а (0x20C4..0x2358): reg → shadow-офсет (парсинг дизасма, §91)
I2C2_SHADOW_OFFS = {
    0x03: 0x15FA, 0x05: 0x15FC, 0x07: 0x15FE,
    0x12: 0x1607, 0x14: 0x1609, 0x16: 0x160B, 0x18: 0x160D, 0x1A: 0x160F,
    0x1C: 0x1611, 0x1E: 0x1613, 0x20: 0x1615, 0x22: 0x1617, 0x24: 0x1619,
    0x26: 0x161B, 0x28: 0x161D, 0x2A: 0x161F, 0x32: 0x1621,
    0x36: 0x162B, 0x38: 0x162D, 0x3A: 0x162F, 0x70: 0x163F, 0x7F: 0x164B,
}
# адреса setter'ов (val=8, len=1 для 0x03/0x05/0x07, len=2 для остальных)
I2C2_SETTERS = {
    0x03: 0x231C, 0x05: 0x2330, 0x07: 0x2344,
    0x12: 0x21DC, 0x14: 0x21F0, 0x16: 0x2204, 0x18: 0x2218, 0x1A: 0x222C,
    0x1C: 0x2240, 0x1E: 0x2254, 0x20: 0x2268, 0x22: 0x227C, 0x24: 0x2290,
    0x26: 0x22A4, 0x28: 0x22B8, 0x2A: 0x22CC, 0x32: 0x22E0,
    0x36: 0x2138, 0x38: 0x20C4, 0x3A: 0x22F4, 0x70: 0x2358, 0x7F: 0x2308,
}


class I2cModel:
    """I2C model — the I2C2 chip (dev 0x3E) + the shadow-register family (A5, section 91).

    Architecture (statics section 49.1/50 + dynamics section 91): the I2C2 block at
    0x40005800 (custom periph; block B1 uses as power stage 2 — bit21/22 pulses),
    I2C1 at 0x40005400 (sensors/EEPROM; B1: power stage 1). The external chip is dev
    0x3E (motor controller/sensor hub; identification = task B via snooping). The shadow
    layer at RAM+0x15FA..0x164C: 22 setters (0x20C4..0x2358, val=8, len 1/2) write the
    fixed chip registers {3,5,7, 0x12..0x2A, 0x32, 0x36, 0x38, 0x3A, 0x70, 0x7F} (the
    I2C2_SHADOW_OFFS table). Chain: setter -> 0x1C60 -> 0x1E52 -> 0x214C -> 0x8F7C (the
    I2C frame sender with the CRC-7 parity verification). Readers: 0x1C1C (read
    transaction + 1000-iteration timeout), 0x1BDC/0x1C7A/0x155AC (results ->
    u16@0xF95+0x1E/0x20), 0x218C (the read cycle reg 0x83 len 2). The model: a scoped
    view — the shadow layer (get/set/seed), the I2C2-block periph capture, and
    ref_frame(val, reg, data) — the reference frame build (the header + the data
    parities with the chained CRC-7, the same algorithm as the 0x8F7C loop).
    A5 (§91): I2C-модель — I2C2-чип (dev 0x3E) + shadow-регистровая семья.

    **Архитектура (статика §49.1/§50 + динамика §91):**
    - I2C2-блок @`0x40005800` (кастомная периферия; тот же блок B1 использует
      как power-стадию 2 — импульсы bit21/22), I2C1 @`0x40005400` (датчики/EEPROM;
      B1: power-стадия 1). Внешний чип — dev `0x3E` (мотор-контроллер/сенсорный
      хаб; идентификация = B-задача по снупу).
    - **Shadow-слой** @RAM+0x15FA..0x164C: 22 setter'а (0x20C4..0x2358, val=8,
      len 1/2) пишут фикс. регистры чипа {3,5,7, 0x12..0x2A, 0x32, 0x36, 0x38,
      0x3A, 0x70, 0x7F} — таблица I2C2_SHADOW_OFFS. Цепочка: setter →
      `0x1C60(val, reg, &shadow, len)` → `0x1E52(·,1,·,·)` → `0x214C(0, val,
      reg, len)` → **`0x8F7C(0x40005800, val, reg, out)`**.
    - **0x8F7C** = I2C-фрейм-отправщик с **CRC-7 par-верификацией**: буфер 0x48
      (memset), pre-roll цепочка `sb = crc7(crc7(crc7(0, u8(val<<1)), reg),
      u8(val)|1)` (0x3C7C), `blx u32[RAM+0xDD8+0x118]` (send-примитив; zero-
      контекст → 0 → векторные байты), затем цикл r4=0..r7 (r7 = верхний байт
      varargs-счётчика [sp+0x78], clamp (sl<<25)>>24 > 0x46 → ret 0): чётные
      → out[i]=frame[i], нечётные → `frame[i] == crc7(frame[i-1], sb)` иначе
      ret 0. Возврат 0 из blx = успех → ret 1.
    - **Reader'ы:** `0x1C1C(reg16, len)` — буфер {reg_lo, reg_hi}, dev 0x3E,
      val 8 → `0x90A0` (read-транзакция) → при ret≠0 **1000-iteration timeout**
      → ret 1 (zero-контекст: 0x90A0-цепь крутится, periph u16 0xFFFF @0x40005800);
      `0x1BDC(reg)`/`0x1C7A(val, reg, &buf, len)`/`0x155AC` — варианты (результат
      → u16@0xF95+0x1E/0x20); `0x218C()` — read-cycle reg 0x83 len 2.
    - **Модель:** scoped-вид — shadow-слой (get/set/seed), periph-захват
      I2C2-блока, `ref_frame(val, reg, data)` — reference-сборка фрейма
      (заголовок + data-par'ы с chained CRC-7, тот же алгоритм что цикл
      0x8F7C)."""

    def __init__(self, emu):
        """Bind the model to the emulator.
        Привязать модель к эмулятору."""
        self.emu = emu

    def shadow_addr(self, reg):
        """The RAM address of the chip register shadow.
        RAM-адрес shadow-регистра чипа."""
        return RAM + I2C2_SHADOW_OFFS[reg]

    def shadow_get(self, reg):
        """Read the chip register shadow byte.
        Прочитать shadow-байт регистра чипа."""
        return self.emu.uc.mem_read(RAM + I2C2_SHADOW_OFFS[reg], 1)[0]

    def shadow_set(self, reg, value):
        """Write the chip register shadow byte.
        Записать shadow-байт регистра чипа."""
        self.emu.uc.mem_write(RAM + I2C2_SHADOW_OFFS[reg], bytes([value & 0xFF]))

    def i2c2_writes(self):
        """The periph writes into the I2C2 block @0x40005800 [(pc, addr, size, value)].
        periph-записи в I2C2-блок @0x40005800 [(pc, addr, size, value)]."""
        out = []
        for w in self.emu.periph_writes:
            if I2C2_BASE <= w[1] < I2C2_BASE + 0x100:
                out.append(w)
        return out

    @staticmethod
    def _crc7(byte, state):
        """A port of 0x3C7C (the same as fv_core.ref_crc7_port): (state^byte) +
        8×((<<1)&0xFF ^ (msb?7:0)).
        Порт 0x3C7C (тот же, что fv_core.ref_crc7_port): (state^byte) +
        8×((<<1)&0xFF ^ (msb?7:0))."""
        r0 = (state ^ byte) & 0xFF
        for _ in range(8):
            if r0 & 0x80:
                r0 = ((r0 << 1) & 0xFF) ^ 7
            else:
                r0 = (r0 << 1) & 0xFF
        return r0

    @classmethod
    def ref_frame(cls, val, reg, data):
        """Reference build of the 0x8F7C I2C frame: frame = [d0, c0, d1, c1, ...]
        (the data parities), where c0 = crc7(d0, sb_pre), ci = crc7(di, c(i-1));
        sb_pre = the pre-roll chain crc7(crc7(crc7(0, u8(val<<1)), reg), u8(val)|1) —
        the header {val<<1, reg, val|1} is NOT in the frame, it only seeds the CRC
        (the same algorithm as the 0x8F7C verification loop: even -> copy to out,
        odd -> frame[i] == crc7(frame[i-1], sb)).
        Reference-сборка I2C-фрейма 0x8F7C: frame = [d0, c0, d1, c1, ...]
        (data-par'ы), где c0 = crc7(d0, sb_pre), ci = crc7(di, c(i-1));
        **sb_pre = pre-roll цепочка** crc7(crc7(crc7(0, u8(val<<1)), reg),
        u8(val)|1) — заголовок {val<<1, reg, val|1} НЕ входит в фрейм, только
        сеет CRC (тот же алгоритм, что цикл верификации 0x8F7C: чётные → copy
        в out, нечётные → frame[i] == crc7(frame[i-1], sb))."""
        sb = cls._crc7((val & 0x7F) << 1, 0)
        sb = cls._crc7(reg & 0xFF, sb)
        sb = cls._crc7((val & 0xFF) | 1, sb)
        frame = []
        for d in data:
            sb = cls._crc7(d & 0xFF, sb)
            frame.append(d & 0xFF)
            frame.append(sb & 0x7F)
        return bytes(frame)


# A6 (§92): NVRAM-зоны (RAM-копии с CRC) — layout + CRC-8/CRC-16-референс
NV_CRC8_POLY = 0x2F      # полином CRC-8 (0x87F8, init 0, MSB-first)
NVM_Z30DD = 0x30DD       # зона 32Б: 24Б данных + CRC-8 @0x18 (0x13B14)
NVM_Z30DD_DATA_LEN = 0x18   # 24Б данных (CRC-8 по ним)
NVM_Z30DD_CRC_OFF = 0x18    # храненный CRC-8 байт
NVM_Z30DD_SIZE = 0x20
NVM_Z30CF = 0x30CF       # зона CRC-16 (0x147AC; табл. @0x08019584/0x08019684 = 0xFF в образе)
NVM_Z304C = 0x304C       # зона read 512Б (0xCFB8)
NVM_Z305C = 0x305C       # зона read 40Б (0xCF60)
NVM_CRC16_TABLES = (0x08019584, 0x08019684)  # hi/lo для 0x8A50 (0xFF в образе — строятся в runtime)
NV_CRC16_POLY = 0x1021     # полином CRC-16 (CCITT), non-reflected — статически выводим (§96)
NVM_CRC16_TABLE16 = 0x08019784  # 16-bit таблица для 0x3C4C (init 0)
# §96: NVRAM save-list @0x1A550 — 26Б = 6 u32-адресов (RAM+TIM1 CCR1) + 2Б трейлер;
# 0x2D5C персистит их во внешнюю NVM через 0x332C (transform 0x163B4 + checksum 0x87B0);
# 0x5C9C: magic 0xAAAA @0x40003000 + 2Б из 0x19B14 (F1 FA) + flush 0xC20C(1)
NVM_SAVELIST_1A550 = 0x1A550
NVM_SAVELIST_ENTRIES = (0x20000258, 0x2000025C, 0x40012C40,  # TIM1 CCR1
                        0x2000026B, 0x2000024C, 0x94E)
NVM_SAVELIST_SIZE = 0x1A   # 26Б


class NvmZoneModel:
    """NVRAM zones (RAM copies with CRC) — the layout + the CRC references (A6, section 92).

    Architecture (statics section 50 + dynamics section 92): four NVRAM-zone RAM copies
    are verified by CRC after being read from the flash: 0x13B14 (the zone @0x30DD, 32B:
    24B of data + the CRC-8 byte @0x18, ret 0/1), 0x147AC (the zone @0x30CF: the
    table-based CRC-16 0x8A50, init 0xFFFF, the tables @0x08019584/0x08019684 are 0xFF in
    the image — built at runtime), 0xCFB8 (the zone @0x304C, 512B read + timeout) and
    0xCF60 (@0x305C, 40B read + timeout). The CRC-8 (0x87F8) is self-contained (the
    polynomial is in the code, no tables): live-verified 7/7. The CRC-16 is closed
    statically (section 96): both variants (0x3C4C init 0, the 16-bit table
    @0x08019784; 0x8A50 init 0xFFFF, hi/lo @0x08019584/0x08019684) are non-reflected ->
    the polynomial 0x1021 (CCITT) (init 0xFFFF over "123456789" = 0x29B1, the documented
    CCITT check value); the image tables are 0xFF (built from the polynomial at runtime)
    and are regenerated by crc16_ccitt. Isolated contract (NVM=0xFF): 0x13B14 ->
    zone=0xFF×32, CRC8(0xFF×24) != 0xFF -> ret=1 (FAIL), insn~5999 (the 100-iteration
    delay + the re-read).
    A6 (§92): NVRAM-зоны (RAM-копии с CRC) — layout + CRC-референс.

    **Архитектура (статика §50 + динамика §92):** четыре RAM-копии NVRAM-зон
    верифицируются CRC после чтения из flash:
    - **0x13B14** (зона @`0x30DD`, 32Б): `0x8380` читает 0x20Б из NVM → RAM-копию;
      если OK — 100-iteration задержка + **re-read** (стабильность); **CRC-8**
      (`0x87F8`, poly 0x2F) по первым **24Б** сверяется с храненным байтом
      `[zone+0x18]` → ret 0 (OK) / 1 (FAIL). **Layout: [0x00..0x17]=данные,
      [0x18]=CRC-8, [0x19..0x1F]=резерв.**
    - **0x147AC** (зона @`0x30CF`): CRC-16 табличный (`0x8A50`, init 0xFFFF,
      hi/lo-таблицы @0x08019584/0x08019684 — **0xFF в образе**, live-задача);
      в изоляции крутится до max_insn.
    - **0xCFB8** (зона @`0x304C`, 512Б) / **0xCF60** (@`0x305C`, 40Б): read +
      timeout (без явной CRC-сверки в хвосте).
    **CRC-8 (0x87F8)** — самодостаточен (poly в коде, без таблиц): live verified
    7/7. **CRC-16 — статически закрыт (§96):** два варианта — `0x3C4C` (init 0x0000,
    16-bit таблица @0x08019784) и `0x8A50` (init 0xFFFF, hi/lo @0x08019584/0x19684);
    оба non-reflected → полином **0x1021 (CCITT)** (init 0xFFFF по "123456789" =
    0x29B1, документированный CCITT check). Таблицы в образе 0xFF (строятся в runtime
    из полинома) — регенерируются `crc16_ccitt`. **Изолированный контракт**
    (NVM=0xFF): 0x13B14 → зона=0xFF×32, CRC8(0xFF×24) ≠ 0xFF → ret=1 (FAIL),
    insn≈5999 (100-итер-задержка + re-read)."""

    def __init__(self, emu):
        """Bind the model to the emulator.
        Привязать модель к эмулятору."""
        self.emu = emu

    @staticmethod
    def crc8(data, poly=NV_CRC8_POLY, init=0):
        """CRC-8 (0x87F8): MSB-first, init 0, poly 0x2F, no final-xor/reflect.
        CRC-8 (0x87F8): MSB-first, init 0, poly 0x2F, без final-xor/reflect."""
        crc = init
        for b in data:
            crc ^= b
            for _ in range(8):
                crc = ((crc << 1) ^ poly) & 0xFF if (crc & 0x80) else (crc << 1) & 0xFF
        return crc

    @staticmethod
    def crc16_ccitt(data, init=0, poly=NV_CRC16_POLY):
        """CRC-16 (CCITT 0x1021, non-reflected) — the reference for 0x3C4C (init 0) /
        0x8A50 (init 0xFFFF). The 0x3C4C algorithm: idx=byte^(crc>>8), crc=(crc<<8)^T16[idx].
        The image tables are 0xFF (built from the polynomial at runtime) — regenerated
        here. Check: init 0xFFFF over "123456789" = 0x29B1 (the documented CCITT check).
        CRC-16 (CCITT 0x1021, non-reflected) — референс для 0x3C4C (init 0) /
        0x8A50 (init 0xFFFF). Алгоритм 0x3C4C: idx=byte^(crc>>8), crc=(crc<<8)^T16[idx].
        Таблицы в образе 0xFF (строятся в runtime из полинома) — регенерируются здесь.
        Проверка: init 0xFFFF по "123456789" = 0x29B1 (документированный CCITT check)."""
        crc = init
        for b in data:
            crc ^= b << 8
            for _ in range(8):
                crc = ((crc << 1) ^ poly) if (crc & 0x8000) else (crc << 1)
                crc &= 0xFFFF
        return crc

    def zone_read(self, off, size):
        """The zone RAM copy (off = the RAM offset).
        RAM-копия зоны (off = RAM-смещение)."""
        return bytes(self.emu.uc.mem_read(RAM + off, size))

    def zone_crc8_valid(self, off, data_len=NVM_Z30DD_DATA_LEN, crc_off=NVM_Z30DD_CRC_OFF):
        """Verify the zone CRC-8: CRC8(data) == the stored byte @crc_off.
        Сверка CRC-8 зоны: CRC8(данные) == храненный байт @crc_off."""
        zone = self.zone_read(off, crc_off + 1)
        return self.crc8(zone[:data_len]) == zone[crc_off]


# B1: кастомный блок управления командами @0x40021000 (u32-поля +0x10/+0x18/+0x1c).
CMD_CTRL_BASE = 0x40021000
CMD_CTRL_FIELDS = (0x10, 0x18, 0x1c)


class CmdControlModel:
    """A scoped view of the custom command-control block @0x40021000 (B1) — it catches
    the bit set/clear/pulse in the fields +0x10/+0x18/+0x1c (the primitives
    0xc664/0xc684/0xc6a4; the dispatcher 0x2e0c, the handler 0x97f4). The firmware
    writes are already in memory; the model mirrors them for inspection of "which
    control bits the command touched". The exact ID->bit table — via the command-ID from
    the RX parser (B2) / live.
    B1: scoped-вид на кастомный блок управления @0x40021000 — ловит set/clear/pulse
    битов в полях +0x10/+0x18/+0x1c (примитивы 0xc664/0xc684/0xc6a4; dispatcher 0x2e0c,
    handler 0x97f4). Записи firmware уже в памяти; модель зеркалирует для инспекции
    «какие управляющие биты пошевелила команда». Точная таблица ID→бит — через command-ID
    из RX-парсера (B2) / live."""
    def __init__(self, emu, base=CMD_CTRL_BASE):
        """Create the model for the control block (a write hook over base..base+0x40).
        Создание модели для блока управления (write-hook на base..base+0x40)."""
        self.emu = emu
        self.base = base
        self.ops = []      # [(pc, offset, value)] записи в поля блока
        self._hook = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                     None, base, base + 0x40)

    def _on_w(self, uc, access, address, size, value, user):
        """Record an operation: (pc, offset, value).
        Записать операцию: (pc, offset, value)."""
        self.ops.append((uc.reg_read(UC_ARM_REG_PC) & 0xFFFFF, address - self.base, value))

    def read(self, off):
        """Read a u32 field at the offset.
        Прочитать u32-поле по смещению."""
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(self.base + off, 4)))[0]

    def set(self, off, val):
        """Write a u32 to the field at the offset.
        Записать u32 в поле по смещению."""
        self.emu.uc.mem_write(self.base + off, struct.pack('<I', val & 0xFFFFFFFF))


# B2: USART3 RX-протокол (BLE→MCU) — ASCII-command-ID. Парсер 0x1e9e0 (1914 Б).
# 15 команд (ASCII-символы), 2 категории:
#   cat=2 (@ G K c)      — response/status-команды;
#   cat=0xa (остальные)  — SET-params.
# RX-кадр: [+1]=cmd(ASCII), [+2]=len/param, [+3..]=payload. Ответные кадры строятся
# с sub 'd'(0x64)/'e'(0x65) + sum-chk. RAM-карты хендлеров верифицированы
# динамикой эмулятора (2026-11-18, §80).
USART_RX_PARSER = 0x1E9E0
USART_RX_COMMANDS = {
    '@': (0x1EB92, 2,   'head++ только (без копирования payload)'),
    'G': (0x1EBAA, 2,   'frame-start len=20: ctx={6,\'e\',20,\'O\',\'K\',0x13,0x9A}, флаг 0x310=0, toggle++'),
    'K': (0x1EBDE, 2,   'frame-start len=0x1b: ctx={6,\'e\',0x1b,\'O\',\'K\',0x1a,0x9A}, флаг 0x369=0, toggle++'),
    'c': (0x1EC14, 2,   'frame-start len=0x53: ctx={6,\'e\',0x53,\'O\',\'K\',0x52,0x9a}, флаг 0x36f=0, toggle++'),
    'A': (0x1EC74, 0xA, 'telemetry-snapshot: ring[3..9]→0x2E8..0x2F1 (rev16/нибблы/бит-сплит) + resp {0xc,\'d\',0x20,7,data,crc,0x9b}'),
    'B': (0x1ED90, 0xA, 'SET: ring[3..8]→RAM+0x2CB..0x2D0 (6B), tail 0x2D1 (carry-over)'),
    'C': (0x1EDBA, 0xA, 'SET: ring[3..8]→RAM+0x2D2..0x2D7 (6B), tail 0x2D8 (carry-over)'),
    'F': (0x1EE86, 0xA, 'varlen-copy: clear 0x2F2..0x305 (20B) + ring[3..3+len)→0x2F2.., len≤0x14'),
    'D': (0x1EEB4, 0xA, 'SET+clamp: ring3→0x2E6, ring4→0x306 (min 0x64), ring6→0x308, ring8→0x30A, ring9→0x30C, 0x30E=0'),
    'E': (0x1EF08, 0xA, 'bulk u16 SET: 6 пар → u16-слоты 0x2DA+2k (k<6), 0x2E7=0'),
    'H': (0x1EF58, 0xA, 'SET 4B: ring[3..6]→0x354..0x357 + resp {9,\'d\',0x2c,4,d1..d4,crc,0x9b}'),
    'I': (0x1EFC8, 0xA, 'resp {5,\'d\',0x2e,0,crc,0x9b}, флаг 0x36a=0'),
    'J': (0x1F036, 0xA, 'resp {6,\'d\',0x2f,1,0,crc,0x9b}, флаг 0x36c=0'),
    '`': (0x1F0CA, 0xA, 'resp {5,\'d\',0x50,0,crc,0x9b}'),
    'a': (0x1F112, 0xA, 'resp {5,\'d\',0x51,0,crc,0x9b}'),
}


def usart_rx_cmd(cmd_byte):
    """Identify the USART3-RX command by its byte (ASCII) (B2). Returns
    (handler_off, cat, desc) or None for an unknown command.
    B2: идентифицировать USART3-RX команду по байту (ASCII). Возвращает
    (handler_off, cat, desc) или None для неизвестного cmd."""
    if isinstance(cmd_byte, int):
        cmd_byte = chr(cmd_byte)
    return USART_RX_COMMANDS.get(cmd_byte)


# B2-динамика (§80): RX-контекст 0x1e9e0 — RAM-адреса, верифицированные
# исполнением на эмуляторе (свежий RAM + state=1/head=0/toggle=0, crafted-кадры):
RX_STATE_OFF = 0x172      # byte: 0 → только 0x171=0; 1 → обработать 1 сообщение
RX_GATE_OFF = 0x171       # byte: гейт «RX-занят» — каждый проход 0x1e9e0 пишет сюда 0
RX_HEAD_OFF = 0x2C0       # byte: индекс ring-слота (0..2, wrap при ≥3)
RX_TOGGLE_OFF = 0x2C9     # byte: индекс context-слота (0..7, wrap при ≥8, frame-start)
RX_RING_OFF = 0x881       # кольцо: 3 слота × 150 B (0x96), кадр [1]=cmd [2]=len [3..]=payload
RX_RING_SLOT = 0x96       # stride ring-слота = 150 B
RX_CTX_BASE = 0x10B5      # база context-слотов (slot0 = TX-ring @0x10b5..)
RX_CTX_STRIDE = 0x96      # stride context-слота = 150 B (тот же, что ring)
RX_RET = 0x20000170       # константа возврата (хвост pop pc @0x1f0c8)
RX_FRAME_START_LEN = {'G': 20, 'K': 0x1B, 'c': 0x53}   # len в ctx[2] frame-start
RX_FLAG_OFF = {'G': 0x310, 'K': 0x369, 'c': 0x36F,     # frame-start/clear-флаги
               'I': 0x36A, 'J': 0x36C}                 # (все = 0)


class UsartRxContext:
    """A scoped view of the RX context 0x1e9e0 (B2 dynamics, section 80).
    cmd() -> the table; slot_base(slot) -> the context-slot address; ring_off(head, k)
    -> the address of the k-th byte of a ring frame; craft(cmd, payload) -> the frame
    bytes in the ring format. Response frame: crc = Σ ctx[1..] & 0xFF, checksum =
    0xFF - ctx[1] ('d' -> 0x9B, 'e' -> 0x9A).
    B2-динамика (§80): scoped-вид на RX-контекст 0x1e9e0.
    cmd() → таблица; slot_base(slot) → адрес context-слота; ring_off(head, k)
    → адрес k-го байта ring-кадра; craft(cmd, payload) → bytes кадра в ring-формат.
    Ответный кадр: crc = Σ ctx[1..] & 0xFF, checksum = 0xFF - ctx[1]
    ('d'→0x9B, 'e'→0x9A)."""

    @classmethod
    def slot_base(cls, slot):
        """The context-slot base address (slot 0..7).
        Базовый адрес context-слота (slot 0..7)."""
        return RAM + RX_CTX_BASE + (slot & 0xFF) * RX_CTX_STRIDE

    @classmethod
    def ring_off(cls, head, k=1):
        """The address of the k-th byte of the ring frame for the head index.
        Адрес k-го байта ring-кадра для индекса head."""
        return RAM + RX_RING_OFF + (head & 3) * RX_RING_SLOT + k

    @classmethod
    def craft(cls, cmd, payload=b''):
        """A frame in the ring format: [0]=0, [1]=cmd, [2]=len(payload), [3..]=payload.
        Кадр ring-формата: [0]=0, [1]=cmd, [2]=len(payload), [3..]=payload."""
        if isinstance(cmd, str):
            cmd = cmd.encode()[0]
        if cmd not in {ord(c) for c in USART_RX_COMMANDS}:
            raise ValueError(f'неизвестная RX-команда {cmd:#x}')
        return bytes([0, cmd, len(payload)]) + bytes(payload)


# C1: LUT-блоки range-эстиматора 0x1d898 (u32-слова, шаг 4; значения из NVM/live).
RANGE_LUT0_OFF = 0x614    # блок0: 0x614..0x6c4
RANGE_LUT0_WORDS = 45
RANGE_LUT1_OFF = 0x738    # блок1: 0x738..0x808
RANGE_LUT1_WORDS = 53
RANGE_FLAG_OFFS = (0x286, 0x290, 0x294, 0x29e, 0x2a8, 0x2ac)   # status-гейты (§73.13)


class LutModel:
    """A scoped view of the range-estimator LUT blocks @RAM+0x614 / RAM+0x738 (C1;
    u32 words, step 4). It catches the firmware READS (which offsets 0x1d898 scanned) and
    provides seed/get for synthetic/live values. The real values come from the NVM
    (a live dump); the default is 0. 0x1d898 scans both blocks, reading each word once
    (the table pass).
    C1: scoped-вид на LUT-блоки range-эстиматора @RAM+0x614 / RAM+0x738 (u32-слова,
    шаг 4). Ловит ЧТЕНИЯ firmware (какие оффсеты просканировал 0x1d898), seed/get для
    synthetic/live значений. Реальные значения — из NVM (live-дамп); дефолт 0. 0x1d898
    сканирует оба блока, читая каждое слово по разу (табличный проход)."""
    def __init__(self, emu):
        """Create the model + the read hooks over both LUT blocks.
        Создание модели + read-hooks на оба LUT-блока."""
        self.emu = emu
        self.reads = set()   # RAM-relative оффсеты, прочитанные firmware
        self._hooks = []
        for off, words in ((RANGE_LUT0_OFF, RANGE_LUT0_WORDS),
                           (RANGE_LUT1_OFF, RANGE_LUT1_WORDS)):
            h = emu.uc.hook_add(UC_HOOK_MEM_READ, self._on_r,
                                None, RAM + off, RAM + off + words * 4)
            self._hooks.append(h)

    def _on_r(self, uc, access, address, size, value, user):
        """Record the read RAM-relative offset.
        Записать прочитанный RAM-relative оффсет."""
        self.reads.add(address - RAM)

    def get_word(self, off):
        """Read a u32 word at the RAM offset.
        Прочитать u32-слово по RAM-оффсету."""
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(RAM + off, 4)))[0]

    def set_word(self, off, val):
        """Write a u32 word at the RAM offset.
        Записать u32-слово по RAM-оффсету."""
        self.emu.uc.mem_write(RAM + off, struct.pack('<I', val & 0xFFFFFFFF))

    def seed_block(self, off, words):
        """words: list[int] (or int = a constant over the whole block).
        words: list[int] (или int = константа на всё слово-блока)."""
        if isinstance(words, int):
            words = [words]
        for i, w in enumerate(words):
            self.set_word(off + i * 4, w)

    def scanned(self, off, words):
        """True if the firmware read all the block's words @off.
        True если firmware прочитал все слова блока @off."""
        return all((off + i * 4) in self.reads for i in range(words))


# C2: FOC-рутина 0x1a938 — value-gated pipeline (не дискретный FSM).
FOC_ROUTINE = 0x1A938
FOC_REF_OFF = 0x224        # u16 current-reference (upstream input)
FOC_P_OFF = 0x388          # u32 P = [ref] (1:1, §73.15)
FOC_PHASE_OFFS = (0x382, 0x384, 0x386)   # u16 PWM-фазы (финальный вывод FOC)
FOC_PHASE_CENTER = 1125    # center (idle): все фазы = 1125


class FocPipelineModel:
    """A scoped view of the FOC routine 0x1a938 as a value-gated pipeline (C2)
    (TIM capture -> cross/dot -> inline -> fixed-point -> 2D rotate -> sector -> PWM).
    NOT a discrete FSM: branches on values (currents/thresholds), not on a state
    register (section 60.3; single byte flags do not change the path). It catches the
    OUTPUTS (P@0x388, the PWM phases @0x382/4/6); a seed for the current-ref @0x224.
    Transfer: phases = 1125 ± ~0.0103·|ref| (the 2-phase split, section 73.14).
    C2: scoped-вид на FOC-рутину 0x1a938 как value-gated pipeline (TIM capture ->
    cross/dot -> inline -> fixed-point -> 2D rotate -> sector -> PWM). НЕ дискретный FSM:
    ветвления по значениям (токи/пороги), не по state-регистру (§60.3; одиночные byte-
    флаги путь не меняют). Ловит ВЫХОДЫ (P@0x388, PWM-фазы @0x382/4/6); seed для
    current-ref @0x224. Transfer: фазы = 1125 ± ~0.0103·|ref| (2-фазный split, §73.14)."""
    def __init__(self, emu):
        """Create the model + a write hook over the FOC outputs region.
        Создание модели + write-hook на регион выходов FOC."""
        self.emu = emu
        self.writes = {}   # RAM-off -> last value
        lo, hi = FOC_P_OFF - 0x10, max(FOC_PHASE_OFFS) + 8
        self._h = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                  None, RAM + lo, RAM + hi)

    def _on_w(self, uc, access, address, size, value, user):
        """Record the last write per RAM offset.
        Записать последнюю запись по RAM-оффсету."""
        self.writes[address - RAM] = value

    def set_ref(self, v):
        """Write the u16 current-reference @0x224.
        Записать u16 current-reference @0x224."""
        self.emu.uc.mem_write(RAM + FOC_REF_OFF, struct.pack('<H', v & 0xFFFF))

    def get_p(self):
        """Read the u32 P output @0x388.
        Прочитать u32-выход P @0x388."""
        return struct.unpack('<I', bytes(self.emu.uc.mem_read(RAM + FOC_P_OFF, 4)))[0]

    def get_phases(self):
        """Read the u16 PWM phases @0x382/4/6.
        Прочитать u16 PWM-фазы @0x382/4/6."""
        return tuple(struct.unpack('<H', bytes(self.emu.uc.mem_read(RAM + o, 2)))[0]
                     for o in FOC_PHASE_OFFS)


# D1: main-loop диспетчер 0x1f600 — round-robin по N слотам (потолок §74.1).
SCHEDULER_FN = 0x1F600
SCHED_SLOT_INDEX_OFF = 0x2C2   # byte текущий слот (wrap 0..3)
SCHED_SLOT_TABLE_OFF = 0xA43   # база slot-descriptor'ов, stride 0x96 (§74)
SCHED_SLOT_STRIDE = 0x96
SCHED_N_SLOTS = 4
SCHED_TICK_WORDS_OFF = 0x17F78   # u32-слова tick/last (эмпирика D1)


class SchedulerModel:
    """A scoped view of the main-loop dispatcher 0x1f600 (D1; round-robin over the N
    slots). It catches the state READS/WRITEs (slot_index @0x2C2, the slot table
    @0xA43 stride 0x96, the tick words @0x17F78+) and provides a seed for the slot_index.
    **The ceiling of section 74.1:** the task function pointers live in the runtime RAM
    (set at init); in a zeroed RAM the dispatch hits an unmapped fetch (a jump to 0) BEFORE
    finishing the rotation, because 0x1f600 reads a byte from the slot descriptor and
    calls 0x1f1c0 (store-byte) while the execution is separated and needs the runtime
    pointers.
    D1: scoped-вид на main-loop диспетчер 0x1f600 (round-robin по N слотам). Ловит
    ЧТЕНИЯ/ЗАПИСИ состояния (slot_index @0x2C2, slot-table @0xA43 stride 0x96, tick-слова
    @0x17F78+); seed для slot_index. **ПОТОЛОК §74.1:** task function-pointers — runtime
    RAM (set при init); в нулевом RAM dispatch упирается в unmapped fetch (jump to 0) ДО
    завершения ротации, т.к. 0x1f600 читает byte из slot-descriptor и вызывает 0x1f1c0
    (store-byte), а исполнение отделено и требует runtime-указателей."""
    def __init__(self, emu):
        """Create the model + full-RAM read/write hooks.
        Создание модели + read/write-hooks на весь RAM."""
        self.emu = emu
        self.reads = set()   # RAM-relative оффсеты, прочитанные
        self.writes = {}     # RAM-off -> last value
        self._hr = emu.uc.hook_add(UC_HOOK_MEM_READ, self._on_r,
                                   None, RAM, RAM + 0x20000)
        self._hw = emu.uc.hook_add(UC_HOOK_MEM_WRITE, self._on_w,
                                   None, RAM, RAM + 0x20000)

    def _on_r(self, uc, access, address, size, value, user):
        """Record the read RAM-relative offset.
        Записать прочитанный RAM-relative оффсет."""
        if RAM <= address < RAM + 0x20000:
            self.reads.add(address - RAM)

    def _on_w(self, uc, access, address, size, value, user):
        """Record the last write per RAM offset.
        Записать последнюю запись по RAM-оффсету."""
        if RAM <= address < RAM + 0x20000:
            self.writes[address - RAM] = value

    def set_slot_index(self, v):
        """Write the slot-index byte @0x2C2.
        Записать byte slot-index @0x2C2."""
        self.emu.uc.mem_write(RAM + SCHED_SLOT_INDEX_OFF, bytes([v & 0xFF]))

    def get_slot_index(self):
        """Read the slot-index byte @0x2C2.
        Прочитать byte slot-index @0x2C2."""
        return bytes(self.emu.uc.mem_read(RAM + SCHED_SLOT_INDEX_OFF, 1))[0]

    def touched(self, off):
        """True if the dispatcher read or wrote the offset @off.
        True если диспетчер прочитал или записал оффсет @off."""
        return off in self.reads or off in self.writes


class ControlLoop:
    """The autonomous motor loop — a time-driven warm-start (section 74).

    A virtual clock + the real firmware PID/FOC on every tick + the behavioral models
    plant/speed/battery/range. NOT a boot from reset and NOT the full scheduler (the
    slot table is set at runtime, boot-blocked section 73.15) — PID/FOC are called
    directly at their real rate (a valid loop abstraction: speed controller -> torque ->
    FOC).

    The chain per tick:
      measured_speed -> SpeedModel.set_speed (V)          [PID input]
      target -> PID 0x1d078 -> throttle s16[RAM+0x42c]     [real firmware]
      throttle -> current-ref u16[RAM+0x224] -> FOC 0x1a938 -> PWM CCR  [real firmware]
      throttle -> MotorModel.step -> speed                 [plant, first-order lag]
      throttle -> BatteryModel.discharge -> SoC            [discharge]
      SoC -> RangeModel.estimate -> the remaining range    [closed form]
    §74 Автономный моторный контур — time-driven warm-start.

    Виртуальные часы + реальный firmware PID/FOC на каждом tick + поведенческие модели
    plant/speed/battery/range. НЕ boot от reset и НЕ полный scheduler (slot-table
    устанавливается runtime, boot-blocked §73.15) — PID/FOC вызываются напрямую на их
    реальной частоте (валидная абстракция контура: speed-controller → torque → FOC).

    Цепочка на tick:
      measured_speed → SpeedModel.set_speed (V)          [вход PID]
      target → PID 0x1d078 → throttle s16[RAM+0x42c]     [реальный firmware]
      throttle → current-ref u16[RAM+0x224] → FOC 0x1a938 → PWM CCR  [реальный firmware]
      throttle → MotorModel.step → speed                 [plant, first-order lag]
      throttle → BatteryModel.discharge → SoC            [разряд]
      SoC → RangeModel.estimate → запас хода             [closed-form]
    """
    def __init__(self, emu=None, v_max=522.0, tau=15.0, throttle_ref=28624.0,
                 batt_rate=0.05, run_foc=True):
        """Create the control loop (an McuEmu by default) + all the models.
        Создание контура (по дефолту McuEmu) + все модели.

        throttle_ref = the full-scale PID output (0x42c ~28624..32760), NOT 4000
        (the section 73.9 default saturated the plant: the speed does not converge to
        the target but runs away to v_max).
        throttle_ref = full-scale PID-вывода (0x42c ~28624..32760), НЕ 4000 (§73.9 дефолт
        дал насыщение plant: speed не сходится к target, а уходит в v_max)."""
        self.emu = emu or McuEmu(max_insn=400000)
        self.sm = SpeedModel(self.emu)
        self.mm = MotorModel(self.emu, v_max=v_max, tau=tau,
                             throttle_ref=throttle_ref, dt=1.0)
        self.bm = BatteryModel(self.emu)
        self.rm = RangeModel(self.emu)
        self.tx = UsartTxSenderModel(self.emu)   # §96: TX-отправитель (0x1F600/0x1F1C0)
        self.batt_rate = float(batt_rate)
        self.run_foc = bool(run_foc)
        self.now = 0

    def setup(self, target, mode=3, soc=100.0):
        """Seed the RAM: the mode, the target, the power enable, the gates, the battery
        (see sections 73.9-73.15).
        Засеять RAM: режим, target, power-enable, гейты, батарея (см. §73.9-73.15)."""
        uc = self.emu.uc
        uc.mem_write(RAM, bytes(0x20000))
        uc.mem_write(RAM + 0x229, bytes([mode]))                          # mode
        uc.mem_write(RAM + 0x326, struct.pack('<H', target & 0xFFFF))     # target
        uc.mem_write(RAM + 0x339, b'\x00')
        uc.mem_write(RAM + 0x333, b'\x00')                                # skip mode-change
        uc.mem_write(RAM + 0x263, b'\x00')                                # gate → ramp-core
        uc.mem_write(RAM + 0x1760, struct.pack('<I', 32760))              # power enable
        uc.mem_write(RAM + 0x3C8 + 0x28, struct.pack('<H', 1))            # counter → phase B
        self.bm.set_soc(soc)
        self.mm.reset(0.0)
        self.now = 0

    def _in_flash(self, aa):
        """True if the address is inside the firmware code (flash0/flash1).
        True если адрес внутри кода firmware (flash0/flash1)."""
        L = self.emu.fw_len
        return (FLASH0 <= aa < FLASH0 + L) or (FLASH1 <= aa < FLASH1 + L)

    def _run_pid(self):
        """The real PID 0x1d078 -> the throttle s16[RAM+0x42c].
        Реальный PID 0x1d078 → throttle s16[RAM+0x42c]."""
        uc = self.emu.uc
        sh = uc.hook_add(UC_HOOK_CODE,
                         lambda u, a, s, ud: u.emu_stop() if not self._in_flash(a & ~1) else None)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        for r in (UC_ARM_REG_R0, UC_ARM_REG_R4):
            uc.reg_write(r, 0)
        try:
            uc.emu_start(PID_OFF | 1, 0, count=400000)
        except Exception:
            pass
        uc.hook_del(sh)
        return struct.unpack('<h', uc.mem_read(RAM + THROTTLE_OFF, 2))[0]

    def _run_foc(self, current_ref):
        """The real FOC 0x1a938 (R4=RAM+0x040, ref=u16[RAM+0x224]) -> the PWM CCR.
        Реальный FOC 0x1a938 (R4=RAM+0x040, ref=u16[RAM+0x224]) → PWM CCR."""
        uc = self.emu.uc
        r4 = RAM + FOC_CTX_OFF
        uc.mem_write(r4, bytes(0x80))
        uc.mem_write(r4 + 2, struct.pack('<h', 16384))
        uc.mem_write(RAM + CURR_REF_OFF, struct.pack('<H', current_ref & 0xFFFF))
        sh = uc.hook_add(UC_HOOK_CODE,
                         lambda u, a, s, ud: u.emu_stop() if not self._in_flash(a & ~1) else None)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x80)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R4, r4)
        uc.reg_write(UC_ARM_REG_R0, 0)
        try:
            uc.emu_start(FOC_OFF | 1, 0, count=200000)
        except Exception:
            pass
        uc.hook_del(sh)
        return tuple(struct.unpack('<H', uc.mem_read(RAM + o, 2))[0] for o in FOC_CCR_OFFS)

    def tick(self):
        """One loop step. Returns a state dict.
        Один шаг контура. Возвращает dict состояния."""
        self.sm.set_speed(int(self.mm.speed))          # measured speed → PID input
        thr = self._run_pid()                          # real firmware: PID → throttle
        self._last_thr = thr
        if self.run_foc:
            ccr = self._run_foc(thr & 0xFFFF)          # real firmware: FOC → PWM
            center = sum(ccr) / 3.0
            amp = max(abs(c - center) for c in ccr)
        else:
            amp = 0.0
        self.mm.step(thr)                              # plant: throttle → speed
        self.bm.discharge(thr, dt=1.0, rate=self.batt_rate)   # battery
        soc = self.bm.get_soc()
        v_batt = BatteryModel._raw(int(soc))           # SoC → сырое [415..535]
        X, R = self.rm.estimate(v_batt)                # запас хода (closed-form)
        tx_byte = self._emit_tx()                      # §96: телеметрия → TX-sender → USART3_DR
        self.now += 1
        return dict(t=self.now, speed=round(self.mm.speed, 1), throttle=thr,
                    pwm_amp=round(amp, 1), soc=round(soc, 2), range=R,
                    tx_byte=tx_byte, tx_sent=self.tx.sent)

    def _emit_tx(self):
        """Section 96: when ready — build the telemetry push frame and hand it to the TX
        sender (1 byte/tick).
        §96: при готовности — собрать push-фрейм телеметрии и отдать TX-sender (1 байт/tick)."""
        if self.tx._frame is None:   # предыдущий фрейм дослан
            sp = int(self.mm.speed)
            thr = self._last_thr if hasattr(self, '_last_thr') else 0
            frame = bytes([8, 0x41, (sp >> 8) & 0xFF, sp & 0xFF,
                           (thr >> 8) & 0xFF, thr & 0xFF,
                           (0x41 ^ sp ^ thr) & 0xFF, 0xA5])
            self.tx.load_frame(frame)
        return self.tx.tick()

    def run(self, ticks):
        """Run the given number of steps. Returns the list of states.
        Прогнать ticks шагов. Возвращает список состояний."""
        return [self.tick() for _ in range(ticks)]


# Phase ② (§94): main-loop tick-harness — виртуальное время + реальный планировщик 0x1f600
SCHED_NOW_OFF = 0x1E0       # u64 "сейчас" (low @0x1E0, high @0x1E4)
SCHED_DESC_OFF = 0x170      # descriptor: +0x28/+0x2C = last_tick (u64 @0x198/0x19C)
SCHED_LAST_OFF = 0x198      # = DESC+0x28 (low)
SCHED_CAP_OFF = 0x17B       # = DESC+0xB (cap slot-counter)
SCHED_PERIOD = 432          # межслотовый период (тик'ов)
SCHED_BYTE_PERIOD = 8       # межбайтовый период (overflow-путь)
COMM_TICK_FN = 0x1DFD8      # комм-тик (RX+TX+агрегатор+push, §22.1)
TIM1_BASE = 0x40012C00      # TIM1 (advanced) — 3-фазный ШИМ BLDC
TIM1_ISR_FN = 0x1A2A4       # реальный TIM1-IRQ (bit7 [base+0x1C] = update-событие)
TIM1_STATUS_OFF = 0x1C      # [base+0x1C] — статус (bit7 = update; lsls #0x18=<<24 тестит bit7)
TIM1_UPDATE_BIT = 0x80      # bit7 — update-событие
FOC_FN = 0x1A938            # FOC-расчёт (PID-выход → PWM CCR)

# Phase ③ (§95): cold-boot — векторная таблица + startup-цепочка
VEC_TABLE = 0x1000          # векторная таблица (НЕ @0x0 — там OTA-заголовок)
SP_INIT = 0x20004E40        # [VEC_TABLE+0] — initial stack pointer
RESET_VECTOR = 0x315C       # [VEC_TABLE+1] & ~1 — reset handler
BOOT_STAGE1_INIT = 0xCD0C   # stage 1: init (r0=SP) + busy-wait 0x2ff
BOOT_STAGE2 = 0x3168        # stage 2: init-цепочка (0xcc68/0xc9dc/0x5970/0xcb40)
BOOT_TRAMP2 = 0x31C6        # TRAMP2: pop {r4,pc} (возврат в init/next)
PENDSV_V14 = 0x3173         # вектор [14] = PendSV
SYSTICK_V15 = 0x13CAD       # вектор [15] = SysTick
FOC_ISR_V22 = 0x7875        # вектор [22] = FOC/моторный timer-ISR

# Phase ④ (§97): C-старт + main + task-цепь (коррекция §74.1)
BOOT_C_START = 0x1148       # C-старт: ldr.w sp,[=0x20004E40]; bl 0x14c4; bl 0x1150
BOOT_SP_LIT = 0x1158        # литерал SP=0x20004E40 для C-старта
BOOT_C_MAIN_LIT = 0x1154    # литерал main-адреса = 0x0801907B
BOOT_MAIN = 0x1907A         # main() — bx [0x1154]
BOOT_CONSTRUCT_WALKER = 0x14C4  # конструктор-тейбл (ldm r4!,{r0-r2}; blx [r4+0xc]|1)
BOOT_CONSTRUCT_TABLE = 0x1AD28  # таблица в FLASH: 2×16Б {a0,a1,a2,fn}
BOOT_CONSTRUCT_END = 0x1AD48
BOOT_CONSTRUCT_FN1 = 0x20000040  # desc1.fn — код в RAM (live, даёт ROM)
BOOT_CONSTRUCT_FN2 = 0x9E38      # desc2.fn — flash-инициализация (исполняется)
ADC_ISR_TICK = 0x1A31C    # ADC-ISR = системный тик (~1 кГц): статическая task-цепь
ADC_TASK_FOC = 0x1A938        # bl @0x1A49E
ADC_TASK_D3D0 = 0x1D3D0       # bl @0x1A514
ADC_TASK_SCHED = 0x1F600      # bl @0x1A518 (планировщик/TX USART3)
ADC_TASK_UART4 = 0x216E4      # bl @0x1A51C
ADC_TASK_SWSTART = 0x1A5C4    # bl @0x1A520 (SWSTART ADC)
APP_CFG_REGION = 0x0EE80000   # регион app-config, который main dereference (live)


class MainLoopHarness:
    """The autonomous main-loop tick harness (Phase 2, section 94; no hardware).

    A virtual clock: the u64 "now" @0x1E0. On every tick:
      now += 1 -> **0x1f600 (the real scheduler)** -> (optional) **FOC-ISR 0x1a2a4**
      on timer update -> (optional) 0x1dfd8 (the communication tick).
    **The scheduler contract (live-verified):** elapsed = now - last (u64 @0x198);
      - elapsed < 432 -> return (no dispatch);
      - elapsed >= 432 AND cap >= slot_counter+1 -> **main path**: slot_idx++, last := now;
      - elapsed >= 432 AND cap < slot_counter+1 -> **overflow path**: the inter-byte counter
        (8 ticks) ++, slot_idx unchanged.
    **FOC-ISR (0x1a2a4, the real TIM1 IRQ):** on timer update it sets bit7 [TIM1+0x1C]
    (the update event; lsls #0x18=<<24 tests bit7) -> bit7 set -> the handler path
    (~39 insns: clear the flag, set bit7 [base+0x20]); bit7 clear -> return (6 insns).
    **The section 95 correction:** 0x7875 is the real FOC/motor timer ISR (vector [22]
    of the vector table @0x1000, section 95) — NOT the "middle of a block" (earlier
    error); with a zeroed context the isolation goes to 0x7992, but in a real timer
    context it works. 0x1a2a4 is a different (TIM1) IRQ handler; both are real, the
    harness integrates 0x1a2a4 (clean/deterministic).
    This extends the "autonomous run" from ~45% (ControlLoop: PID+FOC) to the real
    main loop (scheduler + FOC-ISR + the communication tick) on virtual time. NOT a
    cold boot (the section 74.1 ceiling: task FP = runtime RAM) — the scheduler/ISR/comm
    tick are called directly.
    Phase ② (§94): автономный main-loop tick-harness (без железа).

    Виртуальные часы: u64 "now" @0x1E0. На каждый tick:
      now += 1 → **0x1f600 (реальный планировщик)** → (опц.) **FOC-ISR 0x1a2a4**
      по timer-update → (опц.) 0x1dfd8 (комм-тик).
    **Контракт планировщика (live verified):** elapsed = now − last (u64 @0x198);
      - elapsed < 432 → return (без диспатча);
      - elapsed >= 432 И cap >= slot_counter+1 → **main-путь**: slot_idx++, last := now;
      - elapsed >= 432 И cap < slot_counter+1 → **overflow-путь**: межбайтовый счётчик
        (8 тиков) ++, slot_idx без изменений.
    **FOC-ISR (0x1a2a4, реальный TIM1-IRQ):** на timer-update set bit7 [TIM1+0x1C]
    (update-событие; lsls #0x18=<<24 тестит bit7) → bit7 set → handler-путь
    (~39 insn: clear flag, set bit7 [base+0x20]); bit7 clr → return (6 insn).
    **Коррекция §95:** 0x7875 = реальный FOC/моторный timer-ISR (вектор [22] векторной
    таблицы @0x1000, §95) — НЕ «середина блока» (ранее ошибочно); при нулевом контексте
    изоляция уходит в 0x7992, но в реальном timer-контексте работает. 0x1a2a4 — другой
    (TIM1) IRQ-хендлер; оба реальные, в harness интегрирован 0x1a2a4 (чистый/детерминированный).
    Это расширяет «автономный прогон» с ~45% (ControlLoop: PID+FOC) к реальному
    main-loop (scheduler + FOC-ISR + комм-тик) на виртуальном времени. НЕ cold-boot
    (§74.1 потолок: task-FP = runtime RAM) — планировщик/ISR/комм-тик вызываются напрямую.
    """

    def __init__(self, emu=None, cap=1, run_comm=True, comm_period=1000,
                 run_foc=True, foc_period=1):
        """Create the harness (an McuEmu by default) + the counters.
        Создание harness (по дефолту McuEmu) + счётчики."""
        self.emu = emu or McuEmu(max_insn=400000)
        self.cap = int(cap)
        self.run_comm = bool(run_comm)
        self.comm_period = int(comm_period)   # комм-тик каждые N тиков (мс-счётчик)
        self.run_foc = bool(run_foc)          # FOC-ISR на timer-update
        self.foc_period = int(foc_period)     # период timer-update (тик'ов)
        self.now = 0
        self.dispatches = 0
        self.overflows = 0
        self.comm_ticks = 0
        self.foc_runs = 0
        self.foc_handler = 0

    def _in_flash(self, aa):
        """True if the address is inside the firmware code (flash0/flash1).
        True если адрес внутри кода firmware (flash0/flash1)."""
        L = self.emu.fw_len
        return (FLASH0 <= aa < FLASH0 + L) or (FLASH1 <= aa < FLASH1 + L)

    def _run(self, off, budget=200000):
        """Run the function at off in the flash, stopping on leaving the flash.
        Returns the number of instructions.
        Прогнать off в flash, остановиться на уходе из flash. Возвращает insn."""
        uc = self.emu.uc
        sh = uc.hook_add(UC_HOOK_CODE,
                         lambda u, a, s, ud: u.emu_stop() if not self._in_flash(a & ~1) else None)
        uc.reg_write(UC_ARM_REG_SP, STACK_TOP - 0x40)
        uc.reg_write(UC_ARM_REG_LR, 0x0BADF001)
        uc.reg_write(UC_ARM_REG_R0, 0)
        started = self.emu.insn
        try:
            uc.emu_start(off | 1, 0, count=budget)
        except Exception:
            pass
        uc.hook_del(sh)
        return self.emu.insn - started

    def reset(self, now=0, head=1):
        """Zero the RAM + seed the scheduler: now/last/tail/head/cap.
        The 4-slot ring: head@0x2C1 (the producer), tail/slot_idx@0x2C2 (the consumer);
        the dispatch goes from tail to head (exclusive); tail==head -> stop.
        Занулить RAM + засеять планировщик: now/last/tail/head/cap.
        Кольцо 4 слота: head@0x2C1 (продюсер), tail/slot_idx@0x2C2 (потребитель);
        диспатч идёт от tail до head (exclusive); tail==head → стоп."""
        uc = self.emu.uc
        uc.mem_write(RAM, bytes(0x20000))
        self.emu.hook_periph_ready()
        self._write_now(now)
        self.emu.uc.mem_write(RAM + SCHED_LAST_OFF, struct.pack('<Q', 0))
        self.emu.uc.mem_write(RAM + SCHED_SLOT_INDEX_OFF, bytes([0]))   # tail=0
        self.emu.uc.mem_write(RAM + 0x2C1, bytes([head & 0xFF]))          # head
        if self.cap:
            self.emu.uc.mem_write(RAM + SCHED_CAP_OFF, bytes([self.cap]))
        self.now = int(now)
        self.head = int(head)
        self.dispatches = 0
        self.overflows = 0
        self.comm_ticks = 0
        self.foc_runs = 0
        self.foc_handler = 0

    def foc_isr(self):
        """The FOC-ISR on timer update: set bit7 [TIM1+0x1C] (the update event) ->
        0x1a2a4 (the real TIM1 IRQ). Bit7 set -> the handler path (~39 insns: clear the
        flag, set bit7 [base+0x20], flags); bit7 clear -> the fast return (6 insns).
        Returns True if the handler path ran.
        FOC-ISR по timer-update: set bit7 [TIM1+0x1C] (update-событие) →
        0x1a2a4 (реальный TIM1-IRQ). bit7 set → handler-путь (~39 insn: clear flag,
        set bit7 [base+0x20], флаги); bit7 clr → быстрый return (6 insn).
        Возвращает True если handler-путь отработал."""
        self.emu.uc.mem_write(TIM1_BASE + TIM1_STATUS_OFF,
                              struct.pack('<I', TIM1_UPDATE_BIT))
        before = self.emu.insn
        self._run(TIM1_ISR_FN, budget=10000)
        used = self.emu.insn - before
        self.foc_runs += 1
        if used > 15:   # handler-путь (~39) vs быстрый return (6)
            self.foc_handler += 1
            return True
        return False

    def _write_now(self, now):
        """Write the u64 'now' @0x1E0.
        Записать u64 'now' @0x1E0."""
        self.emu.uc.mem_write(RAM + SCHED_NOW_OFF, struct.pack('<Q', now))

    def _read_last(self):
        """Read the u64 'last' @0x198.
        Прочитать u64 'last' @0x198."""
        return struct.unpack('<Q', self.emu.uc.mem_read(RAM + SCHED_LAST_OFF, 8))[0]

    def _read_slot_idx(self):
        """Read the slot-index byte @0x2C2.
        Прочитать byte slot-index @0x2C2."""
        return bytes(self.emu.uc.mem_read(RAM + SCHED_SLOT_INDEX_OFF, 1))[0]

    def sched_tick(self):
        """One tick of the scheduler 0x1f600. Returns 'main'/'overflow'/'idle'.
        main = last(@0x198) was updated (slot_idx++); overflow = the inter-byte counter
        (@0x1A0 = DESC+0x30) ++; idle = elapsed<432, the early return.
        Один такт планировщика 0x1f600. Возвращает 'main'/'overflow'/'idle'.
        main = last(@0x198) обновлён (slot_idx++); overflow = межбайтовый счётчик
        (@0x1A0 = DESC+0x30) ++; idle = elapsed<432, ранний return."""
        before_last = self._read_last()
        before_bp = struct.unpack('<I', self.emu.uc.mem_read(RAM + 0x1A0, 4))[0]
        self._run(SCHEDULER_FN)
        after_last = self._read_last()
        after_bp = struct.unpack('<I', self.emu.uc.mem_read(RAM + 0x1A0, 4))[0]
        if after_last != before_last:
            return 'main'
        if after_bp != before_bp:
            return 'overflow'
        return 'idle'

    def tick(self):
        """One main-loop step: now++ -> scheduler -> (optional) the communication tick.
        Один шаг main-loop: now++ → планировщик → (опц.) комм-тик."""
        self.now += 1
        self._write_now(self.now)
        res = self.sched_tick()
        if res == 'main':
            self.dispatches += 1
        elif res == 'overflow':
            self.overflows += 1
        ms = struct.unpack('<H', self.emu.uc.mem_read(RAM + 0x2BA, 2))[0]
        if self.run_foc and (self.now % self.foc_period == 0):
            self.foc_isr()
        if self.run_comm and (self.now % self.comm_period == 0):
            self._run(COMM_TICK_FN)
            self.comm_ticks += 1
        return dict(t=self.now, sched=res, slot_idx=self._read_slot_idx(),
                    last=self._read_last(), ms=ms,
                    dispatches=self.dispatches, overflows=self.overflows,
                    comm_ticks=self.comm_ticks, foc_runs=self.foc_runs,
                    foc_handler=self.foc_handler)

    def run(self, ticks):
        """Run the given number of steps. Returns the list of states.
        Прогнать ticks шагов. Возвращает список состояний."""
        return [self.tick() for _ in range(ticks)]


class BootHarness:
    """The cold-boot harness — a start from the reset vector (Phase 3, section 95; no
    hardware).

    **The vector table exists @0x1000** (the correction to section 16.3/"absent"):
      [0]=SP_INIT=0x20004E40, [1]=RESET_VECTOR|1=0x315d, [14]=PendSV, [15]=SysTick,
      [22]=FOC_ISR_V22=0x7875 (confirms the FOC-ISR from the "vector [22]" note).
    **The startup chain (live-verified):** reset 0x315c -> str 0,[sp] -> bl 0xcd0c
      (stage 1: init + busy-wait 0x2ff) -> TRAMP1 `pop {r1,r2,r3,pc}` @0x3166
      (pc=RAM[SP_INIT+12]=stage2|Thumb) -> **stage 2** 0x3168 (the init chain
      0xcc68/0xc9dc/0x5970/0xcb40) -> TRAMP2 `pop {r4,pc}` @0x31c6.
    **The ceiling (live):** the initial stack [SP_INIT..] = the C-runtime/loader data
      (the runtime RAM) — the startup reuses/overwrites the slots, so a full cold boot
      to a working main loop needs either a live RAM dump at reset (SWD GD32) or a
      full reconstruction of the C-runtime stack. The main-loop dispatch is via a
      runtime function pointer (the section 74.1 ceiling; there is no direct
      `bl 0x1f600`).
    `run()` deterministically drives the boot up to TRAMP2 (~6314 insns, periph=0xFF).
    Phase ③ (§95): cold-boot harness — старт с reset-вектора (без железа).

    **Векторная таблица существует @0x1000** (коррекция §16.3/«отсутствует»):
      [0]=SP_INIT=0x20004E40, [1]=RESET_VECTOR|1=0x315d, [14]=PendSV, [15]=SysTick,
      [22]=FOC_ISR_V22=0x7875 (подтверждает FOC-ISR из примечания «вектор [22]»).
    **Startup-цепочка (live verified):** reset 0x315c → str 0,[sp] → bl 0xcd0c
      (stage 1: init + busy-wait 0x2ff) → TRAMP1 `pop {r1,r2,r3,pc}` @0x3166
      (pc=RAM[SP_INIT+12]=stage2|Thumb) → **stage 2** 0x3168 (init-цепочка
      0xcc68/0xc9dc/0x5970/0xcb40) → TRAMP2 `pop {r4,pc}` @0x31c6.
    **Потолок (live):** initial stack [SP_INIT..] = данные C-runtime/загрузчика
      (runtime RAM) — startup переиспользует/перезаписывает слоты, поэтому полный
      cold-boot до работающего main-loop требует либо live-дампа RAM при reset
      (SWD GD32), либо полной реконструкции C-runtime-стека. Main-loop dispatch —
      через runtime function-pointer (потолок §74.1, прямых `bl 0x1f600` нет).
    `run()` детерминированно доводит boot до TRAMP2 (~6314 insn, periph=0xFF).
    **Phase ④ (§97):** `reset(c_start=True)` сидит [SP+12]=0x1149 (C-старт) —
    реальная цепочка: 0x1148 (SP из литерала 0x1158, bl 0x14C4 конструктор-
    тейбл) → desc2 0x9E38 (flash-инит) → bl 0x1150 → **bx main=0x1907A**;
    `run(patch_ram_callback=True)` перенаправляет live RAM-callback (desc1.fn=
    0x20000040, blob от ROM) в конец walker — детерминированно до main.
    """

    def __init__(self, emu=None, max_insn=500000):
        """Create the harness (an McuEmu by default).
        Создание harness (по дефолту McuEmu)."""
        self.emu = emu or McuEmu(max_insn=max_insn)
        self.max_insn = int(max_insn)
        self.insn = 0
        self.final_pc = 0
        self.reached = set()

    def reset(self, seed_stage2=BOOT_STAGE2, c_start=False):
        """Zero the RAM, SP=SP_INIT, seed the initial stack [SP+12]=stage2|Thumb
        (or the C-start 0x1149 when c_start — the Phase 4 entry, section 97).
        Занулить RAM, SP=SP_INIT, seed initial stack [SP+12]=stage2|Thumb
        (или C-старт 0x1149 при c_start — вход Phase ④, §97)."""
        uc = self.emu.uc
        uc.mem_write(RAM, bytes(0x20000))
        self.emu.hook_periph_ready()
        seed = BOOT_C_START if c_start else seed_stage2
        uc.mem_write(SP_INIT, struct.pack('<4I', 0, 0, 0, (seed | 1)))
        uc.reg_write(UC_ARM_REG_SP, SP_INIT)
        uc.reg_write(UC_ARM_REG_LR, 0xFFFFFFFF)
        self.insn = 0
        self.final_pc = 0
        self.reached = set()

    def run(self, patch_ram_callback=False):
        """Run the boot from RESET_VECTOR. Returns (insn, final_pc, reached).
        patch_ram_callback: the live RAM-code callback (0x20000040, the ROM-supplied
        blob) is rerouted to the walker end (r4=desc2, 0x14DB) — the Phase 4
        "reconstructed cold boot" to main. Прогнать boot от RESET_VECTOR.
        patch_ram_callback: live RAM-callback (0x20000040, blob от ROM) перенаправляется
        в конец walker (r4=desc2, 0x14DB) — реконструированный cold-boot до main."""
        uc = self.emu.uc
        last = [0]
        patched = [0]
        marks = {BOOT_STAGE1_INIT: 'stage1', BOOT_STAGE2: 'stage2',
                 BOOT_TRAMP2: 'tramp2', BOOT_C_START: 'cstart',
                 BOOT_MAIN: 'main'}

        def hc(u, a, s, ud):
            """CODE hook: the live-callback patch + the last PC + the boot marks.
            CODE-хук: патч live-callback + последний PC + отметки boot."""
            b = (a & ~1) & ~0x08000000
            if patch_ram_callback and not patched[0] \
                    and BOOT_CONSTRUCT_FN1 <= b < BOOT_CONSTRUCT_FN1 + 0x40:
                patched[0] = 1
                u.reg_write(UC_ARM_REG_R4, 0x08000000 + BOOT_CONSTRUCT_TABLE + 0x10)
                u.reg_write(UC_ARM_REG_PC, 0x14DB)
                return
            last[0] = b
            for m, name in marks.items():
                if m <= b < m + 0x40:
                    self.reached.add(name)
        uc.hook_add(UC_HOOK_CODE, hc)
        try:
            uc.emu_start(RESET_VECTOR | 1, 0, count=self.max_insn)
        except Exception:
            pass
        self.insn = self.emu.insn
        self.final_pc = last[0]
        return self.insn, self.final_pc, set(self.reached)


def find_func_starts():
    """Function starts = the push {..,lr} prologues (0xB5xx) in the code sections.
    Начала функций = пролог push {..,lr} (0xB5xx) в кодовых секциях."""
    import struct as _s
    d = open(FW, "rb").read()
    CODE = [(0x01200, 0x02400), (0x02600, 0x10200), (0x10400, 0x10e00),
            (0x11000, 0x12400), (0x12800, 0x13e00), (0x14200, 0x14400),
            (0x14600, 0x17a00), (0x18e00, 0x19200), (0x19a00, 0x24200),
            (0x24400, 0x24600)]
    starts = []
    for a, b in CODE:
        for o in range(a, b, 2):
            if (_s.unpack_from("<H", d, o)[0] & 0xFF00) == 0xB500:
                starts.append(o)
    return starts


def sweep_writers(target_lo=0x20000A00, target_hi=0x20000C10, cap=8000):
    """Run every function and find those that write to the descriptor region.
    A dynamic taint — what the static analysis cannot give (the base pointer is
    computed at runtime).
    Прогнать каждую функцию и найти те, что пишут в область дескрипторов.
    Динамический taint — то, чего статика не даёт (база указателя в рантайме)."""
    starts = find_func_starts()
    print(f"[sweep] функций: {len(starts)}, ищу запись в 0x{target_lo:08x}..0x{target_hi:08x}")
    hits = {}
    for idx, addr in enumerate(starts):
        emu = McuEmu(trace=False, max_insn=cap)
        emu.uc.mem_write(PERIPH, bytes(PERIPH_SIZE))
        emu.uc.mem_write(SYS, bytes(SYS_SIZE))
        recorded = []

        def on_w(uc, access, address, size, value, user):
            """MEM_WRITE hook: record the writes into the target region.
            MEM_WRITE-хук: записать записи в целевую область."""
            if target_lo <= address < target_hi:
                pc = uc.reg_read(UC_ARM_REG_PC)
                recorded.append((pc, address, size, value))
        from unicorn import UC_HOOK_MEM_WRITE as _W
        emu.uc.hook_add(_W, on_w)
        emu.uc.reg_write(UC_ARM_REG_SP, STACK_TOP)
        emu.uc.reg_write(UC_ARM_REG_LR, 1)
        try:
            emu.uc.emu_start(addr | 1, 0, count=cap)
        except UcError:
            pass
        if recorded:
            hits[addr] = recorded
        del emu
    print(f"\n[sweep] функций, пишущих в область дескрипторов: {len(hits)}")
    for addr, recs in sorted(hits.items(), key=lambda kv: -len(kv[1]))[:25]:
        addrs = sorted(set(r[1] for r in recs))
        print(f"  func 0x{addr:05x}: {len(recs)} записей, адреса "
              f"{[hex(a) for a in addrs[:8]]}{' …' if len(addrs) > 8 else ''}")
    return hits


def main():
    """CLI: run a function / sweep the writers (see --help).
    CLI: прогнать функцию / sweep-записей (см. --help)."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--func", default="0x1f600")
    ap.add_argument("--max", type=int, default=200000)
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--seed-desc", action="store_true",
                    help="засеять дескрипторы маркерами 0xA0..0xAF")
    ap.add_argument("--seed-sched", action="store_true",
                    help="поднять предусловия планировщика 0x1f600")
    ap.add_argument("--find-writers", action="store_true",
                    help="прогнать все функции, найти пишущих в дескрипторы")
    a = ap.parse_args()
    if a.find_writers:
        sweep_writers()
        return
    addr = int(a.func, 16)
    emu = McuEmu(trace=a.trace, max_insn=a.max)
    seed = bytes(range(0xA0, 0xB0)) * 20 if a.seed_desc else None
    emu.run_func(addr, fill_desc=seed, seed_sched=a.seed_sched)


if __name__ == "__main__":
    main()
