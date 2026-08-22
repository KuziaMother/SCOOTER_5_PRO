# func_0x173cc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800173cc) | `0x000173cc` |
| размер кода | 294 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a780 — flash-mirror @0x1a780 (r0)
- 0x0801a794 — flash-mirror @0x1a794 (r1)

## Вызовы (callees)

- `func_0x02d70` (0x00002d70, bl)
- `func_0x085c8` (0x000085c8, bl)
- `func_0x087c8` (0x000087c8, bl)
- `func_0x087e2` (0x000087e2, bl)
- 0x1744a (b, вне списка функций)
- 0x17470 (b, вне списка функций)
- 0x1747a (b, вне списка функций)
- 0x1747e (b, вне списка функций)
- 0x17482 (b, вне списка функций)
- 0x174b8 (b, вне списка функций)
- 0x174d0 (b, вне списка функций)
- 0x174e8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x09678` (bl @0x000096c8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1744a..0x17470` (38 Б); цели из: 0x17444
- `0x17470..0x1747a` (10 Б); цели из: 0x1746a
- `0x1747a..0x1747e` (4 Б); цели из: 0x17476
- `0x1747e..0x17482` (4 Б); цели из: 0x17434
- `0x17482..0x17484` (2 Б); цели из: 0x17478
- `0x17484..0x174b8` (52 Б); цели из: 0x17430
- `0x174b8..0x174d0` (24 Б); цели из: 0x174b2
- `0x174d0..0x174e8` (24 Б); цели из: 0x174ca
- `0x174e8..0x174ec` (4 Б); цели из: 0x174e2
- `0x174ec..0x174f2` (6 Б); цели из: 0x17490

## Дизассембляция

```asm
  173cc:  push {r0, r1, r2, r3, r4, r5, r6, lr}
  173ce:  movs r0, #0                       
  173d0:  str r0, [sp]                      
  173d2:  str r0, [sp, #4]                  
  173d4:  str r0, [sp, #8]                  
  173d6:  str r0, [sp, #0xc]                
  173d8:  movs r5, #0                       
  173da:  movs r4, #0                       
  173dc:  movs r0, #1                       
  173de:  strb.w r0, [sp, #3]               
  173e2:  movs r0, #0                       
  173e4:  str r0, [sp, #8]                  
  173e6:  strb.w r0, [sp, #4]               
  173ea:  ldr r0, [pc, #0x108]              -> flash-mirror @0x1a780
  173ec:  ldrh r0, [r0, #4]                 
  173ee:  ldr r1, [pc, #0x108]              -> flash-mirror @0x1a794
  173f0:  ldrh r1, [r1, #4]                 
  173f2:  orrs r0, r1                       
  173f4:  strh.w r0, [sp]                   
  173f8:  ldr r1, [pc, #0xf8]               -> flash-mirror @0x1a780
  173fa:  ldr r0, [r1]                      
  173fc:  mov r1, sp                        
  173fe:  bl #0x85c8                        -> func_0x085c8
  17402:  movs r0, #0x11                    
  17404:  str r0, [sp, #8]                  
  17406:  ldr r0, [pc, #0xf0]               -> flash-mirror @0x1a794
  17408:  ldrh r0, [r0, #4]                 
  1740a:  strh.w r0, [sp]                   
  1740e:  ldr r1, [pc, #0xe8]               -> flash-mirror @0x1a794
  17410:  ldr r0, [r1]                      
  17412:  mov r1, sp                        
  17414:  bl #0x85c8                        -> func_0x085c8
  17418:  ldr r2, [pc, #0xdc]               -> flash-mirror @0x1a794
  1741a:  ldrh r1, [r2, #4]                 
  1741c:  ldr r0, [r2]                      
  1741e:  movs r2, #0                       
  17420:  bl #0x87e2                        -> func_0x087e2
  17424:  ldr r2, [pc, #0xcc]               -> flash-mirror @0x1a780
  17426:  ldrh r1, [r2, #4]                 
  17428:  ldr r0, [r2]                      
  1742a:  bl #0x87c8                        -> func_0x087c8
  1742e:  cmp r0, #0                        
  17430:  bne #0x17484                      
  17432:  nop                               
  17434:  b #0x1747e                        -> 0x1747e (вне списка функций)
  17436:  ldr r2, [pc, #0xc0]               -> flash-mirror @0x1a794
  17438:  ldrh r1, [r2, #4]                 
  1743a:  ldr r0, [r2]                      
  1743c:  movs r2, #0                       
  1743e:  bl #0x87e2                        -> func_0x087e2
  17442:  movs r4, #0                       
  17444:  b #0x1744a                        -> 0x1744a (вне списка функций)
  17446:  adds r0, r4, #1                   
  17448:  uxth r4, r0                       
  1744a:  cmp.w r4, #0x190                  
  1744e:  blt #0x17446                      
  17450:  ldr r2, [pc, #0xa0]               -> flash-mirror @0x1a780
  17452:  ldrh r1, [r2, #4]                 
  17454:  ldr r0, [r2]                      
  17456:  bl #0x87c8                        -> func_0x087c8
  1745a:  cbnz r0, #0x17478                 
  1745c:  ldr r2, [pc, #0x98]               -> flash-mirror @0x1a794
  1745e:  ldrh r1, [r2, #4]                 
  17460:  ldr r0, [r2]                      
  17462:  movs r2, #1                       
  17464:  bl #0x87e2                        -> func_0x087e2
  17468:  movs r4, #0                       
  1746a:  b #0x17470                        -> 0x17470 (вне списка функций)
  1746c:  adds r0, r4, #1                   
  1746e:  uxth r4, r0                       
  17470:  cmp.w r4, #0x190                  
  17474:  blt #0x1746c                      
  17476:  b #0x1747a                        -> 0x1747a (вне списка функций)
  17478:  b #0x17482                        -> 0x17482 (вне списка функций)
  1747a:  adds r0, r5, #1                   
  1747c:  uxtb r5, r0                       
  1747e:  cmp r5, #9                        
  17480:  blt #0x17436                      
  17482:  nop                               
  17484:  ldr r2, [pc, #0x6c]               -> flash-mirror @0x1a780
  17486:  ldrh r1, [r2, #4]                 
  17488:  ldr r0, [r2]                      
  1748a:  bl #0x87c8                        -> func_0x087c8
  1748e:  cmp r0, #1                        
  17490:  bne #0x174ec                      
  17492:  ldr r0, [pc, #0x60]               -> flash-mirror @0x1a780
  17494:  ldrh r0, [r0, #4]                 
  17496:  strh.w r0, [sp]                   
  1749a:  ldr r1, [pc, #0x58]               -> flash-mirror @0x1a780
  1749c:  ldr r0, [r1]                      
  1749e:  mov r1, sp                        
  174a0:  bl #0x85c8                        -> func_0x085c8
  174a4:  ldr r2, [pc, #0x4c]               -> flash-mirror @0x1a780
  174a6:  ldrh r1, [r2, #4]                 
  174a8:  ldr r0, [r2]                      
  174aa:  movs r2, #0                       
  174ac:  bl #0x87e2                        -> func_0x087e2
  174b0:  movs r4, #0                       
  174b2:  b #0x174b8                        -> 0x174b8 (вне списка функций)
  174b4:  adds r0, r4, #1                   
  174b6:  uxth r4, r0                       
  174b8:  cmp r4, #0xc8                     
  174ba:  blt #0x174b4                      
  174bc:  ldr r2, [pc, #0x38]               -> flash-mirror @0x1a794
  174be:  ldrh r1, [r2, #4]                 
  174c0:  ldr r0, [r2]                      
  174c2:  movs r2, #1                       
  174c4:  bl #0x87e2                        -> func_0x087e2
  174c8:  movs r4, #0                       
  174ca:  b #0x174d0                        -> 0x174d0 (вне списка функций)
  174cc:  adds r0, r4, #1                   
  174ce:  uxth r4, r0                       
  174d0:  cmp r4, #0xc8                     
  174d2:  blt #0x174cc                      
  174d4:  ldr r2, [pc, #0x1c]               -> flash-mirror @0x1a780
  174d6:  ldrh r1, [r2, #4]                 
  174d8:  ldr r0, [r2]                      
  174da:  movs r2, #1                       
  174dc:  bl #0x87e2                        -> func_0x087e2
  174e0:  movs r4, #0                       
  174e2:  b #0x174e8                        -> 0x174e8 (вне списка функций)
  174e4:  adds r0, r4, #1                   
  174e6:  uxth r4, r0                       
  174e8:  cmp r4, #0xc8                     
  174ea:  blt #0x174e4                      
  174ec:  bl #0x2d70                        -> func_0x02d70
  174f0:  pop {r0, r1, r2, r3, r4, r5, r6, pc}
  ; --- literal-пул @0x174f4 (2 слов) — ВНЕ границ функции ---
  174f4:  .word 0x0801a780  ; flash-mirror @0x1a780
  174f8:  .word 0x0801a794  ; flash-mirror @0x1a794
```
