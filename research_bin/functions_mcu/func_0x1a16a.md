# func_0x1a16a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a16a) | `0x0001a16a` |
| размер кода | 26 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x19c58` (bl @0x00019d7e)
- `func_0x19e8c` (bl @0x00019f70)
- `func_0x1a184` (bl @0x0001a222)


## Дизассембляция

```asm
  1a16a:  push {r4, lr}                     
  1a16c:  cmp r3, #0                        
  1a16e:  bge #0x1a182                      
  1a170:  movs r4, #0                       
  1a172:  adds r0, r0, #1                   
  1a174:  adcs r1, r4                       
  1a176:  adds r2, r2, r2                   
  1a178:  adcs r3, r3                       
  1a17a:  orrs r2, r3                       
  1a17c:  bne #0x1a182                      
  1a17e:  lsrs r0, r0, #1                   
  1a180:  lsls r0, r0, #1                   
  1a182:  pop {r4, pc}                      
```
