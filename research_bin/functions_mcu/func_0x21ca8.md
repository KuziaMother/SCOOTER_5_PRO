# func_0x21ca8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080021ca8) | `0x00021ca8` |
| размер кода | 364 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40012400 — периферия (r0)

## Вызовы (callees)

- 0x21cb6 (b, вне списка функций)
- 0x21cc4 (b, вне списка функций)
- 0x21cde (b, вне списка функций)
- 0x21cfc (b, вне списка функций)
- 0x21d12 (b, вне списка функций)
- 0x21d1c (b, вне списка функций)
- 0x21d26 (b, вне списка функций)
- 0x21d98 (b, вне списка функций)
- 0x21fb8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1c0b0` (bl @0x0001c0d6)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x21cb8..0x21cc6` (14 Б); цели из: 0x21cb2
- `0x21cc6..0x21ce0` (26 Б); цели из: 0x21cbc, 0x21cc0
- `0x21ce0..0x21cfe` (30 Б); цели из: 0x21cca, 0x21cce, 0x21cd2, 0x21cd6…
- `0x21cfe..0x21d14` (22 Б); цели из: 0x21ce4, 0x21ce8, 0x21cec, 0x21cf0…
- `0x21d14..0x21d1e` (10 Б); цели из: 0x21d02, 0x21d06, 0x21d0a, 0x21d0e
- `0x21d1e..0x21d28` (10 Б); цели из: 0x21d18
- `0x21d28..0x21d38` (16 Б); цели из: 0x21d22
- `0x21d38..0x21de0` (168 Б); цели из: 0x21d32
- `0x21de0..0x21dfa` (26 Б); цели из: 0x21d80
- `0x21dfa..0x21e14` (26 Б); цели из: 0x21d86

## Дизассембляция

```asm
  21ca8:  push {r4, r5, r6, r7, lr}         
  21caa:  mov r4, r0                        
  21cac:  ldr r1, [r0]                      
  21cae:  ldr r0, [pc, #0x164]              -> периферия
  21cb0:  cmp r1, r0                        
  21cb2:  beq #0x21cb8                      
  21cb4:  cpsid i                           
  21cb6:  b #0x21cb6                        -> 0x21cb6 (вне списка функций)
  21cb8:  ldrb r0, [r4, #4]                 
  21cba:  cmp r0, #0                        
  21cbc:  beq #0x21cc6                      
  21cbe:  cmp r0, #1                        
  21cc0:  beq #0x21cc6                      
  21cc2:  cpsid i                           
  21cc4:  b #0x21cc4                        -> 0x21cc4 (вне списка функций)
  21cc6:  ldrb r0, [r4, #0xb]               
  21cc8:  cmp r0, #0                        
  21cca:  beq #0x21ce0                      
  21ccc:  cmp r0, #1                        
  21cce:  beq #0x21ce0                      
  21cd0:  cmp r0, #2                        
  21cd2:  beq #0x21ce0                      
  21cd4:  cmp r0, #3                        
  21cd6:  beq #0x21ce0                      
  21cd8:  cmp r0, #4                        
  21cda:  beq #0x21ce0                      
  21cdc:  cpsid i                           
  21cde:  b #0x21cde                        -> 0x21cde (вне списка функций)
  21ce0:  ldrb r0, [r4, #0xc]               
  21ce2:  cmp r0, #0                        
  21ce4:  beq #0x21cfe                      
  21ce6:  cmp r0, #1                        
  21ce8:  beq #0x21cfe                      
  21cea:  cmp r0, #2                        
  21cec:  beq #0x21cfe                      
  21cee:  cmp r0, #3                        
  21cf0:  beq #0x21cfe                      
  21cf2:  cmp r0, #4                        
  21cf4:  beq #0x21cfe                      
  21cf6:  cmp r0, #5                        
  21cf8:  beq #0x21cfe                      
  21cfa:  cpsid i                           
  21cfc:  b #0x21cfc                        -> 0x21cfc (вне списка функций)
  21cfe:  ldrb r0, [r4, #0xa]               
  21d00:  cmp r0, #3                        
  21d02:  beq #0x21d14                      
  21d04:  cmp r0, #0                        
  21d06:  beq #0x21d14                      
  21d08:  cmp r0, #1                        
  21d0a:  beq #0x21d14                      
  21d0c:  cmp r0, #2                        
  21d0e:  beq #0x21d14                      
  21d10:  cpsid i                           
  21d12:  b #0x21d12                        -> 0x21d12 (вне списка функций)
  21d14:  ldrb r0, [r4, #6]                 
  21d16:  cmp r0, #0xf                      
  21d18:  bls #0x21d1e                      
  21d1a:  cpsid i                           
  21d1c:  b #0x21d1c                        -> 0x21d1c (вне списка функций)
  21d1e:  ldrb r0, [r4, #9]                 
  21d20:  cmp r0, #7                        
  21d22:  bls #0x21d28                      
  21d24:  cpsid i                           
  21d26:  b #0x21d26                        -> 0x21d26 (вне списка функций)
  21d28:  mov r5, r4                        
  21d2a:  adds r5, #0x20                    
  21d2c:  ldrb r0, [r5, #0x19]              
  21d2e:  movs r6, #0                       
  21d30:  cmp r0, #0                        
  21d32:  bne #0x21d38                      
  21d34:  strb r6, [r5, #0x1a]              
  21d36:  strb r6, [r5, #0x18]              
  21d38:  ldr r0, [r1, #0x18]               
  21d3a:  movs r7, #2                       
  21d3c:  orrs r0, r7                       
  21d3e:  str r0, [r1, #0x18]               
  21d40:  mov r0, r4                        
  21d42:  bl #0x21fb8                       -> 0x21fb8 (вне списка функций)
  21d46:  strb r7, [r5, #0x19]              
  21d48:  ldr r1, [r4]                      
  21d4a:  ldr r0, [r1, #0x1c]               
  21d4c:  movs r2, #0x20                    
  21d4e:  bics r0, r2                       
  21d50:  ldrb r2, [r4, #4]                 
  21d52:  lsls r2, r2, #5                   
  21d54:  orrs r0, r2                       
  21d56:  str r0, [r1, #0x1c]               
  21d58:  ldr r1, [r4]                      
  21d5a:  ldr r0, [r1, #0x1c]               
  21d5c:  movs r2, #0x18                    
  21d5e:  bics r0, r2                       
  21d60:  ldrb r2, [r4, #0xa]               
  21d62:  lsls r2, r2, #3                   
  21d64:  orrs r0, r2                       
  21d66:  str r0, [r1, #0x1c]               
  21d68:  ldr r0, [r4]                      
  21d6a:  ldr r1, [r0, #0x20]               
  21d6c:  ldrb r2, [r4, #0xb]               
  21d6e:  lsrs r1, r1, #3                   
  21d70:  lsls r1, r1, #3                   
  21d72:  orrs r1, r2                       
  21d74:  str r1, [r0, #0x20]               
  21d76:  ldrb r3, [r4, #8]                 
  21d78:  movs r1, #7                       
  21d7a:  lsls r0, r7, #0xf                 
  21d7c:  lsls r1, r1, #0x11                
  21d7e:  cmp r3, #1                        
  21d80:  beq #0x21de0                      
  21d82:  lsls r2, r0, #4                   
  21d84:  cmp r3, #2                        
  21d86:  beq #0x21dfa                      
  21d88:  ldr r1, [r4]                      
  21d8a:  ldr r3, [r1, #0x1c]               
  21d8c:  bics r3, r0                       
  21d8e:  str r3, [r1, #0x1c]               
  21d90:  ldr r0, [r4]                      
  21d92:  ldr r1, [r0, #0x1c]               
  21d94:  bics r1, r2                       
  21d96:  str r1, [r0, #0x1c]               
  21d98:  ldr r0, [r4]                      
  21d9a:  ldr r1, [r0, #0x40]               
  21d9c:  ldrb r2, [r4, #6]                 
  21d9e:  lsrs r1, r1, #4                   
  21da0:  lsls r1, r1, #4                   
  21da2:  orrs r1, r2                       
  21da4:  str r1, [r0, #0x40]               
  21da6:  ldr r1, [r4]                      
  21da8:  ldr r0, [r1, #0x1c]               
  21daa:  movs r2, #1                       
  21dac:  lsls r2, r2, #0xd                 
  21dae:  bics r0, r2                       
  21db0:  ldrb r2, [r4, #5]                 
  21db2:  lsls r2, r2, #0xd                 
  21db4:  orrs r0, r2                       
  21db6:  str r0, [r1, #0x1c]               
  21db8:  ldr r0, [pc, #0x58]               -> периферия
  21dba:  adds r0, #0x40                    
  21dbc:  str r6, [r0, #0x3c]               
  21dbe:  ldr r1, [r0, #0x3c]               
  21dc0:  movs r2, #7                       
  21dc2:  lsls r2, r2, #0x18                
  21dc4:  bics r1, r2                       
  21dc6:  ldrb r2, [r4, #0xc]               
  21dc8:  lsls r2, r2, #0x18                
  21dca:  orrs r1, r2                       
  21dcc:  str r1, [r0, #0x3c]               
  21dce:  strb r6, [r5, #0x1a]              
  21dd0:  movs r0, #1                       
  21dd2:  strb r0, [r5, #0x19]              
  21dd4:  ldr r1, [r4]                      
  21dd6:  ldr r2, [r1, #0x18]               
  21dd8:  orrs r2, r0                       
  21dda:  str r2, [r1, #0x18]               
  21ddc:  movs r0, #0                       
  21dde:  pop {r4, r5, r6, r7, pc}          
  21de0:  strb r6, [r4, #5]                 
  21de2:  ldr r2, [r4]                      
  21de4:  ldr r3, [r2, #0x1c]               
  21de6:  orrs r3, r0                       
  21de8:  str r3, [r2, #0x1c]               
  21dea:  ldr r0, [r4]                      
  21dec:  ldr r2, [r0, #0x1c]               
  21dee:  bics r2, r1                       
  21df0:  ldrb r1, [r4, #9]                 
  21df2:  lsls r1, r1, #0x11                
  21df4:  orrs r2, r1                       
  21df6:  str r2, [r0, #0x1c]               
  21df8:  b #0x21d98                        -> 0x21d98 (вне списка функций)
  21dfa:  strb r6, [r4, #5]                 
  21dfc:  ldr r0, [r4]                      
  21dfe:  ldr r3, [r0, #0x1c]               
  21e00:  orrs r3, r2                       
  21e02:  str r3, [r0, #0x1c]               
  21e04:  ldr r2, [r4]                      
  21e06:  ldr r0, [r2, #0x1c]               
  21e08:  bics r0, r1                       
  21e0a:  ldrb r1, [r4, #9]                 
  21e0c:  lsls r1, r1, #0x11                
  21e0e:  orrs r0, r1                       
  21e10:  str r0, [r2, #0x1c]               
  21e12:  b #0x21d98                        -> 0x21d98 (вне списка функций)
  ; --- literal-пул @0x21e14 (1 слов) — ВНЕ границ функции ---
  21e14:  .word 0x40012400  ; периферия
```
