# func_0x09f64

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080009f64) | `0x00009f64` |
| размер кода | 12 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x09b44` (0x00009b44, bl)
- `func_0x09f70` (0x00009f70, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0c200` (bl @0x0000c204)


## Дизассембляция

```asm
  09f64:  push {lr}                         
  09f66:  bl #0x9b44                        -> func_0x09b44
  09f6a:  bl #0x9f70                        -> func_0x09f70
  09f6e:  pop {pc}                          
```
