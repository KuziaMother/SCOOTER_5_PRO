# func_0x19b64

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019b64) | `0x00019b64` |
| размер кода | 120 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x19bd2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x19bb0..0x19bb8` (8 Б); цели из: 0x19bac
- `0x19bb8..0x19bca` (18 Б); цели из: 0x19bb2
- `0x19bca..0x19bcc` (2 Б); цели из: 0x19b72
- `0x19bcc..0x19bce` (2 Б); цели из: 0x19b6e
- `0x19bce..0x19bd2` (4 Б); цели из: 0x19bc6
- `0x19bd2..0x19bd8` (6 Б); цели из: 0x19bc8
- `0x19bd8..0x19bdc` (4 Б); цели из: 0x19bd4

## Дизассембляция

```asm
  19b64:  push {r4, r5, r6, lr}             
  19b66:  eors r2, r1                       
  19b68:  lsrs r3, r2, #0x1f                
  19b6a:  lsls r3, r3, #0x1f                
  19b6c:  lsls r0, r0, #1                   
  19b6e:  beq #0x19bcc                      
  19b70:  lsls r2, r1, #1                   
  19b72:  beq #0x19bca                      
  19b74:  lsrs r1, r0, #0x18                
  19b76:  lsrs r4, r2, #0x18                
  19b78:  lsls r0, r0, #8                   
  19b7a:  lsls r2, r2, #8                   
  19b7c:  adds r1, r1, r4                   
  19b7e:  lsrs r0, r0, #9                   
  19b80:  lsrs r2, r2, #9                   
  19b82:  adds r4, r0, r2                   
  19b84:  lsls r5, r4, #7                   
  19b86:  mov r4, r0                        
  19b88:  muls r4, r2, r4                   
  19b8a:  lsrs r0, r0, #8                   
  19b8c:  lsrs r2, r2, #8                   
  19b8e:  lsls r6, r5, #0x10                
  19b90:  muls r0, r2, r0                   
  19b92:  adds r4, r4, r6                   
  19b94:  adds r2, r0, r5                   
  19b96:  lsrs r0, r4, #0x10                
  19b98:  mvns r5, r0                       
  19b9a:  adds r2, r5, r2                   
  19b9c:  lsrs r2, r2, #0x10                
  19b9e:  movs r5, #1                       
  19ba0:  lsls r5, r5, #0xe                 
  19ba2:  adds r2, r2, #1                   
  19ba4:  adds r2, r2, r5                   
  19ba6:  lsls r2, r2, #0x10                
  19ba8:  subs r1, #0x7f                    
  19baa:  lsls r4, r4, #0x10                
  19bac:  beq #0x19bb0                      
  19bae:  adds r2, r2, #1                   
  19bb0:  orrs r0, r2                       
  19bb2:  bmi #0x19bb8                      
  19bb4:  lsls r0, r0, #1                   
  19bb6:  subs r1, r1, #1                   
  19bb8:  uxtb r2, r0                       
  19bba:  lsls r4, r1, #0x18                
  19bbc:  lsrs r0, r0, #7                   
  19bbe:  adds r0, r4, r0                   
  19bc0:  adds r0, r0, #1                   
  19bc2:  lsrs r0, r0, #1                   
  19bc4:  cmp r2, #0x80                     
  19bc6:  beq #0x19bce                      
  19bc8:  b #0x19bd2                        -> 0x19bd2 (вне списка функций)
  19bca:  movs r0, #0                       
  19bcc:  pop {r4, r5, r6, pc}              
  19bce:  lsrs r0, r0, #1                   
  19bd0:  lsls r0, r0, #1                   
  19bd2:  cmp r1, #0                        
  19bd4:  bge #0x19bd8                      
  19bd6:  movs r0, #0                       
  19bd8:  orrs r0, r3                       
  19bda:  pop {r4, r5, r6, pc}              
```
