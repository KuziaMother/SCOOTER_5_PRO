# func_0x0c6c4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c6c4) | `0x0000c6c4` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40021000 — периферия (r2)

## Вызовы (callees)

- 0x0c6dc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x106d8` (bl @0x000106e6)
- `func_0x106d8` (bl @0x000106ee)
- `func_0x106d8` (bl @0x000106fe)
- `func_0x106d8` (bl @0x00010708)
- `func_0x1302c` (bl @0x0001303a)
- `func_0x1302c` (bl @0x00013044)
- `func_0x1302c` (bl @0x00013088)
- `func_0x1302c` (bl @0x00013092)
- `func_0x1302c` (bl @0x000130a2)
- `func_0x1302c` (bl @0x000130ac)


## Дизассембляция

```asm
  0c6c4:  cbz r1, #0xc6d2                   
  0c6c6:  ldr r2, [pc, #0x18]               -> периферия
  0c6c8:  ldr r2, [r2, #0xc]                
  0c6ca:  orrs r2, r0                       
  0c6cc:  ldr r3, [pc, #0x10]               -> периферия
  0c6ce:  str r2, [r3, #0xc]                
  0c6d0:  b #0xc6dc                         -> 0x0c6dc (вне списка функций)
  0c6d2:  ldr r2, [pc, #0xc]                -> периферия
  0c6d4:  ldr r2, [r2, #0xc]                
  0c6d6:  bics r2, r0                       
  0c6d8:  ldr r3, [pc, #4]                  -> периферия
  0c6da:  str r2, [r3, #0xc]                
  0c6dc:  bx lr                             
  ; --- literal-пул @0x0c6e0 (1 слов) — ВНЕ границ функции ---
  0c6e0:  .word 0x40021000  ; периферия
```
