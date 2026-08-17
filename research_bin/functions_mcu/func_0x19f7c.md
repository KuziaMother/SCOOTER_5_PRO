# func_0x19f7c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019f7c) | `0x00019f7c` |
| размер кода | 44 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x22274` (bl @0x000222ea)


## Дизассембляция

```asm
  19f7c:  push {r4, r5, r6, lr}             
  19f7e:  lsls r3, r1, #1                   
  19f80:  lsrs r3, r3, #1                   
  19f82:  orrs r3, r0                       
  19f84:  beq #0x19f9e                      
  19f86:  lsls r3, r1, #1                   
  19f88:  lsrs r4, r3, #0x15                
  19f8a:  movs r6, #0                       
  19f8c:  mov r3, r6                        
  19f8e:  rsbs r5, r4, #0                   
  19f90:  sbcs r3, r6                       
  19f92:  asrs r4, r2, #0x1f                
  19f94:  subs r5, r5, r2                   
  19f96:  sbcs r3, r4                       
  19f98:  blt #0x19fa0                      
  19f9a:  movs r0, #0                       
  19f9c:  mov r1, r0                        
  19f9e:  pop {r4, r5, r6, pc}              
  19fa0:  lsls r2, r2, #0x14                
  19fa2:  adds r0, r6, r0                   
  19fa4:  adcs r1, r2                       
  19fa6:  pop {r4, r5, r6, pc}              
```
