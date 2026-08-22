# func_0x11c3c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080011c3c) | `0x00011c3c` |
| размер кода | 34 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01c1c` (0x00001c1c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11c5e` (bl @0x00011c7a)


## Дизассембляция

```asm
  11c3c:  push {r3, r4, r5, lr}             
  11c3e:  movw r0, #0x29bc                  
  11c42:  bl #0x1c1c                        -> func_0x01c1c
  11c46:  mov r4, r0                        
  11c48:  movw r0, #0x2710                  
  11c4c:  str r0, [sp]                      
  11c4e:  nop                               
  11c50:  ldr r0, [sp]                      
  11c52:  subs r1, r0, #1                   
  11c54:  str r1, [sp]                      
  11c56:  cmp r0, #0                        
  11c58:  bne #0x11c50                      
  11c5a:  mov r0, r4                        
  11c5c:  pop {r3, r4, r5, pc}              
```
