# func_0x03b20

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003b20) | `0x00003b20` |
| размер кода | 10 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01cf6` (bl @0x00001d0e)


## Дизассембляция

```asm
  03b20:  push {r4, lr}                     
  03b22:  movs r0, #0x9a                    
  03b24:  bl #0x1bdc                        -> func_0x01bdc
  03b28:  pop {r4, pc}                      
```
