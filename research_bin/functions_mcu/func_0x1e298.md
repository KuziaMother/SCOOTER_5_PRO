# func_0x1e298

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e298) | `0x0001e298` |
| размер кода | 34 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40012400 — периферия (r0)
- 0x40020000 — периферия (r4)
- 0x5d000041 — периферия (r2)

## Вызовы (callees)

- `func_0x1a5d4` (0x0001a5d4, bl)
- 0x2359c (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a340)


## Дизассембляция

```asm
  1e298:  push {r4, lr}                     
  1e29a:  bl #0x1a5d4                       -> func_0x1a5d4
  1e29e:  ldr r4, [pc, #0x20]               -> периферия
  1e2a0:  ldr r2, [pc, #0x18]               -> периферия
  1e2a2:  movs r1, #0                       
  1e2a4:  mov r0, r4                        
  1e2a6:  bl #0x2359c                       -> 0x2359c (вне списка функций)
  1e2aa:  movs r0, #1                       
  1e2ac:  str r0, [r4, #0x28]               
  1e2ae:  ldr r0, [pc, #0x14]               -> периферия
  1e2b0:  ldr r1, [r0, #0x18]               
  1e2b2:  movs r2, #4                       
  1e2b4:  orrs r1, r2                       
  1e2b6:  str r1, [r0, #0x18]               
  1e2b8:  pop {r4, pc}                      
  ; --- literal-пул @0x1e2bc (3 слов) — ВНЕ границ функции ---
  1e2bc:  .word 0x5d000041  ; периферия
  1e2c0:  .word 0x40020000  ; периферия
  1e2c4:  .word 0x40012400  ; периферия
```
