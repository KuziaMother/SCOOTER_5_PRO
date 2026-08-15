# func_0x05b98

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005b98) | `0x00005b98` |
| размер кода | 30 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40003000 — периферия (r1)
- 0x40010818 — периферия (r1)
- 0x40010c18 — периферия (r1)

## Вызовы (callees)

- `func_0x0c20c` (0x0000c20c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11de8` (bl @0x0001203a)


## Дизассембляция

```asm
  05b98:  push {r4, lr}                     
  05b9a:  movw r0, #0xaaaa                  
  05b9e:  ldr r1, [pc, #0x18]               -> периферия
  05ba0:  str r0, [r1]                      
  05ba2:  asrs r0, r1, #0xf                 
  05ba4:  ldr r1, [pc, #0x14]               -> периферия
  05ba6:  str r0, [r1]                      
  05ba8:  movs r0, #4                       
  05baa:  ldr r1, [pc, #0x14]               -> периферия
  05bac:  str r0, [r1]                      
  05bae:  movs r0, #3                       
  05bb0:  bl #0xc20c                        -> func_0x0c20c
  05bb4:  pop {r4, pc}                      
  ; --- literal-пул @0x05bb8 (3 слов) — ВНЕ границ функции ---
  05bb8:  .word 0x40003000  ; периферия
  05bbc:  .word 0x40010c18  ; периферия
  05bc0:  .word 0x40010818  ; периферия
```
