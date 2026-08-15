# func_0x07e70

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007e70) | `0x00007e70` |
| размер кода | 40 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x07e86 (b, вне списка функций)
- 0x07e90 (b, вне списка функций)
- `func_0x07e98` (0x00007e98, bl)

## Кто вызывает (callers / xrefs)

- `func_0x07d6c` (bl @0x00007df6)


## Дизассембляция

```asm
  07e70:  push {r4, r5, r6, lr}             
  07e72:  mov r6, r0                        
  07e74:  mov r4, r1                        
  07e76:  movs r5, #0                       
  07e78:  nop                               
  07e7a:  b #0x7e90                         -> 0x07e90 (вне списка функций)
  07e7c:  mov r0, r6                        
  07e7e:  bl #0x7e98                        -> func_0x07e98
  07e82:  cbnz r0, #0x7e88                  
  07e84:  movs r0, #0                       
  07e86:  pop {r4, r5, r6, pc}              
  07e88:  add.w r6, r6, #0x800              
  07e8c:  adds r0, r5, #1                   
  07e8e:  uxth r5, r0                       
  07e90:  cmp r5, r4                        
  07e92:  blt #0x7e7c                       
  07e94:  movs r0, #1                       
  07e96:  b #0x7e86                         -> 0x07e86 (вне списка функций)
```
