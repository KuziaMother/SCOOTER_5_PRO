# func_0x11cac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080011cac) | `0x00011cac` |
| размер кода | 8 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x04c14` (0x00004c14, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  11cac:  push {r4, lr}                     
  11cae:  bl #0x4c14                        -> func_0x04c14
  11cb2:  pop {r4, pc}                      
```
