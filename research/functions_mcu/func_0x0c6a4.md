# func_0x0c6a4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c6a4) | `0x0000c6a4` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40021000 — периферия (r2)

## Вызовы (callees)

- 0x0c6bc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01940` (bl @0x0000194e)
- `func_0x01940` (bl @0x00001956)
- `func_0x01940` (bl @0x0000195e)
- `func_0x0310c` (bl @0x0000311a)
- `func_0x0b09a` (bl @0x0000b108)
- `func_0x0b09a` (bl @0x0000b11a)
- `func_0x0b09a` (bl @0x0000b12a)
- `func_0x0b0fa` (bl @0x0000b108)
- `func_0x0b0fa` (bl @0x0000b11a)
- `func_0x0b0fa` (bl @0x0000b12a)
- `func_0x0b302` (bl @0x0000b3f0)
- `func_0x0b302` (bl @0x0000b3f8)
- `func_0x0b302` (bl @0x0000b444)
- `func_0x0b302` (bl @0x0000b44c)
- `func_0x0b384` (bl @0x0000b3f0)
- `func_0x0b384` (bl @0x0000b3f8)
- `func_0x0b384` (bl @0x0000b444)
- `func_0x0b384` (bl @0x0000b44c)
- `func_0x106b8` (bl @0x000106ce)
- `func_0x107ec` (bl @0x000107f8)
- `func_0x107ec` (bl @0x00010802)
- `func_0x163b4` (bl @0x000163c2)
- `func_0x163b4` (bl @0x000163d2)
- `func_0x163b4` (bl @0x000163e2)
- `func_0x163b4` (bl @0x000163f2)
- `func_0x163b4` (bl @0x000163fa)


## Дизассембляция

```asm
  0c6a4:  cbz r1, #0xc6b2                   
  0c6a6:  ldr r2, [pc, #0x18]               -> периферия
  0c6a8:  ldr r2, [r2, #0x18]               
  0c6aa:  orrs r2, r0                       
  0c6ac:  ldr r3, [pc, #0x10]               -> периферия
  0c6ae:  str r2, [r3, #0x18]               
  0c6b0:  b #0xc6bc                         -> 0x0c6bc (вне списка функций)
  0c6b2:  ldr r2, [pc, #0xc]                -> периферия
  0c6b4:  ldr r2, [r2, #0x18]               
  0c6b6:  bics r2, r0                       
  0c6b8:  ldr r3, [pc, #4]                  -> периферия
  0c6ba:  str r2, [r3, #0x18]               
  0c6bc:  bx lr                             
  ; --- literal-пул @0x0c6c0 (1 слов) — ВНЕ границ функции ---
  0c6c0:  .word 0x40021000  ; периферия
```
