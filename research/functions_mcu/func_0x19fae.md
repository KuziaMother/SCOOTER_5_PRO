# func_0x19fae

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019fae) | `0x00019fae` |
| размер кода | 16 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x1a0f8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  19fae:  push {r4, lr}                     
  19fb0:  adds r0, r0, r1                   
  19fb2:  lsls r2, r1, #0x1f                
  19fb4:  movs r3, #0x96                    
  19fb6:  movs r1, #0                       
  19fb8:  bl #0x1a0f8                       -> 0x1a0f8 (вне списка функций)
  19fbc:  pop {r4, pc}                      
```
