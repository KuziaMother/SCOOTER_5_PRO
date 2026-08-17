# func_0x05b5a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005b5a) | `0x00005b5a` |
| размер кода | 50 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01c1c` (0x00001c1c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11c5e` (bl @0x00011c62)


## Дизассембляция

```asm
  05b5a:  push {r3, r4, r5, lr}             
  05b5c:  movw r0, #0x2710                  
  05b60:  str r0, [sp]                      
  05b62:  nop                               
  05b64:  ldr r0, [sp]                      
  05b66:  subs r1, r0, #1                   
  05b68:  str r1, [sp]                      
  05b6a:  cmp r0, #0                        
  05b6c:  bne #0x5b64                       
  05b6e:  movs r0, #0x90                    
  05b70:  bl #0x1c1c                        -> func_0x01c1c
  05b74:  mov r4, r0                        
  05b76:  movw r0, #0x2710                  
  05b7a:  str r0, [sp]                      
  05b7c:  nop                               
  05b7e:  ldr r0, [sp]                      
  05b80:  subs r1, r0, #1                   
  05b82:  str r1, [sp]                      
  05b84:  cmp r0, #0                        
  05b86:  bne #0x5b7e                       
  05b88:  mov r0, r4                        
  05b8a:  pop {r3, r4, r5, pc}              
```
