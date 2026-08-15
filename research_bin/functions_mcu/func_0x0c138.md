# func_0x0c138

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c138) | `0x0000c138` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a7c — RAM (r0)

## Вызовы (callees)

- `func_0x01d78` (0x00001d78, bl)
- 0x0c14c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01cf6` (bl @0x00001d24)


## Дизассембляция

```asm
  0c138:  push {r4, lr}                     
  0c13a:  bl #0x1d78                        -> func_0x01d78
  0c13e:  ldr r0, [pc, #0x14]               -> RAM
  0c140:  ldrh r0, [r0]                     
  0c142:  movw r1, #0xeb04                  
  0c146:  cmp r0, r1                        
  0c148:  bne #0xc14e                       
  0c14a:  movs r0, #1                       
  0c14c:  pop {r4, pc}                      
  0c14e:  movs r0, #0                       
  0c150:  b #0xc14c                         -> 0x0c14c (вне списка функций)
  ; --- literal-пул @0x0c154 (1 слов) — ВНЕ границ функции ---
  0c154:  .word 0x20000a7c  ; RAM
```
