# func_0x0d7fc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d7fc) | `0x0000d7fc` |
| размер кода | 36 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000008c — RAM (r0)

## Вызовы (callees)

- `func_0x0d46c` (0x0000d46c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0d7fc:  push {r4, lr}                     
  0d7fe:  ldr r0, [pc, #0x20]               -> RAM
  0d800:  ldrh r0, [r0]                     
  0d802:  ubfx r0, r0, #0xc, #1             
  0d806:  cbz r0, #0xd81e                   
  0d808:  movs r0, #0xc                     
  0d80a:  bl #0xd46c                        -> func_0x0d46c
  0d80e:  cmp r0, #1                        
  0d810:  bne #0xd81e                       
  0d812:  ldr r0, [pc, #0xc]                -> RAM
  0d814:  ldr r0, [r0]                      
  0d816:  bic r0, r0, #0x1000               
  0d81a:  ldr r1, [pc, #4]                  -> RAM
  0d81c:  str r0, [r1]                      
  0d81e:  pop {r4, pc}                      
  ; --- literal-пул @0x0d820 (1 слов) — ВНЕ границ функции ---
  0d820:  .word 0x2000008c  ; RAM
```
