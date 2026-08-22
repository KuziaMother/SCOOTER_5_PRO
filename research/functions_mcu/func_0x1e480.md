# func_0x1e480

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e480) | `0x0001e480` |
| размер кода | 180 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000400 — данные @0x00400 (r2)
- 0x20000030 — RAM (r0)
- 0x200002bc — RAM (r2)
- 0x200002be — RAM (r2)
- 0x200002bf — RAM (r3)
- 0x20000881 — RAM (r5)
- 0x40004800 — периферия (r0)
- 0x40004840 — периферия (r1)
- 0xd0142943 — прочее (r4)

## Вызовы (callees)

- 0x1e4d6 (b, вне списка функций)
- 0x21b52 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1e498..0x1e4b0` (24 Б); цели из: 0x1e48a, 0x1e490
- `0x1e4b0..0x1e4be` (14 Б); цели из: 0x1e496
- `0x1e4be..0x1e4d8` (26 Б); цели из: 0x1e4b6
- `0x1e4d8..0x1e534` (92 Б); цели из: 0x1e4bc

## Дизассембляция

```asm
  1e480:  push {r2, r3, r4, r5, r6, r7, lr} 
  1e482:  ldr r0, [pc, #0x1ac]              -> периферия
  1e484:  ldr r1, [r0, #0x3c]               
  1e486:  lsls r2, r1, #0x1f                
  1e488:  ldr r1, [pc, #0x1a8]              -> периферия
  1e48a:  bne #0x1e498                      
  1e48c:  ldr r2, [r0, #0x3c]               
  1e48e:  lsls r2, r2, #0x1b                
  1e490:  bmi #0x1e498                      
  1e492:  ldr r2, [r0, #0x3c]               
  1e494:  lsls r2, r2, #0x17                
  1e496:  bpl #0x1e4b0                      
  1e498:  ldr r2, [r1]                      
  1e49a:  movs r3, #1                       
  1e49c:  orrs r2, r3                       
  1e49e:  str r2, [r1]                      
  1e4a0:  ldr r2, [r1]                      
  1e4a2:  movs r3, #0x10                    
  1e4a4:  orrs r2, r3                       
  1e4a6:  str r2, [r1]                      
  1e4a8:  ldr r2, [r1]                      
  1e4aa:  lsls r3, r3, #4                   
  1e4ac:  orrs r2, r3                       
  1e4ae:  str r2, [r1]                      
  1e4b0:  ldr r2, [r0, #0x3c]               
  1e4b2:  lsls r3, r2, #0x13                
  1e4b4:  ldr r2, [pc, #0x180]              -> данные @0x00400
  1e4b6:  bmi #0x1e4be                      
  1e4b8:  ldr r3, [r0, #0x3c]               
  1e4ba:  lsls r3, r3, #0x14                
  1e4bc:  bpl #0x1e4d8                      
  1e4be:  ldr r0, [r1]                      
  1e4c0:  orrs r0, r2                       
  1e4c2:  str r0, [r1]                      
  1e4c4:  ldr r0, [r1]                      
  1e4c6:  movs r2, #1                       
  1e4c8:  lsls r2, r2, #0xc                 
  1e4ca:  orrs r0, r2                       
  1e4cc:  str r0, [r1]                      
  1e4ce:  ldr r0, [r1]                      
  1e4d0:  asrs r2, r2, #1                   
  1e4d2:  orrs r0, r2                       
  1e4d4:  str r0, [r1]                      
  1e4d6:  pop {r2, r3, r4, r5, r6, r7, pc}  
  1e4d8:  ldr r3, [r0, #0x3c]               
  1e4da:  lsls r3, r3, #0x15                
  1e4dc:  bpl #0x1e4d6                      
  1e4de:  ldr r3, [r1]                      
  1e4e0:  orrs r3, r2                       
  1e4e2:  str r3, [r1]                      
  1e4e4:  ldr r0, [r0]                      
  1e4e6:  ldr r2, [pc, #0x154]              -> RAM
  1e4e8:  uxtb r1, r0                       
  1e4ea:  movs r0, #0                       
  1e4ec:  strh r0, [r2]                     
  1e4ee:  ldr r0, [pc, #0x154]              -> RAM
  1e4f0:  ldr r2, [pc, #0x14c]              -> RAM
  1e4f2:  ldrh r3, [r0, #8]                 
  1e4f4:  ldrb r7, [r2]                     
  1e4f6:  mov r6, r3                        
  1e4f8:  adds r3, r3, #1                   
  1e4fa:  uxth r4, r3                       
  1e4fc:  ldr r3, [pc, #0x148]              -> RAM
  1e4fe:  ldrb r3, [r3]                     
  1e500:  adds r5, r3, #1                   
  1e502:  uxtb r5, r5                       
  1e504:  str r5, [sp]                      
  1e506:  movs r5, #0x96                    
  1e508:  muls r3, r5, r3                   
  1e50a:  ldr r5, [pc, #0x140]              -> RAM
  1e50c:  str r3, [sp, #4]                  
  1e50e:  adds r5, r3, r5                   
  1e510:  movs r3, r7                       
  1e512:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1e516:  lsrs r2, r3, #0x1c                
  1e518:  subs r6, #0x17                    
  1e51a:  str r4, [r0, r5]                  
  1e51c:  lsrs r5, r2, #0x19                
  1e51e:  lsrs r6, r1, #0x18                
  1e520:  ldr r4, [pc, #0x38]               
  1e522:  lsrs r6, r1, #0x18                
  1e524:  lsrs r6, r1, #0x18                
  1e526:  lsrs r6, r1, #0x18                
  1e528:  lsrs r6, r1, #0x18                
  1e52a:  str r6, [r1, #0x40]               
  1e52c:  ldr r2, [r5, #0x54]               
  1e52e:  ldrb r3, [r6, #5]                 
  1e530:  lsrs r0, r0, #0x1a                
  1e532:  b #0x1e4d6                        -> 0x1e4d6 (вне списка функций)
  ; --- literal-пул @0x1e55c (1 слов) — ВНЕ границ функции ---
  1e55c:  .word 0xd0142943
  ; --- literal-пул @0x1e630 (8 слов) — ВНЕ границ функции ---
  1e630:  .word 0x40004800  ; периферия
  1e634:  .word 0x40004840  ; периферия
  1e638:  .word 0x00000400  ; данные @0x00400
  1e63c:  .word 0x200002bc  ; RAM
  1e640:  .word 0x200002be  ; RAM
  1e644:  .word 0x20000030  ; RAM
  1e648:  .word 0x200002bf  ; RAM
  1e64c:  .word 0x20000881  ; RAM
```
