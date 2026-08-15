# func_0x19a8c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019a8c) | `0x00019a8c` |
| размер кода | 14 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x19a94 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x19a9e` (bl @0x00019aa8)


## Дизассембляция

```asm
  19a8c:  uxtb r2, r2                       
  19a8e:  b #0x19a94                        -> 0x19a94 (вне списка функций)
  19a90:  strb r2, [r0]                     
  19a92:  adds r0, r0, #1                   
  19a94:  subs r1, r1, #1                   
  19a96:  bhs #0x19a90                      
  19a98:  bx lr                             
```
