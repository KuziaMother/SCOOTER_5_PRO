# func_0x1a24c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a24c) | `0x0001a24c` |
| размер кода | 86 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x1a270 (b, вне списка функций)
- 0x1a27a (b, вне списка функций)
- 0x1a296 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1a25e..0x1a270` (18 Б); цели из: 0x1a258
- `0x1a270..0x1a284` (20 Б); цели из: 0x1a260, 0x1a266
- `0x1a284..0x1a296` (18 Б); цели из: 0x1a276
- `0x1a296..0x1a29a` (4 Б); цели из: 0x1a28c
- `0x1a29a..0x1a2a2` (8 Б); цели из: 0x1a27c

## Дизассембляция

```asm
  1a24c:  push {r4, r5, r6, lr}             
  1a24e:  adds r4, r1, r2                   
  1a250:  ldrb r5, [r0]                     
  1a252:  adds r0, r0, #1                   
  1a254:  lsls r3, r5, #0x1d                
  1a256:  lsrs r3, r3, #0x1d                
  1a258:  bne #0x1a25e                      
  1a25a:  ldrb r3, [r0]                     
  1a25c:  adds r0, r0, #1                   
  1a25e:  asrs r2, r5, #4                   
  1a260:  bne #0x1a270                      
  1a262:  ldrb r2, [r0]                     
  1a264:  adds r0, r0, #1                   
  1a266:  b #0x1a270                        -> 0x1a270 (вне списка функций)
  1a268:  ldrb r6, [r0]                     
  1a26a:  strb r6, [r1]                     
  1a26c:  adds r0, r0, #1                   
  1a26e:  adds r1, r1, #1                   
  1a270:  subs r3, r3, #1                   
  1a272:  bne #0x1a268                      
  1a274:  lsls r3, r5, #0x1c                
  1a276:  bmi #0x1a284                      
  1a278:  movs r3, #0                       
  1a27a:  subs r2, r2, #1                   
  1a27c:  bmi #0x1a29a                      
  1a27e:  strb r3, [r1]                     
  1a280:  adds r1, r1, #1                   
  1a282:  b #0x1a27a                        -> 0x1a27a (вне списка функций)
  1a284:  ldrb r3, [r0]                     
  1a286:  adds r0, r0, #1                   
  1a288:  subs r3, r1, r3                   
  1a28a:  adds r2, r2, #2                   
  1a28c:  b #0x1a296                        -> 0x1a296 (вне списка функций)
  1a28e:  ldrb r5, [r3]                     
  1a290:  strb r5, [r1]                     
  1a292:  adds r1, r1, #1                   
  1a294:  adds r3, r3, #1                   
  1a296:  subs r2, r2, #1                   
  1a298:  bpl #0x1a28e                      
  1a29a:  cmp r1, r4                        
  1a29c:  blo #0x1a250                      
  1a29e:  movs r0, #0                       
  1a2a0:  pop {r4, r5, r6, pc}              
```
