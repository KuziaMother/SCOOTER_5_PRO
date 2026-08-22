# func_0x1a5e6

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a5e6) | `0x0001a5e6` |
| размер кода | 12 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x1a7ac` (0x0001a7ac, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1a5e6:  push {r4, lr}                     
  1a5e8:  mov r1, r0                        
  1a5ea:  mov r0, r2                        
  1a5ec:  bl #0x1a7ac                       -> func_0x1a7ac
  1a5f0:  pop {r4, pc}                      
```
