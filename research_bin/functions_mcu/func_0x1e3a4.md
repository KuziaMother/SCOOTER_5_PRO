# func_0x1e3a4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e3a4) | `0x0001e3a4` |
| размер кода | 50 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x05fa0004 — прочее (r0)
- 0x40021400 — периферия (r0)
- 0xe000ed00 — Cortex-M (NVIC/SCB/SysTick) (r1)

## Вызовы (callees)

- 0x1e3d2 (b, вне списка функций)
- 0x235b0 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1e3a4:  bl #0x235b0                       -> 0x235b0 (вне списка функций)
  1e3a8:  ldr r0, [pc, #0x2c]               -> периферия
  1e3aa:  ldr r1, [r0]                      
  1e3ac:  movs r2, #0xc                     
  1e3ae:  bics r1, r2                       
  1e3b0:  str r1, [r0]                      
  1e3b2:  ldr r1, [r0]                      
  1e3b4:  movs r2, #0xff                    
  1e3b6:  adds r2, #0xf1                    
  1e3b8:  bics r1, r2                       
  1e3ba:  str r1, [r0]                      
  1e3bc:  ldr r1, [r0]                      
  1e3be:  movs r2, #1                       
  1e3c0:  orrs r1, r2                       
  1e3c2:  str r1, [r0]                      
  1e3c4:  dsb sy                            
  1e3c8:  ldr r1, [pc, #0x14]               -> Cortex-M (NVIC/SCB/SysTick)
  1e3ca:  ldr r0, [pc, #0x10]               
  1e3cc:  str r0, [r1, #0xc]                
  1e3ce:  dsb sy                            
  1e3d2:  nop                               
  1e3d4:  b #0x1e3d2                        -> 0x1e3d2 (вне списка функций)
  ; --- literal-пул @0x1e3d8 (3 слов) — ВНЕ границ функции ---
  1e3d8:  .word 0x40021400  ; периферия
  1e3dc:  .word 0x05fa0004
  1e3e0:  .word 0xe000ed00  ; Cortex-M (NVIC/SCB/SysTick)
```
