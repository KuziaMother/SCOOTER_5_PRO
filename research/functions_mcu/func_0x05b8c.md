# func_0x05b8c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005b8c) | `0x00005b8c` |
| размер кода | 10 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x04de0` (0x00004de0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x110f0` (bl @0x000110f4)


## Дизассембляция

```asm
  05b8c:  push {r4, lr}                     
  05b8e:  mov r4, r0                        
  05b90:  bl #0x4de0                        -> func_0x04de0
  05b94:  pop {r4, pc}                      
```
