# func_0x1c34c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001c34c) | `0x0001c34c` |
| размер кода | 1244 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- `r2`: 0x00013880 — "Hq2H@}"

## Литералы и адреса

- 0x00000352 — данные @0x00352 (r0)
- 0x00000bb7 — данные @0x00bb7 (r1)
- 0x0000176f — данные @0x0176f (r1)
- 0x00007c10 — данные @0x07c10 (r1)
- 0x00007ff8 — данные @0x07ff8 (r2)
- 0x0000bb80 — данные @0x0bb80 (r2)
- 0x200000ac — RAM (r1)
- 0x200001e0 — RAM (r1)
- 0x2000021e — RAM (r1)
- 0x20000220 — RAM (r0)
- 0x20000224 — RAM (r1)
- 0x20000229 — RAM (r0)
- 0x2000022f — RAM (r0)
- 0x20000230 — RAM (r0)
- 0x20000231 — RAM (r1)
- 0x20000233 — RAM (r0)
- 0x2000023e — RAM (r2)
- 0x20000240 — RAM (r0)
- 0x20000245 — RAM (r1)
- 0x20000262 — RAM (r0)
- 0x2000027c — RAM (r1)
- 0x2000027e — RAM (r2)
- 0x20000280 — RAM (r0)
- 0x20000281 — RAM (r0)
- 0x20000282 — RAM (r0)
- 0x20000290 — RAM (r1)
- 0x2000030e — RAM (r1)
- 0x20000311 — RAM (r1)
- 0x2000031c — RAM (r2)
- 0x2000031f — RAM (r3)
- 0x2000032a — RAM (r0)
- 0x2000033a — RAM (r0)
- 0x20000380 — RAM (r1)
- 0x200003c8 — RAM (r1)
- 0x20001768 — RAM (r2)
- 0x40012c40 — периферия (r0)

## Вызовы (callees)

- 0x19968 (bl, вне списка функций)
- 0x19994 (bl, вне списка функций)
- 0x1c362 (b, вне списка функций)
- 0x1c3a2 (b, вне списка функций)
- 0x1c44a (b, вне списка функций)
- 0x1c4ba (b, вне списка функций)
- 0x1c4ea (b, вне списка функций)
- 0x1c4ec (b, вне списка функций)
- 0x1c508 (b, вне списка функций)
- 0x1c528 (b, вне списка функций)
- 0x1c52c (b, вне списка функций)
- 0x1c53c (b, вне списка функций)
- 0x1c61a (b, вне списка функций)
- 0x1c662 (b, вне списка функций)
- 0x1c676 (b, вне списка функций)
- 0x1c6b8 (b, вне списка функций)
- 0x1c6c2 (b, вне списка функций)
- 0x1c70a (b, вне списка функций)
- 0x1c71a (b, вне списка функций)
- 0x1c71e (b, вне списка функций)
- 0x1c724 (b, вне списка функций)
- 0x1c72e (b, вне списка функций)
- 0x1c80c (b, вне списка функций)
- 0x1c820 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1c35e..0x1c362` (4 Б); цели из: 0x1c358
- `0x1c362..0x1c39a` (56 Б); цели из: 0x1c35c
- `0x1c39a..0x1c3a2` (8 Б); цели из: 0x1c394
- `0x1c3a2..0x1c3ec` (74 Б); цели из: 0x1c398, 0x1c39e
- `0x1c3ec..0x1c3fa` (14 Б); цели из: 0x1c3be
- `0x1c3fa..0x1c414` (26 Б); цели из: 0x1c3e4
- `0x1c414..0x1c416` (2 Б); цели из: 0x1c3e8
- `0x1c416..0x1c44a` (52 Б); цели из: 0x1c3fe
- `0x1c44a..0x1c466` (28 Б); цели из: 0x1c3ea
- `0x1c466..0x1c46c` (6 Б); цели из: 0x1c458
- `0x1c46c..0x1c490` (36 Б); цели из: 0x1c464
- `0x1c490..0x1c4a6` (22 Б); цели из: 0x1c474, 0x1c47a, 0x1c482, 0x1c486
- `0x1c4a6..0x1c4b2` (12 Б); цели из: 0x1c49a
- `0x1c4b2..0x1c4be` (12 Б); цели из: 0x1c4aa
- `0x1c4be..0x1c4de` (32 Б); цели из: 0x1c48a
- `0x1c4de..0x1c4ea` (12 Б); цели из: 0x1c4c4
- `0x1c4ea..0x1c4ec` (2 Б); цели из: 0x1c4dc
- `0x1c4ec..0x1c502` (22 Б); цели из: 0x1c414, 0x1c42e, 0x1c448, 0x1c4bc
- `0x1c502..0x1c508` (6 Б); цели из: 0x1c4e4
- `0x1c508..0x1c510` (8 Б); цели из: 0x1c3f8, 0x1c4f2
- `0x1c510..0x1c52c` (28 Б); цели из: 0x1c4fa
- `0x1c52c..0x1c536` (10 Б); цели из: 0x1c500
- `0x1c536..0x1c53a` (4 Б); цели из: 0x1c530
- `0x1c53a..0x1c53c` (2 Б); цели из: 0x1c524
- `0x1c53c..0x1c556` (26 Б); цели из: 0x1c4fe, 0x1c51c, 0x1c526, 0x1c52a
- `0x1c556..0x1c58e` (56 Б); цели из: 0x1c546
- `0x1c58e..0x1c5ea` (92 Б); цели из: 0x1c566
- `0x1c5ea..0x1c60c` (34 Б); цели из: 0x1c594
- `0x1c60c..0x1c60e` (2 Б); цели из: 0x1c5ae
- `0x1c60e..0x1c61a` (12 Б); цели из: 0x1c5c0, 0x1c5c8
- `0x1c61a..0x1c656` (60 Б); цели из: 0x1c5e0, 0x1c5e8
- `0x1c656..0x1c662` (12 Б); цели из: 0x1c62c, 0x1c634
- `0x1c662..0x1c674` (18 Б); цели из: 0x1c64c, 0x1c654
- `0x1c674..0x1c676` (2 Б); цели из: 0x1c58a
- `0x1c676..0x1c6b8` (66 Б); цели из: 0x1c58c
- `0x1c6b8..0x1c6c2` (10 Б); цели из: 0x1c674, 0x1c67a, 0x1c682, 0x1c688…
- `0x1c6c2..0x1c6d4` (18 Б); цели из: 0x1c60c, 0x1c672, 0x1c6b6
- `0x1c6d4..0x1c6f8` (36 Б); цели из: 0x1c6c8
- `0x1c6f8..0x1c70a` (18 Б); цели из: 0x1c6cc
- `0x1c70a..0x1c70e` (4 Б); цели из: 0x1c554
- `0x1c70e..0x1c71a` (12 Б); цели из: 0x1c704
- `0x1c71a..0x1c71e` (4 Б); цели из: 0x1c6f6
- `0x1c71e..0x1c724` (6 Б); цели из: 0x1c6d2
- `0x1c724..0x1c7cc` (168 Б); цели из: 0x1c6d0, 0x1c6da, 0x1c6e2, 0x1c6e8…
- `0x1c7cc..0x1c7da` (14 Б); цели из: 0x1c72a
- `0x1c7da..0x1c7e0` (6 Б); цели из: 0x1c7d0
- `0x1c7e0..0x1c808` (40 Б); цели из: 0x1c734
- `0x1c808..0x1c80c` (4 Б); цели из: 0x1c7e8, 0x1c7ee
- `0x1c80c..0x1c820` (20 Б); цели из: 0x1c73a
- `0x1c820..0x1c828` (8 Б); цели из: 0x1c738, 0x1c7f8, 0x1c806, 0x1c80a…

## Дизассембляция

```asm
  1c34c:  push {r4, r5, r6, r7, lr}         
  1c34e:  ldr r0, [pc, #0x3ec]              -> RAM
  1c350:  ldr r1, [pc, #0x3ec]              -> RAM
  1c352:  ldrb r0, [r0]                     
  1c354:  sub sp, #0x14                     
  1c356:  cmp r0, #0                        
  1c358:  beq #0x1c35e                      
  1c35a:  ldr r0, [pc, #0x3e8]              -> данные @0x00352
  1c35c:  b #0x1c362                        -> 0x1c362 (вне списка функций)
  1c35e:  movs r0, #0x55                    
  1c360:  lsls r0, r0, #3                   
  1c362:  ldr r2, [pc, #0x3e4]              -> RAM
  1c364:  str r0, [r1, #0x4c]               
  1c366:  movs r0, #8                       
  1c368:  ldrsh r0, [r2, r0]                
  1c36a:  str r0, [sp]                      
  1c36c:  ldr r4, [pc, #0x3d0]              -> RAM
  1c36e:  movs r2, #0xf0                    
  1c370:  muls r0, r2, r0                   
  1c372:  ldr r1, [r4, #0x4c]               
  1c374:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1c378:  ldr r2, [pc, #0x3cc]              -> RAM
  1c37a:  movs r1, #0xc                     
  1c37c:  adds r2, #0x2c                    
  1c37e:  str r0, [r4, #0x50]               
  1c380:  ldrsh r1, [r2, r1]                
  1c382:  lsls r2, r0, #0xc                 
  1c384:  subs r0, r2, r0                   
  1c386:  lsls r0, r0, #4                   
  1c388:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1c38c:  ldr r1, [pc, #0x3bc]              -> RAM
  1c38e:  movs r4, #0                       
  1c390:  str r0, [r1]                      
  1c392:  cmp r0, #0                        
  1c394:  bge #0x1c39a                      
  1c396:  str r4, [r1]                      
  1c398:  b #0x1c3a2                        -> 0x1c3a2 (вне списка функций)
  1c39a:  ldr r2, [pc, #0x3b4]              -> данные @0x07ff8
  1c39c:  cmp r0, r2                        
  1c39e:  ble #0x1c3a2                      
  1c3a0:  str r2, [r1]                      
  1c3a2:  ldr r0, [pc, #0x3b0]              -> RAM
  1c3a4:  ldr r1, [pc, #0x3b0]              -> RAM
  1c3a6:  ldrb r0, [r0]                     
  1c3a8:  ldrh r1, [r1]                     
  1c3aa:  str r1, [sp, #0xc]                
  1c3ac:  ldr r1, [pc, #0x3ac]              -> RAM
  1c3ae:  ldr r7, [pc, #0x398]              -> RAM
  1c3b0:  ldrb r1, [r1]                     
  1c3b2:  str r1, [sp, #8]                  
  1c3b4:  ldr r1, [pc, #0x3a8]              -> RAM
  1c3b6:  subs r7, #0xc                     
  1c3b8:  ldr r6, [r1]                      
  1c3ba:  ldr r5, [r1, #4]                  
  1c3bc:  cmp r0, #1                        
  1c3be:  beq #0x1c3ec                      
  1c3c0:  ldr r0, [pc, #0x3a0]              -> RAM
  1c3c2:  movs r1, #0x64                    
  1c3c4:  ldrb r0, [r0]                     
  1c3c6:  lsls r0, r0, #0xf                 
  1c3c8:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1c3cc:  movs r1, #0x2d                    
  1c3ce:  lsls r1, r1, #4                   
  1c3d0:  muls r0, r1, r0                   
  1c3d2:  ldr r1, [pc, #0x394]              -> RAM
  1c3d4:  lsrs r0, r0, #0x10                
  1c3d6:  strh r0, [r1]                     
  1c3d8:  ldr r1, [pc, #0x364]              -> RAM
  1c3da:  ldrb r2, [r1, #5]                 
  1c3dc:  ldr r1, [pc, #0x38c]              -> RAM
  1c3de:  cmp r2, #0                        
  1c3e0:  ldrh r1, [r1]                     
  1c3e2:  mov ip, r1                        
  1c3e4:  beq #0x1c3fa                      
  1c3e6:  cmp r2, #1                        
  1c3e8:  bne #0x1c414                      
  1c3ea:  b #0x1c44a                        -> 0x1c44a (вне списка функций)
  1c3ec:  ldr r0, [pc, #0x37c]              -> RAM
  1c3ee:  strh r4, [r0]                     
  1c3f0:  ldr r0, [pc, #0x37c]              -> RAM
  1c3f2:  strh r4, [r0]                     
  1c3f4:  ldr r0, [pc, #0x358]              -> данные @0x07ff8
  1c3f6:  str r0, [r7]                      
  1c3f8:  b #0x1c508                        -> 0x1c508 (вне списка функций)
  1c3fa:  str r4, [r7]                      
  1c3fc:  cmp r0, #0x1e                     
  1c3fe:  bls #0x1c416                      
  1c400:  ldr r0, [pc, #0x33c]              -> RAM
  1c402:  movs r2, #2                       
  1c404:  adds r0, #0x80                    
  1c406:  str r6, [r0, #0x18]               
  1c408:  str r5, [r0, #0x1c]               
  1c40a:  ldr r0, [pc, #0x360]              -> RAM
  1c40c:  orrs r1, r2                       
  1c40e:  strh r1, [r0]                     
  1c410:  ldr r0, [pc, #0x32c]              -> RAM
  1c412:  strb r4, [r0, #5]                 
  1c414:  b #0x1c4ec                        -> 0x1c4ec (вне списка функций)
  1c416:  ldr r2, [pc, #0x328]              -> RAM
  1c418:  mov r0, r5                        
  1c41a:  adds r2, #0x80                    
  1c41c:  ldr r1, [r2, #0x18]               
  1c41e:  ldr r2, [r2, #0x1c]               
  1c420:  subs r1, r6, r1                   
  1c422:  sbcs r0, r2                       
  1c424:  movs r3, #0x19                    
  1c426:  lsls r3, r3, #6                   
  1c428:  movs r2, #0                       
  1c42a:  subs r1, r3, r1                   
  1c42c:  sbcs r2, r0                       
  1c42e:  bhs #0x1c4ec                      
  1c430:  ldr r0, [pc, #0x30c]              -> RAM
  1c432:  mov r1, ip                        
  1c434:  adds r0, #0x80                    
  1c436:  str r6, [r0, #0x18]               
  1c438:  str r5, [r0, #0x1c]               
  1c43a:  ldr r0, [pc, #0x330]              -> RAM
  1c43c:  movs r2, #2                       
  1c43e:  bics r1, r2                       
  1c440:  strh r1, [r0]                     
  1c442:  ldr r1, [pc, #0x2fc]              -> RAM
  1c444:  movs r0, #1                       
  1c446:  strb r0, [r1, #5]                 
  1c448:  b #0x1c4ec                        -> 0x1c4ec (вне списка функций)
  1c44a:  ldr r1, [pc, #0x328]              -> RAM
  1c44c:  movs r3, #1                       
  1c44e:  ldrb r2, [r1]                     
  1c450:  ldr r1, [pc, #0x318]              -> RAM
  1c452:  ldrh r1, [r1]                     
  1c454:  orrs r1, r3                       
  1c456:  cmp r2, #1                        
  1c458:  beq #0x1c466                      
  1c45a:  ldr r2, [pc, #0x31c]              -> RAM
  1c45c:  ldrh r3, [r2]                     
  1c45e:  movs r2, #0x7d                    
  1c460:  lsls r2, r2, #8                   
  1c462:  cmp r3, r2                        
  1c464:  bls #0x1c46c                      
  1c466:  ldr r0, [pc, #0x304]              -> RAM
  1c468:  strh r1, [r0]                     
  1c46a:  b #0x1c4ba                        -> 0x1c4ba (вне списка функций)
  1c46c:  ldr r1, [sp, #0xc]                
  1c46e:  lsls r2, r1, #0x1d                
  1c470:  ldr r1, [pc, #0x308]              -> RAM
  1c472:  ldrb r1, [r1]                     
  1c474:  bmi #0x1c490                      
  1c476:  ldr r2, [sp, #8]                  
  1c478:  cmp r2, #1                        
  1c47a:  beq #0x1c490                      
  1c47c:  ldr r2, [pc, #0x2ec]              -> RAM
  1c47e:  mov r3, ip                        
  1c480:  cmp r3, #0                        
  1c482:  bne #0x1c490                      
  1c484:  cmp r1, #1                        
  1c486:  beq #0x1c490                      
  1c488:  cmp r0, #0x1e                     
  1c48a:  bhs #0x1c4be                      
  1c48c:  strh r4, [r2]                     
  1c48e:  b #0x1c4ba                        -> 0x1c4ba (вне списка функций)
  1c490:  cmp r0, #0x1e                     
  1c492:  bhs #0x1c4ba                      
  1c494:  ldr r0, [pc, #0x2d4]              -> RAM
  1c496:  mov r2, ip                        
  1c498:  lsls r2, r2, #0x17                
  1c49a:  bpl #0x1c4a6                      
  1c49c:  movs r3, #0xff                    
  1c49e:  mov r2, ip                        
  1c4a0:  adds r3, #1                       
  1c4a2:  bics r2, r3                       
  1c4a4:  strh r2, [r0]                     
  1c4a6:  ldrh r2, [r0]                     
  1c4a8:  lsls r3, r2, #0x1f                
  1c4aa:  beq #0x1c4b2                      
  1c4ac:  lsrs r2, r2, #1                   
  1c4ae:  lsls r2, r2, #1                   
  1c4b0:  strh r2, [r0]                     
  1c4b2:  ldr r0, [pc, #0x2c8]              -> RAM
  1c4b4:  cmp r1, #1                        
  1c4b6:  bne #0x1c4ba                      
  1c4b8:  strb r4, [r0]                     
  1c4ba:  str r4, [r7]                      
  1c4bc:  b #0x1c4ec                        -> 0x1c4ec (вне списка функций)
  1c4be:  movs r1, #0xff                    
  1c4c0:  adds r1, #0x4b                    
  1c4c2:  cmp r0, r1                        
  1c4c4:  bhs #0x1c4de                      
  1c4c6:  ldr r1, [pc, #0x2b8]              -> данные @0x07c10
  1c4c8:  subs r0, #0x1e                    
  1c4ca:  muls r0, r1, r0                   
  1c4cc:  movs r1, #0xff                    
  1c4ce:  strh r4, [r2]                     
  1c4d0:  adds r1, #0x2d                    
  1c4d2:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1c4d6:  movs r1, #0x7d                    
  1c4d8:  lsls r1, r1, #3                   
  1c4da:  adds r0, r0, r1                   
  1c4dc:  b #0x1c4ea                        -> 0x1c4ea (вне списка функций)
  1c4de:  movs r1, #0xff                    
  1c4e0:  adds r1, #0x87                    
  1c4e2:  cmp r0, r1                        
  1c4e4:  bhs #0x1c502                      
  1c4e6:  ldr r0, [pc, #0x268]              -> данные @0x07ff8
  1c4e8:  strh r4, [r2]                     
  1c4ea:  str r0, [r7]                      
  1c4ec:  ldr r0, [pc, #0x294]              -> RAM
  1c4ee:  ldrb r0, [r0]                     
  1c4f0:  cmp r0, #0                        
  1c4f2:  beq #0x1c508                      
  1c4f4:  ldr r0, [pc, #0x248]              -> RAM
  1c4f6:  ldrb r1, [r0, #6]                 
  1c4f8:  cmp r1, #0                        
  1c4fa:  beq #0x1c510                      
  1c4fc:  cmp r1, #1                        
  1c4fe:  bne #0x1c53c                      
  1c500:  b #0x1c52c                        -> 0x1c52c (вне списка функций)
  1c502:  movs r0, #1                       
  1c504:  strh r0, [r2]                     
  1c506:  b #0x1c4ba                        -> 0x1c4ba (вне списка функций)
  1c508:  ldr r0, [pc, #0x234]              -> RAM
  1c50a:  movs r1, #1                       
  1c50c:  strb r1, [r0, #7]                 
  1c50e:  b #0x1c528                        -> 0x1c528 (вне списка функций)
  1c510:  strb r4, [r0, #7]                 
  1c512:  ldr r1, [r7]                      
  1c514:  cmp r1, #0                        
  1c516:  bne #0x1c528                      
  1c518:  ldr r1, [sp]                      
  1c51a:  cmp r1, #0x68                     
  1c51c:  blt #0x1c53c                      
  1c51e:  ldr r1, [pc, #0x268]              -> RAM
  1c520:  ldrb r1, [r1]                     
  1c522:  cmp r1, #1                        
  1c524:  beq #0x1c53a                      
  1c526:  b #0x1c53c                        -> 0x1c53c (вне списка функций)
  1c528:  strb r4, [r0, #6]                 
  1c52a:  b #0x1c53c                        -> 0x1c53c (вне списка функций)
  1c52c:  ldr r1, [sp]                      
  1c52e:  cmp r1, #0x3e                     
  1c530:  bge #0x1c536                      
  1c532:  strb r4, [r0, #7]                 
  1c534:  b #0x1c528                        -> 0x1c528 (вне списка функций)
  1c536:  movs r1, #1                       
  1c538:  strb r1, [r0, #7]                 
  1c53a:  strb r1, [r0, #6]                 
  1c53c:  ldr r0, [pc, #0x24c]              -> RAM
  1c53e:  ldrb r0, [r0]                     
  1c540:  str r0, [sp, #0x10]               
  1c542:  cmp r0, #1                        
  1c544:  ldr r0, [pc, #0x248]              -> RAM
  1c546:  beq #0x1c556                      
  1c548:  strb r4, [r0]                     
  1c54a:  ldr r0, [pc, #0x248]              -> RAM
  1c54c:  strb r4, [r0]                     
  1c54e:  ldr r0, [pc, #0x248]              -> RAM
  1c550:  strb r4, [r0]                     
  1c552:  ldr r0, [pc, #0x1ec]              -> RAM
  1c554:  b #0x1c70a                        -> 0x1c70a (вне списка функций)
  1c556:  ldrb r1, [r0]                     
  1c558:  ldr r0, [pc, #0x240]              -> RAM
  1c55a:  ldr r3, [pc, #0x248]              -> RAM
  1c55c:  ldrb r0, [r0]                     
  1c55e:  str r0, [sp, #4]                  
  1c560:  ldr r0, [pc, #0x23c]              -> RAM
  1c562:  cmp r1, #0                        
  1c564:  ldrb r0, [r0]                     
  1c566:  beq #0x1c58e                      
  1c568:  ldr r1, [pc, #0x228]              -> RAM
  1c56a:  ldr r2, [pc, #0x204]              -> RAM
  1c56c:  strb r4, [r1]                     
  1c56e:  ldr r1, [pc, #0x228]              -> RAM
  1c570:  strb r4, [r1]                     
  1c572:  ldr r1, [pc, #0x1cc]              -> RAM
  1c574:  adds r1, #0x80                    
  1c576:  str r6, [r1, #0x20]               
  1c578:  str r5, [r1, #0x24]               
  1c57a:  str r6, [r1, #0x28]               
  1c57c:  str r5, [r1, #0x2c]               
  1c57e:  str r6, [r1, #0x30]               
  1c580:  str r5, [r1, #0x34]               
  1c582:  ldr r1, [pc, #0x1e8]              -> RAM
  1c584:  ldrh r2, [r2]                     
  1c586:  ldrh r1, [r1]                     
  1c588:  orrs r1, r2                       
  1c58a:  bne #0x1c674                      
  1c58c:  b #0x1c676                        -> 0x1c676 (вне списка функций)
  1c58e:  ldr r1, [r7]                      
  1c590:  mov ip, r1                        
  1c592:  cmp r1, #0                        
  1c594:  beq #0x1c5ea                      
  1c596:  ldr r2, [pc, #0x1a8]              -> RAM
  1c598:  mov r0, r5                        
  1c59a:  adds r2, #0x80                    
  1c59c:  ldr r1, [r2, #0x20]               
  1c59e:  ldr r2, [r2, #0x24]               
  1c5a0:  subs r1, r6, r1                   
  1c5a2:  sbcs r0, r2                       
  1c5a4:  movs r3, #0x7d                    
  1c5a6:  lsls r3, r3, #5                   
  1c5a8:  movs r2, #0                       
  1c5aa:  subs r1, r3, r1                   
  1c5ac:  sbcs r2, r0                       
  1c5ae:  bhs #0x1c60c                      
  1c5b0:  ldr r1, [pc, #0x18c]              -> RAM
  1c5b2:  mov r0, ip                        
  1c5b4:  ldr r1, [r1, #0x48]               
  1c5b6:  subs r0, r0, r1                   
  1c5b8:  ldr r1, [pc, #0x1ec]              -> данные @0x00bb7
  1c5ba:  adds r0, r0, r1                   
  1c5bc:  ldr r1, [pc, #0x1ec]              -> данные @0x0176f
  1c5be:  cmp r0, r1                        
  1c5c0:  bhs #0x1c60e                      
  1c5c2:  ldr r0, [pc, #0x1ec]              -> периферия
  1c5c4:  ldr r0, [r0, #0x14]               
  1c5c6:  lsls r0, r0, #0x10                
  1c5c8:  bpl #0x1c60e                      
  1c5ca:  ldr r2, [pc, #0x174]              -> RAM
  1c5cc:  mov r0, r5                        
  1c5ce:  adds r2, #0x80                    
  1c5d0:  ldr r1, [r2, #0x28]               
  1c5d2:  ldr r2, [r2, #0x2c]               
  1c5d4:  subs r3, r6, r1                   
  1c5d6:  sbcs r0, r2                       
  1c5d8:  ldr r2, [pc, #0x1d8]              -> "Hq2H@}"
  1c5da:  movs r1, #0                       
  1c5dc:  subs r2, r2, r3                   
  1c5de:  sbcs r1, r0                       
  1c5e0:  bhs #0x1c61a                      
  1c5e2:  ldr r1, [pc, #0x1b0]              -> RAM
  1c5e4:  movs r0, #1                       
  1c5e6:  strb r0, [r1]                     
  1c5e8:  b #0x1c61a                        -> 0x1c61a (вне списка функций)
  1c5ea:  ldr r1, [pc, #0x1a8]              -> RAM
  1c5ec:  strb r4, [r1]                     
  1c5ee:  ldr r1, [pc, #0x1a8]              -> RAM
  1c5f0:  strb r4, [r1]                     
  1c5f2:  ldr r1, [pc, #0x14c]              -> RAM
  1c5f4:  str r4, [r1, #0x48]               
  1c5f6:  ldr r2, [sp]                      
  1c5f8:  strh r2, [r1, #0x22]              
  1c5fa:  strb r0, [r3]                     
  1c5fc:  mov r0, r1                        
  1c5fe:  adds r0, #0x80                    
  1c600:  str r6, [r0, #0x20]               
  1c602:  str r5, [r0, #0x24]               
  1c604:  str r6, [r0, #0x28]               
  1c606:  str r5, [r0, #0x2c]               
  1c608:  str r6, [r0, #0x30]               
  1c60a:  str r5, [r0, #0x34]               
  1c60c:  b #0x1c6c2                        -> 0x1c6c2 (вне списка функций)
  1c60e:  ldr r0, [pc, #0x184]              -> RAM
  1c610:  strb r4, [r0]                     
  1c612:  ldr r0, [pc, #0x12c]              -> RAM
  1c614:  adds r0, #0x80                    
  1c616:  str r6, [r0, #0x28]               
  1c618:  str r5, [r0, #0x2c]               
  1c61a:  ldr r0, [pc, #0x12c]              -> RAM
  1c61c:  movs r1, #0x10                    
  1c61e:  ldrsh r1, [r0, r1]                
  1c620:  ldr r0, [pc, #0x11c]              -> RAM
  1c622:  movs r2, #0x22                    
  1c624:  ldrsh r2, [r0, r2]                
  1c626:  subs r0, r1, r2                   
  1c628:  adds r0, r0, #5                   
  1c62a:  cmp r0, #0xb                      
  1c62c:  bhs #0x1c656                      
  1c62e:  ldr r0, [pc, #0x180]              -> периферия
  1c630:  ldr r0, [r0, #0x14]               
  1c632:  lsls r0, r0, #0x10                
  1c634:  bpl #0x1c656                      
  1c636:  ldr r2, [pc, #0x108]              -> RAM
  1c638:  mov r0, r5                        
  1c63a:  adds r2, #0x80                    
  1c63c:  ldr r1, [r2, #0x30]               
  1c63e:  ldr r2, [r2, #0x34]               
  1c640:  subs r3, r6, r1                   
  1c642:  sbcs r0, r2                       
  1c644:  ldr r2, [pc, #0x170]              -> данные @0x0bb80
  1c646:  movs r1, #0                       
  1c648:  subs r2, r2, r3                   
  1c64a:  sbcs r1, r0                       
  1c64c:  bhs #0x1c662                      
  1c64e:  ldr r1, [pc, #0x148]              -> RAM
  1c650:  movs r0, #1                       
  1c652:  strb r0, [r1]                     
  1c654:  b #0x1c662                        -> 0x1c662 (вне списка функций)
  1c656:  ldr r0, [pc, #0x140]              -> RAM
  1c658:  strb r4, [r0]                     
  1c65a:  ldr r0, [pc, #0xe4]               -> RAM
  1c65c:  adds r0, #0x80                    
  1c65e:  str r6, [r0, #0x30]               
  1c660:  str r5, [r0, #0x34]               
  1c662:  ldr r0, [pc, #0xdc]               -> RAM
  1c664:  mov r1, ip                        
  1c666:  str r1, [r0, #0x48]               
  1c668:  ldr r1, [sp]                      
  1c66a:  strh r1, [r0, #0x22]              
  1c66c:  adds r0, #0x80                    
  1c66e:  str r6, [r0, #0x20]               
  1c670:  str r5, [r0, #0x24]               
  1c672:  b #0x1c6c2                        -> 0x1c6c2 (вне списка функций)
  1c674:  b #0x1c6b8                        -> 0x1c6b8 (вне списка функций)
  1c676:  ldr r1, [sp, #4]                  
  1c678:  cmp r1, #1                        
  1c67a:  beq #0x1c6b8                      
  1c67c:  ldr r1, [pc, #0x13c]              -> RAM
  1c67e:  ldrb r1, [r1]                     
  1c680:  cmp r1, #1                        
  1c682:  beq #0x1c6b8                      
  1c684:  ldr r1, [sp, #0xc]                
  1c686:  lsls r1, r1, #0x1d                
  1c688:  bmi #0x1c6b8                      
  1c68a:  ldr r1, [sp, #8]                  
  1c68c:  cmp r1, #1                        
  1c68e:  beq #0x1c6b8                      
  1c690:  ldrb r1, [r3]                     
  1c692:  cmp r1, r0                        
  1c694:  bne #0x1c6b8                      
  1c696:  ldr r1, [pc, #0xa8]               -> RAM
  1c698:  ldrb r1, [r1, #7]                 
  1c69a:  cmp r1, #0                        
  1c69c:  beq #0x1c6b8                      
  1c69e:  ldr r2, [pc, #0x120]              -> RAM
  1c6a0:  movs r1, #0                       
  1c6a2:  ldrsh r1, [r2, r1]                
  1c6a4:  movs r2, #0x28                    
  1c6a6:  cmn r1, r2                        
  1c6a8:  ble #0x1c6b8                      
  1c6aa:  cmp r1, #0x6e                     
  1c6ac:  bgt #0x1c6b8                      
  1c6ae:  ldr r1, [pc, #0x114]              -> RAM
  1c6b0:  movs r2, #0                       
  1c6b2:  ldrsh r2, [r1, r2]                
  1c6b4:  cmp r2, #0x78                     
  1c6b6:  ble #0x1c6c2                      
  1c6b8:  strb r0, [r3]                     
  1c6ba:  ldr r0, [pc, #0xd4]               -> RAM
  1c6bc:  strb r4, [r0]                     
  1c6be:  ldr r0, [pc, #0x80]               -> RAM
  1c6c0:  strb r4, [r0, #8]                 
  1c6c2:  ldr r0, [pc, #0x7c]               -> RAM
  1c6c4:  ldrb r1, [r0, #8]                 
  1c6c6:  cmp r1, #0                        
  1c6c8:  beq #0x1c6d4                      
  1c6ca:  cmp r1, #1                        
  1c6cc:  beq #0x1c6f8                      
  1c6ce:  cmp r1, #2                        
  1c6d0:  bne #0x1c724                      
  1c6d2:  b #0x1c71e                        -> 0x1c71e (вне списка функций)
  1c6d4:  ldr r1, [pc, #0xbc]               -> RAM
  1c6d6:  ldrb r1, [r1]                     
  1c6d8:  cmp r1, #1                        
  1c6da:  bne #0x1c724                      
  1c6dc:  ldr r1, [pc, #0xb8]               -> RAM
  1c6de:  ldrb r1, [r1]                     
  1c6e0:  cmp r1, #1                        
  1c6e2:  bne #0x1c724                      
  1c6e4:  ldr r1, [sp]                      
  1c6e6:  cmp r1, #0x53                     
  1c6e8:  blt #0x1c724                      
  1c6ea:  ldr r1, [sp, #4]                  
  1c6ec:  cmp r1, #0                        
  1c6ee:  bne #0x1c724                      
  1c6f0:  ldr r2, [pc, #0x9c]               -> RAM
  1c6f2:  movs r1, #1                       
  1c6f4:  strb r1, [r2]                     
  1c6f6:  b #0x1c71a                        -> 0x1c71a (вне списка функций)
  1c6f8:  ldr r1, [r7]                      
  1c6fa:  ldr r2, [r0, #0x48]               
  1c6fc:  ldr r3, [pc, #0xa8]               -> данные @0x00bb7
  1c6fe:  subs r2, r1, r2                   
  1c700:  adds r3, r3, #1                   
  1c702:  cmp r2, r3                        
  1c704:  ble #0x1c70e                      
  1c706:  ldr r1, [pc, #0x88]               -> RAM
  1c708:  strb r4, [r1]                     
  1c70a:  strb r4, [r0, #8]                 
  1c70c:  b #0x1c724                        -> 0x1c724 (вне списка функций)
  1c70e:  cmp r1, #0                        
  1c710:  bne #0x1c724                      
  1c712:  ldr r2, [pc, #0x7c]               -> RAM
  1c714:  movs r1, #1                       
  1c716:  strb r1, [r2]                     
  1c718:  movs r1, #2                       
  1c71a:  strb r1, [r0, #8]                 
  1c71c:  b #0x1c724                        -> 0x1c724 (вне списка функций)
  1c71e:  ldr r1, [r7]                      
  1c720:  cmp r1, #0                        
  1c722:  bgt #0x1c706                      
  1c724:  ldr r1, [pc, #0x18]               -> RAM
  1c726:  ldrb r0, [r1, #7]                 
  1c728:  cmp r0, #1                        
  1c72a:  beq #0x1c7cc                      
  1c72c:  str r4, [r7, #4]                  
  1c72e:  ldr r0, [pc, #0x98]               -> RAM
  1c730:  ldrb r2, [r0]                     
  1c732:  cmp r2, #0                        
  1c734:  beq #0x1c7e0                      
  1c736:  cmp r2, #1                        
  1c738:  bne #0x1c820                      
  1c73a:  b #0x1c80c                        -> 0x1c80c (вне списка функций)
  1c73c:  lsls r2, r5, #0xc                 
  1c73e:  movs r0, #0                       
  1c740:  lsls r0, r1, #0xf                 
  1c742:  movs r0, #0                       
  1c744:  lsls r2, r2, #0xd                 
  1c746:  movs r0, r0                       
  1c748:  asrs r0, r5, #0x1d                
  1c74a:  movs r0, #0                       
  1c74c:  lsls r4, r4, #8                   
  1c74e:  movs r0, #0                       
  1c750:  ldrb r0, [r7, #0x1f]              
  1c752:  movs r0, r0                       
  1c754:  lsls r2, r7, #0xc                 
  1c756:  movs r0, #0                       
  1c758:  lsls r6, r1, #0xc                 
  1c75a:  movs r0, #0                       
  1c75c:  lsls r1, r2, #0xc                 
  1c75e:  movs r0, #0                       
  1c760:  lsls r0, r4, #7                   
  1c762:  movs r0, #0                       
  1c764:  lsls r3, r6, #8                   
  1c766:  movs r0, #0                       
  1c768:  lsls r4, r7, #9                   
  1c76a:  movs r0, #0                       
  1c76c:  lsls r6, r3, #8                   
  1c76e:  movs r0, #0                       
  1c770:  lsls r0, r4, #8                   
  1c772:  movs r0, #0                       
  1c774:  lsls r1, r6, #8                   
  1c776:  movs r0, #0                       
  1c778:  lsls r6, r7, #9                   
  1c77a:  movs r0, #0                       
  1c77c:  lsls r5, r0, #9                   
  1c77e:  movs r0, #0                       
  1c780:  ldrb r0, [r2, #0x10]              
  1c782:  movs r0, r0                       
  1c784:  lsls r0, r6, #8                   
  1c786:  movs r0, #0                       
  1c788:  lsls r0, r0, #0xe                 
  1c78a:  movs r0, #0                       
  1c78c:  lsls r7, r5, #8                   
  1c78e:  movs r0, #0                       
  1c790:  lsls r0, r0, #0xa                 
  1c792:  movs r0, #0                       
  1c794:  lsls r1, r0, #0xa                 
  1c796:  movs r0, #0                       
  1c798:  lsls r2, r0, #0xa                 
  1c79a:  movs r0, #0                       
  1c79c:  lsls r2, r4, #9                   
  1c79e:  movs r0, #0                       
  1c7a0:  lsls r1, r5, #8                   
  1c7a2:  movs r0, #0                       
  1c7a4:  lsls r7, r3, #0xc                 
  1c7a6:  movs r0, #0                       
  1c7a8:  lsrs r7, r6, #0xe                 
  1c7aa:  movs r0, r0                       
  1c7ac:  asrs r7, r5, #0x1d                
  1c7ae:  movs r0, r0                       
  1c7b0:  cmp r4, #0x40                     
  1c7b2:  ands r1, r0                       
  1c7b4:  subs r0, #0x80                    
  1c7b6:  movs r1, r0                       
  1c7b8:  cbnz r0, #0x1c81c                 
  1c7ba:  movs r0, r0                       
  1c7bc:  lsls r4, r5, #2                   
  1c7be:  movs r0, #0                       
  1c7c0:  lsls r4, r3, #0xc                 
  1c7c2:  movs r0, #0                       
  1c7c4:  lsls r0, r2, #0xa                 
  1c7c6:  movs r0, #0                       
  1c7c8:  lsls r0, r0, #9                   
  1c7ca:  movs r0, #0                       
  1c7cc:  ldr r0, [sp, #0x10]               
  1c7ce:  cmp r0, #0                        
  1c7d0:  beq #0x1c7da                      
  1c7d2:  ldr r0, [pc, #0x54]               -> RAM
  1c7d4:  ldrb r0, [r0]                     
  1c7d6:  cmp r0, #1                        
  1c7d8:  beq #0x1c72e                      
  1c7da:  ldr r0, [r7]                      
  1c7dc:  str r0, [r7, #4]                  
  1c7de:  b #0x1c72e                        -> 0x1c72e (вне списка функций)
  1c7e0:  ldr r2, [pc, #0x48]               -> периферия
  1c7e2:  ldr r2, [r2, #0x14]               
  1c7e4:  lsls r3, r2, #0x10                
  1c7e6:  ldr r2, [pc, #0x48]               -> RAM
  1c7e8:  bpl #0x1c808                      
  1c7ea:  ldr r3, [r7, #4]                  
  1c7ec:  cmp r3, #0                        
  1c7ee:  ble #0x1c808                      
  1c7f0:  ldrh r3, [r2]                     
  1c7f2:  movs r2, #0x7d                    
  1c7f4:  lsls r2, r2, #8                   
  1c7f6:  cmp r3, r2                        
  1c7f8:  bls #0x1c820                      
  1c7fa:  ldr r2, [pc, #0x38]               -> RAM
  1c7fc:  movs r3, #1                       
  1c7fe:  ldrh r4, [r2]                     
  1c800:  orrs r4, r3                       
  1c802:  strh r4, [r2]                     
  1c804:  strb r3, [r0]                     
  1c806:  b #0x1c820                        -> 0x1c820 (вне списка функций)
  1c808:  strh r4, [r2]                     
  1c80a:  b #0x1c820                        -> 0x1c820 (вне списка функций)
  1c80c:  str r4, [r7, #4]                  
  1c80e:  ldr r2, [r7]                      
  1c810:  cmp r2, #0                        
  1c812:  bne #0x1c820                      
  1c814:  ldr r2, [pc, #0x1c]               -> RAM
  1c816:  ldrh r3, [r2]                     
  1c818:  lsrs r3, r3, #1                   
  1c81a:  lsls r3, r3, #1                   
  1c81c:  strh r3, [r2]                     
  1c81e:  strb r4, [r0]                     
  1c820:  movs r0, #2                       
  1c822:  strb r0, [r1, #0x10]              
  1c824:  add sp, #0x14                     
  1c826:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1c73c (36 слов) ---
  1c73c:  .word 0x2000032a  ; RAM
  1c740:  .word 0x200003c8  ; RAM
  1c744:  .word 0x00000352  ; данные @0x00352
  1c748:  .word 0x20001768  ; RAM
  1c74c:  .word 0x20000224  ; RAM
  1c750:  .word 0x00007ff8  ; данные @0x07ff8
  1c754:  .word 0x2000033a  ; RAM
  1c758:  .word 0x2000030e  ; RAM
  1c75c:  .word 0x20000311  ; RAM
  1c760:  .word 0x200001e0  ; RAM
  1c764:  .word 0x20000233  ; RAM
  1c768:  .word 0x2000027c  ; RAM
  1c76c:  .word 0x2000021e  ; RAM
  1c770:  .word 0x20000220  ; RAM
  1c774:  .word 0x20000231  ; RAM
  1c778:  .word 0x2000027e  ; RAM
  1c77c:  .word 0x20000245  ; RAM
  1c780:  .word 0x00007c10  ; данные @0x07c10
  1c784:  .word 0x20000230  ; RAM
  1c788:  .word 0x20000380  ; RAM
  1c78c:  .word 0x2000022f  ; RAM
  1c790:  .word 0x20000280  ; RAM
  1c794:  .word 0x20000281  ; RAM
  1c798:  .word 0x20000282  ; RAM
  1c79c:  .word 0x20000262  ; RAM
  1c7a0:  .word 0x20000229  ; RAM
  1c7a4:  .word 0x2000031f  ; RAM
  1c7a8:  .word 0x00000bb7  ; данные @0x00bb7
  1c7ac:  .word 0x0000176f  ; данные @0x0176f
  1c7b0:  .word 0x40012c40  ; периферия
  1c7b4:  .word 0x00013880  ; "Hq2H@}"
  1c7b8:  .word 0x0000bb80  ; данные @0x0bb80
  1c7bc:  .word 0x200000ac  ; RAM
  1c7c0:  .word 0x2000031c  ; RAM
  1c7c4:  .word 0x20000290  ; RAM
  1c7c8:  .word 0x20000240  ; RAM
  ; --- literal-пул @0x1c828 (4 слов) — ВНЕ границ функции ---
  1c828:  .word 0x20000280  ; RAM
  1c82c:  .word 0x40012c40  ; периферия
  1c830:  .word 0x2000023e  ; RAM
  1c834:  .word 0x20000220  ; RAM
```
