# func_0x0c984

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c984) | `0x0000c984` |
| размер кода | 30 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000098 — RAM (r0)

## Вызовы (callees)

- `func_0x08a90` (0x00008a90, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0c984:  push {r2, r3, r4, lr}             
  0c986:  mov r4, r0                        
  0c988:  mov r0, sp                        
  0c98a:  bl #0x8a90                        -> func_0x08a90
  0c98e:  ldr r0, [pc, #0x14]               -> RAM
  0c990:  ldr r1, [sp]                      
  0c992:  str r1, [r0]                      
  0c994:  ldrh.w r1, [sp, #4]               
  0c998:  strh r1, [r0, #4]                 
  0c99a:  ldrb.w r1, [sp, #6]               
  0c99e:  strb r1, [r0, #6]                 
  0c9a0:  pop {r2, r3, r4, pc}              
  ; --- literal-пул @0x0c9a4 (1 слов) — ВНЕ границ функции ---
  0c9a4:  .word 0x20000098  ; RAM
```
