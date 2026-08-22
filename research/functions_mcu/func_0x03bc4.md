# func_0x03bc4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003bc4) | `0x00003bc4` |
| размер кода | 62 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x03bf2 (b, вне списка функций)
- 0x03bf4 (b, вне списка функций)
- 0x03bf8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x15918` (bl @0x00015934)
- `func_0x15df4` (bl @0x00015e3e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x03bf2..0x03bf4` (2 Б); цели из: 0x03be8
- `0x03bf4..0x03bf8` (4 Б); цели из: 0x03bda
- `0x03bf8..0x03c02` (10 Б); цели из: 0x03bce

## Дизассембляция

```asm
  03bc4:  push {r4, r5, r6, r7, lr}         
  03bc6:  movw r4, #0x1021                  
  03bca:  movs r5, #0                       
  03bcc:  movs r3, #0                       
  03bce:  b #0x3bf8                         -> 0x03bf8 (вне списка функций)
  03bd0:  ldrb r5, [r1], #1                 
  03bd4:  eor.w r0, r0, r5, lsl #8          
  03bd8:  movs r3, #0                       
  03bda:  b #0x3bf4                         -> 0x03bf4 (вне списка функций)
  03bdc:  and r6, r0, #0x8000               
  03be0:  cbz r6, #0x3bea                   
  03be2:  eor.w r6, r4, r0, lsl #1          
  03be6:  uxth r0, r6                       
  03be8:  b #0x3bf2                         -> 0x03bf2 (вне списка функций)
  03bea:  movw r6, #0xffff                  
  03bee:  and.w r0, r6, r0, lsl #1          
  03bf2:  adds r3, r3, #1                   
  03bf4:  cmp r3, #8                        
  03bf6:  blt #0x3bdc                       
  03bf8:  subs r6, r2, #0                   
  03bfa:  sub.w r2, r2, #1                  
  03bfe:  bne #0x3bd0                       
  03c00:  pop {r4, r5, r6, r7, pc}          
```
