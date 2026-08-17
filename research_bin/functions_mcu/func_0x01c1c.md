# func_0x01c1c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001c1c) | `0x00001c1c` |
| размер кода | 42 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40005800 — периферия (r0)

## Вызовы (callees)

- `func_0x090a0` (0x000090a0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x05b5a` (bl @0x00005b70)
- `func_0x05fb4` (bl @0x00005fb8)
- `func_0x11c3c` (bl @0x00011c42)


## Дизассембляция

```asm
  01c1c:  push {r2, r3, r4, lr}             
  01c1e:  mov r4, r0                        
  01c20:  movs r0, #0                       
  01c22:  str r0, [sp, #4]                  
  01c24:  uxtb r0, r4                       
  01c26:  strb.w r0, [sp, #4]               
  01c2a:  lsrs r0, r4, #8                   
  01c2c:  strb.w r0, [sp, #5]               
  01c30:  movs r0, #2                       
  01c32:  add r3, sp, #4                    
  01c34:  movs r2, #0x3e                    
  01c36:  movs r1, #8                       
  01c38:  str r0, [sp]                      
  01c3a:  ldr r0, [pc, #0x20]               -> периферия
  01c3c:  bl #0x90a0                        -> func_0x090a0
  01c40:  cbnz r0, #0x1c46                  
  01c42:  movs r0, #0                       
  01c44:  pop {r2, r3, r4, pc}              
  ; --- literal-пул @0x01c5c (1 слов) — ВНЕ границ функции ---
  01c5c:  .word 0x40005800  ; периферия
```
