# func_0x01b2a

| | |
|---|---|
| offset в файле | `0x01b2a` |
| vaddr (база 0x01800000) | `0x01801b2a` |
 | размер кода | 218 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200164 — RAM (r0)
- 0x0020036c — RAM (r0)
- 0x0020674c — RAM (r1)

## Вызовы (callees)

- 0x01802d16 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x027d6` (bl @0x01802850)

## Дизассембляция

```asm
  01801b2a:  push {r4, r5, r6, lr}             
  01801b2c:  ldr r0, [pc, #0xd4]               (RAM)
  01801b2e:  ldrb.w r1, [r0, #0x1fa]           
  01801b32:  bic r1, r1, #0x3f                 
  01801b36:  strb.w r1, [r0, #0x1fa]           
  01801b3a:  ldrb.w r1, [r0, #0x1fb]           
  01801b3e:  bic r1, r1, #0x3f                 
  01801b42:  strb.w r1, [r0, #0x1fb]           
  01801b46:  ldr r1, [pc, #0x15c]              (RAM)
  01801b48:  addw r0, r0, #0x1f7               
  01801b4c:  ldr r1, [r1]                      
  01801b4e:  lsls r2, r1, #0x1f                
  01801b50:  beq #0x1801b54                    
  01801b52:  movs r2, #0x1e                    
  01801b54:  strb r2, [r0, #5]                 
  01801b56:  ldr r0, [pc, #0x1c4]              (RAM)
  01801b58:  lsls r1, r1, #0x1e                
  01801b5a:  bpl #0x1801b6c                    
  01801b5c:  ldrb r1, [r0]                     
  01801b5e:  orr r1, r1, #0x80                 
  01801b62:  strb r1, [r0]                     
  01801b64:  ldrb r1, [r0, #1]                 
  01801b66:  orr r1, r1, #1                    
  01801b6a:  strb r1, [r0, #1]                 
  01801b6c:  ldr r5, [pc, #0x94]               (RAM)
  01801b6e:  add.w r4, r5, #0x148              
  01801b72:  ldr.w r0, [r5, #0x1d0]            
  01801b76:  bic r0, r0, #0x800000             
  01801b7a:  orr r0, r0, #0x3500000            
  01801b7e:  str.w r0, [r5, #0x1d0]            
  01801b82:  ldrb.w r0, [r5, #0x1d4]           
  01801b86:  and r0, r0, #3                    
  01801b8a:  cmp r0, #1                        
  01801b8c:  bne #0x1801baa                    
  01801b8e:  ldrb r0, [r4, #1]                 
  01801b90:  cmp r0, #7                        
  01801b92:  bne #0x1801baa                    
  01801b94:  movs r1, #0xfc                    
  01801b96:  movs r2, #0x10                    
  01801b98:  adds r0, r1, #4                   
  01801b9a:  bl #0x1802d16                     -> 0x02d16 (вне списка функций)
  01801b9e:  movs r2, #1                       
  01801ba0:  movs r1, #3                       
  01801ba2:  movw r0, #0x101                   
  01801ba6:  bl #0x1802d16                     -> 0x02d16 (вне списка функций)
  01801baa:  ldrb r0, [r4]                     
  01801bac:  cbz r0, #0x1801bec                
  01801bae:  cmp r0, #0xff                     
  01801bb0:  beq #0x1801bec                    
  01801bb2:  lsls r0, r0, #0x19                
  01801bb4:  lsrs r2, r0, #0x18                
  01801bb6:  movs r1, #0xfe                    
  01801bb8:  movw r0, #0x14d                   
  01801bbc:  bl #0x1802d16                     -> 0x02d16 (вне списка функций)
  01801bc0:  ldrb r0, [r4]                     
  01801bc2:  movs r1, #1                       
  01801bc4:  lsrs r2, r0, #7                   
  01801bc6:  mov.w r0, #0x14e                  
  01801bca:  bl #0x1802d16                     -> 0x02d16 (вне списка функций)
  01801bce:  ldrb r0, [r4]                     
  01801bd0:  movs r1, #0xfe                    
  01801bd2:  lsls r0, r0, #0x19                
  01801bd4:  lsrs r2, r0, #0x18                
  01801bd6:  mov.w r0, #0x150                  
  01801bda:  bl #0x1802d16                     -> 0x02d16 (вне списка функций)
  01801bde:  ldrb r0, [r4]                     
  01801be0:  movs r1, #1                       
  01801be2:  lsrs r2, r0, #7                   
  01801be4:  movw r0, #0x151                   
  01801be8:  bl #0x1802d16                     -> 0x02d16 (вне списка функций)
  01801bec:  ldr r0, [pc, #0x14]               (RAM)
  01801bee:  ldrb.w r0, [r0, #0x147]           
  01801bf2:  lsls r0, r0, #0x18                
  01801bf4:  bmi #0x1801c02                    
  01801bf6:  ldr.w r0, [r5, #0x1d0]            
  01801bfa:  bic r0, r0, #0x200000             
  01801bfe:  str.w r0, [r5, #0x1d0]            
  01801c02:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x01c04 (1 слов) — ВНЕ границ функции ---
  01c04:  .word 0x00200164  ; RAM
  ; --- literal-пул @0x01ca4 (1 слов) — ВНЕ границ функции ---
  01ca4:  .word 0x0020674c  ; RAM
  ; --- literal-пул @0x01d1c (1 слов) — ВНЕ границ функции ---
  01d1c:  .word 0x0020036c  ; RAM
```
