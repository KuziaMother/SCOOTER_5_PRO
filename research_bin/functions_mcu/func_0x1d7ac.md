# func_0x1d7ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001d7ac) | `0x0001d7ac` |
| размер кода | 102 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000010c — RAM (r5)

## Вызовы (callees)

- `func_0x1e410` (0x0001e410, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1a938` (bl @0x0001aa04)


## Дизассембляция

```asm
  1d7ac:  push {r0, r1, r4, r5, r6, r7, lr} 
  1d7ae:  sub sp, #4                        
  1d7b0:  mov r0, r1                        
  1d7b2:  bl #0x1e410                       -> func_0x1e410
  1d7b6:  ldr r5, [pc, #0x5c]               -> RAM
  1d7b8:  mov r4, sp                        
  1d7ba:  str r0, [sp]                      
  1d7bc:  ldrh r0, [r4]                     
  1d7be:  strh r0, [r5]                     
  1d7c0:  ldrh r0, [r4, #2]                 
  1d7c2:  strh r0, [r5, #2]                 
  1d7c4:  movs r0, #4                       
  1d7c6:  ldrsh r0, [r4, r0]                
  1d7c8:  movs r6, #2                       
  1d7ca:  ldrsh r6, [r5, r6]                
  1d7cc:  mov r2, r0                        
  1d7ce:  muls r0, r6, r0                   
  1d7d0:  asrs r1, r0, #0x1f                
  1d7d2:  lsrs r1, r1, #0x11                
  1d7d4:  adds r0, r1, r0                   
  1d7d6:  movs r1, #6                       
  1d7d8:  ldrsh r1, [r4, r1]                
  1d7da:  movs r7, #0                       
  1d7dc:  ldrsh r7, [r5, r7]                
  1d7de:  mov r3, r1                        
  1d7e0:  muls r1, r7, r1                   
  1d7e2:  asrs r4, r1, #0x1f                
  1d7e4:  lsrs r4, r4, #0x11                
  1d7e6:  adds r1, r4, r1                   
  1d7e8:  asrs r0, r0, #0xf                 
  1d7ea:  asrs r1, r1, #0xf                 
  1d7ec:  subs r0, r1, r0                   
  1d7ee:  mov r4, sp                        
  1d7f0:  strh r0, [r4]                     
  1d7f2:  mov r0, r2                        
  1d7f4:  muls r0, r7, r0                   
  1d7f6:  asrs r1, r0, #0x1f                
  1d7f8:  lsrs r1, r1, #0x11                
  1d7fa:  adds r0, r1, r0                   
  1d7fc:  mov r1, r3                        
  1d7fe:  muls r1, r6, r1                   
  1d800:  asrs r2, r1, #0x1f                
  1d802:  lsrs r2, r2, #0x11                
  1d804:  adds r1, r2, r1                   
  1d806:  asrs r0, r0, #0xf                 
  1d808:  asrs r1, r1, #0xf                 
  1d80a:  adds r0, r0, r1                   
  1d80c:  strh r0, [r4, #2]                 
  1d80e:  ldr r0, [sp]                      
  1d810:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  ; --- literal-пул @0x1d814 (1 слов) — ВНЕ границ функции ---
  1d814:  .word 0x2000010c  ; RAM
```
