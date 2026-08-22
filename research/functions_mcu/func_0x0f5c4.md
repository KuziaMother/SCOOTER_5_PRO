# func_0x0f5c4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f5c4) | `0x0000f5c4` |
| размер кода | 102 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000044 — RAM (r0)
- 0x20000a3a — RAM (r0)
- 0x20000fc7 — RAM (r0)

## Вызовы (callees)

- 0x0f682 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11978` (bl @0x0001198e)


## Дизассембляция

```asm
  0f5c4:  ldr r0, [pc, #0xbc]               -> RAM
  0f5c6:  ldrb r0, [r0, #6]                 
  0f5c8:  ubfx r0, r0, #6, #1               
  0f5cc:  cbnz r0, #0xf62a                  
  0f5ce:  ldr r0, [pc, #0xb8]               -> RAM
  0f5d0:  ldrsb.w r0, [r0]                  
  0f5d4:  cmn.w r0, #0x1e                   
  0f5d8:  blt #0xf5fa                       
  0f5da:  ldr r0, [pc, #0xac]               -> RAM
  0f5dc:  ldrsb.w r0, [r0]                  
  0f5e0:  cmp r0, #0x64                     
  0f5e2:  bgt #0xf5fa                       
  0f5e4:  ldr r0, [pc, #0xa0]               -> RAM
  0f5e6:  ldrsb.w r0, [r0, #1]              
  0f5ea:  cmn.w r0, #0x1e                   
  0f5ee:  blt #0xf5fa                       
  0f5f0:  ldr r0, [pc, #0x94]               -> RAM
  0f5f2:  ldrsb.w r0, [r0, #1]              
  0f5f6:  cmp r0, #0x64                     
  0f5f8:  ble #0xf622                       
  0f5fa:  ldr r0, [pc, #0x90]               -> RAM
  0f5fc:  ldrh r0, [r0]                     
  0f5fe:  adds r0, r0, #1                   
  0f600:  ldr r1, [pc, #0x88]               -> RAM
  0f602:  strh r0, [r1]                     
  0f604:  mov r0, r1                        
  0f606:  ldrh r0, [r0]                     
  0f608:  cmp r0, #0x32                     
  0f60a:  blt #0xf682                       
  0f60c:  ldr r0, [pc, #0x74]               -> RAM
  0f60e:  ldrb r0, [r0, #6]                 
  0f610:  bic r0, r0, #0x40                 
  0f614:  adds r0, #0x40                    
  0f616:  ldr r1, [pc, #0x6c]               -> RAM
  0f618:  strb r0, [r1, #6]                 
  0f61a:  movs r0, #0                       
  0f61c:  ldr r1, [pc, #0x6c]               -> RAM
  0f61e:  strh r0, [r1]                     
  0f620:  b #0xf682                         -> 0x0f682 (вне списка функций)
  0f622:  movs r0, #0                       
  0f624:  ldr r1, [pc, #0x64]               -> RAM
  0f626:  strh r0, [r1]                     
  0f628:  b #0xf682                         -> 0x0f682 (вне списка функций)
  ; --- literal-пул @0x0f684 (3 слов) — ВНЕ границ функции ---
  0f684:  .word 0x20000fc7  ; RAM
  0f688:  .word 0x20000044  ; RAM
  0f68c:  .word 0x20000a3a  ; RAM
```
