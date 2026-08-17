# func_0x0c464

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c464) | `0x0000c464` |
| размер кода | 20 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x0ae9a` (bl @0x0000afde)
- `func_0x0aece` (bl @0x0000afde)
- `func_0x0af94` (bl @0x0000afde)


## Дизассембляция

```asm
  0c464:  push {r4, lr}                     
  0c466:  mov r4, r0                        
  0c468:  movs r0, #0                       
  0c46a:  strb r0, [r4, #4]                 
  0c46c:  strb r0, [r4, #5]                 
  0c46e:  strb r2, [r4, #6]                 
  0c470:  strb r3, [r4, #7]                 
  0c472:  str r1, [r4]                      
  0c474:  movs r0, #1                       
  0c476:  pop {r4, pc}                      
```
