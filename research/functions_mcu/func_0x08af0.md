# func_0x08af0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008af0) | `0x00008af0` |
| размер кода | 6 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a73 — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x08bec` (bl @0x00008c1e)
- `func_0x08bec` (bl @0x00008d18)
- `func_0x1395c` (bl @0x00013968)


## Дизассембляция

```asm
  08af0:  ldr r0, [pc, #4]                  -> RAM
  08af2:  ldrb r0, [r0]                     
  08af4:  bx lr                             
  ; --- literal-пул @0x08af8 (1 слов) — ВНЕ границ функции ---
  08af8:  .word 0x20000a73  ; RAM
```
