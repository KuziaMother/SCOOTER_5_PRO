# func_0x19c58

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019c58) | `0x00019c58` |
| размер кода | 328 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xffe00000 — прочее (r2)

## Вызовы (callees)

- 0x19d20 (b, вне списка функций)
- 0x19d7a (b, вне списка функций)
- 0x19d7e (b, вне списка функций)
- 0x19d86 (b, вне списка функций)
- `func_0x1a080` (0x0001a080, bl)
- `func_0x1a0c2` (0x0001a0c2, bl)
- `func_0x1a16a` (0x0001a16a, bl)
- `func_0x1a184` (0x0001a184, bl)

## Кто вызывает (callers / xrefs)

- `func_0x22274` (bl @0x000222f2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x19c82..0x19cc0` (62 Б); цели из: 0x19c74
- `0x19cc0..0x19d24` (100 Б); цели из: 0x19cb2
- `0x19d24..0x19d2a` (6 Б); цели из: 0x19c88
- `0x19d2a..0x19d52` (40 Б); цели из: 0x19cfc
- `0x19d52..0x19d7a` (40 Б); цели из: 0x19cf4
- `0x19d7a..0x19d86` (12 Б); цели из: 0x19cee, 0x19d50
- `0x19d86..0x19da0` (26 Б); цели из: 0x19c9e, 0x19d84

## Дизассембляция

```asm
  19c58:  push {r4, r5, r6, r7, lr}         
  19c5a:  mov r7, r0                        
  19c5c:  mov r0, r1                        
  19c5e:  eors r0, r3                       
  19c60:  sub sp, #0x1c                     
  19c62:  lsrs r0, r0, #0x1f                
  19c64:  str r0, [sp, #0x10]               
  19c66:  lsls r0, r1, #1                   
  19c68:  mov r6, r1                        
  19c6a:  lsls r1, r3, #1                   
  19c6c:  lsrs r0, r0, #1                   
  19c6e:  lsrs r1, r1, #1                   
  19c70:  subs r4, r7, r2                   
  19c72:  sbcs r0, r1                       
  19c74:  bhs #0x19c82                      
  19c76:  mov r0, r7                        
  19c78:  mov r1, r6                        
  19c7a:  mov r6, r3                        
  19c7c:  mov r7, r2                        
  19c7e:  mov r3, r1                        
  19c80:  mov r2, r0                        
  19c82:  lsls r0, r3, #1                   
  19c84:  lsrs r0, r0, #1                   
  19c86:  orrs r0, r2                       
  19c88:  beq #0x19d24                      
  19c8a:  lsrs r0, r6, #0x14                
  19c8c:  str r0, [sp, #0xc]                
  19c8e:  lsls r0, r0, #0x15                
  19c90:  lsls r1, r3, #1                   
  19c92:  lsrs r0, r0, #0x15                
  19c94:  lsrs r1, r1, #0x15                
  19c96:  str r0, [sp, #0x14]               
  19c98:  subs r0, r0, r1                   
  19c9a:  str r0, [sp, #8]                  
  19c9c:  cmp r0, #0x40                     
  19c9e:  bge #0x19d86                      
  19ca0:  lsls r0, r3, #0xc                 
  19ca2:  movs r1, #1                       
  19ca4:  lsrs r0, r0, #0xc                 
  19ca6:  lsls r1, r1, #0x14                
  19ca8:  orrs r0, r1                       
  19caa:  str r0, [sp, #4]                  
  19cac:  ldr r0, [sp, #0x10]               
  19cae:  str r2, [sp]                      
  19cb0:  cmp r0, #0                        
  19cb2:  beq #0x19cc0                      
  19cb4:  ldr r1, [sp, #4]                  
  19cb6:  rsbs r2, r2, #0                   
  19cb8:  movs r0, #0                       
  19cba:  sbcs r0, r1                       
  19cbc:  str r2, [sp]                      
  19cbe:  str r0, [sp, #4]                  
  19cc0:  ldr r0, [sp, #8]                  
  19cc2:  movs r1, #0x40                    
  19cc4:  subs r2, r1, r0                   
  19cc6:  ldr r1, [sp, #4]                  
  19cc8:  ldr r0, [sp]                      
  19cca:  bl #0x1a080                       -> func_0x1a080
  19cce:  mov r5, r0                        
  19cd0:  mov r4, r1                        
  19cd2:  mov r3, sp                        
  19cd4:  ldm r3!, {r0, r1, r2}             
  19cd6:  bl #0x1a0c2                       -> func_0x1a0c2
  19cda:  adds r0, r0, r7                   
  19cdc:  adcs r1, r6                       
  19cde:  ldr r2, [sp, #0xc]                
  19ce0:  lsrs r6, r1, #0x14                
  19ce2:  movs r3, #0                       
  19ce4:  asrs r7, r2, #0x1f                
  19ce6:  eors r6, r2                       
  19ce8:  mov r2, r3                        
  19cea:  eors r2, r7                       
  19cec:  orrs r6, r2                       
  19cee:  beq #0x19d7a                      
  19cf0:  ldr r2, [sp, #0x10]               
  19cf2:  cmp r2, #0                        
  19cf4:  beq #0x19d52                      
  19cf6:  ldr r2, [sp, #8]                  
  19cf8:  cmp r2, #1                        
  19cfa:  ldr r2, [sp, #0xc]                
  19cfc:  bgt #0x19d2a                      
  19cfe:  lsls r2, r2, #0x14                
  19d00:  subs r0, r0, r3                   
  19d02:  sbcs r1, r2                       
  19d04:  movs r6, #1                       
  19d06:  lsls r6, r6, #0x14                
  19d08:  adds r0, r0, #0                   
  19d0a:  adcs r1, r6                       
  19d0c:  lsrs r2, r2, #0x1f                
  19d0e:  ldr r6, [sp, #0x14]               
  19d10:  lsls r2, r2, #0x1f                
  19d12:  str r3, [sp]                      
  19d14:  str r2, [sp, #4]                  
  19d16:  str r6, [sp, #8]                  
  19d18:  mov r2, r5                        
  19d1a:  mov r3, r4                        
  19d1c:  bl #0x1a184                       -> func_0x1a184
  19d20:  add sp, #0x1c                     
  19d22:  pop {r4, r5, r6, r7, pc}          
  19d24:  mov r0, r7                        
  19d26:  mov r1, r6                        
  19d28:  b #0x19d20                        -> 0x19d20 (вне списка функций)
  19d2a:  lsls r6, r2, #0x14                
  19d2c:  ldr r2, [pc, #0x88]               
  19d2e:  mov r7, r1                        
  19d30:  adds r2, r6, r2                   
  19d32:  subs r0, r0, r3                   
  19d34:  sbcs r7, r6                       
  19d36:  movs r1, #1                       
  19d38:  lsls r1, r1, #0x14                
  19d3a:  adds r0, r0, #0                   
  19d3c:  adcs r7, r1                       
  19d3e:  adds r0, r0, r0                   
  19d40:  adcs r7, r7                       
  19d42:  mov r1, r2                        
  19d44:  adds r0, r3, r0                   
  19d46:  adcs r1, r7                       
  19d48:  lsrs r2, r4, #0x1f                
  19d4a:  orrs r0, r2                       
  19d4c:  adds r5, r5, r5                   
  19d4e:  adcs r4, r4                       
  19d50:  b #0x19d7a                        -> 0x19d7a (вне списка функций)
  19d52:  lsls r2, r4, #0x1f                
  19d54:  lsrs r5, r5, #1                   
  19d56:  orrs r5, r2                       
  19d58:  lsrs r4, r4, #1                   
  19d5a:  lsls r2, r0, #0x1f                
  19d5c:  orrs r4, r2                       
  19d5e:  ldr r2, [sp, #0xc]                
  19d60:  movs r6, #1                       
  19d62:  lsls r2, r2, #0x14                
  19d64:  subs r0, r0, r3                   
  19d66:  sbcs r1, r2                       
  19d68:  lsls r6, r6, #0x14                
  19d6a:  adds r0, r0, #0                   
  19d6c:  adcs r1, r6                       
  19d6e:  lsls r6, r1, #0x1f                
  19d70:  lsrs r0, r0, #1                   
  19d72:  orrs r0, r6                       
  19d74:  lsrs r1, r1, #1                   
  19d76:  adds r0, r0, r3                   
  19d78:  adcs r1, r2                       
  19d7a:  mov r2, r5                        
  19d7c:  mov r3, r4                        
  19d7e:  bl #0x1a16a                       -> func_0x1a16a
  19d82:  b #0x19d20                        -> 0x19d20 (вне списка функций)
  19d84:  b #0x19d86                        -> 0x19d86 (вне списка функций)
  19d86:  ldr r0, [sp, #0x10]               
  19d88:  movs r2, #1                       
  19d8a:  lsls r0, r0, #1                   
  19d8c:  asrs r1, r0, #0x1f                
  19d8e:  subs r2, r2, r0                   
  19d90:  movs r3, #0                       
  19d92:  sbcs r3, r1                       
  19d94:  ldr r0, [sp, #0x10]               
  19d96:  mov r1, r6                        
  19d98:  asrs r4, r0, #0x1f                
  19d9a:  subs r0, r7, r0                   
  19d9c:  sbcs r1, r4                       
  19d9e:  b #0x19d7e                        -> 0x19d7e (вне списка функций)
  ; --- literal-пул @0x19db8 (1 слов) — ВНЕ границ функции ---
  19db8:  .word 0xffe00000
```
