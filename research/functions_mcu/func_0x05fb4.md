# func_0x05fb4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005fb4) | `0x00005fb4` |
| размер кода | 32 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01c1c` (0x00001c1c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11c5e` (bl @0x00011c7e)


## Дизассембляция

```asm
  05fb4:  push {r3, r4, r5, lr}             
  05fb6:  movs r0, #0x92                    
  05fb8:  bl #0x1c1c                        -> func_0x01c1c
  05fbc:  mov r4, r0                        
  05fbe:  movw r0, #0x2710                  
  05fc2:  str r0, [sp]                      
  05fc4:  nop                               
  05fc6:  ldr r0, [sp]                      
  05fc8:  subs r1, r0, #1                   
  05fca:  str r1, [sp]                      
  05fcc:  cmp r0, #0                        
  05fce:  bne #0x5fc6                       
  05fd0:  mov r0, r4                        
  05fd2:  pop {r3, r4, r5, pc}              
```
