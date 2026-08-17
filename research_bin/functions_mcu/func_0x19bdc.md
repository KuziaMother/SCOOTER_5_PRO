# func_0x19bdc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019bdc) | `0x00019bdc` |
| размер кода | 124 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x19c18 (b, вне списка функций)
- 0x19c4c (b, вне списка функций)
- 0x1a0e8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1de5e` (bl @0x0001de9e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x19c16..0x19c18` (2 Б); цели из: 0x19c10
- `0x19c18..0x19c1c` (4 Б); цели из: 0x19c14
- `0x19c1c..0x19c20` (4 Б); цели из: 0x19bf0, 0x19bf4
- `0x19c20..0x19c2a` (10 Б); цели из: 0x19c1a
- `0x19c2a..0x19c40` (22 Б); цели из: 0x19c24
- `0x19c40..0x19c48` (8 Б); цели из: 0x19c38
- `0x19c48..0x19c4c` (4 Б); цели из: 0x19c42
- `0x19c4c..0x19c58` (12 Б); цели из: 0x19c34, 0x19c3e, 0x19c46

## Дизассембляция

```asm
  19bdc:  push {r4, r5, r6, lr}             
  19bde:  mov r2, r0                        
  19be0:  eors r2, r1                       
  19be2:  lsrs r5, r2, #0x1f                
  19be4:  lsls r0, r0, #1                   
  19be6:  lsls r2, r1, #1                   
  19be8:  lsls r5, r5, #0x1f                
  19bea:  lsrs r0, r0, #1                   
  19bec:  lsrs r2, r2, #1                   
  19bee:  cmp r0, #0                        
  19bf0:  beq #0x19c1c                      
  19bf2:  cmp r2, #0                        
  19bf4:  beq #0x19c1c                      
  19bf6:  lsrs r4, r0, #0x17                
  19bf8:  lsrs r3, r2, #0x17                
  19bfa:  lsls r1, r0, #9                   
  19bfc:  movs r0, #1                       
  19bfe:  lsls r0, r0, #0x17                
  19c00:  lsls r2, r2, #9                   
  19c02:  lsrs r1, r1, #9                   
  19c04:  lsrs r2, r2, #9                   
  19c06:  subs r4, r4, r3                   
  19c08:  adds r1, r1, r0                   
  19c0a:  adds r2, r2, r0                   
  19c0c:  adds r4, #0x7d                    
  19c0e:  cmp r1, r2                        
  19c10:  blo #0x19c16                      
  19c12:  adds r4, r4, #1                   
  19c14:  b #0x19c18                        -> 0x19c18 (вне списка функций)
  19c16:  lsls r1, r1, #1                   
  19c18:  cmp r4, #0                        
  19c1a:  bge #0x19c20                      
  19c1c:  movs r0, #0                       
  19c1e:  pop {r4, r5, r6, pc}              
  19c20:  movs r3, #0                       
  19c22:  cmp r1, r2                        
  19c24:  blo #0x19c2a                      
  19c26:  subs r1, r1, r2                   
  19c28:  orrs r3, r0                       
  19c2a:  lsrs r0, r0, #1                   
  19c2c:  lsls r1, r1, #1                   
  19c2e:  cmp r0, #0                        
  19c30:  bne #0x19c22                      
  19c32:  cmp r1, #0                        
  19c34:  beq #0x19c4c                      
  19c36:  cmp r1, r2                        
  19c38:  bne #0x19c40                      
  19c3a:  movs r1, #1                       
  19c3c:  lsls r1, r1, #0x1f                
  19c3e:  b #0x19c4c                        -> 0x19c4c (вне списка функций)
  19c40:  cmp r1, r2                        
  19c42:  bhs #0x19c48                      
  19c44:  movs r1, #1                       
  19c46:  b #0x19c4c                        -> 0x19c4c (вне списка функций)
  19c48:  movs r1, #1                       
  19c4a:  mvns r1, r1                       
  19c4c:  lsls r0, r4, #0x17                
  19c4e:  adds r0, r0, r3                   
  19c50:  adds r0, r0, r5                   
  19c52:  bl #0x1a0e8                       -> 0x1a0e8 (вне списка функций)
  19c56:  pop {r4, r5, r6, pc}              
```
