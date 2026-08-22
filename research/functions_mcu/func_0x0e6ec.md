# func_0x0e6ec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e6ec) | `0x0000e6ec` |
| размер кода | 18 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001384 — RAM (r0)

## Вызовы (callees)

- `func_0x0f14c` (0x0000f14c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0e6ec:  push {r4, lr}                     
  0e6ee:  ldr r0, [pc, #0x10]               -> RAM
  0e6f0:  ldrb.w r0, [r0, #0x45]            
  0e6f4:  cmp r0, #1                        
  0e6f6:  bne #0xe6fc                       
  0e6f8:  bl #0xf14c                        -> func_0x0f14c
  0e6fc:  pop {r4, pc}                      
  ; --- literal-пул @0x0e700 (1 слов) — ВНЕ границ функции ---
  0e700:  .word 0x20001384  ; RAM
```
