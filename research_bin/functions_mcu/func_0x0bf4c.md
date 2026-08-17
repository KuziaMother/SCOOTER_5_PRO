# func_0x0bf4c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000bf4c) | `0x0000bf4c` |
| размер кода | 12 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0d878` (0x0000d878, bl)
- `func_0x0ddc4` (0x0000ddc4, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0bf4c:  push {r4, lr}                     
  0bf4e:  bl #0xd878                        -> func_0x0d878
  0bf52:  bl #0xddc4                        -> func_0x0ddc4
  0bf56:  pop {r4, pc}                      
```
