# func_0x229d4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800229d4) | `0x000229d4` |
| размер кода | 44 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00ffffff — прочее (r4)
- 0x2000001c — RAM (r2)
- 0xe000e000 — Cortex-M (NVIC/SCB/SysTick) (r0)

## Вызовы (callees)

- 0x229f4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x22274` (bl @0x000223ba)
- `func_0x22274` (bl @0x000223ee)


## Дизассембляция

```asm
  229d4:  push {r4, lr}                     
  229d6:  ldr r2, [pc, #0x28]               -> RAM
  229d8:  ldr r4, [pc, #0x2c]               
  229da:  ldr r2, [r2, #8]                  
  229dc:  muls r0, r2, r0                   
  229de:  movs r2, #1                       
  229e0:  lsls r2, r2, #0x18                
  229e2:  subs r2, r2, r0                   
  229e4:  ldr r0, [pc, #0x1c]               -> Cortex-M (NVIC/SCB/SysTick)
  229e6:  b #0x229f4                        -> 0x229f4 (вне списка функций)
  229e8:  str r4, [r0, #0x18]               
  229ea:  ldr r3, [r0, #0x18]               
  229ec:  lsls r3, r3, #8                   
  229ee:  lsrs r3, r3, #8                   
  229f0:  cmp r3, r2                        
  229f2:  bhi #0x229ea                      
  229f4:  mov r3, r1                        
  229f6:  subs r1, r1, #1                   
  229f8:  uxth r1, r1                       
  229fa:  cmp r3, #0                        
  229fc:  bne #0x229e8                      
  229fe:  pop {r4, pc}                      
  ; --- literal-пул @0x22a00 (3 слов) — ВНЕ границ функции ---
  22a00:  .word 0x2000001c  ; RAM
  22a04:  .word 0xe000e000  ; Cortex-M (NVIC/SCB/SysTick)
  22a08:  .word 0x00ffffff
```
