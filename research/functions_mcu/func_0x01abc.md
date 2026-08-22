# func_0x01abc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001abc) | `0x00001abc` |
| размер кода | 12 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x019f4` (0x000019f4, bl)
- `func_0x01a68` (0x00001a68, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  01abc:  push {r4, lr}                     
  01abe:  bl #0x1a68                        -> func_0x01a68
  01ac2:  bl #0x19f4                        -> func_0x019f4
  01ac6:  pop {r4, pc}                      
```
