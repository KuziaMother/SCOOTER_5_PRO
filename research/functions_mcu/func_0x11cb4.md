# func_0x11cb4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080011cb4) | `0x00011cb4` |
| размер кода | 188 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x04bf8000 — прочее (r0)
- 0x0700ffff — прочее (r1)
- 0x08003000 — flash-mirror @0x03000 (r0)
- 0x40001820 — периферия (r0)
- 0x40007000 — периферия (r0)
- 0x40021000 — периферия (r0)
- 0x40022000 — периферия (r0)
- 0xe000ed88 — Cortex-M (NVIC/SCB/SysTick) (r0)
- 0xf8ffc000 — прочее (r1)
- 0xfef6ffff — прочее (r1)

## Вызовы (callees)

- `func_0x10abc` (0x00010abc, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  11cb4:  push {r4, lr}                     
  11cb6:  ldr r0, [pc, #0xb8]               -> Cortex-M (NVIC/SCB/SysTick)
  11cb8:  ldr r0, [r0]                      
  11cba:  orr r0, r0, #0xf00000             
  11cbe:  ldr r1, [pc, #0xb0]               -> Cortex-M (NVIC/SCB/SysTick)
  11cc0:  str r0, [r1]                      
  11cc2:  ldr r0, [pc, #0xb0]               -> периферия
  11cc4:  ldr r0, [r0, #0x24]               
  11cc6:  orr r0, r0, #4                    
  11cca:  ldr r1, [pc, #0xa8]               -> периферия
  11ccc:  str r0, [r1, #0x24]               
  11cce:  mov r0, r1                        
  11cd0:  ldr r0, [r0, #4]                  
  11cd2:  ldr r1, [pc, #0xa4]               
  11cd4:  ands r0, r1                       
  11cd6:  ldr r1, [pc, #0x9c]               -> периферия
  11cd8:  str r0, [r1, #4]                  
  11cda:  mov r0, r1                        
  11cdc:  ldr r0, [r0]                      
  11cde:  ldr r1, [pc, #0x9c]               
  11ce0:  ands r0, r1                       
  11ce2:  ldr r1, [pc, #0x90]               -> периферия
  11ce4:  str r0, [r1]                      
  11ce6:  mov r0, r1                        
  11ce8:  ldr r0, [r0]                      
  11cea:  bic r0, r0, #0x40000              
  11cee:  str r0, [r1]                      
  11cf0:  mov r0, r1                        
  11cf2:  ldr r0, [r0, #4]                  
  11cf4:  ldr r1, [pc, #0x88]               
  11cf6:  ands r0, r1                       
  11cf8:  ldr r1, [pc, #0x78]               -> периферия
  11cfa:  str r0, [r1, #4]                  
  11cfc:  movs r0, #0                       
  11cfe:  str r0, [r1, #0x2c]               
  11d00:  mov.w r0, #0x3800                 
  11d04:  str r0, [r1, #0x30]               
  11d06:  movs r0, #0                       
  11d08:  str r0, [r1, #0x34]               
  11d0a:  str r0, [r1, #0x40]               
  11d0c:  ldr r0, [pc, #0x74]               
  11d0e:  str r0, [r1, #8]                  
  11d10:  mov r0, r1                        
  11d12:  ldr r0, [r0, #0x1c]               
  11d14:  orr r0, r0, #0x10000000           
  11d18:  str r0, [r1, #0x1c]               
  11d1a:  ldr r0, [pc, #0x6c]               -> периферия
  11d1c:  ldr r0, [r0]                      
  11d1e:  and r0, r0, #0x400                
  11d22:  cmp.w r0, #0x400                  
  11d26:  bne #0x11d42                      
  11d28:  nop                               
  11d2a:  ldr r0, [pc, #0x60]               -> периферия
  11d2c:  ldr r0, [r0]                      
  11d2e:  bic r0, r0, #0x2000000            
  11d32:  ldr r1, [pc, #0x58]               -> периферия
  11d34:  str r0, [r1]                      
  11d36:  mov r0, r1                        
  11d38:  ldr r0, [r0]                      
  11d3a:  orr r0, r0, #0x2000000            
  11d3e:  str r0, [r1]                      
  11d40:  nop                               
  11d42:  ldr r0, [pc, #0x4c]               -> периферия
  11d44:  ldr r0, [r0]                      
  11d46:  orr r0, r0, #0x90                 
  11d4a:  ldr r1, [pc, #0x44]               -> периферия
  11d4c:  str r0, [r1]                      
  11d4e:  mov r0, r1                        
  11d50:  ldr r0, [r0]                      
  11d52:  and r0, r0, #0x100                
  11d56:  cbz r0, #0x11d62                  
  11d58:  mov r0, r1                        
  11d5a:  ldr r0, [r0]                      
  11d5c:  bic r0, r0, #0x200                
  11d60:  str r0, [r1]                      
  11d62:  bl #0x10abc                       -> func_0x10abc
  11d66:  ldr r0, [pc, #0x2c]               -> flash-mirror @0x03000
  11d68:  ldr r1, [pc, #4]                  -> Cortex-M (NVIC/SCB/SysTick)
  11d6a:  subs r1, #0x80                    
  11d6c:  str r0, [r1]                      
  11d6e:  pop {r4, pc}                      
  ; --- literal-пул @0x11d70 (10 слов) — ВНЕ границ функции ---
  11d70:  .word 0xe000ed88  ; Cortex-M (NVIC/SCB/SysTick)
  11d74:  .word 0x40021000  ; периферия
  11d78:  .word 0xf8ffc000
  11d7c:  .word 0xfef6ffff
  11d80:  .word 0x0700ffff
  11d84:  .word 0x04bf8000
  11d88:  .word 0x40007000  ; периферия
  11d8c:  .word 0x40001820  ; периферия
  11d90:  .word 0x40022000  ; периферия
  11d94:  .word 0x08003000  ; flash-mirror @0x03000
```
