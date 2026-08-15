# func_0x1f6b4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001f6b4) | `0x0001f6b4` |
| размер кода | 94 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40004800 — периферия (r5)
- 0x48000800 — периферия (r5)

## Вызовы (callees)

- 0x21b6c (bl, вне списка функций)
- 0x21bc8 (bl, вне списка функций)
- `func_0x22000` (0x00022000, bl)
- `func_0x23188` (0x00023188, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1f6b4:  push {r4, r5, lr}                 
  1f6b6:  sub sp, #0x8c                     
  1f6b8:  movs r1, #2                       
  1f6ba:  mov r0, sp                        
  1f6bc:  strb r1, [r0]                     
  1f6be:  movs r4, #0                       
  1f6c0:  strb r4, [r0, #1]                 
  1f6c2:  strb r4, [r0, #2]                 
  1f6c4:  strb r4, [r0, #3]                 
  1f6c6:  strb r4, [r0, #4]                 
  1f6c8:  strb r4, [r0, #5]                 
  1f6ca:  strb r1, [r0, #6]                 
  1f6cc:  ldr r5, [pc, #0x44]               -> периферия
  1f6ce:  mov r2, sp                        
  1f6d0:  movs r1, #0x40                    
  1f6d2:  mov r0, r5                        
  1f6d4:  bl #0x22000                       -> func_0x22000
  1f6d8:  mov r2, sp                        
  1f6da:  movs r1, #0x80                    
  1f6dc:  mov r0, r5                        
  1f6de:  bl #0x22000                       -> func_0x22000
  1f6e2:  movs r0, #0x4b                    
  1f6e4:  lsls r0, r0, #8                   
  1f6e6:  ldr r5, [pc, #0x30]               -> периферия
  1f6e8:  str r0, [sp, #0xc]                
  1f6ea:  str r5, [sp, #8]                  
  1f6ec:  str r4, [sp, #0x10]               
  1f6ee:  mov r0, sp                        
  1f6f0:  strb r4, [r0, #0x14]              
  1f6f2:  add r0, sp, #8                    
  1f6f4:  bl #0x23188                       -> func_0x23188
  1f6f8:  movs r1, #5                       
  1f6fa:  movs r0, #0x1d                    
  1f6fc:  bl #0x21bc8                       -> 0x21bc8 (вне списка функций)
  1f700:  movs r0, #0x1d                    
  1f702:  bl #0x21b6c                       -> 0x21b6c (вне списка функций)
  1f706:  ldr r0, [r5, #0x2c]               
  1f708:  asrs r1, r5, #0x14                
  1f70a:  orrs r0, r1                       
  1f70c:  str r0, [r5, #0x2c]               
  1f70e:  add sp, #0x8c                     
  1f710:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x1f714 (2 слов) — ВНЕ границ функции ---
  1f714:  .word 0x48000800  ; периферия
  1f718:  .word 0x40004800  ; периферия
```
