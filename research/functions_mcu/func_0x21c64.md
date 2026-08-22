# func_0x21c64

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080021c64) | `0x00021c64` |
| размер кода | 12 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200016aa — RAM (r0)

## Вызовы (callees)

- 0x1a5e4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1f71c` (bl @0x000200e4)
- `func_0x1f71c` (bl @0x00020212)


## Дизассембляция

```asm
  21c64:  push {r4, lr}                     
  21c66:  mov r1, r0                        
  21c68:  ldr r0, [pc, #4]                  -> RAM
  21c6a:  bl #0x1a5e4                       -> 0x1a5e4 (вне списка функций)
  21c6e:  pop {r4, pc}                      
  ; --- literal-пул @0x21c70 (1 слов) — ВНЕ границ функции ---
  21c70:  .word 0x200016aa  ; RAM
```
