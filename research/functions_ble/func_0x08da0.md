# func_0x08da0

| | |
|---|---|
| offset в файле | `0x08da0` |
| vaddr (база 0x01800000) | `0x01808da0` |
 | размер кода | 130 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00201994 — RAM (r0)
- 0x00201bcc — RAM (r4)
- 0x00201bce — RAM (r1)
- 0x00201bd0 — RAM (r0)
- 0x00202000 — RAM (r5)
- 0x00206320 — RAM (r0)
- 0x00206838 — RAM (r4)
- 0x21600002 — прочее (r5)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x016158ce (bl, вне списка функций)
- 0x0162b5d4 (bl, вне списка функций)
- `func_0x08d24` (0x01808d24, bl)
- 0x01808e18 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08eb6` (bl @0x01808edc)

## Дизассембляция

```asm
  01808da0:  push {r3, r4, r5, lr}             
  01808da2:  ldrh r3, [r0]                     
  01808da4:  movs r4, #3                       
  01808da6:  ldr r5, [pc, #0xb0]               (RAM)
  01808da8:  add.w r4, r4, r3, lsr #8          
  01808dac:  bic r4, r4, #1                    
  01808db0:  ldrb r5, [r5]                     
  01808db2:  adds r4, r4, #6                   
  01808db4:  add.w r4, r4, r5, lsl #1          
  01808db8:  str r0, [sp]                      
  01808dba:  lsrs r3, r3, #8                   
  01808dbc:  mov r0, r4                        
  01808dbe:  bl #0x1808d24                     -> func_0x08d24
  01808dc2:  cmp r0, #0                        
  01808dc4:  beq #0x1808e20                    
  01808dc6:  ldr r4, [pc, #0x70]               (RAM)
  01808dc8:  ldrb r0, [r4, #3]                 
  01808dca:  cbnz r0, #0x1808e1e               
  01808dcc:  ldr r0, [pc, #0x7c]               (RAM)
  01808dce:  add.w r1, r0, #0x38               
  01808dd2:  ldr r0, [r0, #0x44]               
  01808dd4:  ldm r1, {r1, r2, r3}              
  01808dd6:  str r0, [sp]                      
  01808dd8:  ldr r0, [pc, #0x74]               (RAM)
  01808dda:  ldr r0, [r0]                      
  01808ddc:  bl #0x162b5d4                     
  01808de0:  ldr r5, [pc, #0x4c]               
  01808de2:  cbz r0, #0x1808dec                
  01808de4:  movs r2, #0                       
  01808de6:  movw r1, #0x449                   
  01808dea:  b #0x1808e18                      -> 0x08e18 (вне списка функций)
  01808dec:  movs r0, #1                       
  01808dee:  strb r0, [r4, #3]                 
  01808df0:  ldr r4, [pc, #0x4c]               (RAM)
  01808df2:  ldrb r0, [r4]                     
  01808df4:  cbnz r0, #0x1808e0c               
  01808df6:  ldr r0, [pc, #0x4c]               (RAM)
  01808df8:  ldrh r0, [r0]                     
  01808dfa:  orr r1, r0, #0x100                
  01808dfe:  movs r0, #0xda                    
  01808e00:  bl #0x16158ce                     
  01808e04:  ldr r1, [pc, #0x40]               (RAM)
  01808e06:  mov.w r0, #0x100                  
  01808e0a:  strh r0, [r1]                     
  01808e0c:  ldrb r0, [r4]                     
  01808e0e:  mov.w r1, #0x448                  
  01808e12:  adds r0, r0, #1                   
  01808e14:  strb r0, [r4]                     
  01808e16:  movs r2, #0                       
  01808e18:  mov r0, r5                        
  01808e1a:  bl #0x15f5b92                     
  01808e1e:  movs r0, #1                       
  01808e20:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x08e30 (1 слов) — ВНЕ границ функции ---
  08e30:  .word 0x21600002
  ; --- literal-пул @0x08e38 (1 слов) — ВНЕ границ функции ---
  08e38:  .word 0x00206838  ; RAM
  ; --- literal-пул @0x08e40 (5 слов) — ВНЕ границ функции ---
  08e40:  .word 0x00201bcc  ; RAM
  08e44:  .word 0x00201bd0  ; RAM
  08e48:  .word 0x00201bce  ; RAM
  08e4c:  .word 0x00206320  ; RAM
  08e50:  .word 0x00201994  ; RAM
  ; --- literal-пул @0x08e58 (1 слов) — ВНЕ границ функции ---
  08e58:  .word 0x00202000  ; RAM
```
