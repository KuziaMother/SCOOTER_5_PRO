# func_0x0cd0c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cd0c) | `0x0000cd0c` |
| размер кода | 110 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40002824 — периферия (r1)

## Вызовы (callees)

- `func_0x0cbb8` (0x0000cbb8, bl)
- `func_0x0cc08` (0x0000cc08, bl)
- 0x0cd62 (b, вне списка функций)
- 0x0cd6e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03150` (bl @0x00003162)


## Дизассембляция

```asm
  0cd0c:  push {r4, r5, r6, lr}             
  0cd0e:  mov r4, r0                        
  0cd10:  movs r6, #0                       
  0cd12:  movs r5, #0                       
  0cd14:  movs r0, #0xca                    
  0cd16:  ldr r1, [pc, #0x64]               -> периферия
  0cd18:  str r0, [r1]                      
  0cd1a:  movs r0, #0x53                    
  0cd1c:  str r0, [r1]                      
  0cd1e:  bl #0xcbb8                        -> func_0x0cbb8
  0cd22:  cbnz r0, #0xcd26                  
  0cd24:  b #0xcd62                         -> 0x0cd62 (вне списка функций)
  0cd26:  ldr r0, [pc, #0x54]               -> периферия
  0cd28:  subs r0, #0x1c                    
  0cd2a:  ldr r0, [r0]                      
  0cd2c:  bic r0, r0, #0x40                 
  0cd30:  ldr r1, [pc, #0x48]               -> периферия
  0cd32:  subs r1, #0x1c                    
  0cd34:  str r0, [r1]                      
  0cd36:  mov r0, r1                        
  0cd38:  ldr r0, [r0]                      
  0cd3a:  ldr r1, [r4]                      
  0cd3c:  orrs r0, r1                       
  0cd3e:  ldr r1, [pc, #0x3c]               -> периферия
  0cd40:  subs r1, #0x1c                    
  0cd42:  str r0, [r1]                      
  0cd44:  ldr r1, [pc, #0x34]               -> периферия
  0cd46:  subs r1, #0x14                    
  0cd48:  ldr r0, [r4, #8]                  
  0cd4a:  str r0, [r1]                      
  0cd4c:  mov r0, r1                        
  0cd4e:  ldr r0, [r0]                      
  0cd50:  ldrh r1, [r4, #4]                 
  0cd52:  orr.w r0, r0, r1, lsl #16         
  0cd56:  ldr r1, [pc, #0x24]               -> периферия
  0cd58:  subs r1, #0x14                    
  0cd5a:  str r0, [r1]                      
  0cd5c:  bl #0xcc08                        -> func_0x0cc08
  0cd60:  movs r6, #1                       
  0cd62:  movs r0, #0xff                    
  0cd64:  ldr r1, [pc, #0x14]               -> периферия
  0cd66:  str r0, [r1]                      
  0cd68:  movs r5, #0                       
  0cd6a:  b #0xcd6e                         -> 0x0cd6e (вне списка функций)
  0cd6c:  adds r5, r5, #1                   
  0cd6e:  movw r0, #0x2ff                   
  0cd72:  cmp r5, r0                        
  0cd74:  blo #0xcd6c                       
  0cd76:  mov r0, r6                        
  0cd78:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x0cd7c (1 слов) — ВНЕ границ функции ---
  0cd7c:  .word 0x40002824  ; периферия
```
