# func_0x085c8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800085c8) | `0x000085c8` |
| размер кода | 484 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40010400 — периферия (r7)

## Вызовы (callees)

- 0x0864e (b, вне списка функций)
- 0x086e2 (b, вне списка функций)
- 0x0879e (b, вне списка функций)
- 0x087a0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01858` (bl @0x0000187a)
- `func_0x0332c` (bl @0x00003412)
- `func_0x0332c` (bl @0x0000351c)
- `func_0x03588` (bl @0x000035b6)
- `func_0x03588` (bl @0x000035be)
- `func_0x03588` (bl @0x000035c6)
- `func_0x03588` (bl @0x000035d6)
- `func_0x0ae9a` (bl @0x0000aef4)
- `func_0x0ae9a` (bl @0x0000af14)
- `func_0x0ae9a` (bl @0x0000af64)
- `func_0x0ae9a` (bl @0x0000af8a)
- `func_0x0aece` (bl @0x0000aef4)
- `func_0x0aece` (bl @0x0000af14)
- `func_0x0aece` (bl @0x0000af64)
- `func_0x0aece` (bl @0x0000af8a)
- `func_0x0b302` (bl @0x0000b320)
- `func_0x0bc86` (bl @0x0000bcb0)
- `func_0x107ec` (bl @0x0001081e)
- `func_0x107ec` (bl @0x00010836)
- `func_0x107ec` (bl @0x0001084c)
- `func_0x107ec` (bl @0x00010864)
- `func_0x173cc` (bl @0x000173fe)
- `func_0x173cc` (bl @0x00017414)
- `func_0x173cc` (bl @0x000174a0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x08602..0x0864e` (76 Б); цели из: 0x085f0, 0x085f6
- `0x0864e..0x0869e` (80 Б); цели из: 0x08600, 0x0862a
- `0x0869e..0x086ca` (44 Б); цели из: 0x08686
- `0x086ca..0x086cc` (2 Б); цели из: 0x085e8
- `0x086cc..0x086e2` (22 Б); цели из: 0x086b6
- `0x086e2..0x086fa` (24 Б); цели из: 0x086c8, 0x086d0
- `0x086fa..0x0870e` (20 Б); цели из: 0x086e6, 0x086ec, 0x086f2
- `0x0870e..0x08734` (38 Б); цели из: 0x086f8
- `0x08734..0x08754` (32 Б); цели из: 0x0872c
- `0x08754..0x08776` (34 Б); цели из: 0x0874c
- `0x08776..0x08798` (34 Б); цели из: 0x0876e
- `0x08798..0x0879e` (6 Б); цели из: 0x08790
- `0x0879e..0x087a0` (2 Б); цели из: 0x086ca, 0x08716
- `0x087a0..0x087ac` (12 Б); цели из: 0x085d6

## Дизассембляция

```asm
  085c8:  push {r4, r5, r6, r7, lr}         
  085ca:  mov r3, r0                        
  085cc:  movs r5, #0                       
  085ce:  movs r0, #0                       
  085d0:  movs r4, #0                       
  085d2:  movs r2, #0                       
  085d4:  movs r6, #0                       
  085d6:  b #0x87a0                         -> 0x087a0 (вне списка функций)
  085d8:  ldrh r7, [r1]                     
  085da:  mov.w ip, #1                      
  085de:  lsl.w ip, ip, r2                  
  085e2:  and.w r6, r7, ip                  
  085e6:  cmp r6, #0                        
  085e8:  beq #0x86ca                       
  085ea:  lsls r5, r2, #1                   
  085ec:  ldr r7, [r1, #8]                  
  085ee:  cmp r7, #2                        
  085f0:  beq #0x8602                       
  085f2:  ldr r7, [r1, #8]                  
  085f4:  cmp r7, #0x12                     
  085f6:  beq #0x8602                       
  085f8:  ldr r7, [r1, #8]                  
  085fa:  cbz r7, #0x8602                   
  085fc:  ldr r7, [r1, #8]                  
  085fe:  cmp r7, #3                        
  08600:  bne #0x864e                       
  08602:  and r7, r2, #8                    
  08606:  cbz r7, #0x862c                   
  08608:  ldr r0, [r3, #0x24]               
  0860a:  lsls r7, r2, #0x1d                
  0860c:  lsr.w ip, r7, #0x1b               
  08610:  movs r7, #0xf                     
  08612:  lsl.w r7, r7, ip                  
  08616:  bics r0, r7                       
  08618:  lsl.w ip, r2, #0x1d               
  0861c:  lsr.w ip, ip, #0x1b               
  08620:  ldr r7, [r1, #0xc]                
  08622:  lsl.w r7, r7, ip                  
  08626:  orrs r0, r7                       
  08628:  str r0, [r3, #0x24]               
  0862a:  b #0x864e                         -> 0x0864e (вне списка функций)
  0862c:  ldr r0, [r3, #0x20]               
  0862e:  lsls r7, r2, #0x1d                
  08630:  lsr.w ip, r7, #0x1b               
  08634:  movs r7, #0xf                     
  08636:  lsl.w r7, r7, ip                  
  0863a:  bics r0, r7                       
  0863c:  lsl.w ip, r2, #0x1d               
  08640:  lsr.w ip, ip, #0x1b               
  08644:  ldr r7, [r1, #0xc]                
  08646:  lsl.w r7, r7, ip                  
  0864a:  orrs r0, r7                       
  0864c:  str r0, [r3, #0x20]               
  0864e:  ldr r4, [r3]                      
  08650:  ldrb r7, [r1, #8]                 
  08652:  and r0, r7, #0xf                  
  08656:  movs r7, #3                       
  08658:  lsls r7, r5                       
  0865a:  bics r4, r7                       
  0865c:  lsl.w r7, r0, r5                  
  08660:  orrs r4, r7                       
  08662:  str r4, [r3]                      
  08664:  ldr r4, [r3, #0xc]                
  08666:  ldrb r7, [r1, #4]                 
  08668:  and r0, r7, #3                    
  0866c:  movs r7, #3                       
  0866e:  lsls r7, r5                       
  08670:  bics r4, r7                       
  08672:  lsl.w r7, r0, r5                  
  08676:  orrs r4, r7                       
  08678:  str r4, [r3, #0xc]                
  0867a:  ldrb r7, [r1, #8]                 
  0867c:  and r7, r7, #3                    
  08680:  cbz r7, #0x869e                   
  08682:  ldr r7, [r1, #8]                  
  08684:  cmp r7, #3                        
  08686:  beq #0x869e                       
  08688:  ldr r4, [r3, #0x2c]               
  0868a:  ldrb r7, [r1, #2]                 
  0868c:  and r0, r7, #3                    
  08690:  movs r7, #3                       
  08692:  lsls r7, r5                       
  08694:  bics r4, r7                       
  08696:  lsl.w r7, r0, r5                  
  0869a:  orrs r4, r7                       
  0869c:  str r4, [r3, #0x2c]               
  0869e:  ldr r0, [r3, #8]                  
  086a0:  movs r7, #1                       
  086a2:  lsls r7, r2                       
  086a4:  bics r0, r7                       
  086a6:  ldrb r7, [r1, #3]                 
  086a8:  and r7, r7, #1                    
  086ac:  lsls r7, r2                       
  086ae:  orrs r0, r7                       
  086b0:  str r0, [r3, #8]                  
  086b2:  ldrb r7, [r1, #4]                 
  086b4:  cmp r7, #2                        
  086b6:  bne #0x86cc                       
  086b8:  ldr r7, [r3, #0x28]               
  086ba:  mov.w ip, #1                      
  086be:  lsl.w ip, ip, r2                  
  086c2:  orr.w r7, r7, ip                  
  086c6:  str r7, [r3, #0x28]               
  086c8:  b #0x86e2                         -> 0x086e2 (вне списка функций)
  086ca:  b #0x879e                         -> 0x0879e (вне списка функций)
  086cc:  ldrb r7, [r1, #4]                 
  086ce:  cmp r7, #1                        
  086d0:  bne #0x86e2                       
  086d2:  ldr r7, [r3, #0x18]               
  086d4:  mov.w ip, #1                      
  086d8:  lsl.w ip, ip, r2                  
  086dc:  orr.w r7, r7, ip                  
  086e0:  str r7, [r3, #0x18]               
  086e2:  ldr r7, [r1, #8]                  
  086e4:  cmp r7, #1                        
  086e6:  beq #0x86fa                       
  086e8:  ldr r7, [r1, #8]                  
  086ea:  cmp r7, #2                        
  086ec:  beq #0x86fa                       
  086ee:  ldr r7, [r1, #8]                  
  086f0:  cmp r7, #0x11                     
  086f2:  beq #0x86fa                       
  086f4:  ldr r7, [r1, #8]                  
  086f6:  cmp r7, #0x12                     
  086f8:  bne #0x870e                       
  086fa:  ldr r0, [r3, #4]                  
  086fc:  movs r7, #1                       
  086fe:  lsls r7, r2                       
  08700:  bics r0, r7                       
  08702:  ldrb r7, [r1, #8]                 
  08704:  ubfx r7, r7, #4, #1               
  08708:  lsls r7, r2                       
  0870a:  orrs r0, r7                       
  0870c:  str r0, [r3, #4]                  
  0870e:  ldr r7, [r1, #8]                  
  08710:  and r7, r7, #0x10000000           
  08714:  cmp r7, #0                        
  08716:  beq #0x879e                       
  08718:  ldr r7, [pc, #0x90]               -> периферия
  0871a:  ldr r0, [r7]                      
  0871c:  movs r7, #1                       
  0871e:  lsls r7, r2                       
  08720:  bics r0, r7                       
  08722:  ldr r7, [r1, #8]                  
  08724:  and r7, r7, #0x10000              
  08728:  cmp.w r7, #0x10000                
  0872c:  bne #0x8734                       
  0872e:  movs r7, #1                       
  08730:  lsls r7, r2                       
  08732:  orrs r0, r7                       
  08734:  ldr r7, [pc, #0x74]               -> периферия
  08736:  str r0, [r7]                      
  08738:  adds r7, r7, #4                   
  0873a:  ldr r0, [r7]                      
  0873c:  movs r7, #1                       
  0873e:  lsls r7, r2                       
  08740:  bics r0, r7                       
  08742:  ldr r7, [r1, #8]                  
  08744:  and r7, r7, #0x20000              
  08748:  cmp.w r7, #0x20000                
  0874c:  bne #0x8754                       
  0874e:  movs r7, #1                       
  08750:  lsls r7, r2                       
  08752:  orrs r0, r7                       
  08754:  ldr r7, [pc, #0x54]               -> периферия
  08756:  adds r7, r7, #4                   
  08758:  str r0, [r7]                      
  0875a:  adds r7, r7, #4                   
  0875c:  ldr r0, [r7]                      
  0875e:  movs r7, #1                       
  08760:  lsls r7, r2                       
  08762:  bics r0, r7                       
  08764:  ldr r7, [r1, #8]                  
  08766:  and r7, r7, #0x100000             
  0876a:  cmp.w r7, #0x100000               
  0876e:  bne #0x8776                       
  08770:  movs r7, #1                       
  08772:  lsls r7, r2                       
  08774:  orrs r0, r7                       
  08776:  ldr r7, [pc, #0x34]               -> периферия
  08778:  adds r7, #8                       
  0877a:  str r0, [r7]                      
  0877c:  adds r7, r7, #4                   
  0877e:  ldr r0, [r7]                      
  08780:  movs r7, #1                       
  08782:  lsls r7, r2                       
  08784:  bics r0, r7                       
  08786:  ldr r7, [r1, #8]                  
  08788:  and r7, r7, #0x200000             
  0878c:  cmp.w r7, #0x200000               
  08790:  bne #0x8798                       
  08792:  movs r7, #1                       
  08794:  lsls r7, r2                       
  08796:  orrs r0, r7                       
  08798:  ldr r7, [pc, #0x10]               -> периферия
  0879a:  adds r7, #0xc                     
  0879c:  str r0, [r7]                      
  0879e:  adds r2, r2, #1                   
  087a0:  ldrh r7, [r1]                     
  087a2:  asrs r7, r2                       
  087a4:  cmp r7, #0                        
  087a6:  bne.w #0x85d8                     
  087aa:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x087ac (1 слов) — ВНЕ границ функции ---
  087ac:  .word 0x40010400  ; периферия
```
