# func_0x01df4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001df4) | `0x00001df4` |
| размер кода | 64 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01cf6` (0x00001cf6, bl)
- `func_0x03b2a` (0x00003b2a, bl)
- `func_0x051d8` (0x000051d8, bl)
- `func_0x082b8` (0x000082b8, bl)
- `func_0x09b08` (0x00009b08, bl)
- `func_0x0c368` (0x0000c368, bl)
- `func_0x0c420` (0x0000c420, bl)
- `func_0x0d00c` (0x0000d00c, bl)
- `func_0x0eddc` (0x0000eddc, bl)
- `func_0x0ef78` (0x0000ef78, bl)
- 0x108d8 (bl, вне списка функций)
- `func_0x1330c` (0x0001330c, bl)
- `func_0x139fc` (0x000139fc, bl)
- `func_0x13c5c` (0x00013c5c, bl)
- 0x143b0 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  01df4:  push {r4, lr}                     
  01df6:  bl #0x51d8                        -> func_0x051d8
  01dfa:  bl #0x13c5c                       -> func_0x13c5c
  01dfe:  bl #0x82b8                        -> func_0x082b8
  01e02:  bl #0x1330c                       -> func_0x1330c
  01e06:  bl #0xeddc                        -> func_0x0eddc
  01e0a:  bl #0xc420                        -> func_0x0c420
  01e0e:  bl #0x143b0                       -> 0x143b0 (вне списка функций)
  01e12:  bl #0xd00c                        -> func_0x0d00c
  01e16:  bl #0xc368                        -> func_0x0c368
  01e1a:  bl #0x139fc                       -> func_0x139fc
  01e1e:  bl #0x1cf6                        -> func_0x01cf6
  01e22:  bl #0x3b2a                        -> func_0x03b2a
  01e26:  bl #0x9b08                        -> func_0x09b08
  01e2a:  bl #0xef78                        -> func_0x0ef78
  01e2e:  bl #0x108d8                       -> 0x108d8 (вне списка функций)
  01e32:  pop {r4, pc}                      
```
