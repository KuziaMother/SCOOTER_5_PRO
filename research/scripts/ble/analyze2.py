#!/usr/bin/env python3
"""Анализ RTL8762C fw, часть 2: строки по категориям, Thumb-функции, cert, заголовок."""
import os, sys, re, struct, base64, collections, math
try:
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN
    HAVE_CS = True
except Exception:
    HAVE_CS = False

IMG = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ble_2.7.0_0015.bin")
FW = sys.argv[1] if len(sys.argv) > 1 else IMG
d = open(FW, "rb").read()

# ---------- заголовок (эвристика) ----------
print("=== заголовок (интерпретация полей LE) ===")
u16 = lambda o: struct.unpack_from("<H", d, o)[0]
u32 = lambda o: struct.unpack_from("<I", d, o)[0]
print(f"  [0x00] u16=0x{u16(0):04x}  [0x02] u16=0x{u16(2):04x}  [0x04] u32=0x{u32(4):08x} ({u32(4)})")
print(f"  [0x08] u32=0x{u32(8):08x} ({u32(8)})  [0x0c..0x1b] = {d[12:28].hex()}")
print(f"  [0x1c] u32=0x{u32(0x1c):08x}  [0x20] u32=0x{u32(0x20):08x}  [0x24] u32=0x{u32(0x24):08x}")
print(f"  [0x28] u32=0x{u32(0x28):08x}")

# ---------- энтропия -> секции ----------
def ent(b):
    if not b: return 0
    c = collections.Counter(b); n = len(b)
    return -sum((x/n)*math.log2(x/n) for x in c.values())
BLK = 512
sect = []  # (start, end, kind)
cur = None
for i in range(0, len(d), BLK):
    e = ent(d[i:i+BLK])
    k = "ENC" if e > 7.4 else ("CODE" if e > 5.2 else "DATA")
    if cur and cur[2] == k:
        cur[1] = min(i+BLK, len(d))
    else:
        if cur: sect.append(cur)
        cur = [i, min(i+BLK, len(d)), k]
if cur: sect.append(cur)
print("\n=== секции по энтропии ===")
plain = []
for s in sect:
    sz = s[1]-s[0]
    print(f"  0x{s[0]:05x}-0x{s[1]:05x}  {s[2]:4}  {sz} байт")
    if s[2] == "CODE" and sz >= 256:
        plain.append((s[0], s[1]))

# ---------- все строки -> файл + категории ----------
strs = [(m.start(), m.group().decode('ascii','ignore'))
        for m in re.finditer(rb'[ -~]{4,}', d)]
with open("strings.txt", "w", encoding="utf-8") as f:
    for o, s in strs:
        f.write(f"{o:06x}  {s}\n")
print(f"\n=== строки: {len(strs)} шт -> strings.txt ===")

CATS = {
    "OTA/DFU/boot": ['dfu','ota','boot','image','flash','eras','unlock bp','bank','upgrade','reset'],
    "батарея/BMS": ['batt','bms','charg','volt','current','cell','soc','temp'],
    "мотор/езда": ['motor','speed','throttle','brake','cruise','km','rpm','wheel','drive','gear','limit'],
    "свет/дисплей": ['light','lamp','led','display','screen','beep','buzz'],
    "замок/защита": ['lock','pin','password','auth','secure','key','verify','sign','cert'],
    "BLE/связь": ['ble','gatt','att','adv','notif','uart','mesh','conn','mtu','miot','spec'],
    "ошибки/лог": ['error','fail','assert','warn','fault','timeout','invalid','overflow'],
    "система": ['version','release','build','init','task','stack','heap','watchdog','sleep','clock'],
}
cat_hits = {c: [] for c in CATS}
for o, s in strs:
    sl = s.lower()
    for c, kws in CATS.items():
        if any(k in sl for k in kws):
            cat_hits[c].append((o, s)); break
for c, hs in cat_hits.items():
    print(f"\n--- {c}: {len(hs)} ---")
    for o, s in hs[:14]:
        print(f"   0x{o:05x}: {s[:74]}")

# ---------- Thumb-функции в открытых секциях ----------
print("\n=== поиск Thumb-функций (push {..,lr}) в открытых секциях ===")
# prologi: PUSH {..,LR} = B5xx (16-bit). Считаем как границы функций.
prologue = re.compile(rb'[\x00-\xff]\xb5')  # ..B5 -> push {...,lr}
for (a, b) in plain:
    region = d[a:b]
    starts = set()
    for m in re.finditer(rb'.\xb5', region):
        off = m.start()
        if off % 2 == 0:  # 16-bit align
            starts.add(a+off)
    print(f"  секция 0x{a:05x}-0x{b:05x}: ~{len(starts)} прологов (push lr)")

if HAVE_CS and plain:
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_LITTLE_ENDIAN)
    a, b = plain[0]
    print(f"\n=== дизасм первых инструкций открытой секции 0x{a:05x} (Thumb) ===")
    n = 0
    for ins in md.disasm(d[a:a+64], a):
        print(f"   0x{ins.address:05x}: {ins.mnemonic:8} {ins.op_str}")
        n += 1
        if n >= 20: break

# ---------- сертификат из хвоста ----------
print("\n=== сертификат в трейлере ===")
m = re.search(rb'MII[0-9A-Za-z+/=\r\n]{200,}', d)
if m:
    b64 = re.sub(rb'[^0-9A-Za-z+/=]', b'', m.group())
    try:
        der = base64.b64decode(b64 + b'=' * (-len(b64) % 4))
        print(f"  base64 @0x{m.start():05x}, DER {len(der)} байт")
        # вытащим печатаемые куски (Organization/CN и т.п.)
        for t in re.finditer(rb'[ -~]{3,}', der):
            s = t.group().decode('ascii','ignore')
            if any(k in s for k in ['Mi','Xiao','scooter','dreame','CN','.com','Root','CA','ECDSA','P-256']):
                print(f"    cert-str: {s}")
    except Exception as e:
        print("  decode err", e)
