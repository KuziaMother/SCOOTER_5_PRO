# func_0x0c94c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c94c) | `0x0000c94c` |
| размер кода | 54 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x058b0` (0x000058b0, bl)
- `func_0x05970` (0x00005970, bl)
- 0x0c9dc (bl, вне списка функций)
- 0x0c9fc (bl, вне списка функций)
- `func_0x0cb40` (0x0000cb40, bl)
- 0x0ce4c (bl, вне списка функций)
- `func_0x14958` (0x00014958, bl)

## Кто вызывает (callers / xrefs)

- `func_0x05cd0` (bl @0x00005cda)
- `func_0x110fc` (bl @0x000111aa)


## Дизассембляция

```asm
  0c94c:  push {r4, lr}                     
  0c94e:  mov r4, r0                        
  0c950:  movs r0, #5                       
  0c952:  bl #0x14958                       -> func_0x14958
  0c956:  mov r0, r4                        
  0c958:  bl #0xce4c                        -> 0x0ce4c (вне списка функций)
  0c95c:  movs r0, #1                       
  0c95e:  bl #0x58b0                        -> func_0x058b0
  0c962:  mov.w r0, #0x100000               
  0c966:  bl #0x5970                        -> func_0x05970
  0c96a:  movs r1, #1                       
  0c96c:  lsls r0, r1, #0xe                 
  0c96e:  bl #0xc9fc                        -> 0x0c9fc (вне списка функций)
  0c972:  mov.w r0, #0x4000                 
  0c976:  bl #0xc9dc                        -> 0x0c9dc (вне списка функций)
  0c97a:  movs r0, #1                       
  0c97c:  bl #0xcb40                        -> func_0x0cb40
  0c980:  pop {r4, pc}                      
```
