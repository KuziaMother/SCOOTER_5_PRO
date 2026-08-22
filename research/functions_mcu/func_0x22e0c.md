# func_0x22e0c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022e0c) | `0x00022e0c` |
| размер кода | 186 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40012c00 — периферия (r2)
- 0x40014000 — периферия (r2)
- 0x40014400 — периферия (r2)
- 0x40014800 — периферия (r2)
- 0x40014c00 — периферия (r2)

## Вызовы (callees)

- 0x22e56 (b, вне списка функций)
- 0x22e86 (b, вне списка функций)
- 0x22e92 (b, вне списка функций)
- 0x22ea0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x23040` (bl @0x00023150)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x22e58..0x22e6e` (22 Б); цели из: 0x22e4e, 0x22e52
- `0x22e6e..0x22e86` (24 Б); цели из: 0x22e48
- `0x22e86..0x22e94` (14 Б); цели из: 0x22e6c, 0x22e72, 0x22e78, 0x22e7e
- `0x22e94..0x22ea2` (14 Б); цели из: 0x22e8a, 0x22e8e
- `0x22ea2..0x22ebe` (28 Б); цели из: 0x22e98, 0x22e9c
- `0x22ebe..0x22ec6` (8 Б); цели из: 0x22e84

## Дизассембляция

```asm
  22e0c:  push {r4, lr}                     
  22e0e:  ldr r2, [r0, #0x30]               
  22e10:  movs r3, #0x10                    
  22e12:  bics r2, r3                       
  22e14:  str r2, [r0, #0x30]               
  22e16:  ldr r2, [r0, #0x28]               
  22e18:  movs r3, #7                       
  22e1a:  lsls r3, r3, #0xc                 
  22e1c:  bics r2, r3                       
  22e1e:  str r2, [r0, #0x28]               
  22e20:  ldr r2, [r0, #0x28]               
  22e22:  movs r4, #3                       
  22e24:  lsls r4, r4, #8                   
  22e26:  bics r2, r4                       
  22e28:  str r2, [r0, #0x28]               
  22e2a:  ldr r2, [r0, #0x28]               
  22e2c:  bics r2, r3                       
  22e2e:  ldrb r3, [r1]                     
  22e30:  lsls r3, r3, #0xc                 
  22e32:  orrs r2, r3                       
  22e34:  str r2, [r0, #0x28]               
  22e36:  ldr r2, [r0, #0x30]               
  22e38:  movs r3, #0x20                    
  22e3a:  bics r2, r3                       
  22e3c:  ldrb r3, [r1, #8]                 
  22e3e:  lsls r3, r3, #5                   
  22e40:  orrs r2, r3                       
  22e42:  str r2, [r0, #0x30]               
  22e44:  ldr r2, [pc, #0x80]               -> периферия
  22e46:  cmp r0, r2                        
  22e48:  bne #0x22e6e                      
  22e4a:  ldrb r2, [r1, #9]                 
  22e4c:  cmp r2, #0                        
  22e4e:  beq #0x22e58                      
  22e50:  cmp r2, #1                        
  22e52:  beq #0x22e58                      
  22e54:  cpsid i                           
  22e56:  b #0x22e56                        -> 0x22e56 (вне списка функций)
  22e58:  ldr r3, [r0, #0x30]               
  22e5a:  movs r4, #0x80                    
  22e5c:  bics r3, r4                       
  22e5e:  lsls r2, r2, #7                   
  22e60:  orrs r3, r2                       
  22e62:  str r3, [r0, #0x30]               
  22e64:  ldr r2, [r0, #0x30]               
  22e66:  movs r3, #0x40                    
  22e68:  bics r2, r3                       
  22e6a:  str r2, [r0, #0x30]               
  22e6c:  b #0x22e86                        -> 0x22e86 (вне списка функций)
  22e6e:  ldr r2, [pc, #0x5c]               -> периферия
  22e70:  cmp r0, r2                        
  22e72:  beq #0x22e86                      
  22e74:  ldr r2, [pc, #0x58]               -> периферия
  22e76:  cmp r0, r2                        
  22e78:  beq #0x22e86                      
  22e7a:  ldr r2, [pc, #0x58]               -> периферия
  22e7c:  cmp r0, r2                        
  22e7e:  beq #0x22e86                      
  22e80:  ldr r2, [pc, #0x54]               -> периферия
  22e82:  cmp r0, r2                        
  22e84:  bne #0x22ebe                      
  22e86:  ldrb r2, [r1, #0xc]               
  22e88:  cmp r2, #0                        
  22e8a:  beq #0x22e94                      
  22e8c:  cmp r2, #1                        
  22e8e:  beq #0x22e94                      
  22e90:  cpsid i                           
  22e92:  b #0x22e92                        -> 0x22e92 (вне списка функций)
  22e94:  ldrb r2, [r1, #0xb]               
  22e96:  cmp r2, #0                        
  22e98:  beq #0x22ea2                      
  22e9a:  cmp r2, #1                        
  22e9c:  beq #0x22ea2                      
  22e9e:  cpsid i                           
  22ea0:  b #0x22ea0                        -> 0x22ea0 (вне списка функций)
  22ea2:  ldr r3, [r0, #4]                  
  22ea4:  movs r4, #1                       
  22ea6:  lsls r4, r4, #0xa                 
  22ea8:  bics r3, r4                       
  22eaa:  lsls r2, r2, #0xa                 
  22eac:  orrs r3, r2                       
  22eae:  str r3, [r0, #4]                  
  22eb0:  ldr r2, [r0, #4]                  
  22eb2:  lsls r3, r4, #1                   
  22eb4:  bics r2, r3                       
  22eb6:  ldrb r3, [r1, #0xc]               
  22eb8:  lsls r3, r3, #0xb                 
  22eba:  orrs r2, r3                       
  22ebc:  str r2, [r0, #4]                  
  22ebe:  ldr r2, [r0, #0x48]               
  22ec0:  ldr r1, [r1, #4]                  
  22ec2:  str r1, [r0, #0x48]               
  22ec4:  pop {r4, pc}                      
  ; --- literal-пул @0x22ec8 (5 слов) — ВНЕ границ функции ---
  22ec8:  .word 0x40012c00  ; периферия
  22ecc:  .word 0x40014000  ; периферия
  22ed0:  .word 0x40014400  ; периферия
  22ed4:  .word 0x40014800  ; периферия
  22ed8:  .word 0x40014c00  ; периферия
```
