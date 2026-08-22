# func_0x0f304

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f304) | `0x0000f304` |
| размер кода | 88 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000080 — RAM (r0)
- 0x20000a30 — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x20000fbb — RAM (r0)

## Вызовы (callees)

- 0x0f35a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11978` (bl @0x00011986)


## Дизассембляция

```asm
  0f304:  ldr r0, [pc, #0x54]               -> RAM
  0f306:  ldrb r0, [r0, #2]                 
  0f308:  ubfx r0, r0, #3, #1               
  0f30c:  cbnz r0, #0xf352                  
  0f30e:  ldr r0, [pc, #0x4c]               -> RAM
  0f310:  ldrb r0, [r0, #1]                 
  0f312:  and r0, r0, #1                    
  0f316:  cbnz r0, #0xf354                  
  0f318:  ldr r0, [pc, #0x44]               -> RAM
  0f31a:  ldrb r0, [r0]                     
  0f31c:  cmp r0, #1                        
  0f31e:  bne #0xf354                       
  0f320:  ldr r0, [pc, #0x40]               -> RAM
  0f322:  ldr r0, [r0, #4]                  
  0f324:  cmp.w r0, #0x3e8                  
  0f328:  blo #0xf354                       
  0f32a:  ldr r0, [pc, #0x3c]               -> RAM
  0f32c:  ldrh r0, [r0]                     
  0f32e:  adds r0, r0, #1                   
  0f330:  ldr r1, [pc, #0x34]               -> RAM
  0f332:  strh r0, [r1]                     
  0f334:  mov r0, r1                        
  0f336:  ldrh r0, [r0]                     
  0f338:  cmp.w r0, #0x12c                  
  0f33c:  blt #0xf35a                       
  0f33e:  ldr r0, [pc, #0x1c]               -> RAM
  0f340:  ldrb r0, [r0, #2]                 
  0f342:  bic r0, r0, #8                    
  0f346:  adds r0, #8                       
  0f348:  ldr r1, [pc, #0x10]               -> RAM
  0f34a:  strb r0, [r1, #2]                 
  0f34c:  movs r0, #0                       
  0f34e:  ldr r1, [pc, #0x18]               -> RAM
  0f350:  strh r0, [r1]                     
  0f352:  b #0xf35a                         -> 0x0f35a (вне списка функций)
  0f354:  movs r0, #0                       
  0f356:  ldr r1, [pc, #0x10]               -> RAM
  0f358:  strh r0, [r1]                     
  0f35a:  bx lr                             
  ; --- literal-пул @0x0f35c (4 слов) — ВНЕ границ функции ---
  0f35c:  .word 0x20000f70  ; RAM
  0f360:  .word 0x20000080  ; RAM
  0f364:  .word 0x20000fbb  ; RAM
  0f368:  .word 0x20000a30  ; RAM
```
