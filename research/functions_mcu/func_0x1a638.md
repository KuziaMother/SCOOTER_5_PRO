# func_0x1a638

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a638) | `0x0001a638` |
| размер кода | 66 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000734 — RAM (r4)
- 0x429c0000 — периферия (r0)
- 0xc1e00000 — прочее (r1)

## Вызовы (callees)

- `func_0x1de5e` (0x0001de5e, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1d898` (bl @0x0001d938)


## Дизассембляция

```asm
  1a638:  push {r3, r4, r5, r6, r7, lr}     
  1a63a:  ldr r4, [pc, #0x40]               -> RAM
  1a63c:  movs r1, #0                       
  1a63e:  lsls r2, r1, #2                   
  1a640:  adds r2, r2, r4                   
  1a642:  ldr r2, [r2, #4]                  
  1a644:  cmp r2, r0                        
  1a646:  bhs #0x1a66e                      
  1a648:  str r0, [sp]                      
  1a64a:  lsls r0, r1, #2                   
  1a64c:  ldr r5, [pc, #0x2c]               -> RAM
  1a64e:  adds r2, r0, r4                   
  1a650:  lsls r6, r1, #1                   
  1a652:  subs r5, #0x6c                    
  1a654:  ldr r3, [r2, #4]                  
  1a656:  adds r1, r6, r5                   
  1a658:  movs r2, #2                       
  1a65a:  ldrsh r2, [r1, r2]                
  1a65c:  ldr r1, [r4, r0]                  
  1a65e:  ldrsh r0, [r5, r6]                
  1a660:  bl #0x1de5e                       -> func_0x1de5e
  1a664:  ldr r1, [pc, #0x18]               
  1a666:  cmp r0, r1                        
  1a668:  bls #0x1a66c                      
  1a66a:  mov r0, r1                        
  1a66c:  pop {r3, r4, r5, r6, r7, pc}      
  1a66e:  adds r1, r1, #1                   
  1a670:  uxtb r1, r1                       
  1a672:  cmp r1, #0x35                     
  1a674:  blo #0x1a63e                      
  1a676:  ldr r0, [pc, #0xc]                -> периферия
  1a678:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1a67c (3 слов) — ВНЕ границ функции ---
  1a67c:  .word 0x20000734  ; RAM
  1a680:  .word 0xc1e00000
  1a684:  .word 0x429c0000  ; периферия
```
