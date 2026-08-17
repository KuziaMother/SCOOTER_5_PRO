# func_0x1a7ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a7ac) | `0x0001a7ac` |
| размер кода | 136 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0000a907 — данные @0x0a907 (r6)

## Вызовы (callees)

- `func_0x1a5fa` (0x0001a5fa, bl)
- 0x1a7c0 (b, вне списка функций)
- `func_0x1dd8c` (0x0001dd8c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1a5e6` (bl @0x0001a5ec)


## Дизассембляция

```asm
  1a7ac:  push {r3, r4, r5, r6, r7, lr}     
  1a7ae:  mov r7, r1                        
  1a7b0:  mov r2, r1                        
  1a7b2:  mov r4, r0                        
  1a7b4:  mov r1, r0                        
  1a7b6:  movs r0, #0                       
  1a7b8:  bl #0x1a5fa                       -> func_0x1a5fa
  1a7bc:  ldr r6, [pc, #0x74]               -> данные @0x0a907
  1a7be:  movs r5, #1                       
  1a7c0:  movs r2, #0                       
  1a7c2:  movs r0, #0                       
  1a7c4:  lsls r1, r0, #2                   
  1a7c6:  adds r1, r1, r4                   
  1a7c8:  ldrb r3, [r1, r2]                 
  1a7ca:  adds r0, r0, #1                   
  1a7cc:  ldrb r3, [r6, r3]                 
  1a7ce:  uxtb r0, r0                       
  1a7d0:  strb r3, [r1, r2]                 
  1a7d2:  cmp r0, #4                        
  1a7d4:  blo #0x1a7c4                      
  1a7d6:  adds r2, r2, #1                   
  1a7d8:  uxtb r2, r2                       
  1a7da:  cmp r2, #4                        
  1a7dc:  blo #0x1a7c2                      
  1a7de:  ldrb r0, [r4, #1]                 
  1a7e0:  ldrb r1, [r4, #5]                 
  1a7e2:  strb r1, [r4, #1]                 
  1a7e4:  ldrb r1, [r4, #9]                 
  1a7e6:  strb r1, [r4, #5]                 
  1a7e8:  ldrb r1, [r4, #0xd]               
  1a7ea:  strb r1, [r4, #9]                 
  1a7ec:  strb r0, [r4, #0xd]               
  1a7ee:  ldrb r0, [r4, #2]                 
  1a7f0:  ldrb r1, [r4, #0xa]               
  1a7f2:  strb r1, [r4, #2]                 
  1a7f4:  strb r0, [r4, #0xa]               
  1a7f6:  ldrb r0, [r4, #6]                 
  1a7f8:  ldrb r1, [r4, #0xe]               
  1a7fa:  strb r1, [r4, #6]                 
  1a7fc:  strb r0, [r4, #0xe]               
  1a7fe:  ldrb r0, [r4, #3]                 
  1a800:  ldrb r1, [r4, #0xf]               
  1a802:  strb r1, [r4, #3]                 
  1a804:  ldrb r1, [r4, #0xb]               
  1a806:  strb r1, [r4, #0xf]               
  1a808:  ldrb r1, [r4, #7]                 
  1a80a:  strb r1, [r4, #0xb]               
  1a80c:  strb r0, [r4, #7]                 
  1a80e:  cmp r5, #0xa                      
  1a810:  beq #0x1a828                      
  1a812:  mov r0, r4                        
  1a814:  bl #0x1dd8c                       -> func_0x1dd8c
  1a818:  mov r2, r7                        
  1a81a:  mov r1, r4                        
  1a81c:  mov r0, r5                        
  1a81e:  bl #0x1a5fa                       -> func_0x1a5fa
  1a822:  adds r5, r5, #1                   
  1a824:  uxtb r5, r5                       
  1a826:  b #0x1a7c0                        -> 0x1a7c0 (вне списка функций)
  1a828:  mov r2, r7                        
  1a82a:  mov r1, r4                        
  1a82c:  movs r0, #0xa                     
  1a82e:  bl #0x1a5fa                       -> func_0x1a5fa
  1a832:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1a834 (1 слов) — ВНЕ границ функции ---
  1a834:  .word 0x0000a907  ; данные @0x0a907
```
