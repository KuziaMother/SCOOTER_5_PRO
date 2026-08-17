# func_0x04f58

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004f58) | `0x00004f58` |
| размер кода | 20 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x04f6e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04fc0` (bl @0x00004fc6)
- `func_0x05000` (bl @0x00005008)


## Дизассембляция

```asm
  04f58:  push {r4, lr}                     
  04f5a:  mov r2, r0                        
  04f5c:  movs r0, #0                       
  04f5e:  movs r3, #0                       
  04f60:  ldr r3, [r1]                      
  04f62:  and.w r4, r3, r2                  
  04f66:  cbz r4, #0x4f6c                   
  04f68:  movs r0, #1                       
  04f6a:  b #0x4f6e                         -> 0x04f6e (вне списка функций)
```
