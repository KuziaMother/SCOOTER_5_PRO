# func_0x0d7ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d7ac) | `0x0000d7ac` |
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
  0d7ac:  push {r4, lr}                     
  0d7ae:  ldr r0, [pc, #0x20]               -> RAM
  0d7b0:  ldrh r0, [r0]                     
  0d7b2:  ubfx r0, r0, #0xb, #1             
  0d7b6:  cbz r0, #0xd7ce                   
  0d7b8:  movs r0, #0xb                     
  0d7ba:  bl #0xd46c                        -> func_0x0d46c
  0d7be:  cmp r0, #1                        
  0d7c0:  bne #0xd7ce                       
  0d7c2:  ldr r0, [pc, #0xc]                -> RAM
  0d7c4:  ldr r0, [r0]                      
  0d7c6:  bic r0, r0, #0x800                
  0d7ca:  ldr r1, [pc, #4]                  -> RAM
  0d7cc:  str r0, [r1]                      
  0d7ce:  pop {r4, pc}                      
  ; --- literal-пул @0x0d7d0 (1 слов) — ВНЕ границ функции ---
  0d7d0:  .word 0x2000008c  ; RAM
```
