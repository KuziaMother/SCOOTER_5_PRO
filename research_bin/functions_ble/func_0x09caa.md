# func_0x09caa

| | |
|---|---|
| offset в файле | `0x09caa` |
| vaddr (база 0x01800000) | `0x01809caa` |
 | размер кода | 150 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005ec — RAM (r5)
- 0x00206958 — RAM (r4)

## Вызовы (callees)

- `func_0x09bec` (0x01809bec, bl)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01809caa:  push {r4, r5, r6, lr}             
  01809cac:  mov.w r1, #0x758                  
  01809cb0:  movs r0, #9                       
  01809cb2:  bl #0x1809bec                     -> func_0x09bec
  01809cb6:  ldr r4, [pc, #0x24c]              (RAM)
  01809cb8:  ldr r5, [pc, #0x264]              (RAM)
  01809cba:  lsls r2, r0, #5                   
  01809cbc:  strb r0, [r4, #2]                 
  01809cbe:  movs r1, #0x60                    
  01809cc0:  ldr r3, [r5]                      
  01809cc2:  movs r0, #0x20                    
  01809cc4:  blx r3                            
  01809cc6:  movw r1, #0x2eea                  
  01809cca:  movs r0, #0xb                     
  01809ccc:  bl #0x1809bec                     -> func_0x09bec
  01809cd0:  strb r0, [r4, #3]                 
  01809cd2:  lsls r2, r0, #7                   
  01809cd4:  ldr r3, [r5]                      
  01809cd6:  mov.w r1, #0x380                  
  01809cda:  movs r0, #0x20                    
  01809cdc:  blx r3                            
  01809cde:  mov.w r1, #0x410                  
  01809ce2:  movs r0, #0xa                     
  01809ce4:  bl #0x1809bec                     -> func_0x09bec
  01809ce8:  strb r0, [r4, #1]                 
  01809cea:  lsls r2, r0, #3                   
  01809cec:  movs r1, #0x38                    
  01809cee:  ldr r3, [r5]                      
  01809cf0:  movs r0, #0x27                    
  01809cf2:  blx r3                            
  01809cf4:  movw r1, #0x665                   
  01809cf8:  movs r0, #0xc                     
  01809cfa:  bl #0x1809bec                     -> func_0x09bec
  01809cfe:  strb r0, [r4]                     
  01809d00:  ldr r3, [r5]                      
  01809d02:  movw r1, #0xffff                  
  01809d06:  pop.w {r4, r5, r6, lr}            
  01809d0a:  and.w r2, r1, r0, lsl #12         
  01809d0e:  mov.w r1, #0xf000                 
  01809d12:  movs r0, #0x28                    
  01809d14:  bx r3                             
  01809d16:  ldr r0, [pc, #0x1ec]              (RAM)
  01809d18:  ldr r0, [r0, #4]                  
  01809d1a:  ldrb r1, [r0, #2]                 
  01809d1c:  lsls r1, r1, #0x1a                
  01809d1e:  bmi #0x1809d3e                    
  01809d20:  ldrb.w r0, [r0, #0x5a]            
  01809d24:  movs r2, #0x38                    
  01809d26:  and r1, r0, #7                    
  01809d2a:  and.w r0, r2, r0, lsr #1          
  01809d2e:  ldr r3, [pc, #0x1f0]              (RAM)
  01809d30:  orrs r1, r0                       
  01809d32:  lsls r2, r1, #4                   
  01809d34:  ldr r3, [r3]                      
  01809d36:  mov.w r1, #0x3f0                  
  01809d3a:  movs r0, #0x23                    
  01809d3c:  bx r3                             
  01809d3e:  bx lr                             
  ; --- literal-пул @0x09f04 (1 слов) — ВНЕ границ функции ---
  09f04:  .word 0x00206958  ; RAM
  ; --- literal-пул @0x09f20 (1 слов) — ВНЕ границ функции ---
  09f20:  .word 0x002005ec  ; RAM
```
