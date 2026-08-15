# func_0x1d3d0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001d3d0) | `0x0001d3d0` |
| размер кода | 588 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200001e0 — RAM (r0)
- 0x20000229 — RAM (r4)
- 0x2000022a — RAM (r0)
- 0x20000262 — RAM (r5)
- 0x2000031e — RAM (r3)
- 0x20000328 — RAM (r4)
- 0x2000032a — RAM (r6)
- 0x200003c8 — RAM (r1)
- 0x48000c00 — периферия (r1)

## Вызовы (callees)

- 0x1d442 (b, вне списка функций)
- 0x1d4b4 (b, вне списка функций)
- 0x1d4e2 (b, вне списка функций)
- 0x1d50c (b, вне списка функций)
- 0x1d518 (b, вне списка функций)
- 0x1d526 (b, вне списка функций)
- 0x1d52a (b, вне списка функций)
- 0x1d578 (b, вне списка функций)
- 0x1d57e (b, вне списка функций)
- 0x1d584 (b, вне списка функций)
- 0x1d59c (b, вне списка функций)
- 0x1d5a2 (b, вне списка функций)
- 0x1d5a8 (b, вне списка функций)
- 0x1d5c6 (b, вне списка функций)
- 0x1d5dc (b, вне списка функций)
- 0x1d5e6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a514)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1d3f4..0x1d450` (92 Б); цели из: 0x1d3e8
- `0x1d450..0x1d480` (48 Б); цели из: 0x1d410
- `0x1d480..0x1d482` (2 Б); цели из: 0x1d45a
- `0x1d482..0x1d4e8` (102 Б); цели из: 0x1d430
- `0x1d4e8..0x1d50c` (36 Б); цели из: 0x1d488
- `0x1d50c..0x1d522` (22 Б); цели из: 0x1d4b2
- `0x1d522..0x1d524` (2 Б); цели из: 0x1d434, 0x1d484
- `0x1d524..0x1d52a` (6 Б); цели из: 0x1d438
- `0x1d52a..0x1d54c` (34 Б); цели из: 0x1d520
- `0x1d54c..0x1d574` (40 Б); цели из: 0x1d4ce
- `0x1d574..0x1d576` (2 Б); цели из: 0x1d474, 0x1d4a6
- `0x1d576..0x1d578` (2 Б); цели из: 0x1d47e, 0x1d4b0
- `0x1d578..0x1d58c` (20 Б); цели из: 0x1d572
- `0x1d58c..0x1d5a2` (22 Б); цели из: 0x1d56e
- `0x1d5a2..0x1d5a8` (6 Б); цели из: 0x1d522
- `0x1d5a8..0x1d5c6` (30 Б); цели из: 0x1d524
- `0x1d5c6..0x1d5d0` (10 Б); цели из: 0x1d500, 0x1d574
- `0x1d5d0..0x1d5dc` (12 Б); цели из: 0x1d5c4
- `0x1d5dc..0x1d5e6` (10 Б); цели из: 0x1d50a, 0x1d576
- `0x1d5e6..0x1d5f4` (14 Б); цели из: 0x1d480, 0x1d5da
- `0x1d5f4..0x1d5fe` (10 Б); цели из: 0x1d564
- `0x1d5fe..0x1d606` (8 Б); цели из: 0x1d54a
- `0x1d606..0x1d61c` (22 Б); цели из: 0x1d58a

## Дизассембляция

```asm
  1d3d0:  push {r4, r5, r6, r7, lr}         
  1d3d2:  ldr r0, [pc, #0x248]              -> RAM
  1d3d4:  ldr r1, [pc, #0x248]              -> RAM
  1d3d6:  ldrb r4, [r0]                     
  1d3d8:  ldr r0, [pc, #0x244]              -> RAM
  1d3da:  adds r1, #0x80                    
  1d3dc:  ldrb r3, [r0, #0xf]               
  1d3de:  ldr r0, [pc, #0x244]              -> RAM
  1d3e0:  mov ip, r4                        
  1d3e2:  ldr r2, [r0]                      
  1d3e4:  ldr r0, [r0, #4]                  
  1d3e6:  cmp r4, r3                        
  1d3e8:  beq #0x1d3f4                      
  1d3ea:  ldr r3, [pc, #0x234]              -> RAM
  1d3ec:  mov r4, ip                        
  1d3ee:  strb r4, [r3, #0xf]               
  1d3f0:  str r2, [r1, #0x60]               
  1d3f2:  str r0, [r1, #0x64]               
  1d3f4:  ldr r1, [pc, #0x228]              -> RAM
  1d3f6:  mov r4, r0                        
  1d3f8:  adds r1, #0x80                    
  1d3fa:  ldr r3, [r1, #0x60]               
  1d3fc:  ldr r1, [r1, #0x64]               
  1d3fe:  subs r5, r2, r3                   
  1d400:  sbcs r4, r1                       
  1d402:  movs r6, #0x7d                    
  1d404:  lsls r6, r6, #6                   
  1d406:  ldr r1, [pc, #0x220]              -> периферия
  1d408:  movs r3, #2                       
  1d40a:  movs r7, #0                       
  1d40c:  subs r5, r5, r6                   
  1d40e:  sbcs r4, r7                       
  1d410:  blo #0x1d450                      
  1d412:  ldr r5, [pc, #0x20c]              -> RAM
  1d414:  movs r4, #0                       
  1d416:  strb r4, [r5, #0xe]               
  1d418:  ldr r5, [pc, #0x210]              -> RAM
  1d41a:  mov r7, ip                        
  1d41c:  ldrb r5, [r5]                     
  1d41e:  ldr r4, [pc, #0x214]              -> RAM
  1d420:  mov ip, r5                        
  1d422:  ldrb r5, [r4]                     
  1d424:  ldr r6, [pc, #0x208]              -> RAM
  1d426:  ldr r4, [pc, #0x210]              -> RAM
  1d428:  ldrb r6, [r6]                     
  1d42a:  ldrb r4, [r4]                     
  1d42c:  cmp r7, #1                        
  1d42e:  mov r7, ip                        
  1d430:  beq #0x1d482                      
  1d432:  cmp r7, #1                        
  1d434:  beq #0x1d522                      
  1d436:  cmp r4, #0xb                      
  1d438:  beq #0x1d524                      
  1d43a:  ldr r4, [r1, #4]                  
  1d43c:  bics r4, r3                       
  1d43e:  str r4, [r1, #4]                  
  1d440:  movs r1, #0                       
  1d442:  ldr r3, [pc, #0x1f8]              -> RAM
  1d444:  strb r1, [r3]                     
  1d446:  ldr r1, [pc, #0x1d8]              -> RAM
  1d448:  adds r1, #0x80                    
  1d44a:  str r2, [r1, #0x50]               
  1d44c:  str r0, [r1, #0x54]               
  1d44e:  b #0x1d4e2                        -> 0x1d4e2 (вне списка функций)
  1d450:  ldr r5, [pc, #0x1cc]              -> RAM
  1d452:  movs r4, #1                       
  1d454:  strb r4, [r5, #0xe]               
  1d456:  mov r4, ip                        
  1d458:  cmp r4, #1                        
  1d45a:  bne #0x1d480                      
  1d45c:  mov r4, r5                        
  1d45e:  adds r4, #0x80                    
  1d460:  ldr r5, [r4, #0x50]               
  1d462:  ldr r6, [r4, #0x54]               
  1d464:  mov r4, r0                        
  1d466:  subs r5, r2, r5                   
  1d468:  sbcs r4, r6                       
  1d46a:  movs r6, #8                       
  1d46c:  mov ip, r4                        
  1d46e:  movs r7, #0                       
  1d470:  subs r6, r5, r6                   
  1d472:  sbcs r4, r7                       
  1d474:  blo #0x1d574                      
  1d476:  movs r6, #0x1e                    
  1d478:  mov r4, ip                        
  1d47a:  subs r5, r5, r6                   
  1d47c:  sbcs r4, r7                       
  1d47e:  blo #0x1d576                      
  1d480:  b #0x1d5e6                        -> 0x1d5e6 (вне списка функций)
  1d482:  cmp r7, #1                        
  1d484:  beq #0x1d522                      
  1d486:  cmp r5, #1                        
  1d488:  beq #0x1d4e8                      
  1d48a:  cmp r4, #0xb                      
  1d48c:  beq #0x1d530                      
  1d48e:  ldr r4, [pc, #0x190]              -> RAM
  1d490:  movs r7, #0                       
  1d492:  adds r4, #0x80                    
  1d494:  ldr r5, [r4, #0x50]               
  1d496:  ldr r6, [r4, #0x54]               
  1d498:  mov r4, r0                        
  1d49a:  subs r5, r2, r5                   
  1d49c:  sbcs r4, r6                       
  1d49e:  movs r6, #8                       
  1d4a0:  mov ip, r4                        
  1d4a2:  subs r6, r5, r6                   
  1d4a4:  sbcs r4, r7                       
  1d4a6:  blo #0x1d574                      
  1d4a8:  movs r6, #0x1e                    
  1d4aa:  mov r4, ip                        
  1d4ac:  subs r5, r5, r6                   
  1d4ae:  sbcs r4, r7                       
  1d4b0:  blo #0x1d576                      
  1d4b2:  b #0x1d50c                        -> 0x1d50c (вне списка функций)
  1d4b4:  ldr r4, [pc, #0x168]              -> RAM
  1d4b6:  movs r7, #0                       
  1d4b8:  adds r4, #0x80                    
  1d4ba:  ldr r5, [r4, #0x58]               
  1d4bc:  ldr r6, [r4, #0x5c]               
  1d4be:  mov r4, r0                        
  1d4c0:  subs r5, r2, r5                   
  1d4c2:  sbcs r4, r6                       
  1d4c4:  movs r6, #0x19                    
  1d4c6:  lsls r6, r6, #6                   
  1d4c8:  mov ip, r4                        
  1d4ca:  subs r6, r5, r6                   
  1d4cc:  sbcs r4, r7                       
  1d4ce:  blo #0x1d54c                      
  1d4d0:  movs r6, #0x19                    
  1d4d2:  mov r4, ip                        
  1d4d4:  lsls r6, r6, #7                   
  1d4d6:  b #0x1d584                        -> 0x1d584 (вне списка функций)
  1d4d8:  ldr r4, [r1, #4]                  
  1d4da:  orrs r4, r3                       
  1d4dc:  str r4, [r1, #4]                  
  1d4de:  movs r1, #1                       
  1d4e0:  b #0x1d442                        -> 0x1d442 (вне списка функций)
  1d4e2:  str r2, [r1, #0x58]               
  1d4e4:  str r0, [r1, #0x5c]               
  1d4e6:  pop {r4, r5, r6, r7, pc}          
  1d4e8:  ldr r5, [pc, #0x134]              -> RAM
  1d4ea:  movs r7, #0                       
  1d4ec:  adds r5, #0x80                    
  1d4ee:  ldr r4, [r5, #0x50]               
  1d4f0:  ldr r6, [r5, #0x54]               
  1d4f2:  mov r5, r0                        
  1d4f4:  subs r4, r2, r4                   
  1d4f6:  sbcs r5, r6                       
  1d4f8:  movs r6, #8                       
  1d4fa:  mov ip, r5                        
  1d4fc:  subs r6, r4, r6                   
  1d4fe:  sbcs r5, r7                       
  1d500:  blo #0x1d5c6                      
  1d502:  movs r6, #0x1e                    
  1d504:  mov r5, ip                        
  1d506:  subs r4, r4, r6                   
  1d508:  sbcs r5, r7                       
  1d50a:  blo #0x1d5dc                      
  1d50c:  ldr r4, [r1, #4]                  
  1d50e:  bics r4, r3                       
  1d510:  str r4, [r1, #4]                  
  1d512:  ldr r1, [pc, #0x128]              -> RAM
  1d514:  movs r3, #0                       
  1d516:  strb r3, [r1]                     
  1d518:  ldr r1, [pc, #0x104]              -> RAM
  1d51a:  adds r1, #0x80                    
  1d51c:  str r2, [r1, #0x50]               
  1d51e:  str r0, [r1, #0x54]               
  1d520:  b #0x1d52a                        -> 0x1d52a (вне списка функций)
  1d522:  b #0x1d5a2                        -> 0x1d5a2 (вне списка функций)
  1d524:  b #0x1d5a8                        -> 0x1d5a8 (вне списка функций)
  1d526:  ldr r3, [pc, #0x114]              -> RAM
  1d528:  strb r1, [r3]                     
  1d52a:  ldr r1, [pc, #0xf4]               -> RAM
  1d52c:  adds r1, #0x80                    
  1d52e:  b #0x1d4e2                        -> 0x1d4e2 (вне списка функций)
  1d530:  ldr r4, [pc, #0xec]               -> RAM
  1d532:  movs r7, #0                       
  1d534:  adds r4, #0x80                    
  1d536:  ldr r5, [r4, #0x58]               
  1d538:  ldr r6, [r4, #0x5c]               
  1d53a:  mov r4, r0                        
  1d53c:  subs r5, r2, r5                   
  1d53e:  sbcs r4, r6                       
  1d540:  movs r6, #0x19                    
  1d542:  lsls r6, r6, #8                   
  1d544:  mov ip, r4                        
  1d546:  subs r6, r5, r6                   
  1d548:  sbcs r4, r7                       
  1d54a:  bhs #0x1d5fe                      
  1d54c:  ldr r4, [pc, #0xd0]               -> RAM
  1d54e:  movs r7, #0                       
  1d550:  adds r4, #0x80                    
  1d552:  ldr r5, [r4, #0x50]               
  1d554:  ldr r6, [r4, #0x54]               
  1d556:  mov r4, r0                        
  1d558:  subs r5, r2, r5                   
  1d55a:  sbcs r4, r6                       
  1d55c:  movs r6, #8                       
  1d55e:  mov ip, r4                        
  1d560:  subs r6, r5, r6                   
  1d562:  sbcs r4, r7                       
  1d564:  blo #0x1d5f4                      
  1d566:  movs r6, #0x1e                    
  1d568:  mov r4, ip                        
  1d56a:  subs r5, r5, r6                   
  1d56c:  sbcs r4, r7                       
  1d56e:  bhs #0x1d58c                      
  1d570:  ldr r0, [r1, #4]                  
  1d572:  b #0x1d578                        -> 0x1d578 (вне списка функций)
  1d574:  b #0x1d5c6                        -> 0x1d5c6 (вне списка функций)
  1d576:  b #0x1d5dc                        -> 0x1d5dc (вне списка функций)
  1d578:  bics r0, r3                       
  1d57a:  str r0, [r1, #4]                  
  1d57c:  movs r0, #0                       
  1d57e:  ldr r1, [pc, #0xbc]               -> RAM
  1d580:  strb r0, [r1]                     
  1d582:  pop {r4, r5, r6, r7, pc}          
  1d584:  movs r7, #0                       
  1d586:  subs r5, r5, r6                   
  1d588:  sbcs r4, r7                       
  1d58a:  bhs #0x1d606                      
  1d58c:  ldr r4, [r1, #4]                  
  1d58e:  bics r4, r3                       
  1d590:  str r4, [r1, #4]                  
  1d592:  ldr r3, [pc, #0xa8]               -> RAM
  1d594:  movs r1, #0                       
  1d596:  strb r1, [r3]                     
  1d598:  ldr r1, [pc, #0x84]               -> RAM
  1d59a:  adds r1, #0x80                    
  1d59c:  str r2, [r1, #0x50]               
  1d59e:  str r0, [r1, #0x54]               
  1d5a0:  pop {r4, r5, r6, r7, pc}          
  1d5a2:  cmp r6, #1                        
  1d5a4:  bne #0x1d4d8                      
  1d5a6:  b #0x1d4b4                        -> 0x1d4b4 (вне списка функций)
  1d5a8:  cmp r5, #1                        
  1d5aa:  bne #0x1d530                      
  1d5ac:  ldr r5, [pc, #0x70]               -> RAM
  1d5ae:  movs r7, #0                       
  1d5b0:  adds r5, #0x80                    
  1d5b2:  ldr r4, [r5, #0x50]               
  1d5b4:  ldr r6, [r5, #0x54]               
  1d5b6:  mov r5, r0                        
  1d5b8:  subs r4, r2, r4                   
  1d5ba:  sbcs r5, r6                       
  1d5bc:  movs r6, #8                       
  1d5be:  mov ip, r5                        
  1d5c0:  subs r6, r4, r6                   
  1d5c2:  sbcs r5, r7                       
  1d5c4:  bhs #0x1d5d0                      
  1d5c6:  ldr r4, [r1, #4]                  
  1d5c8:  orrs r4, r3                       
  1d5ca:  str r4, [r1, #4]                  
  1d5cc:  movs r1, #1                       
  1d5ce:  b #0x1d526                        -> 0x1d526 (вне списка функций)
  1d5d0:  movs r6, #0x1e                    
  1d5d2:  mov r5, ip                        
  1d5d4:  movs r7, #0                       
  1d5d6:  subs r4, r4, r6                   
  1d5d8:  sbcs r5, r7                       
  1d5da:  bhs #0x1d5e6                      
  1d5dc:  ldr r4, [r1, #4]                  
  1d5de:  bics r4, r3                       
  1d5e0:  str r4, [r1, #4]                  
  1d5e2:  movs r1, #0                       
  1d5e4:  b #0x1d526                        -> 0x1d526 (вне списка функций)
  1d5e6:  ldr r4, [r1, #4]                  
  1d5e8:  bics r4, r3                       
  1d5ea:  str r4, [r1, #4]                  
  1d5ec:  ldr r3, [pc, #0x4c]               -> RAM
  1d5ee:  movs r1, #0                       
  1d5f0:  strb r1, [r3]                     
  1d5f2:  b #0x1d518                        -> 0x1d518 (вне списка функций)
  1d5f4:  ldr r0, [r1, #4]                  
  1d5f6:  orrs r0, r3                       
  1d5f8:  str r0, [r1, #4]                  
  1d5fa:  movs r0, #1                       
  1d5fc:  b #0x1d57e                        -> 0x1d57e (вне списка функций)
  1d5fe:  movs r6, #0x19                    
  1d600:  mov r4, ip                        
  1d602:  lsls r6, r6, #9                   
  1d604:  b #0x1d584                        -> 0x1d584 (вне списка функций)
  1d606:  ldr r4, [r1, #4]                  
  1d608:  bics r4, r3                       
  1d60a:  str r4, [r1, #4]                  
  1d60c:  ldr r3, [pc, #0x2c]               -> RAM
  1d60e:  movs r1, #0                       
  1d610:  strb r1, [r3]                     
  1d612:  ldr r1, [pc, #0xc]                -> RAM
  1d614:  adds r1, #0x80                    
  1d616:  str r2, [r1, #0x58]               
  1d618:  str r0, [r1, #0x5c]               
  1d61a:  b #0x1d59c                        -> 0x1d59c (вне списка функций)
  ; --- literal-пул @0x1d61c (9 слов) — ВНЕ границ функции ---
  1d61c:  .word 0x2000022a  ; RAM
  1d620:  .word 0x200003c8  ; RAM
  1d624:  .word 0x200001e0  ; RAM
  1d628:  .word 0x48000c00  ; периферия
  1d62c:  .word 0x20000262  ; RAM
  1d630:  .word 0x2000032a  ; RAM
  1d634:  .word 0x20000328  ; RAM
  1d638:  .word 0x20000229  ; RAM
  1d63c:  .word 0x2000031e  ; RAM
```
