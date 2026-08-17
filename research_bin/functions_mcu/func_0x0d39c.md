# func_0x0d39c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d39c) | `0x0000d39c` |
| размер кода | 202 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f70 — RAM (r0)

## Вызовы (callees)

- `func_0x08a50` (0x00008a50, bl)
- `func_0x0abf0` (0x0000abf0, bl)
- 0x0ad9c (bl, вне списка функций)
- 0x0d3be (b, вне списка функций)
- 0x0d3c2 (b, вне списка функций)
- 0x0d442 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0d6e4` (bl @0x0000d6f2)
- `func_0x0d734` (bl @0x0000d742)
- `func_0x0d75c` (bl @0x0000d76a)
- `func_0x0d784` (bl @0x0000d792)
- `func_0x0d7d4` (bl @0x0000d7e2)
- `func_0x0d850` (bl @0x0000d85e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d3ba..0x0d3be` (4 Б); цели из: 0x0d3b6
- `0x0d3be..0x0d3c2` (4 Б); цели из: 0x0d3aa
- `0x0d3c2..0x0d3ee` (44 Б); цели из: 0x0d3b8
- `0x0d3ee..0x0d3fc` (14 Б); цели из: 0x0d3d8
- `0x0d3fc..0x0d40a` (14 Б); цели из: 0x0d3f0
- `0x0d40a..0x0d418` (14 Б); цели из: 0x0d3fe
- `0x0d418..0x0d426` (14 Б); цели из: 0x0d40c
- `0x0d426..0x0d434` (14 Б); цели из: 0x0d41a
- `0x0d434..0x0d442` (14 Б); цели из: 0x0d428
- `0x0d442..0x0d466` (36 Б); цели из: 0x0d3c6, 0x0d3fa, 0x0d408, 0x0d416…

## Дизассембляция

```asm
  0d39c:  push {r4, r5, r6, r7, lr}         
  0d39e:  sub sp, #0x24                     
  0d3a0:  mov r4, r0                        
  0d3a2:  movs r7, #0                       
  0d3a4:  movs r5, #0                       
  0d3a6:  movs r6, #0                       
  0d3a8:  nop                               
  0d3aa:  b #0xd3be                         -> 0x0d3be (вне списка функций)
  0d3ac:  add r0, sp, #0xc                  
  0d3ae:  bl #0xabf0                        -> func_0x0abf0
  0d3b2:  mov r5, r0                        
  0d3b4:  cmp r5, #1                        
  0d3b6:  bne #0xd3ba                       
  0d3b8:  b #0xd3c2                         -> 0x0d3c2 (вне списка функций)
  0d3ba:  adds r0, r6, #1                   
  0d3bc:  uxtb r6, r0                       
  0d3be:  cmp r6, #3                        
  0d3c0:  blt #0xd3ac                       
  0d3c2:  nop                               
  0d3c4:  cmp r5, #1                        
  0d3c6:  bne #0xd442                       
  0d3c8:  movs r1, #0x16                    
  0d3ca:  add r0, sp, #0xc                  
  0d3cc:  bl #0x8a50                        -> func_0x08a50
  0d3d0:  mov r7, r0                        
  0d3d2:  ldrh.w r0, [sp, #0x22]            
  0d3d6:  cmp r0, r7                        
  0d3d8:  beq #0xd3ee                       
  0d3da:  movs r0, #0                       
  0d3dc:  str r0, [sp, #0xc]                
  0d3de:  str r0, [sp, #0x10]               
  0d3e0:  movs r0, #0x78                    
  0d3e2:  str r0, [sp, #0x14]               
  0d3e4:  movs r0, #0                       
  0d3e6:  str r0, [sp, #0x18]               
  0d3e8:  str r0, [sp, #0x1c]               
  0d3ea:  strh.w r0, [sp, #0x20]            
  0d3ee:  cmp r4, #0xd                      
  0d3f0:  bne #0xd3fc                       
  0d3f2:  ldr r0, [pc, #0x74]               -> RAM
  0d3f4:  ldr.w r0, [r0, #9]                
  0d3f8:  str r0, [sp, #0xc]                
  0d3fa:  b #0xd442                         -> 0x0d442 (вне списка функций)
  0d3fc:  cmp r4, #0xe                      
  0d3fe:  bne #0xd40a                       
  0d400:  ldr r0, [pc, #0x64]               -> RAM
  0d402:  ldr.w r0, [r0, #0xd]              
  0d406:  str r0, [sp, #0x10]               
  0d408:  b #0xd442                         -> 0x0d442 (вне списка функций)
  0d40a:  cmp r4, #0xf                      
  0d40c:  bne #0xd418                       
  0d40e:  ldr r0, [pc, #0x58]               -> RAM
  0d410:  ldr.w r0, [r0, #0x11]             
  0d414:  str r0, [sp, #0x14]               
  0d416:  b #0xd442                         -> 0x0d442 (вне списка функций)
  0d418:  cmp r4, #0x10                     
  0d41a:  bne #0xd426                       
  0d41c:  ldr r0, [pc, #0x48]               -> RAM
  0d41e:  ldr.w r0, [r0, #0x15]             
  0d422:  str r0, [sp, #0x18]               
  0d424:  b #0xd442                         -> 0x0d442 (вне списка функций)
  0d426:  cmp r4, #0x11                     
  0d428:  bne #0xd434                       
  0d42a:  ldr r0, [pc, #0x3c]               -> RAM
  0d42c:  ldr.w r0, [r0, #0x1f]             
  0d430:  str r0, [sp, #0x1c]               
  0d432:  b #0xd442                         -> 0x0d442 (вне списка функций)
  0d434:  cmp r4, #0x12                     
  0d436:  bne #0xd442                       
  0d438:  ldr r0, [pc, #0x2c]               -> RAM
  0d43a:  ldrh.w r0, [r0, #0x23]            
  0d43e:  strh.w r0, [sp, #0x20]            
  0d442:  movs r1, #0x16                    
  0d444:  add r0, sp, #0xc                  
  0d446:  bl #0x8a50                        -> func_0x08a50
  0d44a:  strh.w r0, [sp, #0x22]            
  0d44e:  ldrd r0, r1, [sp, #0x1c]          
  0d452:  strd r0, r1, [sp]                 
  0d456:  add r0, sp, #0xc                  
  0d458:  ldm r0, {r0, r1, r2, r3}          
  0d45a:  bl #0xad9c                        -> 0x0ad9c (вне списка функций)
  0d45e:  mov r5, r0                        
  0d460:  mov r0, r5                        
  0d462:  add sp, #0x24                     
  0d464:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x0d468 (1 слов) — ВНЕ границ функции ---
  0d468:  .word 0x20000f70  ; RAM
```
