import sys, struct, random
sys.path.insert(0,'..'); sys.path.insert(0,'../../..')
from unicorn import UcError, UC_HOOK_CODE
from unicorn.arm_const import *
from emulator.mcu_emu import McuEmu, FLASH0, FLASH1, RAM, STACK_TOP
FW_LEN=len(open(r'D:\SCOOTER_5_PRO\research\images\mcu_0007.bin','rb').read())
def sdiv(a,b):
    if b==0: return 0
    q=abs(a)//abs(b); return q if (a<0)==(b<0) else -q
def s16(x): x&=0xffff; return x-0x10000 if x>=0x8000 else x
def run(V,F,acc1,out1,acc2,out2,mode,maxc,m2t,m3t):
    emu=McuEmu(max_insn=400000); uc=emu.uc
    uc.mem_write(RAM,b'\x00'*0x20000)
    def w16(o,v): uc.mem_write(RAM+o,struct.pack('<H',v&0xffff))
    def w32(o,v): uc.mem_write(RAM+o,struct.pack('<I',v&0xffffffff))
    def wb (o,v): uc.mem_write(RAM+o,bytes([v&0xff]))
    w32(0x158,V); wb(0x100,F)
    w16(0x1768+0,0); w32(0x1768+4,acc2); w16(0x1768+8,out2&0xffff)
    w32(0x1768+0xc,acc1); w16(0x1768+0x10,out1&0xffff)
    wb(0x229,mode); w16(0x339,maxc); w16(0x324,m2t); w16(0x326,m3t)
    uc.reg_write(UC_ARM_REG_SP,STACK_TOP); uc.reg_write(UC_ARM_REG_LR,0x0BADF001)
    def stop(uc_,a,s,u):
        if not(FLASH0<=a<FLASH0+FW_LEN or FLASH1<=a<FLASH1+FW_LEN): uc_.emu_stop()
    hs=uc.hook_add(UC_HOOK_CODE,stop)
    try: uc.emu_start(0x1d078|1,0,count=400000)
    except UcError: pass
    uc.hook_del(hs)
    r=lambda o: struct.unpack('<H',bytes(uc.mem_read(RAM+o,2)))[0]
    return r(0x1768),r(0x1778),r(0x1770),r(0x236),r(0x177c)  # sp0,out1,out2,pct,tgt
rng=random.Random(777)
ok=sp0o=o1o=o2o=pcto=tgo=0; N=200; fails=[]
for i in range(N):
    V=rng.randint(50,60000); F=rng.getrandbits(1)
    acc1=rng.getrandbits(32); out1=rng.randint(-32768,32767)
    acc2=rng.getrandbits(32); out2=rng.randint(-32768,32767)
    mode=rng.choice([2,3,0xb,5,7]); maxc=rng.getrandbits(16)
    m2t=rng.getrandbits(16); m3t=rng.getrandbits(16)
    # MODEL (corrected)
    val = 0 if F==0 else s16(sdiv(48000,V))
    na1=(acc1+val-out1)&0xffffffff; e_sp0=val&0xffff; e_o1=s16(na1>>5)
    na2=(acc2+val-out2)&0xffffffff; e_o2=s16(na2>>3); e_o2=max(0,e_o2)
    e_pct=(sdiv(100*e_o2,208))&0xffff
    flagb=maxc&0xff
    if flagb==1: tgt=522
    elif mode==0xb: tgt=125
    elif mode==2: tgt=m2t
    elif mode==3: tgt=m3t
    else: tgt=208
    e_tgt = tgt if s16(tgt) <= m3t else m3t   # signed clamp vs u16[RAM+0x326]
    g_sp0,g_o1,g_o2,g_pct,g_tgt=run(V,F,acc1,out1,acc2,out2,mode,maxc,m2t,m3t)
    a=(g_sp0==e_sp0); b=(g_o1==e_o1&0xffff); c=(g_o2==e_o2&0xffff); d=(g_pct==e_pct); e=(g_tgt==e_tgt)
    sp0o+=a; o1o+=b; o2o+=c; pcto+=d; tgo+=e; ok+=(a and b and c and d and e)
    if not(a and b and c and d and e): fails.append((V,F,acc1,out1,acc2,out2,mode,maxc,m2t,m3t,(g_sp0,e_sp0,g_o1,e_o1,g_o2,e_o2,g_pct,e_pct,g_tgt,e_tgt)))
print(f"N={N}: sp0 {sp0o}/{N} out1 {o1o}/{N} out2 {o2o}/{N} pct {pcto}/{N} tgt {tgo}/{N} | ALL {ok}/{N}")
for f in fails[:4]: print("  FAIL:",f)
