# func_0x04fba

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004fba) | `0x00004fba` |
| размер кода | 4 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x12b50` (bl @0x00012bf8)
- `func_0x12d90` (bl @0x00012e38)


## Дизассембляция

```asm
  04fba:  str r1, [r0, #4]                  
  04fbc:  bx lr                             
```
