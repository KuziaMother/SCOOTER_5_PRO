# func_0x0d7d4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d7d4) | `0x0000d7d4` |
| размер кода | 36 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000008c — RAM (r0)

## Вызовы (callees)

- `func_0x0d39c` (0x0000d39c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0d7d4:  push {r4, lr}                     
  0d7d6:  ldr r0, [pc, #0x20]               -> RAM
  0d7d8:  ldrh r0, [r0]                     
  0d7da:  ubfx r0, r0, #0xf, #1             
  0d7de:  cbz r0, #0xd7f6                   
  0d7e0:  movs r0, #0xf                     
  0d7e2:  bl #0xd39c                        -> func_0x0d39c
  0d7e6:  cmp r0, #1                        
  0d7e8:  bne #0xd7f6                       
  0d7ea:  ldr r0, [pc, #0xc]                -> RAM
  0d7ec:  ldr r0, [r0]                      
  0d7ee:  bic r0, r0, #0x8000               
  0d7f2:  ldr r1, [pc, #4]                  -> RAM
  0d7f4:  str r0, [r1]                      
  0d7f6:  pop {r4, pc}                      
  ; --- literal-пул @0x0d7f8 (1 слов) — ВНЕ границ функции ---
  0d7f8:  .word 0x2000008c  ; RAM
```
