# func_0x139ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800139ac) | `0x000139ac` |
| размер кода | 14 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x13c78` (0x00013c78, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11de8` (bl @0x00011ef2)
- `func_0x11de8` (bl @0x00012044)


## Дизассембляция

```asm
  139ac:  push {r3, lr}                     
  139ae:  movs r0, #3                       
  139b0:  str r0, [sp]                      
  139b2:  mov r0, sp                        
  139b4:  bl #0x13c78                       -> func_0x13c78
  139b8:  pop {r3, pc}                      
```
