# func_0x05c9c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005c9c) | `0x00005c9c` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019b14 — flash-mirror @0x19b14 (r0)
- 0x40003000 — периферия (r1)

## Вызовы (callees)

- `func_0x0332c` (0x0000332c, bl)
- `func_0x0c20c` (0x0000c20c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x110fc` (bl @0x00011146)


## Дизассембляция

```asm
  05c9c:  push {r4, lr}                     
  05c9e:  movw r0, #0xaaaa                  
  05ca2:  ldr r1, [pc, #0x14]               -> периферия
  05ca4:  str r0, [r1]                      
  05ca6:  movs r1, #2                       
  05ca8:  ldr r0, [pc, #0x10]               -> flash-mirror @0x19b14
  05caa:  bl #0x332c                        -> func_0x0332c
  05cae:  movs r0, #1                       
  05cb0:  bl #0xc20c                        -> func_0x0c20c
  05cb4:  pop {r4, pc}                      
  ; --- literal-пул @0x05cb8 (2 слов) — ВНЕ границ функции ---
  05cb8:  .word 0x40003000  ; периферия
  05cbc:  .word 0x08019b14  ; flash-mirror @0x19b14
```
