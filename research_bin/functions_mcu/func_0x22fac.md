# func_0x22fac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022fac) | `0x00022fac` |
| размер кода | 126 Б |
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

- 0x23012 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x23040` (bl @0x0002315c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x23006..0x23014` (14 Б); цели из: 0x22fec, 0x22ff2, 0x22ff8, 0x22ffe
- `0x23014..0x23022` (14 Б); цели из: 0x2300a, 0x2300e
- `0x23022..0x2302a` (8 Б); цели из: 0x23004

## Дизассембляция

```asm
  22fac:  push {r4, lr}                     
  22fae:  ldr r2, [r0, #0x30]               
  22fb0:  movs r3, #1                       
  22fb2:  lsls r3, r3, #0xc                 
  22fb4:  bics r2, r3                       
  22fb6:  str r2, [r0, #0x30]               
  22fb8:  ldr r2, [r0, #0x2c]               
  22fba:  movs r3, #7                       
  22fbc:  lsls r3, r3, #0xc                 
  22fbe:  bics r2, r3                       
  22fc0:  str r2, [r0, #0x2c]               
  22fc2:  ldr r2, [r0, #0x2c]               
  22fc4:  movs r4, #3                       
  22fc6:  lsls r4, r4, #8                   
  22fc8:  bics r2, r4                       
  22fca:  str r2, [r0, #0x2c]               
  22fcc:  ldr r2, [r0, #0x2c]               
  22fce:  bics r2, r3                       
  22fd0:  ldrb r3, [r1]                     
  22fd2:  lsls r3, r3, #0xc                 
  22fd4:  orrs r2, r3                       
  22fd6:  str r2, [r0, #0x2c]               
  22fd8:  ldr r2, [r0, #0x30]               
  22fda:  movs r3, #1                       
  22fdc:  lsls r3, r3, #0xd                 
  22fde:  bics r2, r3                       
  22fe0:  ldrb r3, [r1, #8]                 
  22fe2:  lsls r3, r3, #0xd                 
  22fe4:  orrs r2, r3                       
  22fe6:  str r2, [r0, #0x30]               
  22fe8:  ldr r2, [pc, #0x40]               -> периферия
  22fea:  cmp r0, r2                        
  22fec:  beq #0x23006                      
  22fee:  ldr r2, [pc, #0x40]               -> периферия
  22ff0:  cmp r0, r2                        
  22ff2:  beq #0x23006                      
  22ff4:  ldr r2, [pc, #0x3c]               -> периферия
  22ff6:  cmp r0, r2                        
  22ff8:  beq #0x23006                      
  22ffa:  ldr r2, [pc, #0x3c]               -> периферия
  22ffc:  cmp r0, r2                        
  22ffe:  beq #0x23006                      
  23000:  ldr r2, [pc, #0x38]               -> периферия
  23002:  cmp r0, r2                        
  23004:  bne #0x23022                      
  23006:  ldrb r2, [r1, #0xb]               
  23008:  cmp r2, #0                        
  2300a:  beq #0x23014                      
  2300c:  cmp r2, #1                        
  2300e:  beq #0x23014                      
  23010:  cpsid i                           
  23012:  b #0x23012                        -> 0x23012 (вне списка функций)
  23014:  ldr r3, [r0, #4]                  
  23016:  movs r4, #1                       
  23018:  lsls r4, r4, #0xe                 
  2301a:  bics r3, r4                       
  2301c:  lsls r2, r2, #0xe                 
  2301e:  orrs r3, r2                       
  23020:  str r3, [r0, #4]                  
  23022:  ldr r2, [r0, #0x50]               
  23024:  ldr r1, [r1, #4]                  
  23026:  str r1, [r0, #0x50]               
  23028:  pop {r4, pc}                      
  ; --- literal-пул @0x2302c (5 слов) — ВНЕ границ функции ---
  2302c:  .word 0x40012c00  ; периферия
  23030:  .word 0x40014000  ; периферия
  23034:  .word 0x40014400  ; периферия
  23038:  .word 0x40014800  ; периферия
  2303c:  .word 0x40014c00  ; периферия
```
