# func_0x0d298

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d298) | `0x0000d298` |
| размер кода | 46 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000304c — RAM (r0)

## Вызовы (callees)

- `func_0x0cfb8` (0x0000cfb8, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0395c` (bl @0x00003960)
- `func_0x03966` (bl @0x0000396a)


## Дизассембляция

```asm
  0d298:  push {r3, r4, r5, lr}             
  0d29a:  mov r4, r0                        
  0d29c:  movs r5, #0                       
  0d29e:  cbnz r4, #0xd2bc                  
  0d2a0:  bl #0xcfb8                        -> func_0x0cfb8
  0d2a4:  cbnz r0, #0xd2bc                  
  0d2a6:  mov.w r0, #0x1f4                  
  0d2aa:  str r0, [sp]                      
  0d2ac:  nop                               
  0d2ae:  ldr r0, [sp]                      
  0d2b0:  subs r1, r0, #1                   
  0d2b2:  str r1, [sp]                      
  0d2b4:  cmp r0, #0                        
  0d2b6:  bne #0xd2ae                       
  0d2b8:  bl #0xcfb8                        -> func_0x0cfb8
  0d2bc:  ldr r0, [pc, #0x70]               -> RAM
  0d2be:  ldr r0, [r0]                      
  0d2c0:  cbnz r0, #0xd2c6                  
  0d2c2:  movs r0, #0                       
  0d2c4:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x0d330 (1 слов) — ВНЕ границ функции ---
  0d330:  .word 0x2000304c  ; RAM
```
