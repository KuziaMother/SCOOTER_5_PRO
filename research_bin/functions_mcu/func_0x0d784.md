# func_0x0d784

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d784) | `0x0000d784` |
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
  0d784:  push {r4, lr}                     
  0d786:  ldr r0, [pc, #0x20]               -> RAM
  0d788:  ldr r0, [r0]                      
  0d78a:  ubfx r0, r0, #0x11, #1            
  0d78e:  cbz r0, #0xd7a6                   
  0d790:  movs r0, #0x11                    
  0d792:  bl #0xd39c                        -> func_0x0d39c
  0d796:  cmp r0, #1                        
  0d798:  bne #0xd7a6                       
  0d79a:  ldr r0, [pc, #0xc]                -> RAM
  0d79c:  ldr r0, [r0]                      
  0d79e:  bic r0, r0, #0x20000              
  0d7a2:  ldr r1, [pc, #4]                  -> RAM
  0d7a4:  str r0, [r1]                      
  0d7a6:  pop {r4, pc}                      
  ; --- literal-пул @0x0d7a8 (1 слов) — ВНЕ границ функции ---
  0d7a8:  .word 0x2000008c  ; RAM
```
