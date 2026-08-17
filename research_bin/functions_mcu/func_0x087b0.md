# func_0x087b0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800087b0) | `0x000087b0` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x01858` (bl @0x0000185e)
- `func_0x0332c` (bl @0x0000334e)
- `func_0x03588` (bl @0x0000358c)
- `func_0x0ae9a` (bl @0x0000aed4)
- `func_0x0aece` (bl @0x0000aed4)
- `func_0x0b302` (bl @0x0000b308)
- `func_0x0bc86` (bl @0x0000bc8a)
- `func_0x107ec` (bl @0x000107f0)


## Дизассембляция

```asm
  087b0:  movw r1, #0xffff                  
  087b4:  strh r1, [r0]                     
  087b6:  movs r1, #0                       
  087b8:  strb r1, [r0, #3]                 
  087ba:  str r1, [r0, #8]                  
  087bc:  movs r1, #0xf                     
  087be:  str r1, [r0, #0xc]                
  087c0:  movs r1, #0                       
  087c2:  strb r1, [r0, #4]                 
  087c4:  strb r1, [r0, #2]                 
  087c6:  bx lr                             
```
