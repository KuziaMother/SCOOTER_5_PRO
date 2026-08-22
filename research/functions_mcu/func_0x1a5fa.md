# func_0x1a5fa

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a5fa) | `0x0001a5fa` |
| размер кода | 46 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1a7ac` (bl @0x0001a7b8)
- `func_0x1a7ac` (bl @0x0001a81e)
- `func_0x1a7ac` (bl @0x0001a82e)


## Дизассембляция

```asm
  1a5fa:  push {r4, r5, r6, r7, lr}         
  1a5fc:  movs r3, #0                       
  1a5fe:  mov ip, r1                        
  1a600:  lsls r6, r0, #2                   
  1a602:  adds r1, r6, r3                   
  1a604:  movs r0, #0                       
  1a606:  lsls r5, r1, #2                   
  1a608:  lsls r4, r3, #2                   
  1a60a:  add r4, ip                        
  1a60c:  adds r1, r5, r0                   
  1a60e:  ldrb r7, [r4, r0]                 
  1a610:  ldrb r1, [r2, r1]                 
  1a612:  eors r7, r1                       
  1a614:  strb r7, [r4, r0]                 
  1a616:  adds r0, r0, #1                   
  1a618:  uxtb r0, r0                       
  1a61a:  cmp r0, #4                        
  1a61c:  blo #0x1a60c                      
  1a61e:  adds r3, r3, #1                   
  1a620:  uxtb r3, r3                       
  1a622:  cmp r3, #4                        
  1a624:  blo #0x1a602                      
  1a626:  pop {r4, r5, r6, r7, pc}          
```
