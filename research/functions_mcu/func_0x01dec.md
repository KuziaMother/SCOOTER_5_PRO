# func_0x01dec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001dec) | `0x00001dec` |
| размер кода | 8 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x029e8` (0x000029e8, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  01dec:  push {r4, lr}                     
  01dee:  bl #0x29e8                        -> func_0x029e8
  01df2:  pop {r4, pc}                      
```
