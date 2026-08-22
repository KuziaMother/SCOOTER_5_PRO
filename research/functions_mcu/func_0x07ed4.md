# func_0x07ed4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007ed4) | `0x00007ed4` |
| размер кода | 18 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x061e4` (0x000061e4, bl)
- 0x07ee0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03034` (bl @0x00003058)


## Дизассембляция

```asm
  07ed4:  push {r4, lr}                     
  07ed6:  bl #0x61e4                        -> func_0x061e4
  07eda:  cmp r0, #1                        
  07edc:  bne #0x7ee2                       
  07ede:  movs r0, #0                       
  07ee0:  pop {r4, pc}                      
  07ee2:  movs r0, #1                       
  07ee4:  b #0x7ee0                         -> 0x07ee0 (вне списка функций)
```
