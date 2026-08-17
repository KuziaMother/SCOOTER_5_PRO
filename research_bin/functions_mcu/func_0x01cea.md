# func_0x01cea

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001cea) | `0x00001cea` |
| размер кода | 12 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01fe0` (0x00001fe0, bl)
- `func_0x020d8` (0x000020d8, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  01cea:  push {r4, lr}                     
  01cec:  bl #0x1fe0                        -> func_0x01fe0
  01cf0:  bl #0x20d8                        -> func_0x020d8
  01cf4:  pop {r4, pc}                      
```
