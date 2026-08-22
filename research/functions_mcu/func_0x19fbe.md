# func_0x19fbe

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019fbe) | `0x00019fbe` |
| размер кода | 14 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x1a0f8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1de5e` (bl @0x0001de6e)
- `func_0x1de5e` (bl @0x0001de76)
- `func_0x1de5e` (bl @0x0001de92)


## Дизассембляция

```asm
  19fbe:  push {r4, lr}                     
  19fc0:  movs r2, #0                       
  19fc2:  movs r3, #0x96                    
  19fc4:  mov r1, r2                        
  19fc6:  bl #0x1a0f8                       -> 0x1a0f8 (вне списка функций)
  19fca:  pop {r4, pc}                      
```
