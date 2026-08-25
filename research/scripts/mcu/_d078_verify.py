import sys, struct
sys.path.insert(0,'..'); sys.path.insert(0,'../../..')
from unicorn import UcError, UC_HOOK_CODE
from unicorn.arm_const import *
from emulator.mcu_emu import McuEmu, FLASH0, FLASH1, RAM, STACK_TOP
FW_LEN=len(open(r'D:\SCOOTER_5_PRO\research\images\mcu_0007.bin','rb').read())

def run_setup(V,F,acc1,out1,acc2,out2,mode,maxc,m2t,m3t):
    emu=McuEmu(max_insn=300000); uc=emu.uc
    uc.mem_write(RAM,b'\x00'*0x20000)
    def w16(o,v): uc.mem_write(RAM+o,struct.pack('<H',v&0xffff))
    def w32(o,v): uc.mem_write(RAM+o,struct.pack('<I',v&0xffffffff))
    def wb (o,v): uc.mem_write(RAM+o,bytes([v&0xff]))
    w32(0x158,V); wb(0x100,F)
    # r4 = RAM+0x1768
    w16(0x1768+0,0); w32(0x1768+4,acc2); w16(0x1768+8,out2&0xffff)
    w32(0x1768+0xc,acc1); w16(0x1768+0x10,out1&0xffff)
    wb(0x229,mode); w16(0x339,maxc); w16(0x324,m2t); w16(0x326,m3t)
    uc.reg_write(UC_ARM_REG_SP,STACK_TOP); uc.reg_write(UC_ARM_REG_LR,0x0BADF001)
    def stop(uc_,addr,size,user):
        if not(FLASH0<=addr<FLASH0+FW_LEN or FLASH1<=addr<FLASH1+FW_LEN): uc_.emu_stop()
    hs=uc.hook_add(UC_HOOK_CODE,stop)
    err=None
    try: uc.emu_start(0x1d078|1,0,count=300000)
    except UcError as e: err=str(e)[:60]
    uc.hook_del(hs)
    def r16(o): return struct.unpack('<H',bytes(uc.mem_read(RAM+o,2)))[0]
    def r32(o): return struct.unpack('<I',bytes(uc.mem_read(RAM+o,4)))[0]
    return emu,err,r16,r32

def sdiv(a,b):
    q=abs(a)//abs(b) if b else 0
    return q if (a<0)==(b<0) else -q
def s16(x): x&=0xffff; return x-0x10000 if x>=0x8000 else x

# Test A: F=1, V=60032 → val=2; acc1=100,out1=10; acc2=200,out2=20; mode=3,maxc=500,m3t=300
emu,err,r16,r32=run_setup(60032,1,100,10,200,20,3,500,999,300)
val=sdiv(60032,30016); print(f"A: insns={emu.insn} err={err}")
print(f"  val={val}")
na1=100+val-10; o1=s16((na1>>5)&0xffffffff if na1>=0 else -((-na1)>>5))
# asr for negative: python >> is arithmetic already
o1=na1>>5; o1=s16(o1)
na2=200+val-20; o2=na2>>3; o2=s16(o2); 
print(f"  exp out1(r4+0x10)={o1} got={r16(0x1768+0x10)}")
print(f"  exp out2(r4+8)   ={o2 if o2>=0 else 0} got={r16(0x1768+8)}")
pct_in=(o2 if o2>=0 else 0); pct=sdiv(pct_in*100,208)
print(f"  exp pct(u16@0x236)={pct} got={r16(0x236)}")
tgt=min(300,500)
print(f"  exp target(r4+0x14)={tgt} got={r16(0x1768+0x14)}")

# Test B: mode=0xb → target=0x7d(125); maxc=100 → clamp to 100
emu,err,r16,r32=run_setup(30016,1,0,0,0,0,0xb,100,999,999)
print(f"\nB: insns={emu.insn} err={err}")
val=sdiv(30016,30016)
na2=0+val-0; o2=s16(na2>>3); 
print(f"  val={val} out2={o2 if o2>=0 else 0} pct={sdiv((o2 if o2>=0 else 0)*100,208)} got_pct={r16(0x236)}")
print(f"  exp target=min(125,100)=100 got={r16(0x1768+0x14)}")

# Test C: mode=2 → target=u16[RAM+0x324]=777; maxc=900
emu,err,r16,r32=run_setup(30016,1,0,0,0,0,2,900,777,999)
print(f"\nC: insns={emu.insn} err={err}")
print(f"  exp target=min(777,900)=777 got={r16(0x1768+0x14)}")

# Test D: default mode (5) → target=0xd0(208); maxc=150 → clamp 150
emu,err,r16,r32=run_setup(30016,1,0,0,0,0,5,150,999,999)
print(f"\nD: insns={emu.insn} err={err}")
print(f"  exp target=min(208,150)=150 got={r16(0x1768+0x14)}")
