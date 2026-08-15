# func_0x07fd4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007fd4) | `0x00007fd4` |
| размер кода | 6 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x0a8c4` (bl @0x0000a8e8)
- `func_0x0a910` (bl @0x0000a938)


## Дизассембляция

```asm
  07fd4:  mov r1, r0                        
  07fd6:  ldrb r0, [r1]                     
  07fd8:  bx lr                             
```
