# func_0x0c9a8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c9a8) | `0x0000c9a8` |
| размер кода | 22 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x0ca3c` (bl @0x0000ca6a)
- `func_0x0cc1c` (bl @0x0000cc48)
- `func_0x0cc1c` (bl @0x0000cc50)
- `func_0x0cc1c` (bl @0x0000cc58)
- `func_0x0ccbc` (bl @0x0000ccec)
- `func_0x0ccbc` (bl @0x0000ccf4)
- `func_0x0ccbc` (bl @0x0000ccfc)
- `func_0x0cd80` (bl @0x0000cda8)
- `func_0x0cd80` (bl @0x0000cdb0)


## Дизассембляция

```asm
  0c9a8:  mov r1, r0                        
  0c9aa:  nop                               
  0c9ac:  lsrs r0, r1, #4                   
  0c9ae:  add.w r0, r0, r0, lsl #2          
  0c9b2:  lsls r2, r0, #1                   
  0c9b4:  and r0, r1, #0xf                  
  0c9b8:  add r0, r2                        
  0c9ba:  uxtb r0, r0                       
  0c9bc:  bx lr                             
```
