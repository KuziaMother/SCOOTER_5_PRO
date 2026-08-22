# func_0x0f290

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f290) | `0x0000f290` |
| размер кода | 94 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000080 — RAM (r0)
- 0x20000107 — RAM (r0)
- 0x20000a2e — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x20000fbb — RAM (r0)

## Вызовы (callees)

- 0x0f2ec (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11978` (bl @0x00011982)


## Дизассембляция

```asm
  0f290:  ldr r0, [pc, #0x5c]               -> RAM
  0f292:  ldrb r0, [r0, #2]                 
  0f294:  ubfx r0, r0, #2, #1               
  0f298:  cbnz r0, #0xf2e4                  
  0f29a:  ldr r0, [pc, #0x54]               -> RAM
  0f29c:  ldrb r0, [r0, #1]                 
  0f29e:  ubfx r0, r0, #1, #1               
  0f2a2:  cbnz r0, #0xf2e6                  
  0f2a4:  ldr r0, [pc, #0x4c]               -> RAM
  0f2a6:  ldrb r0, [r0]                     
  0f2a8:  cbnz r0, #0xf2e6                  
  0f2aa:  ldr r0, [pc, #0x4c]               -> RAM
  0f2ac:  ldr r0, [r0, #4]                  
  0f2ae:  cmp.w r0, #0x3e8                  
  0f2b2:  blo #0xf2e6                       
  0f2b4:  ldr r0, [pc, #0x44]               -> RAM
  0f2b6:  ldrb r0, [r0]                     
  0f2b8:  cmp r0, #1                        
  0f2ba:  bne #0xf2e6                       
  0f2bc:  ldr r0, [pc, #0x40]               -> RAM
  0f2be:  ldrh r0, [r0]                     
  0f2c0:  adds r0, r0, #1                   
  0f2c2:  ldr r1, [pc, #0x3c]               -> RAM
  0f2c4:  strh r0, [r1]                     
  0f2c6:  mov r0, r1                        
  0f2c8:  ldrh r0, [r0]                     
  0f2ca:  cmp.w r0, #0x12c                  
  0f2ce:  blt #0xf2ec                       
  0f2d0:  ldr r0, [pc, #0x1c]               -> RAM
  0f2d2:  ldrb r0, [r0, #2]                 
  0f2d4:  bic r0, r0, #4                    
  0f2d8:  adds r0, r0, #4                   
  0f2da:  ldr r1, [pc, #0x14]               -> RAM
  0f2dc:  strb r0, [r1, #2]                 
  0f2de:  movs r0, #0                       
  0f2e0:  ldr r1, [pc, #0x1c]               -> RAM
  0f2e2:  strh r0, [r1]                     
  0f2e4:  b #0xf2ec                         -> 0x0f2ec (вне списка функций)
  0f2e6:  movs r0, #0                       
  0f2e8:  ldr r1, [pc, #0x14]               -> RAM
  0f2ea:  strh r0, [r1]                     
  0f2ec:  bx lr                             
  ; --- literal-пул @0x0f2f0 (5 слов) — ВНЕ границ функции ---
  0f2f0:  .word 0x20000f70  ; RAM
  0f2f4:  .word 0x20000080  ; RAM
  0f2f8:  .word 0x20000fbb  ; RAM
  0f2fc:  .word 0x20000107  ; RAM
  0f300:  .word 0x20000a2e  ; RAM
```
