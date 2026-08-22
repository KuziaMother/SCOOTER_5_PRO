# func_0x1d818

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001d818) | `0x0001d818` |
| размер кода | 86 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000010c — RAM (r6)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1a938` (bl @0x0001b5f4)


## Дизассембляция

```asm
  1d818:  push {r0, r4, r5, r6, r7, lr}     
  1d81a:  sub sp, #4                        
  1d81c:  mov r4, sp                        
  1d81e:  movs r0, #4                       
  1d820:  ldr r6, [pc, #0x4c]               -> RAM
  1d822:  ldrsh r0, [r4, r0]                
  1d824:  movs r5, #2                       
  1d826:  ldrsh r5, [r6, r5]                
  1d828:  mov r2, r0                        
  1d82a:  muls r0, r5, r0                   
  1d82c:  asrs r1, r0, #0x1f                
  1d82e:  lsrs r1, r1, #0x11                
  1d830:  adds r0, r1, r0                   
  1d832:  movs r1, #6                       
  1d834:  ldrsh r1, [r4, r1]                
  1d836:  movs r7, #0                       
  1d838:  ldrsh r7, [r6, r7]                
  1d83a:  mov r3, r1                        
  1d83c:  muls r1, r7, r1                   
  1d83e:  asrs r4, r1, #0x1f                
  1d840:  lsrs r4, r4, #0x11                
  1d842:  adds r1, r4, r1                   
  1d844:  asrs r0, r0, #0xf                 
  1d846:  asrs r1, r1, #0xf                 
  1d848:  subs r0, r1, r0                   
  1d84a:  mov r4, sp                        
  1d84c:  strh r0, [r4]                     
  1d84e:  mov r0, r2                        
  1d850:  muls r0, r7, r0                   
  1d852:  asrs r1, r0, #0x1f                
  1d854:  lsrs r1, r1, #0x11                
  1d856:  adds r0, r1, r0                   
  1d858:  mov r1, r3                        
  1d85a:  muls r1, r5, r1                   
  1d85c:  asrs r2, r1, #0x1f                
  1d85e:  lsrs r2, r2, #0x11                
  1d860:  adds r1, r2, r1                   
  1d862:  asrs r0, r0, #0xf                 
  1d864:  asrs r1, r1, #0xf                 
  1d866:  adds r0, r0, r1                   
  1d868:  strh r0, [r4, #2]                 
  1d86a:  ldr r0, [sp]                      
  1d86c:  pop {r2, r3, r4, r5, r6, r7, pc}  
  ; --- literal-пул @0x1d870 (1 слов) — ВНЕ границ функции ---
  1d870:  .word 0x2000010c  ; RAM
```
