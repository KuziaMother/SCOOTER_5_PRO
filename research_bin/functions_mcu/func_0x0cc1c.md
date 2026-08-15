# func_0x0cc1c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cc1c) | `0x0000cc1c` |
| размер кода | 68 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00ffff3f — прочее (r1)
- 0x40002804 — периферия (r0)

## Вызовы (callees)

- `func_0x0c9a8` (0x0000c9a8, bl)

## Кто вызывает (callers / xrefs)

- `func_0x08a90` (bl @0x00008a98)


## Дизассембляция

```asm
  0cc1c:  push {r4, r5, r6, lr}             
  0cc1e:  mov r6, r0                        
  0cc20:  mov r4, r1                        
  0cc22:  movs r5, #0                       
  0cc24:  ldr r0, [pc, #0x38]               -> периферия
  0cc26:  ldr r0, [r0]                      
  0cc28:  ldr r1, [pc, #0x38]               
  0cc2a:  and.w r5, r0, r1                  
  0cc2e:  lsrs r0, r5, #0x10                
  0cc30:  strb r0, [r4, #3]                 
  0cc32:  ubfx r0, r5, #8, #5               
  0cc36:  strb r0, [r4, #1]                 
  0cc38:  and r0, r5, #0x3f                 
  0cc3c:  strb r0, [r4, #2]                 
  0cc3e:  ubfx r0, r5, #0xd, #3             
  0cc42:  strb r0, [r4]                     
  0cc44:  cbnz r6, #0xcc5e                  
  0cc46:  ldrb r0, [r4, #3]                 
  0cc48:  bl #0xc9a8                        -> func_0x0c9a8
  0cc4c:  strb r0, [r4, #3]                 
  0cc4e:  ldrb r0, [r4, #1]                 
  0cc50:  bl #0xc9a8                        -> func_0x0c9a8
  0cc54:  strb r0, [r4, #1]                 
  0cc56:  ldrb r0, [r4, #2]                 
  0cc58:  bl #0xc9a8                        -> func_0x0c9a8
  0cc5c:  strb r0, [r4, #2]                 
  0cc5e:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x0cc60 (2 слов) — ВНЕ границ функции ---
  0cc60:  .word 0x40002804  ; периферия
  0cc64:  .word 0x00ffff3f
```
