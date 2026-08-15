# func_0x09a18

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080009a18) | `0x00009a18` |
| размер кода | 8 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x099f0` (0x000099f0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0c368` (bl @0x0000c40e)


## Дизассембляция

```asm
  09a18:  push {r4, lr}                     
  09a1a:  bl #0x99f0                        -> func_0x099f0
  09a1e:  pop {r4, pc}                      
```
