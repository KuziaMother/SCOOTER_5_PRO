# func_0x0ced0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ced0) | `0x0000ced0` |
| размер кода | 16 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0310c` (0x0000310c, bl)
- `func_0x03150` (0x00003150, bl)
- `func_0x031dc` (0x000031dc, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03034` (bl @0x0000303e)


## Дизассембляция

```asm
  0ced0:  push {r4, lr}                     
  0ced2:  bl #0x310c                        -> func_0x0310c
  0ced6:  bl #0x3150                        -> func_0x03150
  0ceda:  bl #0x31dc                        -> func_0x031dc
  0cede:  pop {r4, pc}                      
```
