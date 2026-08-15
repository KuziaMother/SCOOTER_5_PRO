# func_0x0a6a4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000a6a4) | `0x0000a6a4` |
| размер кода | 6 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000040 — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x04630` (bl @0x0000467a)
- `func_0x08834` (bl @0x00008846)
- `func_0x1337c` (bl @0x0001366c)


## Дизассембляция

```asm
  0a6a4:  ldr r0, [pc, #4]                  -> RAM
  0a6a6:  ldrb r0, [r0]                     
  0a6a8:  bx lr                             
  ; --- literal-пул @0x0a6ac (1 слов) — ВНЕ границ функции ---
  0a6ac:  .word 0x20000040  ; RAM
```
