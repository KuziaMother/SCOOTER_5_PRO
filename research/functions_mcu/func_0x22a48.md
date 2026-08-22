# func_0x22a48

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022a48) | `0x00022a48` |
| размер кода | 148 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40000400 — периферия (r1)
- 0x40000800 — периферия (r1)
- 0x40000c00 — периферия (r1)
- 0x40001000 — периферия (r1)
- 0x40012c00 — периферия (r1)
- 0x40014000 — периферия (r1)
- 0x40014400 — периферия (r1)
- 0x40014800 — периферия (r1)
- 0x40014c00 — периферия (r1)

## Вызовы (callees)

- 0x22a90 (b, вне списка функций)
- 0x22aae (b, вне списка функций)
- 0x22ac0 (b, вне списка функций)
- `func_0x22b7c` (0x00022b7c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1d640` (bl @0x0001d6d6)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x22a92..0x22a96` (4 Б); цели из: 0x22a4c
- `0x22a96..0x22ab0` (26 Б); цели из: 0x22a54, 0x22a5a, 0x22a60, 0x22a66…
- `0x22ab0..0x22ac2` (18 Б); цели из: 0x22a9a, 0x22a9e, 0x22aa2, 0x22aa6…
- `0x22ac2..0x22aca` (8 Б); цели из: 0x22ab4, 0x22ab8, 0x22abc
- `0x22aca..0x22adc` (18 Б); цели из: 0x22ac6

## Дизассембляция

```asm
  22a48:  push {r4, lr}                     
  22a4a:  movs r4, r0                       
  22a4c:  beq #0x22a92                      
  22a4e:  ldr r1, [pc, #0x8c]               -> периферия
  22a50:  ldr r0, [r4]                      
  22a52:  cmp r0, r1                        
  22a54:  beq #0x22a96                      
  22a56:  ldr r1, [pc, #0x88]               -> периферия
  22a58:  cmp r0, r1                        
  22a5a:  beq #0x22a96                      
  22a5c:  ldr r1, [pc, #0x84]               -> периферия
  22a5e:  cmp r0, r1                        
  22a60:  beq #0x22a96                      
  22a62:  ldr r1, [pc, #0x84]               -> периферия
  22a64:  cmp r0, r1                        
  22a66:  beq #0x22a96                      
  22a68:  ldr r1, [pc, #0x80]               -> периферия
  22a6a:  cmp r0, r1                        
  22a6c:  beq #0x22a96                      
  22a6e:  ldr r1, [pc, #0x80]               -> периферия
  22a70:  cmp r0, r1                        
  22a72:  beq #0x22a96                      
  22a74:  ldr r1, [pc, #0x7c]               -> периферия
  22a76:  cmp r0, r1                        
  22a78:  beq #0x22a96                      
  22a7a:  ldr r1, [pc, #0x7c]               -> периферия
  22a7c:  cmp r0, r1                        
  22a7e:  beq #0x22a96                      
  22a80:  ldr r1, [pc, #0x78]               -> периферия
  22a82:  cmp r0, r1                        
  22a84:  beq #0x22a96                      
  22a86:  movs r1, #1                       
  22a88:  lsls r1, r1, #0x1e                
  22a8a:  cmp r0, r1                        
  22a8c:  beq #0x22a96                      
  22a8e:  cpsid i                           
  22a90:  b #0x22a90                        -> 0x22a90 (вне списка функций)
  22a92:  movs r0, #1                       
  22a94:  pop {r4, pc}                      
  22a96:  ldrb r1, [r4, #8]                 
  22a98:  cmp r1, #0                        
  22a9a:  beq #0x22ab0                      
  22a9c:  cmp r1, #1                        
  22a9e:  beq #0x22ab0                      
  22aa0:  cmp r1, #2                        
  22aa2:  beq #0x22ab0                      
  22aa4:  cmp r1, #3                        
  22aa6:  beq #0x22ab0                      
  22aa8:  cmp r1, #4                        
  22aaa:  beq #0x22ab0                      
  22aac:  cpsid i                           
  22aae:  b #0x22aae                        -> 0x22aae (вне списка функций)
  22ab0:  ldrb r1, [r4, #0x10]              
  22ab2:  cmp r1, #0                        
  22ab4:  beq #0x22ac2                      
  22ab6:  cmp r1, #1                        
  22ab8:  beq #0x22ac2                      
  22aba:  cmp r1, #2                        
  22abc:  beq #0x22ac2                      
  22abe:  cpsid i                           
  22ac0:  b #0x22ac0                        -> 0x22ac0 (вне списка функций)
  22ac2:  ldrb r1, [r4, #0x1a]              
  22ac4:  cmp r1, #0                        
  22ac6:  bne #0x22aca                      
  22ac8:  strb r1, [r4, #0x19]              
  22aca:  movs r1, #2                       
  22acc:  strb r1, [r4, #0x1a]              
  22ace:  adds r1, r4, #4                   
  22ad0:  bl #0x22b7c                       -> func_0x22b7c
  22ad4:  movs r0, #1                       
  22ad6:  strb r0, [r4, #0x1a]              
  22ad8:  movs r0, #0                       
  22ada:  pop {r4, pc}                      
  ; --- literal-пул @0x22adc (9 слов) — ВНЕ границ функции ---
  22adc:  .word 0x40012c00  ; периферия
  22ae0:  .word 0x40001000  ; периферия
  22ae4:  .word 0x40014000  ; периферия
  22ae8:  .word 0x40014400  ; периферия
  22aec:  .word 0x40014800  ; периферия
  22af0:  .word 0x40014c00  ; периферия
  22af4:  .word 0x40000400  ; периферия
  22af8:  .word 0x40000800  ; периферия
  22afc:  .word 0x40000c00  ; периферия
```
