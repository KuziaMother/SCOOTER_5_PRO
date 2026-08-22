# func_0x12fd0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012fd0) | `0x00012fd0` |
| размер кода | 8 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x12b50` (0x00012b50, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  12fd0:  push {r4, lr}                     
  12fd2:  bl #0x12b50                       -> func_0x12b50
  12fd6:  pop {r4, pc}                      
```
