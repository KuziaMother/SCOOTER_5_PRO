# func_0x0e3e4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e3e4) | `0x0000e3e4` |
| размер кода | 6 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x0ec70` (bl @0x0000ec92)
- `func_0x0ec70` (bl @0x0000ecf0)


## Дизассембляция

```asm
  0e3e4:  movs r1, #0                       
  0e3e6:  strh r1, [r0]                     
  0e3e8:  bx lr                             
```
