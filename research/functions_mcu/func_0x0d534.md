# func_0x0d534

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d534) | `0x0000d534` |
| размер кода | 152 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000098 — RAM (r0)
- 0x20000f64 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x08a90` (0x00008a90, bl)
- `func_0x0ab0c` (0x0000ab0c, bl)
- 0x0accc (bl, вне списка функций)
- 0x0d556 (b, вне списка функций)
- 0x0d55a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04508` (bl @0x000045f2)
- `func_0x055c8` (bl @0x000055e8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d552..0x0d556` (4 Б); цели из: 0x0d54e
- `0x0d556..0x0d55a` (4 Б); цели из: 0x0d544
- `0x0d55a..0x0d5cc` (114 Б); цели из: 0x0d550

## Дизассембляция

```asm
  0d534:  push {r4, lr}                     
  0d536:  sub sp, #0x50                     
  0d538:  movs r1, #0x30                    
  0d53a:  add r0, sp, #0x20                 
  0d53c:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0d540:  movs r4, #0                       
  0d542:  nop                               
  0d544:  b #0xd556                         -> 0x0d556 (вне списка функций)
  0d546:  add r0, sp, #0x20                 
  0d548:  bl #0xab0c                        -> func_0x0ab0c
  0d54c:  cmp r0, #1                        
  0d54e:  bne #0xd552                       
  0d550:  b #0xd55a                         -> 0x0d55a (вне списка функций)
  0d552:  adds r0, r4, #1                   
  0d554:  uxtb r4, r0                       
  0d556:  cmp r4, #3                        
  0d558:  blt #0xd546                       
  0d55a:  nop                               
  0d55c:  add r0, sp, #0x18                 
  0d55e:  bl #0x8a90                        -> func_0x08a90
  0d562:  ldr r0, [pc, #0x68]               -> RAM
  0d564:  ldr r1, [sp, #0x18]               
  0d566:  str r1, [r0]                      
  0d568:  ldrh.w r1, [sp, #0x1c]            
  0d56c:  strh r1, [r0, #4]                 
  0d56e:  ldrb.w r1, [sp, #0x1e]            
  0d572:  strb r1, [r0, #6]                 
  0d574:  ldrb r0, [r0, #5]                 
  0d576:  add.w r0, r0, #0x7d0              
  0d57a:  strh.w r0, [sp, #0x38]            
  0d57e:  ldr r0, [pc, #0x4c]               -> RAM
  0d580:  ldrb r1, [r0, #4]                 
  0d582:  add r0, sp, #0x20                 
  0d584:  strb r1, [r0, #0x1a]              
  0d586:  ldr r0, [pc, #0x44]               -> RAM
  0d588:  ldrb r1, [r0, #3]                 
  0d58a:  add r0, sp, #0x20                 
  0d58c:  strb r1, [r0, #0x1b]              
  0d58e:  ldr r0, [pc, #0x3c]               -> RAM
  0d590:  ldrb r1, [r0, #2]                 
  0d592:  add r0, sp, #0x20                 
  0d594:  strb r1, [r0, #0x1c]              
  0d596:  movs r1, #0                       
  0d598:  str.w r1, [sp, #0x3e]             
  0d59c:  movs r1, #0xa                     
  0d59e:  add r0, sp, #0x38                 
  0d5a0:  bl #0x8a50                        -> func_0x08a50
  0d5a4:  add r1, sp, #0x20                 
  0d5a6:  strh r0, [r1, #0x22]              
  0d5a8:  movs r2, #0x20                    
  0d5aa:  add r1, sp, #0x30                 
  0d5ac:  mov r0, sp                        
  0d5ae:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0d5b2:  add r0, sp, #0x20                 
  0d5b4:  ldm r0, {r0, r1, r2, r3}          
  0d5b6:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  0d5ba:  ldr r0, [pc, #0x14]               -> RAM
  0d5bc:  ldr r1, [sp, #0x38]               
  0d5be:  str r1, [r0]                      
  0d5c0:  ldr r1, [sp, #0x3c]               
  0d5c2:  str r1, [r0, #4]                  
  0d5c4:  ldr r1, [sp, #0x40]               
  0d5c6:  str r1, [r0, #8]                  
  0d5c8:  add sp, #0x50                     
  0d5ca:  pop {r4, pc}                      
  ; --- literal-пул @0x0d5cc (2 слов) — ВНЕ границ функции ---
  0d5cc:  .word 0x20000098  ; RAM
  0d5d0:  .word 0x20000f64  ; RAM
```
