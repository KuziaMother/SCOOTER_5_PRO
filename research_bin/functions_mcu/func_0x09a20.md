# func_0x09a20

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080009a20) | `0x00009a20` |
| размер кода | 34 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x099d4` (0x000099d4, bl)
- `func_0x099e0` (0x000099e0, bl)
- `func_0x099f0` (0x000099f0, bl)
- `func_0x09a00` (0x00009a00, bl)
- `func_0x09a0c` (0x00009a0c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03034` (bl @0x00003064)


## Дизассембляция

```asm
  09a20:  push {r4, lr}                     
  09a22:  mov r4, r0                        
  09a24:  movw r0, #0x5555                  
  09a28:  bl #0x9a0c                        -> func_0x09a0c
  09a2c:  movs r0, #6                       
  09a2e:  bl #0x9a00                        -> func_0x09a00
  09a32:  uxth r0, r4                       
  09a34:  bl #0x99d4                        -> func_0x099d4
  09a38:  bl #0x99f0                        -> func_0x099f0
  09a3c:  bl #0x99e0                        -> func_0x099e0
  09a40:  pop {r4, pc}                      
```
