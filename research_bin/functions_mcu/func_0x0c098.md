# func_0x0c098

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c098) | `0x0000c098` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x04630` (0x00004630, bl)
- `func_0x048f8` (0x000048f8, bl)
- `func_0x05274` (0x00005274, bl)
- `func_0x0c02c` (0x0000c02c, bl)
- `func_0x0d33c` (0x0000d33c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1238c` (bl @0x000123b6)


## Дизассембляция

```asm
  0c098:  push {r4, lr}                     
  0c09a:  bl #0x4630                        -> func_0x04630
  0c09e:  bl #0xd33c                        -> func_0x0d33c
  0c0a2:  bl #0x5274                        -> func_0x05274
  0c0a6:  bl #0x48f8                        -> func_0x048f8
  0c0aa:  bl #0xc02c                        -> func_0x0c02c
  0c0ae:  pop {r4, pc}                      
```
