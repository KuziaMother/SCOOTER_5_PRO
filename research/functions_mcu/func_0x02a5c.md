# func_0x02a5c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002a5c) | `0x00002a5c` |
| размер кода | 16 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01fe0` (bl @0x00002064)
- `func_0x020d8` (bl @0x00002110)
- `func_0x09b08` (bl @0x00009b0e)


## Дизассембляция

```asm
  02a5c:  push {r4, lr}                     
  02a5e:  movs r4, #1                       
  02a60:  movs r0, #0x9a                    
  02a62:  bl #0x1bdc                        -> func_0x01bdc
  02a66:  ands r4, r0                       
  02a68:  mov r0, r4                        
  02a6a:  pop {r4, pc}                      
```
