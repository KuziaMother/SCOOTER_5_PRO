# func_0x05dbc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005dbc) | `0x00005dbc` |
| размер кода | 22 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40003000 — периферия (r1)

## Вызовы (callees)

- `func_0x02d5c` (0x00002d5c, bl)
- `func_0x0c20c` (0x0000c20c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11de8` (bl @0x000120e4)
- `func_0x11de8` (bl @0x0001214a)
- `func_0x11de8` (bl @0x000122e8)


## Дизассембляция

```asm
  05dbc:  push {r4, lr}                     
  05dbe:  movw r0, #0xaaaa                  
  05dc2:  ldr r1, [pc, #0x10]               -> периферия
  05dc4:  str r0, [r1]                      
  05dc6:  bl #0x2d5c                        -> func_0x02d5c
  05dca:  movs r0, #4                       
  05dcc:  bl #0xc20c                        -> func_0x0c20c
  05dd0:  pop {r4, pc}                      
  ; --- literal-пул @0x05dd4 (1 слов) — ВНЕ границ функции ---
  05dd4:  .word 0x40003000  ; периферия
```
