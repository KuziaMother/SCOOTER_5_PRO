# func_0x1a080

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a080) | `0x0001a080` |
| размер кода | 32 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x19c58` (bl @0x00019cca)
- `func_0x1a184` (bl @0x0001a1a6)
- `func_0x1a184` (bl @0x0001a1d8)


## Дизассембляция

```asm
  1a080:  push {r4, lr}                     
  1a082:  cmp r2, #0x20                     
  1a084:  blt #0x1a090                      
  1a086:  mov r1, r0                        
  1a088:  subs r2, #0x20                    
  1a08a:  lsls r1, r2                       
  1a08c:  movs r0, #0                       
  1a08e:  pop {r4, pc}                      
  1a090:  lsls r1, r2                       
  1a092:  movs r3, #0x20                    
  1a094:  subs r4, r3, r2                   
  1a096:  mov r3, r0                        
  1a098:  lsrs r3, r4                       
  1a09a:  orrs r1, r3                       
  1a09c:  lsls r0, r2                       
  1a09e:  pop {r4, pc}                      
```
