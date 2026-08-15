# func_0x035ec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800035ec) | `0x000035ec` |
| размер кода | 18 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x05cd0` (bl @0x00005d10)


## Дизассембляция

```asm
  035ec:  mov.w r0, #-0x1fff2000            
  035f0:  ldr r0, [r0, #0x10]               
  035f2:  bic r0, r0, #2                    
  035f6:  mov.w r1, #-0x1fff2000            
  035fa:  str r0, [r1, #0x10]               
  035fc:  bx lr                             
```
