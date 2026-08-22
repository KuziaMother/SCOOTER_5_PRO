# func_0x097e2

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800097e2) | `0x000097e2` |
| размер кода | 18 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x097f2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0ae9a` (bl @0x0000b034)
- `func_0x0aece` (bl @0x0000b034)
- `func_0x0af94` (bl @0x0000b034)
- `func_0x0b582` (bl @0x0000b5c4)
- `func_0x0b59c` (bl @0x0000b5c4)
- `func_0x0b618` (bl @0x0000b648)


## Дизассембляция

```asm
  097e2:  cbz r2, #0x97ec                   
  097e4:  ldrh r3, [r0, #4]                 
  097e6:  orrs r3, r1                       
  097e8:  strh r3, [r0, #4]                 
  097ea:  b #0x97f2                         -> 0x097f2 (вне списка функций)
  097ec:  ldrh r3, [r0, #4]                 
  097ee:  bics r3, r1                       
  097f0:  strh r3, [r0, #4]                 
  097f2:  bx lr                             
```
