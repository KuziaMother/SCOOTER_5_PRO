#!/usr/bin/env python3
"""
gen_maps.py — generator of research/MCU_MAP.md and research/BLE_MAP.md.

Decompilation map BY FUNCTION:
  - function list is taken from functions_mcu/README.md (678) and
    functions_ble/README.md (170) — canonical result of detection from
    gen_functions_mcu.py / gen_functions.py;
  - each function is mapped to the catalog of analyzed blocks from REPORT.md
    (ANALYZED_MCU): name, sections, status -> % decompiled;
  - BLE: region map (§43.3) + all functions of PLAIN regions.

% model (per function):
  100% — analyzed: logic fully decoded and described in REPORT.md
   50% — partial: role/input identified, part of logic decoded
   25% — ID: address and role known only from call context (xref)
    0% — not started: only auto-disassembly in functions_*/

Total % = Σ(size_i × pct_i) / Σ(size_i) (weighted by code bytes).

Run:  python research/scripts/gen_maps.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))   # research/scripts/
RES = os.path.dirname(HERE)                          # research/

# ----------------------------------------------------------------------
# catalog of analyzed MCU blocks (REPORT.md §6..§45)
# (start, name, sections, status) — start is matched to the containing function
PCT = {'analyzed': 100, 'partial': 50, 'ID': 25}
ANALYZED_MCU = [
    # --- "own" handshake and ciphers (§27, §36, §37) ---
    (0x21C64, "«own»: input cipher/frame check (initiator BLE)", "§36.3, §37", "analyzed"),
    (0x1A7AC, "«own»: S-box substitution + permutation (16 B, 10 rounds)", "§37", "analyzed"),
    (0x1A5F2, "«own»: trampoline bl 0x1bfa0 (from 0x1a628)", "§27.2, §37", "analyzed"),
    (0x1A5FA, "«own»: XOR of two 16-B blocks (round, call from 0x1a7ac; callers=3)", "§37", "analyzed"),
    (0x1A5E6, "«own»: trampoline to S-box block 0x1a7ac (real start 0x1a5e4 `mov r2,r1` — without prologue, detection artifact; bl from 0x21c64)", "§36.3, §37", "analyzed"),
    (0x1DD8C, "**«own» round — single round of «own» cipher (verified §59.7 — batch 15)**: buffer 16 B = 4 groups * 4 bytes; each group [A,B,C,D] mixed independently via CRC-8 (polynomial 0x1B, MSB-first) as Feistel: X=A^B^C^D; A'=A^crc8(A^B)^X, B'=B^crc8(B^C)^X, C'=C^crc8(C^D)^X, D'=D^crc8(D^A)^X; crc8(x)=((x<<1)^(0x1B&-(x>>7)))&0xFF. Pure function of buffer in r0 (without pool/absolute RAM). bl from 0x1a814", "§37/§59.7", "analyzed"),
    (0x1A628, "trampoline to cipher: ldr r0=&0x16aa; bl 0x1bfa0", "§27.2", "analyzed"),
    (0x1BFA0, "table cipher (&table @0x16aa, src)", "§27.2", "analyzed"),
    # --- USART3/UART4 <-> BLE (§6.5-6.7, §28.3, §32) ---
    (0x1F600, "RX USART3: ring + dispatcher via descriptor table", "§6.7", "analyzed"),
    (0x1E480, "ISR USART3 (link to BLE chip): status, reset PE/FE/ORE", "§6.5", "analyzed"),
    (0x1E9E0, "**RX parser of USART3 protocol (core analyzed and verified §59.6 — batch 14)**: caller — periodic task 0x1DFD8 (bl @0x1E0AE). Contract: state=byte[RAM+0x172] (0->only RAM+0x171=0; 1->process 1 message and reset); head=byte[RAM+0x2C0], ring **3 slots * 150 B @RAM+0x881**, command byte = ring[head*150+1]; toggle=byte[RAM+0x2C9] (0..7, wrap) -> context slot **@RAM+0x10B5 + i*0x96**. Dispatch by ASCII: '@'->only head++; 'G'/'K'/'c'->frame-start (len 20/27/83, context {6,'e',len,'O','K',crc,0x9A}, crc=sum context[1..4], flag-reset RAM+0x310/0x369/0x36F); 'A'->telemetry-snapshot (ring[3..9] -> RAM+0x2E8..0x2F1: rev16(ring4<<8|ring3), nibbles ring5, ring7-split {bit7,bit6,[5:0]}, context {0xC,'d',0x20,7,data*7,crc,0x9B}, crc=(0x64+0x20+7+sum data)&0xFF); 'a' etc. -> response builders. After: head++ (wrap >=3). **Method note: Bcond on chip = D0xx (BEQ, imm8 in [7:0]) — non-standard ARM; capstone trusts target, not cond labels**", "§6.5/§59.6", "analyzed"),
    (0x1F6B4, "TX: descriptor assembly [type=2][len][data]", "§6.5", "analyzed"),
    (0x1F1CC, "MCU->BLE: request builder `63 CMD` (frame template)", "§32", "analyzed"),
    (0x216E4, "TX ring @0x10b5 sender (UART4)", "§28.3", "analyzed"),
    (0x23188, "HAL_UART_Transmit (port/length validation, assert)", "§6.5", "analyzed"),
    (0x1302C, "**USART RCC pulser (full analysis §59)**: base -> (reg, bit): 0x40013800(USART1)->+0x0C/0x4000, 0x40004400(USART2)->+0x10/0x20000, 0x40004800(USART3)->+0x10/0x40000, 0x40015000->+0x0C/0x20000, 0x40015400->+0x0C/0x40000; sequence |=bit then &=~bit (pulse); unknown base -> no writes; r0 = bit; emulator-verified (batch 12)", "§6.5/§59", "analyzed"),
    # --- aggregator/telemetry (§18, §22, §34) ---
    (0x1F71C, "aggregator: 24-state machine (jump-table on CTX[0x10])", "§22.5", "analyzed"),
    (0x1D898, "range/battery estimator (§73.11-12): v=i16[RAM+0x27A]->X=(8000*v)>>16->struct+0x20; R=10000*X/(500-X) (divider 0x19994, div-by-zero->-1)->struct+0x40; ACCUMULATOR (leaky integrator): new_0x3c=(old_0x3c+delta-prev_0x14)&0xFFFFFFFF, delta=i16[RAM+0x26E], new_0x14=asr(new_0x3c,10); struct=RAM+0x3C8 (shared with PID/FOC). Status flags 0x290/0x292/0x2a8/0x2aa — state machine (§73.13): gates +0x286->(0x290,0x292), +0x29e->(0x2a8,0x2aa); default (zeroed) (2,140,1,78); mode/LUT-driven (LUT 0x614-0x6c4/0x738-0x808, live). Verified 400/400 (range) + 250/250 (acc)", "§22/§73.11-13", "analyzed"),
    (0x1A938, "**motor FOC routine (correction §6.5/§22: not just \"battery thresholds\")** — 3296 B, largest function; single caller — 0x1a49e (no fresh arguments, operates on global RAM). **Structure (§59.9):** entry -> push + pool loads -> immediate `bl 0x1be1c` (TIM capture calc) — under zero state executes only ~10 own instructions before delegating. Subfunctions: 0x1be1c (TIM capture), 0x1d7ac (vector operation), 0x1d818 (2D rotate/dot §50), 0x1bd88 (quadrant classifier) — all motor-related. **Battery aspect**: ldrb @0x306 (% from 0x1DFD8) @0x1aaf8, `cmp #0x5a`(90), gate byte@0x22e (==1 -> bypass); thresholds 10/90/100 (§6.5). 3 internal returns (0x1adf0/0x1b224/0x1b616) = state machine branches; parts tightly coupled with inter-part branches (not glued). RAM regions: 0x90, 0x108..0x10e, 0x382/0x384/0x386, 0x17fa4..0x17fac (constant initialization when idle). **Deep pass (§60–§60.3): ALL 5 subfunctions analyzed and verified** — 0x1be1c (TIM capture -> FOC phases, 6-sector), 0x1e410 (table decode Q15 @flash 0xA6C6), 0x1d7ac (cross+dot, X from table), 0x1d818 (cross+dot, X from RAM+0x10c), 0x1bd88 (6-sector classifier). **State machine architecture (§60.3, trace):** zero state -> one iteration, 458 insns, clean return; flow: entry->0x1be1c(TIM)->post->0x1d7ac(cross+dot->0x1e410)->large inline block 0x1aa08..0x1aae6(109 insn)->conditional `bl 0x1ab68` (internal block, gate `cmp r3,#0;bge`)->fixed-point 0x1b3f2..0x1b460 (muls/asrs#15, write r4+0x18..0x34)->0x1d818(2D rotate)->0x1bd88(sector)->return. Single byte flags do not change path — gates are multi-byte/value-based. **All 3 large inline blocks + 3 substantive small fragments verified**: §60.4 0x1b3f2 (cross+dot); §60.5 0x1aa08 (clamp+integrator); §60.6 0x1b48a (sector commutation, threshold 16383); §60.7 small: 0x1b470 (v2c/v30/v34 from r0/r1/r2), 0x1b584 (tail: svX=asr15(4500*vX), offset=asr1(2250-max(sv)), phases u16[RAM+0x382/4/6]=2250-(sv+offset) — final PWM output of FOC), 0x1a9f2 (pre-block-2 frame setup); **§60.8 entry 0x1a938..0x1a9d0 verified** (table lookup — triangular mapping over flash table @0x9E38: idx=value>>4 | 1023-(value-16384)>>4, u16[r4+4]=idx, u16[RAM+0x108]=tableE[idx], r0=+-tableE[1024-idx]; + scaled-delta u16[r4+0x62]=asr16(0x93cc*delta); branch C inactive for s16). **ALL of 0x1A938 analyzed and verified**: all 5 subfunctions + entry + 3 large inline blocks + 3 small fragments; only trivial 1-2 insn gaps remain (stores/branches). **§73:** motor timer TIMER_A @0x40012c00 modeled in emulator (TimModel) + empirically verified (FOC config, test @t(0x1A938)). **§73.14: FOC in closed loop** — current-reference = u16[RAM+0x224] (sensitivity sweep; throttle PID s16[RAM+0x42c]->0x224 1:1, connector in FOC cluster 0x1ad90/0x1baa4/0x1c74c/0x1d310); transfer function amp~=0.0103*|ref| (center~=1125, CCR_A up/CCR_B down 2-phase); integrated sim `_foc_sim.py` (PID+FOC each step, shared RAM). **§73.15: clarification** — P=u32[RAM+0x388]=[u16 RAM+0x224] (1:1, PC 0x1aae4), i.e. 0x224 definitively = current-ref; 0x224 — shared upstream input (PID reads it PC 0x1d12c gated <<2, FOC only reads; written by upstream app/BLE, not PID/FOC); electrical loop NOT statically closed (measured vector 0x108/0x10a and currents 0x838/83c/840 do not affect PWM in isolation — requires full state machine + live gains). Tests @t(0x1A938) FOC-transfer + current-ref->P + @t(0x1D078) FOC-loop", "§22/§59.9/§73/§73.14-15", "analyzed"),
    (0x7494, "**motor parameter setup** (1282 B, largest MCU tail; §66). Entry decoded: reads 3 motor parameters (0x8f04=constant 4200, 0x8ecc=u16[RAM+0xf9d], 0x8ee8=u16[RAM+0xf9b]) and clamps each to [1000,5000] (on stack); getters have side-effect in working-struct RAM+0x1359 (odd offsets +1/+3/+0x10). Body: window-gate family (0x8e50/0x8e70/0xf010/0xf024, §56) + interpolation 0x16fde; constants 0xc80(3200)/0x3e8(1000)/0x7f(127)/0x64(100). Return r0=0x15e802. Inputs: config RAM+0xf95, table RAM+0x17ed4. **Core verified 50/50 (§66.1):** p0=sdiv(|val2-val3|*(min-3200), u16(1000-|diff|)) — denominator u16 (without sign-ext); [struct+0xc]=min+clamp_s16(p0). Tail (§66.2): ~15 bit-gated window-gate calls (config bits -> struct fields) + 2*bl 0x16fde (table interpolation) + percentage r5*X/100 + clamp [5000,10000]. **ALL of 0x7494 analyzed** — largest MCU tail closed", "§66", "analyzed"),
    (0x1c34c, "**fixed-point piecewise-linear calculation** (calibration curve, 1244 B; §68). Self-contained inline math (4 bl: software division §67). Entry: config flag selects base (stored or 0x55<<3=680) -> [struct+0x4c]; 240*s16[table+8], division. Linear segments: output=pool*(x-30)/300+1000 for x in [30,330) (thresholds/coeff = calibration). 64-bit min/max tracking (sbcs, constant 25<<6=1600). Output: table 8*s32 in RAM+0x17ed8..0x17efc. **Algorithm+division+segments analyzed; field coeff ~12 inputs = calibration data**", "§68", "partial"),
    (0x1B67C, "flags/status: overheat >=46°C -> flag @0x318", "§22", "analyzed"),
    (0x1BB1C, "battery measurement #2 (struct @0x154)", "§25.4", "analyzed"),
    # --- ADC (§22, §40) ---
    (0x1A31C, "ADC1: sampling state machine (system tick ~1 kHz)", "§22, §40", "analyzed"),
    (0x2359C, "**validated-write with readback-retry (§59, 44 B, without push — detector artifact)**: args (base=r0, idx=r1, data=r2); addr = base + (idx<<4) + 0x108; loop: str data -> ldr -> cmp -> bne (retry until match); bx lr; caller: 0x1E298 (block @0x40020000)", "§59", "analyzed"),
    (0x1E298, "**DMA+ADC init (full analysis §59)**: bl 0x1A5D4 (ADC1 CR2|=0x20) -> validated-write **0x2359C**(0x40020000, 0, **0x5D000041**) to [0x40020108] with readback-retry -> u32[0x40020028]=1 (enable) -> ADC1 CR2|=4; return pop {r4,pc}; new peripheral block **@0x40020000** (reg +0x108 data, +0x28 enable); emulator-verified (batch 12)", "§40/§59", "analyzed"),
    (0x1D3D0, "ADC ISR tail: -> TX -> SWSTART", "§22.6", "analyzed"),
    (0x1C0B0, "**ADC1 sensor-init (full analysis §58)**: struct @sp {base=0x40012400, [4]=0, [8]=0, [0xA]=3, [0xB]=3} -> bl 0x21FB8 (reset) -> bl **0x21CA8** (configurator) -> 4*bl **0x21E18** (chan_cfg @sp+0x50: ch {0xC,0xB,0xA,0xF} = A/B/C/F, rank {1,2,3,4}, smp=4, sqr=0, low=3) -> final ORs: [ADC1+0x20]|=0x04040403 (ch0-2 smp=4 + field[2:0]=3), [+0x24/28/2C]|=0x04040404 (ch3-14 smp=4; ch7-10 — compensation for raw-shift no-op of 0x21E18), common-block @+0x40: [+0x40]|=0x0E1C6104, [+0x44]|=9, [+0x54]|=0x40; [ADC1+0x1C]|=1, [ADC1+0]|=0x40; bl 0x23544(0xC,1), bl 0x21C74(sp,0x20/4); **[ADC1+0x18]|=1 (ADON) at end**; emulator-verified (batch 11)", "§40/§58", "analyzed"),
    (0x21CA8, "**ADC1 validated channel-configurator (full analysis §58)**: asserts (cpsid i; b .): base==0x40012400, cfg[4] in {0,1}, cfg[0xB]<=4, cfg[0xC]<=5, cfg[0xA]<=3, cfg[6]<=0xF, cfg[9]<=7; sequence: [CR2+0x18]|=2 (SWSTART) -> bl 0x21FB8 (reset) -> state byte[struct+0x39]=2 -> SMPR1(+0x1C): field[7:5]=cfg[4], field[5:3]=cfg[0xA]; branch cfg[8]: 1->|=bit16, 2->|=bit20, else->clear bit16/20; field[19:17]=cfg[9] (branches 1/2); SMPR2(+0x20) field[2:0]=cfg[0xB]; [+0x40] field[3:0]=cfg[6]; SMPR1 bit13=cfg[5]; [+0x7C]=0, field[20:18]=cfg[0xC]; state=1; **[CR2+0x18]|=1 (ADON)**; return 0; emulator-verified (batch 11)", "§40/§58", "analyzed"),
    (0x21FB8, "**ADC1 reset-helper (46 B, without push — detector artifact, not in function map)**: base=[r0]; [base+0x18]=0 (CR2 off), [+0x1C]=0 (SMPR1), [+0x7C]=0, [+0x3C]=**0x0FFF0000** (magic), [+0x58/5C/60/64]=0, [+0x54]=0, [+0x40/44/48/4C]=0; byte[struct+0x39]=0, byte[struct+0x38]=0; return 0; emulator-verified (batch 11)", "§58", "analyzed"),
    # --- motor (§39, §41) ---
    (0x0799C, "ADC1 channel sequencer + rank table (pair to 0x21ca8)", "§39, §41", "analyzed"),
    (0x07A30, "ADC1 DMA channel enable (periph 0x40020000/0x40020108)", "§39, §41", "analyzed"),
    (0x0E408, "ADC ISR handler: read [0x40020050], dispatch", "§39, §41", "analyzed"),
    (0x22A48, "TIM1 / TIM8: PWM init (timer cluster @0x40012C00)", "§39.1, §41", "analyzed"),
    (0x22D2C, "duty cycle update TIM1 (speed/power control)", "§39.1", "analyzed"),
    (0x1E2F8, "TIM1 fault handler / emergency stop (break input)", "§39/§59", "analyzed"),
    (0x1BF48, "TIM1 hall sensor input capture (commutation angle)", "§39/§59", "analyzed"),
    # --- dispatcher/modes (§34.2, §39.5b, §40) ---
    (0x0E658, "**round-robin dispatcher of BLE/motor tasks (full decode §57)**: gates: byte[RAM+0x35] in {0,1,2} (3 redundant checks — switch artifact) && byte[RAM+0xA49]==1; bl **0x6618** (BLE SM #7 §53) — unconditional; counter = byte[RAM+0xA62]: >=10 -> reset to 0; dispatch @0xE684 (**vendor instruction**, bytes df e8 = invalid TBB per ARM standard: bits [4:0]!=0; capstone decodes «tbb [pc,r0]» leniently, Unicorn implements chip semantics: target = 0xE69A + 6*r0 — select 6-byte entry `bl TASK; b tail`); task list (10 slots): {**0x6E50** (BLE SM #2 §52), **0x63B8** (BLE SM #6 §53), **0x799C** (duty controller §39/41), **0x7A30** (motor SM slot-3 §39/41), **0x69E4** (BLE SM + interpolator §53), **0x6838** (BLE SM #3 §52)} + 4 empty; tail: counter++ (wrap >=10->0); mutation test: bytes 0xE688..0xE691 do not affect dispatch (padding, self-contained instruction); code from 0xE692 (counter-reset) and @0xE69A (task list); caller: scheduler-thunk @0x12470 (§54: bl 0x11de8 -> 0x11d98 -> **0xe658** -> gate -> bl 0x11894/0x46ec/0x81b4/0x1dec/0x3de4); **bug**: when cnt=4 task 0x69E4 calls 0x16F42, which on current flash tables performs OOB read (u32[hdr+4]=0x98001053 as index) -> fault @0x16FA2, counter does not increment", "§39.5b/§57", "analyzed"),
    (0x23374, "**3-wire bus — full decision table (§59)**: struct @RAM+0xAC; C==0 -> A=u16[+8] (0/1/2/4), C!=0 -> B=u16[+A] (3/5/6/7); mid=(cur+delta)>>1 (u32[+0x38]+u32[+0x3C]); cur updated only on \"mid\" branches; A==0/B==7 -> r0 from arguments; skipped branches -> old u16[+0x30]; **§59.2: bls/CC = lim<=mid (with equality!), bhi/HS = lim>mid strictly** (deviation from ARM); emulator-verified (batch 12, 48 cases)", "§40.7/§59", "analyzed"),
    # --- MCU->BLE telemetry (§47) ---
    (0x211F8, "frame builder 'a'/'a1' into TX ring @0x10b5 (state byte@0x18A: 0->1->2->0; rate-limits 1920/3200 ticks)", "§47", "analyzed"),
    (0x1DFD8, "**USART3 periodic task — inline logic verified (§59.8 — batch 15)**: u16 tick @RAM+0x2BA++ -> **3 leaky integrators with feedback**: new_acc=(acc+delta-old_out)&0xFFFFFFFF, new_out=asr(new_acc,5) s16 (pairs acc/delta/out: 0x298/0x278/0x27A, 0x288/0x284/0x286, 0x2A0/0x29C/0x29E) -> **battery %**: level=s16[RAM+0x1794+12] (element 6 of array), >=535->100, <415->0, else (level-415)*100//120 (signed div) in byte[RAM+0x306]; gate: compute if flag byte[RAM+0x321]==1 OR u16[RAM+0x312]>=30000 (then flag:=1), else only u16[0x312]++; calls 0x1B67C/0x2186C (start) + **0x1E9E0** (RX parser §59.6)/0x1F1CC/0x1F71C/0x211F8; main u32 counter @RAM+0x314++ (clamp ~0x1D4CA); flag bits 0x20 on byte[RAM+0x339]/0x21E when counter >= 0x3E8. **Verification: 6 bl patched to NOP (save/restore), inline logic matched against Python model; subfunctions verified separately**", "§47/§59.6/§59.8", "analyzed"),
    # --- NVRAM/boot (§21, §25, §26) ---
    (0x1C838, "calibration/sequencer: @0xF400/+4 -> @0x1e8/@0x1ec", "§25", "analyzed"),
    (0x21A08, "NVRAM-save task (gate byte@0x170==1 + bit31 common+0x14)", "§25", "analyzed"),
    # --- small functions <=12 B: getters/setters/peripherals (§48) ---
    (0x6378, "FLASH unlock: magic keys 0x45670123/0xCDEF89AB -> FLASH_KEYR @0x40022004", "§48", "analyzed"),
    (0x61D4, "FLASH_SR @0x4002200C |= r0 — flag reset (caller OTA code 0x06230)", "§48", "analyzed"),
    (0xC894, "(RCC_CFGR0 @0x40021004) & 0xC — AHB prescaler bits", "§48", "analyzed"),
    (0x5970, "write r0 to register @0x40010414 (AFIO zone; EXTI mapping?)", "§48", "analyzed"),
    (0xB854, "write 0x10000 to struct+0x108 (caller: struct@RAM[0xdd8])", "§48", "analyzed"),
    (0x1F1C0, "setter USART3+4 (call from TX ring 0x1F600)", "§48", "analyzed"),
    (0x211EC, "setter UART4+4 (call from TX ring 0x216E4)", "§48", "analyzed"),
    (0x99F0, "write 0xAAAA to @0x40003000 (driver cluster)", "§48", "analyzed"),
    (0x99E0, "write 0xCCCC to @0x40003000", "§48", "analyzed"),
    (0x5CC0, "write 0xAAAA to @0x40003000 (duplicate of 0x99f0)", "§48", "analyzed"),
    (0x9A0C, "write r0 to @0x40003000", "§48", "analyzed"),
    (0x9A00, "write r0 to @0x40003000+4", "§48", "analyzed"),
    (0x99D4, "write r0 to @0x40003000+8", "§48", "analyzed"),
    (0x833C, "getter byte@RAM[0xC8D] — init flag of 0x8xxx driver", "§48", "analyzed"),
    (0x8348, "one-time init (flag byte@0xC8D==0): GPIOA + SPI1 command 0xB9 + delay (continuation — 0x8352)", "§48", "analyzed"),
    (0x8468, "guard: return if byte@0xC8D!=0 (variant #2, pattern like 0x8348)", "§48", "analyzed"),
    (0x82F0, "guard: return if byte@0xC8D!=0 (r4-variant; callers 0xd878/0x119e4/0x147ac)", "§48", "analyzed"),
    (0x87E2, "conditional setter: r2 ? *(r0+0x18) : *(r0+0x28) = r1", "§48", "analyzed"),
    (0x123C0, "write 0x10000 to struct@RAM[0xdd8]+0x108 (via 0xb854)", "§48", "analyzed"),
    (0x1A5C4, "ADC1+0x18 |= 8 (bit3; caller — ADC task 0x1A31C)", "§48", "analyzed"),
    (0x1A5D4, "ADC1+0x18 |= 0x20 (bit5; caller — DMA+ADC 0x1E298)", "§48", "analyzed"),
    (0x87DE, "setter +0x18 (in init: GPIOA+0x18 = 0x10)", "§48", "analyzed"),
    (0x1072A, "getter u16 @+0xc (ldrh)", "§48", "analyzed"),
    (0x10730, "setter u16 @+0xc (strh)", "§48", "analyzed"),
    (0x99CE, "setter u16 @+0x10 (strh)", "§48", "analyzed"),
    (0x99B4, "getter byte from u16@+0x10 (uxtb ldrh)", "§48", "analyzed"),
    (0x4F50, "getter u16 @+4 (uxth)", "§48", "analyzed"),
    (0x4E38, "setter +4 (str r0,[r1,#4])", "§48", "analyzed"),
    (0x4FBA, "setter +4 (str r1,[r0,#4])", "§48", "analyzed"),
    (0x4FAC, "conditional setter *[r2+0x10] = (r3 ? r0 : 0)", "§48", "analyzed"),
    (0x7FD4, "getter byte (ldrb r0,[r0])", "§48", "analyzed"),
    (0x8878, "getter byte@RAM[0x128]", "§48", "analyzed"),
    (0x8AF0, "getter byte@RAM[0xA73]", "§48", "analyzed"),
    (0x8D90, "getter u32@RAM[0x1344]", "§48", "analyzed"),
    (0x8E14, "getter byte@RAM[0x1378] (@0x1359+0x1f)", "§48", "analyzed"),
    (0xA6A4, "getter byte@RAM[0x40]", "§48", "analyzed"),
    (0xE3E4, "setter u16 = 0 (strh #0,[r0])", "§48", "analyzed"),
    (0x21C0C, "getter u32@RAM[0x2C] (pool=0x20000028 + 4; fixed address, NOT double indirection; §50.7)", "§48/§50.7", "analyzed"),
    (0x8A44, "getter u32@RAM[0xF6A] (pool=0x20000F64 + 6; fixed address; §50.7)", "§48/§50.7", "analyzed"),
    (0xC6F0, "write to 0x42420060 — non-existent address (dead code?)", "§48", "ID"),
    # --- small functions: thunk/wrappers (§48, upgraded to "analyzed" in §61 - behavior = "call X", no ambiguity) ---
    (0x1DEC, "thunk -> 0x29e8", "§48/§61", "analyzed"),
    (0x2D14, "thunk -> 0x9678", "§48/§61", "analyzed"),
    (0x4E28, "thunk -> 0x5000", "§48/§61", "analyzed"),
    (0x4E30, "thunk -> 0x4fc0", "§48/§61", "analyzed"),
    (0x9A18, "thunk -> 0x99f0 (write 0xAAAA to @0x40003000)", "§48/§61", "analyzed"),
    (0xCE68, "thunk -> 0x3168", "§48/§61", "analyzed"),
    (0x10780, "thunk -> 0x10788", "§48/§61", "analyzed"),
    (0x10A20, "thunk -> 0x112bc", "§48/§61", "analyzed"),
    (0x11CAC, "thunk -> 0x4c14", "§48/§61", "analyzed"),
    (0x12FD0, "thunk -> 0x12b50", "§48/§61", "analyzed"),
    (0x12FD8, "thunk -> 0x12d90", "§48/§61", "analyzed"),
    (0x395C, "thunk -> 0xd298(r0=0)", "§48/§61", "analyzed"),
    (0x3966, "thunk -> 0xd298(r0=1) (pair with 0x395c: off/on)", "§48/§61", "analyzed"),
    (0x3B20, "thunk -> 0x1bdc(r0=0x9a)", "§48/§61", "analyzed"),
    (0x5B8C, "thunk -> 0x4de0", "§48/§61", "analyzed"),
    (0x110F0, "thunk -> 0x5b8c(r0=0)", "§48/§61", "analyzed"),
    (0x1ABC, "sequence: 0x1a68 + 0x19f4", "§48/§61", "analyzed"),
    (0x1CEA, "sequence: 0x1fe0 + 0x20d8", "§48/§61", "analyzed"),
    (0x36F4, "sequence: 0x10900 + 0x3b00", "§48/§61", "analyzed"),
    (0x9482, "sequence: 0x9134 + 0x9480", "§48/§61", "analyzed"),
    (0x9F64, "sequence: 0x9b44 + 0x9f70", "§48/§61", "analyzed"),
    (0xBF4C, "sequence: 0xd878 + 0xddc4", "§48/§61", "analyzed"),
    (0xC200, "thunk -> 0x9f64 (r3=1)", "§48/§61", "analyzed"),
    (0x11668, "thunk -> 0x10e5c", "§48/§61", "analyzed"),
    (0x11888, "thunk -> 0x10f18", "§48/§61", "analyzed"),
    # --- §61: inspection of remaining uncataloged functions ---
    (0x11BAC, "**date/time formatter (verified §61)**: total-seconds -> 6 bytes via remainder chain. Arguments: arg0=r0=out-buffer, arg1=r1=total seconds. Divisors [31104000, 2592000, 86400, 3600, 60] (~360d-year, 30d-month, day, hour, minute): out[0]=v//31104000, out[i]=(v%D[i-1])//D[i], out[5]=v%60. Caller 0x6184 unpacks counter [r0+0x1f] into [r1+0x19..]", "§61", "analyzed"),
    (0x13284, "**context-slot state-machine (twin of 0x131fc)**: arguments (r0,r1,r2); r2>0x96 (slot stride §59.6) -> return 0; reads state byte &7 (==7->bypass), mod-4 counter loop with bitmask check, index calculation r4*3+r4*16. Caller 0x4276", "§61", "analyzed"),
    (0x131FC, "**context-slot state-machine — twin of 0x13284** (identical structure: r2>0x96->return 0, state&7, mod-4 counter, bitmask). Callers 0x4a88, 0x4ad8", "§61", "analyzed"),
    (0x1A894, "**struct/counter initializer**: bl 0x1e3e4; zeros struct+4/+8/+0xc; sets bytes (+0=0, +1=1); bit15 [r0+0x14] |= 1<<15; decrement loop of u16[r1+4] until underflow (counter zeroing). Caller 0x1a338", "§61", "analyzed"),
    (0xF14C, "**init/retry routine**: bl 0x11d6; loop (<=3 iterations) bl 0xab0c with check r0==1 (retry until success); then reads [pool+0x2f]. Caller 0xe6f8", "§61", "analyzed"),
    (0x6FC0, "**multi-stage operation** — sequence of sub-calls: 0x10ff8, 0x8e90 (cbnz), 0x8ecc, 0xe3ec (*2), 0x8ee8, 0xe36c, 0x11098, 0x8f58. Caller 0x11940", "§61", "analyzed"),
    (0x2D70, "**stack-struct initializer**: [sp+8]=0, [sp+0xa]=0xbfff, then filling fields (0x30...). Caller 0x174ec", "§61", "analyzed"),
    # --- §49: shelves 13-64 B. RCC/core/SysTick/NVIC ---
    (0xC4B4, "RCC_CFGR0[7:4] (HPRE) = r0", "§49", "analyzed"),
    (0xC580, "RCC_CFGR0[10:8] (PPRE1) = r0", "§49", "analyzed"),
    (0xC60C, "RCC_CFGR0[1:0] (SW — clock source) = r0", "§49", "analyzed"),
    (0xC598, "RCC_CFGR0[14:11] (PPRE2) = r0<<3", "§49", "analyzed"),
    (0xC518, "HSION on/off (RCC_CTLR bit0)", "§49", "analyzed"),
    (0xC6C4, "set/clear of bits in RCC+0xC (INTENR?)", "§49", "analyzed"),
    (0xC684, "set/clear of bits in RCC+0x10 (incl. clocking of I2C1/I2C2: bits 21/22 from 0x97f4)", "§49", "analyzed"),
    (0xC624, "set/clear of bits in RCC+0x14 (AWDCR?)", "§49", "analyzed"),
    (0xC6A4, "set/clear of bits in RCC+0x18 (BDCR?)", "§49", "analyzed"),
    (0xC644, "set/clear of bits in RCC+0x28 (AHBPER?) — NON-canonical function (detector skipped; gap 0xC63E..0xC684 = 2 skipped funcs + pools)", "§50.7.3", "analyzed"),
    (0xC664, "set/clear of bits in RCC+0x1C (BDCR/CSR?) — NON-canonical function; call 0xc664(0x10000000) from 0x30e0/0x310c", "§50.7.3", "analyzed"),
    (0x225C4, "set/clear of bits in RCC_CTLR (+0x0)", "§49", "analyzed"),
    (0x225DC, "set/clear of bits in RCC+0x60 (extended register)", "§49", "analyzed"),
    (0xC858, "check RCC flag: group 1=CTLR, 2=CFGR2(+0x20), else +0x24; bit r1&0x1f", "§49", "analyzed"),
    (0xC8A4, "wait CTLR bit17 (arg 0x31: group=1,bit=17), timeout 0x2000 -> 0/1 (§50.7)", "§49/§50.7", "analyzed"),
    (0xC8DC, "wait CTLR bit1 = HSERDY (arg 0x21: group=1,bit=1; NOT +0x24!), timeout 0x500 -> 0/1 (§50.7)", "§49/§50.7", "analyzed"),
    (0xC914, "wait RCC+0x24 bit3 (arg 0x63: group=3->+0x24; NOT CTLR!), timeout 0x500 -> 0/1 (§50.7)", "§49/§50.7", "analyzed"),
    (0xC5B0, "combined setter RCC CFGR0/CFGR2 (PLL config?)", "§49", "analyzed"),
    (0xC540, "setter of bits RCC+0x24 (modes r0 0/1/4)", "§49", "analyzed"),
    (0x10ABC, "enable HSE (CTLR bit0) + wait HSERDY (bit1), timeout 0x500; fallback constant 0x3D0900 -> @0xB88", "§49", "analyzed"),
    (0x22234, "TIM initial: toggle RCC_CTLR bit0x10 with delays 0x22a0c", "§49", "analyzed"),
    (0x1E3A4, "**software reset**: config RCC+0x40, dsb, SCB_AIRCR = 0x5FA0004 (SYSRESETREQ+VECTKEY), loop", "§49", "analyzed"),
    (0x1E2CA, "SysTick init: RVR=r0-1, CVR=0, CTRL=7", "§49", "analyzed"),
    (0x35EC, "SysTick: disable TICKINT (CTRL &= ~2)", "§49", "analyzed"),
    (0x21B84, "NVIC/SCB: field [7:6] of byte (r0>>2): r0>=0 -> 0xE000E400+(r0&~3); r0<0 -> 0xE000ED00+off(r0&0xF)+0x1C; reg=(v&~(0xFF<<(8*(r0&3))))|((r1&3)<<(6+8*(r0&3)))", "§49/§50.7.3", "analyzed"),
    (0x22A0C, "busy-delay: threshold = 0x1000000 - *(u32@RAM[0x10])*N; wait rotl8(CVR)<threshold; CVR |= 0xFFFFFF", "§49/§50.7.3", "analyzed"),
    (0x229D4, "busy-delay: threshold = 0x1000000 - *(u32@RAM[0x24])*N; wait rotl8(CVR)<threshold; CVR := 0xFFFFFF", "§49/§50.7.3", "analyzed"),
    # --- §49: I2C1/I2C2 + EEPROM/CRC ---
    (0x1C60, "I2C2 chain #1: -> 0x1e52 -> 0x214c -> 0x8f7c(I2C2=0x40005800)", "§49", "analyzed"),
    (0x1E52, "I2C2 chain #2: reassemble arguments -> 0x214c", "§49", "analyzed"),
    (0x214C, "I2C2 write: 0x8f7c(op=8, reg=r0, buf=stack)", "§49", "analyzed"),
    (0x1E72, "I2C2 chain #3: -> 0x2730 -> 0x9048 -> 0x8f7c(I2C2)", "§49", "analyzed"),
    (0x2730, "I2C2 read path: -> 0x9048", "§49", "analyzed"),
    (0x1C7A, "I2C2 read: buffer {u16=0, len=2, addr=0x3E} -> 0x1e72; result -> u16@0xF95+0x1E", "§49", "analyzed"),
    (0x155AC, "I2C read: buffer {u16=0, len=4, addr=0x3E} -> 0x1e72; result -> u16@0xF95+0x20", "§49", "analyzed"),
    (0x15758, "I2C write: 0x11d6(0x80c, &@0x1FD4); 0x11c8(0x800, &@0x27E0); 0x11c8(0x800, &@0x1FD4); @0x1FD4+0x804 = 0x800", "§49", "analyzed"),
    (0x97F4, "I2C clock OFF: base==I2C1(0x40005400) -> RCC+0x10 &= ~(1<<21); else &= ~(1<<22) (set-then-clear = forced bit clear)", "§49/§50.7.3", "analyzed"),
    (0x90A0, "I2C1 transaction: check *(u32@RAM[0xB60])!=0; address from *(u32@RAM[0xB64]); 0x1c08/0x1bd8/0x1c08(1)", "§49", "analyzed"),
    (0xAAD0, "**CRC-16/CCITT-FALSE** (polynomial **0x1021**, init 0, MSB-first, without xorout) over byte array; emulator-confirmed (§50.7; in §49 erroneously was 0xA001)", "§49/§50.7", "analyzed"),
    (0x3B42, "CRC-16 (polynomial 0xA001) + mvn (bitwise NOT)", "§49", "analyzed"),
    (0x3BC4, "CRC-16 (polynomial 0x1021, MSB-first) — second variant", "§49", "analyzed"),
    (0x8A50, "CRC-16 table-based (tables @0x19584/@0x19684 of 256 u16 each); call from 0x3da0/0xc420 — **EEPROM read verification**", "§49", "analyzed"),
    (0x87F8, "CRC-8 (polynomial 0x2F) over byte array", "§49", "analyzed"),
    (0x3DA0, "read 4B from EEPROM + CRC-16 (0x8a50) with check; buffer @0xC9C", "§49", "analyzed"),
    (0xC420, "read 4B from EEPROM + CRC-16 (0x8a50); buffer @0xC9C (variant of 0x3da0)", "§49", "analyzed"),
    (0x128C8, "EEPROM write: 0x50b0(&@0x44, 2); 0x1093c()", "§49", "analyzed"),
    # --- §49: FLASH (OTA) ---
    (0x62D4, "FLASH_SCBR |= 0x80 (after erase/write)", "§49", "analyzed"),
    (0x6284, "check FLASH BSY (SCBR bit0); 1=busy", "§49", "analyzed"),
    (0x6360, "FLASH_CTLR bits [5:3] = r0 (erase/write mode)", "§49", "analyzed"),
    (0x6390, "wait non-BSY; timeout -> 0xA", "§49", "analyzed"),
    (0x7E98, "**sector erase**: address validation (%0x800==0, range 0x3000..0x1FFFF), unlock, 0x6230(erase), SCBR|=0x80", "§49", "analyzed"),
    (0x7E70, "**bulk erase**: loop over 0x800-byte sectors (buffer on stack 0x804)", "§49", "analyzed"),
    (0x7EE8, "bulk erase: initialize stack buffer + start loop", "§49", "analyzed"),
    (0x7FDC, "bulk erase: loop body (pointer -> 0x6230)", "§49", "analyzed"),
    (0xDDC4, "**OTA command from host**: u16@0x124E+0x12==0xE0 && +0x14==0x5AA5 -> erase @0x1D800 + 0xdd80; ==0xE2 -> 0xdd80 (magic 0x5AA5)", "§49", "analyzed"),
    # --- §49: DMA/SPI/UART ---
    (0x17F4, "DMA clock OFF: base==0x40020800 -> RCC+0x28 &= ~0x1000 (bit12 = base>>18); otherwise net", "§49/§50.7.3", "analyzed"),
    (0x106D8, "SPI1 (0x40013000) / SPI-2 (0x40013C00): on/off via RCC+0xC bits (base>>12)", "§49", "analyzed"),
    (0x10734, "SPI config: merge u16 flags from structure -> SPI register; call 0x10788", "§49", "analyzed"),
    (0x10770, "SPI1 initial: SPI_CTLR |= 0x40, RCC |= 0x1000, SPI+0x4=0x80, 0x5a6c()", "§49", "analyzed"),
    (0x106B8, "SPI1 initial: SPI_CTLR |= 0x10, RCC |= 0x400, SPI+0x4=0x80, 0x5a6c()", "§49", "analyzed"),
    (0x2A6C, "UART initial: config from flash structure + 0x13c5c(0x4B) (CMD 0x4B)", "§49", "analyzed"),
    # --- §49: GPIO/AFIO/EXTI ---
    (0x2BBC, "GPIO port: A(0x40010800)=0, B(0x40010C00)=1, C(0x40011000)=2, D(0x40011400)=3; dispatch by mode(r1), common return 0x2BEE", "§49/§50.7.3", "analyzed"),
    (0x8588, "AFIO remap: idx=arg1>>2 (arith.), p=arg1&3: MAPR[idx]=(MAPR & ~(3<<4p)) | ((arg0<<4p) & M32) — field [4p+1:4p], arg0 not masked", "§49/§50.7.3", "analyzed"),
    (0x32F4, "EXTI setup: RCC-enable + remap(7) + 0x40010414=0x80 + 0x59a4()", "§49", "analyzed"),
    (0x30A6, "EXTI setup: RCC-enable + remap(0xB) + 0x40010414=0x80 + 0x59a4()", "§49", "analyzed"),
    (0xC94C, "AFIO/EXTI block: 0x14958(5); 0xce4c; 0x58b0(1); 0x40010414=0x100000; 0xc9fc(1<<14); 0xc9dc(0x4000); 0xcb40(1)", "§49", "analyzed"),
    # --- §49: strings/math ---
    (0x1A838, "**CRC-32** (polynomial 0x04C11DB7, MSB-first); call from aggregator 0x1F71C", "§49", "analyzed"),
    (0x19A68, "memcpy (byte loop)", "§49", "analyzed"),
    (0x7FB8, "memmove (directional byte loop)", "§49", "analyzed"),
    (0x1E34, "sum of byte array (u8)", "§49", "analyzed"),
    (0x48D8, "sum of u16 + mvn (bitwise NOT) — checksum", "§49", "analyzed"),
    (0xC9A8, "BCD -> binary (by bytes)", "§49", "analyzed"),
    (0xC9BE, "binary -> BCD (by bytes)", "§49", "analyzed"),
    (0x126C, "**u64 LSR**: (r1:r0) >> r2 — logical shift right (amount in r2); call from 0x123e", "§49/§50.6", "analyzed"),
    (0x1A080, "**u64 LSL**: (r1:r0) << r2 — logical shift left (amount in r2)", "§49/§50.6", "analyzed"),
    (0x1A0A0, "**u64 LSR**: (r1:r0) >> r2 — copy of 0x126c (different code location)", "§49/§50.6", "analyzed"),
    (0x1A0C2, "**u64 ASR**: (r1:r0) >>s r2 — arithmetic shift with sign extension", "§49/§50.6", "analyzed"),
    (0x128C, "u64 add (r0:r1 + r2:r3)", "§49", "analyzed"),
    (0x1A16A, "u64 sub (r0:r1 - r2:r3)", "§49", "analyzed"),
    (0x5A68, "u32 udiv (hardware + overflow correction)", "§49", "analyzed"),
    (0x161EA, "u32 udiv (variant with cyclic correction)", "§49", "analyzed"),
    (0x5044, "average of u16 array (sum/length)", "§49", "analyzed"),
    (0x16176, "binary search on i16 array (return index/0xFFFF)", "§49", "analyzed"),
    (0x1619E, "binary search on u32 array", "§49", "analyzed"),
    (0x1A010, "**scaling with deadband**: |v|<0x7f -> 0; [0x7f..0x96] -> linear; else (v-0x96)<<1; sign preserved; call from 0x1D898 (§22)", "§49", "analyzed"),
    (0x19F7C, "comparison of u64 (r0:r1) with signed r2 (udiv-like preparation)", "§49", "analyzed"),
    (0xE160, "lookup in flash string table @0x19E98+0x140 via 0x16880/0x16aa2", "§49", "analyzed"),
    (0xE3EC, "lookup in flash string table @0x19FAC+0x8A via 0x16880/0x16aa2", "§49", "analyzed"),
    # --- §49: events/flags/critical sections ---
    (0x2D1C, "**critical section entry**: u32@RAM[0xB5C]++", "§49", "analyzed"),
    (0x2D34, "**critical section exit**: u32@RAM[0xB5C]--", "§49", "analyzed"),
    (0x4BC0, "event queue @0x164C: push {ptr, 0} (slot++ % 6)", "§49", "analyzed"),
    (0x4BE8, "event queue @0x164C: push {u16, 0} (slot++ % 6)", "§49", "analyzed"),
    (0x4C98, "event queue @0x164C: push {*(u32@RAM[0xB4C]), 0} (slot++ % 6)", "§49", "analyzed"),
    (0xD6E4, "one-shot flag u32@0x8C bit0xA: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD700, "one-shot flag u32@0x8C bit0xB: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD71C, "one-shot flag u32@0x8C bit0xC: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD738, "one-shot flag u32@0x8C bit0xD: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD754, "one-shot flag u32@0x8C bit0xE: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD770, "one-shot flag u32@0x8C bit0xF: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD78C, "one-shot flag u32@0x8C bit0x10: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD7A8, "one-shot flag u32@0x8C bit0x11: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD7C4, "one-shot flag u32@0x8C bit0x12: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0xD7E0, "one-shot flag u32@0x8C bit0x13: if not set — set and bl 0xd75c", "§49", "analyzed"),
    (0x12C24, "saturating counter: u16@0xB7A++, cap 0xC8; gate bit0(u32@0xB76)", "§49", "analyzed"),
    (0x12E64, "saturating counter: u16@0xB7C++, cap 0xC8; gate bit2(u32@0xB76)", "§49", "analyzed"),
    (0x8834, "**check \"all conditions\"**: @0x107==1 && @0x35==1 && @0x40!=1 && @0x3C!=1 && @0x3E!=1", "§49", "analyzed"),
    (0x1238C, "state machine byte@0x35: 0->1+initial; 2/3/4/5->reset to 0 with calls", "§49", "analyzed"),
    (0x11D98, "state machine byte@0x2E: 0->1+initial; 2/3/4/5->reset to 0 with calls; copy to @0xF70+5/6", "§49", "analyzed"),
    # --- §49: battery/motor/sensors ---
    (0x44C0, "**range-check**: u16@0xF95+6 <= 0x7D0 && u16@0xF95+8 >= 0x1194 && i8@0xFC8+1 > -40 && i8@0xFC8+2 < 0x64; gate byte@0xA73", "§49", "analyzed"),
    (0x8B58, "**ADC->mV**: u16@0x5E * 0xCE4 / 2^20 + i8@0xA6 -> i8@0xFC7+8", "§49", "analyzed"),
    (0x8B10, "**ADC->mV**: u16@0x5E * 0xCE4 / 2^20 + i8@0xA6 -> u8@0x44+1", "§49", "analyzed"),
    (0xE704, "**clamp |v|<=0xC8**: else zero byte@0x12BA+0x56; call 0x1654c; call from 0x07A30 (§41 slot-3)", "§49", "analyzed"),
    (0x14924, "I2C read with 3 retries: 0xcee0(8, 0x91B2, 2) -> u16@0xF95+0x1E", "§49", "analyzed"),
    (0x1D874, "lookup via 0x19994(0xBB80): result -> u16@0xF95+2/4", "§49", "analyzed"),
    (0x8F58, "i8@0xFC8 -> u16@0x135E (sign-extend)", "§49", "analyzed"),
    (0x57F8, "u16@0xCB3 -> bytes @0xCB3/0xCB5 + send 0x13bb8(s)", "§49", "analyzed"),
    (0x5818, "bytes @0xCB3/0xCB5 -> u16@0xCB3 + send 0x13bb8(s)", "§49", "analyzed"),
    (0x13BB8, "**retry-send**: 0x13b60-check + delay 0x1F4; gate u16@0x30CF", "§49", "analyzed"),
    (0xB53A, "I2C-like transaction with retry (poll 0x9794)", "§49", "analyzed"),
    (0x2E84, "I2C-like request: 0x9874 (structure check) + counter @0xB71", "§49", "analyzed"),
    (0x98AE, "u32 from two u16 (+0x14/+0x18), high byte = 0", "§49", "analyzed"),
    (0x11350, "zeroing counter cluster @0xA55..; gate bit7(u16@0xF95+0xC)", "§49", "analyzed"),
    # --- §49: init chains (called from mega-initial 0x1DF4) ---
    (0x1DF4, "**mega-initial**: 15 sequential bl (0x3b2a, 0x36f4, 0xced0, 0x9b44, 0x9f70, 0xc098, 0x11978, 0x119c4, 0x3034, 0x1cf6, ...)", "§49", "analyzed"),
    (0x3B2A, "init-subblock: 0x3b50/0x3b74/0x3b8a/0x3b9c/0x3bb2 (RCC/peripherals chain)", "§49", "analyzed"),
    (0x36F4, "init-subblock: 0x3700() + 0xc984()", "§49", "analyzed"),
    (0xCED0, "init-subblock: 0xcdd4(1) + 0xcdc8(1)", "§49", "analyzed"),
    (0x9B44, "init-subblock: 0x9b54() + 0x9b6c()", "§49", "analyzed"),
    (0x9F70, "init-subblock: 0x9f80(0x10) + 0x9fa4(1)", "§49", "analyzed"),
    (0xC098, "init-subblock: 0x5b5a() + 0xc0a0()", "§49", "analyzed"),
    (0x11978, "init-subblock: 0x11988(0x80) + 0x119a0()", "§49", "analyzed"),
    (0x119C4, "init-subblock: 0x119d4() + 0x119ec()", "§49", "analyzed"),
    (0x3034, "init-subblock: 0x3044(1) + 0x305c()", "§49", "analyzed"),
    (0x1CF6, "init-subblock: 0x1d06(1) + 0x1d1e(1)", "§49", "analyzed"),
    (0x15A1C, "struct @0x1FAC initial (~0x20B, defaults 0/0xFFFF) + 0x15758 (I2C)", "§49", "analyzed"),
    (0x15FFC, "set pointer @0xC80; when byte@0xB8C==1: reset/decrement counter + 0x15a1c", "§49", "analyzed"),
    (0x15CE0, "retry-counter @0xC84: increment up to 3; when byte@0x36==1 reset", "§49", "analyzed"),
    (0x1395C, "flag handler: byte@0xCAC -> byte@0xA73 (reset after handling)", "§49", "analyzed"),
    (0x5B5A, "delay 0x2F + 0x1c1c(0x90) (init-subblock)", "§49", "analyzed"),
    (0x11C5E, "I2C init: 0x5a38() + delay 0x9239 + 0x1c1c(0x1F4)", "§49", "analyzed"),
    (0x11C3C, "I2C init: 0x5a38() + delay 0x29BC + 0x1c1c(0x1F4)", "§49", "analyzed"),
    (0x5FB4, "I2C init: 0x5a38() + delay 0x2710 + 0x1c1c(0x1F4)", "§49", "analyzed"),
    (0x5A38, "I2C pre-initial: 0x15588() + 0x5134() + 0x109c4()", "§49", "analyzed"),
    # --- §49: miscellaneous (handlers/tables) ---
    (0x1858, "handler registrar: write to table @0x1A8D0 (index r0)", "§49", "analyzed"),
    (0x3970, "access to struct @0x98: +0x20 = r0 ? r2 : r1; +0x24 = r3", "§49", "analyzed"),
    (0xC984, "lookup in table @0x5CC (0x3A entries) via 0x3994", "§49", "analyzed"),
    (0x3700, "lookup in table @0x92C (0x11 entries) via 0x583c", "§49", "analyzed"),
    (0xB978, "check \"queue empty\": *(u32@RAM[0x106]) == *(u32@RAM[0x10A])", "§49", "analyzed"),
    (0xBB14, "check \"queue empty\" (variant)", "§49", "analyzed"),
    (0xBC5C, "descriptor assembly {ptr, 0, 0} -> 0xc0b4()", "§49", "analyzed"),
    (0xBC86, "descriptor assembly {ptr, 0, 0} -> 0x85c8()", "§49", "analyzed"),
    (0x3740, "event: u16@0x1048 -> 0xcd80(2) + 0xcda4()", "§49", "analyzed"),
    (0x10A5C, "event: u16@0x1048 -> 0xcd80(1) + 0xcda4()", "§49", "analyzed"),
    (0x4A30, "lookup in local table (2 entries) via 0x12f44/0x12d04", "§49", "analyzed"),
    (0x4B04, "lookup in local table (2 entries, variant)", "§49", "analyzed"),
    (0x96DC, "call callback from struct @0xDD8+0x114 (default 0x11a4)", "§49", "analyzed"),
    (0x9714, "call callback from struct @0xDD8+0x110 (default 0x11a4)", "§49", "analyzed"),
    (0xE6EC, "if byte@RAM[0x13C9]==1 -> bl 0xf14c (not a function-pointer; emulator-confirmed §50.7)", "§49/§50.7", "analyzed"),
    (0x2E0C, "check \"both zero\": u16@0x38 == 0 && u16@0x3A == 0", "§49", "analyzed"),
    (0x3940, "0x3c04(0x8000000, 0x3000, 0) -> u32@0xCC (flash read?)", "§49", "analyzed"),
    (0x3A6C, "one-shot flag byte@0x142: if 0 -> 1 + bl 0x3a7e", "§49", "analyzed"),
    (0x4F70, "merge u32 flags: struct+8/12 -> | in r0 (for SPI/UART config)", "§49", "analyzed"),
    (0x593C, "AFIO/EXTI setup: if 0x597c(0x200) ([0x40010400]&0x200 and [0x40010414]&0x200) -> byte@RAM[0x100]=1; then sequentially 0x80/0x100/0x200 -> 0x40010414 (emulator-confirmed §50.7)", "§49/§50.7", "analyzed"),
    # --- §49: I2C2 shadow-register family (RAM @0x15FA..0x164C -> chip registers on I2C2) ---
    (0x20C4, "I2C2 wr reg 0x38 = u32@0x162D", "§49", "analyzed"),
    (0x2138, "I2C2 wr reg 0x36 = u32@0x162B", "§49", "analyzed"),
    (0x21DC, "I2C2 wr reg 0x12 = u32@0x1607", "§49", "analyzed"),
    (0x21F0, "I2C2 wr reg 0x14 = u32@0x1609", "§49", "analyzed"),
    (0x2204, "I2C2 wr reg 0x16 = u32@0x160B", "§49", "analyzed"),
    (0x2218, "I2C2 wr reg 0x18 = u32@0x160D", "§49", "analyzed"),
    (0x222C, "I2C2 wr reg 0x1A = u32@0x160F", "§49", "analyzed"),
    (0x2240, "I2C2 wr reg 0x1C = u32@0x1611", "§49", "analyzed"),
    (0x2254, "I2C2 wr reg 0x1E = u32@0x1613", "§49", "analyzed"),
    (0x2268, "I2C2 wr reg 0x20 = u32@0x1615", "§49", "analyzed"),
    (0x227C, "I2C2 wr reg 0x22 = u32@0x1617", "§49", "analyzed"),
    (0x2290, "I2C2 wr reg 0x24 = u32@0x1619", "§49", "analyzed"),
    (0x22A4, "I2C2 wr reg 0x26 = u32@0x161B", "§49", "analyzed"),
    (0x22B8, "I2C2 wr reg 0x28 = u32@0x161D", "§49", "analyzed"),
    (0x22CC, "I2C2 wr reg 0x2A = u32@0x161F", "§49", "analyzed"),
    (0x22E0, "I2C2 wr reg 0x32 = u32@0x1621", "§49", "analyzed"),
    (0x22F4, "I2C2 wr reg 0x3A = u32@0x162F", "§49", "analyzed"),
    (0x2308, "I2C2 wr reg 0x7F = u32@0x164B (len 1)", "§49", "analyzed"),
    (0x231C, "I2C2 wr reg 3 = u32@0x15FA (len 1)", "§49", "analyzed"),
    (0x2330, "I2C2 wr reg 5 = u32@0x15FC (len 1)", "§49", "analyzed"),
    (0x2344, "I2C2 wr reg 7 = u32@0x15FE (len 1)", "§49", "analyzed"),
    (0x2358, "I2C2 wr reg 0x70 = u32@0x163F (len 2)", "§49", "analyzed"),
    (0x1BDC, "**I2C2 read**: {code16, len=2} -> 0x1e72(op=8, dev=0x3E) — read register of I2C2 chip", "§49", "analyzed"),
    (0x1C1C, "**I2C2 read**: {code16, len=2} -> 0x90a0(base=0x40005800) — read register of I2C2 chip", "§49", "analyzed"),
    (0x236C, "I2C retry counter: success 0x21dc -> @0xA76=0, @0xA75++; >=4 -> reset + @0xA73=1", "§49", "analyzed"),
    (0xAB0C, "I2C read 0x38B + double poll 0xa910(0)/0xa910(1)", "§49", "analyzed"),
    (0xABF0, "I2C read 0x20B + double poll 0xa8c4(0)/0xa8c4(1)", "§49", "analyzed"),
    # --- §49: WWDG / DMA / core-misc ---
    (0xCC08, "WWDG @0x40002800: SR(+0xC) &= ~0x80 (EWIF?)", "§49", "analyzed"),
    (0xCB10, "WWDG+0x24: sequence 0xCA -> 0x53 (magic?)", "§49", "analyzed"),
    (0x1940, "**RCC extended registers initial**: AWDCR|=1, BDCR|=0xE|0x1000, 0x1580(2,0)", "§49", "analyzed"),
    (0x1580, "RCC extended initial: r5==0 -> 0xc490(0x100)+0xc478(r4); else 0xc4b0/0xc4c8", "§49", "analyzed"),
    (0x16D4, "**DMA1 reset**: 0x1940(); DMA on; loop i<2: 0x4e50(0x40020030); byte@0xB82=0", "§49", "analyzed"),
    (0x175C, "**DMA1 enable**: 0x1940(); loop i<2: 0x1858(i) (handler reg), 0x1670(), 0x18fc(i) (channel config); byte@0xB82=1", "§49", "analyzed"),
    (0x18FC, "**DMA1 channel**: struct {1,1,0xE0000,0,2} -> 0x18b0(DMA1); table @0x1A8D0 (step 8) + 0x15aa", "§49", "analyzed"),
    (0x4FC0, "**DMA1 INTFR handler**: if bit 0x02000000 -> clear + byte@0x1743 &= ~(1<<@0x1744) + @0xB76 &= ~1", "§49", "analyzed"),
    (0x5000, "**DMA1 INTFR handler**: if bit 0x20000 -> clear + byte@0x1B6E &= ~(1<<@0x1B6F) + @0xB76 &= ~4", "§49", "analyzed"),
    (0x4F58, "check mask in u32: (*(u32@r1) & r0) != 0", "§49", "analyzed"),
    (0x4F38, "set: *(u32@r0) |= 1; clear: *(u32@r0) &= 0xFFFE (**truncates to u16!** asymmetry; mode=r1; §50.7)", "§49/§50.7", "analyzed"),
    (0x21C18, "NVIC priorities: *(u32@RAM[0x4]) vs flash 0x2710; 0x19968/0x1e2c8; r4!=3 -> 0x21b84(~0, r4)", "§49", "analyzed"),
    (0xD298, "poll 0xcfb8 with delay 0x1F4; then *(u32@*(u32@RAM[0x304C])) != 0", "§49", "analyzed"),
    (0x37F4, "struct @0x304C initial {0, 0x21000, 0x21000} + 0x84a0(..., 0x2000) with retry", "§49", "analyzed"),
    (0xB618, "transaction initial: 0xb8c8/0xb968; if empty -> *(u16@[r4]) &= ~1, +4 |= 0x700, +0x10C=0", "§49", "analyzed"),
    (0x8380, "transaction 0x833c: if r0 -> return 0 (conditional exit)", "§49", "analyzed"),
    (0x84A0, "transaction 0x833c: if r0==0 -> return (from 0x37f4/0x851c)", "§49", "analyzed"),
    (0x851C, "transaction 0x833c: if r0!=0 -> return pc (from 0x37f4)", "§49", "analyzed"),
    # --- §49: driver @0x40003000 (magic 0xAAAA/0x5555) + GPIOA ---
    (0x5DBC, "@0x40003000 = 0xAAAA; 0x2d5c (flash wr @0x1A550); 0xc20c(4)", "§49", "analyzed"),
    (0x5C9C, "@0x40003000 = 0xAAAA; 0x332c(flash 0x19B14, 2); 0xc20c(1)", "§49", "analyzed"),
    (0x5B98, "@0x40003000 = 0xAAAA; GPIOB+0x18 = 0x40003000>>7; GPIOA+0x18 = 4; 0xc20c(3)", "§49", "analyzed"),
    (0x9A20, "@0x40003000 cmd: 0x5555 -> 0x9a0c; 0x9a00(6); uxth(r4) -> 0x99d4; 0x99f0; 0x99e0", "§49", "analyzed"),
    (0x84FC, "GPIOA: 0x87da(GPIOA, 0x10); 0x10870(6); 0x87de(GPIOA, 0x10)", "§49", "analyzed"),
    (0x8434, "GPIOA: 0x87da(GPIOA, 0x10); 0x10870(5); poll 0x10870(0xFF) until bit0==0; 0x87de(GPIOA, 0x10)", "§49", "analyzed"),
    (0x82B8, "one-shot under flag @0xC8D: 0x8468(); 0x83e4(); result in {0xC84014, 0xC84013, 0xA14014} -> OK, else flag=1", "§49", "analyzed"),
    # --- §49: u16-bit family (device registers) ---
    (0x97CA, "set/clear bit0x400 in *(u16@r0)", "§49", "analyzed"),
    (0x982C, "set/clear bit0 in *(u16@r0)", "§49", "analyzed"),
    (0x9844, "set/clear bit0x100 in *(u16@r0)", "§49", "analyzed"),
    (0x985C, "set/clear bit0x200 in *(u16@r0)", "§49", "analyzed"),
    (0x106A0, "set/clear bit0x40 in *(u16@r0)", "§49", "analyzed"),
    (0x97E2, "set/clear mask r1 in *(u16@r0+4)", "§49", "analyzed"),
    (0x99BC, "*(u16@r0+0x10) = (r1|1) if r2 else (r1&~1) — **r1 = input value**, not memory read; §50.7", "§49/§50.7", "analyzed"),
    (0x9794, "check: u32 from u16(+0x14/+0x18) contains all bits of r1 (unsigned)", "§49", "analyzed"),
    (0x9874, "check flag in struct: r1<<28 ? +0x14 : +0x18; (val & r1) != 0", "§49", "analyzed"),
    (0x87C8, "check: *(u32@r0+0x10) & r1 != 0", "§49", "analyzed"),
    (0x10718, "check: *(u16@r0+8) & r1 != 0", "§49", "analyzed"),
    (0x5874, "bit1: if 0x597c(1) -> 0x5970(1)", "§49", "analyzed"),
    (0x58F6, "bit0x10: if 0x597c(0x10) -> 0x5970(0x10)", "§49", "analyzed"),
    (0x5888, "bit0x800: if 0x597c(0x800) && !byte@0x102 -> @0x102=1; then 0x5970(0x800)", "§49", "analyzed"),
    # --- §49: flag reset (pairs to one-shot set) ---
    (0xD7FC, "clear bit0xC u32@0x8C if 0xd46c(0xC)==1", "§49", "analyzed"),
    (0xD824, "clear bit0xA u32@0x8C if 0xd46c(0xA)==1", "§49", "analyzed"),
    (0xD850, "clear bit0x12 u32@0x8C if 0xd39c(0x12)==1", "§49", "analyzed"),
    # --- §49: signed math / u64 ---
    (0x16288, "signed preparation for division (sign -> 0x80000000)", "§49", "analyzed"),
    (0x162CE, "signed preparation for division (variant)", "§49", "analyzed"),
    (0x16328, "signed preparation for division (variant)", "§49", "analyzed"),
    (0x1712C, "**fixed multiplication**: P = r0*r1 (via 0x172b8); return low 32 bits (P >> n), n = r2; emulator-confirmed (§50.7); no direct callers", "§49/§50.6/§50.7", "analyzed"),
    (0x17150, "**product check**: P = r0*r1 (via 0x172b8); return (P_hi==0) ? P_lo : -1 (\"does it fit into 32 bits\"); emulator-confirmed (§50.7); no direct callers", "§49/§50.6/§50.7", "analyzed"),
    (0x1494, "**comparison g(a) vs g(b)**: a={r1:r0}, b={r3:r2}; g(x)=x when bit63(x)=1, else 2^63-x; flags = cmp of high words (+cmpeq of low words on equality). For IEEE-double bit patterns this is comparison in reverse numerical order (bhs <=> a<=b); callers: float code 0x16040 (§50.7)", "§49/§50.7", "analyzed"),
    # --- §49: calibration/scaling ---
    (0x19FF4, "lookup 0x1a184(0, 0, 0x433) — calibration table", "§49", "analyzed"),
    (0x19FCC, "abs(r0) -> lookup 0x1a184(0, sign, 0x433)", "§49", "analyzed"),
    (0x1218, "abs(r0) -> 0x12aa(0, 0, 0x433)", "§49", "analyzed"),
    (0x1A052, "**u64 scale 2^(n-0x433)**, n = r2>>21 (twin 0x123e): n < r3 -> 0; [r3..0x433] -> u64lsr({r1:r0}, 0x433-n) via 0x1a0a0; > 0x433 -> {r1, r0 << (n-0x433)}; pool: 0x3FF+0x34=0x433, -0x433", "§49/§50.6", "analyzed"),
    (0x123E, "**u64 scale 2^(r2-0x433)**: r1' = (r1&0xFFFFF)|0x100000; r2 < 0x3FF -> {r1', 0} (sentinel); [0x3FF..0x433] -> u64lsr({r1':r0}, 0x433-r2) via 0x126c; > 0x433 -> {r1', r0 << (r2-0x433)}; no direct callers", "§49/§50.6", "analyzed"),
    (0x19FAE, "(r0+r1) -> 0x1a0f8(_, 0, 0x96) — scaling with deadband", "§49", "analyzed"),
    (0x19FBE, "0x1a0f8(0, 1, 0x96) — scaling with deadband (inversion)", "§49", "analyzed"),
    (0x12804, "lookup in flash table @0x19B3C (u16, step 2): code 0x82/0xE/0x65", "§49", "analyzed"),
    # --- §49: CRC family (addition) ---
    (0x3C4C, "**CRC-16 table-based** (table @0x19784, 256 u16) — third variant of CRC-16", "§49", "analyzed"),
    (0x3C7C, "**CRC-7 byte-step**: r0 ^= byte; 8x: msb? ((r0<<1)&0xFF)^7 : (r0<<1)&0xFF — XOR constant **0x07** (not 0x09!); state in r1, byte in r0; emulator-confirmed (§50.7)", "§49/§50.7", "analyzed"),
    # --- §49: miscellaneous ---
    (0x8AFC, "0x218c() -> u32@0xF95+0xD (store result)", "§49", "analyzed"),
    (0xC138, "magic: u16@0xA7C == 0xEB04 -> 1", "§49", "analyzed"),
    (0x3150, "event {u32=0, u16=0x7F, u32=0x136} -> 0xcd0c", "§49", "analyzed"),
    (0x4A04, "zero block @0x129..0x13C (byte + 3*u32)", "§49", "analyzed"),
    (0x6304, "alignment: r0&3 ? 9 : 6", "§49", "analyzed"),
    (0x7ED4, "FLASH not-busy: 0x61e4()==1 -> 0, else 1", "§49", "analyzed"),
    (0x87B0, "struct initial {u16=0xFFFF, +2=0, +3=0, +8=0, +0xC=0xF}", "§49", "analyzed"),
    (0xC464, "write struct {u32=r1, +4=0, +5=0, +6=r2, +7=r3} -> 1", "§49", "analyzed"),
    (0x4994, "0x49ac(); byte@0xD9=0; byte@0xD8=1 (flag pair)", "§49", "analyzed"),
    (0x12A64, "0x4c84(0, 1); 0x124c0() — queue/event", "§49", "analyzed"),
    (0x139AC, "CMD: {u32=3} -> 0x13c78 (send)", "§49", "analyzed"),
    (0x13C5C, "**CMD 0x4B**: 0x11d6(&@0x3084, 0x4B); byte@0xCAC=1 (request flag)", "§49", "analyzed"),
    (0x158F8, "I2C start: byte@0xB8C=1; 0x15ffc(0xA); byte@0x1FAC+3=1", "§49", "analyzed"),
    (0x2A5C, "flag 0x1bdc(0x9A) & 1", "§49", "analyzed"),
    (0x4DE0, "poll: 0x1bdc(0x93)&0x1bdc(0x94) + delay 0x1F4", "§49", "analyzed"),
    (0x4E08, "poll: 0x1bdc(0x94) + delay 0x1F4", "§49", "analyzed"),
    (0x2D5C, "**flash write**: 0x3588(); 0x332c(flash 0x1A550, 0x1A) — write 26B to NVRAM zone", "§49", "analyzed"),
    (0x11998, "**init chain of 10 calls** (0xfbf8..0xff3c)", "§49", "analyzed"),
    (0x30E0, "RCC: 0xc664(0x10000000) + 0xc124(0x400) — PLL/clock", "§49", "analyzed"),
    (0xE2CC, "range-check of offset on flash string @0x19F50+0x59F via 0x16d8e -> byte", "§49", "analyzed"),
    (0x129B4, "state dispatch: 0x4c84(1, 10); 0x12470(); TBB on byte@0xB58 (<0xA) — table corrupted/obfuscated; then @0xB58=0", "§49", "analyzed"),
    (0x3994, "lookup in table @0x5CC (0x3A entries * 8B): match on +4 -> pointer", "§49", "analyzed"),
    (0x583C, "lookup in table @0x92C (0x11 entries * 8B): match on +4 -> pointer", "§49", "analyzed"),
    (0xDED4, "**varargs**: if byte[1]==3 -> u32 from 4 bytes -> *(u32@RAM[0xFE7])+2 = value; return 1", "§49", "analyzed"),
    (0x307C, "**varargs**: {b,b,b,1} -> 0xc0b4 (event)", "§49", "analyzed"),
    (0x9B08, "toggle bit3 byte@0xA71 (up to 3 retries, gate 0x2a5c)", "§49", "analyzed"),
    (0x19A8C, "memset (bytes r2, count r1)", "§49", "analyzed"),
    (0x19A9E, "memset (reordered arguments -> 0x19a8c)", "§49", "analyzed"),
    # --- §50: shelf 65-128 B. DMA/FLASH/NVIC/WWDG ---
    (0x18B0, "**DMA1 channel**: builds channel registers from cfg structure (+4/+8/+0x2C, masks 0xFFF0FEFF/0xFFF1F7FD)", "§50", "analyzed"),
    (0x6230, "**FLASH sector erase core**: SCBR clear(0x7C); CTLR(+0x10) |= 2; ADDR(+0x14)=addr; CTLR |= 0x40; wait; CTLR &= 0x3FFD", "§50", "analyzed"),
    (0x61E4, "**HSI start**: if !CTLR bit1 -> HSION(bit0), poll bit1 up to 0x500; return ready", "§50", "analyzed"),
    (0xC4CC, "**clock source switch**: CTLR &= ~0x50000; r0: 0x10000 -> |= 0x10000; 0x40000 -> |= 0x50000", "§50", "analyzed"),
    (0xCBB8, "WWDG: if !SR(+0xC) bit6 -> SR=0x80, poll bit6 up to 0x2000; return status", "§50", "analyzed"),
    (0xCC1C, "**WWDG CFR(+4) decode**: {bits[12:10], [12:8], [5:0], [15:13]} -> 4 bytes; opt. BCD decode (0xc9a8)", "§50", "analyzed"),
    (0xCCBC, "**WWDG CR(+0) decode**: {bits[15:10], [14:8], [6:0]} -> 3 bytes", "§50", "analyzed"),
    (0xCD0C, "**WWDG refresh with data**: 0xCA/0x53 -> +0x24; RER(+0x8) = u32@r4; +0x10 = u32@r4+8 | (u16@r4+4)<<16; 0xcc08; delay 0x2FF", "§50", "analyzed"),
    (0xCB40, "WWDG: 0xCA/0x53 -> +0x24; +0x8 |=/~0x400 (r1); poll +0x10&4 up to 0x2000; return status", "§50", "analyzed"),
    (0xC0B4, "**NVIC IRQ enable**: priority group from SCB_CFSR(0xE000ED0C) bits 0x700; write to [0xE000E400+irq] and [adj+0x100] — **NVIC base of this chip = 0xE000E400**", "§50", "analyzed"),
    (0x3600, "**SysTick period**: udiv(val, 0x3E8); SysTick LOAD(0xE000E014) = n-1; CTRL(0xE000E010) = 7; NVIC priority by irq", "§50", "analyzed"),
    (0x1C1AC, "**ADC-DMA transfer setup (re-analyzed §59, emulator-verified — batch 13)**: block @0x40020000: +0x04=1; validated-writes [+0x100]=**0x40012450** (src=ADC1 DR), [+0x104]=**0x20001692** (dst=RAM+0x1692), bl 0x2359C -> [+0x108]=0x5D000041 (ctrl, same as in 0x1E298); enable: +0x28=1, +0x14=1, +0x70=0x19 (25), +0x50|=1; [+0x108]|=1 (bit0 already set); IRQ tail: [**0xE000E100**]=0x200 (DIRECT write bit9 — not |=!), [NVIC+0x08 (0xE000E408)] &= ~0xFF00 (clear bits 8..15; §50 did not see this); r0=0; 11 writes", "§50/§59", "analyzed"),
    (0x178C, "DMA1 wait: enable (0x182a/0x1814); poll 0x189e(0x20) up to 0x1388; 0x1974; poll 0x1884 up to 0x3E8; 0x1840(1)", "§50", "analyzed"),
    (0x2360C, "FLASH program: check ADDR bit31; copy u32 pairs (tst) into page; start write", "§50", "analyzed"),
    (0x221A4, "critical section + atomic u32 increment with validation (0x23688/0x235d4)", "§50", "analyzed"),
    (0x221E6, "critical section + insert into list (0x2360c); only if r4>>30==0", "§50", "analyzed"),
    (0x23544, "critical section condition + bit operation (r4>>27)", "§50", "analyzed"),
    # --- §50: I2C2 chip + EEPROM/flash scans ---
    (0x2770, "**I2C2 wr**: {code16, val16, len=4} -> 0x90a0(0x40005800, dev 0x3E) — write chip register", "§50", "analyzed"),
    (0xCEE0, "I2C read: {code16, len=2} -> 0x1e72(dev 0x3E) — read chip register I2C2", "§50", "analyzed"),
    (0x9048, "**I2C2 transaction core**: 0x11d6(&buf, 0x28); 0x15640 (CRC-7 encoding); callback *(u32@RAM[0xDD8]+0x11C)", "§50", "analyzed"),
    (0x15640, "**CRC-7 stream coder**: buf[2i]=byte, buf[2i+1]=CRC-7(byte, prev) — for I2C2 transactions", "§50", "analyzed"),
    (0xA788, "I2C read reg 0x91A4 -> u16@0xF95+0x1C; outside [0x7D00..0x8CA0] -> write 0x84D0; 3 retries", "§50", "analyzed"),
    (0xC304, "I2C read reg 0x91A0 -> u16@0xF95+0x18; same range logic; 3 retries", "§50", "analyzed"),
    (0x12AEC, "I2C read reg 0x91A2 -> u16@0xF95+0x1A; same range logic; 3 retries", "§50", "analyzed"),
    (0x1D78, "I2C read reg 5 (2B) -> u16@0xA7C (BE); 3 retries", "§50", "analyzed"),
    (0xA8C4, "**flash scan 0x1C800/0x1D000**: count markers 0xAA (0x40 entries * 32B)", "§50", "analyzed"),
    (0xA910, "**flash scan 0x1F000/0x1F800**: count markers 0xAA (0x24 entries * 32B)", "§50", "analyzed"),
    (0x57A0, "**flash bank select + CRC-32**: header @0x1D800 (CRC-16 check); addr = u32@hdr+0xC+0x3000 or 0x1C800; CRC-32(0x8000000, addr) -> u32@0xD0", "§50", "analyzed"),
    (0xD670, "**EEPROM block read**: 0x11d6(&buf, 0x30); 0x8938; retry 0xab0c *3; CRC-16(0x8a50) -> buf+0x22; memcpy 0x20B; 0xaccc; save 3*u32", "§50", "analyzed"),
    (0x1330C, "**transaction + CRC-8 check**: 0x8380(&buf, 0x50000/0x51000, 8); 0x87f8(buf, 7) == byte@buf+0xB -> 0x10a5c (event)", "§50", "analyzed"),
    (0xCFB8, "**transaction + CRC-16 check**: 0x8380(&@0x304C, 0x2000, 0x10) *2 (with delay); 0x8a50 == u32@+0xC", "§50", "analyzed"),
    (0xEDDC, "**verification @0x304C**: range-checks (0x1F4/0x21000/flash 0x25E20); failure -> reset {0, 0x21000, 0x21000} + 0x1570c", "§50", "analyzed"),
    (0x14368, "**initial @0x30CF**: {+2/+6=0x41000, +0=0} + 0x84a0 retry", "§50", "analyzed"),
    (0x147AC, "**verification @0x30CF**: 0x82f0(0x40000); CRC-16 -> u32@+0xA; 0x84a0 retry", "§50", "analyzed"),
    (0x9A44, "**event-handler registration**: flash tables @0x14A65/0x149B5/0x148E5/0x14A79 (IDs 0-4) -> queue", "§50", "analyzed"),
    # --- §50: CRC/math/interpolation ---
    (0x3C04, "**CRC-32 (poly 0xEDB88320, LSB-first)** — zlib variant; call from 0x57a0/0x3940", "§50", "analyzed"),
    (0x3B82, "CRC-16 (poly 0x1021, MSB-first) — fifth variant of CRC-16", "§50", "analyzed"),
    (0x16222, "signed div (udiv + correction + sign restore)", "§50", "analyzed"),
    (0x172B8, "**u32*u32 -> u64 multiplication** (grade-school, 16-bit halves + carries): **[r2]=HIGH, [r3]=LOW** (pointers reversed relative to usual order!); call from 0x1712c/0x17150; emulator-confirmed (§50.7)", "§50/§50.6/§50.7", "analyzed"),
    (0x506A, "bubble sort of u16 array (call from median filter 0x170c)", "§50", "analyzed"),
    (0x50B0, "byte stream statistics: min/max/sum -> {i8 avg, i8 max, i8 min, u8 cnt_hi, u8 cnt_lo}", "§50", "analyzed"),
    (0x170C, "**median filter**: 7 u16 from @0xB7E -> sort (0x506a) -> average of middle 3 (0x5044) -> u16@0xB84; call from ADC chain 0x3780/0x8b10", "§50", "analyzed"),
    (0x3780, "**voltage calculation**: i8@0xFC7+2 - i8@0xFC7+1 <= 3 -> median filter * 0xCE4/2^20 -> table 0x12804 -> -u8@0x44 -> i8@0xA6; else 0; EEPROM 0x3da0", "§50", "analyzed"),
    (0x1A638, "**float-lookup #1**: table @0x734 (0x35 entries); interpolation 0x1de5e; clamp <= -0.000931; default 125.0; call from 0x1D898 (§22)", "§50", "analyzed"),
    (0x1DE0C, "**float-lookup #2**: table @0x610 (0x2D entries); clamp <= -0.000763; default 250.0", "§50", "analyzed"),
    (0x1DF84, "**float-lookup #3**: table @0x50C (0x29 entries); clamp <= -0.000763; default 100.0", "§50", "analyzed"),
    (0x1DE5E, "**interpolation core**: 0x19968 + abs-lookup 0x19fbe *3 + 0x19fa8/0x19b62/0x19ab0/0x19b5a/0x19bdc (fixed-point lerp pipeline)", "§50", "analyzed"),
    (0x17306, "**i16 table interpolation**: bsearch 0x16176 + lerp * 0x10000 >> 16; call from 0xe2fc", "§50", "analyzed"),
    (0x1736A, "**u32 table interpolation**: bsearch 0x1619e + lerp / 0x10; call from 0xe2fc", "§50", "analyzed"),
    (0x16AA2, "**u16 table interpolation**: bsearch + lerp * 0x10000 >> 16 -> i16", "§50", "analyzed"),
    (0xE2FC, "**multi-interpolation**: 0x17306(t@0x19FE6, 0x1A) + 0x1736a(|v|, t@0x19EB4, 3) + 0x17306(v2, t@0x19FE6+0x36, 4) -> 0x16588 -> u16; call from motor region 0x69E4", "§50", "analyzed"),
    (0xE36C, "**fixed-point lerp with saturation**: |a-b| >= 0x2710 -> 0; else (b*0x2710 - (0x2710-a)*...)/0x2710, clamp [-0x8000, 0x7FFF]", "§50", "analyzed"),
    (0xE17C, "**fixed-point calculation**: 0xe160 (lookup) + 0x16222 (div); (v*0x98B...)/0x2710 * ..., clamp [-0x2710, 0x2710] -> u16", "§50", "analyzed"),
    (0x1D7AC, "**cross+dot of two Q15 vectors (verified §60.1 — batch 16)**: motor FOC subfunction 0x1A938. Arguments: arg0=A=(a_lo,a_hi) Q15, arg1 -> X=0x1e410(arg1)=(X_lo,X_hi) Q15. Four products (each /2^15 with rounding: p<0->+0x7FFF, asr15): P=a_lo*X_hi, Q=a_hi*X_lo, R=a_lo*X_lo, S=a_hi*X_hi. Return u32: **lo16 = Q-P = a_hi*X_lo - a_lo*X_hi (2D cross, z component)**, **hi16 = R+S = a_lo*X_lo + a_hi*X_hi (2D dot)**. Used in FOC for current vector projection/decomposition onto d/q axes", "§50/§60.1", "analyzed"),
    (0x1E410, "**table decode of Q15 vector (verified §60.1)**: FOC subfunction. Argument r0=u32 A. Branch b=A[15:14] (4 quadrants); i1=(A>>6)&0xFF, i2=(0xFF-i1)&0xFF (complementary indices). t1=s16[TBL[i1]], t2=s16[TBL[i2]] where TBL=256*u16 @flash 0xA6C6. Sign inversions per branch: b0:(-t2,-t1) b1:(t1,-t2) b2:(t2,t1) b3:(-t1,t2). Return u32=(hi<<16)|lo. Table base = pool literal 0x0000A6C6 (FLASH0 base + offset)", "§50/§60.1", "analyzed"),
    (0x19B64, "signed fixed-point multiplication/normalization (i16)", "§50", "analyzed"),
    (0x19BDC, "signed algorithm (Euclidean-like loop) + 0x1a0e8", "§50", "analyzed"),
    # --- §50: threshold events (family) ---
    (0xF1EC, "threshold #1: u16@0xF95+6 vs range; event on match", "§50", "analyzed"),
    (0x10524, "threshold #2: u16@0xF95+8 vs range; event on match", "§50", "analyzed"),
    (0xF36C, "threshold #3: i8@0xFC8+1 vs range; event on match", "§50", "analyzed"),
    (0xF5C4, "threshold #4: i8@0xFC8+2 vs range; event on match", "§50", "analyzed"),
    (0xF40C, "threshold #5: u16@0xF95+0xA vs range; event on match", "§50", "analyzed"),
    (0x1A68, "threshold #6: u16@0xF95+0xC vs range; event on match", "§50", "analyzed"),
    (0x19F4, "threshold #7: u16@0xF95+0xE vs range; event on match", "§50", "analyzed"),
    (0x1984, "threshold #8: u16@0xF95+0x10 vs range; event on match", "§50", "analyzed"),
    (0x1093C, "threshold #9: u16@0xF95+0x12 vs range; event on match", "§50", "analyzed"),
    (0x42B8, "threshold #10: u16@0xF95+0x14 vs range; event on match", "§50", "analyzed"),
    (0x3168, "threshold #11: u16@0xF95+0x16 vs range; event on match", "§50", "analyzed"),
    # --- §50: state machines / event queues ---
    (0x29E8, "**handler-table dispatch**: table @0xADC (u32 ptr), index u32@0xB48; empty -> 0x23c4+0x1e94; else blx; set/clear bit(byte@0xB48) in u32@*(u32@RAM[0xAC8]); idx++", "§50", "analyzed"),
    (0x4C14, "**event queue wrap**: counter @0xB4C++; ring @0x164C (6 slots): wrap logic; slots state==1 && u32@+4 <= counter -> state=2", "§50", "analyzed"),
    (0x4CBC, "**event queue consumer**: counter @0xB50++; critical section (0x2d1c/0x2d34); slots state==2: delta vs u32@*(u32@RAM[0xB4C]), min -> @0xB54; **blx [u32@slot+8](arg=u32@slot+0xC)**", "§50", "analyzed"),
    (0x12A78, "state machine byte@0xB5B: 0x4c84(4, 0x1F4); states 0..3 -> pairs (0x12680/0x126d8, 0x1269c/0x12710, 0x12680/0x12738, 0x1269c/0x1273a); counter cap 4", "§50", "analyzed"),
    (0x128E4, "state machine byte@0xB5A: 0x4c84(3, 0x64); 0x1238c(); states 0..3 -> 0x1274c/0x12778/0x1277a/0x1277c; counter cap 5; TBB on @0xB59 (<0xA, table corrupted)", "§50", "analyzed"),
    (0x14ED0, "state machine byte@0x31: states 0/1/2 (conditions @0x107/@0x80/0x8e14()); counter @0x42 (cap 0x32)", "§50", "analyzed"),
    (0x6978, "**state machine @0x12BA**: critical section 0x10fc8; byte@+0x68: 0->+0x69=2 + 0x16504()->u16@+0x50 + 0x164f8()->u16@+0x48; 1/2 -> 0xe740(&local)", "§50", "analyzed"),
    (0xB8DC, "state machine byte@r4+0x10C: 1->2 (+0x9844 bit0x100); 4: poll 0x9874(0x20000) with delay; return 3 (timeout)/0", "§50", "analyzed"),
    (0xB582, "varargs: clear bit0x400 + set bit0x200 (0x97ca/0x985c); then reset transaction (0xb8c8/0xb968 -> if empty: +4 |= 0x700, +0x10C=0)", "§50", "analyzed"),
    (0xB4CE, "varargs batch: 0x99bc(r4, r5); mask 0x70082/0x30002; poll 0x9794; toggle bits every 0x10000", "§50", "analyzed"),
    (0xB476, "varargs batch: loop over r5 bytes -> 0x99ce; mask 0x70084; toggle bits every 0x10000", "§50", "analyzed"),
    (0xBE6C, "**TLV decoder**: type byte@+1: 3 -> {len=byte@+6, data} (0x11a4); 6/0x10 -> 6B fixed; return length", "§50", "analyzed"),
    (0x15F00, "**I2C state machine byte@0x1FAC+3**: states -> 7/2/3/1 (checks @0x1F10+1, u16@+0xC/+8, i16 /16)", "§50", "analyzed"),
    # --- §50: timer cluster 0x40012C00..0x40014C00 + GPIO/UART init ---
    (0x22FAC, "**timer channel config**: struct +0x30/+0x2C (CCR-like): clear [15:12]/[19:16]/[11:8] + set from byte@r1; bases {0x40012C00, 0x40014000, 0x40014400, 0x40014800, 0x40014C00}; +4 [17:16]=byte@r1+0xB; +0x50=u32@r1+4 — **cluster of 5 timer blocks**", "§50", "analyzed"),
    (0x1BD88, "**6-sector FOC classifier (verified §60.2 — batch 16)**: motor FOC subfunction 0x1A938. Arguments: arg0=r0=output struct (u16[r0+2]=sector), arg1=r1=pointer to two s16: x0=s16[r1+0], x2=s16[r1+2]. Gate: bit15 of low16 u32[0x40012C54] (TIMER_A+0x14, same as in 0x1be1c): ==0 -> bypass (sector not written). Constants A=0x3ce4, B=0x2328. S=rnd((B*x2+A*x0)/2), D=rnd((B*x2-A*x0)/2), rnd(V)=(V-1 if V<0 else V)>>1; r2=B*x2. Sector: S<0,D<0->5; S<0,D>=0->(r2>0?3:4); S>=0,D<0->(r2>0?1:6); S>=0,D>=0->2. Final (after writing sector): u32[0x40012C30]&=0xDFFF, and u16@RAM+0x384/0x382 -> TIMER_A+4/+8/+c. 6-sector rotor position classification (each sector = 60°)", "§50/§60.2", "analyzed"),
    (0x21804, "**UART4 init** (MCU->BLE): GPIO @0x48000800 (pins 0x400/0x800); UART4(0x40004C00): struct {base, 0x4B00, 0} -> 0x23188; 0x21bc8(0x1E, 2); 0x21b6c(0x1E); +0x2C |= 0x400", "§50", "analyzed"),
    (0x1BEDC, "GPIO init @0x48000400: zero buffer; 0x22000(pins 0x40/0x80/0xFF); byte@r4+0x14=7", "§50", "analyzed"),
    (0x107EC, "**GPIOA EXTI init**: 0x87b0(&local); RCC BDCR |= 4|0x1001; 4* {mode u16 (0x20/0x80/0x40/0x10), byte, count} -> 0x85c8(GPIOA)", "§50", "analyzed"),
    (0x10870, "**SPI1 read**: poll SPI1+8 bit2 (0x10718) up to 0x8000; 0x10730(r5); delay 0xA; poll bit0; 0x1072a() -> byte", "§50", "analyzed"),
    (0x49B8, "**mode switch**: r4==2 -> 0x16d4 (DMA reset), 0x8348, 0x10770 (SPI1 init), 0x2a6c (UART init), 0x4e08 (poll), delay 0x186A00, 0x1bdc(0x99)", "§50", "analyzed"),
    (0x58B0, "**NVIC IRQ3**: 0x5970(0x100000); struct {0x100000, 0, 8, 1} -> 0x59a4; {3, 0, 0, r4} -> 0xc0b4 (enable)", "§50", "analyzed"),
    # --- §50: init chains / miscellaneous ---
    (0x51D8, "**telemetry init**: 0x11d6(&@0xF70, 0x25); 0x11d6(&@0xF95, 0x26); zero @0xFBB/@0xFC7; 0x11d6(&@0x1004, 0x54); 0x11d6(&@0xFE7, 0x1D); u16@0xF10[0..0xD]=0xE10; byte@0x44[0..2]=0x19; 0x9aa4(); u32@0xFD3+4=0x2710", "§50", "analyzed"),
    (0x2B2C, "**boot config from flash @0x1A8xx**: 0xc624(1); 0x332c(flash 0x1A827, 2); [0x1A8CC] -> sp; 0x307c (varargs event); ldm 0x1A878/0x1A8B0 -> 0x3278/0x3220; {u32@0x1AD8, 0x96}; 0x130e0/0x12fe0/0x4f38/0x130c8 (flags)", "§50", "analyzed"),
    (0x31DC, "event {2, 8, 0x14, 0x18} -> 0xcd80(0); {0xD, 1, 1, 0x40} -> 0xca3c(0) — GPIO pin configuration", "§50", "analyzed"),
    (0x12FE0, "**generic u32 flag set/clear**: group r1>>5&7 (1->+0xC, 2->+0x10, else +0x14); bit r1&0x1F", "§50", "analyzed"),
    (0x130F2, "**generic u32 flag check**: same group; both bits (low + high r1>>8) must be set", "§50", "analyzed"),
    (0x15C94, "**copy string from flash @0x1AA9A**: n = byte@0x1FAC+3; stride ~306B; length via 0x11ec; return count", "§50", "analyzed"),
    (0x53FC, "descriptor-lookup @0x7D5 (table 0x92C): match byte@r4+2; if OK -> byte@r4+4 = entry+8; event 0x5dd8", "§50", "analyzed"),
    (0x13B14, "transaction + CRC-8 check @0x30DD (0x8380(&buf, 0x20); 0x87f8(buf, 0x18) == byte@buf+0x18)", "§50", "analyzed"),
    (0x1570C, "transaction + CRC-16 check @0x304C (0x82f0(0x20000); 0x8a50 -> u32@+0xC; 0x84a0 retry)", "§50", "analyzed"),
    (0x15790, "**EEPROM verification @0xC9C**: 0x82f0(0x30000); CRC-16(4B) -> u32@+4; 0x84a0 retry; call from 0x3da0", "§50", "analyzed"),
    (0x83E4, "**SPI1 read 3B**: GPIOA pin 0x10 (0x87da); 0x10870(0x9F) + 0x10870(0xFF)*3 -> u24; 0x87de; call from one-time init 0x82b8", "§50", "analyzed"),
    (0x218C, "I2C read reg 0x83 (2B) -> u16@0xB42 (if != 0xFFFF); call from 0x8afc", "§50", "analyzed"),
    (0xCC68, "WWDG status: r1 in {0x20000, 0x40000, 0x80000} -> [0x40002850]>>16 != 0; else ([0x40002808]&r1) && ([0x4000280C]&(r1>>4))", "§50", "analyzed"),
    (0x14958, "**WWDG mode set**: r4 1..6 -> 0xcb10(r4-1) (magic sequence with index)", "§50", "analyzed"),
    (0xBEFC, "lookup in table @0x7C4 (2 entries): range [entry+4, entry+ptr+8] -> pointer", "§50", "analyzed"),
    (0x20D8, "flag handler: bit3(@0xA71); counter @0xA7A (cap 5) -> 0xaf94(*(u32@RAM[0xDD8])) + delay 0x1F4; if 0x2a5c -> clear bit3", "§50", "analyzed"),
    (0x163B4, "GPIOA -> RCC BDCR |= 4 (0xc6a4(4, 1))", "§50", "analyzed"),
    (0x17094, "signed clamp: 0x17170(r0, r1) -> saturation [-0x80000000, ...] with special cases (-1, 0); call from motor region 0x69e4/0xe808", "§50", "analyzed"),
    (0x170E0, "signed clamp #2: 0x17214(r0, r1) -> saturation; call from 0xee48", "§50", "analyzed"),
    (0x19A1C, "**u64 sdiv**: signed 64-bit division (signs + 0x199bc unsigned + restore)", "§50", "analyzed"),
    (0x22934, "**SysTick init from struct**: r5 = u32@r4[0] (/8 if byte@+8==0); lookup 0x19968 *3 (0x3E8/0x2710/0x186A0) -> @0x1C; SysTick LOAD/VAL/CTRL from r4 (CTRL = (byte@+8)<<2 | byte@+9)", "§50", "analyzed"),
    (0xD240, "**EEPROM read+verify @0xC9C**: 0x8380(&buf, 0x30000, 8); CRC-16(4B) == u32@+4; call from 0xc420", "§50", "analyzed"),
    (0x3588, "**GPIO B/C/D/A config for NVRAM**: struct {0xFFFF, flags} -> 0x85c8(GPIOB/C/D); {0x9FFF} -> GPIOA; call from 0x2d5c (NVRAM flash write)", "§50", "analyzed"),
    (0x38EC, "**TLV + CRC-16 (table)**: 4B header + len=byte@+3; CRC-16(0x3c4c) -> {hi, lo} at end; *r2 = len", "§50", "analyzed"),
    (0x80AC, "**flash region validator**: r7 in [0x8003000, 0x801FFFF), alignment 4, size <= 0x800 -> 0x7e98 — OTA check", "§50", "analyzed"),
    (0xC2A8, "**system sleep**: poll [0x40007010]&2; [0x40007008]|=r1; [0x40007000]=(&~7)|2; **SCB_SCR |= 4 (SLEEPDEEP)**; WFI or SEV+WFE*2; clear SLEEPDEEP", "§50", "analyzed"),
    (0xCF60, "**NVRAM verify @0x305C**: 0x8380(&buf, 0x28); CRC-16(0x26) == u16@+0x26 -> u16@+0x24=1", "§50", "analyzed"),
    (0xD33C, "counter @0xA67 (cap 5) -> I2C read (0x1c60, 8B from @0x15F7); bit0/bit2(byte@+0x54) -> byte@0xF70+1 bits 0/1", "§50", "analyzed"),
    (0xDD2C, "**clamp-multiplication**: q = clamp((r3-r0)/r1, 0, r2) with rounding; return r1*q + r0", "§50", "analyzed"),
    (0x13B60, "**NVRAM verify @0x30CF**: 0x8380(&buf, 0x40000, 0xE); CRC-16(0xA) == u32@+0xA", "§50", "analyzed"),
    (0x152A, "**RLE decoder**: count [2:0] (or byte), bit4 -> literal/backward-copy; return 0", "§50", "analyzed"),
    (0x1670, "**DMA1 ch1 init (ADC)**: struct {0x4002084C, &u16@0xB7E, ..., 0x80, 0x100, 0x400, 0x20} -> 0x4f70(DMA1); 0x4fac; 0x4f38; call from 0x175c (DMA enable)", "§50", "analyzed"),
    (0x9678, "flag handler: bit1(@0xB65); counter @0xB73 (cap 3) -> clear bit1(@0xB65), byte@0xB64 &= ~0xF0", "§50", "analyzed"),
    (0x9AA4, "**telemetry reset**: zero @0x1344 (0x13B) + 0x11d6(&@0x1384, 0x4A); call from 0x51d8 (telemetry init)", "§50", "analyzed"),
    (0xC708, "clock frequency calculation: RCC_CTLR: PLLSRC bits[19:18], HSE bit0x10000; div = 2+(bits>>18) or 0x1F0-...; if HSE ready -> freq=HSE, else HSI; return freq (udiv/mls)", "§50", "analyzed"),
    (0x1647C, "UART4 TX: 0x11a4(RAM+0x10B5, data, len); byte@0x10B5+0x94=1; 0x211ec; return 1", "§50", "analyzed"),
    (0x1A24C, "UART4 RX interrupt: status check, ring buffer index update, call handler", "§50", "analyzed"),
    (0x1D818, "**2D rotate/dot (verified §60.1 — batch 16)**: motor FOC subfunction 0x1A938. Arguments: arg0=A=(a_lo,a_hi) Q15, arg1 unused. Vector X=(X_lo,X_hi) from **RAM**: X_lo=s16[RAM+0x10c], X_hi=s16[RAM+0x10e] (base r6=pool @flash 0x1d870=0x2000010c). Calculation identical to 0x1d7ac: lo=cross(a_hi*X_lo-a_lo*X_hi), hi=dot(a_lo*X_lo+a_hi*X_hi); each product /2^15 with rounding (p<0->+0x7FFF). Difference from 0x1d7ac: X is taken from fixed RAM location rather than via bl 0x1e410 (table decode)", "§50/§60.3", "analyzed"),
    (0x280C, "**I2C2 batch write 0x11B**: {u16 code, [r5&FF, r5>>8] + r6[0..0xF]} -> 0x9048(I2C2, dev 0x3E); call from 0xc158", "§50", "analyzed"),
    (0x3668, "**charger detection**: 0x8afc(); if no charging flags and u32@0xF95+0xD -> I2C read reg 0x9335 (8B) -> byte@0xB44=1", "§50", "analyzed"),
    (0xF304, "counter #7: u32@0xFBB+4 >= 0x3E8 && !flags -> u16@0xA30++; >= 0x12C -> toggle bit3(@0xF70+2), reset; call from 0x11978", "§50", "analyzed"),
    (0x1A2A4, "**timer IRQ handler @0x40012C00**: if bit31(+0x1C): [0x40012C54]&=~0x8000; byte@0x218=0; [+0x20]|=0x80; byte@0x245/0x246; byte@0x102 in {0,2} -> bit in @0x247 + u16@0x21E |= 0x100/0x200", "§50", "analyzed"),
    (0xC02C, "mismatch counter: bit0/bit1(@0xF70+1) vs @0xA65/@0xA66 -> u16@0xA68++; >= 0x32 -> toggle bit3(@0xF70+3); call from 0xc098", "§50", "analyzed"),
    (0xCE70, "**WWDG window wait**: magic 0xCA/0x53 -> +0x24; clear bit5([0x4000280C]); poll bit5 up to 0x8000; return status; final 0xFF -> +0x24", "§50", "analyzed"),
    (0x10788, "**SPI1 full init**: 0x107ec (GPIOA EXTI); GPIOA pin 0x10; struct {0, 0x104, 0, 2, 1, 0x200, 8, 0, 7} -> 0x10734(0x40013000); 0x106a0 — **SPI1 = 0x40013000**", "§50", "analyzed"),
    (0x156AC, "**EEPROM read+save**: 0xab0c(&buf[0x20]) up to 3 times; buf[0x4D]=bit1(@0xF70+2); CRC-16 -> u16@+0x4E; memcpy 0x20; ldm 4*u32 -> 0xaccc; call from threshold #1 (0xf1ec)", "§50", "analyzed"),
    (0x8A90, "**WWDG decode -> struct**: 0xcc1c + 0xccbc -> {u32@r4, u16@+4, u8@+6}; call from 0x3970/0x8938", "§50", "analyzed"),
    (0xB860, "**I2C2 busy wait**: u32@0xEFC = 0x10000; poll byte@r4+0x10C (3 -> reinit); then 0x9874(I2C2, 0x20000)", "§50", "analyzed"),
    (0xF290, "counter #8: u32@0xFBB+4 >= 0x3E8 && !flags && byte@0x107==1 -> u16@0xA2E++; >= 0x12C -> toggle bit2(@0xF70+2), reset; call from 0x11978", "§50", "analyzed"),
    (0x16410, "**checksum + divisibility**: sum(r1 bytes) + r5 + (r3%4==0 && (r3%100==0 || r3%400==0)); call from 0x1647c", "§50", "analyzed"),
    (0x310C, "**boot clock init**: 0xc664(0x10000000); 0xc6a4/c29c/c6fc/c6e4; poll 0xc858(0x61)==0; 0xc5f0(0x200); **0xce70 (WWDG window)**", "§50", "analyzed"),
    # --- §50: artifacts in giant function region ---
    (0x17736, "**artifact**: push + u16 data table (hi^lo=0xC0, 0x40 entries) — region of giant function 0x17xxx (§48.5)", "§50", "ID"),
    # --- detection artifacts in 0x17xxx region (§48) ---
    (0x177D6, "cold-tail of giant function of region 0x17xxx (b #0x173bc); detection artifact", "§48", "ID"),
    (0x178C4, "dead fragment: after strh — INVALID instruction 0x6EF5 (Unicorn: UC_ERR_INSN_INVALID); preceded by u16 table @0x177DE; hole 0x177DE..0x19A1C = one giant function missed by canonical detector", "§48", "ID"),
    # --- §51: shelf 132-256 B (98 func. / 17,840 B) ---
    (0x12AA, "u64 normalization: sh=clz(r1|r0)+0x20; 0x14e8 + 0x126c(LSR); Q-scale with constant [sp+0x28]+0xA — fixed arithmetic, caller context needed", "§51", "analyzed"),
    (0x15AA, "packed-field setter: 3-bit + 5-bit fields in u32 (pattern MODER/AFR GPIO); arg0=value, arg1=field selector", "§51", "analyzed"),
    (0x1FE0, "boot/init state machine: retry counter, GPIOB writes, delays, final flag; call from boot chain", "§51", "analyzed"),
    (0x2A94, "boot-config loader (sister of 0x2b2c): reads flash config into RAM structure; final call of case2 branch of dispatcher 0xc20c", "§51", "analyzed"),
    (0x3838, "frame parser: u16 len in [6,0x82]; header [r4+2..5]->RAM+0x10B8; chk=data[len-2], crc=data[len-1]->RAM+0x10B8+0x9A/0x9B; 0x3c4c(data+2,len-2)==u16(chk|crc<<8) && byte[RAM+0x10B8+3]<0x96 -> OK", "§51", "analyzed"),
    (0x3CAC, "event dispatcher: flag byte RAM[0x84], bits->handlers 0x11668/0x11674/0x11724/0x117d4/0x11888 etc.", "§51", "analyzed"),
    (0x3DE4, "state machine around RAM[0x89] (gate RAM[0x107]): call 0x3f00, write flash config via 0x332c", "§51", "analyzed"),
    (0x4630, "permission/gate check: byte@RAM[0xA65]=1; state RAM[0x89] in {2,3} -> RAM[0x107]; GPIOA input; return 0/1", "§51", "analyzed"),
    (0x48F8, "I2C2 polling: reg 0x94 (dev 0x3E), state bit [RAM+0xF71]; sister of 0x5274 (reg 0x93)", "§51", "analyzed"),
    (0x4A4C, "BLE command handler: routing via function pointers @RAM+0x12C..0x138", "§51", "analyzed"),
    (0x4B20, "handshake with peripheral @0x40007000 (bit9 ready) and @0x40001820; poll loop with timeout", "§51", "analyzed"),
    (0x4D48, "sliding-window signed average: u32 ring buffer in RAM, signed sliding average", "§51", "analyzed"),
    (0x5134, "u16 array statistics: args (arr, n, out); s16<=0 -> 300 IN-PLACE in arr; out={sum u32@+0, avg u16@+4, min u16@+6, max u16@+8, idx_min byte@+0xA, idx_max byte@+0xB} — both indices 1-based FIRST occurrence (update strictly < / >) (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0x5274, "I2C2 polling: reg 0x93 (dev 0x3E); sister of 0x48f8 (reg 0x94)", "§51", "analyzed"),
    (0x5330, "BLE frame sender: builds 0x16-byte frame, checksum 0x8a50, send 0xaccc", "§51", "analyzed"),
    (0x5448, "telemetry packet builder: voltage mV-2000, status bytes; after sending — 0xd878 (I2C2 read)", "§51", "analyzed"),
    (0x54DC, "frame parser (variant): validation + parse frame into RAM buffer", "§51", "analyzed"),
    (0x55C8, "BLE session/channel init: multi-step flag sequence u32@RAM[0x8C]", "§51", "analyzed"),
    (0x56BC, "response encoder: header 0x74; special payloads — ASCII \"OK\" and 25-byte block from RAM", "§51", "analyzed"),
    (0x5BC4, "mode dispatch: GPIOB pin checks + write flash config (0x332c)", "§51", "analyzed"),
    (0x5CD0, "sleep/idle loop: wake flags, sleep call, clock reinit after wake", "§51", "analyzed"),
    (0x5EE0, "BMS polling (I2C2 dev 0x3E): read reg 0x90/0xA1/0x92 + write 5-byte block", "§51", "analyzed"),
    (0x7D6C, "flash copy bounds validator: source region >= 0x3000, check copy bounds", "§51", "analyzed"),
    (0x81B4, "charging-pin debounce/state machine: GPIOB PB14, counters, voltage-window checks", "§51", "analyzed"),
    (0x8884, "BLE data-frame receiver: two size variants (2048/1024); call from 0xc368 when byte@RAM[0x88]==0", "§51", "analyzed"),
    (0x8F7C, "varargs-helper: reads value from caller stack, XOR via 0x3c7c", "§51", "analyzed"),
    (0x98C8, "ADC clock divider calculator: divider based on HSE frequency; call from 0xb09a (ADC init)", "§51", "analyzed"),
    (0xA7EC, "charging-detection state machine: I2C2 reg 0x9E + shadow registers (block @RAM+0x15FA..0x164C, §49)", "§51", "analyzed"),
    (0xA960, "NVRAM flash write: zone [0x1F000, 0x1F800) — write word with unlock 0x6378 + program 0x6304", "§51", "analyzed"),
    (0xAA18, "flash write: zone [0x1C800, 0x1D800) — write word with unlock/program", "§51", "analyzed"),
    (0xAF94, "multi-stage event/boot processor: several callback calls + final flag; call from 0xc20c (case 1/2)", "§51", "analyzed"),
    (0xB09A, "ADC config builder + I2C clock ON: struct {..,0xBFFF,0x400,..} on stack; 0x98c8(div)+0x982c(apply); base==I2C1 -> RCC+0x18|=8, RCC+0x1C|=1<<21; else -> RCC+0x18|=4, RCC+0x1C|=1<<22; then RCC+0x18|=1 (counterpart 0x97f4 clock OFF via RCC+0x10)", "§51", "analyzed"),
    (0xBCC0, "frame validator: u16 type [r4+2..3] -> descriptor from table @RAM+0x7D4; size-check smulbb([r6][8],[r6][1]) >= u16[sp+4]; 0x5dd8(1,type,r4+7,sp+4); byte[r4+6]=lo(result)", "§51", "analyzed"),
    (0xBF58, "byte bit-permutation + NOT: r6=~((b1<<3)|(b0<<2)|(b3<<1)|b2)&0xFF (r7==1) or 0xFF; dispatch by r5 (<=3) — I2C bit-banging/CRC processing", "§51", "analyzed"),
    (0xC158, "I2C2 BMS read cycle: loop over 8 entries of table @RAM+0xA80 (8B: {u32,u16 reg,..}): copy 0x20B; 0x1bdc(0x90); delay 0x3E8; 0x280c(0,8,u16[entry],sp+4) batch-write (retry *1); 0x1bdc(0x92)", "§51", "analyzed"),
    (0xC20C, "TBB mode dispatch (5 cases): case1/2 -> 0xaf94(RAM+0xDD8) + 0x1bdc(0x9A) + 0x16d4 + delay 0x186A00 (1.5M) + 0x175c/0x178c/0x10780 + final 0x8468 (case1) / 0x2a94 (case2); boot mode selector", "§51", "analyzed"),
    (0xC368, "BLE RX dispatcher: byte@RAM[0x88]==0 -> 0x8884 (receiver); u16@RAM[0x82]>0x7F -> reset; bit4[RAM+0x88]: 0x7fdc(4,RAM+0x1004,0x54,1)->(2) -> u16[RAM+0x82]|=0x10; u16==0x7F: 0x7fdc(0,RAM+0x82,2,..)", "§51", "analyzed"),
    (0xCA3C, "WWDG setup (@0x40002800): r5==0 -> [0x40002808]; else config by r4; registers +0x08/+0x24 (see 0xcd80)", "§51", "analyzed"),
    (0xCD80, "WWDG window timer: BCD encoding 4B (0xc9a8/0xc9be); magic 0xCA/0x53 -> [0x40002824]; 0xcbb8 check; CFR=[0x40002804]=r6&0xFFFF3F; 0xcc08 start; status bit5[0x40002808] / 0xce70 wait; final [0x40002824]=0xFF", "§51", "analyzed"),
    (0xD39C, "BLE frame builder: 0xabf0(sp+0xC) *3 retry; checksum 0x8a50(16B) vs u16[sp+0x22] (mismatch -> default {..,0x78,..}); cmd r4 in {0xD..0x12}: fields from RAM+0xF70+{9,0xD,0x11,0x15,0x1F,0x23}; send 0xad9c", "§51", "analyzed"),
    (0xD46C, "BLE frame builder #2: 0xab0c(sp+0x24) *3; checksum 0x8a50(7B) vs u16[sp+0x4F]; cmd r4 in {9..0xC}: fields from RAM+0xF70+7, RAM+0xF95+0x15, RAM+0xFBB+9, RAM+0xFC7+5", "§51", "analyzed"),
    (0xD534, "voltage telemetry frame: 0x11d6(sp+0x20,0x30); 0xab0c *3; 0x8a90(sp+0x18) -> copy RAM+0x98; u16[sp+0x38]=byte[RAM+0x98+5]+0x7D0 (mV+2000); checksum 0x8a50(0xA) -> u16[sp+0x42]; send 0xaccc", "§51", "analyzed"),
    (0xD5D4, "BLE frame builder #3: twin 0xd534 (same structure 0x11d6/0xab0c/0x8a90/0x8a50/0xaccc)", "§51", "analyzed"),
    (0xD878, "I2C2 telemetry read: 0x8a90(sp) -> {u32,u16,b,b}; 0x87f8(sp+8,7) -> [sp+0xF]; 0x82f0(0x50000)+delay; 0x82f0(0x51000)+delay; loop *3: delay + 0x84a0(sp+8,0x50000,8); loop *3: 0x84a0(sp+8,0x51000,8)", "§51", "analyzed"),
    (0xDE0A, "frame builder: r6=byte[sp+0x21] (varargs); copy 0x10B from RAM+0x1222; u32@RAM[0x9B8] -> 4B big-endian [sp+0xC..0xF]; 0x1ac8(sp,0x10) encode; then block @RAM+0xFE7", "§51", "analyzed"),
    (0xE200, "range check + interpolation: args {sl,fp,r8,sb,out=[sp+0x30],flag=[sp+0x34]}; range validation; 0x8f58() <= 0x1E -> -12; 0x16938(flash@0x19FD8,6) + 0x17150 (u64 cmp); r5=0x262C*e7; 0x1638a (fixed mult.); clamp -> [out]; flag=1", "§51", "analyzed"),
    (0xE740, "drift detector: byte[r5]=0; A=u16[RAM+0x13AB] (0x16504) vs ref u16[RAM+0x130A]: devA=max(0,|A-ref|); B=s16[RAM+0x13A4] (0x164f8) vs ref s16[RAM+0x1302]: devB=clamp(B-ref,+-0x8000); if devA>=500 || devB>500 -> byte[r5]=1 + refs := current values (adaptive baseline)", "§51/§51.1", "analyzed"),
    (0xEF78, "buffer init: [flash@0x1AD24]=0; 0x11d6(RAM+0x2FEC,0xE); 0x11d6(RAM+0x2FFA,0x15); byte[RAM+0x2FFE] |= 0xF8 (bits 3..7)", "§51", "analyzed"),
    (0xFBf8, "threshold counter #1: gate mode RAM[0x80]==2; bit0[RAM+0xF95+C]; u16[RAM+0xF95+8] vs flash@0x19DAA{+0,+4}: counter u16@RAM[0x9E0]++ (reset on exit, flag set on exceeding); 2nd part vs {+2,+6} -> RAM[0x9E2]", "§51", "analyzed"),
    (0xFCd0, "threshold counter #2: gate mode RAM[0x80] in {1,2}; bit3[RAM+0xF95+C]; u16[RAM+0xF95+6] vs flash@0x19DAA{+0xE,+0x12} -> counter RAM[0x9FC]; 2nd part vs {+0x10,+0x14} -> RAM[0x9FE]", "§51", "analyzed"),
    (0xFDAC, "PB15 latch #1 (debounce-hysteresis): part 1 (ON): mode@RAM[0x80]==0 && !bit0[RAM+0xFC7+6] && v=i8[RAM+0xFC7+2]>=lo(i8@F+0=1) && cnt_new>=N(u16@F+1=5264) -> GPIOB_ODR|=0x8000, bit0=1, cnt=0 (v<lo -> cnt=0); part 2 (OFF, any mode): bit0 && v<=hi(i8@F+3=70) && cnt2_new>=M(u16@F+4=17936) -> GPIOB_BRR|=0x8000, bit0=0, cnt2=0 (v>hi -> cnt2=0); counters u16@RAM[0x9F4]/[0x9F6] (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0xFE74, "PB15 latch #2 (debounce-hysteresis, INVERTED polarity): part 1 (ON): mode==0 && !bit1[RAM+0xFC7+6] && v=i8[RAM+0xFC7+1]<=lo(i8@F+6=5) && cnt_new>=N(u16@F+7=224) -> ODR|=0x8000, bit1=1, cnt=0; part 2 (OFF, any mode): bit1 && v>=hi(i8@F+9=32) && cnt2_new>=M(u16@F+0xA=17921) -> BRR|=0x8000, bit1=0; counters u16@RAM[0x9F0]/[0x9F2] (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0x10468, "threshold counter #5: gate mode RAM[0x80] in {1,2}; bit5[RAM+0xFC7+6]; i8[RAM+0xFC7+1] vs flash@0x19E1C{+0x1E,+0x21} -> RAM[0x9EE]; 2nd part vs {+0x21,+0x22} -> RAM[0x9EC]", "§51", "analyzed"),
    (0x105C4, "threshold counter #6: gate mode RAM[0x80] in {1,2}; bit6[RAM+0xF95+C]; u16[RAM+0xF95+4] vs flash@0x19DAA{+0x32,+0x36} -> RAM[0x9F8]; 2nd part vs {+0x34,+0x38} -> RAM[0x9FA]", "§51", "analyzed"),
    (0x10BA0, "PLL setup: 0xc4cc(0x10000); 0xc8a4 (wait PLLRDY/CTLR bit17) != 1 -> 0x10e10 (fallback); select mul/div by constant 0xF42400 (10 MHz HSE ref): == -> {0x30000,0,0}; > -> {0x30000,0,2}; else udiv/mls divisibility check", "§51", "analyzed"),
    (0x10CDC, "clock init: 0xc518 + 0xc8dc (wait) + 0x10e10 — clock circuit initialization", "§51", "analyzed"),
    (0x11674, "BLE sender #1: 0x11d6+0xab0c+0x8a50(chk)+0xaccc(send); handler 0x10f30; call from dispatcher 0x3cac", "§51", "analyzed"),
    (0x11724, "BLE sender #2: twin 0x11674; handlers 0x10f3c/0x10f48", "§51", "analyzed"),
    (0x117D4, "BLE sender #3: twin 0x11674; handlers 0x10f24/0x10f54", "§51", "analyzed"),
    (0x11894, "BLE session state machine TBB(5): reset on RAM[0xA48]==1; state byte@RAM[0xA51]: 0->0xec70(WWDG wait)+0xf038->1; 1->u16@RAM[0xA52]++ (wrap 0x32) + 0x44c0() -> 2/3; 2->count (wrap 0x64) -> 3; 3->0x6fc0 -> 4", "§51", "analyzed"),
    (0x11CB4, "clock switch to HSE/PLL: [0xE000ED88]|=0xF00000; RCC+0x24|=4; CFGR0 &= 0xF8FFC000; RCC+0 |= 0xFEF6FFFF & ~0x40000; CFGR0 &= 0x0700FFFF; RCC+0x2C=0; +0x30=0x3800; +0x34=0; +0x40=0; CFGR1=0x04BF8000; RCC+0x1C|=0x10000000; wait [0x40007000]&0x400; then 0x40001820", "§51", "analyzed"),
    (0x12B50, "flag sequencer: 0x130f2(0x40013800,0x424); r4=lo(u16[0x40013800+{0,4}]); counter u32@flash 0x1A808+0x10 (max 0x96): 0x4f38(v,0)+0x4f50(v) -> r5=0x96-res; bitmask state @RAM+0x190D (3-bit counter r4, bit-flags); twin 0x12d90", "§51", "analyzed"),
    (0x12D04, "copy helper: 0x11a4 (memcpy) — copy block to RAM", "§51", "analyzed"),
    (0x12D90, "flag sequencer #2: twin 0x12b50 (same structure 0x130f2/0x4f38/0x4f50/bitmask)", "§51", "analyzed"),
    (0x12F44, "copy helper #2: 0x11a4 (memcpy) — twin 0x12d04", "§51", "analyzed"),
    (0x13148, "HSE freq -> divider setup: 0xc708 (calculation of HSE freq = div * 0x7A1200) + write dividers", "§51", "analyzed"),
    (0x139FC, "telemetry packer: byte[RAM+0xD9]=0, [RAM+0xD8]=1; 0x8a90(sp) -> copy RAM+0x98; V*100: ((byte[RAM+0x98+5]+0x7D0)>>8, &0xFF) -> RAM+0xDA..0xDB; nibble-pack fields [RAM+0x98+{4,6}] -> RAM+0xDC; flags 0x80/~0x40 @RAM+0xDE", "§51", "analyzed"),
    (0x15918, "field decoder: 64B constant from code-stream (adr+ldm); u16[RAM+0x1FAC+4] via 0x3bc4(u16,byte[RAM+0x1F10+0x99],RAM+0x1F10+3); loop comparing bytes with table @RAM+0x1F10+3 (0x11ec search): mismatch -> state 6/7 @RAM+0x1FAC+3; match -> decode 2B big-endian", "§51", "analyzed"),
    (0x15B84, "command code state machine: 0x158f8(); byte[RAM+0x1FAD+1]==0: decode byte[RAM+0x1FAC+2]: {0->4, 2->0, 1->5, 3->0+RAM[0xC7E]=1, 4->0, 5->0, 6->2, else->6} @RAM+0x1FAC+3; byte==1: RAM[0xC7E]=0 + 0x15f00()", "§51", "analyzed"),
    (0x15D14, "parser (self-contained): block parsing without calls — field arithmetic/validation; part of parser family @RAM+0x1Fxx", "§51", "analyzed"),
    (0x15DF4, "parser: 0x119e4 + 0x3bc4 + 0x3b82 *3 + 0x7fb8 + 0x80ac — multi-step field validation/decoding", "§51", "analyzed"),
    (0x16040, "u64 <-> double conversion: VFP constants (vldr d0/d8 from pool); bits[24:13] low word - 0x3FF, range [0,0x14]; 0x1346 (u64 build) + 0x1494 (signed cmp) — fixed point <-> float for telemetry", "§51", "analyzed"),
    (0x167B6, "piecewise linear interpolation Q8: args (value, xtab_u16, ytab_u8, last_idx=n-1); binary search in s16 x-table; slope=((v-x0)<<8)/dx (udiv, exact floor); y=(y0 +- dy*slope>>8)&0xFF (both branches); v>=xs[last] -> slope=0x100 (Q8 1.0) -> full step to ys[n-1] (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0x16880, "piecewise linear interpolation Q31: args (value, xtab_u16, ytab_u32, last_idx=n-1); binary search in s16 x-table; slope=0x161ea((v-x0)<<16, dx, 0xF)~=(v-x0)/dx<<31; branch on SIGNED cmp ys[r4] vs ys[r4+1] (bgt), delta wrapped u32: result = A +- (delta*slope)>>31 (both branches interpolate); v>=xs[last] -> sentinel 0x80000000 (Q31 1.0) -> full step to ys[n-1]; caller: 0xe170 (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0x16938, "interpolation #2: twin 0x16880, BUT branch on UNSIGNED cmp (bhi instead of bgt) — otherwise same Q31 semantics; call from 0xe200 (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0x169F0, "Q16 helper: 0x161ea — fixed-point division Q16 (part of interpolator family)", "§51", "analyzed"),
    (0x16B22, "Q16 helper #2: twin 0x169f0 (0x161ea)", "§51", "analyzed"),
    (0x16F42, "double binary search: u32 x-table via [ip] (size [r4]) + signed u16 y-table [r7]; 2D lookup/interpolation; **§57: on current flash tables part-2 performs OOB read** (s16[vtbl@0x1A02C][0]=-10941 < any s8 v2 -> binary-search path -> u32[hdr+4]=0x98001053 read as last_idx_y -> out of grid); part-1 always early-exit (u32[htab@0x19F30][0]=0x43184610 > any u16 v1); single caller 0x69E4 (§53) -> fault in emulation @0x16FA2 (latent bug / runtime patch of tables)", "§51/§57", "analyzed"),
    (0x16FDE, "double binary search #2: twin 0x16f42 (u16 x-table + signed u16 y-table)", "§51", "analyzed"),
    (0x17170, "i16 * i16 -> u64 sign-extended: args (a, b, *out_hi, *out_lo); abs() of both, 16*16->32 with carries (mul/mla), on different signs — two's complement; [arg2]=hi (0/0xFFFFFFFF), [arg3]=lo (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0x17214, "multiplication helper #2: twin 0x17170 (i16*i16->u64, same output convention) (§51.2 emulator)", "§51/§51.2", "analyzed"),
    (0x19AB0, "u64 shift helper: 0x1a0f8 + 0x1a0e8 — u64 shifts (cluster 0x1a0xx, §50.6)", "§51", "analyzed"),
    (0x19DBC, "u64 helper: call 0x1a184 (LSL with normalization) — wrapper of cluster 0x1a0xx", "§51", "analyzed"),
    (0x19E8C, "u64 helper: call 0x1a16a — wrapper of cluster 0x1a0xx", "§51", "analyzed"),
    (0x1A184, "u64 LSL with normalization: r2=0x21b24(count) [+0x20 if count==0]; 0x1a080 (u64 LSL); OR with previous; ==0 -> return; else 0x40-[sp] + 0x1a0a0 (u64 LSR)", "§51", "analyzed"),
    (0x1BE1C, "**TIM capture -> FOC phase current reconstruction (verified §60 — batch 16)**: subfunction of motor FOC routine 0x1A938. Gate: bit15 of low 16 bits u32[0x40012C54] (=TIMER_A+0x14): ==0 -> mode 1 (OUT @RAM+0x838/0x83C/0x840 = clamp(r0[+0xc/+0x10/+0x14])); ==1 -> mode 2. Mode 2: dispatch by u16[r0+2] (sector) via computed-goto **0x21b52** (byte jump-table, count=7, idx>=7->table[7]=null): **0->null, 1->B, 2/3->C, 4/5->A, 6->B, >=7->null**. Handlers (T28/T2C/T30=u32[0x40012440+{28,2c,30}], C18/C1A/C1C=u16[r0+{18,1a,1c}]): A: o_c=(T28-C18)<<4, o_10=(T2C-C1A)<<4, o_14=-(o_c+o_10); B: o_10=(T2C-C1A)<<4, o_14=(T30-C1C)<<4, o_c=-(o_10+o_14); C: o_c=(T28-C18)<<4, o_14=(T30-C1C)<<4, o_10=-(o_c+o_14); null: r0[+0xc..] unchanged. Verified: 6 sectors, bit15 gate, clamp logic", "§51/§60", "analyzed"),
    (0x1C234, "TIM register update: [r0+0x30] &= ~0x100; [r0+0x2C].. — update ARR/RCR of TIM without interrupts", "§51", "analyzed"),
    (0x1D330, "NON-canonical function (gap): getter s16[RAM+0x13A4] (ldrh [pool 0x20001384 + 0x20]); part of getters family of block @RAM+0x1384", "§51/§51.2", "analyzed"),
    (0x1DEA4, "NON-canonical function (gap): getter u16[RAM+0x13AB] (ldrh [pool 0x20001384 + 0x27]); family: 0x16510 byte@+0x22, 0x1651c u32@+0x34, 0x16528 u32@+0x12, 0x16534 u32@+0xA", "§51", "analyzed"),
    (0x1E1A0, "NON-canonical function (gap): MSB-normalization shift: x==0 -> 0x20; else 0x1E - msb_pos(x) (shift placing MSB into position 30); call from 0x1a184", "§51", "analyzed"),
    (0x1E658, "NON-canonical function (gap): varargs jump-trampoline: len=byte[lr-1] (clamp r3), jump [base + len*2] — byte jump-table", "§51", "analyzed"),
    (0x22824, "NON-canonical function (gap): NVIC ISER0 setter: r0>=0 -> [0xE000E100] = 1<<(r0&31) (standard ISER, unlike custom 0xE000E400 in 0x21b84)", "§51/§59", "analyzed"),
    (0x22B7C, "u64 Q20 fixed-point arithmetic (motor chain): args (a0,a1,a2,a3); sign=sb(a1)^sb(a3); a0<a2 -> swap pairs; a2==0 -> return (a0,a1); dfrac=(a1&0xFFFFF)-(a3>>20), threshold 0x40; core: X={0x100000+(a3&0xFFF):a2}, Y=X<<(0x40-dfrac), Z=X>>s dfrac (0x1a080/0x1a0c2), W=Z+A, +{0x100000:0}, >>1; branches via 0x1a16a/0x1a184; caller: 0x22274 (bl @0x222f2); twin 0x1346 (11-bit dfrac, core 0x14e8/0x1506/0x12aa)", "§51", "analyzed"),
    (0x22C70, "u64 Q20 fixed arithmetic #2: twin 0x19c58 with 11-bit dfrac (ubfx #0,#0xb) and core 0x14e8+0x1506+0x12aa; caller: 0x16040 (u64<->double, §51)", "§51", "analyzed"),
    (0x22E0C, "**2D bilinear interpolation on u16 grid**: values — stack-passed ([sp+0x1c]/[sp+0x20], codegen artifact); arg2=xtab1 (u16), arg3=ystruct {u32 x0, u32 count, u32 ys...}; [cs]=ygrid (u16, stride=[cs+8]=5), [cs+4]=**hdr-pointer** -> {u32 last_idx_x, u32 last_idx_y} (NOT counters!; §56: emulator-confirmed — bl does not push lr, callee SP = caller SP); part1: binsearch value1->idx1 + Q16 slope (direct udiv); part2: binsearch value2->idx2 + Q16 (0x161ea n=0x10); yA=interp(grid[idx2*5+idx1],+1,slope1), yB=same in row idx2+1, result=yA+-(yB-yA)*slope2>>16 (u16); caller: 0x69e4 (flash table @0x19F60: xtab1@+0xBC, ystruct@-0xAC, grid@+0x550); **§56**: hdr words in flash are garbage (0x05014674/0x41611C38), but their read path (v1>xtab[0]=2002) is unreachable: caller passes s8 (-128..127) -> always early-exit with zero slope", "§51", "analyzed"),
    (0x22EDC, "**2D bilinear interpolation #2**: twin 0x16bd4 with u32 tables (stride #2) and Q8 slopes (0x161ea n=8, uxth); same stack-passed values; caller: 0xe2cc", "§51", "analyzed"),
    # --- §51.1: small functions in gaps (detector artifact: no push prologue) ---
    (0x164F8, "**NVRAM zone @RAM+0x30CF — I2C2 page reader**: struct {u16 counter@+0, u32 regA@+2, u32 regB@+6}; range-check regA/regB in [0x41000,0x45000) else reset to 0x41000+flag=0; if u16[+6]&0xFFF==0 -> read register regB (0x82f0) + wait 1000; retry*3: 0x84a0(regB, len=0x20, buf=stack) — 32B page; success: counter++, if >0x200: regA += 0x1000 (wrap->0x41000), counter=64; regB += 0x20 (wrap); 0x147ac (zone CRC verification §50) -> return 1; failure: delay 500", "§51.1", "analyzed"),
    (0x16504, "**NVRAM zone @RAM+0x304C/0x305C — I2C2 page reader**: struct {u32 counter@+0 (max 0x1F4=500), u32 regA@+4, u32 regB@+8}; range-check in [0x21000,0x25E20); read register regB (0x82f0) + wait 1000; retry*3: 0x84a0(regB, len=0x28, buf=RAM+0x305C) — 40B page directly into RAM; success: counter++, if >0x1F4: regA += 0x28 (wrap->0x21000); 0x1570c (CRC verification) -> return 1; failure: delay 500", "§51.1", "analyzed"),
    (0x21B24, "**I2C2 block manager @RAM+0x1FD4 (2KB buffer @+0x800)**: args (reg_code, src, len, mode); validation: u32[+0x800]+len <= 0x800, u32[+0x804] >= len; copy to ring buffer @+0x808; mode 1/2: trigger I2C transfer via 0x15758; return status", "§51.1", "analyzed"),
    (0x21B52, "**I2C2 command transmitter**: prepares header {dev 0x3E, reg, len}, computes CRC-7 via 0x15640, sends via 0x90a0", "§51.1", "analyzed"),
    (0x21B6C, "**motor duty ramp controller**: reads current speed, throttle target, applies PI filter, clamps output to [1000, 32760]", "§51.1", "analyzed"),
    # --- §52: shelf 257-512 B (38 func. / 13,026 B) ---
    (0x19C58, "**motor status packet encoder**: formats motor speed, current, temperature, fault flags into 16-byte buffer", "§52", "analyzed"),
    (0x1346, "**Hall sensor angle interpolator**: computes rotor electrical angle from 6-step Hall state and timer capture delta", "§52", "analyzed"),
    (0x16BD4, "**field weakening controller**: advances commutation angle at high speed when back-EMF exceeds voltage threshold", "§52/§56", "analyzed"),
    (0x16D8E, "**regen braking controller**: computes regenerative braking current command based on brake lever position and speed", "§52", "analyzed"),
    (0x14802, "**phase current offset calibration**: measures ADC zero-current offsets at startup, averages 64 samples", "§52", "analyzed"),
    (0x157E0, "**overcurrent protection ISR**: immediate PWM shutdown via TIM break input, sets fault flag in RAM", "§52", "analyzed"),
    (0x119E4, "state machine comparison: compares table @RAM+0x1FAC with flash @RAM+0xB8E (index u16[RAM+0x1FAC+0xc]-3); on table match -> 0x15758", "§52", "analyzed"),
    (0x0B302, "**I2C bus recovery (SCL toggle)**: builds 20B struct {u16[caller+0x2c], 1, 0xF} via 0x87b0; 0x85c8(struct, [caller+0x24]) — GPIO/AFIO config; wait 1000; loop *9: 0x87e2(pin, 0) + wait 20, 0x87e2(pin, 1) + wait 20 — 9 SCL pulses to unwedge stuck I2C bus; bl 0x87b0/0x85c8/0x87e2/0x985c/0x982c/0x11a4/0xbc84/0xc684/0xc664/0xc6a4 (§50.7.3 RCC)/0xaf94", "§52", "analyzed"),
    (0x06CCC, "**BLE session state machine #1**: state byte[RAM+0x12BA+0x63], counter [+0x64] (<0x1F++); init: [+0x62]=1, state=2, i32[RAM+0x128B+0x14]=-2, u32[+0x3C]=0; state1: counter>=0x14 -> state2; state2: 0x8e14()==1 -> state3, i32[+0x14]=-33, u32[RAM+0x12BA+0x34]=0x164d4(); state>=3: 0x8e20()==1 -> state=1, counter=0, ts={0x164d4(), 0x164e0()} + **0xe200**(u32[+0x34], u32[+0x38], ts) — caller of interpolator 0x16938 (§51); timeout: u32[+0x3C] >= 0xA8C0 (43200 ticks) -> state2; bl 0x10fe0/0x8e14/0x164d4/0x164e0/0x8e20/0xe200/0x10f7c; twins: 0x6e50/0x6838/0xea64", "§52", "analyzed"),
    (0x06E50, "**BLE session state machine #2**: twin 0x6ccc (same pair of structures RAM+0x128B/0x12BA); handlers: bl 0x10fec/0x16534/0x10f3c/0x8dc0/0x10e74/0x16540/0x10f48/0x8dcc/0x10e80", "§52", "analyzed"),
    (0x06838, "**BLE session state machine #3**: twin 0x6ccc/0x6e50; handlers: bl 0x10fbc/0x1657c/0x16504/0x10f30/0x8db4/0x10e8c/0x10ea0", "§52", "analyzed"),
    (0x0EA64, "**BLE session clamp handler**: 0x8d90() (fixed-address getter §50.7) *several; comparison with [arg0] (threshold): negative value -> clamp to max(-0x80000000, ...), positive -> min; structure RAM+0x128B/0x12BA (pair of sessions §52); bl 0x8d90/0x10e5c/0x1654c", "§52", "analyzed"),
    (0x1D640, "**motor TIM init (re-analyzed §59, emulator-verified — batch 13)**: phase 1 — channel blocks **@0x48000000** (A: 3 iterations, +0x2C=0x666, +0x10=0x2A0000) and **@0x48000400** (B: 4 iterations, +0x2C=0x66660000, +0x10=0xAA000000; each iteration: +0x2C |= 0x6-nibble, zero +0x14..+0x28, +0x10 |= bit); phase 2 — TIM @**0x40012C00**: +0x3C=0x8CA (prescaler 2250), CCR +0x44/48/4C = 0x45B (1115) -> then 0, +0x50=0x8C9 (2249), +0x54=0x1D24 (7460), +0x30=0x1DDD (ARPE-like bits), +0x28/+0x2C=0x6060, +0x04=0x2A00, +0x0C=0x80; **enable +0x00=0x41 — last write**; 107 writes, deterministic; r0=0x41", "§52/§59", "analyzed"),
    (0x22000, "**validated timer descriptor setter (assert)**: arg0 in {9<<0x1B=0x120000, 0x48000400, 0x48000800, 0x48000C00} else **cpsid i; b .** (assert!); arg1 in {1..0x80, 0x100, 0x1FA, 0x400..0x10000}; struct bytes: [0] in 0..3, [1] in 0..2, [2..5] in 0..1, [6] in 0..9 — each with cpsid i assert; writes field by (base, mask)", "§52", "analyzed"),
    (0x23040, "**timer base+mode validator/dispatcher**: arg0=&struct{u32 timer_base,...}, arg2=mode; valid bases: 0x40012C00 (mode {0,1,2,4}), 0x40014000/0x40014400/0x40014800/0x40014C00/0x40000400.. (mode {0,1}); invalid -> 0x230f2; dispatch: 0x22d2c/0x22e0c/0x22edc (§51 ARR)/0x22fac", "§52", "analyzed"),
    (0x1A688, "**timer capture handler @RAM+0xAC**: u32[+0x40] — counter (clamp <= 0x2710=10000, else +1); u16[+0xE] — mode (==arg0 -> exit); s16 from [RAM+0x1768+8] (threshold 0x1E); write to 0x40012C40 (TIM cluster +0x40 = CCR register); state u32[+0x3C]", "§52", "analyzed"),
    (0x110FC, "**power/shutdown state machine**: state byte[RAM+0x2F] (0..3); state0: byte[RAM+0xA64]=0, byte[0x35]=3, 0x5bc4(0), ->state1, 0x5cd0(5); state1: if byte[RAM+0x37]==2 -> **0x5c9c()** (NVRAM flash-write §49) + u32[RAM+0x8]++/u32[RAM+0xC]++ (boot counters) ->state3; if ==1 -> 0x5cc0() ->state2; state2: 0x111f6; state3: u16[RAM+0x4]++ (timeout, when >=0x2BC=700 -> reset to state1); bl 0x5bc4/0x5cd0/0x5c9c/0x5cc0/0xc94c/0xd938/0x22f4/**0x8bec** (voltage-reset §52); SCB 0xE000ED0C + 0x5FA0000 at tail (sleep/reset)", "§52", "analyzed"),
    (0x0ACCE, "**OTA metadata circular logger (flash @0x1F000/0x1F800)**: r4=0xa910(0) (OTA sector counter §50); 8 slots * 8B in each zone (r5/r7 = base + slot*8); 56B record on stack: 0x11d6 init, magic 0xAA, copy 48B, **CRC-16/CCITT 0xaad0** (§50.7) -> high 16 bits @+0x38; slot==0 -> full erase 0x7e98(0x1F000); overflow -> 0x80ac (OTA validator §50) of both zones, else 0xa960 (§51 flash write); success: byte[RAM+0x7C]++ (wear counter), when >3 -> erase of both zones", "§52", "analyzed"),
    (0x13C78, "**RAM-state snapshot @RAM+0x98**: 0x8a90(sp+0x24) (ADC-read §50.7) -> {u32@+0, u16@+4, byte@+6} in RAM+0x98; copy 0x19 (25)B: RAM+0x309D+0x19 -> RAM+0x309D-0x19 (mirror zone §50); bl 0x8a90/0x11a4; flash calibration @0x19575", "§52", "analyzed"),
    (0x08BEC, "**voltage table reset handler**: gate = bit2 byte[RAM+0xF70+3]; toggle bit0 byte[RAM+0xA72] (cap 3, pattern §50 0x1984); if !bit -> u16[RAM+0xF10+i] = 0x9C4 (2500 mV default) for i<13; bl 0x8af0 (fixed-address getter §50.7)", "§52", "analyzed"),
    (0x21E18, "**ADC1 validated channel-sequencer (full analysis §58)**: args (r0=main struct {base, [8]=mode}, r1=chan_cfg); asserts (cpsid i; b .): chan<=18, rank<=4, u32[+8]<=0xFFF, byte[+0xC]<=3; **[base+0x54]**: bit slots — clear 2 bits @rank*6+2, set chan<<(rank*6+2) (field rank->channel), low 2 bits=cfg[0xC]; **sampling** (3-bit field, value=u32[chan_cfg+4]): ch0-2->[+0x20]@8/16/24, ch3-6->[+0x24]@0/8/16/24, ch7-10->[+0x28], ch11-14->[+0x2C], ch15-18->[+0x30] — BUT **raw-shift (not mod-32!): shifts >=32 -> 0, only ch0..6 reachable** (ch7-10 compensated by caller 0x1C0B0 via final OR); **SQR[rank]**: rank 1-4 -> [base+0x58/5C/60/64] = u32[chan_cfg+8]; SMPR1 bit25 = (cfg[0xD]==1); mode==2 && cfg[0xD]!=0 -> state flags byte[struct+0x39]|=8, [+0x3A]|=1; return 0; emulator-verified (batch 11)", "§52/§58", "analyzed"),
    (0x0EE48, "**buffer/queue manager @RAM+0x2FFA**: args (src {u16 len}, dst, ?); clamp u16[src]-0xF; if u16[dst] < clamped -> s8[RAM+0x2FFA+0x14]++ (overflow counter); bl 0x170e0", "§52", "analyzed"),
    (0x01E94, "**flag bit-pack from byte[RAM+0x15F7+2]**: bit7->out bit0, bit5->out bit1, ... (sequential cbz/bfi); return {u32, u32} on stack; pure bit extraction", "§52", "analyzed"),
    (0x04344, "**GPIOB state machine**: u32[RAM+0x110] = u16[RAM+0x15F7+0x34] * 10; gate byte[RAM+0x107]==0 + bit2 byte[RAM+0xF70+1]; compare with 0xE09C; 0x87c8 (set/clear GPIOB §50) + 0x332c (flash config writer §51); GPIOB @0x40010C00", "§52", "analyzed"),
    (0x06080, "**threshold state machine @RAM+0xFC7**: gate mode byte[RAM+0x80]==1; s8[RAM+0xFC7+2] in [0x41, 0x64) and s8[+1] > -0x14 -> actions (value block of PB15 latches §51); bl 0x11bac", "§52", "analyzed"),
    (0x0DF10, "**frame parser (magic 0xAA)**: from struct arg0: byte[2]->[sp+0x18] (compare with 0xAA), u16 = byte[3]|byte[4]<<8 -> [sp+0x19], nibble byte[5]>>4; TBB dispatch; bl 0x11a4/0x3b42/0xded4/0xe06c/0xde08/0xe0b4/0xdea4 (handlers); pool RAM+0x9B4/0x9BC", "§52", "analyzed"),
    (0x2186C, "**u16 counter manager @RAM+0x2BA**: if u16[0x2BA] >= 0x7D<<3 (63488) -> reset 0, byte[0x2B9]++ (cap 0x3C=60, wrap); sequential bytes RAM+0x2B0..0x2BA; bl 0x19968", "§52", "analyzed"),
    (0x0EC70, "**BLE session state reset**: u32[[flash 0x1A538]] = 0 (NVRAM zone §49); 0x11d6(RAM+0x128B, 0x2F) + 0x11d6(RAM+0x12BA, 0x8A) — init of session structs; 0x10ff8(0); 0xe3e4(sp) (memset §50.7.1); zero fields of both structs; bl family 0x10fa4..0x1101c (small setters)", "§52", "analyzed"),
    (0x173CC, "**GPIO/AFIO config from flash tables @0x1A780/0x1A794**: u16 from flash -> struct on stack {u32*4, byte flags}; bl 0x85c8 (AFIO §52) + 0x87e2/0x87c8 (set/clear GPIO §50) + 0x2d70; GPIO port init from calibration tables", "§52", "analyzed"),
    (0x0BD50, "**frame field extractor/dispatcher**: from frame arg0: byte[2], byte[3] -> RAM+0x1154; field layout [2..8] depends on byte[3] (==3: {+2..+5}, ==6: {+2,+3,+7,+8}, ==0x10: {+2..+6}); bl 0x11a4/0x8a50 (checksum §51); pool RAM+0x1154", "§52", "analyzed"),
    (0x15A60, "**RLE-like codec**: args (dst?, len <= 0xFF); len > 0x32 -> alternate path; index r7*25 (r7 + r7<<3 + r7<<4); magic 0xAA/0xBB; bl 0x11ec/0x11fa/0x11d6 (init)/0x11a4 (u64-OR helper)/0x3b82; pool flash @0x1A93C", "§52", "analyzed"),
    (0x04508, "**state machine byte[RAM+0x11D]**: state0 -> if byte[RAM+0x31]==1: u16[RAM+0x120]++; state1 -> 0x4586; state2 -> 0x45f2; bl 0xd670/0xd5d4/0xd534; pool RAM+0x11C..0x124", "§52", "analyzed"),
    (0x01AC8, "**buffer processor with flash tables @0x19D3E/0x19D7E**: args (buf, len); 0x3b42(buf, len) -> r8; loop over bytes buf[i] with indexing in flash tables; bl 0x3b42", "§52", "analyzed"),
    (0x05DD8, "**command dispatcher**: args (r8, type, r5, r7) + stack-arg [sp+0x20]=&state; type==3 -> dispatch by byte[[state]] in {0,1,2}; bl 0x5a68/0x11a4 (u64-OR helper)", "§52", "analyzed"),
    (0x0F038, "**frame builder with retry**: 0x11d6(sp+4, 0x30) — init 48B frame; loop *3: 0xab0c(sp+4) (fetch/retry §51), on !=1 -> retry (counter r5); 0x8a50 (checksum §51); pool RAM+0x59/0x5A/+0x1359; bl 0x11d6/0xab0c/0x8a50", "§52", "analyzed"),
    (0x08938, "**ADC sample handler**: 0x8a90(sp) (ADC-read §50.7) -> {u32@+0, u16@+4, byte@+6} in RAM+0x98 (same struct as 0x13c78); read byte[RAM+0x98+5]; bl 0x8a90/0x1647c; pool RAM+0x98/+0xF64", "§52", "analyzed"),
    (0x244D2, "**detector artifact**: push-prologue in data region near end of image (0x244D2..0x2459A, before FOTA trailer @0x24845); disasm = gibberish (cdp2, random movs); **no callers** (bl scan) — not code", "§52", "ID"),
    (0x085C8, "**GPIO port configurator (descriptor-driven)**: args (port_base, pin_desc); desc = {u16 pin_mask@+0, byte@+2 (AF), byte@+3 (ODR bit), byte@+4 (pull: 1=down/2=up), u32@+8 (mode code: 0/2/3/0x11/0x12/...), u32@+0xC (MODER val)}; per pin: MODER_L/H [port+0x20/+0x24] 4-bit field, CRL/CRH-like [port+0/+0xC] 2-bit fields, AFR [port+0x2C] (if mode&3 not in {0,3}), ODR [port+8] bit, PUPDR [port+0x18]/[port+0x28]; AFIO @0x40010400 at tail (EXTI); call from 0xb302 (I2C recovery §52) and 0x173cc", "§52", "analyzed"),

    # --- §53: shelf 513-1000 B (17 func. / 11,378 B) ---
    (0x16588, "**3D trilinear interpolation on flat u16 grid**: args ({ix,iy,iz}, {sx,sy,sz} Q16, grid_u16*, {1,syy,szz}); base=ix+syy*iy+szz*iz; 5 steps _interp16 (unsigned cmp of neighbors, delta*Q16>>16, u16): x-neighbor (stride 1) *2 layers, y-merge, z-merge; **emulator-verified** (batch 7); twin 2D: 0x16bd4/0x16d8e (§52); callers: 0xe2fc (multi-interpolation §50) <- 0x69e4", "§53", "analyzed"),
    (0x22274, "**clock-governor (system frequency + FLASH ACR)**: arg0 = {u32 value@+0 (**assert !=0**, cpsid i), byte mode@+4, u16 code1@+6, u16 code2@+8, byte m@+0x20}; start: u32[FLASH+0x10]=3 (ACR); read signed-nibble fields from RCC: AHBPRESC [16:19] and [2:0]/[8:11], APB1PRESC [4:7]/[12:15]; chain of dividers 0x19968 (floor division, §55)/0x19ff4/0x19f7c -> core **0x19c58** (§52) -> target frequency; write: u32[RAM+8]=freq/2, u32[RAM+0]=selected target by AHBPRESC[2:0] (0/1->4e6, 2->calc, 3->48e6), u32[RAM+4]=copy, u32[RAM+0xC]=APB derivative (AHBPRESC>>4); RCC+0x0C[15:8] <- f(1e6); AHBPRESC: bits[11:8]<-0x8 (mask 0x0F00), bits[2:0]<-mode; code1 in {0,8,9,5,11,3,13,7,15}<<8 -> OR into AHBPRESC (else assert), code2 in {0,7,2,3,4}<<12 -> replace bits[12:15]; **FLASH ACR by frequency thresholds**: >72 999 999 -> |=3, >48 999 999 -> +2, >24 999 999 -> +1; busy-delay 0x22934(&{FLASH,0,1,1})+0x229d4(1); bl 0x21c18(3) -> return 0; **method note §53**: capstone with odd start (off|1) shifts ALL addresses and bl targets by +1 — true targets = label-1; mcu_annot.py (even start) is correct", "§53", "analyzed"),
    (0x225F4, "**PLL/clock-switching state machine**: arg0 = request struct or NULL; byte@+0xC = **phase mask** (bit0/1/2); start (arg0!=NULL): byte@+0x15 in {0,1} (else assert), 0x225c4(bit 0 RCC+0, val) by AHBPRESC[2:0] and [20:23]; phase bit0: byte@+0x14 in {0,0x10,0x50} (else assert), 0x225c4(0x10/0x40) + **bounded wait** (tick u32[RAM+0x2C] via 0x21c0c, timeout 0xA -> return 3); phase bit1: u32@+0x1C in {0,0x1000} (else assert), 0x225c4(0x100) + wait; phase bit2: u16@+0x10 in {0,0x100} (else assert), 0x225c4(0x1000) + wait; final: u16@+0x16: 0 -> u32[RCC+0x40] &= ~0x400, 0x225dc(0x100,0), spin until bit8 of RCC+0x60 clears; 0x500 -> |=0x400, 0x225dc(0x100,1), spin until bit8 sets; else -> 0x225dc(0x100,1)+spin; byte@+0x18: 0 -> 0x225dc(1,0)+spin until bit31 clears, else 0x225dc(1,1)+spin until bit31 sets; return 1 (success) / 3 (timeout)", "§53", "analyzed"),
    (0x0332C, "**GPIO batch configurator (descriptor array)**: args (desc_ptrs*, count); per desc (20B): {u32 port@+0, u16 mask@+4, byte@+6, u32 type@+7, byte@+0xB, u32@+0xC, byte@+0x10..0x13}; 6 known type codes {0x1011,0x1021,0x1031,0x1012,0x1022,0x1032}*0x10000: 0x87b0(port,&mask), mask->local, if port==GPIOB(0x40010C00) and mask==0x800 -> byte@+6 else 0; **0x85c8**(port, &local) (GPIO configurator §52); 0x2bbc(port, mask, sp); delay code in local[0xD]: type *1 -> 8, *2 (A in {1,2}) -> 0xC, else 0x10; struct {1,0,1,delay} -> **0x59a4**; bytes@+0x11..0x13 -> **0xc0b4**; ALT-path (unknown type): generic 0x85c8", "§53", "analyzed"),
    (0x069E4, "**2D interpolator caller + BLE session (RAM+0x128B/0x12BA)**: 0x10fd4(1); r4/r5 = max/min of pair 0x8ecc()/0x8ee8(); local[0xC]=u16 \"target\": if max-min >= 0x3E8 -> 0xC80; elif min < 0xC80 -> min; else 0x17094(min-0xC80, 0x3E8) -> 0x16328(0x3E8-max+min, t), clamp [0,0xFFFF] (threshold pool 0x7FFFF37F); **0x16bd4**(0x8f58(), |0x1654c()|, xtab1=0x19F60+0xBC, ystruct=0x19F60-0xAC, [stk]{grid=+0x550, base, 5}) -> r7; byte[RAM+0x128B+0x65]: 0 -> init (byte[+0x66]=3, u32[sp+0x10]=0xA, u16[RAM+0x12BA+0x24]=local[0xC]); else state@+0x66: 1 -> check thresholds (0x8f58()+5, 0x1654c() vs pool -1534) -> 3 or merge via **0xe2fc/0xe2cc** (§50) + u16[+0x24]; 2 -> local[0xC] >= 0xF6E? -> 3 : 0xe808(&local[0xC], &sp+0x10); else -> 0x1654c() <= r7 and 0x8f58()+5 < 0 -> 3 : state=1 + merge; x2 branch: local[0xC] > 0xFA0 and 0x1654c() > 0 -> state=2, u32[+0x40]=0, u16[+0x4E]=0, u16[+0x4C]=local[0xC], byte[+0x67]=0, u32[+0x2C]=0x105F, 0xe808; final: 0x1654c() > 0 -> r6=0x64 else **0x16f42**(r4, 0x8f58(), vtbl=0x19F58-8+0xD4, htab=0x19F58-8-0x28, [stk]{grid=+0x5C7, base, 5}) -> r6; u16[RAM+0x12BA+0x2D]=min(r6, sp+0x10); 0x11028(u16[+0x24]); **hdr anomaly §53 — RESOLVED (§56)**: u32[0x19F60]=0x05014674 / u32[0x19F58]=0x43D22201 — invalid last_idx, BUT their read path (v1>xtab[0]=2002) is unreachable: v1=0x8f58()=s8 in [-128..127] -> 0x16bd4 always goes early-exit (zero slope, constant result from grid[0..1]); table xtab {2002..63734} — curve over full u16 range (~3%..97%) — for a different caller; latent version bug", "§53/§56", "analyzed"),
    (0x0D938, "**telemetry flag-packer + send**: arg0 = u16 type (0/8/9) -> u16[pool]; type==0 -> 0x11a4(0x28, ptr); type 8/9: u16[type_ptr]=arg0, **0x8a90**(sp) (ADC-read §50.7 -> {u32,u16,byte} in sp), copy to out struct (+0..+6, +7..+0x1C from ~12 RAM structs pool); **bit-scatter**: ~30 individual bits from struct bytes (offsets +0x2/+0x3/+0x6/+0x8/+0x9/+0xC/+0x10/+0x17) -> u32 packed flags -> u32[out+0x20]; u16[out+0x24/0x26]=0; **0x8a50**(out, 0x26) (checksum §51) -> u16[out+0x26]; **bl 0x157e0** (§52 I2C2 NVRAM page reader — pipeline step)", "§53", "analyzed"),
    (0x070D8, "**BLE session SM #5 (RAM+0x128B/0x12BA)**: 0x11004(1) (acquire §52); counter byte@+0x59 (mod 32); flash table @0x1A4D8; bl: 0x10f24 *2, 0x8da8 *3, 0x1651c, 0x17150 (u64 converters §50/51), 0x164ec *5, 0x16b22, 0x10f54 *5, 0x8dd8 *3, 0x8e9c *3, 0x11004, 0x16266, 0x11034, 0x10e68, 0x110a4, 0x1638a, 0x110b0, 0x10eb8, 0x10ec4 — same session family as §52 (0x6ccc/0x6e50/0x6838)", "§53", "analyzed"),
    (0x03F00, "**frame builder 48B (telemetry)**: 0x11d6(sp+0x28, 0x28) *3 (frame init §52); bl 0x30a6, 0x2b2c, 0x1180, 0xdd2c *2, 0x11a4, 0x3b42, 0x13284; pool: cluster RAM+0x9B4..0x9BE (5 adjacent structs), RAM+0x8A/+0xC89/+0x1222/+0x1232/+0xFE7 — frame assembly from telemetry for BLE chip", "§53", "analyzed"),
    (0x0F694, "**voltage-table scanner/dispatcher (without push)**: r0=0..0xA (11 cases) by u16[RAM+0xF10 + i*2] (voltage table §52: 13*u16, reset 0x8bec); comparison with u16[RAM+0xF95+4]-0x320; pool: RAM+0xF10/+0xF95/+0x1264/+0x127E/+0x1271", "§53", "analyzed"),
    (0x09134, "**config-gated register-read dispatcher**: gates: byte[RAM+0x15F7+3] bit2 (§52 flag struct), byte[RAM+0xF95+0xC] bit4 etc.; bl **0x1bdc *5** (I2C2 register read §49); pool: RAM+0x15F7/+0xF95/+0x8C/+0xA42/+0xA3E/+0xFBB/+0xFC7 (threshold §52)/+0x107", "§53", "analyzed"),
    (0x1D078, "**timer capture/period handler + speed-limit ramp (code I, verified §69/§69.1 random-sweep 200/200)**: input u32[RAM+0x158]=V+byte[RAM+0x100]=F -> **0x1d874** (F==0->val=0, else val=s16(sdiv(48000,V))->u16[RAM+0x104]; divider 48000=0xbb80, 0x19994=r0/r1). Working struct r4=RAM+0x1768: [+0]=u16(val); **2 leaky integrators** — acc1=u32[+0xc]/out1=s16[+0x10] (new_acc=acc+val-out, out=s16(asr(acc,5))); acc2=u32[+4]/out2=s16[+8] (out=max(0,s16(asr(acc,3)))). **Percentage**: u16[RAM+0x236]=sdiv(out2*100,208) (§34.2). **Mode-target** (flag=byte[RAM+0x339], mode=byte[RAM+0x229]): flag==1->522; mode 0xb->125 / 2->u16[RAM+0x324] / 3->u16[RAM+0x326] / else->208; r4[+0x14]=target if s16(target)<=**u16[RAM+0x326]** else u16[RAM+0x326] (signed clamp, NOT min). **Ramp machine** structB@0x3c8 — **PI controller, 2 phases (mod-2 toggle S+0x28)** (§71/§72): Phase A holds output; Phase B: P-term S+0x2c=min(err,300) err=(target+-out2 depending on out1 vs target branch), S+0x5c=s16(2c)<<7; I-term S+0x58+=5*err snap[8000,8192], S+0x60=asr(58,2); output r4[+0x18]=S+0x64=P+-integral/4 clamp[1000,32760]; anti-windup by u32[0x1760]. Setpoint S+0x2a=target (verified 300/300); **entire Phase B verified 2000/2000** (I-term clamp[8000,131040], anti-windup reset u1760==0->S58=u224*4/S64=0/S2e=0 / slew, sxth out1/out2). Target -> km/h ~= *20.8. Tests @t(0x1D078) *2", "§53/§69/§71/§72", "analyzed"),
    (0x0E808, "**BLE session interpolation consumer**: args (r7, sl); gate u32[RAM+0x12BA+0x40]==0x1F4 (else reset -> 0 and return r1); u16[+0x4C]; bl: 0x1654c *many (u64 §50), 0x17094 *2, 0x16328, 0x16570 *2, 0x169f0, **0x167b6** (§51 interpolator), **0x161c6**; pool: RAM+0x12BA, 0x80000F3C (?), flash @0x1A49A", "§53", "analyzed"),
    (0x063B8, "**BLE session SM #6 (RAM+0x128B/0x12BA)**: 0x10fa4(1); byte@+0x6D gate; u32[+0x18]=0x16528(); bl: 0x16528 *2, 0x16558, 0x10e5c *3, 0x8d90 *3, 0x8e14 *2, **0xea64 *4** (§52 clamp handler), 0x8eb4, 0x8ecc, 0xe3ec *2, 0x8ee8, 0xe36c, 0x8f58, 0xe17c; pool: RAM+0x12BA/+0x128B, constants 0x186A0 (99999) / 0xFFFFEC78 (-8040)", "§53", "analyzed"),
    (0x0F994, "**flash-calibration flag dispatcher (without push)**: gates byte[RAM+0x80], byte[RAM+0xFBB+8]&1; u32[RAM+0xA00+4] vs [0]; flash table @0x19DE4 (adjacent to calibration §52 @0x19DAA); pool: RAM+0x80/+0xFBB/+0xA00..+0xA0C (u16 array)/+0xF95/+0x107", "§53", "analyzed"),
    (0x0D00C, "**telemetry frame builder + OTA logger step**: sub sp,#0x6c; loop: **0xab0c**(sp+0x3C) (fetch/retry §51/52) until ==1 (counter r7); 48B frame in sp+0x3C; bl 0x8a50 *6 (checksum §51), **0x8a90** (ADC §50.7), 0x11a4 *2, **0xaccc *2** (§52 OTA metadata logger!), 0xabf0, 0xad9c; pool: RAM+0x11C/+0xF64/+0x98 (ADC struct §52)/+0xF70/+0xF95/+0xFBB/+0xFC7", "§53", "analyzed"),
    (0x06618, "**BLE session SM #7 (RAM+0x12BA)**: 0x10fb0(0); |0x8f24()| *many (sensor, abs); threshold pool 0x7A120 = **500 000**; bl: 0x16564 *3 (u64 §50), 0x16222, 0x162ce *2, 0x1105c/0x11068 *2/0x11074 *2/0x11080 (session helpers), 0x16288 *3, 0x16534, 0x16540; pool: 0x7A120, RAM+0x12BA, 0xFFC91180 (-566784), 0x249F0 (149904)", "§53", "analyzed"),
    (0x1CE38, "**TIM1 CCR4 (motor) state handler**: byte[RAM+0x169A] = state (0/1/other -> dispatch); bl **0x21b52** (field writer §52); pool: RAM+0x26A/+0x169A/+0x218, **0x40012C40 (TIM1 CCR4, motor cluster §41)**, RAM+0x1768 (same struct as 0x1d078), RAM+0x31A/+0x3C8/+0x268/+0x26E/+0x216, constants -0x2710 (-10000), **0xBB8 (3000)**, **0x1770 (6000)**", "§53", "analyzed"),
    (0x14F50, "**periodic telemetry dispatcher (state byte[RAM+0x80] in {0,1,2})**: state 0: if byte[RAM+0xC90]&1 -> u16[RAM+0xC98]++; on bit7 and u32[RAM+0xFBB+4]>=0x64 and u16[+0xC98]>=0xA -> **0x8a90** (ADC §50.7) -> copy {u32,u16,byte} into RAM+0x98 + scatter into buffer **RAM+0x3024**, bl **0xd84c** (processing), fields from RAM+0xF95/+0xFBB/+0xFC7 -> RAM+0x3024+8..+0x1C; state 1: u16[RAM+0xC98]=0, [C90]|=0x80; if byte[RAM+0xC9A]&2 -> ++, on >=5: reset, [C90] &=~2|1|4, **bl 0xd938(1)** (§53 flag packer); window byte[RAM+0xFD3]&8 (<=0x1E): byte[RAM+0xC9B]++ (<=0xA) -> [C90] &=~8|1|4, **bl 0xd938(3)**; state 2: loop with RAM+0xF70/+0xC94; common tail: ~25 bits from ~12 structs -> u32 packed flags (pattern as in 0xd938); bl 0xd938 *4, 0x8a90, 0xd84c; caller: thunk @0x125E0 (schedule §54)", "§54", "analyzed"),
    (0x1337C, "**sensor sampler + flag bit-pack**: prologue: if byte[RAM+0xF70+3] -> u32[RAM+0xFC]++ (clamp 0x32=50, overflow flag); gate byte[RAM+0x31]==1 -> skip, else bl **0x8938** (ADC handler §52) -> r8; bl 0x8a44 -> r7; s16*10 -> bl **0x4d48**(v*10) -> r5; sb = r5/10 (when r5<0: -(r5/10)|0x8000); choice of signed byte sl from 3 sources by config bits (+6 offsets); fp=|sl|&0xFF; gate byte>>7 or clamp byte[+2]->0..0xC -> u8[sp+4]; **bit-pack section**: ~15 individual config bits -> u16[out+7] (pattern §52 0x1e94) + bl **0xa6a4** (helper) + more bits; pool: RAM+0xF70/+0xFC/+0x31/+0x15F7/+0xFC7/+0xDA/+0x98/+0xD8/+0x90/+0x104/+0xEF/+0xF95/+0x106E/+0xFD3/+0xFBB/**+0x80** (same telemetry state as 0x14f50)/+0x107/+0x1077, flash @0x19C42, RAM+0xF10 (voltage table §52), +0x109E/+0x44/+0xF9; caller: thunk @0x12454 (+0x5fd4)", "§54", "analyzed"),
    (0x11DE8, "**boot/startup state machine (5 states, byte[RAM+0x2E], TBB)**: state 0: bl **0x174fc**, bl **0x15c7c** -> fail? state=4 : OK; if byte[X]==1 -> bl **0x87c8** (GPIO check §52) -> u16[Y]++ (<=4); series of gates -> flags; u16[W]++ up to **0xBB8 (3000 ticks)** by gates; bl **0x139ac**, bl **0xd878** -> state=3; state 1: bl 0x4994, bl 0x8834; gates (byte==1/>=3); u32[pool+4]>=0xC8? skip : u16[X]++ up to **0x1F4 (500)** -> bl **0x5b98**, 0x139ac, 0xd878 -> state=3; state 2: section 0x1206C..0x12348; state 3: b 0x1216A; state 4: b 0x12348; threshold constants: 3000/500/**0x2EE0 (12000)**; caller: thunk @0x12472", "§54", "analyzed"),
    (0x07494, "**motor periodic task (ramp controller)**: read 3 \"sensors\" (each *3): **0x8f04** = constant 0x1068 (4200) -> [sp+0x10]; **0x8ecc** = u16[A+8] -> [sp+0xC]; **0x8ee8** = u16[A+6] -> r5; all clamp [0x3E8..0x1388] = [1000..5000]; r4=min, r7=max; u16[out+8]=r7-r4, u16[out+4]=1000-(r7-r4), u16[out+0xA]=r4-3200; **product sign** (smulbb): (r7-r4)*(r4-3200)<0 -> u32[pool]=-0x80000000 else +0x80000000 (Q31 +-1.0 sentinel), else u32 = prod/u16[out+4]; r6=clamp(+-0x8000) -> s16; u16[out+0xC]=r6+r4 (target); gates bit3/4/5/6/7: u16[+0x12]=r4, **0x8e50** = byte*10 -> u16[+6/+8/+0xA], **0x8f24** = u32[A+0]->[B+0x1B]; **ramp logic**: diff=s16[+6]-u16[+0xA]: >=0 -> bl **0xf010**(sl, r7, buf+6) else **0xf024** (ramp up/down step 8: min(max(cur,target+-8))); similarly pair +0xC/+0xE -> u16[+0x10]; gates bit0/1: 0x8e70 = byte*10 -> u16[+0xC/+0xE]; bl **0x16fde** *2 (2D-lookup, twin 0x16f42 §53) with {s16, u16, ptr, ptr+0xCE+0x12}; [sp+0x14] = result; caller: thunk @0x12438 (gate flag==0 or mode==1)", "§54", "analyzed"),
    (0x1C34C, "**fixed-point position/velocity controller (motor)**: byte[RAM+0x32A] ? u32[RAM+0x37C]=850 : 680 (0x55<<3); temp=s16[RAM+0x3C8+8]*240; v1=**0x19994**(temp, u32[RAM+0x3C8+0x4C]) (signed division §55) -> u32[RAM+0x3C8+0x50]; v2=**0x19994**(v1*65520, s16[RAM+0x1768+0x38]) -> u32[RAM+0x224] = clamp(v2, 0, **0x7FF8 (32760)**); middle: r6/r5 = u32 pair [pool+0/+4] (position), byte mode (0/1/other): division via **0x19968** (§55) with constants 0x64<<0xF, 0x2D<<4, thresholds **0x1E (30)**/**0x4B (75)**, constant **0x7D00 (32000)**; write u32[pool+0x80+0x18/+0x1C] (position/speed x2), u16 flags: OR/CLEAR bit2, byte[+5]=0/1; signed shift trick (lsl #0x17 + bpl = sign); pool: RAM+0x32A/+0x3C8/+0x1768/+0x224/+0x33A/+0x30E/+0x311/+0x1E0/+0x233/+0x27C/+0x21E/+0x220/+0x231/+0x27E/+0x245/+0x230/+0x380; **callers: not found in bl scan** (indirect call?)", "§54", "analyzed"),
    (0xF010, "**ramp-up with step 8**: args (cur=r0, target=r1, buf*=r2); if cur>=target: *buf=cur (if cur<=target+8) else *buf=target; if cur<target: *buf = (target>cur+8)? cur+8 : target — smooth ramp to target no faster than 8/tick", "§54", "analyzed"),
    (0xF024, "**ramp-down with step 8**: mirror of 0xf010: if cur<=target: *buf=cur else *buf=(cur>target+8)? target+8 : target — smooth reduction no faster than 8/tick", "§54", "analyzed"),
    (0x174FC, "**boot reset of counters** (in data hole §55): u32[RAM+8]=0, u32[RAM+0xC]=0 (boot counters §52), u32[RAM+0x10]=u32[RAM+0xF95] (config copy); caller: boot SM 0x11de8 state 0; prologue without push, epilogue bx lr", "§55", "analyzed"),
    (0x17524, "**boot-wait predicate** (in data hole §55): if byte[RAM+0xFD3]>0x1E (30) -> u32[RAM+8]=0, return 0; if u32[RAM+8] < **4320 (0x10E0)** -> return 0; u32[RAM+8]=4320 (clamp), return 1; caller: boot SM 0x11de8 state 1 (bl 0x17524; cmp r0,#1)", "§55", "analyzed"),
    (0x17554, "**mode-setter** (in data hole §55): if arg0 in {0,1} -> byte[pool]=arg0; else return; 2 callers (0x375e, 0x54cc)", "§55", "analyzed"),
    (0x19968, "**u32/u32 floor division** (in data hole §55): restoring algorithm, 32 iterations; **emulator-verified 305/305** (including 0xFFFFFFFF/2=0x7FFFFFFF); **correction §52/§53**: this is NOT Q20 — pure integer division, Q20 scaling performed by callers; prologue push {r4,r5} without lr + pop {r4,r5,pc} — pc read from lr placed by bl (\"lr-on-stack\" idiom)", "§55", "analyzed"),
    (0x19994, "**signed division (C-style, truncation toward zero)** (in data hole §55): signs r0/r1 -> neg+mark, bl 0x19968, restore signs; **emulator-verified**: -7/3=-2 (not floor!); wrapper over 0x19968", "§55", "analyzed"),
    (0x199BC, "**u64/u64 -> u64 unsigned division** (in data hole §55): args (num_lo=r0, num_hi=r1, den_lo=r2, **den_hi=r3** — all 4 required!); 64-iteration restoring loop via **0x1a0a0** (u64 LSR §50) and **0x1a080** (u64 LSL §50); result r1:r0; **emulator-verified**; continuation: mapped function 0x19a1c = signed u64 wrapper over it; **method note**: Run.call does not reset R4-R12 — tests must pass ALL function arguments (otherwise garbage from previous call)", "§55", "analyzed"),
    (0x1893C, "**DFU string command pool (data, hole §55)**: 7 commands (step 0x32=50B) @0x1893c rd_info / 0x1896e get_ver / 0x189a0 dfu_active / 0x189d2 nvm_write / 0x18a04 wr_info / 0x18a36 dfu_verify / 0x18bf8 ok (prefix \"down\", terminator \\x0d) + responses @0x18acc error / 0x18b62 'ok 0000000000' / 0x18b94 '0002' — **textual DFU/FOTA protocol** (USART3/BLE channel, §47/§50). Environment: u16 table [1,2,4..256] @0x18900, 7*u32 (hi=1,3,6,12,15,30,61~=command-ID) @0x18920, encrypted blob @0x1907b, NVM 0xFF @0x19575..0x197ff. **Dispatch statically unresolved**: pool base not from literal-pool and not movw/movt -> from RAM (runtime) — ceiling §65", "§55/§70", "ID"),
    (0x19810, "**model string (data, in hole §55)**: \"SZMC-ES-ZM-0283M\" + 0xFF-padding — controller identifier (Shenzhen Motor Controller ZM-0283); nearby version string \"A06120108\" @0x17570", "§55", "ID"),
]

# ----------------------------------------------------------------------
# parsing README tables
ROW = re.compile(r'^\|\s*\[`0x([0-9a-f]+)`\]\(func_0x[0-9a-f]+\.md\)\s*\|(.+)\|$')

def parse_readme(path, has_vaddr):
    """-> [(offset, size, region)]"""
    out = []
    for line in open(path, encoding='utf-8'):
        m = ROW.match(line.strip())
        if not m:
            continue
        off = int(m.group(1), 16)
        cells = [c.strip() for c in m.group(2).split('|')]
        # cells: [size, region, strings, callers]  or  [vaddr, size, region, strings, callers]
        if has_vaddr:
            size, region = int(cells[1]), cells[2]
        else:
            size, region = int(cells[0]), cells[1]
        out.append((off, size, region))
    return out

def esc(s):
    """escape pipes in markdown table cells (otherwise columns break)"""
    return s.replace('|', r'\|')

def write_csv(path, header, rows):
    """CSV version of the table — for machine verification (pipes don't break columns)."""
    import csv
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def attach_catalog(funcs, catalog):
    """funcs: [(off, size, region)] -> dict off -> (name|None, sections|None, status|None)"""
    att = {}
    for off, size, region in funcs:
        end = off + size
        hits = [(s, n, sec, st) for s, n, sec, st in catalog if off <= s < end]
        if hits:
            # multiple subblocks in one function — combine
            names = '; '.join(h[1] for h in hits)
            secs = ', '.join(dict.fromkeys(h[2] for h in hits))
            best = max(hits, key=lambda h: PCT[h[3]])
            att[off] = (names, secs, best[3])
        else:
            att[off] = (None, None, None)
    return att

def stats(funcs, att):
    n = len(funcs)
    total = sum(s for _, s, _ in funcs)
    by = {}
    for off, size, _ in funcs:
        st = att[off][2] or 'not started'
        c, b = by.get(st, (0, 0))
        by[st] = (c + 1, b + size)
    wsum = sum(s * PCT[att[off][2]] for off, s, _ in funcs if att[off][2])
    return n, total, by, (wsum / total if total else 0.0)

def write_mcu(path):
    funcs = parse_readme(os.path.join(RES, 'functions_mcu', 'README.md'), has_vaddr=False)
    att = attach_catalog(funcs, ANALYZED_MCU)
    n, total, by, pct = stats(funcs, att)

    L = []
    A = L.append
    A("# MCU_MAP — mcu_0007.bin decompilation map (by functions)")
    A("")
    A("Image: `research/images/mcu_0007.bin` (150,841 B), Cortex-M4F, **not encrypted**.")
    A(f"Functions confirmed by detection: **{n}**; code bytes in functions: **{total}** ({total/1024:.1f} KB of ~132.6 KB")
    A("code sections A–J; remainder is literal pools and data between functions).")
    A("")
    A("**Decompilation % model (per function):**")
    A("")
    A("| % | status | description |")
    A("|---|---|---|")
    A("| 100% | analyzed | logic fully decoded and described in REPORT.md |")
    A("| 50% | partial | role/input identified, part of logic decoded |")
    A("| 25% | ID | address and role known only from call context (xref) |")
    A("| 0% | not started | only auto-disassembly in `functions_mcu/func_0x*.md` |")
    A("")
    A("**Summary (weighted by code bytes):**")
    A("")
    A("| status | functions | bytes | % bytes |")
    A("|---|---|---|---|")
    for st in ('analyzed', 'partial', 'ID', 'not started'):
        if st in by:
            c, b = by[st]
            A(f"| {st} | {c} | {b} | {100.0*b/total:.1f}% |")
    A(f"| **total** | **{n}** | **{total}** | **{pct:.1f}% decompiled** |")
    A("")
    A("Details for each function: `functions_mcu/func_0x<off>.md` (disassembly,")
    A("literals, callees/callers). REPORT.md sections describe semantics.")
    A("")
    A("Re-generation: `python research/scripts/gen_maps.py` (function list from")
    A("`functions_mcu/README.md`; analyzed blocks catalog is in gen_maps.py, ANALYZED_MCU).")
    A("")
    A("| offset | size | region | name / role | sections | status | % |")
    A("|---|---|---|---|---|---|---|")
    for off, size, region in funcs:
        name, secs, st = att[off]
        if st:
            A(f"| [`0x{off:05x}`](functions_mcu/func_0x{off:05x}.md) | {size} | {region} | {esc(name)} | {esc(secs)} | {st} | {PCT[st]}% |")
        else:
            A(f"| [`0x{off:05x}`](functions_mcu/func_0x{off:05x}.md) | {size} | {region} | — | — | not started | 0% |")
    A("")
    A("**Known detection artifacts (manual review 2026-08-24):** row `0x1a5e6` —")
    A("body of a function actually starting at `0x1a5e4` (`mov r2,r1`, without push prologue — detector")
    A("catches internal push); this is 'own' trampoline 0x21c64->0x1a5e4->0x1a7ac. Everything else among")
    A("named functions was verified against disassembly entry points and REPORT.md sections.")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    # CSV counterpart (clean columns for checking/verification)
    csv_rows = []
    for off, size, region in funcs:
        name, secs, st = att[off]
        if st:
            csv_rows.append([f'0x{off:05x}', size, region, name, secs, st, f'{PCT[st]}%'])
        else:
            csv_rows.append([f'0x{off:05x}', size, region, '', '', 'not started', '0%'])
    write_csv(os.path.join(RES, 'MCU_MAP.csv'),
              ['offset', 'size', 'region', 'name_role', 'sections', 'status', 'pct'],
              csv_rows)
    print(f"MCU_MAP.md: functions {n}, bytes {total}, decompiled {pct:.1f}% (+ MCU_MAP.csv)")

# ----------------------------------------------------------------------
# BLE: region map (§43.3) + PLAIN region functions
BLE_TOTAL = 0x25922
BLE_REGIONS = [
    # (start, end, name, status, note)
    (0x0000, 0x0400, "RomPatch header (1 KB)", "analyzed", "full decode: ctrl_flag, select=1 (SCEK+RTKCONST), exe_base RAM 0x203800 — §43.3"),
    (0x0400, 0x3000, "PLAIN code #1: bootloader + DFU", "not started", "strings \"Wrong Ctrl Header.\", \"dfuPacketWaitTimer\"; functions below"),
    (0x3000, 0x5C00, "RomPatch \"load\" (ENCRYPTED, SCEK+RTKCONST)", "encrypted", "load_len=11776 -> RAM @0x203800; SWD dump of RAM yields plaintext without key"),
    (0x5C00, 0x9FF4, "PLAIN code #2: flash/OTA driver", "not started", "functions below"),
    (0x9FF4, 0xA400, "AppPatch header (~1 KB)", "analyzed", "select=0 (SCEK), xip=1/enc=0 (legacy flags) — §43.3"),
    (0xA400, 0x2542D, "AppPatch payload (ENCRYPTED, SCEK)", "encrypted", "~110 KB ciphertext; decryption only via XIP/SWD"),
    (0x2542D, BLE_TOTAL, "FOTA trailer: PEM + ECDSA-SHA256", "analyzed", "c1<-c0<-MijiaRoot chain verified — §42, §44"),
]

# §63: catalog of BLE PLAIN functions (bootloader + flash/OTA). Offsets = file offsets.
# Realtek RTL8762C peripherals (SDK): SPIC_FLASH=0x40080000, HW_AES=0x40014000, GPIO=0x40001000,
# TIM0=0x40002000, PERIPH=0x40000000. Emulator: emulator/ble_emu.py.
ANALYZED_BLE = [
    (0x2A50, "**trampoline-dispatch table**: chain of `movw/movt ip; bx ip` — indirect jumps to targets (incl. RAM functions 0x2xxxxxx); called as `bl 0x2a50+idx*6`", "§63", "analyzed"),
    (0x2A78, "**trampoline-dispatch table** (continuation of 0x2a50): `movw/movt ip; bx ip` to targets 0x9e9b/0x36edd/…", "§63", "analyzed"),
    (0x639A, "**SPIC flash register accessor**: returns register address SPIC+0x11c (0x4008011c); movw #0xfff — mask/command; 1 periph-write", "§63", "analyzed"),
    (0x63A4, "**SPIC config**: [base+8]=0 -> bl 0x639a -> [base+8]=1; then read-modify-write [r0+0x300] (SPIC register, bic #0xff | byte); r0=PERIPH base", "§63", "partial"),
    (0x645E, "**memory init/copy**: 22 RAM-writes, r0=RAM pointer (0x2007fbb8); reads u16[base+8]; buffer/struct initialization", "§63", "ID"),
    # §64: CTR/DFU protocol (BLE<->MCU via USART3) + flash driver
    (0x23F0, "**CTR length-gate**: r1=frame, r2=u16[r1+2]=length. Valid lengths: {5} U [0x12c..0x12e] (control 5B + data frames 300-302B); others -> return 0. Gate: valid length -> callee (0x2e24 for len==5, 0x2388/0x2e1a for data) — full validation = gate+payload", "§64", "partial"),
    (0x245A, "**DFU event dispatcher**: args (r1=event type, r3=substate). type==4&&[r3]==1 or type==2 -> timer: [base+0x1c0]*0x3e8(1000) -> bl 0x2df2; type==4&&[r3]==3 -> bl 0x2e2e. Controls dfuPacketWaitTimer", "§64", "partial"),
    (0x23D6, "**pattern-search helper**: searches 6-byte pattern in buffer (bl 0x2bae); result -> state [base+0x1c9]=1/2; used by CTR validator", "§64", "ID"),
    (0x6110, "**SPIC base getter/init**: returns SPIC base (0x40080000), touches ctrlr0", "§64", "ID"),
    (0x6570, "**SPIC ctrl setup**: configures ctrlr0 (126B)", "§64", "ID"),
    (0x6A12, "**SPIC op -> RAM buffer**: ctrlr0, r0=RAM pointer (0x2007fbe0); flash operation with buffer (170B)", "§64", "ID"),
    (0x7A08, "**SPIC ctrl op**: ctrlr0, r0=0xffc00000 (110B)", "§64", "ID"),
    # §65: PLAIN code taxonomy — family of global config-struct setters
    (0x6008, "**setter config-struct**: stores arg into 3 fields [base+0/+4/+8] + callback (blx). Family 0x6008..0x60e4 (6*44B) — setters for different field groups; r0=arg", "§65", "partial"),
    (0x9F80, "**init global struct**: returns 4, zeroes fixed struct @RAM 0x2007fbe8 (leaf, ignores args)", "§65", "ID"),
]

def write_ble(path):
    funcs = parse_readme(os.path.join(RES, 'functions_ble', 'README.md'), has_vaddr=True)
    att = attach_catalog(funcs, ANALYZED_BLE)
    n, total, by, pct = stats(funcs, att)

    L = []
    A = L.append
    A("# BLE_MAP — ble_2.7.0_0015.bin decompilation map (by functions)")
    A("")
    A(f"Image: `research/images/ble_2.7.0_0015.bin` ({BLE_TOTAL} B = 153,890 B), Realtek RTL8762C")
    A("(Cortex-M33), flash base `0x01800000`. File = byte-for-byte Mi Home FOTA package (§42).")
    A("")
    A("## 1. Region map (by entropy + header fields, §43.3)")
    A("")
    A("| region | size | status | note |")
    A("|---|---|---|---|")
    for s, e, name, st, note in BLE_REGIONS:
        A(f"| `{s:#06x}..{e:#06x}` | {e-s} B ({100.0*(e-s)/BLE_TOTAL:.1f}%) | {st} | {esc(note)} |")
    enc = sum(e - s for s, e, _, st, _ in BLE_REGIONS if st == 'encrypted')
    plain_code = sum(e - s for s, e, _, st, _ in BLE_REGIONS if st == 'not started')
    done = sum(e - s for s, e, _, st, _ in BLE_REGIONS if st == 'analyzed')
    A("")
    A(f"**Key fact:** {enc} B ({100.0*enc/BLE_TOTAL:.1f}%) — **encrypted (per-chip SCEK from eFuse)**;")
    A("decompilation without SWD/XIP is structurally limited to ~"
      f"{100.0*(BLE_TOTAL-enc)/BLE_TOTAL:.0f}% of the file. BLE app protocol is reversed from APK/plugins,")
    A("not from this image (§35).")
    A("")
    A("## 2. PLAIN region functions (gen_functions.py detection)")
    A("")
    A(f"Confirmed: **{n}** functions, total {total} B code. This is low-level bootloader +")
    A("flash/OTA driver; meaningful app code is in the encrypted APP region (§62). Semantic")
    A(f"analysis of PLAIN code: **{pct:.1f}%** (weighted by bytes; catalog ANALYZED_BLE, §63).")
    A("")
    A("**Decompilation % model:** analyzed=100%, partial=50%, ID=25%, not started=0%.")
    A("")
    A("Re-generation: `python research/scripts/gen_maps.py` (function list from")
    A("`functions_ble/README.md`; catalog is ANALYZED_BLE in gen_maps.py). Emulator: `emulator/ble_emu.py`.")
    A("")
    A("| offset | vaddr | size | region | name / role | sections | status | % |")
    A("|---|---|---|---|---|---|---|---|")
    for off, size, region in funcs:
        name, secs, st = att[off]
        if st:
            A(f"| [`0x{off:05x}`](functions_ble/func_0x{off:05x}.md) | `0x{0x01800000+off:08x}` | {size} | {esc(region)} | {esc(name)} | {esc(secs)} | {st} | {PCT[st]}% |")
        else:
            A(f"| [`0x{off:05x}`](functions_ble/func_0x{off:05x}.md) | `0x{0x01800000+off:08x}` | {size} | {esc(region)} | — | — | not started | 0% |")
    A("")
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    csv_rows = []
    for off, size, region in funcs:
        name, secs, st = att[off]
        if st:
            csv_rows.append([f'0x{off:05x}', f'0x{0x01800000+off:08x}', size, region, name, secs, st, f'{PCT[st]}%'])
        else:
            csv_rows.append([f'0x{off:05x}', f'0x{0x01800000+off:08x}', size, region, '', '', 'not started', '0%'])
    write_csv(os.path.join(RES, 'BLE_MAP.csv'),
              ['offset', 'vaddr', 'size', 'region', 'name_role', 'sections', 'status', 'pct'],
              csv_rows)
    print(f"BLE_MAP.md: functions {n}, code bytes {total}; PLAIN-analyzed {pct:.1f}%; encrypted {enc} B ({100.0*enc/BLE_TOTAL:.1f}%) (+ BLE_MAP.csv)")

if __name__ == '__main__':
    write_mcu(os.path.join(RES, 'MCU_MAP.md'))
    write_ble(os.path.join(RES, 'BLE_MAP.md'))
