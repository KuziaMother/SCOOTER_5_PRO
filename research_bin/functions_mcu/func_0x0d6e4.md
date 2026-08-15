# func_0x0d6e4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d6e4) | `0x0000d6e4` |
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
  0d6e4:  push {r4, lr}                     
  0d6e6:  ldr r0, [pc, #0x20]               -> RAM
  0d6e8:  ldrh r0, [r0]                     
  0d6ea:  ubfx r0, r0, #0xe, #1             
  0d6ee:  cbz r0, #0xd706                   
  0d6f0:  movs r0, #0xe                     
  0d6f2:  bl #0xd39c                        -> func_0x0d39c
  0d6f6:  cmp r0, #1                        
  0d6f8:  bne #0xd706                       
  0d6fa:  ldr r0, [pc, #0xc]                -> RAM
  0d6fc:  ldr r0, [r0]                      
  0d6fe:  bic r0, r0, #0x4000               
  0d702:  ldr r1, [pc, #4]                  -> RAM
  0d704:  str r0, [r1]                      
  0d706:  pop {r4, pc}                      
  ; --- literal-пул @0x0d708 (1 слов) — ВНЕ границ функции ---
  0d708:  .word 0x2000008c  ; RAM
```
