# func_0x050b0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800050b0) | `0x000050b0` |
| размер кода | 128 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000044 — RAM (sb)

## Вызовы (callees)

- 0x05112 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x128c8` (bl @0x000128d0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x050e4..0x050fc` (24 Б); цели из: 0x050d2
- `0x050fc..0x05112` (22 Б); цели из: 0x050ea
- `0x05112..0x05130` (30 Б); цели из: 0x050ca

## Дизассембляция

```asm
  050b0:  push.w {r4, r5, r6, r7, r8, sb, lr}
  050b4:  mov r3, r0                        
  050b6:  movs r7, #0                       
  050b8:  ldrsb.w r4, [r3]                  
  050bc:  ldrsb.w r5, [r3]                  
  050c0:  mov.w ip, #1                      
  050c4:  mov.w r8, #1                      
  050c8:  movs r0, #0                       
  050ca:  b #0x5112                         -> 0x05112 (вне списка функций)
  050cc:  ldrsb.w sb, [r3, r0]              
  050d0:  cmp sb, r4                        
  050d2:  ble #0x50e4                       
  050d4:  ldr.w sb, [pc, #0x58]             -> RAM
  050d8:  ldrsb.w r4, [sb, r0]              
  050dc:  add.w sb, r0, #1                  
  050e0:  and ip, sb, #0xff                 
  050e4:  ldrsb.w sb, [r3, r0]              
  050e8:  cmp sb, r5                        
  050ea:  bge #0x50fc                       
  050ec:  ldr.w sb, [pc, #0x40]             -> RAM
  050f0:  ldrsb.w r5, [sb, r0]              
  050f4:  add.w sb, r0, #1                  
  050f8:  and r8, sb, #0xff                 
  050fc:  ldr.w sb, [pc, #0x30]             -> RAM
  05100:  ldrsb.w sb, [sb, r0]              
  05104:  add sb, r7                        
  05106:  sxth.w r7, sb                     
  0510a:  add.w sb, r0, #1                  
  0510e:  and r0, sb, #0xff                 
  05112:  cmp r0, r1                        
  05114:  blt #0x50cc                       
  05116:  sdiv sb, r7, r1                   
  0511a:  sxtb.w r6, sb                     
  0511e:  strb r6, [r2]                     
  05120:  strb r5, [r2, #1]                 
  05122:  strb r4, [r2, #2]                 
  05124:  strb.w r8, [r2, #3]               
  05128:  strb.w ip, [r2, #4]               
  0512c:  pop.w {r4, r5, r6, r7, r8, sb, pc}
  ; --- literal-пул @0x05130 (1 слов) — ВНЕ границ функции ---
  05130:  .word 0x20000044  ; RAM
```
