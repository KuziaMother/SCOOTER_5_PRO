# func_0x0d70c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d70c) | `0x0000d70c` |
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
  0d70c:  push {r4, lr}                     
  0d70e:  ldr r0, [pc, #0x20]               -> RAM
  0d710:  ldrh r0, [r0]                     
  0d712:  ubfx r0, r0, #9, #1               
  0d716:  cbz r0, #0xd72e                   
  0d718:  movs r0, #9                       
  0d71a:  bl #0xd46c                        -> func_0x0d46c
  0d71e:  cmp r0, #1                        
  0d720:  bne #0xd72e                       
  0d722:  ldr r0, [pc, #0xc]                -> RAM
  0d724:  ldr r0, [r0]                      
  0d726:  bic r0, r0, #0x200                
  0d72a:  ldr r1, [pc, #4]                  -> RAM
  0d72c:  str r0, [r1]                      
  0d72e:  pop {r4, pc}                      
  ; --- literal-пул @0x0d730 (1 слов) — ВНЕ границ функции ---
  0d730:  .word 0x2000008c  ; RAM
```
