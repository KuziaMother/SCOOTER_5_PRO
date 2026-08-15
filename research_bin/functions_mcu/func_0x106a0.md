# func_0x106a0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800106a0) | `0x000106a0` |
| размер кода | 24 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x106b6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x106b8` (bl @0x000106be)
- `func_0x10788` (bl @0x000107dc)


## Дизассембляция

```asm
  106a0:  cbz r1, #0x106ac                  
  106a2:  ldrh r2, [r0]                     
  106a4:  orr r2, r2, #0x40                 
  106a8:  strh r2, [r0]                     
  106aa:  b #0x106b6                        -> 0x106b6 (вне списка функций)
  106ac:  ldrh r2, [r0]                     
  106ae:  movw r3, #0xffbf                  
  106b2:  ands r2, r3                       
  106b4:  strh r2, [r0]                     
  106b6:  bx lr                             
```
