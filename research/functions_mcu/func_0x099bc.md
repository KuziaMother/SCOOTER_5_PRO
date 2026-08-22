# func_0x099bc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800099bc) | `0x000099bc` |
| размер кода | 18 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x099ca (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0b4ce` (bl @0x0000b4f2)


## Дизассембляция

```asm
  099bc:  cbz r2, #0x99c4                   
  099be:  orr r1, r1, #1                    
  099c2:  b #0x99ca                         -> 0x099ca (вне списка функций)
  099c4:  movw r3, #0xfffe                  
  099c8:  ands r1, r3                       
  099ca:  strh r1, [r0, #0x10]              
  099cc:  bx lr                             
```
