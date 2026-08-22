# func_0x211f8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800211f8) | `0x000211f8` |
| размер кода | 1246 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200000ac — RAM (r0)
- 0x20000170 — RAM (r0)
- 0x200001e0 — RAM (r6)
- 0x20000218 — RAM (r1)
- 0x2000021e — RAM (r0)
- 0x20000220 — RAM (r0)
- 0x20000228 — RAM (r0)
- 0x20000229 — RAM (r7)
- 0x2000022a — RAM (r0)
- 0x2000022d — RAM (r0)
- 0x2000022e — RAM (r7)
- 0x20000230 — RAM (r6)
- 0x20000236 — RAM (r0)
- 0x20000238 — RAM (r3)
- 0x20000244 — RAM (r0)
- 0x20000245 — RAM (r0)
- 0x20000247 — RAM (r1)
- 0x20000280 — RAM (r5)
- 0x20000290 — RAM (r3)
- 0x200002c9 — RAM (r0)
- 0x200002e6 — RAM (r1)
- 0x20000306 — RAM (r1)
- 0x20000308 — RAM (r1)
- 0x2000030a — RAM (r1)
- 0x2000030c — RAM (r1)
- 0x2000030e — RAM (r1)
- 0x2000031c — RAM (r1)
- 0x20000321 — RAM (r0)
- 0x20000334 — RAM (r0)
- 0x20000335 — RAM (r1)
- 0x20000336 — RAM (r0)
- 0x20000339 — RAM (r0)
- 0x20000358 — RAM (r1)
- 0x20000381 — RAM (r1)
- 0x200010b5 — RAM (r5)

## Вызовы (callees)

- 0x2130a (b, вне списка функций)
- 0x21396 (b, вне списка функций)
- 0x213a4 (b, вне списка функций)
- 0x213b2 (b, вне списка функций)
- 0x21404 (b, вне списка функций)
- 0x21414 (b, вне списка функций)
- 0x2143e (b, вне списка функций)
- 0x21450 (b, вне списка функций)
- 0x21456 (b, вне списка функций)
- 0x2145a (b, вне списка функций)
- 0x214a0 (b, вне списка функций)
- 0x214a8 (b, вне списка функций)
- 0x21538 (b, вне списка функций)
- 0x2153c (b, вне списка функций)
- 0x21548 (b, вне списка функций)
- 0x21556 (b, вне списка функций)
- 0x21564 (b, вне списка функций)
- 0x215c0 (b, вне списка функций)
- 0x21676 (b, вне списка функций)
- 0x21686 (b, вне списка функций)
- 0x2168c (b, вне списка функций)
- 0x21690 (b, вне списка функций)
- 0x216ca (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1dfd8` (bl @0x0001e0d0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x21308..0x2130a` (2 Б); цели из: 0x21208
- `0x2130a..0x2135e` (84 Б); цели из: 0x21306
- `0x2135e..0x2138a` (44 Б); цели из: 0x21310
- `0x2138a..0x21390` (6 Б); цели из: 0x21384
- `0x21390..0x21394` (4 Б); цели из: 0x21388
- `0x21394..0x21396` (2 Б); цели из: 0x2138e
- `0x21396..0x213a2` (12 Б); цели из: 0x21392
- `0x213a2..0x213a4` (2 Б); цели из: 0x2139c
- `0x213a4..0x213b0` (12 Б); цели из: 0x213a0
- `0x213b0..0x213b2` (2 Б); цели из: 0x213aa
- `0x213b2..0x213be` (12 Б); цели из: 0x213ae
- `0x213be..0x213d4` (22 Б); цели из: 0x213b8
- `0x213d4..0x213d8` (4 Б); цели из: 0x213c2
- `0x213d8..0x213dc` (4 Б); цели из: 0x213c8
- `0x213dc..0x213e6` (10 Б); цели из: 0x213ce
- `0x213e6..0x213f0` (10 Б); цели из: 0x213e0
- `0x213f0..0x213fe` (14 Б); цели из: 0x213ea
- `0x213fe..0x21402` (4 Б); цели из: 0x213f8
- `0x21402..0x21404` (2 Б); цели из: 0x21314
- `0x21404..0x21406` (2 Б); цели из: 0x21308, 0x21318
- `0x21406..0x21408` (2 Б); цели из: 0x21332
- `0x21408..0x21424` (28 Б); цели из: 0x213fc
- `0x21424..0x21428` (4 Б); цели из: 0x2140c
- `0x21428..0x2142c` (4 Б); цели из: 0x21410
- `0x2142c..0x21446` (26 Б); цели из: 0x2141c
- `0x21446..0x21448` (2 Б); цели из: 0x2135a
- `0x21448..0x2144c` (4 Б); цели из: 0x2143a
- `0x2144c..0x21450` (4 Б); цели из: 0x21434
- `0x21450..0x2145a` (10 Б); цели из: 0x21422
- `0x2145a..0x2148a` (48 Б); цели из: 0x21420, 0x21444, 0x2144e
- `0x2148a..0x214a4` (26 Б); цели из: 0x21486
- `0x214a4..0x214a8` (4 Б); цели из: 0x21452
- `0x214a8..0x2152a` (130 Б); цели из: 0x21402
- `0x2152a..0x21532` (8 Б); цели из: 0x21524
- `0x21532..0x21538` (6 Б); цели из: 0x214c0
- `0x21538..0x2153c` (4 Б); цели из: 0x21446
- `0x2153c..0x21542` (6 Б); цели из: 0x2135c
- `0x21542..0x21546` (4 Б); цели из: 0x2153a
- `0x21546..0x21548` (2 Б); цели из: 0x21540
- `0x21548..0x21554` (12 Б); цели из: 0x21544
- `0x21554..0x21556` (2 Б); цели из: 0x2154e
- `0x21556..0x21562` (12 Б); цели из: 0x21552
- `0x21562..0x21564` (2 Б); цели из: 0x2155c
- `0x21564..0x21570` (12 Б); цели из: 0x21560
- `0x21570..0x21586` (22 Б); цели из: 0x2156a
- `0x21586..0x2158a` (4 Б); цели из: 0x21574
- `0x2158a..0x2158e` (4 Б); цели из: 0x2157a
- `0x2158e..0x21598` (10 Б); цели из: 0x21580
- `0x21598..0x215a2` (10 Б); цели из: 0x21592
- `0x215a2..0x215b0` (14 Б); цели из: 0x2159c
- `0x215b0..0x215b4` (4 Б); цели из: 0x215aa
- `0x215b4..0x215d0` (28 Б); цели из: 0x215ae
- `0x215d0..0x215d4` (4 Б); цели из: 0x215b8
- `0x215d4..0x21664` (144 Б); цели из: 0x215bc
- `0x21664..0x2167e` (26 Б); цели из: 0x215c8
- `0x2167e..0x21682` (4 Б); цели из: 0x21672
- `0x21682..0x21686` (4 Б); цели из: 0x2166c
- `0x21686..0x21690` (10 Б); цели из: 0x215ce
- `0x21690..0x216c0` (48 Б); цели из: 0x215cc, 0x2167c, 0x21684
- `0x216c0..0x216ca` (10 Б); цели из: 0x216bc
- `0x216ca..0x216d2` (8 Б); цели из: 0x21406
- `0x216d2..0x216d6` (4 Б); цели из: 0x21688

## Дизассембляция

```asm
  211f8:  push {r4, r5, r6, r7, lr}         
  211fa:  ldr r0, [pc, #0x3dc]              -> RAM
  211fc:  ldr r1, [pc, #0x3dc]              -> RAM
  211fe:  ldrb r0, [r0]                     
  21200:  ldrb r1, [r1]                     
  21202:  movs r2, #0                       
  21204:  sub sp, #0x7c                     
  21206:  orrs r0, r1                       
  21208:  bne #0x21308                      
  2120a:  ldr r0, [pc, #0x3d4]              -> RAM
  2120c:  ldr r7, [pc, #0x3e8]              -> RAM
  2120e:  ldrb r4, [r0, #0x1a]              
  21210:  ldr r0, [pc, #0x3e0]              -> RAM
  21212:  ldrb r7, [r7]                     
  21214:  ldrb r0, [r0]                     
  21216:  lsls r7, r7, #0x1c                
  21218:  lsls r0, r0, #0x1c                
  2121a:  lsrs r0, r0, #0x18                
  2121c:  lsrs r7, r7, #0x1c                
  2121e:  orrs r0, r7                       
  21220:  str r0, [sp, #0x24]               
  21222:  ldr r0, [pc, #0x3d8]              -> RAM
  21224:  ldr r7, [pc, #0x3dc]              -> RAM
  21226:  ldrb r0, [r0]                     
  21228:  ldr r5, [pc, #0x3b8]              -> RAM
  2122a:  lsls r0, r0, #0x1f                
  2122c:  lsrs r0, r0, #0x1d                
  2122e:  str r0, [sp, #0x28]               
  21230:  ldr r0, [pc, #0x3cc]              -> RAM
  21232:  ldrb r7, [r7]                     
  21234:  ldrb r0, [r0]                     
  21236:  str r7, [sp, #0x3c]               
  21238:  ldrb r5, [r5]                     
  2123a:  lsls r0, r0, #0x1f                
  2123c:  lsls r7, r7, #0x1f                
  2123e:  lsrs r0, r0, #0x18                
  21240:  lsrs r7, r7, #0x19                
  21242:  lsls r5, r5, #0x1f                
  21244:  ldr r6, [pc, #0x3a0]              -> RAM
  21246:  orrs r0, r7                       
  21248:  lsrs r5, r5, #0x1a                
  2124a:  ldr r3, [pc, #0x3a0]              -> RAM
  2124c:  orrs r0, r5                       
  2124e:  ldrb r5, [r6]                     
  21250:  ldrb r3, [r3]                     
  21252:  lsls r5, r5, #0x1f                
  21254:  lsrs r5, r5, #0x1c                
  21256:  lsls r3, r3, #0x1f                
  21258:  orrs r0, r5                       
  2125a:  lsrs r3, r3, #0x1e                
  2125c:  ldr r1, [pc, #0x390]              -> RAM
  2125e:  orrs r0, r3                       
  21260:  str r0, [sp, #4]                  
  21262:  ldrb r0, [r1]                     
  21264:  str r0, [sp, #0x78]               
  21266:  ldr r0, [sp, #4]                  
  21268:  movs r1, #4                       
  2126a:  orrs r0, r1                       
  2126c:  str r0, [sp, #0x20]               
  2126e:  ldr r0, [sp, #4]                  
  21270:  movs r1, #0xfb                    
  21272:  ands r0, r1                       
  21274:  ldr r1, [pc, #0x390]              -> RAM
  21276:  str r0, [sp, #0x1c]               
  21278:  ldrsh r0, [r1, r2]                
  2127a:  movs r1, #0x80                    
  2127c:  mov ip, r0                        
  2127e:  rsbs r3, r0, #0                   
  21280:  mov r0, r1                        
  21282:  orrs r0, r3                       
  21284:  uxtb r0, r0                       
  21286:  str r0, [sp, #0x18]               
  21288:  mov r0, ip                        
  2128a:  uxtb r0, r0                       
  2128c:  ldr r3, [pc, #0x37c]              -> RAM
  2128e:  str r0, [sp, #0x14]               
  21290:  ldrsh r0, [r3, r2]                
  21292:  str r0, [sp, #0x58]               
  21294:  rsbs r0, r0, #0                   
  21296:  orrs r1, r0                       
  21298:  uxtb r0, r1                       
  2129a:  str r0, [sp, #0x10]               
  2129c:  ldr r0, [sp, #0x58]               
  2129e:  uxtb r0, r0                       
  212a0:  str r0, [sp, #0xc]                
  212a2:  ldr r0, [pc, #0x36c]              -> RAM
  212a4:  ldr r6, [pc, #0x39c]              -> RAM
  212a6:  ldrh r0, [r0]                     
  212a8:  str r0, [sp, #0x74]               
  212aa:  ldr r0, [pc, #0x368]              -> RAM
  212ac:  ldrb r0, [r0]                     
  212ae:  str r0, [sp, #0x70]               
  212b0:  ldr r0, [pc, #0x364]              -> RAM
  212b2:  ldrb r0, [r0]                     
  212b4:  str r0, [sp, #0x6c]               
  212b6:  ldr r0, [pc, #0x364]              -> RAM
  212b8:  ldrh r0, [r0]                     
  212ba:  str r0, [sp, #0x68]               
  212bc:  ldr r0, [pc, #0x360]              -> RAM
  212be:  ldrb r0, [r0]                     
  212c0:  str r0, [sp, #0x64]               
  212c2:  ldr r0, [pc, #0x360]              -> RAM
  212c4:  ldrb r0, [r0]                     
  212c6:  str r0, [sp, #0x60]               
  212c8:  ldr r0, [pc, #0x35c]              -> RAM
  212ca:  ldrb r0, [r0]                     
  212cc:  str r0, [sp, #0x5c]               
  212ce:  ldr r0, [pc, #0x35c]              -> RAM
  212d0:  ldrh r0, [r0]                     
  212d2:  lsrs r1, r0, #8                   
  212d4:  uxtb r0, r0                       
  212d6:  str r0, [sp, #8]                  
  212d8:  ldr r0, [pc, #0x354]              -> RAM
  212da:  str r1, [sp, #0x48]               
  212dc:  ldrb r0, [r0]                     
  212de:  lsls r0, r0, #0x1f                
  212e0:  lsrs r0, r0, #0x1a                
  212e2:  str r0, [sp, #0x44]               
  212e4:  ldr r0, [pc, #0x34c]              -> RAM
  212e6:  ldrb r0, [r0]                     
  212e8:  adds r1, r0, #1                   
  212ea:  uxtb r1, r1                       
  212ec:  str r1, [sp, #0x40]               
  212ee:  ldr r1, [pc, #0x348]              -> RAM
  212f0:  ldrb r1, [r1]                     
  212f2:  str r1, [sp, #0x50]               
  212f4:  ldr r1, [pc, #0x344]              -> RAM
  212f6:  ldm r6, {r5, r6}                  
  212f8:  ldrb r3, [r1]                     
  212fa:  str r5, [sp, #0x30]               
  212fc:  movs r5, #0x96                    
  212fe:  muls r0, r5, r0                   
  21300:  ldr r1, [pc, #0x33c]              -> RAM
  21302:  str r6, [sp, #0x2c]               
  21304:  ldr r5, [pc, #0x340]              -> RAM
  21306:  b #0x2130a                        -> 0x2130a (вне списка функций)
  21308:  b #0x21404                        -> 0x21404 (вне списка функций)
  2130a:  str r0, [sp, #0x54]               
  2130c:  adds r0, r0, r5                   
  2130e:  cmp r4, #0                        
  21310:  beq #0x2135e                      
  21312:  cmp r4, #1                        
  21314:  beq #0x21402                      
  21316:  cmp r4, #2                        
  21318:  bne #0x21404                      
  2131a:  ldr r7, [pc, #0x2c4]              -> RAM
  2131c:  mov r4, r6                        
  2131e:  ldr r5, [sp, #0x30]               
  21320:  ldr r6, [r7, #0x58]               
  21322:  ldr r7, [r7, #0x5c]               
  21324:  subs r5, r5, r6                   
  21326:  sbcs r4, r7                       
  21328:  movs r7, #0x19                    
  2132a:  lsls r7, r7, #6                   
  2132c:  movs r6, #0                       
  2132e:  subs r5, r7, r5                   
  21330:  sbcs r6, r4                       
  21332:  bhs #0x21406                      
  21334:  ldr r4, [pc, #0x310]              -> RAM
  21336:  ldr r5, [sp, #0x54]               
  21338:  movs r6, #0xf                     
  2133a:  strb r6, [r4, r5]                 
  2133c:  movs r4, #0x61                    
  2133e:  strb r4, [r0, #1]                 
  21340:  movs r4, #0x30                    
  21342:  strb r4, [r0, #2]                 
  21344:  movs r4, #0xa                     
  21346:  strb r4, [r0, #3]                 
  21348:  ldr r5, [sp, #0x24]               
  2134a:  strb r5, [r0, #4]                 
  2134c:  ldr r5, [sp, #0x28]               
  2134e:  strb r5, [r0, #5]                 
  21350:  ldr r5, [sp, #4]                  
  21352:  strb r5, [r0, #6]                 
  21354:  ldr r5, [sp, #0x3c]               
  21356:  movs r4, #0                       
  21358:  cmp r5, #1                        
  2135a:  beq #0x21446                      
  2135c:  b #0x2153c                        -> 0x2153c (вне списка функций)
  2135e:  ldr r4, [pc, #0x2e8]              -> RAM
  21360:  ldr r5, [sp, #0x54]               
  21362:  movs r6, #0xf                     
  21364:  strb r6, [r4, r5]                 
  21366:  movs r4, #0x61                    
  21368:  strb r4, [r0, #1]                 
  2136a:  movs r4, #0x30                    
  2136c:  strb r4, [r0, #2]                 
  2136e:  movs r4, #0xa                     
  21370:  strb r4, [r0, #3]                 
  21372:  ldr r5, [sp, #0x24]               
  21374:  strb r5, [r0, #4]                 
  21376:  ldr r5, [sp, #0x28]               
  21378:  strb r5, [r0, #5]                 
  2137a:  ldr r5, [sp, #4]                  
  2137c:  strb r5, [r0, #6]                 
  2137e:  ldr r5, [sp, #0x3c]               
  21380:  movs r4, #0                       
  21382:  cmp r5, #1                        
  21384:  bne #0x2138a                      
  21386:  cmp r3, #1                        
  21388:  beq #0x21390                      
  2138a:  ldr r5, [sp, #0x78]               
  2138c:  cmp r5, #0                        
  2138e:  beq #0x21394                      
  21390:  ldr r5, [sp, #0x20]               
  21392:  b #0x21396                        -> 0x21396 (вне списка функций)
  21394:  ldr r5, [sp, #0x1c]               
  21396:  strb r5, [r0, #6]                 
  21398:  mov r5, ip                        
  2139a:  cmp r5, #0                        
  2139c:  bge #0x213a2                      
  2139e:  ldr r5, [sp, #0x18]               
  213a0:  b #0x213a4                        -> 0x213a4 (вне списка функций)
  213a2:  ldr r5, [sp, #0x14]               
  213a4:  strb r5, [r0, #7]                 
  213a6:  ldr r5, [sp, #0x58]               
  213a8:  cmp r5, #0                        
  213aa:  bge #0x213b0                      
  213ac:  ldr r5, [sp, #0x10]               
  213ae:  b #0x213b2                        -> 0x213b2 (вне списка функций)
  213b0:  ldr r5, [sp, #0xc]                
  213b2:  strb r5, [r0, #8]                 
  213b4:  ldr r5, [sp, #0x74]               
  213b6:  lsls r5, r5, #0x1a                
  213b8:  bpl #0x213be                      
  213ba:  movs r5, #0x10                    
  213bc:  b #0x21414                        -> 0x21414 (вне списка функций)
  213be:  ldr r5, [sp, #0x70]               
  213c0:  cmp r5, #1                        
  213c2:  beq #0x213d4                      
  213c4:  ldr r5, [sp, #0x6c]               
  213c6:  cmp r5, #1                        
  213c8:  beq #0x213d8                      
  213ca:  ldr r5, [sp, #0x68]               
  213cc:  lsls r5, r5, #0x1e                
  213ce:  bpl #0x213dc                      
  213d0:  movs r5, #0x24                    
  213d2:  b #0x21414                        -> 0x21414 (вне списка функций)
  213d4:  movs r5, #0x11                    
  213d6:  b #0x21414                        -> 0x21414 (вне списка функций)
  213d8:  movs r5, #0x18                    
  213da:  b #0x21414                        -> 0x21414 (вне списка функций)
  213dc:  ldr r5, [sp, #0x50]               
  213de:  lsls r5, r5, #0x1f                
  213e0:  beq #0x213e6                      
  213e2:  movs r5, #0x28                    
  213e4:  b #0x21414                        -> 0x21414 (вне списка функций)
  213e6:  ldr r5, [sp, #0x50]               
  213e8:  lsls r5, r5, #0x1e                
  213ea:  bpl #0x213f0                      
  213ec:  movs r5, #0x29                    
  213ee:  b #0x21414                        -> 0x21414 (вне списка функций)
  213f0:  movs r6, #0x27                    
  213f2:  mvns r6, r6                       
  213f4:  mov r5, ip                        
  213f6:  cmp ip, r6                        
  213f8:  ble #0x213fe                      
  213fa:  cmp r5, #0x6e                     
  213fc:  ble #0x21408                      
  213fe:  movs r5, #0x45                    
  21400:  b #0x21414                        -> 0x21414 (вне списка функций)
  21402:  b #0x214a8                        -> 0x214a8 (вне списка функций)
  21404:  b #0x214a0                        -> 0x214a0 (вне списка функций)
  21406:  b #0x216ca                        -> 0x216ca (вне списка функций)
  21408:  ldr r5, [sp, #0x64]               
  2140a:  cmp r5, #1                        
  2140c:  beq #0x21424                      
  2140e:  cmp r3, #1                        
  21410:  beq #0x21428                      
  21412:  movs r5, #1                       
  21414:  strb r5, [r1]                     
  21416:  ldr r6, [sp, #0x60]               
  21418:  ldr r5, [pc, #0x208]              -> RAM
  2141a:  cmp r6, #0                        
  2141c:  beq #0x2142c                      
  2141e:  cmp r6, #1                        
  21420:  bne #0x2145a                      
  21422:  b #0x21450                        -> 0x21450 (вне списка функций)
  21424:  movs r5, #0x21                    
  21426:  b #0x21414                        -> 0x21414 (вне списка функций)
  21428:  movs r5, #2                       
  2142a:  b #0x21414                        -> 0x21414 (вне списка функций)
  2142c:  ldrb r1, [r1]                     
  2142e:  ldr r6, [sp, #0x5c]               
  21430:  ldr r7, [pc, #0x1f4]              -> RAM
  21432:  cmp r6, r1                        
  21434:  beq #0x2144c                      
  21436:  strb r1, [r7]                     
  21438:  cmp r3, #1                        
  2143a:  beq #0x21448                      
  2143c:  movs r1, #1                       
  2143e:  strb r1, [r0, #9]                 
  21440:  movs r1, #1                       
  21442:  strb r1, [r5]                     
  21444:  b #0x2145a                        -> 0x2145a (вне списка функций)
  21446:  b #0x21538                        -> 0x21538 (вне списка функций)
  21448:  movs r1, #2                       
  2144a:  b #0x2143e                        -> 0x2143e (вне списка функций)
  2144c:  strb r1, [r0, #9]                 
  2144e:  b #0x2145a                        -> 0x2145a (вне списка функций)
  21450:  cmp r3, #1                        
  21452:  beq #0x214a4                      
  21454:  movs r1, #1                       
  21456:  strb r1, [r0, #9]                 
  21458:  strb r4, [r5]                     
  2145a:  ldr r1, [sp, #0x48]               
  2145c:  strb r1, [r0, #0xa]               
  2145e:  ldr r1, [sp, #8]                  
  21460:  strb r1, [r0, #0xb]               
  21462:  strb r4, [r0, #0xc]               
  21464:  ldr r1, [sp, #0x44]               
  21466:  ldr r3, [pc, #0x1cc]              -> RAM
  21468:  strb r1, [r0, #0xd]               
  2146a:  movs r1, #1                       
  2146c:  ldrb r5, [r0, r1]                 
  2146e:  adds r1, r1, #1                   
  21470:  adds r2, r5, r2                   
  21472:  uxtb r1, r1                       
  21474:  uxtb r2, r2                       
  21476:  cmp r1, #0xe                      
  21478:  blo #0x2146c                      
  2147a:  strb r2, [r0, #0xe]               
  2147c:  movs r1, #0x9e                    
  2147e:  strb r1, [r0, #0xf]               
  21480:  ldr r0, [sp, #0x40]               
  21482:  strb r0, [r3]                     
  21484:  cmp r0, #8                        
  21486:  blo #0x2148a                      
  21488:  strb r4, [r3]                     
  2148a:  ldr r0, [pc, #0x154]              -> RAM
  2148c:  ldr r2, [sp, #0x2c]               
  2148e:  ldr r1, [sp, #0x30]               
  21490:  str r2, [r0, #0x54]               
  21492:  str r1, [r0, #0x50]               
  21494:  ldr r2, [sp, #0x30]               
  21496:  ldr r1, [sp, #0x2c]               
  21498:  str r2, [r0, #0x58]               
  2149a:  str r1, [r0, #0x5c]               
  2149c:  movs r1, #1                       
  2149e:  strb r1, [r0, #0x1a]              
  214a0:  add sp, #0x7c                     
  214a2:  pop {r4, r5, r6, r7, pc}          
  214a4:  movs r1, #2                       
  214a6:  b #0x21456                        -> 0x21456 (вне списка функций)
  214a8:  mov r1, r6                        
  214aa:  ldr r6, [pc, #0x134]              -> RAM
  214ac:  ldr r3, [sp, #0x30]               
  214ae:  ldr r4, [r6, #0x50]               
  214b0:  ldr r5, [r6, #0x54]               
  214b2:  subs r4, r3, r4                   
  214b4:  sbcs r1, r5                       
  214b6:  movs r5, #0x19                    
  214b8:  lsls r5, r5, #7                   
  214ba:  movs r3, #0                       
  214bc:  subs r4, r5, r4                   
  214be:  sbcs r3, r1                       
  214c0:  bhs #0x21532                      
  214c2:  ldr r1, [pc, #0x184]              -> RAM
  214c4:  ldr r4, [sp, #0x54]               
  214c6:  movs r5, #0xe                     
  214c8:  strb r5, [r1, r4]                 
  214ca:  movs r1, #0x61                    
  214cc:  strb r1, [r0, #1]                 
  214ce:  movs r1, #0x31                    
  214d0:  strb r1, [r0, #2]                 
  214d2:  movs r1, #9                       
  214d4:  strb r1, [r0, #3]                 
  214d6:  ldr r1, [pc, #0x174]              -> RAM
  214d8:  ldr r3, [pc, #0x158]              -> RAM
  214da:  ldrb r1, [r1]                     
  214dc:  strb r1, [r0, #4]                 
  214de:  ldr r1, [pc, #0x170]              -> RAM
  214e0:  ldrb r1, [r1]                     
  214e2:  strb r1, [r0, #5]                 
  214e4:  ldr r1, [pc, #0x16c]              -> RAM
  214e6:  ldrh r1, [r1]                     
  214e8:  lsrs r4, r1, #8                   
  214ea:  strb r4, [r0, #6]                 
  214ec:  strb r1, [r0, #7]                 
  214ee:  ldr r1, [pc, #0x168]              -> RAM
  214f0:  ldrh r1, [r1]                     
  214f2:  lsrs r4, r1, #8                   
  214f4:  strb r4, [r0, #8]                 
  214f6:  strb r1, [r0, #9]                 
  214f8:  ldr r1, [pc, #0x160]              -> RAM
  214fa:  ldrb r1, [r1]                     
  214fc:  strb r1, [r0, #0xa]               
  214fe:  ldr r1, [pc, #0x160]              -> RAM
  21500:  ldrh r1, [r1]                     
  21502:  lsrs r4, r1, #8                   
  21504:  strb r4, [r0, #0xb]               
  21506:  strb r1, [r0, #0xc]               
  21508:  movs r1, #1                       
  2150a:  ldrb r4, [r0, r1]                 
  2150c:  adds r1, r1, #1                   
  2150e:  adds r2, r4, r2                   
  21510:  uxtb r1, r1                       
  21512:  uxtb r2, r2                       
  21514:  cmp r1, #0xd                      
  21516:  blo #0x2150a                      
  21518:  strb r2, [r0, #0xd]               
  2151a:  movs r1, #0x9e                    
  2151c:  strb r1, [r0, #0xe]               
  2151e:  ldr r0, [sp, #0x40]               
  21520:  strb r0, [r3]                     
  21522:  cmp r0, #8                        
  21524:  blo #0x2152a                      
  21526:  movs r0, #0                       
  21528:  strb r0, [r3]                     
  2152a:  ldr r1, [sp, #0x2c]               
  2152c:  ldr r0, [sp, #0x30]               
  2152e:  str r1, [r6, #0x54]               
  21530:  str r0, [r6, #0x50]               
  21532:  movs r0, #2                       
  21534:  strb r0, [r6, #0x1a]              
  21536:  b #0x214a0                        -> 0x214a0 (вне списка функций)
  21538:  cmp r3, #1                        
  2153a:  beq #0x21542                      
  2153c:  ldr r5, [sp, #0x78]               
  2153e:  cmp r5, #0                        
  21540:  beq #0x21546                      
  21542:  ldr r5, [sp, #0x20]               
  21544:  b #0x21548                        -> 0x21548 (вне списка функций)
  21546:  ldr r5, [sp, #0x1c]               
  21548:  strb r5, [r0, #6]                 
  2154a:  mov r5, ip                        
  2154c:  cmp r5, #0                        
  2154e:  bge #0x21554                      
  21550:  ldr r5, [sp, #0x18]               
  21552:  b #0x21556                        -> 0x21556 (вне списка функций)
  21554:  ldr r5, [sp, #0x14]               
  21556:  strb r5, [r0, #7]                 
  21558:  ldr r5, [sp, #0x58]               
  2155a:  cmp r5, #0                        
  2155c:  bge #0x21562                      
  2155e:  ldr r5, [sp, #0x10]               
  21560:  b #0x21564                        -> 0x21564 (вне списка функций)
  21562:  ldr r5, [sp, #0xc]                
  21564:  strb r5, [r0, #8]                 
  21566:  ldr r5, [sp, #0x74]               
  21568:  lsls r5, r5, #0x1a                
  2156a:  bpl #0x21570                      
  2156c:  movs r5, #0x10                    
  2156e:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  21570:  ldr r5, [sp, #0x70]               
  21572:  cmp r5, #1                        
  21574:  beq #0x21586                      
  21576:  ldr r5, [sp, #0x6c]               
  21578:  cmp r5, #1                        
  2157a:  beq #0x2158a                      
  2157c:  ldr r5, [sp, #0x68]               
  2157e:  lsls r5, r5, #0x1e                
  21580:  bpl #0x2158e                      
  21582:  movs r5, #0x24                    
  21584:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  21586:  movs r5, #0x11                    
  21588:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  2158a:  movs r5, #0x18                    
  2158c:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  2158e:  ldr r5, [sp, #0x50]               
  21590:  lsls r5, r5, #0x1f                
  21592:  beq #0x21598                      
  21594:  movs r5, #0x28                    
  21596:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  21598:  ldr r5, [sp, #0x50]               
  2159a:  lsls r5, r5, #0x1e                
  2159c:  bpl #0x215a2                      
  2159e:  movs r5, #0x29                    
  215a0:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  215a2:  movs r6, #0x27                    
  215a4:  mvns r6, r6                       
  215a6:  mov r5, ip                        
  215a8:  cmp ip, r6                        
  215aa:  ble #0x215b0                      
  215ac:  cmp r5, #0x6e                     
  215ae:  ble #0x215b4                      
  215b0:  movs r5, #0x45                    
  215b2:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  215b4:  ldr r5, [sp, #0x64]               
  215b6:  cmp r5, #1                        
  215b8:  beq #0x215d0                      
  215ba:  cmp r3, #1                        
  215bc:  beq #0x215d4                      
  215be:  movs r5, #1                       
  215c0:  strb r5, [r1]                     
  215c2:  ldr r6, [sp, #0x60]               
  215c4:  ldr r5, [pc, #0x5c]               -> RAM
  215c6:  cmp r6, #0                        
  215c8:  beq #0x21664                      
  215ca:  cmp r6, #1                        
  215cc:  bne #0x21690                      
  215ce:  b #0x21686                        -> 0x21686 (вне списка функций)
  215d0:  movs r5, #0x21                    
  215d2:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  215d4:  movs r5, #2                       
  215d6:  b #0x215c0                        -> 0x215c0 (вне списка функций)
  215d8:  lsls r1, r7, #0xc                 
  215da:  movs r0, #0                       
  215dc:  lsls r0, r3, #0xd                 
  215de:  movs r0, #0                       
  215e0:  lsls r0, r6, #5                   
  215e2:  movs r0, #0                       
  215e4:  lsls r0, r0, #0xa                 
  215e6:  movs r0, #0                       
  215e8:  lsls r0, r6, #8                   
  215ea:  movs r0, #0                       
  215ec:  lsls r0, r7, #8                   
  215ee:  movs r0, #0                       
  215f0:  lsls r1, r0, #0xe                 
  215f2:  movs r0, #0                       
  215f4:  lsls r0, r5, #8                   
  215f6:  movs r0, #0                       
  215f8:  lsls r1, r5, #8                   
  215fa:  movs r0, #0                       
  215fc:  lsls r2, r5, #8                   
  215fe:  movs r0, #0                       
  21600:  lsls r5, r5, #8                   
  21602:  movs r0, #0                       
  21604:  lsls r6, r5, #8                   
  21606:  movs r0, #0                       
  21608:  lsls r4, r3, #0xc                 
  2160a:  movs r0, #0                       
  2160c:  lsls r0, r2, #0xa                 
  2160e:  movs r0, #0                       
  21610:  lsls r6, r3, #8                   
  21612:  movs r0, #0                       
  21614:  lsls r5, r0, #9                   
  21616:  movs r0, #0                       
  21618:  lsls r4, r5, #2                   
  2161a:  movs r0, #0                       
  2161c:  lsls r0, r4, #8                   
  2161e:  movs r0, #0                       
  21620:  lsls r1, r4, #0xc                 
  21622:  movs r0, #0                       
  21624:  lsls r4, r6, #0xc                 
  21626:  movs r0, #0                       
  21628:  lsls r6, r6, #0xc                 
  2162a:  movs r0, #0                       
  2162c:  lsls r6, r6, #8                   
  2162e:  movs r0, #0                       
  21630:  lsls r4, r0, #9                   
  21632:  movs r0, #0                       
  21634:  lsls r1, r1, #0xb                 
  21636:  movs r0, #0                       
  21638:  lsls r7, r0, #9                   
  2163a:  movs r0, #0                       
  2163c:  lsls r0, r3, #8                   
  2163e:  movs r0, #0                       
  21640:  lsls r5, r6, #0xc                 
  21642:  movs r0, #0                       
  21644:  lsls r0, r4, #7                   
  21646:  movs r0, #0                       
  21648:  asrs r5, r6, #2                   
  2164a:  movs r0, #0                       
  2164c:  lsls r6, r4, #0xb                 
  2164e:  movs r0, #0                       
  21650:  lsls r6, r0, #0xc                 
  21652:  movs r0, #0                       
  21654:  lsls r0, r1, #0xc                 
  21656:  movs r0, #0                       
  21658:  lsls r2, r1, #0xc                 
  2165a:  movs r0, #0                       
  2165c:  lsls r4, r1, #0xc                 
  2165e:  movs r0, #0                       
  21660:  lsls r6, r1, #0xc                 
  21662:  movs r0, #0                       
  21664:  ldrb r1, [r1]                     
  21666:  ldr r6, [sp, #0x5c]               
  21668:  ldr r7, [pc, #0x6c]               -> RAM
  2166a:  cmp r6, r1                        
  2166c:  beq #0x21682                      
  2166e:  strb r1, [r7]                     
  21670:  cmp r3, #1                        
  21672:  beq #0x2167e                      
  21674:  movs r1, #1                       
  21676:  strb r1, [r0, #9]                 
  21678:  movs r1, #1                       
  2167a:  strb r1, [r5]                     
  2167c:  b #0x21690                        -> 0x21690 (вне списка функций)
  2167e:  movs r1, #2                       
  21680:  b #0x21676                        -> 0x21676 (вне списка функций)
  21682:  strb r1, [r0, #9]                 
  21684:  b #0x21690                        -> 0x21690 (вне списка функций)
  21686:  cmp r3, #1                        
  21688:  beq #0x216d2                      
  2168a:  movs r1, #1                       
  2168c:  strb r1, [r0, #9]                 
  2168e:  strb r4, [r5]                     
  21690:  ldr r1, [sp, #0x48]               
  21692:  strb r1, [r0, #0xa]               
  21694:  ldr r1, [sp, #8]                  
  21696:  strb r1, [r0, #0xb]               
  21698:  strb r4, [r0, #0xc]               
  2169a:  ldr r1, [sp, #0x44]               
  2169c:  ldr r3, [pc, #0x3c]               -> RAM
  2169e:  strb r1, [r0, #0xd]               
  216a0:  movs r1, #1                       
  216a2:  ldrb r5, [r0, r1]                 
  216a4:  adds r1, r1, #1                   
  216a6:  adds r2, r5, r2                   
  216a8:  uxtb r1, r1                       
  216aa:  uxtb r2, r2                       
  216ac:  cmp r1, #0xe                      
  216ae:  blo #0x216a2                      
  216b0:  strb r2, [r0, #0xe]               
  216b2:  movs r1, #0x9e                    
  216b4:  strb r1, [r0, #0xf]               
  216b6:  ldr r0, [sp, #0x40]               
  216b8:  strb r0, [r3]                     
  216ba:  cmp r0, #8                        
  216bc:  blo #0x216c0                      
  216be:  strb r4, [r3]                     
  216c0:  ldr r2, [pc, #0x1c]               -> RAM
  216c2:  ldr r1, [sp, #0x2c]               
  216c4:  ldr r0, [sp, #0x30]               
  216c6:  str r1, [r2, #0x5c]               
  216c8:  str r0, [r2, #0x58]               
  216ca:  ldr r1, [pc, #0x14]               -> RAM
  216cc:  movs r0, #1                       
  216ce:  strb r0, [r1, #0x1a]              
  216d0:  b #0x214a0                        -> 0x214a0 (вне списка функций)
  216d2:  movs r1, #2                       
  216d4:  b #0x2168c                        -> 0x2168c (вне списка функций)
  ; --- literal-пул @0x215d8 (35 слов) ---
  215d8:  .word 0x20000339  ; RAM
  215dc:  .word 0x20000358  ; RAM
  215e0:  .word 0x20000170  ; RAM
  215e4:  .word 0x20000280  ; RAM
  215e8:  .word 0x20000230  ; RAM
  215ec:  .word 0x20000238  ; RAM
  215f0:  .word 0x20000381  ; RAM
  215f4:  .word 0x20000228  ; RAM
  215f8:  .word 0x20000229  ; RAM
  215fc:  .word 0x2000022a  ; RAM
  21600:  .word 0x2000022d  ; RAM
  21604:  .word 0x2000022e  ; RAM
  21608:  .word 0x2000031c  ; RAM
  2160c:  .word 0x20000290  ; RAM
  21610:  .word 0x2000021e  ; RAM
  21614:  .word 0x20000245  ; RAM
  21618:  .word 0x200000ac  ; RAM
  2161c:  .word 0x20000220  ; RAM
  21620:  .word 0x20000321  ; RAM
  21624:  .word 0x20000334  ; RAM
  21628:  .word 0x20000336  ; RAM
  2162c:  .word 0x20000236  ; RAM
  21630:  .word 0x20000244  ; RAM
  21634:  .word 0x200002c9  ; RAM
  21638:  .word 0x20000247  ; RAM
  2163c:  .word 0x20000218  ; RAM
  21640:  .word 0x20000335  ; RAM
  21644:  .word 0x200001e0  ; RAM
  21648:  .word 0x200010b5  ; RAM
  2164c:  .word 0x200002e6  ; RAM
  21650:  .word 0x20000306  ; RAM
  21654:  .word 0x20000308  ; RAM
  21658:  .word 0x2000030a  ; RAM
  2165c:  .word 0x2000030c  ; RAM
  21660:  .word 0x2000030e  ; RAM
  ; --- literal-пул @0x216d8 (3 слов) — ВНЕ границ функции ---
  216d8:  .word 0x20000336  ; RAM
  216dc:  .word 0x200002c9  ; RAM
  216e0:  .word 0x20000170  ; RAM
```
