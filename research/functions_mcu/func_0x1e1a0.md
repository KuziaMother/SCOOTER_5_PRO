# func_0x1e1a0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e1a0) | `0x0001e1a0` |
| размер кода | 200 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000005dc — данные @0x005dc (r0)
- 0x200001d0 — RAM (r2)
- 0x200001d2 — RAM (r2)
- 0x200001d4 — RAM (r7)
- 0x200001d6 — RAM (r5)
- 0x200001d8 — RAM (r2)
- 0x200001da — RAM (r1)
- 0x200001f8 — RAM (r5)
- 0x20000263 — RAM (r2)
- 0x2000026e — RAM (r2)
- 0x20000448 — RAM (r5)
- 0x20001768 — RAM (r2)

## Вызовы (callees)

- 0x199bc (bl, вне списка функций)
- 0x1e254 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1b67c` (bl @0x0001b6d0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1e1be..0x1e21a` (92 Б); цели из: 0x1e1b4
- `0x1e21a..0x1e21e` (4 Б); цели из: 0x1e210
- `0x1e21e..0x1e246` (40 Б); цели из: 0x1e218
- `0x1e246..0x1e254` (14 Б); цели из: 0x1e1f2, 0x1e228, 0x1e232, 0x1e236
- `0x1e254..0x1e260` (12 Б); цели из: 0x1e1dc, 0x1e21c, 0x1e24a
- `0x1e260..0x1e262` (2 Б); цели из: 0x1e25a
- `0x1e262..0x1e268` (6 Б); цели из: 0x1e244

## Дизассембляция

```asm
  1e1a0:  push {r3, r4, r5, r6, r7, lr}     
  1e1a2:  ldr r5, [pc, #0xc4]               -> RAM
  1e1a4:  movs r2, #0                       
  1e1a6:  ldr r0, [r5, #0x68]               
  1e1a8:  ldr r1, [r5, #0x6c]               
  1e1aa:  adds r0, r0, #1                   
  1e1ac:  adcs r1, r2                       
  1e1ae:  str r1, [r5, #0x6c]               
  1e1b0:  str r0, [r5, #0x68]               
  1e1b2:  orrs r0, r1                       
  1e1b4:  bne #0x1e1be                      
  1e1b6:  movs r0, #1                       
  1e1b8:  movs r1, #0                       
  1e1ba:  str r1, [r5, #0x6c]               
  1e1bc:  str r0, [r5, #0x68]               
  1e1be:  ldr r4, [pc, #0xa8]               -> RAM
  1e1c0:  movs r2, #0xa                     
  1e1c2:  subs r4, #0x80                    
  1e1c4:  ldrh r0, [r4, #0x38]              
  1e1c6:  movs r3, #0                       
  1e1c8:  adds r0, r0, #1                   
  1e1ca:  strh r0, [r4, #0x38]              
  1e1cc:  ldr r1, [r5, #0x6c]               
  1e1ce:  ldr r0, [r5, #0x68]               
  1e1d0:  bl #0x199bc                       -> 0x199bc (вне списка функций)
  1e1d4:  movs r1, #0                       
  1e1d6:  mov r0, r2                        
  1e1d8:  mov r5, r3                        
  1e1da:  orrs r2, r3                       
  1e1dc:  bne #0x1e254                      
  1e1de:  ldr r2, [pc, #0x8c]               -> RAM
  1e1e0:  ldr r7, [pc, #0x90]               -> RAM
  1e1e2:  ldrh r3, [r2]                     
  1e1e4:  ldr r2, [pc, #0x88]               -> RAM
  1e1e6:  ldrh r6, [r2]                     
  1e1e8:  subs r6, r3, r6                   
  1e1ea:  sxth r6, r6                       
  1e1ec:  strh r6, [r7]                     
  1e1ee:  strh r3, [r2]                     
  1e1f0:  orrs r0, r5                       
  1e1f2:  bne #0x1e246                      
  1e1f4:  ldr r2, [pc, #0x80]               -> RAM
  1e1f6:  movs r0, #8                       
  1e1f8:  ldrsh r0, [r2, r0]                
  1e1fa:  ldr r2, [pc, #0x80]               -> RAM
  1e1fc:  ldr r5, [pc, #0x80]               -> RAM
  1e1fe:  ldrh r3, [r2]                     
  1e200:  subs r3, r0, r3                   
  1e202:  sxth r3, r3                       
  1e204:  strh r3, [r5]                     
  1e206:  strh r0, [r2]                     
  1e208:  ldr r2, [pc, #0x6c]               -> RAM
  1e20a:  subs r2, #0xc                     
  1e20c:  ldr r2, [r2]                      
  1e20e:  cmp r2, #0                        
  1e210:  beq #0x1e21a                      
  1e212:  ldr r2, [pc, #0x70]               -> RAM
  1e214:  ldrb r2, [r2]                     
  1e216:  cmp r2, #0                        
  1e218:  beq #0x1e21e                      
  1e21a:  strh r1, [r4, #0x36]              
  1e21c:  b #0x1e254                        -> 0x1e254 (вне списка функций)
  1e21e:  ldr r5, [pc, #0x68]               -> RAM
  1e220:  movs r2, #0                       
  1e222:  ldrsh r2, [r5, r2]                
  1e224:  lsls r5, r2, #1                   
  1e226:  cmp r5, r6                        
  1e228:  blt #0x1e246                      
  1e22a:  lsls r5, r2, #1                   
  1e22c:  adds r2, r2, r5                   
  1e22e:  rsbs r2, r2, #0                   
  1e230:  cmp r2, r6                        
  1e232:  bgt #0x1e246                      
  1e234:  cmp r3, #8                        
  1e236:  ble #0x1e246                      
  1e238:  ldrh r2, [r4, #0x36]              
  1e23a:  adds r2, r2, #1                   
  1e23c:  uxth r2, r2                       
  1e23e:  strh r2, [r4, #0x36]              
  1e240:  strh r1, [r4, #0x38]              
  1e242:  cmp r2, #1                        
  1e244:  beq #0x1e262                      
  1e246:  ldrh r0, [r4, #0x36]              
  1e248:  cmp r0, #3                        
  1e24a:  bls #0x1e254                      
  1e24c:  ldr r2, [pc, #0x3c]               -> RAM
  1e24e:  strh r1, [r4, #0x36]              
  1e250:  movs r0, #1                       
  1e252:  strb r0, [r2]                     
  1e254:  ldrh r2, [r4, #0x38]              
  1e256:  ldr r0, [pc, #0x38]               -> данные @0x005dc
  1e258:  cmp r2, r0                        
  1e25a:  bls #0x1e260                      
  1e25c:  strh r0, [r4, #0x38]              
  1e25e:  strh r1, [r4, #0x36]              
  1e260:  pop {r3, r4, r5, r6, r7, pc}      
  1e262:  ldr r1, [pc, #0x30]               -> RAM
  1e264:  strh r0, [r1]                     
  1e266:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1e268 (12 слов) — ВНЕ границ функции ---
  1e268:  .word 0x20000448  ; RAM
  1e26c:  .word 0x2000026e  ; RAM
  1e270:  .word 0x200001d2  ; RAM
  1e274:  .word 0x200001d4  ; RAM
  1e278:  .word 0x20001768  ; RAM
  1e27c:  .word 0x200001d8  ; RAM
  1e280:  .word 0x200001d6  ; RAM
  1e284:  .word 0x20000263  ; RAM
  1e288:  .word 0x200001f8  ; RAM
  1e28c:  .word 0x200001d0  ; RAM
  1e290:  .word 0x000005dc  ; данные @0x005dc
  1e294:  .word 0x200001da  ; RAM
```
