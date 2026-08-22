# func_0x04f38

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004f38) | `0x00004f38` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x04f4e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01670` (bl @0x000016be)
- `func_0x02a94` (bl @0x00002b06)
- `func_0x02b2c` (bl @0x00002b96)
- `func_0x03222` (bl @0x000032e8)
- `func_0x0327a` (bl @0x000032e8)
- `func_0x032a0` (bl @0x000032e8)
- `func_0x12b50` (bl @0x00012b78)
- `func_0x12b50` (bl @0x00012c02)
- `func_0x12d90` (bl @0x00012db8)
- `func_0x12d90` (bl @0x00012e42)


## Дизассембляция

```asm
  04f38:  cbz r1, #0x4f44                   
  04f3a:  ldr r2, [r0]                      
  04f3c:  orr r2, r2, #1                    
  04f40:  str r2, [r0]                      
  04f42:  b #0x4f4e                         -> 0x04f4e (вне списка функций)
  04f44:  ldr r2, [r0]                      
  04f46:  movw r3, #0xfffe                  
  04f4a:  ands r2, r3                       
  04f4c:  str r2, [r0]                      
  04f4e:  bx lr                             
```
