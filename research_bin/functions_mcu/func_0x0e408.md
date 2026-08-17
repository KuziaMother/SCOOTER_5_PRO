# func_0x0e408

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e408) | `0x0000e408` |
| размер кода | 566 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xffff8000 — прочее (r4)

## Вызовы (callees)

- 0x0e452 (b, вне списка функций)
- 0x0e46e (b, вне списка функций)
- 0x0e484 (b, вне списка функций)
- 0x0e526 (b, вне списка функций)
- 0x0e580 (b, вне списка функций)
- 0x0e58e (b, вне списка функций)
- 0x0e5ae (b, вне списка функций)
- 0x0e5c6 (b, вне списка функций)
- 0x0e608 (b, вне списка функций)
- 0x0e60e (b, вне списка функций)
- 0x0e63a (b, вне списка функций)
- 0x0e644 (bl, вне списка функций)
- 0x0e64a (bl, вне списка функций)
- 0x0e650 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x07a30` (bl @0x00007b8a)
- `func_0x07a30` (bl @0x00007bda)
- `func_0x07a30` (bl @0x00007c28)
- `func_0x07a30` (bl @0x00007c70)
- `func_0x07a30` (bl @0x00007cc0)
- `func_0x07a30` (bl @0x00007d0e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0e436..0x0e442` (12 Б); цели из: 0x0e42c
- `0x0e442..0x0e44e` (12 Б); цели из: 0x0e438
- `0x0e44e..0x0e452` (4 Б); цели из: 0x0e444
- `0x0e452..0x0e466` (20 Б); цели из: 0x0e434, 0x0e440, 0x0e44c
- `0x0e466..0x0e46e` (8 Б); цели из: 0x0e45e
- `0x0e46e..0x0e47c` (14 Б); цели из: 0x0e464, 0x0e46a
- `0x0e47c..0x0e484` (8 Б); цели из: 0x0e474
- `0x0e484..0x0e490` (12 Б); цели из: 0x0e47a, 0x0e480
- `0x0e490..0x0e4aa` (26 Б); цели из: 0x0e48c
- `0x0e4aa..0x0e4b6` (12 Б); цели из: 0x0e496, 0x0e4a2
- `0x0e4b6..0x0e4e0` (42 Б); цели из: 0x0e41c, 0x0e420
- `0x0e4e0..0x0e4e4` (4 Б); цели из: 0x0e4da
- `0x0e4e4..0x0e4f2` (14 Б); цели из: 0x0e4ce
- `0x0e4f2..0x0e502` (16 Б); цели из: 0x0e4e8
- `0x0e502..0x0e512` (16 Б); цели из: 0x0e4f8
- `0x0e512..0x0e522` (16 Б); цели из: 0x0e508
- `0x0e522..0x0e526` (4 Б); цели из: 0x0e51a
- `0x0e526..0x0e53e` (24 Б); цели из: 0x0e4f0, 0x0e500, 0x0e510, 0x0e520
- `0x0e53e..0x0e54e` (16 Б); цели из: 0x0e538
- `0x0e54e..0x0e562` (20 Б); цели из: 0x0e54a
- `0x0e562..0x0e56a` (8 Б); цели из: 0x0e554, 0x0e55a
- `0x0e56a..0x0e57c` (18 Б); цели из: 0x0e4ba, 0x0e4be
- `0x0e57c..0x0e580` (4 Б); цели из: 0x0e570
- `0x0e580..0x0e58c` (12 Б); цели из: 0x0e57a
- `0x0e58c..0x0e58e` (2 Б); цели из: 0x0e586
- `0x0e58e..0x0e5ae` (32 Б); цели из: 0x0e58a
- `0x0e5ae..0x0e5be` (16 Б); цели из: 0x0e5aa
- `0x0e5be..0x0e5c6` (8 Б); цели из: 0x0e5b6
- `0x0e5c6..0x0e5da` (20 Б); цели из: 0x0e5bc, 0x0e5c2
- `0x0e5da..0x0e5f2` (24 Б); цели из: 0x0e5cc, 0x0e5d2
- `0x0e5f2..0x0e5fe` (12 Б); цели из: 0x0e5e0, 0x0e5ea
- `0x0e5fe..0x0e608` (10 Б); цели из: 0x0e5f8
- `0x0e608..0x0e60e` (6 Б); цели из: 0x0e5d8, 0x0e5f0, 0x0e5fc, 0x0e602
- `0x0e60e..0x0e622` (20 Б); цели из: 0x0e4a8, 0x0e4b4, 0x0e560, 0x0e568
- `0x0e622..0x0e632` (16 Б); цели из: 0x0e618
- `0x0e632..0x0e63a` (8 Б); цели из: 0x0e628
- `0x0e63a..0x0e63e` (4 Б); цели из: 0x0e620, 0x0e630

## Дизассембляция

```asm
  0e408:  push.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  0e40c:  mov r7, r0                        
  0e40e:  mov r6, r1                        
  0e410:  mov r8, r2                        
  0e412:  mov sb, r3                        
  0e414:  ldr.w sl, [sp, #0x34]             
  0e418:  cmp.w sb, #0                      
  0e41c:  ble #0xe4b6                       
  0e41e:  cmp r7, r6                        
  0e420:  bge #0xe4b6                       
  0e422:  sxth r5, r7                       
  0e424:  subs r0, r6, r5                   
  0e426:  sxth r4, r0                       
  0e428:  cmp.w sb, #0x14                   
  0e42c:  bge #0xe436                       
  0e42e:  add r0, sp, #8                    
  0e430:  bl #0xe650                        -> 0x0e650 (вне списка функций)
  0e434:  b #0xe452                         -> 0x0e452 (вне списка функций)
  0e436:  cmp r4, #9                        
  0e438:  bge #0xe442                       
  0e43a:  add r0, sp, #8                    
  0e43c:  bl #0xe644                        -> 0x0e644 (вне списка функций)
  0e440:  b #0xe452                         -> 0x0e452 (вне списка функций)
  0e442:  cmp r4, #0x32                     
  0e444:  bge #0xe44e                       
  0e446:  add r0, sp, #8                    
  0e448:  bl #0xe64a                        -> 0x0e64a (вне списка функций)
  0e44c:  b #0xe452                         -> 0x0e452 (вне списка функций)
  0e44e:  movs r0, #5                       
  0e450:  str r0, [sp, #8]                  
  0e452:  ldrsh.w r0, [sp, #8]              
  0e456:  mul r4, r8, r0                    
  0e45a:  cmp.w r4, #0x8000                 
  0e45e:  blt #0xe466                       
  0e460:  movw r4, #0x7fff                  
  0e464:  b #0xe46e                         -> 0x0e46e (вне списка функций)
  0e466:  cmn.w r4, #0x8000                 
  0e46a:  bge #0xe46e                       
  0e46c:  ldr r4, [pc, #0x1d0]              
  0e46e:  add r4, r5                        
  0e470:  cmp.w r4, #0x8000                 
  0e474:  blt #0xe47c                       
  0e476:  movw r4, #0x7fff                  
  0e47a:  b #0xe484                         -> 0x0e484 (вне списка функций)
  0e47c:  cmn.w r4, #0x8000                 
  0e480:  bge #0xe484                       
  0e482:  ldr r4, [pc, #0x1bc]              
  0e484:  sxth r0, r4                       
  0e486:  str r0, [sp, #8]                  
  0e488:  sxth r0, r4                       
  0e48a:  cmp r0, r6                        
  0e48c:  blt #0xe490                       
  0e48e:  str r6, [sp, #8]                  
  0e490:  movw r0, #0x26d4                  
  0e494:  cmp r5, r0                        
  0e496:  bgt #0xe4aa                       
  0e498:  ldrsh.w r0, [sp, #8]              
  0e49c:  movw r1, #0x26d4                  
  0e4a0:  cmp r0, r1                        
  0e4a2:  ble #0xe4aa                       
  0e4a4:  mov r0, r1                        
  0e4a6:  str r0, [sp, #8]                  
  0e4a8:  b #0xe60e                         -> 0x0e60e (вне списка функций)
  0e4aa:  movw r0, #0x26d4                  
  0e4ae:  cmp r5, r0                        
  0e4b0:  ble #0xe4a8                       
  0e4b2:  str r5, [sp, #8]                  
  0e4b4:  b #0xe60e                         -> 0x0e60e (вне списка функций)
  0e4b6:  cmp.w sb, #0                      
  0e4ba:  bge #0xe56a                       
  0e4bc:  cmp r7, r6                        
  0e4be:  ble #0xe56a                       
  0e4c0:  sxth r5, r7                       
  0e4c2:  subs r0, r5, r6                   
  0e4c4:  sxth r0, r0                       
  0e4c6:  str r0, [sp, #8]                  
  0e4c8:  ldrsh.w r0, [sp, #8]              
  0e4cc:  cmp r0, #0                        
  0e4ce:  bge #0xe4e4                       
  0e4d0:  ldrsh.w r0, [sp, #8]              
  0e4d4:  rsbs r4, r0, #0                   
  0e4d6:  cmp.w r4, #0x8000                 
  0e4da:  blt #0xe4e0                       
  0e4dc:  movw r4, #0x7fff                  
  0e4e0:  sxth r0, r4                       
  0e4e2:  str r0, [sp, #8]                  
  0e4e4:  cmn.w sb, #0x14                   
  0e4e8:  ble #0xe4f2                       
  0e4ea:  add r0, sp, #8                    
  0e4ec:  bl #0xe644                        -> 0x0e644 (вне списка функций)
  0e4f0:  b #0xe526                         -> 0x0e526 (вне списка функций)
  0e4f2:  ldrsh.w r0, [sp, #8]              
  0e4f6:  cmp r0, #9                        
  0e4f8:  bge #0xe502                       
  0e4fa:  add r0, sp, #8                    
  0e4fc:  bl #0xe650                        -> 0x0e650 (вне списка функций)
  0e500:  b #0xe526                         -> 0x0e526 (вне списка функций)
  0e502:  ldrsh.w r0, [sp, #8]              
  0e506:  cmp r0, #0xc8                     
  0e508:  bge #0xe512                       
  0e50a:  add r0, sp, #8                    
  0e50c:  bl #0xe64a                        -> 0x0e64a (вне списка функций)
  0e510:  b #0xe526                         -> 0x0e526 (вне списка функций)
  0e512:  ldrsh.w r0, [sp, #8]              
  0e516:  cmp.w r0, #0x190                  
  0e51a:  bge #0xe522                       
  0e51c:  movs r0, #3                       
  0e51e:  str r0, [sp, #8]                  
  0e520:  b #0xe526                         -> 0x0e526 (вне списка функций)
  0e522:  movs r0, #7                       
  0e524:  str r0, [sp, #8]                  
  0e526:  movs r1, #0xa                     
  0e528:  ldr r0, [sp, #0x30]               
  0e52a:  udiv r0, r0, r1                   
  0e52e:  sxth.w fp, r0                     
  0e532:  ldrsh.w r0, [sp, #8]              
  0e536:  cmp r0, fp                        
  0e538:  bge #0xe53e                       
  0e53a:  str.w fp, [sp, #8]                
  0e53e:  ldrh.w r1, [sp, #8]               
  0e542:  mla r0, r8, r1, r5                
  0e546:  sxth r5, r0                       
  0e548:  cmp r5, r6                        
  0e54a:  bgt #0xe54e                       
  0e54c:  mov r5, r6                        
  0e54e:  uxth r0, r5                       
  0e550:  str r0, [sp, #4]                  
  0e552:  cmp r7, #0x64                     
  0e554:  blt #0xe562                       
  0e556:  ldr r0, [sp, #4]                  
  0e558:  cmp r0, #0x64                     
  0e55a:  bge #0xe562                       
  0e55c:  movs r0, #0x64                    
  0e55e:  str r0, [sp, #8]                  
  0e560:  b #0xe60e                         -> 0x0e60e (вне списка функций)
  0e562:  ldr r0, [sp, #4]                  
  0e564:  sxth r0, r0                       
  0e566:  str r0, [sp, #8]                  
  0e568:  b #0xe60e                         -> 0x0e60e (вне списка функций)
  0e56a:  sxth r5, r7                       
  0e56c:  cmp.w r8, #0                      
  0e570:  bge #0xe57c                       
  0e572:  rsb.w r0, r8, #0                  
  0e576:  sxth r0, r0                       
  0e578:  str r0, [sp, #8]                  
  0e57a:  b #0xe580                         -> 0x0e580 (вне списка функций)
  0e57c:  str.w r8, [sp, #8]                
  0e580:  ldrsh.w r0, [sp, #8]              
  0e584:  cmp r0, #0                        
  0e586:  ble #0xe58c                       
  0e588:  movs r1, #1                       
  0e58a:  b #0xe58e                         -> 0x0e58e (вне списка функций)
  0e58c:  movs r1, #0                       
  0e58e:  ldr r0, [sp, #0x38]               
  0e590:  ldrb r0, [r0]                     
  0e592:  add r0, r1                        
  0e594:  uxtb r0, r0                       
  0e596:  str r0, [sp]                      
  0e598:  movs r1, #3                       
  0e59a:  ldr r0, [sp]                      
  0e59c:  sdiv r2, r0, r1                   
  0e5a0:  mls r0, r1, r2, r0                
  0e5a4:  uxtb r0, r0                       
  0e5a6:  cbnz r0, #0xe5ac                  
  0e5a8:  movs r0, #1                       
  0e5aa:  b #0xe5ae                         -> 0x0e5ae (вне списка функций)
  0e5ac:  movs r0, #0                       
  0e5ae:  mla r4, r0, r8, r5                
  0e5b2:  cmp.w r4, #0x8000                 
  0e5b6:  blt #0xe5be                       
  0e5b8:  movw r4, #0x7fff                  
  0e5bc:  b #0xe5c6                         -> 0x0e5c6 (вне списка функций)
  0e5be:  cmn.w r4, #0x8000                 
  0e5c2:  bge #0xe5c6                       
  0e5c4:  ldr r4, [pc, #0x78]               
  0e5c6:  sxth r0, r4                       
  0e5c8:  str r0, [sp, #8]                  
  0e5ca:  cmp r5, #0x64                     
  0e5cc:  blt #0xe5da                       
  0e5ce:  sxth r0, r4                       
  0e5d0:  cmp r0, #0x64                     
  0e5d2:  bge #0xe5da                       
  0e5d4:  movs r0, #0x64                    
  0e5d6:  str r0, [sp, #8]                  
  0e5d8:  b #0xe608                         -> 0x0e608 (вне списка функций)
  0e5da:  movw r0, #0x26d4                  
  0e5de:  cmp r5, r0                        
  0e5e0:  bgt #0xe5f2                       
  0e5e2:  sxth r0, r4                       
  0e5e4:  movw r1, #0x26d4                  
  0e5e8:  cmp r0, r1                        
  0e5ea:  ble #0xe5f2                       
  0e5ec:  mov r0, r1                        
  0e5ee:  str r0, [sp, #8]                  
  0e5f0:  b #0xe608                         -> 0x0e608 (вне списка функций)
  0e5f2:  movw r0, #0x26d4                  
  0e5f6:  cmp r5, r0                        
  0e5f8:  ble #0xe5fe                       
  0e5fa:  str r5, [sp, #8]                  
  0e5fc:  b #0xe608                         -> 0x0e608 (вне списка функций)
  0e5fe:  sxth r0, r4                       
  0e600:  cmp r0, #0                        
  0e602:  bgt #0xe608                       
  0e604:  movs r0, #0                       
  0e606:  str r0, [sp, #8]                  
  0e608:  ldr r1, [sp, #0x38]               
  0e60a:  ldr r0, [sp]                      
  0e60c:  strb r0, [r1]                     
  0e60e:  ldrsh.w r0, [sp, #8]              
  0e612:  movw r1, #0x2710                  
  0e616:  cmp r0, r1                        
  0e618:  ble #0xe622                       
  0e61a:  mov r0, r1                        
  0e61c:  strh.w r0, [sl]                   
  0e620:  b #0xe63a                         -> 0x0e63a (вне списка функций)
  0e622:  ldrsh.w r0, [sp, #8]              
  0e626:  cmp r0, #0                        
  0e628:  bge #0xe632                       
  0e62a:  movs r0, #0                       
  0e62c:  strh.w r0, [sl]                   
  0e630:  b #0xe63a                         -> 0x0e63a (вне списка функций)
  0e632:  ldrh.w r0, [sp, #8]               
  0e636:  strh.w r0, [sl]                   
  0e63a:  pop.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x0e640 (1 слов) — ВНЕ границ функции ---
  0e640:  .word 0xffff8000
```
