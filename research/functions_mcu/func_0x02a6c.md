# func_0x02a6c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002a6c) | `0x00002a6c` |
| размер кода | 28 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a7d0 — flash-mirror @0x1a7d0 (r1)
- 0x0801a7ec — flash-mirror @0x1a7ec (r1)
- 0x0801a808 — flash-mirror @0x1a808 (r1)

## Вызовы (callees)

- 0x04e50 (bl, вне списка функций)
- `func_0x1302c` (0x0001302c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x049b8` (bl @0x000049d8)


## Дизассембляция

```asm
  02a6c:  push {r4, lr}                     
  02a6e:  ldr r1, [pc, #0x18]               -> flash-mirror @0x1a7d0
  02a70:  ldr r0, [r1, #8]                  
  02a72:  bl #0x1302c                       -> func_0x1302c
  02a76:  ldr r1, [pc, #0x14]               -> flash-mirror @0x1a808
  02a78:  ldr r0, [r1, #0x10]               
  02a7a:  bl #0x4e50                        -> 0x04e50 (вне списка функций)
  02a7e:  ldr r1, [pc, #0x10]               -> flash-mirror @0x1a7ec
  02a80:  ldr r0, [r1, #0x10]               
  02a82:  bl #0x4e50                        -> 0x04e50 (вне списка функций)
  02a86:  pop {r4, pc}                      
  ; --- literal-пул @0x02a88 (3 слов) — ВНЕ границ функции ---
  02a88:  .word 0x0801a7d0  ; flash-mirror @0x1a7d0
  02a8c:  .word 0x0801a808  ; flash-mirror @0x1a808
  02a90:  .word 0x0801a7ec  ; flash-mirror @0x1a7ec
```
