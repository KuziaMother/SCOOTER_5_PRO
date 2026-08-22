# func_0x0d824

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d824) | `0x0000d824` |
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
  0d824:  push {r4, lr}                     
  0d826:  ldr r0, [pc, #0x20]               -> RAM
  0d828:  ldrh r0, [r0]                     
  0d82a:  ubfx r0, r0, #0xa, #1             
  0d82e:  cbz r0, #0xd846                   
  0d830:  movs r0, #0xa                     
  0d832:  bl #0xd46c                        -> func_0x0d46c
  0d836:  cmp r0, #1                        
  0d838:  bne #0xd846                       
  0d83a:  ldr r0, [pc, #0xc]                -> RAM
  0d83c:  ldr r0, [r0]                      
  0d83e:  bic r0, r0, #0x400                
  0d842:  ldr r1, [pc, #4]                  -> RAM
  0d844:  str r0, [r1]                      
  0d846:  pop {r4, pc}                      
  ; --- literal-пул @0x0d848 (1 слов) — ВНЕ границ функции ---
  0d848:  .word 0x2000008c  ; RAM
```
