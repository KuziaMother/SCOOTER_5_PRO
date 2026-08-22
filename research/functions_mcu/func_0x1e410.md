# func_0x1e410

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e410) | `0x0001e410` |
| размер кода | 106 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0000a6c6 — данные @0x0a6c6 (r0)

## Вызовы (callees)

- 0x1e44c (b, вне списка функций)
- 0x1e456 (b, вне списка функций)
- 0x1e476 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1d7ac` (bl @0x0001d7b2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1e442..0x1e44c` (10 Б); цели из: 0x1e438
- `0x1e44c..0x1e456` (10 Б); цели из: 0x1e440
- `0x1e456..0x1e45a` (4 Б); цели из: 0x1e44a
- `0x1e45a..0x1e46a` (16 Б); цели из: 0x1e42c
- `0x1e46a..0x1e476` (12 Б); цели из: 0x1e432
- `0x1e476..0x1e47a` (4 Б); цели из: 0x1e43e, 0x1e458, 0x1e468

## Дизассембляция

```asm
  1e410:  push {r3, r4, lr}                 
  1e412:  lsls r1, r0, #0x10                
  1e414:  movs r2, #3                       
  1e416:  lsls r0, r0, #0x12                
  1e418:  lsrs r1, r1, #0x16                
  1e41a:  lsls r2, r2, #8                   
  1e41c:  lsrs r3, r0, #0x18                
  1e41e:  ands r1, r2                       
  1e420:  lsls r2, r3, #1                   
  1e422:  movs r4, #0xff                    
  1e424:  subs r3, r4, r3                   
  1e426:  ldr r0, [pc, #0x54]               -> данные @0x0a6c6
  1e428:  lsls r3, r3, #1                   
  1e42a:  cmp r1, #0                        
  1e42c:  beq #0x1e45a                      
  1e42e:  subs r1, #0xff                    
  1e430:  subs r1, r1, #1                   
  1e432:  beq #0x1e46a                      
  1e434:  subs r1, #0xff                    
  1e436:  subs r1, r1, #1                   
  1e438:  beq #0x1e442                      
  1e43a:  subs r1, #0xff                    
  1e43c:  cmp r1, #1                        
  1e43e:  bne #0x1e476                      
  1e440:  b #0x1e44c                        -> 0x1e44c (вне списка функций)
  1e442:  ldrh r2, [r0, r2]                 
  1e444:  mov r1, sp                        
  1e446:  strh r2, [r1, #2]                 
  1e448:  ldrh r0, [r0, r3]                 
  1e44a:  b #0x1e456                        -> 0x1e456 (вне списка функций)
  1e44c:  ldrh r3, [r0, r3]                 
  1e44e:  mov r1, sp                        
  1e450:  strh r3, [r1, #2]                 
  1e452:  ldrh r0, [r0, r2]                 
  1e454:  rsbs r0, r0, #0                   
  1e456:  strh r0, [r1]                     
  1e458:  b #0x1e476                        -> 0x1e476 (вне списка функций)
  1e45a:  ldrh r1, [r0, r2]                 
  1e45c:  mov r2, sp                        
  1e45e:  rsbs r1, r1, #0                   
  1e460:  strh r1, [r2, #2]                 
  1e462:  ldrh r0, [r0, r3]                 
  1e464:  rsbs r0, r0, #0                   
  1e466:  strh r0, [r2]                     
  1e468:  b #0x1e476                        -> 0x1e476 (вне списка функций)
  1e46a:  ldrh r1, [r0, r3]                 
  1e46c:  mov r3, sp                        
  1e46e:  rsbs r1, r1, #0                   
  1e470:  strh r1, [r3, #2]                 
  1e472:  ldrh r0, [r0, r2]                 
  1e474:  strh r0, [r3]                     
  1e476:  ldr r0, [sp]                      
  1e478:  pop {r3, r4, pc}                  
  ; --- literal-пул @0x1e47c (1 слов) — ВНЕ границ функции ---
  1e47c:  .word 0x0000a6c6  ; данные @0x0a6c6
```
