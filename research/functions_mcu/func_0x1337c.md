# func_0x1337c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001337c) | `0x0001337c` |
| размер кода | 1472 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0009eb10 — прочее (r1)
- 0x08019c42 — flash-mirror @0x19c42 (r0)
- 0x20000031 — RAM (r0)
- 0x20000044 — RAM (r0)
- 0x20000080 — RAM (r0)
- 0x20000090 — RAM (r1)
- 0x20000098 — RAM (r0)
- 0x200000d8 — RAM (r0)
- 0x200000da — RAM (r0)
- 0x200000ef — RAM (r0)
- 0x200000f0 — RAM (r1)
- 0x200000f9 — RAM (r1)
- 0x200000fc — RAM (r0)
- 0x20000104 — RAM (r0)
- 0x20000107 — RAM (r0)
- 0x20000f10 — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)
- 0x20000fc7 — RAM (r0)
- 0x20000fd3 — RAM (r0)
- 0x2000106e — RAM (r1)
- 0x20001077 — RAM (r1)
- 0x20001084 — RAM (r1)
- 0x2000109e — RAM (r1)
- 0x200015f7 — RAM (r1)

## Вызовы (callees)

- `func_0x04d48` (0x00004d48, bl)
- `func_0x08938` (0x00008938, bl)
- `func_0x08a44` (0x00008a44, bl)
- `func_0x0a6a4` (0x0000a6a4, bl)
- 0x133c2 (b, вне списка функций)
- 0x133d2 (b, вне списка функций)
- 0x1340c (b, вне списка функций)
- 0x1344a (b, вне списка функций)
- 0x1345c (b, вне списка функций)
- 0x1347c (b, вне списка функций)
- 0x1348e (b, вне списка функций)
- 0x134ae (b, вне списка функций)
- 0x1362c (b, вне списка функций)
- 0x13648 (b, вне списка функций)
- 0x1376a (b, вне списка функций)
- 0x137ee (b, вне списка функций)
- 0x13810 (b, вне списка функций)
- 0x13830 (b, вне списка функций)
- 0x13870 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x133c2..0x133ce` (12 Б); цели из: 0x133ae, 0x133b8
- `0x133ce..0x133d2` (4 Б); цели из: 0x133c8
- `0x133d2..0x13402` (48 Б); цели из: 0x133cc
- `0x13402..0x1340c` (10 Б); цели из: 0x133ee
- `0x1340c..0x1344a` (62 Б); цели из: 0x13400
- `0x1344a..0x13454` (10 Б); цели из: 0x13426, 0x13442
- `0x13454..0x1345c` (8 Б); цели из: 0x1344e
- `0x1345c..0x13478` (28 Б); цели из: 0x13452
- `0x13478..0x1347c` (4 Б); цели из: 0x1346e
- `0x1347c..0x1348c` (16 Б); цели из: 0x13476
- `0x1348c..0x1348e` (2 Б); цели из: 0x13486
- `0x1348e..0x134ae` (32 Б); цели из: 0x1348a
- `0x134ae..0x1362c` (382 Б); цели из: 0x1349a
- `0x1362c..0x13646` (26 Б); цели из: 0x13628
- `0x13646..0x13648` (2 Б); цели из: 0x13642
- `0x13648..0x1376a` (290 Б); цели из: 0x13644
- `0x1376a..0x137e0` (118 Б); цели из: 0x1374c
- `0x137e0..0x137ee` (14 Б); цели из: 0x13776
- `0x137ee..0x13802` (20 Б); цели из: 0x13780
- `0x13802..0x13810` (14 Б); цели из: 0x137f6
- `0x13810..0x13830` (32 Б); цели из: 0x13800
- `0x13830..0x13862` (50 Б); цели из: 0x13822
- `0x13862..0x13870` (14 Б); цели из: 0x13852
- `0x13870..0x1389e` (46 Б); цели из: 0x13860
- `0x1389e..0x138b0` (18 Б); цели из: 0x13894
- `0x138b0..0x13916` (102 Б); цели из: 0x138a6
- `0x13916..0x1393c` (38 Б); цели из: 0x1390c

## Дизассембляция

```asm
  1337c:  push.w {r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, ip, lr}
  13380:  nop                               
  13382:  nop                               
  13384:  mov.w sb, #0                      
  13388:  mov fp, sb                        
  1338a:  mov sl, sb                        
  1338c:  movs r0, #0                       
  1338e:  str r0, [sp, #4]                  
  13390:  str r0, [sp]                      
  13392:  movs r4, #0                       
  13394:  nop                               
  13396:  movs r6, #0                       
  13398:  ldr r0, [pc, #0x3e8]              -> RAM
  1339a:  ldrb r0, [r0, #3]                 
  1339c:  cbz r0, #0x133ba                  
  1339e:  ldr r0, [pc, #0x3e8]              -> RAM
  133a0:  ldr r0, [r0]                      
  133a2:  adds r0, r0, #1                   
  133a4:  ldr r1, [pc, #0x3e0]              -> RAM
  133a6:  str r0, [r1]                      
  133a8:  mov r0, r1                        
  133aa:  ldr r0, [r0]                      
  133ac:  cmp r0, #0x32                     
  133ae:  blo #0x133c2                      
  133b0:  movs r0, #0x32                    
  133b2:  str r0, [r1]                      
  133b4:  movs r0, #1                       
  133b6:  str r0, [sp]                      
  133b8:  b #0x133c2                        -> 0x133c2 (вне списка функций)
  133ba:  movs r0, #0                       
  133bc:  ldr r1, [pc, #0x3c8]              -> RAM
  133be:  str r0, [r1]                      
  133c0:  str r0, [sp]                      
  133c2:  ldr r0, [pc, #0x3c8]              -> RAM
  133c4:  ldrb r0, [r0]                     
  133c6:  cmp r0, #1                        
  133c8:  bne #0x133ce                      
  133ca:  movs r0, #0                       
  133cc:  b #0x133d2                        -> 0x133d2 (вне списка функций)
  133ce:  bl #0x8938                        -> func_0x08938
  133d2:  mov r8, r0                        
  133d4:  bl #0x8a44                        -> func_0x08a44
  133d8:  mov r7, r0                        
  133da:  ldr r1, [pc, #0x3b4]              -> RAM
  133dc:  ldrh r1, [r1, #0x38]              
  133de:  sxth r1, r1                       
  133e0:  add.w r1, r1, r1, lsl #2          
  133e4:  lsls r0, r1, #1                   
  133e6:  bl #0x4d48                        -> func_0x04d48
  133ea:  mov r5, r0                        
  133ec:  cmp r5, #0                        
  133ee:  bge #0x13402                      
  133f0:  movs r0, #0xa                     
  133f2:  sdiv r0, r5, r0                   
  133f6:  rsbs r0, r0, #0                   
  133f8:  uxth.w sb, r0                     
  133fc:  orr sb, sb, #0x8000               
  13400:  b #0x1340c                        -> 0x1340c (вне списка функций)
  13402:  movs r0, #0xa                     
  13404:  sdiv r0, r5, r0                   
  13408:  uxth.w sb, r0                     
  1340c:  ldr r0, [pc, #0x384]              -> RAM
  1340e:  ldrb r0, [r0, #6]                 
  13410:  ubfx r0, r0, #1, #1               
  13414:  ldr r1, [pc, #0x37c]              -> RAM
  13416:  ldrb r1, [r1, #6]                 
  13418:  ubfx r1, r1, #4, #1               
  1341c:  orrs r0, r1                       
  1341e:  cbz r0, #0x13428                  
  13420:  ldr r0, [pc, #0x370]              -> RAM
  13422:  ldrsb.w sl, [r0, #1]              
  13426:  b #0x1344a                        -> 0x1344a (вне списка функций)
  13428:  ldr r0, [pc, #0x368]              -> RAM
  1342a:  ldrb r0, [r0, #6]                 
  1342c:  and r0, r0, #1                    
  13430:  ldr r1, [pc, #0x360]              -> RAM
  13432:  ldrb r1, [r1, #6]                 
  13434:  ubfx r1, r1, #2, #1               
  13438:  orrs r0, r1                       
  1343a:  cbz r0, #0x13444                  
  1343c:  ldr r0, [pc, #0x354]              -> RAM
  1343e:  ldrsb.w sl, [r0, #2]              
  13442:  b #0x1344a                        -> 0x1344a (вне списка функций)
  13444:  ldr r0, [pc, #0x34c]              -> RAM
  13446:  ldrsb.w sl, [r0]                  
  1344a:  cmp.w sl, #0                      
  1344e:  blt #0x13454                      
  13450:  mov r0, sl                        
  13452:  b #0x1345c                        -> 0x1345c (вне списка функций)
  13454:  rsb.w r0, sl, #0                  
  13458:  orr r0, r0, #0x80                 
  1345c:  and fp, r0, #0xff                 
  13460:  ldr r0, [pc, #0x334]              -> RAM
  13462:  ldrb r0, [r0, #4]                 
  13464:  lsrs r0, r0, #7                   
  13466:  cbnz r0, #0x1349c                 
  13468:  ldr r0, [pc, #0x330]              -> RAM
  1346a:  ldrb r0, [r0, #2]                 
  1346c:  cmp r0, #0xc                      
  1346e:  ble #0x13478                      
  13470:  ldr r0, [pc, #0x328]              -> RAM
  13472:  ldrb r0, [r0, #2]                 
  13474:  subs r0, #0xc                     
  13476:  b #0x1347c                        -> 0x1347c (вне списка функций)
  13478:  ldr r0, [pc, #0x320]              -> RAM
  1347a:  ldrb r0, [r0, #2]                 
  1347c:  uxtb r0, r0                       
  1347e:  str r0, [sp, #4]                  
  13480:  ldr r0, [pc, #0x318]              -> RAM
  13482:  ldrb r0, [r0, #2]                 
  13484:  cmp r0, #0xc                      
  13486:  ble #0x1348c                      
  13488:  movs r0, #1                       
  1348a:  b #0x1348e                        -> 0x1348e (вне списка функций)
  1348c:  movs r0, #0                       
  1348e:  ldr r1, [pc, #0x308]              -> RAM
  13490:  ldrb r1, [r1, #4]                 
  13492:  bfi r1, r0, #6, #1                
  13496:  ldr r0, [pc, #0x300]              -> RAM
  13498:  strb r1, [r0, #4]                 
  1349a:  b #0x134ae                        -> 0x134ae (вне списка функций)
  1349c:  ldr r0, [pc, #0x2fc]              -> RAM
  1349e:  ldrb r0, [r0, #2]                 
  134a0:  str r0, [sp, #4]                  
  134a2:  ldr r0, [pc, #0x2f4]              -> RAM
  134a4:  ldrb r0, [r0, #4]                 
  134a6:  bic r0, r0, #0x40                 
  134aa:  ldr r1, [pc, #0x2ec]              -> RAM
  134ac:  strb r0, [r1, #4]                 
  134ae:  ldr r0, [pc, #0x2f0]              -> RAM
  134b0:  ldrb r0, [r0]                     
  134b2:  ldr r1, [pc, #0x2f0]              -> RAM
  134b4:  strb r0, [r1]                     
  134b6:  ldr r0, [pc, #0x2e8]              -> RAM
  134b8:  ldrb r0, [r0, #1]                 
  134ba:  strb r0, [r1, #1]                 
  134bc:  strh.w r8, [r1, #2]               
  134c0:  strh r7, [r1, #4]                 
  134c2:  ldr r0, [pc, #0x2e4]              -> RAM
  134c4:  ldrb r0, [r0]                     
  134c6:  strb r0, [r1, #6]                 
  134c8:  ldr r0, [pc, #0x2e0]              -> RAM
  134ca:  ldrb r0, [r0]                     
  134cc:  strb r0, [r1, #7]                 
  134ce:  ldr r0, [pc, #0x2cc]              -> RAM
  134d0:  ldrb r0, [r0, #5]                 
  134d2:  add.w r0, r0, #0x7d0              
  134d6:  lsrs r0, r0, #8                   
  134d8:  ldr r1, [pc, #0x2bc]              -> RAM
  134da:  strb r0, [r1]                     
  134dc:  ldr r0, [pc, #0x2bc]              -> RAM
  134de:  ldrb r0, [r0, #5]                 
  134e0:  add.w r0, r0, #0x7d0              
  134e4:  strb r0, [r1, #1]                 
  134e6:  ldr r0, [pc, #0x2b4]              -> RAM
  134e8:  ldrb r1, [r0, #4]                 
  134ea:  ldr r0, [pc, #0x2ac]              -> RAM
  134ec:  ldrb r0, [r0, #2]                 
  134ee:  bfi r0, r1, #0, #4                
  134f2:  ldr r1, [pc, #0x2a4]              -> RAM
  134f4:  strb r0, [r1, #2]                 
  134f6:  ldr r0, [pc, #0x2a4]              -> RAM
  134f8:  ldrb r1, [r0, #6]                 
  134fa:  ldr r0, [pc, #0x29c]              -> RAM
  134fc:  ldrb r0, [r0, #2]                 
  134fe:  bfi r0, r1, #4, #4                
  13502:  ldr r1, [pc, #0x294]              -> RAM
  13504:  strb r0, [r1, #2]                 
  13506:  ldr r0, [pc, #0x294]              -> RAM
  13508:  ldrb r0, [r0, #3]                 
  1350a:  strb r0, [r1, #3]                 
  1350c:  ldrb r1, [r1, #4]                 
  1350e:  ldr r0, [sp, #4]                  
  13510:  bfi r1, r0, #0, #6                
  13514:  ldr r0, [pc, #0x280]              -> RAM
  13516:  strb r1, [r0, #4]                 
  13518:  ldr r0, [pc, #0x280]              -> RAM
  1351a:  ldrb r0, [r0, #1]                 
  1351c:  ldr r1, [pc, #0x278]              -> RAM
  1351e:  strb r0, [r1, #5]                 
  13520:  ldr r0, [pc, #0x278]              -> RAM
  13522:  ldrb r0, [r0]                     
  13524:  strb r0, [r1, #6]                 
  13526:  ldr r0, [pc, #0x288]              -> RAM
  13528:  ldrh r0, [r0, #8]                 
  1352a:  movs r1, #0xa                     
  1352c:  sdiv r0, r0, r1                   
  13530:  adds r0, r0, #6                   
  13532:  ldr r1, [pc, #0x280]              -> RAM
  13534:  strb r0, [r1]                     
  13536:  ldr r0, [pc, #0x280]              -> RAM
  13538:  ldrb r0, [r0]                     
  1353a:  strb r0, [r1, #1]                 
  1353c:  ldr r0, [pc, #0x270]              -> RAM
  1353e:  ldrh r0, [r0]                     
  13540:  lsrs r0, r0, #8                   
  13542:  strb r0, [r1, #2]                 
  13544:  ldr r0, [pc, #0x268]              -> RAM
  13546:  ldrb r0, [r0]                     
  13548:  strb r0, [r1, #3]                 
  1354a:  lsr.w r0, sb, #8                  
  1354e:  strb r0, [r1, #4]                 
  13550:  strb.w sb, [r1, #5]               
  13554:  sxtb.w r0, fp                     
  13558:  strb r0, [r1, #6]                 
  1355a:  ldr r0, [pc, #0x254]              -> RAM
  1355c:  ldrb r0, [r0, #0xc]               
  1355e:  lsrs r0, r0, #2                   
  13560:  ldr r1, [pc, #0x24c]              -> RAM
  13562:  ldrb r1, [r1, #0xc]               
  13564:  orr.w r0, r0, r1, lsr #5          
  13568:  ldr r1, [pc, #0x248]              -> RAM
  1356a:  ldrh.w r1, [r1, #7]               
  1356e:  bfi r1, r0, #7, #1                
  13572:  ldr r0, [pc, #0x240]              -> RAM
  13574:  strh.w r1, [r0, #7]               
  13578:  ldr r0, [pc, #0x234]              -> RAM
  1357a:  ldrb r0, [r0, #0xc]               
  1357c:  ldr r1, [pc, #0x230]              -> RAM
  1357e:  ldrb r1, [r1, #0xc]               
  13580:  orr.w r0, r0, r1, lsr #1          
  13584:  ldr r1, [pc, #0x228]              -> RAM
  13586:  ldrb r1, [r1, #0x17]              
  13588:  orrs r0, r1                       
  1358a:  ldr r1, [pc, #0x228]              -> RAM
  1358c:  ldrh.w r1, [r1, #7]               
  13590:  bfi r1, r0, #6, #1                
  13594:  ldr r0, [pc, #0x21c]              -> RAM
  13596:  strh.w r1, [r0, #7]               
  1359a:  ldr r0, [pc, #0x220]              -> RAM
  1359c:  ldrb r0, [r0, #8]                 
  1359e:  lsrs r1, r0, #2                   
  135a0:  ldr r0, [pc, #0x210]              -> RAM
  135a2:  ldrh.w r0, [r0, #7]               
  135a6:  bfi r0, r1, #5, #1                
  135aa:  ldr r1, [pc, #0x208]              -> RAM
  135ac:  strh.w r0, [r1, #7]               
  135b0:  ldr r0, [pc, #0x208]              -> RAM
  135b2:  ldrb r0, [r0, #8]                 
  135b4:  ldr r1, [pc, #0x204]              -> RAM
  135b6:  ldrb r1, [r1, #8]                 
  135b8:  orr.w r0, r0, r1, lsr #1          
  135bc:  ldr r1, [pc, #0x1f4]              -> RAM
  135be:  ldrh.w r1, [r1, #7]               
  135c2:  bfi r1, r0, #4, #1                
  135c6:  ldr r0, [pc, #0x1ec]              -> RAM
  135c8:  strh.w r1, [r0, #7]               
  135cc:  ldr r0, [pc, #0x1c4]              -> RAM
  135ce:  ldrb r0, [r0, #6]                 
  135d0:  lsrs r1, r0, #4                   
  135d2:  ldr r0, [pc, #0x1e0]              -> RAM
  135d4:  ldrh.w r0, [r0, #7]               
  135d8:  bfi r0, r1, #3, #1                
  135dc:  ldr r1, [pc, #0x1d4]              -> RAM
  135de:  strh.w r0, [r1, #7]               
  135e2:  ldr r0, [pc, #0x1b0]              -> RAM
  135e4:  ldrb r0, [r0, #6]                 
  135e6:  lsrs r1, r0, #2                   
  135e8:  ldr r0, [pc, #0x1c8]              -> RAM
  135ea:  ldrh.w r0, [r0, #7]               
  135ee:  bfi r0, r1, #2, #1                
  135f2:  ldr r1, [pc, #0x1c0]              -> RAM
  135f4:  strh.w r0, [r1, #7]               
  135f8:  ldr r0, [pc, #0x198]              -> RAM
  135fa:  ldrb r0, [r0, #6]                 
  135fc:  lsrs r1, r0, #1                   
  135fe:  ldr r0, [pc, #0x1b4]              -> RAM
  13600:  ldrh.w r0, [r0, #7]               
  13604:  bfi r0, r1, #1, #1                
  13608:  ldr r1, [pc, #0x1a8]              -> RAM
  1360a:  strh.w r0, [r1, #7]               
  1360e:  ldr r0, [pc, #0x184]              -> RAM
  13610:  ldrb r0, [r0, #6]                 
  13612:  ldrh.w r1, [r1, #7]               
  13616:  bfi r1, r0, #0, #1                
  1361a:  ldr r0, [pc, #0x198]              -> RAM
  1361c:  strh.w r1, [r0, #7]               
  13620:  ldr r0, [pc, #0x19c]              -> RAM
  13622:  ldrb r0, [r0]                     
  13624:  cbnz r0, #0x1362a                 
  13626:  movs r0, #1                       
  13628:  b #0x1362c                        -> 0x1362c (вне списка функций)
  1362a:  movs r0, #0                       
  1362c:  ldr r1, [pc, #0x184]              -> RAM
  1362e:  ldrh.w r1, [r1, #7]               
  13632:  bfi r1, r0, #0xf, #1              
  13636:  ldr r0, [pc, #0x17c]              -> RAM
  13638:  strh.w r1, [r0, #7]               
  1363c:  ldr r0, [pc, #0x180]              -> RAM
  1363e:  ldrb r0, [r0]                     
  13640:  cmp r0, #1                        
  13642:  bne #0x13646                      
  13644:  b #0x13648                        -> 0x13648 (вне списка функций)
  13646:  movs r0, #0                       
  13648:  ldr r1, [pc, #0x168]              -> RAM
  1364a:  ldrh.w r1, [r1, #7]               
  1364e:  bfi r1, r0, #0xe, #1              
  13652:  ldr r0, [pc, #0x160]              -> RAM
  13654:  strh.w r1, [r0, #7]               
  13658:  ldr r0, [pc, #0x168]              -> RAM
  1365a:  ldrb r1, [r0]                     
  1365c:  ldr r0, [pc, #0x154]              -> RAM
  1365e:  ldrh.w r0, [r0, #7]               
  13662:  bfi r0, r1, #0xd, #1              
  13666:  ldr r1, [pc, #0x14c]              -> RAM
  13668:  strh.w r0, [r1, #7]               
  1366c:  bl #0xa6a4                        -> func_0x0a6a4
  13670:  ldr r1, [pc, #0x140]              -> RAM
  13672:  ldrh.w r1, [r1, #7]               
  13676:  bfi r1, r0, #0xc, #1              
  1367a:  ldr r0, [pc, #0x138]              -> RAM
  1367c:  strh.w r1, [r0, #7]               
  13680:  ldr r0, [pc, #0x100]              -> RAM
  13682:  ldrb r0, [r0, #2]                 
  13684:  lsrs r1, r0, #4                   
  13686:  ldr r0, [pc, #0x12c]              -> RAM
  13688:  ldrh.w r0, [r0, #7]               
  1368c:  bfi r0, r1, #0xb, #1              
  13690:  ldr r1, [pc, #0x120]              -> RAM
  13692:  strh.w r0, [r1, #7]               
  13696:  ldrh.w r1, [r1, #7]               
  1369a:  ldr r0, [sp]                      
  1369c:  bfi r1, r0, #0xa, #1              
  136a0:  ldr r0, [pc, #0x110]              -> RAM
  136a2:  strh.w r1, [r0, #7]               
  136a6:  ldr r0, [pc, #0xec]               -> RAM
  136a8:  ldrb r0, [r0, #9]                 
  136aa:  lsrs r0, r0, #3                   
  136ac:  ldr r1, [pc, #0xe4]               -> RAM
  136ae:  ldrb r1, [r1, #6]                 
  136b0:  orr.w r0, r0, r1, lsr #6          
  136b4:  ldr r1, [pc, #0xfc]               -> RAM
  136b6:  ldrh.w r1, [r1, #7]               
  136ba:  bfi r1, r0, #9, #1                
  136be:  ldr r0, [pc, #0xf4]               -> RAM
  136c0:  strh.w r1, [r0, #7]               
  136c4:  ldr r0, [pc, #0xcc]               -> RAM
  136c6:  ldrb r0, [r0, #9]                 
  136c8:  lsrs r1, r0, #2                   
  136ca:  ldr r0, [pc, #0xe8]               -> RAM
  136cc:  ldrh.w r0, [r0, #7]               
  136d0:  bfi r0, r1, #8, #1                
  136d4:  ldr r1, [pc, #0xdc]               -> RAM
  136d6:  strh.w r0, [r1, #7]               
  136da:  ldr r0, [pc, #0xdc]               -> RAM
  136dc:  ldrh r0, [r0, #2]                 
  136de:  lsrs r0, r0, #8                   
  136e0:  ldr r1, [pc, #0xe4]               -> RAM
  136e2:  strb r0, [r1]                     
  136e4:  ldr r0, [pc, #0xd0]               -> RAM
  136e6:  ldrb r0, [r0, #2]                 
  136e8:  strb r0, [r1, #1]                 
  136ea:  ldr r0, [pc, #0xcc]               -> RAM
  136ec:  ldr r0, [r0, #0xc]                
  136ee:  movs r1, #0xa                     
  136f0:  udiv r0, r0, r1                   
  136f4:  lsrs r0, r0, #8                   
  136f6:  ldr r1, [pc, #0xd0]               -> RAM
  136f8:  strb r0, [r1, #2]                 
  136fa:  ldr r0, [pc, #0xbc]               -> RAM
  136fc:  ldr r0, [r0, #0xc]                
  136fe:  movs r1, #0xa                     
  13700:  udiv r0, r0, r1                   
  13704:  ldr r1, [pc, #0xc0]               -> RAM
  13706:  strb r0, [r1, #3]                 
  13708:  ldr r0, [pc, #0xac]               -> RAM
  1370a:  ldr r0, [r0, #8]                  
  1370c:  movs r1, #0xa                     
  1370e:  udiv r0, r0, r1                   
  13712:  lsrs r0, r0, #8                   
  13714:  ldr r1, [pc, #0xb0]               -> RAM
  13716:  strb r0, [r1, #4]                 
  13718:  ldr r0, [pc, #0x9c]               -> RAM
  1371a:  ldr r0, [r0, #8]                  
  1371c:  movs r1, #0xa                     
  1371e:  udiv r0, r0, r1                   
  13722:  ldr r1, [pc, #0xa4]               -> RAM
  13724:  strb r0, [r1, #5]                 
  13726:  ldr r0, [pc, #0xa4]               -> flash-mirror @0x19c42
  13728:  ldrh r0, [r0]                     
  1372a:  lsrs r0, r0, #8                   
  1372c:  strb r0, [r1, #0xa]               
  1372e:  ldr r0, [pc, #0x9c]               -> flash-mirror @0x19c42
  13730:  ldrb r0, [r0]                     
  13732:  strb r0, [r1, #0xb]               
  13734:  lsr.w r0, r8, #8                  
  13738:  strb r0, [r1, #6]                 
  1373a:  strb.w r8, [r1, #7]               
  1373e:  lsrs r0, r7, #8                   
  13740:  strb r0, [r1, #8]                 
  13742:  strb r7, [r1, #9]                 
  13744:  ldr r0, [pc, #0x70]               -> RAM
  13746:  ldrb r0, [r0, #1]                 
  13748:  strb r0, [r1, #0xc]               
  1374a:  movs r4, #0                       
  1374c:  b #0x1376a                        -> 0x1376a (вне списка функций)
  1374e:  ldr r0, [pc, #0x80]               -> RAM
  13750:  ldrh.w r0, [r0, r4, lsl #1]       
  13754:  asrs r0, r0, #8                   
  13756:  ldr r1, [pc, #0x78]               -> RAM
  13758:  ldrb.w r1, [r1, r4, lsl #1]       
  1375c:  orr.w r0, r0, r1, lsl #8          
  13760:  ldr r1, [pc, #0x70]               -> RAM
  13762:  strh.w r0, [r1, r4, lsl #1]       
  13766:  adds r0, r4, #1                   
  13768:  uxtb r4, r0                       
  1376a:  cmp r4, #0xd                      
  1376c:  blt #0x1374e                      
  1376e:  ldr r0, [pc, #0x68]               -> RAM
  13770:  ldrsb.w r0, [r0]                  
  13774:  cmp r0, #0                        
  13776:  blt #0x137e0                      
  13778:  ldr r0, [pc, #0x5c]               -> RAM
  1377a:  ldrb r0, [r0]                     
  1377c:  ldr r1, [pc, #0x5c]               -> RAM
  1377e:  strb r0, [r1]                     
  13780:  b #0x137ee                        -> 0x137ee (вне списка функций)
  13782:  movs r0, r0                       
  13784:  lsrs r0, r6, #0x1d                
  13786:  movs r0, #0                       
  13788:  lsls r4, r7, #3                   
  1378a:  movs r0, #0                       
  1378c:  movs r1, r6                       
  1378e:  movs r0, #0                       
  13790:  asrs r7, r6, #0x17                
  13792:  movs r0, #0                       
  13794:  lsrs r7, r0, #0x1f                
  13796:  movs r0, #0                       
  13798:  lsls r2, r3, #3                   
  1379a:  movs r0, #0                       
  1379c:  lsls r0, r3, #2                   
  1379e:  movs r0, #0                       
  137a0:  lsls r0, r3, #3                   
  137a2:  movs r0, #0                       
  137a4:  lsls r0, r2, #2                   
  137a6:  movs r0, #0                       
  137a8:  lsls r4, r0, #4                   
  137aa:  movs r0, #0                       
  137ac:  lsls r7, r5, #3                   
  137ae:  movs r0, #0                       
  137b0:  lsrs r5, r2, #0x1e                
  137b2:  movs r0, #0                       
  137b4:  asrs r6, r5, #1                   
  137b6:  movs r0, #0                       
  137b8:  lsrs r3, r2, #0x1f                
  137ba:  movs r0, #0                       
  137bc:  lsrs r3, r7, #0x1e                
  137be:  movs r0, #0                       
  137c0:  lsls r0, r0, #2                   
  137c2:  movs r0, #0                       
  137c4:  lsls r7, r0, #4                   
  137c6:  movs r0, #0                       
  137c8:  asrs r7, r6, #1                   
  137ca:  movs r0, #0                       
  137cc:  ldr r4, [sp, #0x108]              
  137ce:  lsrs r1, r0, #0x20                
  137d0:  lsrs r0, r2, #0x1c                
  137d2:  movs r0, #0                       
  137d4:  asrs r6, r3, #2                   
  137d6:  movs r0, #0                       
  137d8:  lsls r4, r0, #1                   
  137da:  movs r0, #0                       
  137dc:  lsls r1, r7, #3                   
  137de:  movs r0, #0                       
  137e0:  ldr r0, [pc, #0x158]              -> RAM
  137e2:  ldrsb.w r0, [r0]                  
  137e6:  rsb.w r0, r0, #0x80               
  137ea:  ldr r1, [pc, #0x154]              -> RAM
  137ec:  strb r0, [r1]                     
  137ee:  ldr r0, [pc, #0x14c]              -> RAM
  137f0:  ldrsb.w r0, [r0, #1]              
  137f4:  cmp r0, #0                        
  137f6:  blt #0x13802                      
  137f8:  ldr r0, [pc, #0x140]              -> RAM
  137fa:  ldrb r0, [r0, #1]                 
  137fc:  ldr r1, [pc, #0x140]              -> RAM
  137fe:  strb r0, [r1, #1]                 
  13800:  b #0x13810                        -> 0x13810 (вне списка функций)
  13802:  ldr r0, [pc, #0x138]              -> RAM
  13804:  ldrsb.w r0, [r0, #1]              
  13808:  rsb.w r0, r0, #0x80               
  1380c:  ldr r1, [pc, #0x130]              -> RAM
  1380e:  strb r0, [r1, #1]                 
  13810:  ldr r0, [pc, #0x130]              -> RAM
  13812:  ldrb r0, [r0, #9]                 
  13814:  and r0, r0, #1                    
  13818:  cbnz r0, #0x13824                 
  1381a:  ldr r0, [pc, #0x128]              -> RAM
  1381c:  ldr.w r0, [r0, #9]                
  13820:  lsrs r6, r0, #1                   
  13822:  b #0x13830                        -> 0x13830 (вне списка функций)
  13824:  ldr r0, [pc, #0x11c]              -> RAM
  13826:  ldr.w r0, [r0, #9]                
  1382a:  movs r1, #1                       
  1382c:  add.w r6, r1, r0, lsr #1          
  13830:  lsrs r0, r6, #0x10                
  13832:  ldr r1, [pc, #0x114]              -> RAM
  13834:  strb r0, [r1]                     
  13836:  lsrs r0, r6, #8                   
  13838:  strb r0, [r1, #1]                 
  1383a:  strb r6, [r1, #2]                 
  1383c:  ldr r0, [pc, #0x104]              -> RAM
  1383e:  ldr.w r0, [r0, #0xd]              
  13842:  mov.w r1, #0x3e8                  
  13846:  udiv r2, r0, r1                   
  1384a:  mls r0, r1, r2, r0                
  1384e:  cmp.w r0, #0x1f4                  
  13852:  blo #0x13862                      
  13854:  ldr r0, [pc, #0xec]               -> RAM
  13856:  ldr.w r0, [r0, #0xd]              
  1385a:  udiv r0, r0, r1                   
  1385e:  adds r6, r0, #1                   
  13860:  b #0x13870                        -> 0x13870 (вне списка функций)
  13862:  ldr r0, [pc, #0xe0]               -> RAM
  13864:  ldr.w r0, [r0, #0xd]              
  13868:  mov.w r1, #0x3e8                  
  1386c:  udiv r6, r0, r1                   
  13870:  lsrs r0, r6, #8                   
  13872:  ldr r1, [pc, #0xd4]               -> RAM
  13874:  strb r0, [r1, #3]                 
  13876:  strb r6, [r1, #4]                 
  13878:  ldr r0, [pc, #0xd0]               -> RAM
  1387a:  ldrh.w r0, [r0, #0x15]            
  1387e:  asrs r0, r0, #8                   
  13880:  strb r0, [r1, #5]                 
  13882:  ldr r0, [pc, #0xc8]               -> RAM
  13884:  ldrb r0, [r0, #0x15]              
  13886:  strb r0, [r1, #6]                 
  13888:  ldr r0, [pc, #0xb8]               -> RAM
  1388a:  ldr.w r0, [r0, #0x11]             
  1388e:  movw r1, #0x2710                  
  13892:  cmp r0, r1                        
  13894:  blo #0x1389e                      
  13896:  mov r0, r1                        
  13898:  ldr r1, [pc, #0xa8]               -> RAM
  1389a:  str.w r0, [r1, #0x11]             
  1389e:  ldr r0, [pc, #0xa4]               -> RAM
  138a0:  ldr.w r0, [r0, #0x11]             
  138a4:  cmp r0, #0x78                     
  138a6:  bhs #0x138b0                      
  138a8:  movs r0, #0x78                    
  138aa:  ldr r1, [pc, #0x98]               -> RAM
  138ac:  str.w r0, [r1, #0x11]             
  138b0:  ldr r0, [pc, #0x90]               -> RAM
  138b2:  ldrb r0, [r0, #0x11]              
  138b4:  movs r1, #0x28                    
  138b6:  sdiv r0, r0, r1                   
  138ba:  ldr r1, [pc, #0x8c]               -> RAM
  138bc:  strb r0, [r1, #7]                 
  138be:  ldr r0, [pc, #0x90]               -> RAM
  138c0:  ldr r0, [r0, #4]                  
  138c2:  movs r1, #0xa                     
  138c4:  udiv r0, r0, r1                   
  138c8:  lsrs r0, r0, #8                   
  138ca:  ldr r1, [pc, #0x7c]               -> RAM
  138cc:  strb r0, [r1, #8]                 
  138ce:  ldr r0, [pc, #0x80]               -> RAM
  138d0:  ldr r0, [r0, #4]                  
  138d2:  movs r1, #0xa                     
  138d4:  udiv r0, r0, r1                   
  138d8:  ldr r1, [pc, #0x6c]               -> RAM
  138da:  strb r0, [r1, #9]                 
  138dc:  ldr r0, [pc, #0x64]               -> RAM
  138de:  ldrb r0, [r0, #0x19]              
  138e0:  ldr r1, [pc, #0x70]               -> RAM
  138e2:  strb r0, [r1]                     
  138e4:  ldr r0, [pc, #0x5c]               -> RAM
  138e6:  ldrb r0, [r0, #0x1a]              
  138e8:  strb r0, [r1, #1]                 
  138ea:  ldr r0, [pc, #0x58]               -> RAM
  138ec:  ldrb r0, [r0, #0x1b]              
  138ee:  strb r0, [r1, #2]                 
  138f0:  ldr r0, [pc, #0x50]               -> RAM
  138f2:  ldrb r0, [r0, #0x1c]              
  138f4:  strb r0, [r1, #3]                 
  138f6:  ldr r0, [pc, #0x4c]               -> RAM
  138f8:  ldrb r0, [r0, #0x1d]              
  138fa:  strb r0, [r1, #4]                 
  138fc:  ldr r0, [pc, #0x44]               -> RAM
  138fe:  ldrb r0, [r0, #0x1e]              
  13900:  strb r0, [r1, #5]                 
  13902:  ldr r0, [pc, #0x40]               -> RAM
  13904:  ldr.w r0, [r0, #0x15]             
  13908:  ldr r1, [pc, #0x4c]               
  1390a:  cmp r0, r1                        
  1390c:  blo #0x13916                      
  1390e:  mov r0, r1                        
  13910:  ldr r1, [pc, #0x30]               -> RAM
  13912:  str.w r0, [r1, #0x15]             
  13916:  ldr r0, [pc, #0x2c]               -> RAM
  13918:  ldr.w r0, [r0, #0x15]             
  1391c:  movs r1, #0xa                     
  1391e:  udiv r0, r0, r1                   
  13922:  lsrs r0, r0, #8                   
  13924:  ldr r1, [pc, #0x2c]               -> RAM
  13926:  strb r0, [r1, #6]                 
  13928:  ldr r0, [pc, #0x18]               -> RAM
  1392a:  ldr.w r0, [r0, #0x15]             
  1392e:  movs r1, #0xa                     
  13930:  udiv r0, r0, r1                   
  13934:  ldr r1, [pc, #0x1c]               -> RAM
  13936:  strb r0, [r1, #7]                 
  13938:  pop.w {r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, ip, pc}
  ; --- literal-пул @0x13784 (23 слов) ---
  13784:  .word 0x20000f70  ; RAM
  13788:  .word 0x200000fc  ; RAM
  1378c:  .word 0x20000031  ; RAM
  13790:  .word 0x200015f7  ; RAM
  13794:  .word 0x20000fc7  ; RAM
  13798:  .word 0x200000da  ; RAM
  1379c:  .word 0x20000098  ; RAM
  137a0:  .word 0x200000d8  ; RAM
  137a4:  .word 0x20000090  ; RAM
  137a8:  .word 0x20000104  ; RAM
  137ac:  .word 0x200000ef  ; RAM
  137b0:  .word 0x20000f95  ; RAM
  137b4:  .word 0x2000106e  ; RAM
  137b8:  .word 0x20000fd3  ; RAM
  137bc:  .word 0x20000fbb  ; RAM
  137c0:  .word 0x20000080  ; RAM
  137c4:  .word 0x20000107  ; RAM
  137c8:  .word 0x20001077  ; RAM
  137cc:  .word 0x08019c42  ; flash-mirror @0x19c42
  137d0:  .word 0x20000f10  ; RAM
  137d4:  .word 0x2000109e  ; RAM
  137d8:  .word 0x20000044  ; RAM
  137dc:  .word 0x200000f9  ; RAM
  ; --- literal-пул @0x1393c (8 слов) — ВНЕ границ функции ---
  1393c:  .word 0x20000044  ; RAM
  13940:  .word 0x200000f9  ; RAM
  13944:  .word 0x20000f70  ; RAM
  13948:  .word 0x20001084  ; RAM
  1394c:  .word 0x20000f95  ; RAM
  13950:  .word 0x20000fd3  ; RAM
  13954:  .word 0x200000f0  ; RAM
  13958:  .word 0x0009eb10
```
