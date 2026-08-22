# func_0x0d850

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d850) | `0x0000d850` |
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
  0d850:  push {r4, lr}                     
  0d852:  ldr r0, [pc, #0x20]               -> RAM
  0d854:  ldr r0, [r0]                      
  0d856:  ubfx r0, r0, #0x12, #1            
  0d85a:  cbz r0, #0xd872                   
  0d85c:  movs r0, #0x12                    
  0d85e:  bl #0xd39c                        -> func_0x0d39c
  0d862:  cmp r0, #1                        
  0d864:  bne #0xd872                       
  0d866:  ldr r0, [pc, #0xc]                -> RAM
  0d868:  ldr r0, [r0]                      
  0d86a:  bic r0, r0, #0x40000              
  0d86e:  ldr r1, [pc, #4]                  -> RAM
  0d870:  str r0, [r1]                      
  0d872:  pop {r4, pc}                      
  ; --- literal-пул @0x0d874 (1 слов) — ВНЕ границ функции ---
  0d874:  .word 0x2000008c  ; RAM
```
