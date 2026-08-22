# func_0x063b8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800063b8) | `0x000063b8` |
| размер кода | 590 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000186a0 — данные @0x186a0 (r0)
- 0x2000128b — RAM (r0)
- 0x200012ba — RAM (r0)
- 0xffffec78 — прочее (r1)

## Вызовы (callees)

- 0x063ea (b, вне списка функций)
- 0x064ac (b, вне списка функций)
- 0x06562 (b, вне списка функций)
- 0x06572 (b, вне списка функций)
- 0x06574 (b, вне списка функций)
- 0x065a6 (b, вне списка функций)
- 0x065a8 (b, вне списка функций)
- 0x065fa (b, вне списка функций)
- `func_0x08d90` (0x00008d90, bl)
- `func_0x08e14` (0x00008e14, bl)
- 0x08eb4 (bl, вне списка функций)
- 0x08ecc (bl, вне списка функций)
- 0x08ee8 (bl, вне списка функций)
- `func_0x08f58` (0x00008f58, bl)
- `func_0x0e17c` (0x0000e17c, bl)
- `func_0x0e36c` (0x0000e36c, bl)
- `func_0x0e3ec` (0x0000e3ec, bl)
- `func_0x0ea64` (0x0000ea64, bl)
- 0x10e5c (bl, вне списка функций)
- 0x10eac (bl, вне списка функций)
- 0x10f60 (bl, вне списка функций)
- 0x10fa4 (bl, вне списка функций)
- `func_0x16222` (0x00016222, bl)
- 0x16528 (bl, вне списка функций)
- 0x16558 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e658` (bl @0x0000e6a0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x063e8..0x063ea` (2 Б); цели из: 0x063e0
- `0x063ea..0x063f2` (8 Б); цели из: 0x063e6
- `0x063f2..0x06416` (36 Б); цели из: 0x063ec
- `0x06416..0x06466` (80 Б); цели из: 0x06406
- `0x06466..0x0648c` (38 Б); цели из: 0x0645a
- `0x0648c..0x064ac` (32 Б); цели из: 0x0645e
- `0x064ac..0x064d6` (42 Б); цели из: 0x06464
- `0x064d6..0x064ec` (22 Б); цели из: 0x064ba
- `0x064ec..0x0655e` (114 Б); цели из: 0x064e0
- `0x0655e..0x06560` (2 Б); цели из: 0x06558
- `0x06560..0x06562` (2 Б); цели из: 0x06462
- `0x06562..0x0656c` (10 Б); цели из: 0x0655e
- `0x0656c..0x06572` (6 Б); цели из: 0x064ea
- `0x06572..0x06574` (2 Б); цели из: 0x064d4, 0x0656a
- `0x06574..0x065a4` (48 Б); цели из: 0x06560
- `0x065a4..0x065a6` (2 Б); цели из: 0x06584
- `0x065a6..0x065a8` (2 Б); цели из: 0x0648a, 0x064aa, 0x06572
- `0x065a8..0x065e0` (56 Б); цели из: 0x06450
- `0x065e0..0x065f2` (18 Б); цели из: 0x065d6
- `0x065f2..0x065fa` (8 Б); цели из: 0x065e8
- `0x065fa..0x06606` (12 Б); цели из: 0x065de, 0x065f0

## Дизассембляция

```asm
  063b8:  push {r1, r2, r3, r4, r5, r6, r7, lr}
  063ba:  movs r0, #1                       
  063bc:  bl #0x10fa4                       -> 0x10fa4 (вне списка функций)
  063c0:  ldr r0, [pc, #0x244]              -> RAM
  063c2:  ldrb.w r0, [r0, #0x6d]            
  063c6:  cbz r0, #0x63d0                   
  063c8:  bl #0x16528                       -> 0x16528 (вне списка функций)
  063cc:  ldr r1, [pc, #0x238]              -> RAM
  063ce:  str r0, [r1, #0x18]               
  063d0:  bl #0x16528                       -> 0x16528 (вне списка функций)
  063d4:  ldr r1, [pc, #0x230]              -> RAM
  063d6:  ldr r1, [r1, #0x18]               
  063d8:  subs r0, r0, r1                   
  063da:  str r0, [sp, #8]                  
  063dc:  ldr r0, [sp, #8]                  
  063de:  cmp r0, #0                        
  063e0:  bge #0x63e8                       
  063e2:  ldr r0, [sp, #8]                  
  063e4:  rsbs r4, r0, #0                   
  063e6:  b #0x63ea                         -> 0x063ea (вне списка функций)
  063e8:  ldr r4, [sp, #8]                  
  063ea:  cmp r4, #0x32                     
  063ec:  blt #0x63f2                       
  063ee:  movs r0, #0                       
  063f0:  str r0, [sp, #8]                  
  063f2:  ldr r0, [pc, #0x218]              -> RAM
  063f4:  ldrb.w r0, [r0, #0x2d]            
  063f8:  ldr r1, [sp, #8]                  
  063fa:  muls r0, r1, r0                   
  063fc:  str r0, [sp, #8]                  
  063fe:  ldr r0, [pc, #0x208]              -> RAM
  06400:  ldrb.w r0, [r0, #0x70]            
  06404:  cmp r0, #0x1f                     
  06406:  bhs #0x6416                       
  06408:  ldr r0, [pc, #0x1fc]              -> RAM
  0640a:  ldrb.w r0, [r0, #0x70]            
  0640e:  adds r0, r0, #1                   
  06410:  ldr r1, [pc, #0x1f4]              -> RAM
  06412:  strb.w r0, [r1, #0x70]            
  06416:  ldr r0, [pc, #0x1f0]              -> RAM
  06418:  ldrb.w r0, [r0, #0x6e]            
  0641c:  cbnz r0, #0x6452                  
  0641e:  movs r0, #1                       
  06420:  ldr r1, [pc, #0x1e4]              -> RAM
  06422:  strb.w r0, [r1, #0x6e]            
  06426:  movs r0, #2                       
  06428:  strb.w r0, [r1, #0x6f]            
  0642c:  bl #0x16558                       -> 0x16558 (вне списка функций)
  06430:  add.w r0, r0, r0, lsl #2          
  06434:  lsls r6, r0, #1                   
  06436:  mov r0, r6                        
  06438:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  0643c:  bl #0x8d90                        -> func_0x08d90
  06440:  ldr r1, [pc, #0x1c8]              -> RAM
  06442:  str r0, [r1, #0x18]               
  06444:  movs r0, #0                       
  06446:  strb.w r0, [r1, #0x2e]            
  0644a:  movw r0, #0xfffe                  
  0644e:  strh r0, [r1, #0x28]              
  06450:  b #0x65a8                         -> 0x065a8 (вне списка функций)
  06452:  ldr r0, [pc, #0x1b4]              -> RAM
  06454:  ldrb.w r0, [r0, #0x6f]            
  06458:  cmp r0, #1                        
  0645a:  beq #0x6466                       
  0645c:  cmp r0, #2                        
  0645e:  beq #0x648c                       
  06460:  cmp r0, #3                        
  06462:  bne #0x6560                       
  06464:  b #0x64ac                         -> 0x064ac (вне списка функций)
  06466:  bl #0x8e14                        -> func_0x08e14
  0646a:  cbnz r0, #0x648a                  
  0646c:  movs r0, #3                       
  0646e:  ldr r1, [pc, #0x198]              -> RAM
  06470:  strb.w r0, [r1, #0x6f]            
  06474:  movs r0, #0                       
  06476:  str r0, [r1, #0x44]               
  06478:  ldr r1, [pc, #0x190]              -> RAM
  0647a:  strb.w r0, [r1, #0x2e]            
  0647e:  movw r0, #0xfffe                  
  06482:  strh r0, [r1, #0x28]              
  06484:  add r0, sp, #8                    
  06486:  bl #0xea64                        -> func_0x0ea64
  0648a:  b #0x65a6                         -> 0x065a6 (вне списка функций)
  0648c:  movs r0, #3                       
  0648e:  ldr r1, [pc, #0x178]              -> RAM
  06490:  strb.w r0, [r1, #0x6f]            
  06494:  movs r0, #0                       
  06496:  str r0, [r1, #0x44]               
  06498:  ldr r1, [pc, #0x170]              -> RAM
  0649a:  strb.w r0, [r1, #0x2e]            
  0649e:  movw r0, #0xfffe                  
  064a2:  strh r0, [r1, #0x28]              
  064a4:  add r0, sp, #8                    
  064a6:  bl #0xea64                        -> func_0x0ea64
  064aa:  b #0x65a6                         -> 0x065a6 (вне списка функций)
  064ac:  movs r0, #0                       
  064ae:  ldr r1, [pc, #0x15c]              -> RAM
  064b0:  strb.w r0, [r1, #0x2e]            
  064b4:  bl #0x8e14                        -> func_0x08e14
  064b8:  cmp r0, #1                        
  064ba:  bne #0x64d6                       
  064bc:  ldr r1, [pc, #0x148]              -> RAM
  064be:  strb.w r0, [r1, #0x6f]            
  064c2:  movs r0, #0                       
  064c4:  str r0, [r1, #0x44]               
  064c6:  ldr r0, [pc, #0x148]              -> данные @0x186a0
  064c8:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  064cc:  bl #0x8d90                        -> func_0x08d90
  064d0:  ldr r1, [pc, #0x138]              -> RAM
  064d2:  str r0, [r1, #0x18]               
  064d4:  b #0x6572                         -> 0x06572 (вне списка функций)
  064d6:  ldr r0, [pc, #0x130]              -> RAM
  064d8:  ldr r0, [r0, #0x44]               
  064da:  movw r1, #0x8ca0                  
  064de:  cmp r0, r1                        
  064e0:  bhs #0x64ec                       
  064e2:  bl #0x8eb4                        -> 0x08eb4 (вне списка функций)
  064e6:  cmp.w r0, #0xe10                  
  064ea:  blo #0x656c                       
  064ec:  movs r0, #4                       
  064ee:  ldr r1, [pc, #0x118]              -> RAM
  064f0:  strb.w r0, [r1, #0x6f]            
  064f4:  movs r0, #0                       
  064f6:  strb.w r0, [r1, #0x70]            
  064fa:  str r0, [r1, #0x44]               
  064fc:  bl #0x8ecc                        -> 0x08ecc (вне списка функций)
  06500:  mov r6, r0                        
  06502:  add r1, sp, #4                    
  06504:  bl #0xe3ec                        -> func_0x0e3ec
  06508:  ldrsh.w r5, [sp, #4]              
  0650c:  bl #0x8ee8                        -> 0x08ee8 (вне списка функций)
  06510:  mov r6, r0                        
  06512:  add r1, sp, #4                    
  06514:  bl #0xe3ec                        -> func_0x0e3ec
  06518:  mov r2, sp                        
  0651a:  ldrsh.w r1, [sp, #4]              
  0651e:  mov r0, r5                        
  06520:  bl #0xe36c                        -> func_0x0e36c
  06524:  ldrsh.w r1, [sp]                  
  06528:  add.w r1, r1, r1, lsl #2          
  0652c:  lsls r0, r1, #1                   
  0652e:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  06532:  bl #0x8d90                        -> func_0x08d90
  06536:  ldr r1, [pc, #0xd4]               -> RAM
  06538:  str r0, [r1, #0x18]               
  0653a:  movs r0, #1                       
  0653c:  strb.w r0, [r1, #0x2e]            
  06540:  bl #0x8f58                        -> func_0x08f58
  06544:  mov r6, r0                        
  06546:  add r2, sp, #4                    
  06548:  mov r1, r6                        
  0654a:  ldrsh.w r0, [sp]                  
  0654e:  bl #0xe17c                        -> func_0x0e17c
  06552:  ldrsh.w r0, [sp, #4]              
  06556:  cmp r0, #0                        
  06558:  bge #0x655e                       
  0655a:  movs r0, #0                       
  0655c:  str r0, [sp, #4]                  
  0655e:  b #0x6562                         -> 0x06562 (вне списка функций)
  06560:  b #0x6574                         -> 0x06574 (вне списка функций)
  06562:  ldrh.w r0, [sp, #4]               
  06566:  ldr r1, [pc, #0xa4]               -> RAM
  06568:  strh r0, [r1, #0x28]              
  0656a:  b #0x6572                         -> 0x06572 (вне списка функций)
  0656c:  add r0, sp, #8                    
  0656e:  bl #0xea64                        -> func_0x0ea64
  06572:  b #0x65a6                         -> 0x065a6 (вне списка функций)
  06574:  movs r0, #1                       
  06576:  ldr r1, [pc, #0x94]               -> RAM
  06578:  strb.w r0, [r1, #0x2e]            
  0657c:  ldr r0, [pc, #0x88]               -> RAM
  0657e:  ldrb.w r0, [r0, #0x70]            
  06582:  cmp r0, #0x14                     
  06584:  blt #0x65a4                       
  06586:  movs r0, #3                       
  06588:  ldr r1, [pc, #0x7c]               -> RAM
  0658a:  strb.w r0, [r1, #0x6f]            
  0658e:  movs r0, #0                       
  06590:  str r0, [r1, #0x44]               
  06592:  ldr r1, [pc, #0x78]               -> RAM
  06594:  strb.w r0, [r1, #0x2e]            
  06598:  movw r0, #0xfffe                  
  0659c:  strh r0, [r1, #0x28]              
  0659e:  add r0, sp, #8                    
  065a0:  bl #0xea64                        -> func_0x0ea64
  065a4:  nop                               
  065a6:  nop                               
  065a8:  movs r0, #0                       
  065aa:  ldr r1, [pc, #0x5c]               -> RAM
  065ac:  strb.w r0, [r1, #0x6d]            
  065b0:  bl #0x16528                       -> 0x16528 (вне списка функций)
  065b4:  ldr r1, [pc, #0x50]               -> RAM
  065b6:  str r0, [r1, #0x18]               
  065b8:  movs r0, #0                       
  065ba:  bl #0x10fa4                       -> 0x10fa4 (вне списка функций)
  065be:  ldr r1, [pc, #0x4c]               -> RAM
  065c0:  ldr r0, [r1, #0x18]               
  065c2:  movs r1, #0xa                     
  065c4:  bl #0x16222                       -> func_0x16222
  065c8:  sxth r0, r0                       
  065ca:  str r0, [sp, #4]                  
  065cc:  ldrsh.w r0, [sp, #4]              
  065d0:  movw r1, #0x2710                  
  065d4:  cmp r0, r1                        
  065d6:  ble #0x65e0                       
  065d8:  mov r0, r1                        
  065da:  bl #0x10eac                       -> 0x10eac (вне списка функций)
  065de:  b #0x65fa                         -> 0x065fa (вне списка функций)
  065e0:  ldrsh.w r0, [sp, #4]              
  065e4:  ldr r1, [pc, #0x2c]               
  065e6:  cmp r0, r1                        
  065e8:  bge #0x65f2                       
  065ea:  mov r0, r1                        
  065ec:  bl #0x10eac                       -> 0x10eac (вне списка функций)
  065f0:  b #0x65fa                         -> 0x065fa (вне списка функций)
  065f2:  ldrsh.w r0, [sp, #4]              
  065f6:  bl #0x10eac                       -> 0x10eac (вне списка функций)
  065fa:  ldr r1, [pc, #0x10]               -> RAM
  065fc:  ldrb.w r0, [r1, #0x2e]            
  06600:  bl #0x10f60                       -> 0x10f60 (вне списка функций)
  06604:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  ; --- literal-пул @0x06608 (4 слов) — ВНЕ границ функции ---
  06608:  .word 0x200012ba  ; RAM
  0660c:  .word 0x2000128b  ; RAM
  06610:  .word 0x000186a0  ; данные @0x186a0
  06614:  .word 0xffffec78
```
