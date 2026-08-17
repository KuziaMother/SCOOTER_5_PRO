# func_0x11c5e

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080011c5e) | `0x00011c5e` |
| размер кода | 38 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x02770` (0x00002770, bl)
- `func_0x05b5a` (0x00005b5a, bl)
- `func_0x05fb4` (0x00005fb4, bl)
- `func_0x11c3c` (0x00011c3c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01cf6` (bl @0x00001cf8)


## Дизассембляция

```asm
  11c5e:  push {r3, r4, r5, lr}             
  11c60:  movs r4, #0                       
  11c62:  bl #0x5b5a                        -> func_0x05b5a
  11c66:  movs r4, #0x11                    
  11c68:  movs r0, #2                       
  11c6a:  mov r3, r4                        
  11c6c:  movw r2, #0x9239                  
  11c70:  movs r1, #8                       
  11c72:  str r0, [sp]                      
  11c74:  movs r0, #0                       
  11c76:  bl #0x2770                        -> func_0x02770
  11c7a:  bl #0x11c3c                       -> func_0x11c3c
  11c7e:  bl #0x5fb4                        -> func_0x05fb4
  11c82:  pop {r3, r4, r5, pc}              
```
