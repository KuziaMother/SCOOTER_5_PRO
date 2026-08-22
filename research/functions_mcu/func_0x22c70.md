# func_0x22c70

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022c70) | `0x00022c70` |
| размер кода | 168 Б |
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

- 0x22c94 (b, вне списка функций)
- 0x22caa (b, вне списка функций)
- 0x22cb4 (b, вне списка функций)
- 0x22cc2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1d640` (bl @0x0001d76c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x22c96..0x22cac` (22 Б); цели из: 0x22c78, 0x22c7e, 0x22c84, 0x22c8a…
- `0x22cac..0x22cb6` (10 Б); цели из: 0x22c9a, 0x22c9e, 0x22ca2, 0x22ca6
- `0x22cb6..0x22cc4` (14 Б); цели из: 0x22cb0
- `0x22cc4..0x22d18` (84 Б); цели из: 0x22cba, 0x22cbe

## Дизассембляция

```asm
  22c70:  push {r4, r5, r6, r7, lr}         
  22c72:  ldr r2, [pc, #0xa4]               -> периферия
  22c74:  ldr r3, [r0]                      
  22c76:  cmp r3, r2                        
  22c78:  beq #0x22c96                      
  22c7a:  ldr r2, [pc, #0xa0]               -> периферия
  22c7c:  cmp r3, r2                        
  22c7e:  beq #0x22c96                      
  22c80:  ldr r2, [pc, #0x9c]               -> периферия
  22c82:  cmp r3, r2                        
  22c84:  beq #0x22c96                      
  22c86:  ldr r2, [pc, #0x9c]               -> периферия
  22c88:  cmp r3, r2                        
  22c8a:  beq #0x22c96                      
  22c8c:  ldr r2, [pc, #0x98]               -> периферия
  22c8e:  cmp r3, r2                        
  22c90:  beq #0x22c96                      
  22c92:  cpsid i                           
  22c94:  b #0x22c94                        -> 0x22c94 (вне списка функций)
  22c96:  ldrb r4, [r1, #2]                 
  22c98:  cmp r4, #0                        
  22c9a:  beq #0x22cac                      
  22c9c:  cmp r4, #1                        
  22c9e:  beq #0x22cac                      
  22ca0:  cmp r4, #2                        
  22ca2:  beq #0x22cac                      
  22ca4:  cmp r4, #3                        
  22ca6:  beq #0x22cac                      
  22ca8:  cpsid i                           
  22caa:  b #0x22caa                        -> 0x22caa (вне списка функций)
  22cac:  ldr r6, [r1, #4]                  
  22cae:  cmp r6, #0xff                     
  22cb0:  bls #0x22cb6                      
  22cb2:  cpsid i                           
  22cb4:  b #0x22cb4                        -> 0x22cb4 (вне списка функций)
  22cb6:  ldrb r5, [r1, #9]                 
  22cb8:  cmp r5, #0                        
  22cba:  beq #0x22cc4                      
  22cbc:  cmp r5, #1                        
  22cbe:  beq #0x22cc4                      
  22cc0:  cpsid i                           
  22cc2:  b #0x22cc2                        -> 0x22cc2 (вне списка функций)
  22cc4:  ldr r2, [r3, #0x54]               
  22cc6:  movs r7, #1                       
  22cc8:  lsls r7, r7, #0xb                 
  22cca:  bics r2, r7                       
  22ccc:  ldrb r7, [r1]                     
  22cce:  lsls r4, r4, #8                   
  22cd0:  lsls r7, r7, #0xb                 
  22cd2:  orrs r2, r7                       
  22cd4:  movs r7, #1                       
  22cd6:  lsls r7, r7, #0xa                 
  22cd8:  bics r2, r7                       
  22cda:  ldrb r7, [r1, #1]                 
  22cdc:  lsls r7, r7, #0xa                 
  22cde:  orrs r2, r7                       
  22ce0:  movs r7, #3                       
  22ce2:  lsls r7, r7, #8                   
  22ce4:  bics r2, r7                       
  22ce6:  orrs r2, r4                       
  22ce8:  lsrs r2, r2, #8                   
  22cea:  lsls r2, r2, #8                   
  22cec:  movs r4, #1                       
  22cee:  orrs r2, r6                       
  22cf0:  lsls r4, r4, #0xc                 
  22cf2:  bics r2, r4                       
  22cf4:  ldrb r4, [r1, #8]                 
  22cf6:  ldrb r1, [r1, #0xa]               
  22cf8:  lsls r4, r4, #0xc                 
  22cfa:  orrs r2, r4                       
  22cfc:  movs r4, #1                       
  22cfe:  lsls r4, r4, #0xd                 
  22d00:  bics r2, r4                       
  22d02:  lsls r4, r5, #0xd                 
  22d04:  orrs r2, r4                       
  22d06:  movs r4, #1                       
  22d08:  lsls r4, r4, #0xe                 
  22d0a:  bics r2, r4                       
  22d0c:  lsls r1, r1, #0xe                 
  22d0e:  orrs r2, r1                       
  22d10:  str r2, [r3, #0x54]               
  22d12:  movs r1, #1                       
  22d14:  strb r1, [r0, #0x1a]              
  22d16:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x22d18 (5 слов) — ВНЕ границ функции ---
  22d18:  .word 0x40012c00  ; периферия
  22d1c:  .word 0x40014000  ; периферия
  22d20:  .word 0x40014400  ; периферия
  22d24:  .word 0x40014800  ; периферия
  22d28:  .word 0x40014c00  ; периферия
```
