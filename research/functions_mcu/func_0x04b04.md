# func_0x04b04

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004b04) | `0x00004b04` |
| размер кода | 28 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x04a04` (0x00004a04, bl)
- `func_0x04a4c` (0x00004a4c, bl)
- `func_0x12d04` (0x00012d04, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  04b04:  push {lr}                         
  04b06:  sub sp, #0x9c                     
  04b08:  bl #0x4a04                        -> func_0x04a04
  04b0c:  add r0, sp, #4                    
  04b0e:  bl #0x12d04                       -> func_0x12d04
  04b12:  cbz r0, #0x4b1c                   
  04b14:  add r1, sp, #4                    
  04b16:  movs r0, #0                       
  04b18:  bl #0x4a4c                        -> func_0x04a4c
  04b1c:  add sp, #0x9c                     
  04b1e:  pop {pc}                          
```
