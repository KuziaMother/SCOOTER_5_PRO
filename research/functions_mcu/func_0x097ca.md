# func_0x097ca

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800097ca) | `0x000097ca` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x097e0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0acce` (bl @0x0000ae6c)
- `func_0x0ad9e` (bl @0x0000ae6c)
- `func_0x0ae66` (bl @0x0000ae6c)
- `func_0x0b09a` (bl @0x0000b148)
- `func_0x0b09a` (bl @0x0000b17a)
- `func_0x0b0fa` (bl @0x0000b148)
- `func_0x0b0fa` (bl @0x0000b17a)
- `func_0x0b13a` (bl @0x0000b148)
- `func_0x0b13a` (bl @0x0000b17a)
- `func_0x0b476` (bl @0x0000b49e)
- `func_0x0b4ce` (bl @0x0000b508)
- `func_0x0b53a` (bl @0x0000b556)
- `func_0x0b582` (bl @0x0000b588)
- `func_0x0b582` (bl @0x0000b5b2)
- `func_0x0b59c` (bl @0x0000b5b2)
- `func_0x0b618` (bl @0x0000b636)


## Дизассембляция

```asm
  097ca:  cbz r1, #0x97d6                   
  097cc:  ldrh r2, [r0]                     
  097ce:  orr r2, r2, #0x400                
  097d2:  strh r2, [r0]                     
  097d4:  b #0x97e0                         -> 0x097e0 (вне списка функций)
  097d6:  ldrh r2, [r0]                     
  097d8:  movw r3, #0xfbff                  
  097dc:  ands r2, r3                       
  097de:  strh r2, [r0]                     
  097e0:  bx lr                             
```
