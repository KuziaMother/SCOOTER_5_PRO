# func_0x08e14

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008e14) | `0x00008e14` |
| размер кода | 6 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001359 — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x04630` (bl @0x00004650)
- `func_0x063b8` (bl @0x00006466)
- `func_0x063b8` (bl @0x000064b4)
- `func_0x06ccc` (bl @0x00006d4c)
- `func_0x06ccc` (bl @0x00006de6)
- `func_0x07a30` (bl @0x00007b3a)
- `func_0x07a30` (bl @0x00007b9e)
- `func_0x14ed0` (bl @0x00014ef4)


## Дизассембляция

```asm
  08e14:  ldr r0, [pc, #4]                  -> RAM
  08e16:  ldrb r0, [r0, #0x1f]              
  08e18:  bx lr                             
  ; --- literal-пул @0x08e1c (1 слов) — ВНЕ границ функции ---
  08e1c:  .word 0x20001359  ; RAM
```
