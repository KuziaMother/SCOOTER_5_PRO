# func_0x054dc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800054dc) | `0x000054dc` |
| размер кода | 230 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200011f3 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x01e34` (0x00001e34, bl)
- 0x054fc (b, вне списка функций)
- 0x05568 (b, вне списка функций)
- 0x055be (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x054f8..0x05500` (8 Б); цели из: 0x054f0
- `0x05500..0x05548` (72 Б); цели из: 0x054f6
- `0x05548..0x05562` (26 Б); цели из: 0x05542
- `0x05562..0x05568` (6 Б); цели из: 0x05528
- `0x05568..0x055b2` (74 Б); цели из: 0x05560
- `0x055b2..0x055b8` (6 Б); цели из: 0x0559e
- `0x055b8..0x055be` (6 Б); цели из: 0x055b0
- `0x055be..0x055c2` (4 Б); цели из: 0x055b6

## Дизассембляция

```asm
  054dc:  push.w {r4, r5, r6, r7, r8, lr}   
  054e0:  mov r4, r0                        
  054e2:  mov r6, r1                        
  054e4:  movs r7, #0xff                    
  054e6:  movs r5, #0                       
  054e8:  mov r8, r5                        
  054ea:  nop                               
  054ec:  ldrh r0, [r4]                     
  054ee:  cmp r0, #4                        
  054f0:  blt #0x54f8                       
  054f2:  ldrh r0, [r4]                     
  054f4:  cmp r0, #0x28                     
  054f6:  ble #0x5500                       
  054f8:  movs r6, #0                       
  054fa:  movs r0, #0                       
  054fc:  pop.w {r4, r5, r6, r7, r8, pc}    
  05500:  movs r1, #0x2f                    
  05502:  ldr r0, [pc, #0xc0]               -> RAM
  05504:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  05508:  mov r0, r5                        
  0550a:  adds r1, r5, #1                   
  0550c:  uxtb r5, r1                       
  0550e:  adds r1, r4, #2                   
  05510:  ldrb r0, [r1, r0]                 
  05512:  ldr r1, [pc, #0xb0]               -> RAM
  05514:  strb r0, [r1, #1]                 
  05516:  mov r0, r5                        
  05518:  adds r1, r5, #1                   
  0551a:  uxtb r5, r1                       
  0551c:  adds r1, r4, #2                   
  0551e:  ldrb r0, [r1, r0]                 
  05520:  ldr r1, [pc, #0xa0]               -> RAM
  05522:  strb r0, [r1, #2]                 
  05524:  ldrh r0, [r4]                     
  05526:  cmp r0, #4                        
  05528:  beq #0x5562                       
  0552a:  movs r0, #0x10                    
  0552c:  strb r0, [r1]                     
  0552e:  mov r0, r5                        
  05530:  adds r1, r5, #1                   
  05532:  uxtb r5, r1                       
  05534:  adds r1, r4, #2                   
  05536:  ldrb r0, [r1, r0]                 
  05538:  ldr r1, [pc, #0x88]               -> RAM
  0553a:  strb r0, [r1, #3]                 
  0553c:  mov r0, r1                        
  0553e:  ldrb r0, [r0, #3]                 
  05540:  cmp r0, #0x28                     
  05542:  ble #0x5548                       
  05544:  movs r0, #0                       
  05546:  b #0x54fc                         -> 0x054fc (вне списка функций)
  05548:  ldr r0, [pc, #0x78]               -> RAM
  0554a:  ldrb r2, [r0, #3]                 
  0554c:  adds r0, r4, #2                   
  0554e:  adds r1, r0, r5                   
  05550:  ldr r0, [pc, #0x70]               -> RAM
  05552:  adds r0, r0, #5                   
  05554:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  05558:  ldr r0, [pc, #0x68]               -> RAM
  0555a:  ldrb r0, [r0, #3]                 
  0555c:  add r0, r5                        
  0555e:  uxtb r5, r0                       
  05560:  b #0x5568                         -> 0x05568 (вне списка функций)
  05562:  movs r0, #3                       
  05564:  ldr r1, [pc, #0x5c]               -> RAM
  05566:  strb r0, [r1]                     
  05568:  mov r0, r5                        
  0556a:  adds r1, r5, #1                   
  0556c:  uxtb r5, r1                       
  0556e:  adds r1, r4, #2                   
  05570:  ldrb r0, [r1, r0]                 
  05572:  ldr r1, [pc, #0x50]               -> RAM
  05574:  strb.w r0, [r1, #0x2d]            
  05578:  mov r0, r5                        
  0557a:  adds r1, r5, #1                   
  0557c:  uxtb r5, r1                       
  0557e:  adds r1, r4, #2                   
  05580:  ldrb r0, [r1, r0]                 
  05582:  ldr r1, [pc, #0x40]               -> RAM
  05584:  strb.w r0, [r1, #0x2e]            
  05588:  ldrb r0, [r4]                     
  0558a:  subs r0, r0, #2                   
  0558c:  uxtb r1, r0                       
  0558e:  adds r0, r4, #2                   
  05590:  bl #0x1e34                        -> func_0x01e34
  05594:  mov r7, r0                        
  05596:  ldr r0, [pc, #0x2c]               -> RAM
  05598:  ldrb.w r0, [r0, #0x2d]            
  0559c:  cmp r0, r7                        
  0559e:  bne #0x55b2                       
  055a0:  ldr r0, [pc, #0x20]               -> RAM
  055a2:  ldrb.w r0, [r0, #0x2e]            
  055a6:  ldr r1, [pc, #0x1c]               -> RAM
  055a8:  ldrb r1, [r1, #1]                 
  055aa:  rsb.w r1, r1, #0xff               
  055ae:  cmp r0, r1                        
  055b0:  beq #0x55b8                       
  055b2:  movs r6, #0                       
  055b4:  mov r8, r6                        
  055b6:  b #0x55be                         -> 0x055be (вне списка функций)
  055b8:  ldr r6, [pc, #8]                  -> RAM
  055ba:  mov.w r8, #1                      
  055be:  mov r0, r8                        
  055c0:  b #0x54fc                         -> 0x054fc (вне списка функций)
  ; --- literal-пул @0x055c4 (1 слов) — ВНЕ границ функции ---
  055c4:  .word 0x200011f3  ; RAM
```
