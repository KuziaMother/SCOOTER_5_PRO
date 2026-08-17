# func_0x1a0c2

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a0c2) | `0x0001a0c2` |
| размер кода | 38 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x1a0e4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x19c58` (bl @0x00019cd6)


## Дизассембляция

```asm
  1a0c2:  push {r4, lr}                     
  1a0c4:  cmp r2, #0x20                     
  1a0c6:  blt #0x1a0d6                      
  1a0c8:  asrs r3, r1, #0x1f                
  1a0ca:  mov r0, r1                        
  1a0cc:  subs r2, #0x20                    
  1a0ce:  asrs r0, r2                       
  1a0d0:  asrs r1, r0, #0x1f                
  1a0d2:  orrs r3, r1                       
  1a0d4:  b #0x1a0e4                        -> 0x1a0e4 (вне списка функций)
  1a0d6:  mov r3, r1                        
  1a0d8:  asrs r3, r2                       
  1a0da:  lsrs r0, r2                       
  1a0dc:  movs r4, #0x20                    
  1a0de:  subs r2, r4, r2                   
  1a0e0:  lsls r1, r2                       
  1a0e2:  orrs r0, r1                       
  1a0e4:  mov r1, r3                        
  1a0e6:  pop {r4, pc}                      
```
