# func_0x0f36c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f36c) | `0x0000f36c` |
| размер кода | 80 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a36 — RAM (r0)
- 0x20000fc7 — RAM (r0)

## Вызовы (callees)

- 0x0f3fe (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11978` (bl @0x00011992)


## Дизассембляция

```asm
  0f36c:  ldr r0, [pc, #0x90]               -> RAM
  0f36e:  ldrb r0, [r0, #9]                 
  0f370:  ubfx r0, r0, #3, #1               
  0f374:  cbnz r0, #0xf3bc                  
  0f376:  ldr r0, [pc, #0x88]               -> RAM
  0f378:  ldrsb.w r0, [r0, #8]              
  0f37c:  cmn.w r0, #0x1e                   
  0f380:  blt #0xf38c                       
  0f382:  ldr r0, [pc, #0x7c]               -> RAM
  0f384:  ldrsb.w r0, [r0, #8]              
  0f388:  cmp r0, #0x64                     
  0f38a:  ble #0xf3b4                       
  0f38c:  ldr r0, [pc, #0x74]               -> RAM
  0f38e:  ldrh r0, [r0]                     
  0f390:  adds r0, r0, #1                   
  0f392:  ldr r1, [pc, #0x70]               -> RAM
  0f394:  strh r0, [r1]                     
  0f396:  mov r0, r1                        
  0f398:  ldrh r0, [r0]                     
  0f39a:  cmp r0, #0x32                     
  0f39c:  blt #0xf3fe                       
  0f39e:  ldr r0, [pc, #0x60]               -> RAM
  0f3a0:  ldrb r0, [r0, #9]                 
  0f3a2:  bic r0, r0, #8                    
  0f3a6:  adds r0, #8                       
  0f3a8:  ldr r1, [pc, #0x54]               -> RAM
  0f3aa:  strb r0, [r1, #9]                 
  0f3ac:  movs r0, #0                       
  0f3ae:  ldr r1, [pc, #0x54]               -> RAM
  0f3b0:  strh r0, [r1]                     
  0f3b2:  b #0xf3fe                         -> 0x0f3fe (вне списка функций)
  0f3b4:  movs r0, #0                       
  0f3b6:  ldr r1, [pc, #0x4c]               -> RAM
  0f3b8:  strh r0, [r1]                     
  0f3ba:  b #0xf3fe                         -> 0x0f3fe (вне списка функций)
  ; --- literal-пул @0x0f400 (2 слов) — ВНЕ границ функции ---
  0f400:  .word 0x20000fc7  ; RAM
  0f404:  .word 0x20000a36  ; RAM
```
