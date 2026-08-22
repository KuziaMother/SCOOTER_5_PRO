# func_0x1a010

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a010) | `0x0001a010` |
| размер кода | 50 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x1a03a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1d898` (bl @0x0001d8c0)
- `func_0x1d898` (bl @0x0001d8fe)
- `func_0x1d898` (bl @0x0001d93c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1a02a..0x1a036` (12 Б); цели из: 0x1a024
- `0x1a036..0x1a03a` (4 Б); цели из: 0x1a02c
- `0x1a03a..0x1a042` (8 Б); цели из: 0x1a034

## Дизассембляция

```asm
  1a010:  lsrs r2, r0, #0x1f                
  1a012:  lsls r1, r0, #1                   
  1a014:  lsls r0, r0, #9                   
  1a016:  movs r3, #1                       
  1a018:  lsrs r0, r0, #9                   
  1a01a:  lsls r3, r3, #0x17                
  1a01c:  lsls r2, r2, #0x1f                
  1a01e:  lsrs r1, r1, #0x18                
  1a020:  adds r0, r0, r3                   
  1a022:  cmp r1, #0x7f                     
  1a024:  bge #0x1a02a                      
  1a026:  movs r0, #0                       
  1a028:  bx lr                             
  1a02a:  cmp r1, #0x96                     
  1a02c:  bgt #0x1a036                      
  1a02e:  movs r3, #0x96                    
  1a030:  subs r1, r3, r1                   
  1a032:  lsrs r0, r1                       
  1a034:  b #0x1a03a                        -> 0x1a03a (вне списка функций)
  1a036:  subs r1, #0x96                    
  1a038:  lsls r0, r1                       
  1a03a:  cmp r2, #0                        
  1a03c:  beq #0x1a028                      
  1a03e:  rsbs r0, r0, #0                   
  1a040:  bx lr                             
```
