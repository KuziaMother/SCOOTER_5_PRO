import sys, struct, random
sys.path.insert(0,'..'); sys.path.insert(0,'../../..')
from unicorn import UcError, UC_HOOK_CODE
from unicorn.arm_const import *
from emulator.mcu_emu import McuEmu, FLASH0, FLASH1, RAM, STACK_TOP
FW_LEN=len(open(r'D:\SCOOTER_5_PRO\research\images\mcu_0007.bin','rb').read())
def run(A,B,refA,refB):
    emu=McuEmu(max_insn=20000); uc=emu.uc
    uc.mem_write(RAM,b'\x00'*0x20000)
    uc.mem_write(RAM+0x13AB,struct.pack('<H',A&0xffff))
    uc.mem_write(RAM+0x13A4,struct.pack('<h',B))
    uc.mem_write(RAM+0x130A,struct.pack('<H',refA&0xffff))
    uc.mem_write(RAM+0x1302,struct.pack('<h',refB))
    uc.mem_write(RAM+0x500,b'\x7f')
    uc.reg_write(UC_ARM_REG_R0,RAM+0x500)
    uc.reg_write(UC_ARM_REG_SP,STACK_TOP); uc.reg_write(UC_ARM_REG_LR,0x0BADF001)
    def stop(uc_,addr,size,user):
        if not(FLASH0<=addr<FLASH0+FW_LEN or FLASH1<=addr<FLASH1+FW_LEN): uc_.emu_stop()
    hs=uc.hook_add(UC_HOOK_CODE,stop)
    try: uc.emu_start(0xe740|1,0,count=20000)
    except UcError: pass
    uc.hook_del(hs)
    return uc.mem_read(RAM+0x500,1)[0]
def model(A,B,refA,refB,use_abs):
    devA=abs((A&0xffff)-(refA&0xffff))
    devB=(B-refB) if not use_abs else abs(B-refB)
    devB=min(devB,0x7fff); devB=max(devB,-0x8000)
    return 1 if (devA>=500 or devB>500) else 0
# failing case + random sweep
cases=[(48823,1670,48956,23387)]
rng=random.Random(42)
for _ in range(200):
    cases.append((rng.getrandbits(16),rng.randint(-32768,32767),rng.getrandbits(16),rng.randint(-32768,32767)))
ok_abs=ok_sgn=0
for A,B,ra,rb in cases:
    got=run(A,B,ra,rb)
    if got==model(A,B,ra,rb,True): ok_abs+=1
    if got==model(A,B,ra,rb,False): ok_sgn+=1
print(f"Случаев: {len(cases)}")
print(f"Модель devB=ABS : совпадений {ok_abs}/{len(cases)}")
print(f"Модель devB=SGN : совпадений {ok_sgn}/{len(cases)}")
