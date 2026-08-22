# func_0x04bc0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004bc0) | `0x00004bc0` |
| размер кода | 36 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000164c — RAM (r0)

## Вызовы (callees)

- `func_0x02d1c` (0x00002d1c, bl)
- `func_0x02d34` (0x00002d34, bl)

## Кто вызывает (callers / xrefs)

- `func_0x09a44` (bl @0x00009a50)
- `func_0x09a44` (bl @0x00009a5a)
- `func_0x09a44` (bl @0x00009a64)
- `func_0x09a44` (bl @0x00009a6e)


## Дизассембляция

```asm
  04bc0:  push.w {r4, r5, r6, r7, r8, lr}   
  04bc4:  mov r4, r0                        
  04bc6:  mov r6, r1                        
  04bc8:  mov r7, r2                        
  04bca:  cmp r4, #6                        
  04bcc:  bge #0x4be0                       
  04bce:  bl #0x2d1c                        -> func_0x02d1c
  04bd2:  ldr r0, [pc, #0x10]               -> RAM
  04bd4:  add.w r5, r0, r4, lsl #4          
  04bd8:  str r6, [r5, #8]                  
  04bda:  str r7, [r5, #0xc]                
  04bdc:  bl #0x2d34                        -> func_0x02d34
  04be0:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x04be4 (1 слов) — ВНЕ границ функции ---
  04be4:  .word 0x2000164c  ; RAM
```
