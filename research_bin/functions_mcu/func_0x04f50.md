# func_0x04f50

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004f50) | `0x00004f50` |
| размер кода | 8 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x12b50` (bl @0x00012b80)
- `func_0x12d90` (bl @0x00012dc0)


## Дизассембляция

```asm
  04f50:  mov r1, r0                        
  04f52:  ldr r0, [r1, #4]                  
  04f54:  uxth r0, r0                       
  04f56:  bx lr                             
```
