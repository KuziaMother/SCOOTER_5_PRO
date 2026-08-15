# func_0x0d5d4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d5d4) | `0x0000d5d4` |
| размер кода | 146 Б |
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
- 0x0d5f6 (b, вне списка функций)
- 0x0d5fa (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04508` (bl @0x000045a4)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d5f2..0x0d5f6` (4 Б); цели из: 0x0d5ee
- `0x0d5f6..0x0d5fa` (4 Б); цели из: 0x0d5e4
- `0x0d5fa..0x0d666` (108 Б); цели из: 0x0d5f0

## Дизассембляция

```asm
  0d5d4:  push {r4, lr}                     
  0d5d6:  sub sp, #0x50                     
  0d5d8:  movs r1, #0x30                    
  0d5da:  add r0, sp, #0x20                 
  0d5dc:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0d5e0:  movs r4, #0                       
  0d5e2:  nop                               
  0d5e4:  b #0xd5f6                         -> 0x0d5f6 (вне списка функций)
  0d5e6:  add r0, sp, #0x20                 
  0d5e8:  bl #0xab0c                        -> func_0x0ab0c
  0d5ec:  cmp r0, #1                        
  0d5ee:  bne #0xd5f2                       
  0d5f0:  b #0xd5fa                         -> 0x0d5fa (вне списка функций)
  0d5f2:  adds r0, r4, #1                   
  0d5f4:  uxtb r4, r0                       
  0d5f6:  cmp r4, #3                        
  0d5f8:  blt #0xd5e6                       
  0d5fa:  nop                               
  0d5fc:  add r0, sp, #0x18                 
  0d5fe:  bl #0x8a90                        -> func_0x08a90
  0d602:  ldr r0, [pc, #0x64]               -> RAM
  0d604:  ldr r1, [sp, #0x18]               
  0d606:  str r1, [r0]                      
  0d608:  ldrh.w r1, [sp, #0x1c]            
  0d60c:  strh r1, [r0, #4]                 
  0d60e:  ldrb.w r1, [sp, #0x1e]            
  0d612:  strb r1, [r0, #6]                 
  0d614:  ldrb r0, [r0, #5]                 
  0d616:  add.w r0, r0, #0x7d0              
  0d61a:  strh.w r0, [sp, #0x38]            
  0d61e:  ldr r0, [pc, #0x48]               -> RAM
  0d620:  ldrb r1, [r0, #4]                 
  0d622:  add r0, sp, #0x20                 
  0d624:  strb r1, [r0, #0x1a]              
  0d626:  ldr r0, [pc, #0x40]               -> RAM
  0d628:  ldrb r1, [r0, #3]                 
  0d62a:  add r0, sp, #0x20                 
  0d62c:  strb r1, [r0, #0x1b]              
  0d62e:  ldr r0, [pc, #0x38]               -> RAM
  0d630:  ldrb r1, [r0, #2]                 
  0d632:  add r0, sp, #0x20                 
  0d634:  strb r1, [r0, #0x1c]              
  0d636:  movs r1, #0xa                     
  0d638:  add r0, sp, #0x38                 
  0d63a:  bl #0x8a50                        -> func_0x08a50
  0d63e:  add r1, sp, #0x20                 
  0d640:  strh r0, [r1, #0x22]              
  0d642:  movs r2, #0x20                    
  0d644:  add r1, sp, #0x30                 
  0d646:  mov r0, sp                        
  0d648:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0d64c:  add r0, sp, #0x20                 
  0d64e:  ldm r0, {r0, r1, r2, r3}          
  0d650:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  0d654:  ldr r0, [pc, #0x14]               -> RAM
  0d656:  ldr r1, [sp, #0x38]               
  0d658:  str r1, [r0]                      
  0d65a:  ldr r1, [sp, #0x3c]               
  0d65c:  str r1, [r0, #4]                  
  0d65e:  ldr r1, [sp, #0x40]               
  0d660:  str r1, [r0, #8]                  
  0d662:  add sp, #0x50                     
  0d664:  pop {r4, pc}                      
  ; --- literal-пул @0x0d668 (2 слов) — ВНЕ границ функции ---
  0d668:  .word 0x20000098  ; RAM
  0d66c:  .word 0x20000f64  ; RAM
```
