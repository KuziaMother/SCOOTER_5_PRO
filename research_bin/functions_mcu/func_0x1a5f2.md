# func_0x1a5f2

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a5f2) | `0x0001a5f2` |
| размер кода | 8 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x1bfa0` (0x0001bfa0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1a628` (bl @0x0001a62e)


## Дизассембляция

```asm
  1a5f2:  push {r4, lr}                     
  1a5f4:  bl #0x1bfa0                       -> func_0x1bfa0
  1a5f8:  pop {r4, pc}                      
```
