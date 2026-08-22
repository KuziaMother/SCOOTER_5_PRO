# func_0x21e18

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080021e18) | `0x00021e18` |
| размер кода | 412 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000fff — данные @0x00fff (r5)

## Вызовы (callees)

- 0x21e24 (b, вне списка функций)
- 0x21e2e (b, вне списка функций)
- 0x21e3a (b, вне списка функций)
- 0x21e44 (b, вне списка функций)
- 0x21e8a (b, вне списка функций)
- 0x21eb4 (b, вне списка функций)
- 0x21f7e (b, вне списка функций)
- 0x21faa (b, вне списка функций)
- 0x21fb0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1c0b0` (bl @0x0001c0f4)
- `func_0x1c0b0` (bl @0x0001c108)
- `func_0x1c0b0` (bl @0x0001c11a)
- `func_0x1c0b0` (bl @0x0001c12c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x21e26..0x21e30` (10 Б); цели из: 0x21e20
- `0x21e30..0x21e3c` (12 Б); цели из: 0x21e2a
- `0x21e3c..0x21e46` (10 Б); цели из: 0x21e36
- `0x21e46..0x21e98` (82 Б); цели из: 0x21e40
- `0x21e98..0x21e9c` (4 Б); цели из: 0x21e86
- `0x21e9c..0x21ede` (66 Б); цели из: 0x21e94
- `0x21ede..0x21eec` (14 Б); цели из: 0x21ea0
- `0x21eec..0x21f12` (38 Б); цели из: 0x21eba
- `0x21f12..0x21f38` (38 Б); цели из: 0x21eee
- `0x21f38..0x21f5e` (38 Б); цели из: 0x21f14
- `0x21f5e..0x21f7e` (32 Б); цели из: 0x21f3a
- `0x21f7e..0x21f92` (20 Б); цели из: 0x21edc, 0x21f10, 0x21f36, 0x21f5c
- `0x21f92..0x21f9a` (8 Б); цели из: 0x21f82
- `0x21f9a..0x21fa2` (8 Б); цели из: 0x21f86
- `0x21fa2..0x21faa` (8 Б); цели из: 0x21f8a
- `0x21faa..0x21fb0` (6 Б); цели из: 0x21f90
- `0x21fb0..0x21fb4` (4 Б); цели из: 0x21f8e, 0x21f98, 0x21fa0, 0x21fa8

## Дизассембляция

```asm
  21e18:  push {r4, r5, r6, lr}             
  21e1a:  ldrb r2, [r1]                     
  21e1c:  movs r4, #0                       
  21e1e:  cmp r2, #0x12                     
  21e20:  bls #0x21e26                      
  21e22:  cpsid i                           
  21e24:  b #0x21e24                        -> 0x21e24 (вне списка функций)
  21e26:  ldrb r3, [r1, #1]                 
  21e28:  cmp r3, #4                        
  21e2a:  bls #0x21e30                      
  21e2c:  cpsid i                           
  21e2e:  b #0x21e2e                        -> 0x21e2e (вне списка функций)
  21e30:  ldr r5, [pc, #0x180]              -> данные @0x00fff
  21e32:  ldr r2, [r1, #8]                  
  21e34:  cmp r2, r5                        
  21e36:  bls #0x21e3c                      
  21e38:  cpsid i                           
  21e3a:  b #0x21e3a                        -> 0x21e3a (вне списка функций)
  21e3c:  ldrb r2, [r1, #0xc]               
  21e3e:  cmp r2, #3                        
  21e40:  bls #0x21e46                      
  21e42:  cpsid i                           
  21e44:  b #0x21e44                        -> 0x21e44 (вне списка функций)
  21e46:  ldr r2, [r0]                      
  21e48:  ldr r5, [r2, #0x54]               
  21e4a:  movs r6, #6                       
  21e4c:  muls r3, r6, r3                   
  21e4e:  movs r6, #0x1f                    
  21e50:  adds r3, r3, #2                   
  21e52:  lsls r6, r3                       
  21e54:  bics r5, r6                       
  21e56:  str r5, [r2, #0x54]               
  21e58:  ldrb r2, [r1, #1]                 
  21e5a:  movs r5, #6                       
  21e5c:  ldrb r3, [r1]                     
  21e5e:  muls r2, r5, r2                   
  21e60:  adds r2, r2, #2                   
  21e62:  lsls r3, r2                       
  21e64:  ldr r2, [r0]                      
  21e66:  ldr r5, [r2, #0x54]               
  21e68:  orrs r3, r5                       
  21e6a:  str r3, [r2, #0x54]               
  21e6c:  ldr r2, [r0]                      
  21e6e:  ldr r3, [r2, #0x54]               
  21e70:  ldrb r5, [r1, #0xc]               
  21e72:  lsrs r3, r3, #2                   
  21e74:  lsls r3, r3, #2                   
  21e76:  orrs r3, r5                       
  21e78:  str r3, [r2, #0x54]               
  21e7a:  ldrb r2, [r1, #0xd]               
  21e7c:  movs r3, #1                       
  21e7e:  lsls r3, r3, #0x19                
  21e80:  cmp r2, #1                        
  21e82:  ldr r2, [r0]                      
  21e84:  ldr r5, [r2, #0x1c]               
  21e86:  beq #0x21e98                      
  21e88:  bics r5, r3                       
  21e8a:  str r5, [r2, #0x1c]               
  21e8c:  ldrb r2, [r0, #8]                 
  21e8e:  movs r3, #1                       
  21e90:  movs r5, #8                       
  21e92:  cmp r2, #2                        
  21e94:  beq #0x21e9c                      
  21e96:  b #0x21eb4                        -> 0x21eb4 (вне списка функций)
  21e98:  orrs r5, r3                       
  21e9a:  b #0x21e8a                        -> 0x21e8a (вне списка функций)
  21e9c:  ldrb r2, [r1, #0xd]               
  21e9e:  cmp r2, #0                        
  21ea0:  beq #0x21ede                      
  21ea2:  mov r2, r0                        
  21ea4:  adds r2, #0x20                    
  21ea6:  ldrb r4, [r2, #0x19]              
  21ea8:  orrs r4, r5                       
  21eaa:  strb r4, [r2, #0x19]              
  21eac:  ldrb r4, [r2, #0x1a]              
  21eae:  orrs r4, r3                       
  21eb0:  strb r4, [r2, #0x1a]              
  21eb2:  movs r4, #1                       
  21eb4:  ldrb r3, [r1]                     
  21eb6:  movs r2, #0xff                    
  21eb8:  cmp r3, #2                        
  21eba:  bhi #0x21eec                      
  21ebc:  lsls r3, r3, #3                   
  21ebe:  adds r3, #8                       
  21ec0:  lsls r2, r3                       
  21ec2:  ldr r3, [r0]                      
  21ec4:  ldr r5, [r3, #0x20]               
  21ec6:  bics r5, r2                       
  21ec8:  str r5, [r3, #0x20]               
  21eca:  ldrb r2, [r1]                     
  21ecc:  ldr r3, [r1, #4]                  
  21ece:  lsls r2, r2, #3                   
  21ed0:  adds r2, #8                       
  21ed2:  lsls r3, r2                       
  21ed4:  ldr r2, [r0]                      
  21ed6:  ldr r5, [r2, #0x20]               
  21ed8:  orrs r3, r5                       
  21eda:  str r3, [r2, #0x20]               
  21edc:  b #0x21f7e                        -> 0x21f7e (вне списка функций)
  21ede:  ldr r2, [r0]                      
  21ee0:  ldr r3, [r2, #0x1c]               
  21ee2:  movs r5, #1                       
  21ee4:  lsls r5, r5, #0x14                
  21ee6:  orrs r3, r5                       
  21ee8:  str r3, [r2, #0x1c]               
  21eea:  b #0x21eb4                        -> 0x21eb4 (вне списка функций)
  21eec:  cmp r3, #6                        
  21eee:  bhi #0x21f12                      
  21ef0:  lsls r3, r3, #3                   
  21ef2:  subs r3, #0x18                    
  21ef4:  lsls r2, r3                       
  21ef6:  ldr r3, [r0]                      
  21ef8:  ldr r5, [r3, #0x24]               
  21efa:  bics r5, r2                       
  21efc:  str r5, [r3, #0x24]               
  21efe:  ldrb r2, [r1]                     
  21f00:  ldr r3, [r1, #4]                  
  21f02:  lsls r2, r2, #3                   
  21f04:  subs r2, #0x18                    
  21f06:  lsls r3, r2                       
  21f08:  ldr r2, [r0]                      
  21f0a:  ldr r5, [r2, #0x24]               
  21f0c:  orrs r3, r5                       
  21f0e:  str r3, [r2, #0x24]               
  21f10:  b #0x21f7e                        -> 0x21f7e (вне списка функций)
  21f12:  cmp r3, #0xa                      
  21f14:  bhi #0x21f38                      
  21f16:  lsls r3, r3, #3                   
  21f18:  subs r3, #0x18                    
  21f1a:  lsls r2, r3                       
  21f1c:  ldr r3, [r0]                      
  21f1e:  ldr r5, [r3, #0x28]               
  21f20:  bics r5, r2                       
  21f22:  str r5, [r3, #0x28]               
  21f24:  ldrb r2, [r1]                     
  21f26:  ldr r3, [r1, #4]                  
  21f28:  lsls r2, r2, #3                   
  21f2a:  subs r2, #0x18                    
  21f2c:  lsls r3, r2                       
  21f2e:  ldr r2, [r0]                      
  21f30:  ldr r5, [r2, #0x28]               
  21f32:  orrs r3, r5                       
  21f34:  str r3, [r2, #0x28]               
  21f36:  b #0x21f7e                        -> 0x21f7e (вне списка функций)
  21f38:  cmp r3, #0xe                      
  21f3a:  bhi #0x21f5e                      
  21f3c:  lsls r3, r3, #3                   
  21f3e:  subs r3, #0x18                    
  21f40:  lsls r2, r3                       
  21f42:  ldr r3, [r0]                      
  21f44:  ldr r5, [r3, #0x2c]               
  21f46:  bics r5, r2                       
  21f48:  str r5, [r3, #0x2c]               
  21f4a:  ldrb r2, [r1]                     
  21f4c:  lsls r3, r2, #3                   
  21f4e:  ldr r2, [r1, #4]                  
  21f50:  subs r3, #0x18                    
  21f52:  lsls r2, r3                       
  21f54:  ldr r3, [r0]                      
  21f56:  ldr r5, [r3, #0x2c]               
  21f58:  orrs r2, r5                       
  21f5a:  str r2, [r3, #0x2c]               
  21f5c:  b #0x21f7e                        -> 0x21f7e (вне списка функций)
  21f5e:  lsls r3, r3, #3                   
  21f60:  subs r3, #0x18                    
  21f62:  lsls r2, r3                       
  21f64:  ldr r3, [r0]                      
  21f66:  ldr r5, [r3, #0x30]               
  21f68:  bics r5, r2                       
  21f6a:  str r5, [r3, #0x30]               
  21f6c:  ldrb r2, [r1]                     
  21f6e:  ldr r3, [r1, #4]                  
  21f70:  lsls r2, r2, #3                   
  21f72:  subs r2, #0x18                    
  21f74:  lsls r3, r2                       
  21f76:  ldr r2, [r0]                      
  21f78:  ldr r5, [r2, #0x30]               
  21f7a:  orrs r3, r5                       
  21f7c:  str r3, [r2, #0x30]               
  21f7e:  ldrb r2, [r1, #1]                 
  21f80:  cmp r2, #1                        
  21f82:  beq #0x21f92                      
  21f84:  cmp r2, #2                        
  21f86:  beq #0x21f9a                      
  21f88:  cmp r2, #3                        
  21f8a:  beq #0x21fa2                      
  21f8c:  cmp r2, #4                        
  21f8e:  bne #0x21fb0                      
  21f90:  b #0x21faa                        -> 0x21faa (вне списка функций)
  21f92:  ldr r0, [r0]                      
  21f94:  ldr r1, [r1, #8]                  
  21f96:  str r1, [r0, #0x58]               
  21f98:  b #0x21fb0                        -> 0x21fb0 (вне списка функций)
  21f9a:  ldr r0, [r0]                      
  21f9c:  ldr r1, [r1, #8]                  
  21f9e:  str r1, [r0, #0x5c]               
  21fa0:  b #0x21fb0                        -> 0x21fb0 (вне списка функций)
  21fa2:  ldr r0, [r0]                      
  21fa4:  ldr r1, [r1, #8]                  
  21fa6:  str r1, [r0, #0x60]               
  21fa8:  b #0x21fb0                        -> 0x21fb0 (вне списка функций)
  21faa:  ldr r0, [r0]                      
  21fac:  ldr r1, [r1, #8]                  
  21fae:  str r1, [r0, #0x64]               
  21fb0:  mov r0, r4                        
  21fb2:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x21fb4 (1 слов) — ВНЕ границ функции ---
  21fb4:  .word 0x00000fff  ; данные @0x00fff
```
