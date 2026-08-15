# func_0x0cc08

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cc08) | `0x0000cc08` |
| размер кода | 14 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x4000280c — периферия (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x0cd0c` (bl @0x0000cd5c)


## Дизассембляция

```asm
  0cc08:  ldr r0, [pc, #0xc]                -> периферия
  0cc0a:  ldr r0, [r0]                      
  0cc0c:  bic r0, r0, #0x80                 
  0cc10:  ldr r1, [pc, #4]                  -> периферия
  0cc12:  str r0, [r1]                      
  0cc14:  bx lr                             
  ; --- literal-пул @0x0cc18 (1 слов) — ВНЕ границ функции ---
  0cc18:  .word 0x4000280c  ; периферия
```
