# func_0x087c8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800087c8) | `0x000087c8` |
| размер кода | 18 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x087d8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x042b8` (bl @0x000042c6)
- `func_0x04344` (bl @0x0000437e)
- `func_0x04344` (bl @0x00004416)
- `func_0x04630` (bl @0x000046ac)
- `func_0x05bc4` (bl @0x00005bec)
- `func_0x05bc4` (bl @0x00005c26)
- `func_0x05bc4` (bl @0x00005c62)
- `func_0x081b4` (bl @0x000081bc)
- `func_0x081b4` (bl @0x0000826a)
- `func_0x11de8` (bl @0x00011e20)
- `func_0x11de8` (bl @0x00012108)
- `func_0x11de8` (bl @0x000122be)
- `func_0x173cc` (bl @0x0001742a)
- `func_0x173cc` (bl @0x00017456)
- `func_0x173cc` (bl @0x0001748a)


## Дизассембляция

```asm
  087c8:  mov r2, r0                        
  087ca:  movs r0, #0                       
  087cc:  ldr r3, [r2, #0x10]               
  087ce:  ands r3, r1                       
  087d0:  cbz r3, #0x87d6                   
  087d2:  movs r0, #1                       
  087d4:  b #0x87d8                         -> 0x087d8 (вне списка функций)
  087d6:  movs r0, #0                       
  087d8:  bx lr                             
```
