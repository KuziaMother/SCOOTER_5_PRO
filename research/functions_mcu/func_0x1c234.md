# func_0x1c234

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001c234) | `0x0001c234` |
| размер кода | 228 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200001e0 — RAM (r2)
- 0x2000021e — RAM (r5)
- 0x20000232 — RAM (r0)
- 0x20000234 — RAM (r0)
- 0x20000260 — RAM (r2)
- 0x20000262 — RAM (r6)
- 0x20000263 — RAM (r7)
- 0x2000027e — RAM (r0)
- 0x2000033a — RAM (r0)
- 0x200003c8 — RAM (r1)

## Вызовы (callees)

- 0x19968 (bl, вне списка функций)
- 0x1c2d6 (b, вне списка функций)
- 0x1c308 (b, вне списка функций)
- 0x1c30c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1c27e..0x1c286` (8 Б); цели из: 0x1c244
- `0x1c286..0x1c2a8` (34 Б); цели из: 0x1c276
- `0x1c2a8..0x1c2d6` (46 Б); цели из: 0x1c290
- `0x1c2d6..0x1c304` (46 Б); цели из: 0x1c27c
- `0x1c304..0x1c30c` (8 Б); цели из: 0x1c2ee
- `0x1c30c..0x1c314` (8 Б); цели из: 0x1c27a, 0x1c284, 0x1c2a6, 0x1c2c4…
- `0x1c314..0x1c318` (4 Б); цели из: 0x1c2dc, 0x1c2e8, 0x1c2f6

## Дизассембляция

```asm
  1c234:  push {r3, r4, r5, r6, r7, lr}     
  1c236:  ldr r0, [pc, #0xe0]               -> RAM
  1c238:  movs r4, #0                       
  1c23a:  ldrb r0, [r0]                     
  1c23c:  ldr r6, [pc, #0xdc]               -> RAM
  1c23e:  ldr r7, [pc, #0xe0]               -> RAM
  1c240:  ldr r5, [pc, #0xe0]               -> RAM
  1c242:  cmp r0, #1                        
  1c244:  beq #0x1c27e                      
  1c246:  ldr r0, [pc, #0xe0]               -> RAM
  1c248:  movs r1, #0x64                    
  1c24a:  ldrb r0, [r0]                     
  1c24c:  lsls r0, r0, #0xf                 
  1c24e:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1c252:  ldr r1, [pc, #0xd8]               -> RAM
  1c254:  movs r2, #0x2d                    
  1c256:  lsls r2, r2, #4                   
  1c258:  str r0, [r1, #0x54]               
  1c25a:  muls r0, r2, r0                   
  1c25c:  lsrs r0, r0, #0x10                
  1c25e:  ldr r2, [pc, #0xd0]               -> RAM
  1c260:  mov ip, r0                        
  1c262:  strh r0, [r2]                     
  1c264:  mov r0, r5                        
  1c266:  ldrh r0, [r0]                     
  1c268:  ldrb r3, [r1, #9]                 
  1c26a:  movs r2, #4                       
  1c26c:  mov r1, r0                        
  1c26e:  bics r0, r2                       
  1c270:  orrs r1, r2                       
  1c272:  mov lr, r0                        
  1c274:  cmp r3, #0                        
  1c276:  beq #0x1c286                      
  1c278:  cmp r3, #1                        
  1c27a:  bne #0x1c30c                      
  1c27c:  b #0x1c2d6                        -> 0x1c2d6 (вне списка функций)
  1c27e:  strb r4, [r6]                     
  1c280:  strb r4, [r7]                     
  1c282:  strh r4, [r5]                     
  1c284:  b #0x1c30c                        -> 0x1c30c (вне списка функций)
  1c286:  ldr r2, [pc, #0xac]               -> RAM
  1c288:  mov r0, ip                        
  1c28a:  ldr r3, [r2]                      
  1c28c:  ldr r2, [r2, #4]                  
  1c28e:  cmp r0, #0                        
  1c290:  beq #0x1c2a8                      
  1c292:  movs r0, #1                       
  1c294:  strb r0, [r6]                     
  1c296:  strb r0, [r7]                     
  1c298:  ldr r0, [pc, #0x90]               -> RAM
  1c29a:  adds r0, #0x80                    
  1c29c:  str r3, [r0, #0x38]               
  1c29e:  str r2, [r0, #0x3c]               
  1c2a0:  strh r1, [r5]                     
  1c2a2:  subs r0, #0x80                    
  1c2a4:  strb r4, [r0, #9]                 
  1c2a6:  b #0x1c30c                        -> 0x1c30c (вне списка функций)
  1c2a8:  strb r4, [r6]                     
  1c2aa:  strb r4, [r7]                     
  1c2ac:  ldr r7, [pc, #0x7c]               -> RAM
  1c2ae:  mov r0, r2                        
  1c2b0:  adds r7, #0x80                    
  1c2b2:  ldr r1, [r7, #0x38]               
  1c2b4:  ldr r4, [r7, #0x3c]               
  1c2b6:  subs r6, r3, r1                   
  1c2b8:  sbcs r0, r4                       
  1c2ba:  movs r4, #0x19                    
  1c2bc:  lsls r4, r4, #6                   
  1c2be:  movs r1, #0                       
  1c2c0:  subs r4, r4, r6                   
  1c2c2:  sbcs r1, r0                       
  1c2c4:  bhs #0x1c30c                      
  1c2c6:  str r3, [r7, #0x38]               
  1c2c8:  mov r0, lr                        
  1c2ca:  str r2, [r7, #0x3c]               
  1c2cc:  strh r0, [r5]                     
  1c2ce:  ldr r1, [pc, #0x5c]               -> RAM
  1c2d0:  movs r0, #1                       
  1c2d2:  strb r0, [r1, #9]                 
  1c2d4:  b #0x1c30c                        -> 0x1c30c (вне списка функций)
  1c2d6:  ldr r0, [pc, #0x60]               -> RAM
  1c2d8:  ldrb r0, [r0]                     
  1c2da:  cmp r0, #1                        
  1c2dc:  beq #0x1c314                      
  1c2de:  ldr r0, [pc, #0x5c]               -> RAM
  1c2e0:  movs r3, #0x7d                    
  1c2e2:  ldrh r2, [r0]                     
  1c2e4:  lsls r3, r3, #8                   
  1c2e6:  cmp r2, r3                        
  1c2e8:  bhi #0x1c314                      
  1c2ea:  mov r0, ip                        
  1c2ec:  cmp r0, #0                        
  1c2ee:  beq #0x1c304                      
  1c2f0:  movs r2, #0xff                    
  1c2f2:  adds r2, #0x87                    
  1c2f4:  cmp ip, r2                        
  1c2f6:  bhs #0x1c314                      
  1c2f8:  mov r0, lr                        
  1c2fa:  strh r0, [r5]                     
  1c2fc:  movs r0, #1                       
  1c2fe:  strb r0, [r6]                     
  1c300:  strb r0, [r7]                     
  1c302:  b #0x1c30c                        -> 0x1c30c (вне списка функций)
  1c304:  mov r0, lr                        
  1c306:  strh r0, [r5]                     
  1c308:  strb r4, [r6]                     
  1c30a:  strb r4, [r7]                     
  1c30c:  ldr r0, [pc, #0x1c]               -> RAM
  1c30e:  movs r1, #3                       
  1c310:  strb r1, [r0, #0x10]              
  1c312:  pop {r3, r4, r5, r6, r7, pc}      
  1c314:  strh r1, [r5]                     
  1c316:  b #0x1c308                        -> 0x1c308 (вне списка функций)
  ; --- literal-пул @0x1c318 (10 слов) — ВНЕ границ функции ---
  1c318:  .word 0x2000033a  ; RAM
  1c31c:  .word 0x20000262  ; RAM
  1c320:  .word 0x20000263  ; RAM
  1c324:  .word 0x2000021e  ; RAM
  1c328:  .word 0x20000234  ; RAM
  1c32c:  .word 0x200003c8  ; RAM
  1c330:  .word 0x20000260  ; RAM
  1c334:  .word 0x200001e0  ; RAM
  1c338:  .word 0x20000232  ; RAM
  1c33c:  .word 0x2000027e  ; RAM
```
