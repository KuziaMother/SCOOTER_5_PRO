# func_0x244d2

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800244d2) | `0x000244d2` |
| размер кода | 262 Б |
| регион | код J |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x23e14 (b, вне списка функций)
- 0x24008 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  244d2:  push {r0, r1, r3, r6, r7, lr}     
  244d4:  ldrh r3, [r4, #0x10]              
  244d6:  movs r3, #0x97                    
  244d8:  ldrb r6, [r2, #0x1b]              
  244da:  str r5, [sp, #0x8c]               
  244dc:  movs r3, #0x6a                    
  244de:  ldr r1, [r5, r7]                  
  244e0:  movs r2, #0x23                    
  244e2:  movs r3, #0x4c                    
  244e4:  lsls r4, r6                       
  244e6:  cmp r7, #0x23                     
  244e8:  movs r3, #0x37                    
  244ea:  cmp r7, #0x3b                     
  244ec:  ldrh r3, [r4, #0x38]              
  244ee:  movs r3, #0x28                    
  244f0:  movs r2, #0xf1                    
  244f2:  adds r3, #0x23                    
  244f4:  movs r3, #0x1e                    
  244f6:  subs r6, r5, r0                   
  244f8:  stm r4!, {r0, r1, r5}             
  244fa:  movs r3, #0x16                    
  244fc:  asrs r2, r3, #0xf                 
  244fe:  ldrb r3, [r4, r4]                 
  24500:  movs r3, #0x11                    
  24502:  lsrs r2, r7, #0x1c                
  24504:  str r3, [r4, #0x30]               
  24506:  movs r3, #0xd                     
  24508:  lsrs r5, r1, #0xf                 
  2450a:  ldr r3, [r4, #0x60]               
  2450c:  movs r3, #0xa                     
  2450e:  lsrs r6, r7, #4                   
  24510:  adds r5, #0x23                    
  24512:  movs r3, #8                       
  24514:  lsls r6, r1, #0x1d                
  24516:  strh r3, [r4, #0x28]              
  24518:  movs r3, #6                       
  2451a:  lsls r4, r2, #0x17                
  2451c:  subs r1, #0x1a                    
  2451e:  movs r3, #4                       
  24520:  lsls r0, r6, #0x12                
  24522:  subs r0, #0x1a                    
  24524:  movs r3, #4                       
  24526:  lsls r6, r1, #0xf                 
  24528:  strb r2, [r3]                     
  2452a:  subs r4, r0, r0                   
  2452c:  lsls r4, r3, #0x10                
  2452e:  bhs #0x24568                      
  24530:  ldrb r2, [r0, r0]                 
  24532:  lsls r1, r3, #0x10                
  24534:  strb r2, [r3, r0]                 
  24536:  subs r4, r0, r0                   
  24538:  lsls r7, r3, #0x10                
  2453a:  strh r1, [r1, r0]                 
  2453c:  asrs r4, r7, #0xb                 
  2453e:  asrs r0, r0, #0xa                 
  24540:  asrs r4, r0, #0xa                 
  24542:  asrs r0, r1, #0xa                 
  24544:  asrs r4, r1, #0x12                
  24546:  ldr r4, [r2, #0x20]               
  24548:  asrs r4, r0, #0x10                
  2454a:  strb r0, [r3, #0x13]              
  2454c:  asrs r3, r0, #0x10                
  2454e:  stm r0!, {r2, r5, r6, r7}         
  24550:  asrs r2, r0, #0x10                
  24552:  adds r5, #0xde                    
  24554:  asrs r2, r0, #0x10                
  24556:  stm r7!, {r0, r1, r2, r5, r7}     
  24558:  asrs r1, r0, #0x10                
  2455a:  ldr r2, [r3, #0x74]               
  2455c:  asrs r1, r0, #0x10                
  2455e:  cmp r0, #0x6e                     
  24560:  subs r1, r0, r4                   
  24562:  vrshr.s64 q1, q12, #0x3c          
  24566:  movs r3, #0xc1                    
  24568:  ldr r5, [sp, #0x1a8]              
  2456a:  strb r3, [r4, #0xc]               
  2456c:  movs r3, #0x7e                    
  2456e:  ldr r1, [r2, #0xc]                
  24570:  lsrs r3, r4, #0x10                
  24572:  movs r3, #0x56                    
  24574:  mov sl, lr                        
  24576:  stm r0!, {r0, r1, r5}             
  24578:  subs r2, r7, r4                   
  2457a:  adds r0, #0xdf                    
  2457c:  movs r2, #0xc8                    
  2457e:  movs r3, #0x28                    
  24580:  movs r2, #0x42                    
  24582:  ble #0x245cc                      
  24584:  movs r3, #0x1c                    
  24586:  adds r3, r5, r1                   
  24588:  pop {r0, r1, r5, pc}              
  2458a:  movs r3, #0x14                    
  2458c:  asrs r6, r5, #6                   
  2458e:  movs r1, #0x23                    
  24590:  movs r3, #0xf                     
  24592:  lsrs r6, r7, #0x13                
  24594:  adds r2, #0x23                    
  24596:  subs r3, r1, r0                   
  24598:  stc2 p4, c6, [sp], #0x68          
  2459c:  subs r4, r7, r3                   
  2459e:  mcrr2 p15, #1, r5, sp, c10        
  245a2:  subs r4, r7, r3                   
  245a4:  ldrb.w lr, [r3, #0x51a]           
  245a8:  subs r4, r6, r3                   
  245aa:  lsls r7, r1, #0x11                
  245ac:  ldm r5!, {r1, r3, r4}             
  245ae:  subs r0, r6, r3                   
  245b0:  lsls r5, r3, #0x11                
  245b2:  .byte 0x1a, 0xfc                  
  245b4:  subs r0, r5, r3                   
  245b6:  lsls r5, r4, #0x12                
  245b8:  ldrsh r2, [r3, r0]                
  245ba:  subs r4, r0, r0                   
  245bc:  lsls r5, r3, #0x10                
  245be:  b #0x24008                        -> 0x24008 (вне списка функций)
  245c0:  subs r1, r0, r0                   
  245c2:  lsls r3, r6, #0x12                
  245c4:  strh r2, [r3, #0x38]              
  245c6:  subs r4, r0, r0                   
  245c8:  lsls r1, r4, #0x11                
  245ca:  subs r7, #0x1a                    
  245cc:  subs r4, r0, r0                   
  245ce:  lsls r1, r4, #0x10                
  245d0:  lsls r2, r3, #0x18                
  245d2:  adds r2, #4                       
  245d4:  movs r0, #0xee                    
  245d6:  b #0x23e14                        -> 0x23e14 (вне списка функций)
```
