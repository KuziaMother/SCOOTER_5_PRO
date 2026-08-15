# func_0x1e2f8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e2f8) | `0x0001e2f8` |
| размер кода | 164 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x044aa200 — прочее (r1)
- 0x40021000 — периферия (r0)

## Вызовы (callees)

- 0x19a9a (bl, вне списка функций)
- `func_0x22274` (0x00022274, bl)
- `func_0x225f4` (0x000225f4, bl)
- `func_0x22824` (0x00022824, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1e2f8:  push {r4, r5, lr}                 
  1e2fa:  ldr r0, [pc, #0xa0]               -> периферия
  1e2fc:  sub sp, #0x2c                     
  1e2fe:  ldr r1, [r0, #0x3c]               
  1e300:  movs r2, #1                       
  1e302:  lsls r2, r2, #0x13                
  1e304:  orrs r1, r2                       
  1e306:  str r1, [r0, #0x3c]               
  1e308:  ldr r1, [r0, #0x3c]               
  1e30a:  asrs r3, r2, #1                   
  1e30c:  orrs r1, r3                       
  1e30e:  str r1, [r0, #0x3c]               
  1e310:  ldr r1, [r0, #0x3c]               
  1e312:  asrs r4, r2, #2                   
  1e314:  orrs r1, r4                       
  1e316:  str r1, [r0, #0x3c]               
  1e318:  ldr r1, [r0, #0x3c]               
  1e31a:  asrs r5, r2, #3                   
  1e31c:  orrs r1, r5                       
  1e31e:  str r1, [r0, #0x3c]               
  1e320:  ldr r1, [pc, #0x78]               -> периферия
  1e322:  adds r1, #0x40                    
  1e324:  ldr r5, [r1]                      
  1e326:  orrs r5, r2                       
  1e328:  str r5, [r1]                      
  1e32a:  ldr r2, [r1]                      
  1e32c:  orrs r2, r3                       
  1e32e:  str r2, [r1]                      
  1e330:  ldr r2, [r1, #4]                  
  1e332:  asrs r3, r3, #4                   
  1e334:  orrs r2, r3                       
  1e336:  str r2, [r1, #4]                  
  1e338:  ldr r2, [r1]                      
  1e33a:  orrs r2, r4                       
  1e33c:  str r2, [r1]                      
  1e33e:  ldr r2, [r1, #4]                  
  1e340:  asrs r3, r0, #0x13                
  1e342:  orrs r2, r3                       
  1e344:  str r2, [r1, #4]                  
  1e346:  ldr r2, [r1, #4]                  
  1e348:  asrs r3, r0, #0x15                
  1e34a:  orrs r2, r3                       
  1e34c:  str r2, [r1, #4]                  
  1e34e:  ldr r1, [r0, #0x3c]               
  1e350:  lsls r2, r3, #6                   
  1e352:  orrs r1, r2                       
  1e354:  str r1, [r0, #0x3c]               
  1e356:  ldr r1, [r0, #0x3c]               
  1e358:  movs r4, #1                       
  1e35a:  orrs r1, r4                       
  1e35c:  str r1, [r0, #0x3c]               
  1e35e:  movs r1, #0x28                    
  1e360:  mov r0, sp                        
  1e362:  bl #0x19a9a                       -> 0x19a9a (вне списка функций)
  1e366:  movs r0, #0                       
  1e368:  add r2, sp, #0x20                 
  1e36a:  strb r0, [r2]                     
  1e36c:  ldr r1, [pc, #0x30]               
  1e36e:  str r1, [sp, #0x24]               
  1e370:  lsls r1, r4, #0x14                
  1e372:  str r1, [sp, #0x1c]               
  1e374:  movs r1, #7                       
  1e376:  str r1, [sp]                      
  1e378:  movs r1, #2                       
  1e37a:  mov r2, sp                        
  1e37c:  strb r1, [r2, #4]                 
  1e37e:  strh r0, [r2, #6]                 
  1e380:  strh r0, [r2, #8]                 
  1e382:  str r1, [sp, #0xc]                
  1e384:  strb r4, [r2, #0x15]              
  1e386:  mov r0, sp                        
  1e388:  bl #0x22824                       -> func_0x22824
  1e38c:  mov r0, sp                        
  1e38e:  bl #0x225f4                       -> func_0x225f4
  1e392:  mov r0, sp                        
  1e394:  bl #0x22274                       -> func_0x22274
  1e398:  add sp, #0x2c                     
  1e39a:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x1e39c (2 слов) — ВНЕ границ функции ---
  1e39c:  .word 0x40021000  ; периферия
  1e3a0:  .word 0x044aa200
```
