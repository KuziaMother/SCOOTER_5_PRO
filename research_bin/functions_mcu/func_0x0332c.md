# func_0x0332c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000332c) | `0x0000332c` |
| размер кода | 574 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x10110000 — прочее (r1)
- 0x10120000 — прочее (r1)
- 0x10210000 — прочее (r1)
- 0x10220000 — прочее (r1)
- 0x10310000 — прочее (r1)
- 0x10320000 — прочее (r1)
- 0x40010c00 — периферия (r1)

## Вызовы (callees)

- `func_0x02bbc` (0x00002bbc, bl)
- 0x03402 (b, вне списка функций)
- 0x03488 (b, вне списка функций)
- 0x034c8 (b, вне списка функций)
- 0x034da (b, вне списка функций)
- 0x03520 (b, вне списка функций)
- 0x03560 (b, вне списка функций)
- 0x059a4 (bl, вне списка функций)
- `func_0x085c8` (0x000085c8, bl)
- `func_0x087b0` (0x000087b0, bl)
- `func_0x087e2` (0x000087e2, bl)
- `func_0x0c0b4` (0x0000c0b4, bl)
- `func_0x163b4` (0x000163b4, bl)

## Кто вызывает (callers / xrefs)

- `func_0x02a94` (bl @0x00002aac)
- `func_0x02b2c` (bl @0x00002b3c)
- `func_0x02d5c` (bl @0x00002d66)
- `func_0x02d70` (bl @0x00002da4)
- `func_0x02d70` (bl @0x00002dac)
- `func_0x03de4` (bl @0x00003e74)
- `func_0x03de4` (bl @0x00003e7c)
- `func_0x03de4` (bl @0x00003eae)
- `func_0x03de4` (bl @0x00003eb6)
- `func_0x04344` (bl @0x00004450)
- `func_0x04344` (bl @0x00004458)
- `func_0x05bc4` (bl @0x00005be2)
- `func_0x05bc4` (bl @0x00005c1c)
- `func_0x05bc4` (bl @0x00005c58)
- `func_0x05c9c` (bl @0x00005caa)
- `func_0x05cd0` (bl @0x00005d76)
- `func_0x05cd0` (bl @0x00005d7e)
- `func_0x11de8` (bl @0x00012180)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x033cc..0x033fc` (48 Б); цели из: 0x03370, 0x03382, 0x03394, 0x033a6…
- `0x033fc..0x03402` (6 Б); цели из: 0x033da, 0x033ea
- `0x03402..0x0344e` (76 Б); цели из: 0x033fa
- `0x0344e..0x03456` (8 Б); цели из: 0x0343a
- `0x03456..0x0347a` (36 Б); цели из: 0x0344c
- `0x0347a..0x03482` (8 Б); цели из: 0x03466
- `0x03482..0x03488` (6 Б); цели из: 0x03478
- `0x03488..0x034c6` (62 Б); цели из: 0x03454, 0x03480
- `0x034c6..0x034c8` (2 Б); цели из: 0x033ca
- `0x034c8..0x034da` (18 Б); цели из: 0x034c4
- `0x034da..0x03520` (70 Б); цели из: 0x034c6
- `0x03520..0x03540` (32 Б); цели из: 0x034d8
- `0x03540..0x0355c` (28 Б); цели из: 0x0352e
- `0x0355c..0x03560` (4 Б); цели из: 0x0353e
- `0x03560..0x0356a` (10 Б); цели из: 0x0333c

## Дизассембляция

```asm
  0332c:  push {r4, r5, r6, lr}             
  0332e:  sub sp, #0x20                     
  03330:  mov r5, r0                        
  03332:  mov r6, r1                        
  03334:  movs r0, #1                       
  03336:  str r0, [sp]                      
  03338:  movs r4, #0                       
  0333a:  nop                               
  0333c:  b #0x3560                         -> 0x03560 (вне списка функций)
  0333e:  add.w r1, r4, r4, lsl #2          
  03342:  add.w r1, r5, r1, lsl #2          
  03346:  ldr r0, [r1]                      
  03348:  bl #0x163b4                       -> func_0x163b4
  0334c:  add r0, sp, #0x10                 
  0334e:  bl #0x87b0                        -> func_0x087b0
  03352:  add.w r0, r4, r4, lsl #2          
  03356:  add.w r0, r5, r0, lsl #2          
  0335a:  ldrh r0, [r0, #4]                 
  0335c:  strh.w r0, [sp, #0x10]            
  03360:  add.w r0, r4, r4, lsl #2          
  03364:  add.w r0, r5, r0, lsl #2          
  03368:  ldr.w r0, [r0, #7]                
  0336c:  ldr r1, [pc, #0x1fc]              
  0336e:  cmp r0, r1                        
  03370:  beq #0x33cc                       
  03372:  add.w r0, r4, r4, lsl #2          
  03376:  add.w r0, r5, r0, lsl #2          
  0337a:  ldr.w r0, [r0, #7]                
  0337e:  ldr r1, [pc, #0x1f0]              
  03380:  cmp r0, r1                        
  03382:  beq #0x33cc                       
  03384:  add.w r0, r4, r4, lsl #2          
  03388:  add.w r0, r5, r0, lsl #2          
  0338c:  ldr.w r0, [r0, #7]                
  03390:  ldr r1, [pc, #0x1e0]              
  03392:  cmp r0, r1                        
  03394:  beq #0x33cc                       
  03396:  add.w r0, r4, r4, lsl #2          
  0339a:  add.w r0, r5, r0, lsl #2          
  0339e:  ldr.w r0, [r0, #7]                
  033a2:  ldr r1, [pc, #0x1d4]              
  033a4:  cmp r0, r1                        
  033a6:  beq #0x33cc                       
  033a8:  add.w r0, r4, r4, lsl #2          
  033ac:  add.w r0, r5, r0, lsl #2          
  033b0:  ldr.w r0, [r0, #7]                
  033b4:  ldr r1, [pc, #0x1c4]              
  033b6:  cmp r0, r1                        
  033b8:  beq #0x33cc                       
  033ba:  add.w r0, r4, r4, lsl #2          
  033be:  add.w r0, r5, r0, lsl #2          
  033c2:  ldr.w r0, [r0, #7]                
  033c6:  ldr r1, [pc, #0x1b8]              
  033c8:  cmp r0, r1                        
  033ca:  bne #0x34c6                       
  033cc:  add.w r0, r4, r4, lsl #2          
  033d0:  add.w r0, r5, r0, lsl #2          
  033d4:  ldr r0, [r0]                      
  033d6:  ldr r1, [pc, #0x1ac]              -> периферия
  033d8:  cmp r0, r1                        
  033da:  bne #0x33fc                       
  033dc:  add.w r0, r4, r4, lsl #2          
  033e0:  add.w r0, r5, r0, lsl #2          
  033e4:  ldrh r0, [r0, #4]                 
  033e6:  cmp.w r0, #0x800                  
  033ea:  bne #0x33fc                       
  033ec:  add.w r0, r4, r4, lsl #2          
  033f0:  add.w r0, r5, r0, lsl #2          
  033f4:  ldrb r0, [r0, #6]                 
  033f6:  strb.w r0, [sp, #0x14]            
  033fa:  b #0x3402                         -> 0x03402 (вне списка функций)
  033fc:  movs r0, #0                       
  033fe:  strb.w r0, [sp, #0x14]            
  03402:  movs r0, #0                       
  03404:  str r0, [sp, #0x18]               
  03406:  add.w r1, r4, r4, lsl #2          
  0340a:  add.w r1, r5, r1, lsl #2          
  0340e:  ldr r0, [r1]                      
  03410:  add r1, sp, #0x10                 
  03412:  bl #0x85c8                        -> func_0x085c8
  03416:  ldrh.w r1, [sp, #0x10]            
  0341a:  add.w r2, r4, r4, lsl #2          
  0341e:  add.w r2, r5, r2, lsl #2          
  03422:  ldr r0, [r2]                      
  03424:  mov r2, sp                        
  03426:  bl #0x2bbc                        -> func_0x02bbc
  0342a:  add.w r0, r4, r4, lsl #2          
  0342e:  add.w r0, r5, r0, lsl #2          
  03432:  ldr.w r0, [r0, #7]                
  03436:  ldr r1, [pc, #0x134]              
  03438:  cmp r0, r1                        
  0343a:  beq #0x344e                       
  0343c:  add.w r0, r4, r4, lsl #2          
  03440:  add.w r0, r5, r0, lsl #2          
  03444:  ldr.w r0, [r0, #7]                
  03448:  ldr r1, [pc, #0x12c]              
  0344a:  cmp r0, r1                        
  0344c:  bne #0x3456                       
  0344e:  movs r0, #8                       
  03450:  strb.w r0, [sp, #0xd]             
  03454:  b #0x3488                         -> 0x03488 (вне списка функций)
  03456:  add.w r0, r4, r4, lsl #2          
  0345a:  add.w r0, r5, r0, lsl #2          
  0345e:  ldr.w r0, [r0, #7]                
  03462:  ldr r1, [pc, #0x10c]              
  03464:  cmp r0, r1                        
  03466:  beq #0x347a                       
  03468:  add.w r0, r4, r4, lsl #2          
  0346c:  add.w r0, r5, r0, lsl #2          
  03470:  ldr.w r0, [r0, #7]                
  03474:  ldr r1, [pc, #0x104]              
  03476:  cmp r0, r1                        
  03478:  bne #0x3482                       
  0347a:  movs r0, #0xc                     
  0347c:  strb.w r0, [sp, #0xd]             
  03480:  b #0x3488                         -> 0x03488 (вне списка функций)
  03482:  movs r0, #0x10                    
  03484:  strb.w r0, [sp, #0xd]             
  03488:  ldr r0, [sp]                      
  0348a:  str r0, [sp, #8]                  
  0348c:  movs r0, #0                       
  0348e:  strb.w r0, [sp, #0xc]             
  03492:  movs r0, #1                       
  03494:  strb.w r0, [sp, #0xe]             
  03498:  add r0, sp, #8                    
  0349a:  bl #0x59a4                        -> 0x059a4 (вне списка функций)
  0349e:  movs r0, #1                       
  034a0:  strb.w r0, [sp, #7]               
  034a4:  add.w r0, r4, r4, lsl #2          
  034a8:  add.w r0, r5, r0, lsl #2          
  034ac:  ldrb r0, [r0, #0x11]              
  034ae:  strb.w r0, [sp, #4]               
  034b2:  add.w r0, r4, r4, lsl #2          
  034b6:  add.w r0, r5, r0, lsl #2          
  034ba:  ldrb r0, [r0, #0x12]              
  034bc:  strb.w r0, [sp, #5]               
  034c0:  add.w r0, r4, r4, lsl #2          
  034c4:  b #0x34c8                         -> 0x034c8 (вне списка функций)
  034c6:  b #0x34da                         -> 0x034da (вне списка функций)
  034c8:  add.w r0, r5, r0, lsl #2          
  034cc:  ldrb r0, [r0, #0x13]              
  034ce:  strb.w r0, [sp, #6]               
  034d2:  add r0, sp, #4                    
  034d4:  bl #0xc0b4                        -> func_0x0c0b4
  034d8:  b #0x3520                         -> 0x03520 (вне списка функций)
  034da:  add.w r0, r4, r4, lsl #2          
  034de:  add.w r0, r5, r0, lsl #2          
  034e2:  ldrb r0, [r0, #0x10]              
  034e4:  strb.w r0, [sp, #0x13]            
  034e8:  add.w r0, r4, r4, lsl #2          
  034ec:  add.w r0, r5, r0, lsl #2          
  034f0:  ldrb r0, [r0, #6]                 
  034f2:  strb.w r0, [sp, #0x14]            
  034f6:  add.w r0, r4, r4, lsl #2          
  034fa:  add.w r0, r5, r0, lsl #2          
  034fe:  ldr.w r0, [r0, #7]                
  03502:  str r0, [sp, #0x18]               
  03504:  add.w r0, r4, r4, lsl #2          
  03508:  add.w r0, r5, r0, lsl #2          
  0350c:  ldr r0, [r0, #0xc]                
  0350e:  str r0, [sp, #0x1c]               
  03510:  add.w r1, r4, r4, lsl #2          
  03514:  add.w r1, r5, r1, lsl #2          
  03518:  ldr r0, [r1]                      
  0351a:  add r1, sp, #0x10                 
  0351c:  bl #0x85c8                        -> func_0x085c8
  03520:  add.w r0, r4, r4, lsl #2          
  03524:  add.w r0, r5, r0, lsl #2          
  03528:  ldr.w r0, [r0, #7]                
  0352c:  cmp r0, #1                        
  0352e:  beq #0x3540                       
  03530:  add.w r0, r4, r4, lsl #2          
  03534:  add.w r0, r5, r0, lsl #2          
  03538:  ldr.w r0, [r0, #7]                
  0353c:  cmp r0, #0x11                     
  0353e:  bne #0x355c                       
  03540:  add.w r3, r4, r4, lsl #2          
  03544:  add.w r3, r5, r3, lsl #2          
  03548:  ldrb r2, [r3, #0xb]               
  0354a:  ldrh.w r1, [sp, #0x10]            
  0354e:  add.w r3, r4, r4, lsl #2          
  03552:  add.w r3, r5, r3, lsl #2          
  03556:  ldr r0, [r3]                      
  03558:  bl #0x87e2                        -> func_0x087e2
  0355c:  adds r0, r4, #1                   
  0355e:  uxtb r4, r0                       
  03560:  cmp r4, r6                        
  03562:  blt.w #0x333e                     
  03566:  add sp, #0x20                     
  03568:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x0356c (7 слов) — ВНЕ границ функции ---
  0356c:  .word 0x10110000
  03570:  .word 0x10210000
  03574:  .word 0x10310000
  03578:  .word 0x10120000
  0357c:  .word 0x10220000
  03580:  .word 0x10320000
  03584:  .word 0x40010c00  ; периферия
```
