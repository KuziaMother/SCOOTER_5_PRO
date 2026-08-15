# func_0x061e4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800061e4) | `0x000061e4` |
| размер кода | 72 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40021000 — периферия (r2)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x07ed4` (bl @0x00007ed6)


## Дизассембляция

```asm
  061e4:  push {r3, lr}                     
  061e6:  movs r1, #0                       
  061e8:  movs r2, #0                       
  061ea:  str r2, [sp]                      
  061ec:  movs r0, #0                       
  061ee:  ldr r2, [pc, #0x3c]               -> периферия
  061f0:  ldr r2, [r2]                      
  061f2:  and r2, r2, #2                    
  061f6:  cbnz r2, #0x622a                  
  061f8:  ldr r2, [pc, #0x30]               -> периферия
  061fa:  ldr r2, [r2]                      
  061fc:  orr r2, r2, #1                    
  06200:  ldr r3, [pc, #0x28]               -> периферия
  06202:  str r2, [r3]                      
  06204:  nop                               
  06206:  ldr r2, [pc, #0x24]               -> периферия
  06208:  ldr r2, [r2]                      
  0620a:  ubfx r1, r2, #1, #1               
  0620e:  ldr r2, [sp]                      
  06210:  adds r2, r2, #1                   
  06212:  str r2, [sp]                      
  06214:  cbnz r1, #0x621e                  
  06216:  ldr r2, [sp]                      
  06218:  cmp.w r2, #0x500                  
  0621c:  bne #0x6206                       
  0621e:  ldr r2, [pc, #0xc]                -> периферия
  06220:  ldr r2, [r2]                      
  06222:  ubfx r1, r2, #1, #1               
  06226:  cbnz r1, #0x622a                  
  06228:  movs r0, #1                       
  0622a:  pop {r3, pc}                      
  ; --- literal-пул @0x0622c (1 слов) — ВНЕ границ функции ---
  0622c:  .word 0x40021000  ; периферия
```
