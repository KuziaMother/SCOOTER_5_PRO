# func_0x1d330

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001d330) | `0x0001d330` |
| размер кода | 142 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00007ff8 — данные @0x07ff8 (r1)
- 0x20000220 — RAM (r1)
- 0x200003c8 — RAM (r1)
- 0x20001794 — RAM (r0)

## Вызовы (callees)

- 0x1d348 (b, вне списка функций)
- 0x1d3a2 (b, вне списка функций)
- 0x1d3b6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1d350..0x1d360` (16 Б); цели из: 0x1d346
- `0x1d360..0x1d382` (34 Б); цели из: 0x1d35a
- `0x1d382..0x1d3a0` (30 Б); цели из: 0x1d36c
- `0x1d3a0..0x1d3a2` (2 Б); цели из: 0x1d39a
- `0x1d3a2..0x1d3b0` (14 Б); цели из: 0x1d34e, 0x1d376, 0x1d380, 0x1d388…
- `0x1d3b0..0x1d3b6` (6 Б); цели из: 0x1d3aa
- `0x1d3b6..0x1d3be` (8 Б); цели из: 0x1d3ae, 0x1d3b2

## Дизассембляция

```asm
  1d330:  push {r4, r5, r6, r7, lr}         
  1d332:  ldr r0, [pc, #0x8c]               -> RAM
  1d334:  movs r5, #0xc                     
  1d336:  ldr r1, [pc, #0x8c]               -> RAM
  1d338:  ldrsh r5, [r0, r5]                
  1d33a:  movs r6, #0x91                    
  1d33c:  lsls r6, r6, #2                   
  1d33e:  movs r4, #2                       
  1d340:  ldrh r2, [r1]                     
  1d342:  movs r3, #0                       
  1d344:  cmp r5, r6                        
  1d346:  bls #0x1d350                      
  1d348:  orrs r2, r4                       
  1d34a:  strh r2, [r1]                     
  1d34c:  strh r3, [r0, #0xa]               
  1d34e:  b #0x1d3a2                        -> 0x1d3a2 (вне списка функций)
  1d350:  bics r2, r4                       
  1d352:  movs r4, #0xff                    
  1d354:  adds r4, #0x2d                    
  1d356:  strh r2, [r1]                     
  1d358:  cmp r5, r4                        
  1d35a:  bhs #0x1d360                      
  1d35c:  movs r4, #4                       
  1d35e:  b #0x1d348                        -> 0x1d348 (вне списка функций)
  1d360:  ldr r7, [pc, #0x5c]               -> RAM
  1d362:  movs r6, #0xff                    
  1d364:  movs r4, #0xa                     
  1d366:  adds r6, #0x91                    
  1d368:  ldrsh r4, [r7, r4]                
  1d36a:  cmp r5, r6                        
  1d36c:  bhs #0x1d382                      
  1d36e:  subs r4, #0x64                    
  1d370:  sxth r4, r4                       
  1d372:  strh r4, [r0, #0xa]               
  1d374:  cmp r4, #0                        
  1d376:  bgt #0x1d3a2                      
  1d378:  movs r4, #4                       
  1d37a:  strh r3, [r0, #0xa]               
  1d37c:  orrs r2, r4                       
  1d37e:  strh r2, [r1]                     
  1d380:  b #0x1d3a2                        -> 0x1d3a2 (вне списка функций)
  1d382:  movs r6, #0xff                    
  1d384:  adds r6, #0xaf                    
  1d386:  cmp r5, r6                        
  1d388:  bls #0x1d3a2                      
  1d38a:  movs r5, #4                       
  1d38c:  bics r2, r5                       
  1d38e:  strh r2, [r1]                     
  1d390:  movs r1, #0x7d                    
  1d392:  lsls r1, r1, #3                   
  1d394:  adds r2, r4, r1                   
  1d396:  ldr r1, [pc, #0x30]               -> данные @0x07ff8
  1d398:  cmp r2, r1                        
  1d39a:  bge #0x1d3a0                      
  1d39c:  strh r2, [r0, #0xa]               
  1d39e:  b #0x1d3a2                        -> 0x1d3a2 (вне списка функций)
  1d3a0:  strh r1, [r0, #0xa]               
  1d3a2:  movs r2, #0xa                     
  1d3a4:  ldrsh r2, [r0, r2]                
  1d3a6:  ldr r1, [pc, #0x20]               -> данные @0x07ff8
  1d3a8:  cmp r2, r1                        
  1d3aa:  ble #0x1d3b0                      
  1d3ac:  strh r1, [r0, #0xa]               
  1d3ae:  b #0x1d3b6                        -> 0x1d3b6 (вне списка функций)
  1d3b0:  cmp r2, #0                        
  1d3b2:  bge #0x1d3b6                      
  1d3b4:  strh r3, [r0, #0xa]               
  1d3b6:  ldr r1, [pc, #0x14]               -> RAM
  1d3b8:  movs r0, #4                       
  1d3ba:  strb r0, [r1, #0x10]              
  1d3bc:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1d3c0 (4 слов) — ВНЕ границ функции ---
  1d3c0:  .word 0x20001794  ; RAM
  1d3c4:  .word 0x20000220  ; RAM
  1d3c8:  .word 0x00007ff8  ; данные @0x07ff8
  1d3cc:  .word 0x200003c8  ; RAM
```
