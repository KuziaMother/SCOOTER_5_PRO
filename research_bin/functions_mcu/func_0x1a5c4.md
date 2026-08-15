# func_0x1a5c4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a5c4) | `0x0001a5c4` |
| размер кода | 12 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40012400 — периферия (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a520)


## Дизассембляция

```asm
  1a5c4:  ldr r0, [pc, #8]                  -> периферия
  1a5c6:  ldr r1, [r0, #0x18]               
  1a5c8:  movs r2, #8                       
  1a5ca:  orrs r1, r2                       
  1a5cc:  str r1, [r0, #0x18]               
  1a5ce:  bx lr                             
  ; --- literal-пул @0x1a5d0 (1 слов) — ВНЕ границ функции ---
  1a5d0:  .word 0x40012400  ; периферия
```
