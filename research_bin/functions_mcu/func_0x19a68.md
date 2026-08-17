# func_0x19a68

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019a68) | `0x00019a68` |
| размер кода | 36 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x19a86 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1c838` (bl @0x0001c848)
- `func_0x1c838` (bl @0x0001c852)
- `func_0x1dea4` (bl @0x0001deae)


## Дизассембляция

```asm
  19a68:  mov r3, r0                        
  19a6a:  orrs r3, r1                       
  19a6c:  lsls r3, r3, #0x1e                
  19a6e:  beq #0x19a78                      
  19a70:  b #0x19a86                        -> 0x19a86 (вне списка функций)
  19a72:  ldm r1!, {r3}                     
  19a74:  subs r2, r2, #4                   
  19a76:  stm r0!, {r3}                     
  19a78:  cmp r2, #4                        
  19a7a:  bhs #0x19a72                      
  19a7c:  b #0x19a86                        -> 0x19a86 (вне списка функций)
  19a7e:  ldrb r3, [r1]                     
  19a80:  strb r3, [r0]                     
  19a82:  adds r0, r0, #1                   
  19a84:  adds r1, r1, #1                   
  19a86:  subs r2, r2, #1                   
  19a88:  bhs #0x19a7e                      
  19a8a:  bx lr                             
```
