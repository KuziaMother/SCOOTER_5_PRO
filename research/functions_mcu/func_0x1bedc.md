# func_0x1bedc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001bedc) | `0x0001bedc` |
| размер кода | 66 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x48000400 — периферия (r5)

## Вызовы (callees)

- `func_0x22000` (0x00022000, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1bf48` (bl @0x0001bf58)


## Дизассембляция

```asm
  1bedc:  push {r2, r3, r4, r5, r6, lr}     
  1bede:  movs r1, #0                       
  1bee0:  mov r4, r0                        
  1bee2:  str r1, [sp]                      
  1bee4:  mov r0, sp                        
  1bee6:  str r1, [sp, #4]                  
  1bee8:  strb r1, [r0]                     
  1beea:  strb r1, [r0, #2]                 
  1beec:  strb r1, [r0, #1]                 
  1beee:  strb r1, [r0, #4]                 
  1bef0:  strb r1, [r0, #5]                 
  1bef2:  strb r1, [r0, #3]                 
  1bef4:  strb r1, [r0, #6]                 
  1bef6:  ldr r5, [pc, #0x28]               -> периферия
  1bef8:  mov r2, sp                        
  1befa:  movs r1, #0x40                    
  1befc:  mov r0, r5                        
  1befe:  bl #0x22000                       -> func_0x22000
  1bf02:  mov r2, sp                        
  1bf04:  movs r1, #0x80                    
  1bf06:  mov r0, r5                        
  1bf08:  bl #0x22000                       -> func_0x22000
  1bf0c:  movs r1, #0xff                    
  1bf0e:  mov r2, sp                        
  1bf10:  adds r1, #1                       
  1bf12:  mov r0, r5                        
  1bf14:  bl #0x22000                       -> func_0x22000
  1bf18:  movs r0, #7                       
  1bf1a:  strb r0, [r4, #0x14]              
  1bf1c:  pop {r2, r3, r4, r5, r6, pc}      
  ; --- literal-пул @0x1bf20 (1 слов) — ВНЕ границ функции ---
  1bf20:  .word 0x48000400  ; периферия
```
