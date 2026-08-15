# func_0x084a0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800084a0) | `0x000084a0` |
| размер кода | 22 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0833c` (0x0000833c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x037f4` (bl @0x0000380c)
- `func_0x037f4` (bl @0x0000382c)
- `func_0x0d878` (bl @0x0000d8f2)
- `func_0x0d878` (bl @0x0000d922)
- `func_0x119e4` (bl @0x00011aac)
- `func_0x119e4` (bl @0x00011b14)
- `func_0x14368` (bl @0x00014384)
- `func_0x14368` (bl @0x000143a4)
- `func_0x147ac` (bl @0x000147ce)
- `func_0x147ac` (bl @0x000147f0)
- `func_0x14802` (bl @0x0001487c)
- `func_0x1570c` (bl @0x0001572a)
- `func_0x1570c` (bl @0x0001574a)
- `func_0x15790` (bl @0x000157b0)
- `func_0x15790` (bl @0x000157d2)
- `func_0x157e0` (bl @0x0001584c)


## Дизассембляция

```asm
  084a0:  push.w {r4, r5, r6, r7, r8, lr}   
  084a4:  mov r6, r0                        
  084a6:  mov r7, r1                        
  084a8:  mov r4, r2                        
  084aa:  bl #0x833c                        -> func_0x0833c
  084ae:  cbnz r6, #0x84b6                  
  084b0:  movs r0, #0                       
  084b2:  pop.w {r4, r5, r6, r7, r8, pc}    
```
