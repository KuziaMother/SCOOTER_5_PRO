# func_0x221a4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800221a4) | `0x000221a4` |
| размер кода | 66 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x221de (b, вне списка функций)
- 0x235d4 (bl, вне списка функций)
- 0x23688 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1c838` (bl @0x0001c8c0)
- `func_0x1c838` (bl @0x0001c92c)
- `func_0x1c838` (bl @0x0001ca3c)
- `func_0x1c838` (bl @0x0001ca82)
- `func_0x1c838` (bl @0x0001cda4)
- `func_0x21a08` (bl @0x00021a20)
- `func_0x21a08` (bl @0x00021ac8)


## Дизассембляция

```asm
  221a4:  push {r4, lr}                     
  221a6:  sub sp, #0x14                     
  221a8:  mov r4, r0                        
  221aa:  movs r0, #1                       
  221ac:  mov r1, sp                        
  221ae:  strb r0, [r1]                     
  221b0:  cpsid i                           
  221b2:  bl #0x23688                       -> 0x23688 (вне списка функций)
  221b6:  adds r4, r4, #1                   
  221b8:  mvns r0, r4                       
  221ba:  str r0, [sp, #8]                  
  221bc:  str r4, [sp, #4]                  
  221be:  add r0, sp, #4                    
  221c0:  bl #0x235d4                       -> 0x235d4 (вне списка функций)
  221c4:  cmp r0, #1                        
  221c6:  beq #0x221ce                      
  221c8:  movs r0, #0                       
  221ca:  mov r1, sp                        
  221cc:  strb r0, [r1]                     
  221ce:  bl #0x23688                       -> 0x23688 (вне списка функций)
  221d2:  cpsie i                           
  221d4:  mov r0, sp                        
  221d6:  ldrb r0, [r0]                     
  221d8:  cmp r0, #0                        
  221da:  beq #0x221e2                      
  221dc:  movs r0, #0                       
  221de:  add sp, #0x14                     
  221e0:  pop {r4, pc}                      
  221e2:  movs r0, #1                       
  221e4:  b #0x221de                        -> 0x221de (вне списка функций)
```
