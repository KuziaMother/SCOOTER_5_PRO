# func_0x19ff4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019ff4) | `0x00019ff4` |
| размер кода | 24 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000433 — данные @0x00433 (r1)

## Вызовы (callees)

- `func_0x1a184` (0x0001a184, bl)

## Кто вызывает (callers / xrefs)

- `func_0x22274` (bl @0x000222d4)
- `func_0x22274` (bl @0x000222e2)
- `func_0x22274` (bl @0x00022310)


## Дизассембляция

```asm
  19ff4:  push {r1, r2, r3, lr}             
  19ff6:  ldr r1, [pc, #0x14]               -> данные @0x00433
  19ff8:  str r1, [sp, #8]                  
  19ffa:  movs r1, #0                       
  19ffc:  str r1, [sp]                      
  19ffe:  mov r2, r1                        
  1a000:  mov r3, r1                        
  1a002:  str r1, [sp, #4]                  
  1a004:  bl #0x1a184                       -> func_0x1a184
  1a008:  add sp, #0xc                      
  1a00a:  pop {pc}                          
  ; --- literal-пул @0x1a00c (1 слов) — ВНЕ границ функции ---
  1a00c:  .word 0x00000433  ; данные @0x00433
```
