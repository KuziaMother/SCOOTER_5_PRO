# func_0x1d078

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001d078) | `0x0001d078` |
| размер кода | 610 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0000020a — данные @0x0020a (r1)
- 0x000011f8 — данные @0x011f8 (r2)
- 0x00007ff8 — данные @0x07ff8 (r1)
- 0x0001ffe0 — данные @0x1ffe0 (r3)
- 0x20000100 — RAM (r1)
- 0x20000154 — RAM (r0)
- 0x200001d0 — RAM (r1)
- 0x200001da — RAM (r2)
- 0x20000224 — RAM (r5)
- 0x20000229 — RAM (r2)
- 0x20000236 — RAM (r1)
- 0x20000244 — RAM (r1)
- 0x20000263 — RAM (r1)
- 0x20000320 — RAM (r1)
- 0x20000324 — RAM (r1)
- 0x20000326 — RAM (r0)
- 0x20000333 — RAM (r0)
- 0x20000339 — RAM (r0)
- 0x20000388 — RAM (r1)
- 0x200003c8 — RAM (r0)
- 0x20001768 — RAM (r4)

## Вызовы (callees)

- 0x19994 (bl, вне списка функций)
- 0x1d0e6 (b, вне списка функций)
- 0x1d112 (b, вне списка функций)
- 0x1d18e (b, вне списка функций)
- 0x1d1d2 (b, вне списка функций)
- 0x1d208 (b, вне списка функций)
- 0x1d21e (b, вне списка функций)
- 0x1d26e (b, вне списка функций)
- 0x1d2b2 (b, вне списка функций)
- 0x1d2c2 (b, вне списка функций)
- `func_0x1d874` (0x0001d874, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1d0b6..0x1d0f2` (60 Б); цели из: 0x1d0b2
- `0x1d0f2..0x1d132` (64 Б); цели из: 0x1d0ee
- `0x1d132..0x1d136` (4 Б); цели из: 0x1d0d4
- `0x1d136..0x1d13a` (4 Б); цели из: 0x1d0da
- `0x1d13a..0x1d140` (6 Б); цели из: 0x1d0de
- `0x1d140..0x1d144` (4 Б); цели из: 0x1d0e2
- `0x1d144..0x1d152` (14 Б); цели из: 0x1d0fc
- `0x1d152..0x1d166` (20 Б); цели из: 0x1d14a
- `0x1d166..0x1d190` (42 Б); цели из: 0x1d15c
- `0x1d190..0x1d1a2` (18 Б); цели из: 0x1d186
- `0x1d1a2..0x1d1b2` (16 Б); цели из: 0x1d19a
- `0x1d1b2..0x1d1b6` (4 Б); цели из: 0x1d1ac
- `0x1d1b6..0x1d1be` (8 Б); цели из: 0x1d180
- `0x1d1be..0x1d1d0` (18 Б); цели из: 0x1d16c
- `0x1d1d0..0x1d1d2` (2 Б); цели из: 0x1d1c8
- `0x1d1d2..0x1d1e2` (16 Б); цели из: 0x1d1b4
- `0x1d1e2..0x1d1fa` (24 Б); цели из: 0x1d12a
- `0x1d1fa..0x1d208` (14 Б); цели из: 0x1d1e8
- `0x1d208..0x1d21c` (20 Б); цели из: 0x1d1f8
- `0x1d21c..0x1d21e` (2 Б); цели из: 0x1d11c
- `0x1d21e..0x1d230` (18 Б); цели из: 0x1d21a
- `0x1d230..0x1d232` (2 Б); цели из: 0x1d226
- `0x1d232..0x1d24c` (26 Б); цели из: 0x1d22e
- `0x1d24c..0x1d258` (12 Б); цели из: 0x1d248
- `0x1d258..0x1d264` (12 Б); цели из: 0x1d23e
- `0x1d264..0x1d26e` (10 Б); цели из: 0x1d260
- `0x1d26e..0x1d280` (18 Б); цели из: 0x1d256
- `0x1d280..0x1d282` (2 Б); цели из: 0x1d278
- `0x1d282..0x1d2a4` (34 Б); цели из: 0x1d27e
- `0x1d2a4..0x1d2b2` (14 Б); цели из: 0x1d29e
- `0x1d2b2..0x1d2b4` (2 Б); цели из: 0x1d130
- `0x1d2b4..0x1d2cc` (24 Б); цели из: 0x1d296, 0x1d2b0
- `0x1d2cc..0x1d2da` (14 Б); цели из: 0x1d28a

## Дизассембляция

```asm
  1d078:  push {r3, r4, r5, r6, r7, lr}     
  1d07a:  ldr r0, [pc, #0x260]              -> RAM
  1d07c:  ldr r1, [pc, #0x260]              -> RAM
  1d07e:  ldr r0, [r0, #4]                  
  1d080:  ldrb r1, [r1]                     
  1d082:  bl #0x1d874                       -> func_0x1d874
  1d086:  ldr r4, [pc, #0x25c]              -> RAM
  1d088:  movs r2, #0x10                    
  1d08a:  strh r0, [r4]                     
  1d08c:  ldr r1, [r4, #0xc]                
  1d08e:  ldrsh r2, [r4, r2]                
  1d090:  adds r1, r1, r0                   
  1d092:  subs r1, r1, r2                   
  1d094:  str r1, [r4, #0xc]                
  1d096:  asrs r1, r1, #5                   
  1d098:  sxth r7, r1                       
  1d09a:  strh r7, [r4, #0x10]              
  1d09c:  ldr r1, [r4, #4]                  
  1d09e:  movs r5, #0                       
  1d0a0:  adds r0, r1, r0                   
  1d0a2:  movs r1, #8                       
  1d0a4:  ldrsh r1, [r4, r1]                
  1d0a6:  subs r0, r0, r1                   
  1d0a8:  str r0, [r4, #4]                  
  1d0aa:  asrs r0, r0, #3                   
  1d0ac:  sxth r0, r0                       
  1d0ae:  strh r0, [r4, #8]                 
  1d0b0:  cmp r0, #0                        
  1d0b2:  bge #0x1d0b6                      
  1d0b4:  strh r5, [r4, #8]                 
  1d0b6:  movs r0, #8                       
  1d0b8:  ldrsh r0, [r4, r0]                
  1d0ba:  movs r1, #0x64                    
  1d0bc:  mov r6, r0                        
  1d0be:  muls r0, r1, r0                   
  1d0c0:  movs r1, #0xd0                    
  1d0c2:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1d0c6:  ldr r1, [pc, #0x220]              -> RAM
  1d0c8:  ldr r2, [pc, #0x228]              -> RAM
  1d0ca:  strh r0, [r1]                     
  1d0cc:  ldr r0, [pc, #0x21c]              -> RAM
  1d0ce:  ldrb r1, [r0]                     
  1d0d0:  ldr r0, [pc, #0x21c]              -> RAM
  1d0d2:  cmp r1, #1                        
  1d0d4:  beq #0x1d132                      
  1d0d6:  ldrb r1, [r2]                     
  1d0d8:  cmp r1, #0xb                      
  1d0da:  beq #0x1d136                      
  1d0dc:  cmp r1, #2                        
  1d0de:  beq #0x1d13a                      
  1d0e0:  cmp r1, #3                        
  1d0e2:  beq #0x1d140                      
  1d0e4:  movs r1, #0xd0                    
  1d0e6:  strh r1, [r4, #0x14]              
  1d0e8:  ldrh r0, [r0]                     
  1d0ea:  sxth r1, r1                       
  1d0ec:  cmp r1, r0                        
  1d0ee:  ble #0x1d0f2                      
  1d0f0:  strh r0, [r4, #0x14]              
  1d0f2:  ldr r0, [pc, #0x204]              -> RAM
  1d0f4:  ldr r1, [pc, #0x204]              -> RAM
  1d0f6:  ldrb r3, [r0]                     
  1d0f8:  ldr r0, [pc, #0x204]              -> RAM
  1d0fa:  cmp r3, #1                        
  1d0fc:  beq #0x1d144                      
  1d0fe:  ldrh r3, [r4, #0x14]              
  1d100:  strh r3, [r0, #0x2a]              
  1d102:  ldrb r2, [r2]                     
  1d104:  strb r2, [r1]                     
  1d106:  ldr r1, [pc, #0x1fc]              -> RAM
  1d108:  strh r5, [r0, #0x24]              
  1d10a:  strb r5, [r1]                     
  1d10c:  ldr r1, [pc, #0x1f8]              -> RAM
  1d10e:  strh r5, [r0, #0x26]              
  1d110:  strb r5, [r1]                     
  1d112:  ldrh r1, [r0, #0x28]              
  1d114:  adds r1, r1, #1                   
  1d116:  uxth r1, r1                       
  1d118:  strh r1, [r0, #0x28]              
  1d11a:  cmp r1, #1                        
  1d11c:  bls #0x1d21c                      
  1d11e:  movs r1, #0                       
  1d120:  strh r1, [r0, #0x28]              
  1d122:  ldr r1, [pc, #0x1e8]              -> RAM
  1d124:  ldr r5, [pc, #0x1e8]              -> RAM
  1d126:  ldrb r1, [r1]                     
  1d128:  cmp r1, #0                        
  1d12a:  beq #0x1d1e2                      
  1d12c:  ldr r1, [r5]                      
  1d12e:  lsls r1, r1, #2                   
  1d130:  b #0x1d2b2                        -> 0x1d2b2 (вне списка функций)
  1d132:  ldr r1, [pc, #0x1e0]              -> данные @0x0020a
  1d134:  b #0x1d0e6                        -> 0x1d0e6 (вне списка функций)
  1d136:  movs r1, #0x7d                    
  1d138:  b #0x1d0e6                        -> 0x1d0e6 (вне списка функций)
  1d13a:  ldr r1, [pc, #0x1dc]              -> RAM
  1d13c:  ldrh r1, [r1]                     
  1d13e:  b #0x1d0e6                        -> 0x1d0e6 (вне списка функций)
  1d140:  ldrh r1, [r0]                     
  1d142:  b #0x1d0e6                        -> 0x1d0e6 (вне списка функций)
  1d144:  ldrb r2, [r2]                     
  1d146:  ldrb r3, [r1]                     
  1d148:  cmp r2, r3                        
  1d14a:  beq #0x1d152                      
  1d14c:  ldrh r3, [r4, #0x14]              
  1d14e:  strh r3, [r0, #0x2a]              
  1d150:  strb r2, [r1]                     
  1d152:  ldrb r1, [r4, #0x16]              
  1d154:  adds r1, r1, #1                   
  1d156:  uxtb r1, r1                       
  1d158:  strb r1, [r4, #0x16]              
  1d15a:  cmp r1, #6                        
  1d15c:  bls #0x1d166                      
  1d15e:  strb r5, [r4, #0x16]              
  1d160:  ldrh r1, [r0, #0x2a]              
  1d162:  adds r1, r1, #1                   
  1d164:  strh r1, [r0, #0x2a]              
  1d166:  ldr r1, [pc, #0x1a0]              -> RAM
  1d168:  ldrb r1, [r1]                     
  1d16a:  cmp r1, #0                        
  1d16c:  beq #0x1d1be                      
  1d16e:  ldr r2, [pc, #0x194]              -> RAM
  1d170:  movs r1, #1                       
  1d172:  strb r1, [r2]                     
  1d174:  ldr r3, [pc, #0x16c]              -> RAM
  1d176:  ldr r1, [pc, #0x1a4]              -> RAM
  1d178:  subs r3, #0xc                     
  1d17a:  ldr r2, [r3, #4]                  
  1d17c:  ldr r1, [r1]                      
  1d17e:  cmp r2, r1                        
  1d180:  ble #0x1d1b6                      
  1d182:  ldr r2, [pc, #0x19c]              -> данные @0x011f8
  1d184:  cmp r1, r2                        
  1d186:  ble #0x1d190                      
  1d188:  movs r2, #0x4b                    
  1d18a:  lsls r2, r2, #3                   
  1d18c:  subs r1, r1, r2                   
  1d18e:  str r1, [r3, #4]                  
  1d190:  ldrh r1, [r0, #0x24]              
  1d192:  adds r1, r1, #1                   
  1d194:  sxth r1, r1                       
  1d196:  strh r1, [r0, #0x24]              
  1d198:  cmp r1, #0x50                     
  1d19a:  ble #0x1d1a2                      
  1d19c:  ldr r1, [pc, #0x168]              -> RAM
  1d19e:  strh r5, [r0, #0x24]              
  1d1a0:  strb r5, [r1]                     
  1d1a2:  ldr r2, [pc, #0x180]              -> RAM
  1d1a4:  movs r1, #0                       
  1d1a6:  ldrsh r1, [r2, r1]                
  1d1a8:  strh r1, [r0, #0x2a]              
  1d1aa:  cmp r1, #0x3e                     
  1d1ac:  bge #0x1d1b2                      
  1d1ae:  movs r1, #0x3e                    
  1d1b0:  strh r1, [r0, #0x2a]              
  1d1b2:  strh r5, [r0, #0x26]              
  1d1b4:  b #0x1d1d2                        -> 0x1d1d2 (вне списка функций)
  1d1b6:  movs r1, #0x4b                    
  1d1b8:  lsls r1, r1, #3                   
  1d1ba:  subs r1, r2, r1                   
  1d1bc:  b #0x1d18e                        -> 0x1d18e (вне списка функций)
  1d1be:  ldrh r1, [r0, #0x26]              
  1d1c0:  adds r1, r1, #1                   
  1d1c2:  uxth r1, r1                       
  1d1c4:  strh r1, [r0, #0x26]              
  1d1c6:  cmp r1, #0xfa                     
  1d1c8:  bls #0x1d1d0                      
  1d1ca:  ldr r1, [pc, #0x138]              -> RAM
  1d1cc:  strb r5, [r1]                     
  1d1ce:  strh r5, [r0, #0x26]              
  1d1d0:  strh r5, [r0, #0x24]              
  1d1d2:  movs r1, #0x14                    
  1d1d4:  movs r2, #0x2a                    
  1d1d6:  ldrsh r1, [r4, r1]                
  1d1d8:  ldrsh r2, [r0, r2]                
  1d1da:  cmp r1, r2                        
  1d1dc:  bge #0x1d112                      
  1d1de:  strh r1, [r0, #0x2a]              
  1d1e0:  b #0x1d112                        -> 0x1d112 (вне списка функций)
  1d1e2:  movs r1, #0x2a                    
  1d1e4:  ldrsh r1, [r0, r1]                
  1d1e6:  cmp r7, r1                        
  1d1e8:  bge #0x1d1fa                      
  1d1ea:  subs r2, r1, r6                   
  1d1ec:  sxth r2, r2                       
  1d1ee:  strh r2, [r0, #0x2c]              
  1d1f0:  lsls r3, r2, #2                   
  1d1f2:  adds r2, r2, r3                   
  1d1f4:  ldr r3, [r0, #0x58]               
  1d1f6:  adds r2, r2, r3                   
  1d1f8:  b #0x1d208                        -> 0x1d208 (вне списка функций)
  1d1fa:  subs r2, r6, r1                   
  1d1fc:  sxth r2, r2                       
  1d1fe:  strh r2, [r0, #0x2c]              
  1d200:  lsls r3, r2, #2                   
  1d202:  adds r2, r2, r3                   
  1d204:  ldr r3, [r0, #0x58]               
  1d206:  subs r2, r3, r2                   
  1d208:  str r2, [r0, #0x58]               
  1d20a:  ldr r2, [pc, #0xd8]               -> RAM
  1d20c:  subs r2, #0xc                     
  1d20e:  ldr r3, [r2, #8]                  
  1d210:  ldr r2, [pc, #0x108]              -> RAM
  1d212:  ldr r2, [r2]                      
  1d214:  subs r2, r3, r2                   
  1d216:  asrs r2, r2, #3                   
  1d218:  ldr r3, [r0, #0x58]               
  1d21a:  b #0x1d21e                        -> 0x1d21e (вне списка функций)
  1d21c:  b #0x1d2c2                        -> 0x1d2c2 (вне списка функций)
  1d21e:  subs r2, r3, r2                   
  1d220:  ldr r3, [pc, #0x104]              -> данные @0x1ffe0
  1d222:  str r2, [r0, #0x58]               
  1d224:  cmp r2, r3                        
  1d226:  bgt #0x1d230                      
  1d228:  movs r3, #0x7d                    
  1d22a:  lsls r3, r3, #6                   
  1d22c:  cmp r2, r3                        
  1d22e:  bge #0x1d232                      
  1d230:  str r3, [r0, #0x58]               
  1d232:  ldr r2, [r0, #0x58]               
  1d234:  asrs r3, r2, #2                   
  1d236:  movs r2, #0xff                    
  1d238:  adds r2, #0x2d                    
  1d23a:  str r3, [r0, #0x60]               
  1d23c:  cmp r7, r1                        
  1d23e:  bge #0x1d258                      
  1d240:  subs r1, r1, r6                   
  1d242:  sxth r1, r1                       
  1d244:  strh r1, [r0, #0x2c]              
  1d246:  cmp r1, r2                        
  1d248:  ble #0x1d24c                      
  1d24a:  strh r2, [r0, #0x2c]              
  1d24c:  movs r1, #0x2c                    
  1d24e:  ldrsh r1, [r0, r1]                
  1d250:  lsls r1, r1, #7                   
  1d252:  str r1, [r0, #0x5c]               
  1d254:  adds r1, r1, r3                   
  1d256:  b #0x1d26e                        -> 0x1d26e (вне списка функций)
  1d258:  subs r1, r6, r1                   
  1d25a:  sxth r1, r1                       
  1d25c:  strh r1, [r0, #0x2c]              
  1d25e:  cmp r1, r2                        
  1d260:  ble #0x1d264                      
  1d262:  strh r2, [r0, #0x2c]              
  1d264:  movs r1, #0x2c                    
  1d266:  ldrsh r1, [r0, r1]                
  1d268:  lsls r1, r1, #7                   
  1d26a:  str r1, [r0, #0x5c]               
  1d26c:  subs r1, r3, r1                   
  1d26e:  mov r2, r1                        
  1d270:  str r1, [r0, #0x64]               
  1d272:  movs r1, #0x7d                    
  1d274:  lsls r1, r1, #3                   
  1d276:  cmp r2, r1                        
  1d278:  blt #0x1d280                      
  1d27a:  ldr r1, [pc, #0xb0]               -> данные @0x07ff8
  1d27c:  cmp r2, r1                        
  1d27e:  ble #0x1d282                      
  1d280:  str r1, [r0, #0x64]               
  1d282:  ldr r1, [pc, #0x60]               -> RAM
  1d284:  subs r1, #0xc                     
  1d286:  ldr r1, [r1, #4]                  
  1d288:  cmp r1, #0                        
  1d28a:  beq #0x1d2cc                      
  1d28c:  ldrh r2, [r0, #0x2e]              
  1d28e:  adds r2, r2, #1                   
  1d290:  sxth r2, r2                       
  1d292:  strh r2, [r0, #0x2e]              
  1d294:  cmp r2, #2                        
  1d296:  ble #0x1d2b4                      
  1d298:  movs r2, #2                       
  1d29a:  strh r2, [r0, #0x2e]              
  1d29c:  cmp r1, r3                        
  1d29e:  bge #0x1d2a4                      
  1d2a0:  lsls r1, r1, #2                   
  1d2a2:  str r1, [r0, #0x58]               
  1d2a4:  ldr r1, [r5]                      
  1d2a6:  lsls r2, r1, #3                   
  1d2a8:  subs r1, r2, r1                   
  1d2aa:  ldr r2, [r0, #0x58]               
  1d2ac:  asrs r1, r1, #1                   
  1d2ae:  cmp r1, r2                        
  1d2b0:  ble #0x1d2b4                      
  1d2b2:  str r1, [r0, #0x58]               
  1d2b4:  ldr r1, [pc, #0x2c]               -> RAM
  1d2b6:  ldr r2, [r0, #0x64]               
  1d2b8:  subs r1, #0xc                     
  1d2ba:  ldr r1, [r1, #4]                  
  1d2bc:  cmp r1, r2                        
  1d2be:  bge #0x1d2c2                      
  1d2c0:  str r1, [r0, #0x64]               
  1d2c2:  ldr r1, [r0, #0x64]               
  1d2c4:  str r1, [r4, #0x18]               
  1d2c6:  movs r1, #1                       
  1d2c8:  strb r1, [r0, #0x10]              
  1d2ca:  pop {r3, r4, r5, r6, r7, pc}      
  1d2cc:  ldr r1, [r5]                      
  1d2ce:  lsls r1, r1, #2                   
  1d2d0:  str r1, [r0, #0x58]               
  1d2d2:  movs r1, #0                       
  1d2d4:  str r1, [r0, #0x64]               
  1d2d6:  strh r1, [r0, #0x2e]              
  1d2d8:  b #0x1d2c2                        -> 0x1d2c2 (вне списка функций)
  ; --- literal-пул @0x1d2dc (21 слов) — ВНЕ границ функции ---
  1d2dc:  .word 0x20000154  ; RAM
  1d2e0:  .word 0x20000100  ; RAM
  1d2e4:  .word 0x20001768  ; RAM
  1d2e8:  .word 0x20000236  ; RAM
  1d2ec:  .word 0x20000339  ; RAM
  1d2f0:  .word 0x20000326  ; RAM
  1d2f4:  .word 0x20000229  ; RAM
  1d2f8:  .word 0x20000333  ; RAM
  1d2fc:  .word 0x20000320  ; RAM
  1d300:  .word 0x200003c8  ; RAM
  1d304:  .word 0x20000244  ; RAM
  1d308:  .word 0x200001d0  ; RAM
  1d30c:  .word 0x20000263  ; RAM
  1d310:  .word 0x20000224  ; RAM
  1d314:  .word 0x0000020a  ; данные @0x0020a
  1d318:  .word 0x20000324  ; RAM
  1d31c:  .word 0x20000388  ; RAM
  1d320:  .word 0x000011f8  ; данные @0x011f8
  1d324:  .word 0x200001da  ; RAM
  1d328:  .word 0x0001ffe0  ; данные @0x1ffe0
  1d32c:  .word 0x00007ff8  ; данные @0x07ff8
```
