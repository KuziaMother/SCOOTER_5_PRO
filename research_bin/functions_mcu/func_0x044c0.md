# func_0x044c0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800044c0) | `0x000044c0` |
| размер кода | 58 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a73 — RAM (r0)
- 0x20000f95 — RAM (r0)
- 0x20000fc7 — RAM (r0)

## Вызовы (callees)

- 0x044f4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11894` (bl @0x000118e4)


## Дизассембляция

```asm
  044c0:  ldr r0, [pc, #0x38]               -> RAM
  044c2:  ldrb r0, [r0]                     
  044c4:  cbz r0, #0x44f2                   
  044c6:  ldr r0, [pc, #0x38]               -> RAM
  044c8:  ldrh r0, [r0, #6]                 
  044ca:  cmp.w r0, #0x7d0                  
  044ce:  ble #0x44f2                       
  044d0:  ldr r0, [pc, #0x2c]               -> RAM
  044d2:  ldrh r0, [r0, #8]                 
  044d4:  movw r1, #0x1194                  
  044d8:  cmp r0, r1                        
  044da:  bge #0x44f2                       
  044dc:  ldr r0, [pc, #0x24]               -> RAM
  044de:  ldrsb.w r0, [r0, #1]              
  044e2:  cmn.w r0, #0x28                   
  044e6:  ble #0x44f2                       
  044e8:  ldr r0, [pc, #0x18]               -> RAM
  044ea:  ldrsb.w r0, [r0, #2]              
  044ee:  cmp r0, #0x64                     
  044f0:  blt #0x44f6                       
  044f2:  movs r0, #0                       
  044f4:  bx lr                             
  044f6:  movs r0, #1                       
  044f8:  b #0x44f4                         -> 0x044f4 (вне списка функций)
  ; --- literal-пул @0x044fc (3 слов) — ВНЕ границ функции ---
  044fc:  .word 0x20000a73  ; RAM
  04500:  .word 0x20000f95  ; RAM
  04504:  .word 0x20000fc7  ; RAM
```
