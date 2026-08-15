# func_0x0d75c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d75c) | `0x0000d75c` |
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
  0d75c:  push {r4, lr}                     
  0d75e:  ldr r0, [pc, #0x20]               -> RAM
  0d760:  ldr r0, [r0]                      
  0d762:  ubfx r0, r0, #0x10, #1            
  0d766:  cbz r0, #0xd77e                   
  0d768:  movs r0, #0x10                    
  0d76a:  bl #0xd39c                        -> func_0x0d39c
  0d76e:  cmp r0, #1                        
  0d770:  bne #0xd77e                       
  0d772:  ldr r0, [pc, #0xc]                -> RAM
  0d774:  ldr r0, [r0]                      
  0d776:  bic r0, r0, #0x10000              
  0d77a:  ldr r1, [pc, #4]                  -> RAM
  0d77c:  str r0, [r1]                      
  0d77e:  pop {r4, pc}                      
  ; --- literal-пул @0x0d780 (1 слов) — ВНЕ границ функции ---
  0d780:  .word 0x2000008c  ; RAM
```
