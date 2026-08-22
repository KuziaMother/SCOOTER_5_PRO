# func_0x110f0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800110f0) | `0x000110f0` |
| размер кода | 10 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x05b8c` (0x00005b8c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11de8` (bl @0x00012170)


## Дизассембляция

```asm
  110f0:  push {r4, lr}                     
  110f2:  movs r0, #0                       
  110f4:  bl #0x5b8c                        -> func_0x05b8c
  110f8:  pop {r4, pc}                      
```
