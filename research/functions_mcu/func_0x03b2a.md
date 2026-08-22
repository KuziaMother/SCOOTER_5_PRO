# func_0x03b2a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003b2a) | `0x00003b2a` |
| размер кода | 20 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0a788` (0x0000a788, bl)
- `func_0x0c304` (0x0000c304, bl)
- `func_0x12aec` (0x00012aec, bl)
- `func_0x14924` (0x00014924, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e22)


## Дизассембляция

```asm
  03b2a:  push {r4, lr}                     
  03b2c:  bl #0xc304                        -> func_0x0c304
  03b30:  bl #0x12aec                       -> func_0x12aec
  03b34:  bl #0xa788                        -> func_0x0a788
  03b38:  bl #0x14924                       -> func_0x14924
  03b3c:  pop {r4, pc}                      
```
