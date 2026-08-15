# func_0x22b7c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022b7c) | `0x00022b7c` |
| размер кода | 212 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40000400 — периферия (r2)
- 0x40000800 — периферия (r2)
- 0x40000c00 — периферия (r2)
- 0x40012c00 — периферия (r3)
- 0x40014000 — периферия (r4)
- 0x40014400 — периферия (r5)
- 0x40014800 — периферия (r6)
- 0x40014c00 — периферия (r2)

## Вызовы (callees)

- 0x22b96 (b, вне списка функций)
- 0x22ba8 (b, вне списка функций)
- 0x22bc0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x22a48` (bl @0x00022ad0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x22b98..0x22baa` (18 Б); цели из: 0x22b82, 0x22b86, 0x22b8a, 0x22b8e…
- `0x22baa..0x22bf6` (76 Б); цели из: 0x22b9c, 0x22ba0, 0x22ba4
- `0x22bf6..0x22c06` (16 Б); цели из: 0x22bca, 0x22bce, 0x22bd2, 0x22bd6…
- `0x22c06..0x22c24` (30 Б); цели из: 0x22bf4
- `0x22c24..0x22c30` (12 Б); цели из: 0x22c10, 0x22c14, 0x22c18, 0x22c1c
- `0x22c30..0x22c3a` (10 Б); цели из: 0x22c22
- `0x22c3a..0x22c50` (22 Б); цели из: 0x22bae, 0x22bb2

## Дизассембляция

```asm
  22b7c:  push {r4, r5, r6, r7, lr}         
  22b7e:  ldrb r2, [r1, #4]                 
  22b80:  cmp r2, #0                        
  22b82:  beq #0x22b98                      
  22b84:  cmp r2, #1                        
  22b86:  beq #0x22b98                      
  22b88:  cmp r2, #2                        
  22b8a:  beq #0x22b98                      
  22b8c:  cmp r2, #3                        
  22b8e:  beq #0x22b98                      
  22b90:  cmp r2, #4                        
  22b92:  beq #0x22b98                      
  22b94:  cpsid i                           
  22b96:  b #0x22b96                        -> 0x22b96 (вне списка функций)
  22b98:  ldrb r3, [r1, #0xc]               
  22b9a:  cmp r3, #0                        
  22b9c:  beq #0x22baa                      
  22b9e:  cmp r3, #1                        
  22ba0:  beq #0x22baa                      
  22ba2:  cmp r3, #2                        
  22ba4:  beq #0x22baa                      
  22ba6:  cpsid i                           
  22ba8:  b #0x22ba8                        -> 0x22ba8 (вне списка функций)
  22baa:  movs r4, #0x60                    
  22bac:  cmp r2, #0                        
  22bae:  beq #0x22c3a                      
  22bb0:  cmp r2, #1                        
  22bb2:  beq #0x22c3a                      
  22bb4:  ldr r3, [r0]                      
  22bb6:  lsls r2, r2, #5                   
  22bb8:  bics r3, r4                       
  22bba:  subs r2, #0x20                    
  22bbc:  orrs r3, r2                       
  22bbe:  str r3, [r0]                      
  22bc0:  ldr r3, [pc, #0x8c]               -> периферия
  22bc2:  ldr r4, [pc, #0x90]               -> периферия
  22bc4:  ldr r5, [pc, #0x90]               -> периферия
  22bc6:  ldr r6, [pc, #0x94]               -> периферия
  22bc8:  cmp r0, r3                        
  22bca:  beq #0x22bf6                      
  22bcc:  cmp r0, r4                        
  22bce:  beq #0x22bf6                      
  22bd0:  cmp r0, r5                        
  22bd2:  beq #0x22bf6                      
  22bd4:  cmp r0, r6                        
  22bd6:  beq #0x22bf6                      
  22bd8:  ldr r2, [pc, #0x84]               -> периферия
  22bda:  cmp r0, r2                        
  22bdc:  beq #0x22bf6                      
  22bde:  ldr r2, [pc, #0x84]               -> периферия
  22be0:  cmp r0, r2                        
  22be2:  beq #0x22bf6                      
  22be4:  ldr r2, [pc, #0x80]               -> периферия
  22be6:  cmp r0, r2                        
  22be8:  beq #0x22bf6                      
  22bea:  ldr r2, [pc, #0x80]               -> периферия
  22bec:  cmp r0, r2                        
  22bee:  beq #0x22bf6                      
  22bf0:  lsls r2, r4, #0x10                
  22bf2:  cmp r0, r2                        
  22bf4:  bne #0x22c06                      
  22bf6:  ldr r2, [r0]                      
  22bf8:  movs r7, #3                       
  22bfa:  lsls r7, r7, #8                   
  22bfc:  bics r2, r7                       
  22bfe:  ldrb r7, [r1, #0xc]               
  22c00:  lsls r7, r7, #8                   
  22c02:  orrs r2, r7                       
  22c04:  str r2, [r0]                      
  22c06:  ldr r2, [r1, #8]                  
  22c08:  str r2, [r0, #0x3c]               
  22c0a:  ldr r2, [r1]                      
  22c0c:  str r2, [r0, #0x38]               
  22c0e:  cmp r0, r3                        
  22c10:  beq #0x22c24                      
  22c12:  cmp r0, r4                        
  22c14:  beq #0x22c24                      
  22c16:  cmp r0, r5                        
  22c18:  beq #0x22c24                      
  22c1a:  cmp r0, r6                        
  22c1c:  beq #0x22c24                      
  22c1e:  ldr r2, [pc, #0x40]               -> периферия
  22c20:  cmp r0, r2                        
  22c22:  bne #0x22c30                      
  22c24:  ldr r2, [r0, #0x40]               
  22c26:  ldr r1, [r1, #0x10]               
  22c28:  lsrs r2, r2, #8                   
  22c2a:  lsls r2, r2, #8                   
  22c2c:  orrs r2, r1                       
  22c2e:  str r2, [r0, #0x40]               
  22c30:  ldr r1, [r0, #0x24]               
  22c32:  movs r2, #1                       
  22c34:  orrs r1, r2                       
  22c36:  str r1, [r0, #0x24]               
  22c38:  pop {r4, r5, r6, r7, pc}          
  22c3a:  ldr r2, [r0]                      
  22c3c:  bics r2, r4                       
  22c3e:  str r2, [r0]                      
  22c40:  ldr r2, [r0]                      
  22c42:  movs r3, #0x10                    
  22c44:  bics r2, r3                       
  22c46:  ldrb r3, [r1, #4]                 
  22c48:  lsls r3, r3, #4                   
  22c4a:  orrs r2, r3                       
  22c4c:  str r2, [r0]                      
  22c4e:  b #0x22bc0                        -> 0x22bc0 (вне списка функций)
  ; --- literal-пул @0x22c50 (8 слов) — ВНЕ границ функции ---
  22c50:  .word 0x40012c00  ; периферия
  22c54:  .word 0x40014000  ; периферия
  22c58:  .word 0x40014400  ; периферия
  22c5c:  .word 0x40014800  ; периферия
  22c60:  .word 0x40014c00  ; периферия
  22c64:  .word 0x40000400  ; периферия
  22c68:  .word 0x40000800  ; периферия
  22c6c:  .word 0x40000c00  ; периферия
```
