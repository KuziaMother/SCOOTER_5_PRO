# func_0x0214c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000214c) | `0x0000214c` |
| размер кода | 36 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40005800 — периферия (r0)

## Вызовы (callees)

- `func_0x08f7c` (0x00008f7c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01e52` (bl @0x00001e6a)


## Дизассембляция

```asm
  0214c:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  02150:  mov r8, r0                        
  02152:  mov r5, r1                        
  02154:  mov r6, r2                        
  02156:  mov r7, r3                        
  02158:  ldr r4, [sp, #0x20]               
  0215a:  mov r3, r7                        
  0215c:  mov r2, r6                        
  0215e:  mov r1, r5                        
  02160:  ldr r0, [pc, #0x24]               -> периферия
  02162:  str r4, [sp]                      
  02164:  bl #0x8f7c                        -> func_0x08f7c
  02168:  cbz r0, #0x2170                   
  0216a:  movs r0, #1                       
  0216c:  pop.w {r3, r4, r5, r6, r7, r8, sb, pc}
  ; --- literal-пул @0x02188 (1 слов) — ВНЕ границ функции ---
  02188:  .word 0x40005800  ; периферия
```
