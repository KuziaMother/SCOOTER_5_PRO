# func_0x19a1c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019a1c) | `0x00019a1c` |
| размер кода | 76 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x199bc (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x22824` (bl @0x000228f2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x19a30..0x19a3e` (14 Б); цели из: 0x19a24
- `0x19a3e..0x19a54` (22 Б); цели из: 0x19a32
- `0x19a54..0x19a5e` (10 Б); цели из: 0x19a4a
- `0x19a5e..0x19a68` (10 Б); цели из: 0x19a56

## Дизассембляция

```asm
  19a1c:  push {r3, r4, r5, r6, r7, lr}     
  19a1e:  movs r4, #0                       
  19a20:  mov r5, r4                        
  19a22:  cmp r1, #0                        
  19a24:  bge #0x19a30                      
  19a26:  mov r6, r1                        
  19a28:  movs r4, #1                       
  19a2a:  movs r1, #0                       
  19a2c:  rsbs r0, r0, #0                   
  19a2e:  sbcs r1, r6                       
  19a30:  cmp r3, #0                        
  19a32:  bge #0x19a3e                      
  19a34:  mov r6, r3                        
  19a36:  movs r3, #0                       
  19a38:  rsbs r2, r2, #0                   
  19a3a:  movs r5, #1                       
  19a3c:  sbcs r3, r6                       
  19a3e:  bl #0x199bc                       -> 0x199bc (вне списка функций)
  19a42:  mov ip, r1                        
  19a44:  mov r7, r2                        
  19a46:  mov r6, r3                        
  19a48:  cmp r4, r5                        
  19a4a:  beq #0x19a54                      
  19a4c:  movs r5, #0                       
  19a4e:  rsbs r0, r0, #0                   
  19a50:  sbcs r5, r1                       
  19a52:  mov ip, r5                        
  19a54:  cmp r4, #0                        
  19a56:  beq #0x19a5e                      
  19a58:  movs r6, #0                       
  19a5a:  rsbs r7, r2, #0                   
  19a5c:  sbcs r6, r3                       
  19a5e:  mov r1, ip                        
  19a60:  mov r2, r7                        
  19a62:  mov r3, r6                        
  19a64:  add sp, #4                        
  19a66:  pop {r4, r5, r6, r7, pc}          
```
