# func_0x0b302

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b302) | `0x0000b302` |
| размер кода | 362 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40005400 — периферия (r1)
- 0x40005800 — периферия (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x085c8` (0x000085c8, bl)
- `func_0x087b0` (0x000087b0, bl)
- `func_0x087e2` (0x000087e2, bl)
- `func_0x0982c` (0x0000982c, bl)
- `func_0x0985c` (0x0000985c, bl)
- `func_0x0af94` (0x0000af94, bl)
- 0x0b376 (b, вне списка функций)
- 0x0b462 (b, вне списка функций)
- 0x0bc84 (bl, вне списка функций)
- 0x0c664 (bl, вне списка функций)
- `func_0x0c684` (0x0000c684, bl)
- `func_0x0c6a4` (0x0000c6a4, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0b376..0x0b3a0` (42 Б); цели из: 0x0b338
- `0x0b3a0..0x0b410` (112 Б); цели из: 0x0b396
- `0x0b410..0x0b462` (82 Б); цели из: 0x0b3c2
- `0x0b462..0x0b468` (6 Б); цели из: 0x0b40e, 0x0b416
- `0x0b468..0x0b46c` (4 Б); цели из: 0x0b390

## Дизассембляция

```asm
  0b302:  push {r4, lr}                     
  0b304:  sub sp, #0x18                     
  0b306:  add r0, sp, #8                    
  0b308:  bl #0x87b0                        -> func_0x087b0
  0b30c:  ldrh.w r0, [sp, #0x2c]            
  0b310:  strh.w r0, [sp, #8]               
  0b314:  movs r0, #1                       
  0b316:  str r0, [sp, #0x10]               
  0b318:  movs r0, #0xf                     
  0b31a:  str r0, [sp, #0x14]               
  0b31c:  add r1, sp, #8                    
  0b31e:  ldr r0, [sp, #0x24]               
  0b320:  bl #0x85c8                        -> func_0x085c8
  0b324:  mov.w r0, #0x3e8                  
  0b328:  str r0, [sp, #4]                  
  0b32a:  nop                               
  0b32c:  ldr r0, [sp, #4]                  
  0b32e:  subs r1, r0, #1                   
  0b330:  str r1, [sp, #4]                  
  0b332:  cmp r0, #0                        
  0b334:  bne #0xb32c                       
  0b336:  movs r4, #0                       
  0b338:  b #0xb376                         -> 0x0b376 (вне списка функций)
  0b33a:  ldrh.w r1, [sp, #0x2c]            
  0b33e:  movs r2, #0                       
  0b340:  ldr r0, [sp, #0x24]               
  0b342:  bl #0x87e2                        -> func_0x087e2
  0b346:  movs r0, #0x14                    
  0b348:  str r0, [sp, #4]                  
  0b34a:  nop                               
  0b34c:  ldr r0, [sp, #4]                  
  0b34e:  subs r1, r0, #1                   
  0b350:  str r1, [sp, #4]                  
  0b352:  cmp r0, #0                        
  0b354:  bne #0xb34c                       
  0b356:  ldrh.w r1, [sp, #0x2c]            
  0b35a:  movs r2, #1                       
  0b35c:  ldr r0, [sp, #0x24]               
  0b35e:  bl #0x87e2                        -> func_0x087e2
  0b362:  movs r0, #0x14                    
  0b364:  str r0, [sp, #4]                  
  0b366:  nop                               
  0b368:  ldr r0, [sp, #4]                  
  0b36a:  subs r1, r0, #1                   
  0b36c:  str r1, [sp, #4]                  
  0b36e:  cmp r0, #0                        
  0b370:  bne #0xb368                       
  0b372:  adds r0, r4, #1                   
  0b374:  uxtb r4, r0                       
  0b376:  cmp r4, #9                        
  0b378:  blt #0xb33a                       
  0b37a:  add sp, #0x18                     
  0b37c:  pop {r4}                          
  0b37e:  ldr pc, [sp], #0x14               
  0b382:  movs r0, r0                       
  0b384:  push {r4, lr}                     
  0b386:  sub sp, #0x28                     
  0b388:  mov r4, r0                        
  0b38a:  ldrb.w r0, [r4, #0x10c]           
  0b38e:  cmp r0, #0                        
  0b390:  bne #0xb468                       
  0b392:  ldrb r0, [r4, #0x13]              
  0b394:  cmp r0, #2                        
  0b396:  beq #0xb3a0                       
  0b398:  movs r1, #1                       
  0b39a:  ldr r0, [r4]                      
  0b39c:  bl #0x985c                        -> func_0x0985c
  0b3a0:  movs r1, #0                       
  0b3a2:  ldr r0, [r4]                      
  0b3a4:  bl #0x982c                        -> func_0x0982c
  0b3a8:  movs r2, #0x24                    
  0b3aa:  add.w r1, r4, #0x10               
  0b3ae:  mov r0, sp                        
  0b3b0:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0b3b4:  ldm.w r4, {r0, r1, r2, r3}        
  0b3b8:  bl #0xbc84                        -> 0x0bc84 (вне списка функций)
  0b3bc:  ldr r1, [pc, #0xac]               -> периферия
  0b3be:  ldr r0, [r4]                      
  0b3c0:  cmp r0, r1                        
  0b3c2:  bne #0xb410                       
  0b3c4:  movs r1, #1                       
  0b3c6:  lsls r0, r1, #0x16                
  0b3c8:  bl #0xc684                        -> func_0x0c684
  0b3cc:  movs r1, #0                       
  0b3ce:  mov.w r0, #0x400000               
  0b3d2:  bl #0xc684                        -> func_0x0c684
  0b3d6:  movs r1, #0                       
  0b3d8:  mov.w r0, #0x400000               
  0b3dc:  bl #0xc664                        -> 0x0c664 (вне списка функций)
  0b3e0:  ldr r0, [r4, #4]                  
  0b3e2:  ldr r0, [r0]                      
  0b3e4:  orr r0, r0, #0xf                  
  0b3e8:  ldr r1, [r4, #4]                  
  0b3ea:  str r0, [r1]                      
  0b3ec:  movs r1, #0                       
  0b3ee:  movs r0, #1                       
  0b3f0:  bl #0xc6a4                        -> func_0x0c6a4
  0b3f4:  movs r1, #0                       
  0b3f6:  movs r0, #4                       
  0b3f8:  bl #0xc6a4                        -> func_0x0c6a4
  0b3fc:  movs r1, #1                       
  0b3fe:  lsls r0, r1, #0x16                
  0b400:  bl #0xc684                        -> func_0x0c684
  0b404:  movs r1, #0                       
  0b406:  mov.w r0, #0x400000               
  0b40a:  bl #0xc684                        -> func_0x0c684
  0b40e:  b #0xb462                         -> 0x0b462 (вне списка функций)
  0b410:  ldr r1, [pc, #0x5c]               -> периферия
  0b412:  ldr r0, [r4]                      
  0b414:  cmp r0, r1                        
  0b416:  bne #0xb462                       
  0b418:  movs r1, #1                       
  0b41a:  lsls r0, r1, #0x15                
  0b41c:  bl #0xc684                        -> func_0x0c684
  0b420:  movs r1, #0                       
  0b422:  mov.w r0, #0x200000               
  0b426:  bl #0xc684                        -> func_0x0c684
  0b42a:  movs r1, #0                       
  0b42c:  mov.w r0, #0x200000               
  0b430:  bl #0xc664                        -> 0x0c664 (вне списка функций)
  0b434:  ldr r0, [r4, #4]                  
  0b436:  ldr r0, [r0]                      
  0b438:  orr r0, r0, #0xf                  
  0b43c:  ldr r1, [r4, #4]                  
  0b43e:  str r0, [r1]                      
  0b440:  movs r1, #0                       
  0b442:  movs r0, #1                       
  0b444:  bl #0xc6a4                        -> func_0x0c6a4
  0b448:  movs r1, #0                       
  0b44a:  movs r0, #8                       
  0b44c:  bl #0xc6a4                        -> func_0x0c6a4
  0b450:  movs r1, #1                       
  0b452:  lsls r0, r1, #0x15                
  0b454:  bl #0xc684                        -> func_0x0c684
  0b458:  movs r1, #0                       
  0b45a:  mov.w r0, #0x200000               
  0b45e:  bl #0xc684                        -> func_0x0c684
  0b462:  mov r0, r4                        
  0b464:  bl #0xaf94                        -> func_0x0af94
  0b468:  add sp, #0x28                     
  0b46a:  pop {r4, pc}                      
  ; --- literal-пул @0x0b46c (2 слов) — ВНЕ границ функции ---
  0b46c:  .word 0x40005800  ; периферия
  0b470:  .word 0x40005400  ; периферия
```
