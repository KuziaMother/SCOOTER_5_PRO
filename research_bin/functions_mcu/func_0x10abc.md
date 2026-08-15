# func_0x10abc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080010abc) | `0x00010abc` |
| размер кода | 60 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x003d0900 — прочее (r0)
- 0x20000b88 — RAM (r1)
- 0x40021000 — периферия (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x11cb4` (bl @0x00011d62)


## Дизассембляция

```asm
  10abc:  push {r4, r5, r6, lr}             
  10abe:  movs r3, #0                       
  10ac0:  movs r4, #0                       
  10ac2:  movs r6, #0                       
  10ac4:  movs r5, #0                       
  10ac6:  ldr r0, [pc, #0xc4]               -> периферия
  10ac8:  ldr r0, [r0]                      
  10aca:  orr r0, r0, #1                    
  10ace:  ldr r1, [pc, #0xbc]               -> периферия
  10ad0:  str r0, [r1]                      
  10ad2:  nop                               
  10ad4:  ldr r0, [pc, #0xb4]               -> периферия
  10ad6:  ldr r0, [r0]                      
  10ad8:  ubfx r5, r0, #1, #1               
  10adc:  adds r6, r6, #1                   
  10ade:  cbnz r5, #0x10ae6                 
  10ae0:  cmp.w r6, #0x500                  
  10ae4:  bne #0x10ad4                      
  10ae6:  ldr r0, [pc, #0xa4]               -> периферия
  10ae8:  ldr r0, [r0]                      
  10aea:  ubfx r5, r0, #1, #1               
  10aee:  cbnz r5, #0x10af8                 
  10af0:  ldr r0, [pc, #0x9c]               
  10af2:  ldr r1, [pc, #0xa0]               -> RAM
  10af4:  str r0, [r1]                      
  10af6:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x10b8c (3 слов) — ВНЕ границ функции ---
  10b8c:  .word 0x40021000  ; периферия
  10b90:  .word 0x003d0900
  10b94:  .word 0x20000b88  ; RAM
```
