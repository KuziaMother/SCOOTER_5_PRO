# func_0x12fd8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012fd8) | `0x00012fd8` |
| размер кода | 8 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x12d90` (0x00012d90, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  12fd8:  push {r4, lr}                     
  12fda:  bl #0x12d90                       -> func_0x12d90
  12fde:  pop {r4, pc}                      
```
