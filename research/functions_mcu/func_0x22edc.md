# func_0x22edc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022edc) | `0x00022edc` |
| размер кода | 188 Б |
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

- 0x22f26 (b, вне списка функций)
- 0x22f58 (b, вне списка функций)
- 0x22f64 (b, вне списка функций)
- 0x22f72 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x23040` (bl @0x00023156)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x22f28..0x22f40` (24 Б); цели из: 0x22f1e, 0x22f22
- `0x22f40..0x22f58` (24 Б); цели из: 0x22f18
- `0x22f58..0x22f66` (14 Б); цели из: 0x22f3e, 0x22f44, 0x22f4a, 0x22f50
- `0x22f66..0x22f74` (14 Б); цели из: 0x22f5c, 0x22f60
- `0x22f74..0x22f90` (28 Б); цели из: 0x22f6a, 0x22f6e
- `0x22f90..0x22f98` (8 Б); цели из: 0x22f56

## Дизассембляция

```asm
  22edc:  push {r4, lr}                     
  22ede:  ldr r2, [r0, #0x30]               
  22ee0:  movs r3, #0xff                    
  22ee2:  adds r3, #1                       
  22ee4:  bics r2, r3                       
  22ee6:  str r2, [r0, #0x30]               
  22ee8:  ldr r2, [r0, #0x2c]               
  22eea:  movs r3, #0x70                    
  22eec:  bics r2, r3                       
  22eee:  str r2, [r0, #0x2c]               
  22ef0:  ldr r2, [r0, #0x2c]               
  22ef2:  lsrs r2, r2, #2                   
  22ef4:  lsls r2, r2, #2                   
  22ef6:  str r2, [r0, #0x2c]               
  22ef8:  ldr r2, [r0, #0x2c]               
  22efa:  bics r2, r3                       
  22efc:  ldrb r3, [r1]                     
  22efe:  lsls r3, r3, #4                   
  22f00:  orrs r2, r3                       
  22f02:  str r2, [r0, #0x2c]               
  22f04:  ldr r2, [r0, #0x30]               
  22f06:  movs r3, #1                       
  22f08:  lsls r3, r3, #9                   
  22f0a:  bics r2, r3                       
  22f0c:  ldrb r3, [r1, #8]                 
  22f0e:  lsls r3, r3, #9                   
  22f10:  orrs r2, r3                       
  22f12:  str r2, [r0, #0x30]               
  22f14:  ldr r2, [pc, #0x80]               -> периферия
  22f16:  cmp r0, r2                        
  22f18:  bne #0x22f40                      
  22f1a:  ldrb r2, [r1, #9]                 
  22f1c:  cmp r2, #0                        
  22f1e:  beq #0x22f28                      
  22f20:  cmp r2, #1                        
  22f22:  beq #0x22f28                      
  22f24:  cpsid i                           
  22f26:  b #0x22f26                        -> 0x22f26 (вне списка функций)
  22f28:  ldr r3, [r0, #0x30]               
  22f2a:  movs r4, #1                       
  22f2c:  lsls r4, r4, #0xb                 
  22f2e:  bics r3, r4                       
  22f30:  lsls r2, r2, #0xb                 
  22f32:  orrs r3, r2                       
  22f34:  str r3, [r0, #0x30]               
  22f36:  ldr r2, [r0, #0x30]               
  22f38:  asrs r3, r4, #1                   
  22f3a:  bics r2, r3                       
  22f3c:  str r2, [r0, #0x30]               
  22f3e:  b #0x22f58                        -> 0x22f58 (вне списка функций)
  22f40:  ldr r2, [pc, #0x58]               -> периферия
  22f42:  cmp r0, r2                        
  22f44:  beq #0x22f58                      
  22f46:  ldr r2, [pc, #0x58]               -> периферия
  22f48:  cmp r0, r2                        
  22f4a:  beq #0x22f58                      
  22f4c:  ldr r2, [pc, #0x54]               -> периферия
  22f4e:  cmp r0, r2                        
  22f50:  beq #0x22f58                      
  22f52:  ldr r2, [pc, #0x54]               -> периферия
  22f54:  cmp r0, r2                        
  22f56:  bne #0x22f90                      
  22f58:  ldrb r2, [r1, #0xc]               
  22f5a:  cmp r2, #0                        
  22f5c:  beq #0x22f66                      
  22f5e:  cmp r2, #1                        
  22f60:  beq #0x22f66                      
  22f62:  cpsid i                           
  22f64:  b #0x22f64                        -> 0x22f64 (вне списка функций)
  22f66:  ldrb r2, [r1, #0xb]               
  22f68:  cmp r2, #0                        
  22f6a:  beq #0x22f74                      
  22f6c:  cmp r2, #1                        
  22f6e:  beq #0x22f74                      
  22f70:  cpsid i                           
  22f72:  b #0x22f72                        -> 0x22f72 (вне списка функций)
  22f74:  ldr r3, [r0, #4]                  
  22f76:  movs r4, #1                       
  22f78:  lsls r4, r4, #0xc                 
  22f7a:  bics r3, r4                       
  22f7c:  lsls r2, r2, #0xc                 
  22f7e:  orrs r3, r2                       
  22f80:  str r3, [r0, #4]                  
  22f82:  ldr r2, [r0, #4]                  
  22f84:  lsls r3, r4, #1                   
  22f86:  bics r2, r3                       
  22f88:  ldrb r3, [r1, #0xc]               
  22f8a:  lsls r3, r3, #0xd                 
  22f8c:  orrs r2, r3                       
  22f8e:  str r2, [r0, #4]                  
  22f90:  ldr r2, [r0, #0x4c]               
  22f92:  ldr r1, [r1, #4]                  
  22f94:  str r1, [r0, #0x4c]               
  22f96:  pop {r4, pc}                      
  ; --- literal-пул @0x22f98 (5 слов) — ВНЕ границ функции ---
  22f98:  .word 0x40012c00  ; периферия
  22f9c:  .word 0x40014000  ; периферия
  22fa0:  .word 0x40014400  ; периферия
  22fa4:  .word 0x40014800  ; периферия
  22fa8:  .word 0x40014c00  ; периферия
```
