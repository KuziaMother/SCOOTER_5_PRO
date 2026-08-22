# func_0x0d734

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d734) | `0x0000d734` |
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
  0d734:  push {r4, lr}                     
  0d736:  ldr r0, [pc, #0x20]               -> RAM
  0d738:  ldrh r0, [r0]                     
  0d73a:  ubfx r0, r0, #0xd, #1             
  0d73e:  cbz r0, #0xd756                   
  0d740:  movs r0, #0xd                     
  0d742:  bl #0xd39c                        -> func_0x0d39c
  0d746:  cmp r0, #1                        
  0d748:  bne #0xd756                       
  0d74a:  ldr r0, [pc, #0xc]                -> RAM
  0d74c:  ldr r0, [r0]                      
  0d74e:  bic r0, r0, #0x2000               
  0d752:  ldr r1, [pc, #4]                  -> RAM
  0d754:  str r0, [r1]                      
  0d756:  pop {r4, pc}                      
  ; --- literal-пул @0x0d758 (1 слов) — ВНЕ границ функции ---
  0d758:  .word 0x2000008c  ; RAM
```
