# func_0x1a31c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a31c) | `0x0001a31c` |
| размер кода | 522 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0000094e — данные @0x0094e (r1)
- 0x20000030 — RAM (r4)
- 0x200000ac — RAM (r0)
- 0x20000110 — RAM (r0)
- 0x20000154 — RAM (r0)
- 0x200001e0 — RAM (r2)
- 0x200001ec — RAM (r1)
- 0x20000222 — RAM (r1)
- 0x2000023e — RAM (r2)
- 0x20000246 — RAM (r0)
- 0x20000248 — RAM (r1)
- 0x2000024a — RAM (r1)
- 0x2000024c — RAM (r1)
- 0x20000250 — RAM (r0)
- 0x20000254 — RAM (r0)
- 0x20000258 — RAM (r0)
- 0x2000025c — RAM (r0)
- 0x20000268 — RAM (r1)
- 0x2000026b — RAM (r6)
- 0x2000026c — RAM (r1)
- 0x2000026e — RAM (r1)
- 0x20000270 — RAM (r0)
- 0x20000272 — RAM (r2)
- 0x20000274 — RAM (r0)
- 0x20000278 — RAM (r1)
- 0x2000027e — RAM (r2)
- 0x20000284 — RAM (r1)
- 0x2000029c — RAM (r1)
- 0x200002bc — RAM (r2)
- 0x200002c4 — RAM (r2)
- 0x20000360 — RAM (r2)
- 0x20000370 — RAM (r2)
- 0x20000378 — RAM (r2)
- 0x200003c0 — RAM (r0)
- 0x2000168a — RAM (r5)
- 0x20001794 — RAM (r1)
- 0x40012400 — периферия (r0)
- 0x40012c40 — периферия (r0)
- 0x40023c00 — периферия (r0)

## Вызовы (callees)

- 0x1a344 (b, вне списка функций)
- 0x1a3ec (b, вне списка функций)
- 0x1a3f0 (b, вне списка функций)
- 0x1a4a2 (b, вне списка функций)
- `func_0x1a5c4` (0x0001a5c4, bl)
- `func_0x1a688` (0x0001a688, bl)
- `func_0x1a894` (0x0001a894, bl)
- `func_0x1a938` (0x0001a938, bl)
- `func_0x1bb1c` (0x0001bb1c, bl)
- 0x1bf24 (bl, вне списка функций)
- 0x1c040 (bl, вне списка функций)
- `func_0x1d3d0` (0x0001d3d0, bl)
- `func_0x1e298` (0x0001e298, bl)
- `func_0x1f600` (0x0001f600, bl)
- `func_0x216e4` (0x000216e4, bl)
- `func_0x23374` (0x00023374, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1a338..0x1a33e` (6 Б); цели из: 0x1a32a
- `0x1a33e..0x1a344` (6 Б); цели из: 0x1a334
- `0x1a344..0x1a364` (32 Б); цели из: 0x1a336
- `0x1a364..0x1a370` (12 Б); цели из: 0x1a350
- `0x1a370..0x1a39c` (44 Б); цели из: 0x1a358
- `0x1a39c..0x1a3ec` (80 Б); цели из: 0x1a35c
- `0x1a3ec..0x1a3ee` (2 Б); цели из: 0x1a39a
- `0x1a3ee..0x1a3f0` (2 Б); цели из: 0x1a38c
- `0x1a3f0..0x1a408` (24 Б); цели из: 0x1a362
- `0x1a408..0x1a416` (14 Б); цели из: 0x1a402
- `0x1a416..0x1a4a2` (140 Б); цели из: 0x1a410
- `0x1a4a2..0x1a4e0` (62 Б); цели из: 0x1a33c, 0x1a36e, 0x1a3c8, 0x1a3ee
- `0x1a4e0..0x1a4ec` (12 Б); цели из: 0x1a4da
- `0x1a4ec..0x1a4fc` (16 Б); цели из: 0x1a4e6
- `0x1a4fc..0x1a508` (12 Б); цели из: 0x1a4f6
- `0x1a508..0x1a514` (12 Б); цели из: 0x1a502
- `0x1a514..0x1a526` (18 Б); цели из: 0x1a50e

## Дизассембляция

```asm
  1a31c:  push {r3, r4, r5, r6, r7, lr}     
  1a31e:  ldr r0, [pc, #0x208]              -> периферия
  1a320:  ldr r1, [r0, #0xc]                
  1a322:  str r1, [r0, #0x14]               
  1a324:  ldr r0, [pc, #0x204]              -> RAM
  1a326:  ldrb r0, [r0]                     
  1a328:  cmp r0, #1                        
  1a32a:  beq #0x1a338                      
  1a32c:  ldr r0, [pc, #0x200]              -> RAM
  1a32e:  movs r6, #0                       
  1a330:  ldrb r1, [r0]                     
  1a332:  cmp r1, #1                        
  1a334:  beq #0x1a33e                      
  1a336:  b #0x1a344                        -> 0x1a344 (вне списка функций)
  1a338:  bl #0x1a894                       -> func_0x1a894
  1a33c:  b #0x1a4a2                        -> 0x1a4a2 (вне списка функций)
  1a33e:  strb r6, [r0]                     
  1a340:  bl #0x1e298                       -> func_0x1e298
  1a344:  ldr r1, [pc, #0x1ec]              -> RAM
  1a346:  ldr r5, [pc, #0x1f0]              -> RAM
  1a348:  ldrb r2, [r1]                     
  1a34a:  ldr r0, [pc, #0x1f0]              -> RAM
  1a34c:  ldr r4, [pc, #0x1f0]              -> RAM
  1a34e:  cmp r2, #0                        
  1a350:  beq #0x1a364                      
  1a352:  ldr r7, [pc, #0x1d4]              -> периферия
  1a354:  adds r7, #0x40                    
  1a356:  cmp r2, #1                        
  1a358:  beq #0x1a370                      
  1a35a:  cmp r2, #3                        
  1a35c:  beq #0x1a39c                      
  1a35e:  cmp r2, #5                        
  1a360:  bne #0x1a33c                      
  1a362:  b #0x1a3f0                        -> 0x1a3f0 (вне списка функций)
  1a364:  ldr r1, [pc, #0x1dc]              -> RAM
  1a366:  ldrh r2, [r5, #2]                 
  1a368:  strh r2, [r1]                     
  1a36a:  strh r6, [r4, #6]                 
  1a36c:  str r6, [r0]                      
  1a36e:  b #0x1a4a2                        -> 0x1a4a2 (вне списка функций)
  1a370:  ldr r2, [r7, #0x34]               
  1a372:  ldr r3, [r0]                      
  1a374:  adds r2, r2, r3                   
  1a376:  str r2, [r0]                      
  1a378:  ldr r0, [pc, #0x1c8]              -> RAM
  1a37a:  ldrh r3, [r5, #2]                 
  1a37c:  strh r3, [r0]                     
  1a37e:  ldrh r0, [r4, #6]                 
  1a380:  movs r3, #1                       
  1a382:  adds r0, r0, #1                   
  1a384:  uxth r0, r0                       
  1a386:  lsls r3, r3, #0xa                 
  1a388:  strh r0, [r4, #6]                 
  1a38a:  cmp r0, r3                        
  1a38c:  bne #0x1a3ee                      
  1a38e:  lsls r0, r2, #6                   
  1a390:  lsrs r2, r0, #0x10                
  1a392:  ldr r0, [pc, #0x1b4]              -> RAM
  1a394:  strh r6, [r4, #6]                 
  1a396:  strh r2, [r0, #0x3c]              
  1a398:  movs r0, #2                       
  1a39a:  b #0x1a3ec                        -> 0x1a3ec (вне списка функций)
  1a39c:  ldr r2, [r7, #0x28]               
  1a39e:  ldr r0, [pc, #0x1ac]              -> RAM
  1a3a0:  ldr r3, [r0]                      
  1a3a2:  adds r3, r2, r3                   
  1a3a4:  str r3, [r0]                      
  1a3a6:  ldr r2, [r7, #0x2c]               
  1a3a8:  ldr r0, [pc, #0x1a4]              -> RAM
  1a3aa:  ldr r5, [r0]                      
  1a3ac:  adds r2, r2, r5                   
  1a3ae:  str r2, [r0]                      
  1a3b0:  ldr r5, [r7, #0x30]               
  1a3b2:  ldr r0, [pc, #0x1a0]              -> RAM
  1a3b4:  ldr r7, [r0]                      
  1a3b6:  adds r5, r5, r7                   
  1a3b8:  str r5, [r0]                      
  1a3ba:  ldrh r0, [r4, #6]                 
  1a3bc:  movs r7, #1                       
  1a3be:  adds r0, r0, #1                   
  1a3c0:  uxth r0, r0                       
  1a3c2:  lsls r7, r7, #0xa                 
  1a3c4:  strh r0, [r4, #6]                 
  1a3c6:  cmp r0, r7                        
  1a3c8:  bne #0x1a4a2                      
  1a3ca:  ldr r0, [pc, #0x18c]              -> периферия
  1a3cc:  strh r6, [r4, #6]                 
  1a3ce:  ldr r4, [r0, #0x14]               
  1a3d0:  lsls r6, r7, #5                   
  1a3d2:  bics r4, r6                       
  1a3d4:  str r4, [r0, #0x14]               
  1a3d6:  lsls r0, r3, #6                   
  1a3d8:  lsrs r3, r0, #0x10                
  1a3da:  ldr r0, [pc, #0x16c]              -> RAM
  1a3dc:  lsls r2, r2, #6                   
  1a3de:  strh r3, [r0, #0x18]              
  1a3e0:  lsrs r2, r2, #0x10                
  1a3e2:  strh r2, [r0, #0x1a]              
  1a3e4:  lsls r2, r5, #6                   
  1a3e6:  lsrs r2, r2, #0x10                
  1a3e8:  strh r2, [r0, #0x1c]              
  1a3ea:  movs r0, #4                       
  1a3ec:  strb r0, [r1]                     
  1a3ee:  b #0x1a4a2                        -> 0x1a4a2 (вне списка функций)
  1a3f0:  bl #0x1bf24                       -> 0x1bf24 (вне списка функций)
  1a3f4:  ldr r6, [pc, #0x164]              -> RAM
  1a3f6:  ldr r1, [pc, #0x168]              -> RAM
  1a3f8:  strb r0, [r6]                     
  1a3fa:  movs r2, #0                       
  1a3fc:  ldrsh r2, [r1, r2]                
  1a3fe:  ldr r1, [pc, #0x164]              -> данные @0x0094e
  1a400:  cmp r2, r1                        
  1a402:  ble #0x1a408                      
  1a404:  bl #0x1a688                       -> func_0x1a688
  1a408:  ldr r0, [pc, #0x15c]              -> RAM
  1a40a:  ldrb r0, [r0]                     
  1a40c:  cmp r0, #0                        
  1a40e:  ldrb r0, [r6]                     
  1a410:  beq #0x1a416                      
  1a412:  bl #0x23374                       -> func_0x23374
  1a416:  ldr r1, [pc, #0x154]              -> RAM
  1a418:  strb r0, [r1]                     
  1a41a:  ldr r0, [pc, #0x154]              -> RAM
  1a41c:  bl #0x1bb1c                       -> func_0x1bb1c
  1a420:  ldr r1, [r7, #0x34]               
  1a422:  ldr r0, [pc, #0x124]              -> RAM
  1a424:  movs r2, #0                       
  1a426:  ldrh r0, [r0, #0x3c]              
  1a428:  movs r3, #0                       
  1a42a:  subs r0, r1, r0                   
  1a42c:  ldr r1, [pc, #0x144]              -> RAM
  1a42e:  sxth r0, r0                       
  1a430:  strh r0, [r1]                     
  1a432:  ldr r1, [r4, #0xc]                
  1a434:  adds r0, r1, r0                   
  1a436:  ldr r1, [pc, #0x140]              -> RAM
  1a438:  ldrsh r2, [r1, r2]                
  1a43a:  subs r0, r0, r2                   
  1a43c:  str r0, [r4, #0xc]                
  1a43e:  asrs r0, r0, #3                   
  1a440:  strh r0, [r1]                     
  1a442:  movs r1, #4                       
  1a444:  ldr r0, [pc, #0x134]              -> RAM
  1a446:  ldrsh r1, [r5, r1]                
  1a448:  strh r1, [r0]                     
  1a44a:  ldr r0, [pc, #0x134]              -> RAM
  1a44c:  ldr r2, [r0]                      
  1a44e:  adds r1, r2, r1                   
  1a450:  ldr r2, [pc, #0x130]              -> RAM
  1a452:  ldrsh r3, [r2, r3]                
  1a454:  subs r1, r1, r3                   
  1a456:  str r1, [r0]                      
  1a458:  asrs r0, r1, #8                   
  1a45a:  sxth r1, r0                       
  1a45c:  ldr r0, [pc, #0x128]              -> периферия
  1a45e:  strh r1, [r2]                     
  1a460:  ldr r2, [r0, #0x10]               
  1a462:  movs r3, #1                       
  1a464:  orrs r2, r3                       
  1a466:  str r2, [r0, #0x10]               
  1a468:  movs r2, #0xff                    
  1a46a:  adds r2, #0x9b                    
  1a46c:  muls r1, r2, r1                   
  1a46e:  str r1, [r0]                      
  1a470:  ldr r1, [pc, #0x118]              -> RAM
  1a472:  ldrh r1, [r1]                     
  1a474:  str r1, [r0, #4]                  
  1a476:  ldr r0, [r0, #8]                  
  1a478:  ldr r1, [pc, #0x114]              -> RAM
  1a47a:  strh r0, [r1, #0xc]               
  1a47c:  ldr r0, [pc, #0xc4]               -> RAM
  1a47e:  ldrh r1, [r5, #2]                 
  1a480:  strh r1, [r0]                     
  1a482:  ldr r1, [pc, #0x110]              -> RAM
  1a484:  ldrh r0, [r5, #6]                 
  1a486:  strh r0, [r1]                     
  1a488:  ldr r0, [pc, #0xd4]               -> RAM
  1a48a:  ldrh r0, [r0]                     
  1a48c:  uxth r0, r0                       
  1a48e:  bl #0x1c040                       -> 0x1c040 (вне списка функций)
  1a492:  ldr r1, [pc, #0x104]              -> RAM
  1a494:  ldrh r0, [r5, #8]                 
  1a496:  strh r0, [r1]                     
  1a498:  ldr r1, [pc, #0x100]              -> RAM
  1a49a:  ldrh r0, [r5]                     
  1a49c:  strh r0, [r1]                     
  1a49e:  bl #0x1a938                       -> func_0x1a938
  1a4a2:  ldr r1, [pc, #0xfc]               -> RAM
  1a4a4:  ldr r2, [pc, #0xfc]               -> RAM
  1a4a6:  ldrh r0, [r1]                     
  1a4a8:  movs r3, #0                       
  1a4aa:  adds r0, r0, #1                   
  1a4ac:  strh r0, [r1]                     
  1a4ae:  ldm r2!, {r0, r1}                 
  1a4b0:  subs r2, #8                       
  1a4b2:  adds r0, r0, #1                   
  1a4b4:  adcs r1, r3                       
  1a4b6:  stm r2!, {r0, r1}                 
  1a4b8:  ldr r2, [pc, #0xec]               -> RAM
  1a4ba:  ldm r2!, {r0, r1}                 
  1a4bc:  subs r2, #8                       
  1a4be:  adds r0, r0, #1                   
  1a4c0:  adcs r1, r3                       
  1a4c2:  stm r2!, {r0, r1}                 
  1a4c4:  ldr r2, [pc, #0xe4]               -> RAM
  1a4c6:  ldm r2!, {r0, r1}                 
  1a4c8:  subs r2, #8                       
  1a4ca:  adds r0, r0, #1                   
  1a4cc:  adcs r1, r3                       
  1a4ce:  stm r2!, {r0, r1}                 
  1a4d0:  ldr r2, [pc, #0xdc]               -> RAM
  1a4d2:  movs r0, #0x7d                    
  1a4d4:  ldrh r1, [r2]                     
  1a4d6:  lsls r0, r0, #7                   
  1a4d8:  cmp r1, r0                        
  1a4da:  bhs #0x1a4e0                      
  1a4dc:  adds r1, r1, #1                   
  1a4de:  strh r1, [r2]                     
  1a4e0:  ldr r2, [pc, #0xd0]               -> RAM
  1a4e2:  ldrh r1, [r2]                     
  1a4e4:  cmp r1, r0                        
  1a4e6:  bhs #0x1a4ec                      
  1a4e8:  adds r1, r1, #1                   
  1a4ea:  strh r1, [r2]                     
  1a4ec:  ldr r2, [pc, #0xc8]               -> RAM
  1a4ee:  movs r3, #0x7d                    
  1a4f0:  ldrh r1, [r2]                     
  1a4f2:  lsls r3, r3, #9                   
  1a4f4:  cmp r1, r3                        
  1a4f6:  bhs #0x1a4fc                      
  1a4f8:  adds r1, r1, #1                   
  1a4fa:  strh r1, [r2]                     
  1a4fc:  ldr r2, [pc, #0xbc]               -> RAM
  1a4fe:  ldrh r1, [r2]                     
  1a500:  cmp r1, r3                        
  1a502:  bhs #0x1a508                      
  1a504:  adds r1, r1, #1                   
  1a506:  strh r1, [r2]                     
  1a508:  ldr r2, [pc, #0xb4]               -> RAM
  1a50a:  ldrh r1, [r2]                     
  1a50c:  cmp r1, r0                        
  1a50e:  bhs #0x1a514                      
  1a510:  adds r1, r1, #1                   
  1a512:  strh r1, [r2]                     
  1a514:  bl #0x1d3d0                       -> func_0x1d3d0
  1a518:  bl #0x1f600                       -> func_0x1f600
  1a51c:  bl #0x216e4                       -> func_0x216e4
  1a520:  bl #0x1a5c4                       -> func_0x1a5c4
  1a524:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1a528 (39 слов) — ВНЕ границ функции ---
  1a528:  .word 0x40012400  ; периферия
  1a52c:  .word 0x20000246  ; RAM
  1a530:  .word 0x200003c0  ; RAM
  1a534:  .word 0x20000248  ; RAM
  1a538:  .word 0x2000168a  ; RAM
  1a53c:  .word 0x20000250  ; RAM
  1a540:  .word 0x20000030  ; RAM
  1a544:  .word 0x2000024a  ; RAM
  1a548:  .word 0x20000110  ; RAM
  1a54c:  .word 0x20000254  ; RAM
  1a550:  .word 0x20000258  ; RAM
  1a554:  .word 0x2000025c  ; RAM
  1a558:  .word 0x40012c40  ; периферия
  1a55c:  .word 0x2000026b  ; RAM
  1a560:  .word 0x2000024c  ; RAM
  1a564:  .word 0x0000094e  ; данные @0x0094e
  1a568:  .word 0x200000ac  ; RAM
  1a56c:  .word 0x20000268  ; RAM
  1a570:  .word 0x20000154  ; RAM
  1a574:  .word 0x2000026c  ; RAM
  1a578:  .word 0x2000026e  ; RAM
  1a57c:  .word 0x20000270  ; RAM
  1a580:  .word 0x20000274  ; RAM
  1a584:  .word 0x20000272  ; RAM
  1a588:  .word 0x40023c00  ; периферия
  1a58c:  .word 0x200001ec  ; RAM
  1a590:  .word 0x20001794  ; RAM
  1a594:  .word 0x20000278  ; RAM
  1a598:  .word 0x20000284  ; RAM
  1a59c:  .word 0x2000029c  ; RAM
  1a5a0:  .word 0x20000222  ; RAM
  1a5a4:  .word 0x200001e0  ; RAM
  1a5a8:  .word 0x20000378  ; RAM
  1a5ac:  .word 0x20000360  ; RAM
  1a5b0:  .word 0x200002bc  ; RAM
  1a5b4:  .word 0x200002c4  ; RAM
  1a5b8:  .word 0x2000027e  ; RAM
  1a5bc:  .word 0x2000023e  ; RAM
  1a5c0:  .word 0x20000370  ; RAM
```
