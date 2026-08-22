# func_0x04a30

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004a30) | `0x00004a30` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x04a04` (0x00004a04, bl)
- `func_0x0df10` (0x0000df10, bl)
- `func_0x12f44` (0x00012f44, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  04a30:  push {lr}                         
  04a32:  sub sp, #0x9c                     
  04a34:  bl #0x4a04                        -> func_0x04a04
  04a38:  add r0, sp, #4                    
  04a3a:  bl #0x12f44                       -> func_0x12f44
  04a3e:  cbz r0, #0x4a46                   
  04a40:  add r0, sp, #4                    
  04a42:  bl #0xdf10                        -> func_0x0df10
  04a46:  add sp, #0x9c                     
  04a48:  pop {pc}                          
```
