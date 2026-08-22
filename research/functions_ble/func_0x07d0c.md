# func_0x07d0c

| | |
|---|---|
| offset в файле | `0x07d0c` |
| vaddr (база 0x01800000) | `0x01807d0c` |
 | размер кода | 64 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x239987ff — прочее (r2)
- 0xff00e04c — прочее (r5)

## Вызовы (callees)

- 0x0161fdc0 (bl, вне списка функций)
- 0x016213b6 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x07d4c` (bl @0x01807d92)

## Дизассембляция

```asm
  01807d0c:  push {r4, r5, lr}                 
  01807d0e:  mov r5, r1                        
  01807d10:  sub sp, #0x24                     
  01807d12:  mov r4, r2                        
  01807d14:  movs r1, #2                       
  01807d16:  bl #0x161fdc0                     
  01807d1a:  ldrd r3, r1, [r5]                 
  01807d1e:  eor.w r2, r0, r3                  
  01807d22:  eor.w r5, r0, r1                  
  01807d26:  strd r2, r5, [sp]                 
  01807d2a:  ldr r2, [pc, #0x3d4]              
  01807d2c:  ldr r5, [pc, #0x3d4]              
  01807d2e:  eors r2, r0                       
  01807d30:  strd r3, r1, [sp, #8]             
  01807d34:  eors r0, r5                       
  01807d36:  strd r2, r0, [sp, #0x10]          
  01807d3a:  strd r3, r1, [sp, #0x18]          
  01807d3e:  mov r2, r4                        
  01807d40:  add r1, sp, #0x10                 
  01807d42:  mov r0, sp                        
  01807d44:  bl #0x16213b6                     
  01807d48:  add sp, #0x24                     
  01807d4a:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x08100 (2 слов) — ВНЕ границ функции ---
  08100:  .word 0x239987ff
  08104:  .word 0xff00e04c
```
