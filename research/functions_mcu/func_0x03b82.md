# func_0x03b82

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003b82) | `0x00003b82` |
| размер кода | 66 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x03bb4 (b, вне списка функций)
- 0x03bb6 (b, вне списка функций)
- 0x03bba (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x057a0` (bl @0x000057c4)
- `func_0x119e4` (bl @0x00011a8c)
- `func_0x119e4` (bl @0x00011ace)
- `func_0x119e4` (bl @0x00011b36)
- `func_0x15a60` (bl @0x00015b48)
- `func_0x15df4` (bl @0x00015e64)
- `func_0x15df4` (bl @0x00015e74)
- `func_0x15df4` (bl @0x00015eb0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x03bb4..0x03bb6` (2 Б); цели из: 0x03baa
- `0x03bb6..0x03bba` (4 Б); цели из: 0x03b9c
- `0x03bba..0x03bc4` (10 Б); цели из: 0x03b90

## Дизассембляция

```asm
  03b82:  push {r4, r5, r6, r7, lr}         
  03b84:  mov r2, r0                        
  03b86:  movs r0, #0                       
  03b88:  movw r4, #0x1021                  
  03b8c:  movs r5, #0                       
  03b8e:  movs r3, #0                       
  03b90:  b #0x3bba                         -> 0x03bba (вне списка функций)
  03b92:  ldrb r5, [r2], #1                 
  03b96:  eor.w r0, r0, r5, lsl #8          
  03b9a:  movs r3, #0                       
  03b9c:  b #0x3bb6                         -> 0x03bb6 (вне списка функций)
  03b9e:  and r6, r0, #0x8000               
  03ba2:  cbz r6, #0x3bac                   
  03ba4:  eor.w r6, r4, r0, lsl #1          
  03ba8:  uxth r0, r6                       
  03baa:  b #0x3bb4                         -> 0x03bb4 (вне списка функций)
  03bac:  movw r6, #0xffff                  
  03bb0:  and.w r0, r6, r0, lsl #1          
  03bb4:  adds r3, r3, #1                   
  03bb6:  cmp r3, #8                        
  03bb8:  blt #0x3b9e                       
  03bba:  subs r6, r1, #0                   
  03bbc:  sub.w r1, r1, #1                  
  03bc0:  bne #0x3b92                       
  03bc2:  pop {r4, r5, r6, r7, pc}          
```
