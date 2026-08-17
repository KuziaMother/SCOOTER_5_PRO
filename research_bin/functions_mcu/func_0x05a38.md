# func_0x05a38

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005a38) | `0x00005a38` |
| размер кода | 30 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000080 — RAM (r0)
- 0x20000f10 — RAM (r0)
- 0x20000f2c — RAM (r2)
- 0x20000fbb — RAM (r0)

## Вызовы (callees)

- `func_0x05134` (0x00005134, bl)
- 0x109c4 (bl, вне списка функций)
- 0x15588 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  05a38:  push {r4, lr}                     
  05a3a:  ldr r0, [pc, #0x1c]               -> RAM
  05a3c:  movs r2, #0x64                    
  05a3e:  ldr r1, [r0]                      
  05a40:  ldr r0, [pc, #0x18]               -> RAM
  05a42:  bl #0x15588                       -> 0x15588 (вне списка функций)
  05a46:  ldr r2, [pc, #0x18]               -> RAM
  05a48:  movs r1, #0xd                     
  05a4a:  ldr r0, [pc, #0x18]               -> RAM
  05a4c:  bl #0x5134                        -> func_0x05134
  05a50:  bl #0x109c4                       -> 0x109c4 (вне списка функций)
  05a54:  pop {r4, pc}                      
  ; --- literal-пул @0x05a58 (4 слов) — ВНЕ границ функции ---
  05a58:  .word 0x20000fbb  ; RAM
  05a5c:  .word 0x20000080  ; RAM
  05a60:  .word 0x20000f2c  ; RAM
  05a64:  .word 0x20000f10  ; RAM
```
