# func_0x04fac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004fac) | `0x00004fac` |
| размер кода | 8 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x04fb8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01670` (bl @0x000016b6)
- `func_0x03222` (bl @0x00003266)


## Дизассембляция

```asm
  04fac:  push {r4, lr}                     
  04fae:  cbz r3, #0x4fb4                   
  04fb0:  str r0, [r2, #0x10]               
  04fb2:  b #0x4fb8                         -> 0x04fb8 (вне списка функций)
```
