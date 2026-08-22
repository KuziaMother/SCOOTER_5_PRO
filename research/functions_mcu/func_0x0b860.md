# func_0x0b860

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b860) | `0x0000b860` |
| размер кода | 94 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000efc — RAM (r1)
- 0x40005800 — периферия (r0)

## Вызовы (callees)

- `func_0x09874` (0x00009874, bl)
- 0x0b882 (b, вне списка функций)
- 0x0b884 (b, вне списка функций)
- 0x0b8ac (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0b860:  push {r4, lr}                     
  0b862:  mov r4, r0                        
  0b864:  mov.w r0, #0x10000                
  0b868:  ldr r1, [pc, #0x54]               -> RAM
  0b86a:  str r0, [r1]                      
  0b86c:  b #0xb884                         -> 0x0b884 (вне списка функций)
  0b86e:  ldr r1, [pc, #0x50]               -> RAM
  0b870:  ldr r0, [r1]                      
  0b872:  subs r1, r0, #1                   
  0b874:  ldr r2, [pc, #0x48]               -> RAM
  0b876:  str r1, [r2]                      
  0b878:  cbz r0, #0xb880                   
  0b87a:  ldrb.w r1, [r4, #0x10c]           
  0b87e:  cbnz r1, #0xb884                  
  0b880:  movs r0, #3                       
  0b882:  pop {r4, pc}                      
  0b884:  ldrb.w r0, [r4, #0x10c]           
  0b888:  cmp r0, #3                        
  0b88a:  bne #0xb86e                       
  0b88c:  mov.w r0, #0x10000                
  0b890:  ldr r1, [pc, #0x2c]               -> RAM
  0b892:  str r0, [r1]                      
  0b894:  b #0xb8ac                         -> 0x0b8ac (вне списка функций)
  0b896:  ldr r1, [pc, #0x28]               -> RAM
  0b898:  ldr r0, [r1]                      
  0b89a:  subs r1, r0, #1                   
  0b89c:  ldr r2, [pc, #0x20]               -> RAM
  0b89e:  str r1, [r2]                      
  0b8a0:  cbz r0, #0xb8a8                   
  0b8a2:  ldrb.w r1, [r4, #0x10c]           
  0b8a6:  cbnz r1, #0xb8ac                  
  0b8a8:  movs r0, #3                       
  0b8aa:  b #0xb882                         -> 0x0b882 (вне списка функций)
  0b8ac:  mov.w r1, #0x20000                
  0b8b0:  ldr r0, [pc, #0x10]               -> периферия
  0b8b2:  bl #0x9874                        -> func_0x09874
  0b8b6:  cmp r0, #0                        
  0b8b8:  bne #0xb896                       
  0b8ba:  nop                               
  0b8bc:  b #0xb882                         -> 0x0b882 (вне списка функций)
  ; --- literal-пул @0x0b8c0 (2 слов) — ВНЕ границ функции ---
  0b8c0:  .word 0x20000efc  ; RAM
  0b8c4:  .word 0x40005800  ; периферия
```
