# func_0x0ccbc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ccbc) | `0x0000ccbc` |
| размер кода | 72 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x007f7f7f — прочее (r1)
- 0x40002800 — периферия (r0)

## Вызовы (callees)

- `func_0x0c9a8` (0x0000c9a8, bl)

## Кто вызывает (callers / xrefs)

- `func_0x08a90` (bl @0x00008aa0)


## Дизассембляция

```asm
  0ccbc:  push {r4, r5, r6, lr}             
  0ccbe:  mov r6, r0                        
  0ccc0:  mov r4, r1                        
  0ccc2:  movs r5, #0                       
  0ccc4:  ldr r0, [pc, #0x3c]               -> периферия
  0ccc6:  ldr r0, [r0]                      
  0ccc8:  ldr r1, [pc, #0x3c]               
  0ccca:  and.w r5, r0, r1                  
  0ccce:  ubfx r0, r5, #0x10, #6            
  0ccd2:  strb r0, [r4]                     
  0ccd4:  ubfx r0, r5, #8, #7               
  0ccd8:  strb r0, [r4, #1]                 
  0ccda:  and r0, r5, #0x7f                 
  0ccde:  strb r0, [r4, #2]                 
  0cce0:  and r0, r5, #0x400000             
  0cce4:  lsrs r0, r0, #0x10                
  0cce6:  strb r0, [r4, #3]                 
  0cce8:  cbnz r6, #0xcd02                  
  0ccea:  ldrb r0, [r4]                     
  0ccec:  bl #0xc9a8                        -> func_0x0c9a8
  0ccf0:  strb r0, [r4]                     
  0ccf2:  ldrb r0, [r4, #1]                 
  0ccf4:  bl #0xc9a8                        -> func_0x0c9a8
  0ccf8:  strb r0, [r4, #1]                 
  0ccfa:  ldrb r0, [r4, #2]                 
  0ccfc:  bl #0xc9a8                        -> func_0x0c9a8
  0cd00:  strb r0, [r4, #2]                 
  0cd02:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x0cd04 (2 слов) — ВНЕ границ функции ---
  0cd04:  .word 0x40002800  ; периферия
  0cd08:  .word 0x007f7f7f
```
