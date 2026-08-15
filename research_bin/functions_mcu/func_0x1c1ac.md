# func_0x1c1ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001c1ac) | `0x0001c1ac` |
| размер кода | 106 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001692 — RAM (r1)
- 0x40012450 — периферия (r1)
- 0x40020000 — периферия (r4)
- 0x40020100 — периферия (r1)
- 0x5d000041 — периферия (r2)
- 0xe000e100 — Cortex-M (NVIC/SCB/SysTick) (r1)
- 0xe000e408 — Cortex-M (NVIC/SCB/SysTick) (r1)

## Вызовы (callees)

- 0x1c1c4 (b, вне списка функций)
- 0x1c1da (b, вне списка функций)
- 0x2359c (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1bf48` (bl @0x0001bf52)


## Дизассембляция

```asm
  1c1ac:  push {r4, lr}                     
  1c1ae:  ldr r4, [pc, #0x68]               -> периферия
  1c1b0:  movs r0, #1                       
  1c1b2:  str r0, [r4, #4]                  
  1c1b4:  movs r0, #0                       
  1c1b6:  lsls r0, r0, #4                   
  1c1b8:  adds r0, r0, r4                   
  1c1ba:  adds r0, #0xff                    
  1c1bc:  ldr r1, [pc, #0x5c]               -> периферия
  1c1be:  adds r0, #1                       
  1c1c0:  b #0x1c1c4                        -> 0x1c1c4 (вне списка функций)
  1c1c2:  str r1, [r0]                      
  1c1c4:  ldr r2, [r0]                      
  1c1c6:  cmp r2, r1                        
  1c1c8:  bne #0x1c1c2                      
  1c1ca:  movs r0, #0                       
  1c1cc:  lsls r0, r0, #4                   
  1c1ce:  adds r0, r0, r4                   
  1c1d0:  adds r0, #0xff                    
  1c1d2:  ldr r1, [pc, #0x4c]               -> RAM
  1c1d4:  adds r0, #1                       
  1c1d6:  b #0x1c1da                        -> 0x1c1da (вне списка функций)
  1c1d8:  str r1, [r0, #4]                  
  1c1da:  ldr r2, [r0, #4]                  
  1c1dc:  cmp r2, r1                        
  1c1de:  bne #0x1c1d8                      
  1c1e0:  ldr r2, [pc, #0x40]               -> периферия
  1c1e2:  movs r1, #0                       
  1c1e4:  mov r0, r4                        
  1c1e6:  bl #0x2359c                       -> 0x2359c (вне списка функций)
  1c1ea:  movs r0, #1                       
  1c1ec:  str r0, [r4, #0x28]               
  1c1ee:  str r0, [r4, #0x14]               
  1c1f0:  movs r1, #0x19                    
  1c1f2:  str r1, [r4, #0x70]               
  1c1f4:  ldr r1, [r4, #0x50]               
  1c1f6:  orrs r1, r0                       
  1c1f8:  str r1, [r4, #0x50]               
  1c1fa:  ldr r1, [pc, #0x2c]               -> периферия
  1c1fc:  ldr r2, [r1, #8]                  
  1c1fe:  orrs r2, r0                       
  1c200:  str r2, [r1, #8]                  
  1c202:  ldr r1, [pc, #0x28]               -> Cortex-M (NVIC/SCB/SysTick)
  1c204:  lsls r0, r0, #9                   
  1c206:  str r0, [r1]                      
  1c208:  ldr r1, [pc, #0x24]               -> Cortex-M (NVIC/SCB/SysTick)
  1c20a:  ldr r0, [r1]                      
  1c20c:  movs r2, #0xff                    
  1c20e:  lsls r2, r2, #8                   
  1c210:  bics r0, r2                       
  1c212:  str r0, [r1]                      
  1c214:  pop {r4, pc}                      
  ; --- literal-пул @0x1c218 (7 слов) — ВНЕ границ функции ---
  1c218:  .word 0x40020000  ; периферия
  1c21c:  .word 0x40012450  ; периферия
  1c220:  .word 0x20001692  ; RAM
  1c224:  .word 0x5d000041  ; периферия
  1c228:  .word 0x40020100  ; периферия
  1c22c:  .word 0xe000e100  ; Cortex-M (NVIC/SCB/SysTick)
  1c230:  .word 0xe000e408  ; Cortex-M (NVIC/SCB/SysTick)
```
