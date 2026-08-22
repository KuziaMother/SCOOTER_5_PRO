# func_0x19ab0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019ab0) | `0x00019ab0` |
| размер кода | 162 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x19b42 (b, вне списка функций)
- 0x1a0e8 (bl, вне списка функций)
- 0x1a0f8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1de5e` (bl @0x0001de8a)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x19aca..0x19aec` (34 Б); цели из: 0x19ac2
- `0x19aec..0x19b16` (42 Б); цели из: 0x19ae8
- `0x19b16..0x19b18` (2 Б); цели из: 0x19acc
- `0x19b18..0x19b32` (26 Б); цели из: 0x19b04
- `0x19b32..0x19b48` (22 Б); цели из: 0x19b00
- `0x19b48..0x19b52` (10 Б); цели из: 0x19ada

## Дизассембляция

```asm
  19ab0:  push {r3, r4, r5, r6, r7, lr}     
  19ab2:  mov r2, r0                        
  19ab4:  eors r2, r1                       
  19ab6:  lsrs r4, r2, #0x1f                
  19ab8:  lsls r2, r0, #1                   
  19aba:  lsls r3, r1, #1                   
  19abc:  lsrs r2, r2, #1                   
  19abe:  lsrs r3, r3, #1                   
  19ac0:  cmp r2, r3                        
  19ac2:  bhs #0x19aca                      
  19ac4:  mov r2, r0                        
  19ac6:  mov r0, r1                        
  19ac8:  mov r1, r2                        
  19aca:  lsls r2, r1, #1                   
  19acc:  beq #0x19b16                      
  19ace:  lsrs r3, r0, #0x17                
  19ad0:  lsls r2, r1, #1                   
  19ad2:  uxtb r5, r3                       
  19ad4:  lsrs r2, r2, #0x18                
  19ad6:  subs r5, r5, r2                   
  19ad8:  cmp r5, #0x20                     
  19ada:  bge #0x19b48                      
  19adc:  lsls r1, r1, #9                   
  19ade:  movs r6, #1                       
  19ae0:  lsrs r1, r1, #9                   
  19ae2:  lsls r6, r6, #0x17                
  19ae4:  adds r2, r1, r6                   
  19ae6:  cmp r4, #0                        
  19ae8:  beq #0x19aec                      
  19aea:  rsbs r2, r2, #0                   
  19aec:  movs r1, #0x20                    
  19aee:  subs r7, r1, r5                   
  19af0:  mov r1, r2                        
  19af2:  lsls r1, r7                       
  19af4:  asrs r2, r5                       
  19af6:  adds r0, r2, r0                   
  19af8:  lsrs r2, r0, #0x17                
  19afa:  cmp r2, r3                        
  19afc:  beq #0x19b42                      
  19afe:  cmp r4, #0                        
  19b00:  beq #0x19b32                      
  19b02:  cmp r5, #1                        
  19b04:  bgt #0x19b18                      
  19b06:  lsls r2, r3, #0x17                
  19b08:  subs r0, r0, r2                   
  19b0a:  lsrs r2, r2, #0x1f                
  19b0c:  adds r0, r0, r6                   
  19b0e:  lsls r2, r2, #0x1f                
  19b10:  uxtb r3, r3                       
  19b12:  bl #0x1a0f8                       -> 0x1a0f8 (вне списка функций)
  19b16:  pop {r3, r4, r5, r6, r7, pc}      
  19b18:  lsls r2, r3, #0x17                
  19b1a:  subs r0, r0, r2                   
  19b1c:  movs r3, #1                       
  19b1e:  lsls r0, r0, #1                   
  19b20:  lsls r3, r3, #0x18                
  19b22:  adds r0, r0, r3                   
  19b24:  adds r0, r0, r2                   
  19b26:  rsbs r2, r3, #0                   
  19b28:  adds r0, r0, r2                   
  19b2a:  lsrs r2, r1, #0x1f                
  19b2c:  orrs r0, r2                       
  19b2e:  lsls r1, r1, #1                   
  19b30:  b #0x19b42                        -> 0x19b42 (вне списка функций)
  19b32:  lsrs r1, r1, #1                   
  19b34:  lsls r2, r0, #0x1f                
  19b36:  orrs r1, r2                       
  19b38:  lsls r2, r3, #0x17                
  19b3a:  subs r0, r0, r2                   
  19b3c:  adds r0, r0, r6                   
  19b3e:  lsrs r0, r0, #1                   
  19b40:  adds r0, r0, r2                   
  19b42:  bl #0x1a0e8                       -> 0x1a0e8 (вне списка функций)
  19b46:  pop {r3, r4, r5, r6, r7, pc}      
  19b48:  lsls r1, r4, #1                   
  19b4a:  movs r2, #1                       
  19b4c:  subs r1, r2, r1                   
  19b4e:  subs r0, r0, r4                   
  19b50:  b #0x19b42                        -> 0x19b42 (вне списка функций)
```
