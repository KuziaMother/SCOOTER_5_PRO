# func_0x082b8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800082b8) | `0x000082b8` |
| размер кода | 44 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00a14014 — прочее (r0)
- 0x00c84014 — прочее (r0)
- 0x20000c8d — RAM (r1)

## Вызовы (callees)

- `func_0x083e4` (0x000083e4, bl)
- `func_0x08468` (0x00008468, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001dfe)


## Дизассембляция

```asm
  082b8:  push {r4, lr}                     
  082ba:  movs r0, #0                       
  082bc:  ldr r1, [pc, #0x24]               -> RAM
  082be:  strb r0, [r1]                     
  082c0:  bl #0x8468                        -> func_0x08468
  082c4:  bl #0x83e4                        -> func_0x083e4
  082c8:  mov r4, r0                        
  082ca:  ldr r0, [pc, #0x1c]               
  082cc:  cmp r4, r0                        
  082ce:  beq #0x82e2                       
  082d0:  subs r0, r0, #1                   
  082d2:  cmp r4, r0                        
  082d4:  beq #0x82e2                       
  082d6:  ldr r0, [pc, #0x14]               
  082d8:  cmp r4, r0                        
  082da:  beq #0x82e2                       
  082dc:  movs r0, #1                       
  082de:  ldr r1, [pc, #4]                  -> RAM
  082e0:  strb r0, [r1]                     
  082e2:  pop {r4, pc}                      
  ; --- literal-пул @0x082e4 (3 слов) — ВНЕ границ функции ---
  082e4:  .word 0x20000c8d  ; RAM
  082e8:  .word 0x00c84014
  082ec:  .word 0x00a14014
```
