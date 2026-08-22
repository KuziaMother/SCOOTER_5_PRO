# func_0x087e2

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800087e2) | `0x000087e2` |
| размер кода | 10 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x087ea (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0332c` (bl @0x00003558)
- `func_0x0ae9a` (bl @0x0000af20)
- `func_0x0ae9a` (bl @0x0000af2c)
- `func_0x0aece` (bl @0x0000af20)
- `func_0x0aece` (bl @0x0000af2c)
- `func_0x0b302` (bl @0x0000b342)
- `func_0x0b302` (bl @0x0000b35e)
- `func_0x173cc` (bl @0x00017420)
- `func_0x173cc` (bl @0x0001743e)
- `func_0x173cc` (bl @0x00017464)
- `func_0x173cc` (bl @0x000174ac)
- `func_0x173cc` (bl @0x000174c4)
- `func_0x173cc` (bl @0x000174dc)


## Дизассембляция

```asm
  087e2:  cbz r2, #0x87e8                   
  087e4:  str r1, [r0, #0x18]               
  087e6:  b #0x87ea                         -> 0x087ea (вне списка функций)
  087e8:  str r1, [r0, #0x28]               
  087ea:  bx lr                             
```
