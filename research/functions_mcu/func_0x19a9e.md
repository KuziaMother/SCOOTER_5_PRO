# func_0x19a9e

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019a9e) | `0x00019a9e` |
| размер кода | 18 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x19a8c` (0x00019a8c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  19a9e:  push {r4, lr}                     
  19aa0:  mov r3, r2                        
  19aa2:  mov r2, r1                        
  19aa4:  mov r4, r0                        
  19aa6:  mov r1, r3                        
  19aa8:  bl #0x19a8c                       -> func_0x19a8c
  19aac:  mov r0, r4                        
  19aae:  pop {r4, pc}                      
```
