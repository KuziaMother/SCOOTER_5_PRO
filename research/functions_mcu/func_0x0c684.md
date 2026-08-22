# func_0x0c684

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c684) | `0x0000c684` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40021000 — периферия (r2)

## Вызовы (callees)

- 0x0c69c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x097f4` (bl @0x00009802)
- `func_0x097f4` (bl @0x0000980c)
- `func_0x097f4` (bl @0x00009816)
- `func_0x097f4` (bl @0x00009820)
- `func_0x0b302` (bl @0x0000b3c8)
- `func_0x0b302` (bl @0x0000b3d2)
- `func_0x0b302` (bl @0x0000b400)
- `func_0x0b302` (bl @0x0000b40a)
- `func_0x0b302` (bl @0x0000b41c)
- `func_0x0b302` (bl @0x0000b426)
- `func_0x0b302` (bl @0x0000b454)
- `func_0x0b302` (bl @0x0000b45e)
- `func_0x0b384` (bl @0x0000b3c8)
- `func_0x0b384` (bl @0x0000b3d2)
- `func_0x0b384` (bl @0x0000b400)
- `func_0x0b384` (bl @0x0000b40a)
- `func_0x0b384` (bl @0x0000b41c)
- `func_0x0b384` (bl @0x0000b426)
- `func_0x0b384` (bl @0x0000b454)
- `func_0x0b384` (bl @0x0000b45e)
- `func_0x1302c` (bl @0x00013054)
- `func_0x1302c` (bl @0x0001305e)
- `func_0x1302c` (bl @0x0001306e)
- `func_0x1302c` (bl @0x00013078)


## Дизассембляция

```asm
  0c684:  cbz r1, #0xc692                   
  0c686:  ldr r2, [pc, #0x18]               -> периферия
  0c688:  ldr r2, [r2, #0x10]               
  0c68a:  orrs r2, r0                       
  0c68c:  ldr r3, [pc, #0x10]               -> периферия
  0c68e:  str r2, [r3, #0x10]               
  0c690:  b #0xc69c                         -> 0x0c69c (вне списка функций)
  0c692:  ldr r2, [pc, #0xc]                -> периферия
  0c694:  ldr r2, [r2, #0x10]               
  0c696:  bics r2, r0                       
  0c698:  ldr r3, [pc, #4]                  -> периферия
  0c69a:  str r2, [r3, #0x10]               
  0c69c:  bx lr                             
  ; --- literal-пул @0x0c6a0 (1 слов) — ВНЕ границ функции ---
  0c6a0:  .word 0x40021000  ; периферия
```
