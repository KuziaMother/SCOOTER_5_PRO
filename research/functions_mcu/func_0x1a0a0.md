# func_0x1a0a0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a0a0) | `0x0001a0a0` |
| размер кода | 34 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1a052` (bl @0x0001a068)
- `func_0x1a184` (bl @0x0001a1ca)


## Дизассембляция

```asm
  1a0a0:  push {r4, lr}                     
  1a0a2:  cmp r2, #0x20                     
  1a0a4:  blt #0x1a0b0                      
  1a0a6:  mov r0, r1                        
  1a0a8:  subs r2, #0x20                    
  1a0aa:  lsrs r0, r2                       
  1a0ac:  movs r1, #0                       
  1a0ae:  pop {r4, pc}                      
  1a0b0:  mov r3, r1                        
  1a0b2:  lsrs r3, r2                       
  1a0b4:  lsrs r0, r2                       
  1a0b6:  movs r4, #0x20                    
  1a0b8:  subs r2, r4, r2                   
  1a0ba:  lsls r1, r2                       
  1a0bc:  orrs r0, r1                       
  1a0be:  mov r1, r3                        
  1a0c0:  pop {r4, pc}                      
```
