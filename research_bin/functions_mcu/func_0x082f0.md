# func_0x082f0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800082f0) | `0x000082f0` |
| размер кода | 12 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0833c` (0x0000833c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0d878` (bl @0x0000d8a4)
- `func_0x0d878` (bl @0x0000d8be)
- `func_0x119e4` (bl @0x00011a70)
- `func_0x147ac` (bl @0x000147b4)
- `func_0x14802` (bl @0x00014858)
- `func_0x14802` (bl @0x000148c4)
- `func_0x1570c` (bl @0x00015714)
- `func_0x15790` (bl @0x00015798)
- `func_0x157e0` (bl @0x0001582a)
- `func_0x157e0` (bl @0x000158b6)


## Дизассембляция

```asm
  082f0:  push {r4, lr}                     
  082f2:  mov r4, r0                        
  082f4:  bl #0x833c                        -> func_0x0833c
  082f8:  cbz r0, #0x82fc                   
  082fa:  pop {r4, pc}                      
```
