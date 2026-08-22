# func_0x06dca

| | |
|---|---|
| offset в файле | `0x06dca` |
| vaddr (база 0x01800000) | `0x01806dca` |
 | размер кода | 144 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202044 — RAM (r0)
- 0x00206840 — RAM (r2)
- 0x21600002 — прочее (r6)
- 0x40051000 — периферия (r3)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x0161fdc0 (bl, вне списка функций)
- 0x0161fdde (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x06f28` (bl @0x01807038)

## Дизассембляция

```asm
  01806dca:  push {r3, r4, r5, r6, r7, lr}     
  01806dcc:  mov r5, r0                        
  01806dce:  subs r0, #8                       
  01806dd0:  ldrb r1, [r1, #0xd]               
  01806dd2:  ldr r6, [pc, #0x23c]              
  01806dd4:  uxth r0, r0                       
  01806dd6:  lsls r2, r1, #0x1d                
  01806dd8:  bpl #0x1806dde                    
  01806dda:  lsls r1, r1, #0x1f                
  01806ddc:  beq #0x1806e34                    
  01806dde:  ldr r0, [pc, #0x224]              (RAM)
  01806de0:  add.w r0, r0, r5, lsl #2          
  01806de4:  ldr.w r0, [r0, #0x210]            
  01806de8:  ldrb.w r1, [r0, #0xb0]            
  01806dec:  ldrh.w r0, [r0, #0xa0]            
  01806df0:  lsls r4, r1, #1                   
  01806df2:  lsls r7, r0, #1                   
  01806df4:  movs r1, #0x14                    
  01806df6:  mov r0, r5                        
  01806df8:  bl #0x161fdc0                     
  01806dfc:  subs r2, r7, r4                   
  01806dfe:  ubfx r1, r0, #0xa, #0x10          
  01806e02:  subs r2, r2, #2                   
  01806e04:  sub.w r4, r1, r2, lsr #1          
  01806e08:  cmp r4, #0                        
  01806e0a:  ble #0x1806e32                    
  01806e0c:  mov r7, r0                        
  01806e0e:  subs r1, r1, r4                   
  01806e10:  bfi r7, r1, #0xa, #0x10           
  01806e14:  mov r2, r7                        
  01806e16:  movs r1, #0x14                    
  01806e18:  mov r0, r5                        
  01806e1a:  bl #0x161fdde                     
  01806e1e:  ubfx r0, r7, #0xa, #0x10          
  01806e22:  str r0, [sp]                      
  01806e24:  mov r3, r4                        
  01806e26:  movs r2, #2                       
  01806e28:  movw r1, #0x43d                   
  01806e2c:  mov r0, r6                        
  01806e2e:  bl #0x15f5b92                     
  01806e32:  pop {r3, r4, r5, r6, r7, pc}      
  01806e34:  ldr r3, [pc, #0x1d0]              (периферия)
  01806e36:  ldrh.w r1, [r3, #0x24e]           
  01806e3a:  ldr r2, [pc, #0x1d0]              (RAM)
  01806e3c:  ldrb r4, [r2, r0]                 
  01806e3e:  bfi r1, r4, #0xa, #3              
  01806e42:  strh.w r1, [r3, #0x24e]           
  01806e46:  movs r1, #0                       
  01806e48:  strb r1, [r2, r0]                 
  01806e4a:  mov r0, r6                        
  01806e4c:  pop.w {r3, r4, r5, r6, r7, lr}    
  01806e50:  mov r2, r1                        
  01806e52:  movw r1, #0x43a                   
  01806e56:  b.w #0x15f5b92                    
  ; --- literal-пул @0x07004 (4 слов) — ВНЕ границ функции ---
  07004:  .word 0x00202044  ; RAM
  07008:  .word 0x40051000  ; периферия
  0700c:  .word 0x00206840  ; RAM
  07010:  .word 0x21600002
```
