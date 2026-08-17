# func_0x19dbc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019dbc) | `0x00019dbc` |
| размер кода | 202 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xfffffc0d — прочее (r1)

## Вызовы (callees)

- 0x19e28 (b, вне списка функций)
- 0x19e30 (b, вне списка функций)
- 0x19e36 (b, вне списка функций)
- 0x19e54 (b, вне списка функций)
- `func_0x1a184` (0x0001a184, bl)

## Кто вызывает (callers / xrefs)

- `func_0x22274` (bl @0x00022318)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x19e24..0x19e30` (12 Б); цели из: 0x19de8, 0x19df0
- `0x19e30..0x19e34` (4 Б); цели из: 0x19e22
- `0x19e34..0x19e36` (2 Б); цели из: 0x19e2e
- `0x19e36..0x19e54` (30 Б); цели из: 0x19e32
- `0x19e54..0x19e86` (50 Б); цели из: 0x19e3c

## Дизассембляция

```asm
  19dbc:  push {r4, r5, r6, r7, lr}         
  19dbe:  push {r0, r1, r2, r3, r4}         
  19dc0:  sub sp, #0x20                     
  19dc2:  ldr r1, [sp, #0x2c]               
  19dc4:  ldr r0, [sp, #0x24]               
  19dc6:  movs r4, #0                       
  19dc8:  eors r0, r1                       
  19dca:  ldr r1, [sp, #0x24]               
  19dcc:  lsrs r0, r0, #0x1f                
  19dce:  lsls r1, r1, #1                   
  19dd0:  lsrs r1, r1, #1                   
  19dd2:  str r1, [sp, #0x24]               
  19dd4:  lsls r0, r0, #0x1f                
  19dd6:  ldr r1, [sp, #0x2c]               
  19dd8:  str r0, [sp]                      
  19dda:  lsls r1, r1, #1                   
  19ddc:  lsrs r1, r1, #1                   
  19dde:  str r1, [sp, #0x2c]               
  19de0:  ldr r1, [sp, #0x24]               
  19de2:  ldr r0, [sp, #0x20]               
  19de4:  mov lr, r4                        
  19de6:  orrs r0, r1                       
  19de8:  beq #0x19e24                      
  19dea:  ldr r1, [sp, #0x2c]               
  19dec:  ldr r0, [sp, #0x28]               
  19dee:  orrs r0, r1                       
  19df0:  beq #0x19e24                      
  19df2:  ldr r0, [sp, #0x24]               
  19df4:  movs r4, #1                       
  19df6:  lsls r0, r0, #1                   
  19df8:  lsrs r2, r0, #0x15                
  19dfa:  lsls r0, r1, #1                   
  19dfc:  lsrs r1, r0, #0x15                
  19dfe:  ldr r0, [sp, #0x24]               
  19e00:  lsls r4, r4, #0x14                
  19e02:  lsls r0, r0, #0xc                 
  19e04:  lsrs r0, r0, #0xc                 
  19e06:  orrs r0, r4                       
  19e08:  str r0, [sp, #0x24]               
  19e0a:  ldr r0, [sp, #0x2c]               
  19e0c:  lsls r0, r0, #0xc                 
  19e0e:  lsrs r0, r0, #0xc                 
  19e10:  orrs r0, r4                       
  19e12:  str r0, [sp, #0x2c]               
  19e14:  adds r0, r2, r1                   
  19e16:  ldr r1, [pc, #0x70]               
  19e18:  adds r0, r0, r1                   
  19e1a:  movs r2, #0                       
  19e1c:  str r0, [sp, #4]                  
  19e1e:  mov r4, r2                        
  19e20:  mov r0, r2                        
  19e22:  b #0x19e30                        -> 0x19e30 (вне списка функций)
  19e24:  movs r0, #0                       
  19e26:  mov r1, r0                        
  19e28:  add sp, #0x34                     
  19e2a:  pop {r4, r5, r6, r7, pc}          
  19e2c:  cmp r0, #3                        
  19e2e:  bge #0x19e34                      
  19e30:  mov r3, r0                        
  19e32:  b #0x19e36                        -> 0x19e36 (вне списка функций)
  19e34:  movs r3, #3                       
  19e36:  mov ip, r3                        
  19e38:  subs r1, r0, r3                   
  19e3a:  add r6, sp, #0x28                 
  19e3c:  b #0x19e54                        -> 0x19e54 (вне списка функций)
  19e3e:  lsls r7, r3, #1                   
  19e40:  add r5, sp, #0x20                 
  19e42:  ldrh r5, [r5, r7]                 
  19e44:  lsls r7, r1, #1                   
  19e46:  ldrh r7, [r6, r7]                 
  19e48:  muls r5, r7, r5                   
  19e4a:  movs r7, #0                       
  19e4c:  adds r2, r5, r2                   
  19e4e:  adcs r4, r7                       
  19e50:  adds r1, r1, #1                   
  19e52:  subs r3, r3, #1                   
  19e54:  cmp r1, ip                        
  19e56:  ble #0x19e3e                      
  19e58:  lsls r1, r0, #1                   
  19e5a:  add r3, sp, #0x10                 
  19e5c:  strh r2, [r3, r1]                 
  19e5e:  lsls r1, r4, #0x10                
  19e60:  lsrs r2, r2, #0x10                
  19e62:  orrs r2, r1                       
  19e64:  lsrs r4, r4, #0x10                
  19e66:  adds r0, r0, #1                   
  19e68:  cmp r0, #8                        
  19e6a:  blt #0x19e2c                      
  19e6c:  ldr r0, [sp, #4]                  
  19e6e:  str r0, [sp, #8]                  
  19e70:  ldr r1, [sp]                      
  19e72:  mov r0, lr                        
  19e74:  str r1, [sp, #4]                  
  19e76:  str r0, [sp]                      
  19e78:  ldr r3, [sp, #0x14]               
  19e7a:  ldr r2, [sp, #0x10]               
  19e7c:  ldr r1, [sp, #0x1c]               
  19e7e:  ldr r0, [sp, #0x18]               
  19e80:  bl #0x1a184                       -> func_0x1a184
  19e84:  b #0x19e28                        -> 0x19e28 (вне списка функций)
  ; --- literal-пул @0x19e88 (1 слов) — ВНЕ границ функции ---
  19e88:  .word 0xfffffc0d
```
