# func_0x1e2ca

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e2ca) | `0x0001e2ca` |
| размер кода | 36 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xe000e000 — Cortex-M (NVIC/SCB/SysTick) (r4)

## Вызовы (callees)

- `func_0x21b84` (0x00021b84, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1e2ca:  push {r4, lr}                     
  1e2cc:  subs r0, r0, #1                   
  1e2ce:  cmp r0, r1                        
  1e2d0:  bls #0x1e2d6                      
  1e2d2:  movs r0, #1                       
  1e2d4:  pop {r4, pc}                      
  1e2d6:  ldr r4, [pc, #0x1c]               -> Cortex-M (NVIC/SCB/SysTick)
  1e2d8:  str r0, [r4, #0x14]               
  1e2da:  movs r1, #3                       
  1e2dc:  subs r0, r1, #4                   
  1e2de:  bl #0x21b84                       -> func_0x21b84
  1e2e2:  movs r0, #0                       
  1e2e4:  str r0, [r4, #0x18]               
  1e2e6:  movs r0, #7                       
  1e2e8:  str r0, [r4, #0x10]               
  1e2ea:  movs r0, #0                       
  1e2ec:  pop {r4, pc}                      
  ; --- literal-пул @0x1e2f4 (1 слов) — ВНЕ границ функции ---
  1e2f4:  .word 0xe000e000  ; Cortex-M (NVIC/SCB/SysTick)
```
