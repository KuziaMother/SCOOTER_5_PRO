# func_0x0c9be

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c9be) | `0x0000c9be` |
| размер кода | 28 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x0c9ce (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0ca3c` (bl @0x0000ca94)
- `func_0x0ca3c` (bl @0x0000ca9e)
- `func_0x0ca3c` (bl @0x0000caa8)
- `func_0x0cd80` (bl @0x0000cdd2)
- `func_0x0cd80` (bl @0x0000cddc)
- `func_0x0cd80` (bl @0x0000cde6)


## Дизассембляция

```asm
  0c9be:  mov r1, r0                        
  0c9c0:  movs r2, #0                       
  0c9c2:  b #0xc9ce                         -> 0x0c9ce (вне списка функций)
  0c9c4:  adds r0, r2, #1                   
  0c9c6:  uxtb r2, r0                       
  0c9c8:  sub.w r0, r1, #0xa                
  0c9cc:  uxtb r1, r0                       
  0c9ce:  cmp r1, #0xa                      
  0c9d0:  bge #0xc9c4                       
  0c9d2:  lsls r0, r2, #0x1c                
  0c9d4:  orr.w r0, r1, r0, lsr #24         
  0c9d8:  bx lr                             
```
