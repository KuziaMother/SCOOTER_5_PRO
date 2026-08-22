# func_0x0d46c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d46c) | `0x0000d46c` |
| размер кода | 182 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)
- 0x20000fc7 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x0ab0c` (0x0000ab0c, bl)
- 0x0accc (bl, вне списка функций)
- 0x0d48e (b, вне списка функций)
- 0x0d492 (b, вне списка функций)
- 0x0d4fa (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0d70c` (bl @0x0000d71a)
- `func_0x0d7ac` (bl @0x0000d7ba)
- `func_0x0d7fc` (bl @0x0000d80a)
- `func_0x0d824` (bl @0x0000d832)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d48a..0x0d48e` (4 Б); цели из: 0x0d486
- `0x0d48e..0x0d492` (4 Б); цели из: 0x0d47a
- `0x0d492..0x0d4be` (44 Б); цели из: 0x0d488
- `0x0d4be..0x0d4ce` (16 Б); цели из: 0x0d4a8
- `0x0d4ce..0x0d4de` (16 Б); цели из: 0x0d4c0
- `0x0d4de..0x0d4ee` (16 Б); цели из: 0x0d4d0
- `0x0d4ee..0x0d4fa` (12 Б); цели из: 0x0d4e0
- `0x0d4fa..0x0d522` (40 Б); цели из: 0x0d496, 0x0d4cc, 0x0d4dc, 0x0d4ec…

## Дизассембляция

```asm
  0d46c:  push {r4, r5, r6, r7, lr}         
  0d46e:  sub sp, #0x54                     
  0d470:  mov r4, r0                        
  0d472:  movs r7, #0                       
  0d474:  movs r5, #0                       
  0d476:  movs r6, #0                       
  0d478:  nop                               
  0d47a:  b #0xd48e                         -> 0x0d48e (вне списка функций)
  0d47c:  add r0, sp, #0x24                 
  0d47e:  bl #0xab0c                        -> func_0x0ab0c
  0d482:  mov r5, r0                        
  0d484:  cmp r5, #1                        
  0d486:  bne #0xd48a                       
  0d488:  b #0xd492                         -> 0x0d492 (вне списка функций)
  0d48a:  adds r0, r6, #1                   
  0d48c:  uxtb r6, r0                       
  0d48e:  cmp r6, #3                        
  0d490:  blt #0xd47c                       
  0d492:  nop                               
  0d494:  cmp r5, #1                        
  0d496:  bne #0xd4fa                       
  0d498:  movs r1, #7                       
  0d49a:  add r0, sp, #0x48                 
  0d49c:  bl #0x8a50                        -> func_0x08a50
  0d4a0:  mov r7, r0                        
  0d4a2:  ldrh.w r0, [sp, #0x4f]            
  0d4a6:  cmp r0, r7                        
  0d4a8:  beq #0xd4be                       
  0d4aa:  movs r0, #0                       
  0d4ac:  strh.w r0, [sp, #0x48]            
  0d4b0:  movs r1, #0                       
  0d4b2:  add r0, sp, #0x24                 
  0d4b4:  strh r1, [r0, #0x28]              
  0d4b6:  strh r1, [r0, #0x26]              
  0d4b8:  movs r1, #0x19                    
  0d4ba:  strb.w r1, [sp, #0x4e]            
  0d4be:  cmp r4, #9                        
  0d4c0:  bne #0xd4ce                       
  0d4c2:  ldr r0, [pc, #0x60]               -> RAM
  0d4c4:  ldrh.w r0, [r0, #7]               
  0d4c8:  strh.w r0, [sp, #0x48]            
  0d4cc:  b #0xd4fa                         -> 0x0d4fa (вне списка функций)
  0d4ce:  cmp r4, #0xa                      
  0d4d0:  bne #0xd4de                       
  0d4d2:  ldr r0, [pc, #0x54]               -> RAM
  0d4d4:  ldrh.w r1, [r0, #0x15]            
  0d4d8:  add r0, sp, #0x24                 
  0d4da:  strh r1, [r0, #0x26]              
  0d4dc:  b #0xd4fa                         -> 0x0d4fa (вне списка функций)
  0d4de:  cmp r4, #0xb                      
  0d4e0:  bne #0xd4ee                       
  0d4e2:  ldr r0, [pc, #0x48]               -> RAM
  0d4e4:  ldrh.w r1, [r0, #9]               
  0d4e8:  add r0, sp, #0x24                 
  0d4ea:  strh r1, [r0, #0x28]              
  0d4ec:  b #0xd4fa                         -> 0x0d4fa (вне списка функций)
  0d4ee:  cmp r4, #0xc                      
  0d4f0:  bne #0xd4fa                       
  0d4f2:  ldr r0, [pc, #0x3c]               -> RAM
  0d4f4:  ldrb r1, [r0, #5]                 
  0d4f6:  strb.w r1, [sp, #0x4e]            
  0d4fa:  movs r1, #7                       
  0d4fc:  add r0, sp, #0x48                 
  0d4fe:  bl #0x8a50                        -> func_0x08a50
  0d502:  add r1, sp, #0x24                 
  0d504:  strh.w r0, [sp, #0x4f]            
  0d508:  movs r2, #0x20                    
  0d50a:  add r1, sp, #0x34                 
  0d50c:  mov r0, sp                        
  0d50e:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0d512:  add r0, sp, #0x24                 
  0d514:  ldm r0, {r0, r1, r2, r3}          
  0d516:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  0d51a:  mov r5, r0                        
  0d51c:  mov r0, r5                        
  0d51e:  add sp, #0x54                     
  0d520:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x0d524 (4 слов) — ВНЕ границ функции ---
  0d524:  .word 0x20000f70  ; RAM
  0d528:  .word 0x20000f95  ; RAM
  0d52c:  .word 0x20000fbb  ; RAM
  0d530:  .word 0x20000fc7  ; RAM
```
