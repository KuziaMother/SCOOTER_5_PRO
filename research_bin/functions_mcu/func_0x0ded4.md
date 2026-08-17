# func_0x0ded4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ded4) | `0x0000ded4` |
| размер кода | 54 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000fe7 — RAM (r3)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x0df10` (bl @0x0000dfa6)


## Дизассембляция

```asm
  0ded4:  push {r0, r1, r2, r3}             
  0ded6:  movs r0, #0                       
  0ded8:  movs r1, #0                       
  0deda:  ldrb.w r1, [sp, #1]               
  0dede:  cmp r1, #3                        
  0dee0:  bne #0xdf06                       
  0dee2:  ldrb.w r2, [sp, #3]               
  0dee6:  lsls r3, r2, #0x18                
  0dee8:  ldrb.w r2, [sp, #4]               
  0deec:  add.w r3, r3, r2, lsl #16         
  0def0:  ldrb.w r2, [sp, #5]               
  0def4:  add.w r3, r3, r2, lsl #8          
  0def8:  ldrb.w r2, [sp, #6]               
  0defc:  add r2, r3                        
  0defe:  ldr r3, [pc, #0xc]                -> RAM
  0df00:  str.w r2, [r3, #2]                
  0df04:  movs r0, #1                       
  0df06:  add sp, #0x10                     
  0df08:  bx lr                             
  ; --- literal-пул @0x0df0c (1 слов) — ВНЕ границ функции ---
  0df0c:  .word 0x20000fe7  ; RAM
```
