# func_0x19e8c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019e8c) | `0x00019e8c` |
| размер кода | 234 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000003fd — данные @0x003fd (r1)

## Вызовы (callees)

- 0x19eee (b, вне списка функций)
- 0x19ef6 (b, вне списка функций)
- 0x19f2a (b, вне списка функций)
- 0x19f5e (b, вне списка функций)
- `func_0x1a16a` (0x0001a16a, bl)

## Кто вызывает (callers / xrefs)

- `func_0x22274` (bl @0x00022320)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x19ee8..0x19eee` (6 Б); цели из: 0x19ede
- `0x19eee..0x19ef2` (4 Б); цели из: 0x19ee6
- `0x19ef2..0x19efa` (8 Б); цели из: 0x19eac, 0x19eb2
- `0x19efa..0x19f1e` (36 Б); цели из: 0x19ef0
- `0x19f1e..0x19f2a` (12 Б); цели из: 0x19f0e
- `0x19f2a..0x19f50` (38 Б); цели из: 0x19f04
- `0x19f50..0x19f58` (8 Б); цели из: 0x19f40
- `0x19f58..0x19f5e` (6 Б); цели из: 0x19f48
- `0x19f5e..0x19f76` (24 Б); цели из: 0x19f34, 0x19f4e, 0x19f56

## Дизассембляция

```asm
  19e8c:  push {r4, r5, r6, r7, lr}         
  19e8e:  mov r4, r1                        
  19e90:  eors r4, r3                       
  19e92:  sub sp, #0x14                     
  19e94:  lsrs r4, r4, #0x1f                
  19e96:  lsls r4, r4, #0x1f                
  19e98:  str r4, [sp, #0xc]                
  19e9a:  lsls r4, r1, #1                   
  19e9c:  movs r6, #0                       
  19e9e:  lsrs r4, r4, #1                   
  19ea0:  lsls r1, r3, #1                   
  19ea2:  mov ip, r2                        
  19ea4:  lsrs r1, r1, #1                   
  19ea6:  mov r2, r0                        
  19ea8:  str r6, [sp, #8]                  
  19eaa:  orrs r2, r4                       
  19eac:  beq #0x19ef2                      
  19eae:  mov r2, ip                        
  19eb0:  orrs r2, r1                       
  19eb2:  beq #0x19ef2                      
  19eb4:  lsls r2, r4, #1                   
  19eb6:  lsrs r7, r2, #0x15                
  19eb8:  lsls r2, r1, #1                   
  19eba:  lsls r6, r1, #0xc                 
  19ebc:  lsls r3, r4, #0xc                 
  19ebe:  lsrs r5, r2, #0x15                
  19ec0:  movs r4, #1                       
  19ec2:  mov r2, r0                        
  19ec4:  ldr r1, [pc, #0xb0]               -> данные @0x003fd
  19ec6:  lsls r4, r4, #0x14                
  19ec8:  subs r0, r7, r5                   
  19eca:  lsrs r3, r3, #0xc                 
  19ecc:  lsrs r6, r6, #0xc                 
  19ece:  adds r0, r0, r1                   
  19ed0:  orrs r3, r4                       
  19ed2:  orrs r6, r4                       
  19ed4:  mov r1, ip                        
  19ed6:  str r0, [sp]                      
  19ed8:  mov r4, r3                        
  19eda:  subs r0, r2, r1                   
  19edc:  sbcs r4, r6                       
  19ede:  blo #0x19ee8                      
  19ee0:  ldr r0, [sp]                      
  19ee2:  adds r0, r0, #1                   
  19ee4:  str r0, [sp]                      
  19ee6:  b #0x19eee                        -> 0x19eee (вне списка функций)
  19ee8:  adds r2, r2, r2                   
  19eea:  ldr r0, [sp]                      
  19eec:  adcs r3, r3                       
  19eee:  cmp r0, #0                        
  19ef0:  bge #0x19efa                      
  19ef2:  movs r0, #0                       
  19ef4:  mov r1, r0                        
  19ef6:  add sp, #0x14                     
  19ef8:  pop {r4, r5, r6, r7, pc}          
  19efa:  movs r0, #0                       
  19efc:  movs r1, #1                       
  19efe:  lsls r1, r1, #0x14                
  19f00:  mov r7, r0                        
  19f02:  mov lr, r0                        
  19f04:  b #0x19f2a                        -> 0x19f2a (вне списка функций)
  19f06:  mov r4, ip                        
  19f08:  mov r5, r3                        
  19f0a:  subs r4, r2, r4                   
  19f0c:  sbcs r5, r6                       
  19f0e:  blo #0x19f1e                      
  19f10:  mov r5, ip                        
  19f12:  subs r2, r2, r5                   
  19f14:  sbcs r3, r6                       
  19f16:  mov r4, lr                        
  19f18:  orrs r7, r0                       
  19f1a:  orrs r4, r1                       
  19f1c:  mov lr, r4                        
  19f1e:  lsls r5, r1, #0x1f                
  19f20:  lsrs r0, r0, #1                   
  19f22:  lsrs r1, r1, #1                   
  19f24:  orrs r0, r5                       
  19f26:  adds r2, r2, r2                   
  19f28:  adcs r3, r3                       
  19f2a:  mov r5, r0                        
  19f2c:  orrs r5, r1                       
  19f2e:  bne #0x19f06                      
  19f30:  mov r0, r2                        
  19f32:  orrs r0, r3                       
  19f34:  beq #0x19f5e                      
  19f36:  mov r0, ip                        
  19f38:  mov r1, r3                        
  19f3a:  eors r0, r2                       
  19f3c:  eors r1, r6                       
  19f3e:  orrs r0, r1                       
  19f40:  beq #0x19f50                      
  19f42:  mov r0, ip                        
  19f44:  subs r0, r2, r0                   
  19f46:  sbcs r3, r6                       
  19f48:  bhs #0x19f58                      
  19f4a:  movs r2, #1                       
  19f4c:  movs r3, #0                       
  19f4e:  b #0x19f5e                        -> 0x19f5e (вне списка функций)
  19f50:  movs r2, #0                       
  19f52:  movs r3, #1                       
  19f54:  lsls r3, r3, #0x1f                
  19f56:  b #0x19f5e                        -> 0x19f5e (вне списка функций)
  19f58:  movs r2, #1                       
  19f5a:  mvns r2, r2                       
  19f5c:  asrs r3, r2, #1                   
  19f5e:  ldr r0, [sp]                      
  19f60:  mov r4, lr                        
  19f62:  lsls r1, r0, #0x14                
  19f64:  adds r0, r7, #0                   
  19f66:  adcs r1, r4                       
  19f68:  ldr r4, [sp, #8]                  
  19f6a:  ldr r5, [sp, #0xc]                
  19f6c:  adds r0, r0, r4                   
  19f6e:  adcs r1, r5                       
  19f70:  bl #0x1a16a                       -> func_0x1a16a
  19f74:  b #0x19ef6                        -> 0x19ef6 (вне списка функций)
  ; --- literal-пул @0x19f78 (1 слов) — ВНЕ границ функции ---
  19f78:  .word 0x000003fd  ; данные @0x003fd
```
