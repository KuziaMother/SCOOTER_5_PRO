# func_0x0e2fc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e2fc) | `0x0000e2fc` |
| размер кода | 104 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019eb4 — flash-mirror @0x19eb4 (r1)
- 0x08019fe6 — flash-mirror @0x19fe6 (r1)

## Вызовы (callees)

- 0x0e326 (b, вне списка функций)
- `func_0x16588` (0x00016588, bl)
- `func_0x17306` (0x00017306, bl)
- `func_0x1736a` (0x0001736a, bl)

## Кто вызывает (callers / xrefs)

- `func_0x069e4` (bl @0x00006b3a)
- `func_0x069e4` (bl @0x00006bd2)


## Дизассембляция

```asm
  0e2fc:  push.w {r4, r5, r6, r7, r8, lr}   
  0e300:  sub sp, #0x20                     
  0e302:  mov r8, r0                        
  0e304:  mov r4, r1                        
  0e306:  mov r6, r2                        
  0e308:  mov r7, r3                        
  0e30a:  add r3, sp, #0x1c                 
  0e30c:  movs r2, #0x1a                    
  0e30e:  ldr r1, [pc, #0x54]               -> flash-mirror @0x19fe6
  0e310:  mov r0, r8                        
  0e312:  bl #0x17306                       -> func_0x17306
  0e316:  str r0, [sp, #0x10]               
  0e318:  ldr r0, [sp, #0x1c]               
  0e31a:  str r0, [sp, #4]                  
  0e31c:  cmp r4, #0                        
  0e31e:  bge #0xe324                       
  0e320:  rsbs r5, r4, #0                   
  0e322:  b #0xe326                         -> 0x0e326 (вне списка функций)
  0e324:  mov r5, r4                        
  0e326:  add r3, sp, #0x1c                 
  0e328:  movs r2, #3                       
  0e32a:  ldr r1, [pc, #0x3c]               -> flash-mirror @0x19eb4
  0e32c:  mov r0, r5                        
  0e32e:  bl #0x1736a                       -> func_0x1736a
  0e332:  str r0, [sp, #0x14]               
  0e334:  ldr r0, [sp, #0x1c]               
  0e336:  str r0, [sp, #8]                  
  0e338:  add r3, sp, #0x1c                 
  0e33a:  movs r2, #4                       
  0e33c:  ldr r1, [pc, #0x24]               -> flash-mirror @0x19fe6
  0e33e:  adds r1, #0x36                    
  0e340:  mov r0, r6                        
  0e342:  bl #0x17306                       -> func_0x17306
  0e346:  str r0, [sp, #0x18]               
  0e348:  ldr r0, [sp, #0x1c]               
  0e34a:  str r0, [sp, #0xc]                
  0e34c:  ldr r3, [pc, #0x18]               -> flash-mirror @0x19eb4
  0e34e:  adds r3, #0x90                    
  0e350:  add.w r2, r3, #0x11e              
  0e354:  add r1, sp, #4                    
  0e356:  add r0, sp, #0x10                 
  0e358:  bl #0x16588                       -> func_0x16588
  0e35c:  strh r0, [r7]                     
  0e35e:  add sp, #0x20                     
  0e360:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x0e364 (2 слов) — ВНЕ границ функции ---
  0e364:  .word 0x08019fe6  ; flash-mirror @0x19fe6
  0e368:  .word 0x08019eb4  ; flash-mirror @0x19eb4
```
