# func_0x08d90

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008d90) | `0x00008d90` |
| размер кода | 6 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001344 — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x063b8` (bl @0x0000643c)
- `func_0x063b8` (bl @0x000064cc)
- `func_0x063b8` (bl @0x00006532)
- `func_0x0ea64` (bl @0x0000ea6a)
- `func_0x0ea64` (bl @0x0000ea72)
- `func_0x0ea64` (bl @0x0000ea86)
- `func_0x0ea64` (bl @0x0000ea8e)
- `func_0x0ea64` (bl @0x0000eaa4)
- `func_0x0ea64` (bl @0x0000eaac)
- `func_0x0ea64` (bl @0x0000eac0)
- `func_0x0ea64` (bl @0x0000eaca)
- `func_0x0ea64` (bl @0x0000ead2)
- `func_0x0ea64` (bl @0x0000eae6)
- `func_0x0ea64` (bl @0x0000eaee)
- `func_0x0ea64` (bl @0x0000eb04)
- `func_0x0ea64` (bl @0x0000eb16)
- `func_0x0ea64` (bl @0x0000eb20)
- `func_0x0ea64` (bl @0x0000eb28)
- `func_0x0ea64` (bl @0x0000eb3c)
- `func_0x0ea64` (bl @0x0000eb44)
- `func_0x0ea64` (bl @0x0000eb5a)
- `func_0x0ea64` (bl @0x0000eb6c)
- `func_0x0ea64` (bl @0x0000eb76)
- `func_0x0ea64` (bl @0x0000eb7e)
- `func_0x0ea64` (bl @0x0000eb96)
- `func_0x0ea64` (bl @0x0000eb9e)
- `func_0x0ea64` (bl @0x0000ebb8)
- `func_0x0ea64` (bl @0x0000ebc6)


## Дизассембляция

```asm
  08d90:  ldr r0, [pc, #4]                  -> RAM
  08d92:  ldr r0, [r0]                      
  08d94:  bx lr                             
  ; --- literal-пул @0x08d98 (1 слов) — ВНЕ границ функции ---
  08d98:  .word 0x20001344  ; RAM
```
