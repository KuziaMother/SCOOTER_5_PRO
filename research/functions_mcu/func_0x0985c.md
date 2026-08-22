# func_0x0985c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000985c) | `0x0000985c` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x09872 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0b09a` (bl @0x0000b158)
- `func_0x0b0fa` (bl @0x0000b158)
- `func_0x0b13a` (bl @0x0000b158)
- `func_0x0b302` (bl @0x0000b39c)
- `func_0x0b384` (bl @0x0000b39c)
- `func_0x0b476` (bl @0x0000b4a6)
- `func_0x0b4ce` (bl @0x0000b510)
- `func_0x0b53a` (bl @0x0000b55e)
- `func_0x0b582` (bl @0x0000b590)


## Дизассембляция

```asm
  0985c:  cbz r1, #0x9868                   
  0985e:  ldrh r2, [r0]                     
  09860:  orr r2, r2, #0x200                
  09864:  strh r2, [r0]                     
  09866:  b #0x9872                         -> 0x09872 (вне списка функций)
  09868:  ldrh r2, [r0]                     
  0986a:  movw r3, #0xfdff                  
  0986e:  ands r2, r3                       
  09870:  strh r2, [r0]                     
  09872:  bx lr                             
```
