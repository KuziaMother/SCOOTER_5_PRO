# func_0x1df84

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001df84) | `0x0001df84` |
| размер кода | 66 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000050c — RAM (r4)
- 0x42f80000 — периферия (r0)
- 0xc2200000 — прочее (r1)

## Вызовы (callees)

- `func_0x1de5e` (0x0001de5e, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1d898` (bl @0x0001d8bc)


## Дизассембляция

```asm
  1df84:  push {r3, r4, r5, r6, r7, lr}     
  1df86:  ldr r4, [pc, #0x40]               -> RAM
  1df88:  movs r1, #0                       
  1df8a:  lsls r2, r1, #2                   
  1df8c:  adds r2, r2, r4                   
  1df8e:  ldr r2, [r2, #4]                  
  1df90:  cmp r2, r0                        
  1df92:  bhs #0x1dfba                      
  1df94:  str r0, [sp]                      
  1df96:  lsls r0, r1, #2                   
  1df98:  ldr r5, [pc, #0x2c]               -> RAM
  1df9a:  adds r2, r0, r4                   
  1df9c:  lsls r6, r1, #1                   
  1df9e:  subs r5, #0x54                    
  1dfa0:  ldr r3, [r2, #4]                  
  1dfa2:  adds r1, r6, r5                   
  1dfa4:  movs r2, #2                       
  1dfa6:  ldrsh r2, [r1, r2]                
  1dfa8:  ldr r1, [r4, r0]                  
  1dfaa:  ldrsh r0, [r5, r6]                
  1dfac:  bl #0x1de5e                       -> func_0x1de5e
  1dfb0:  ldr r1, [pc, #0x18]               
  1dfb2:  cmp r0, r1                        
  1dfb4:  bls #0x1dfb8                      
  1dfb6:  mov r0, r1                        
  1dfb8:  pop {r3, r4, r5, r6, r7, pc}      
  1dfba:  adds r1, r1, #1                   
  1dfbc:  uxtb r1, r1                       
  1dfbe:  cmp r1, #0x29                     
  1dfc0:  blo #0x1df8a                      
  1dfc2:  ldr r0, [pc, #0xc]                -> периферия
  1dfc4:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1dfc8 (3 слов) — ВНЕ границ функции ---
  1dfc8:  .word 0x2000050c  ; RAM
  1dfcc:  .word 0xc2200000
  1dfd0:  .word 0x42f80000  ; периферия
```
