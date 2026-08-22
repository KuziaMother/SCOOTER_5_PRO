# func_0x22d2c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022d2c) | `0x00022d2c` |
| размер кода | 204 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40012c00 — периферия (r4)
- 0x40014000 — периферия (r5)
- 0x40014400 — периферия (r6)
- 0x40014800 — периферия (r2)
- 0x40014c00 — периферия (r2)

## Вызовы (callees)

- 0x22d8a (b, вне списка функций)
- 0x22dc4 (b, вне списка функций)
- 0x22dd2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x23040` (bl @0x0002314a)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x22d7e..0x22d8c` (14 Б); цели из: 0x22d68, 0x22d6c, 0x22d70, 0x22d76
- `0x22d8c..0x22da0` (20 Б); цели из: 0x22d82, 0x22d86
- `0x22da0..0x22db8` (24 Б); цели из: 0x22d7c
- `0x22db8..0x22dc6` (14 Б); цели из: 0x22da2, 0x22da6, 0x22daa, 0x22db0
- `0x22dc6..0x22dd4` (14 Б); цели из: 0x22dbc, 0x22dc0
- `0x22dd4..0x22df0` (28 Б); цели из: 0x22dca, 0x22dce
- `0x22df0..0x22df8` (8 Б); цели из: 0x22db6

## Дизассембляция

```asm
  22d2c:  push {r4, r5, r6, r7, lr}         
  22d2e:  ldr r2, [r0, #0x30]               
  22d30:  lsrs r2, r2, #1                   
  22d32:  lsls r2, r2, #1                   
  22d34:  str r2, [r0, #0x30]               
  22d36:  ldr r2, [r0, #0x28]               
  22d38:  movs r3, #0x70                    
  22d3a:  bics r2, r3                       
  22d3c:  str r2, [r0, #0x28]               
  22d3e:  ldr r2, [r0, #0x28]               
  22d40:  lsrs r2, r2, #2                   
  22d42:  lsls r2, r2, #2                   
  22d44:  str r2, [r0, #0x28]               
  22d46:  ldr r2, [r0, #0x28]               
  22d48:  bics r2, r3                       
  22d4a:  ldrb r3, [r1]                     
  22d4c:  lsls r3, r3, #4                   
  22d4e:  orrs r2, r3                       
  22d50:  str r2, [r0, #0x28]               
  22d52:  ldr r2, [r0, #0x30]               
  22d54:  movs r3, #2                       
  22d56:  bics r2, r3                       
  22d58:  ldrb r3, [r1, #8]                 
  22d5a:  lsls r3, r3, #1                   
  22d5c:  orrs r2, r3                       
  22d5e:  str r2, [r0, #0x30]               
  22d60:  ldr r4, [pc, #0x94]               -> периферия
  22d62:  ldr r5, [pc, #0x98]               -> периферия
  22d64:  ldr r6, [pc, #0x98]               -> периферия
  22d66:  cmp r0, r4                        
  22d68:  beq #0x22d7e                      
  22d6a:  cmp r0, r5                        
  22d6c:  beq #0x22d7e                      
  22d6e:  cmp r0, r6                        
  22d70:  beq #0x22d7e                      
  22d72:  ldr r2, [pc, #0x90]               -> периферия
  22d74:  cmp r0, r2                        
  22d76:  beq #0x22d7e                      
  22d78:  ldr r2, [pc, #0x8c]               -> периферия
  22d7a:  cmp r0, r2                        
  22d7c:  bne #0x22da0                      
  22d7e:  ldrb r2, [r1, #9]                 
  22d80:  cmp r2, #0                        
  22d82:  beq #0x22d8c                      
  22d84:  cmp r2, #1                        
  22d86:  beq #0x22d8c                      
  22d88:  cpsid i                           
  22d8a:  b #0x22d8a                        -> 0x22d8a (вне списка функций)
  22d8c:  ldr r3, [r0, #0x30]               
  22d8e:  movs r7, #8                       
  22d90:  bics r3, r7                       
  22d92:  lsls r2, r2, #3                   
  22d94:  orrs r3, r2                       
  22d96:  str r3, [r0, #0x30]               
  22d98:  ldr r2, [r0, #0x30]               
  22d9a:  movs r3, #4                       
  22d9c:  bics r2, r3                       
  22d9e:  str r2, [r0, #0x30]               
  22da0:  cmp r0, r4                        
  22da2:  beq #0x22db8                      
  22da4:  cmp r0, r5                        
  22da6:  beq #0x22db8                      
  22da8:  cmp r0, r6                        
  22daa:  beq #0x22db8                      
  22dac:  ldr r2, [pc, #0x54]               -> периферия
  22dae:  cmp r0, r2                        
  22db0:  beq #0x22db8                      
  22db2:  ldr r2, [pc, #0x54]               -> периферия
  22db4:  cmp r0, r2                        
  22db6:  bne #0x22df0                      
  22db8:  ldrb r2, [r1, #0xc]               
  22dba:  cmp r2, #0                        
  22dbc:  beq #0x22dc6                      
  22dbe:  cmp r2, #1                        
  22dc0:  beq #0x22dc6                      
  22dc2:  cpsid i                           
  22dc4:  b #0x22dc4                        -> 0x22dc4 (вне списка функций)
  22dc6:  ldrb r2, [r1, #0xb]               
  22dc8:  cmp r2, #0                        
  22dca:  beq #0x22dd4                      
  22dcc:  cmp r2, #1                        
  22dce:  beq #0x22dd4                      
  22dd0:  cpsid i                           
  22dd2:  b #0x22dd2                        -> 0x22dd2 (вне списка функций)
  22dd4:  ldr r3, [r0, #4]                  
  22dd6:  movs r4, #0xff                    
  22dd8:  adds r4, #1                       
  22dda:  bics r3, r4                       
  22ddc:  lsls r2, r2, #8                   
  22dde:  orrs r3, r2                       
  22de0:  str r3, [r0, #4]                  
  22de2:  ldr r2, [r0, #4]                  
  22de4:  lsls r3, r4, #1                   
  22de6:  bics r2, r3                       
  22de8:  ldrb r3, [r1, #0xc]               
  22dea:  lsls r3, r3, #9                   
  22dec:  orrs r2, r3                       
  22dee:  str r2, [r0, #4]                  
  22df0:  ldr r2, [r0, #0x44]               
  22df2:  ldr r1, [r1, #4]                  
  22df4:  str r1, [r0, #0x44]               
  22df6:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x22df8 (5 слов) — ВНЕ границ функции ---
  22df8:  .word 0x40012c00  ; периферия
  22dfc:  .word 0x40014000  ; периферия
  22e00:  .word 0x40014400  ; периферия
  22e04:  .word 0x40014800  ; периферия
  22e08:  .word 0x40014c00  ; периферия
```
