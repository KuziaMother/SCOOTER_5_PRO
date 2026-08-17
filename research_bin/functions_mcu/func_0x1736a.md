# func_0x1736a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001736a) | `0x0001736a` |
| размер кода | 96 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x1619e` (0x0001619e, bl)
- `func_0x161ea` (0x000161ea, bl)
- 0x173c4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e2fc` (bl @0x0000e32e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x17386..0x173ba` (52 Б); цели из: 0x1737a
- `0x173ba..0x173c4` (10 Б); цели из: 0x1738c
- `0x173c4..0x173ca` (6 Б); цели из: 0x17384, 0x173b8

## Дизассембляция

```asm
  1736a:  push.w {r4, r5, r6, r7, r8, lr}   
  1736e:  mov r7, r0                        
  17370:  mov r5, r1                        
  17372:  mov r6, r2                        
  17374:  mov r8, r3                        
  17376:  ldr r0, [r5]                      
  17378:  cmp r0, r7                        
  1737a:  blt #0x17386                      
  1737c:  movs r4, #0                       
  1737e:  movs r0, #0                       
  17380:  str.w r0, [r8]                    
  17384:  b #0x173c4                        -> 0x173c4 (вне списка функций)
  17386:  ldr.w r0, [r5, r6, lsl #2]        
  1738a:  cmp r0, r7                        
  1738c:  ble #0x173ba                      
  1738e:  lsrs r2, r6, #1                   
  17390:  mov r3, r6                        
  17392:  mov r1, r5                        
  17394:  mov r0, r7                        
  17396:  bl #0x1619e                       -> func_0x1619e
  1739a:  mov r4, r0                        
  1739c:  adds r2, r4, #1                   
  1739e:  ldr.w r2, [r5, r2, lsl #2]        
  173a2:  ldr.w r3, [r5, r4, lsl #2]        
  173a6:  subs r1, r2, r3                   
  173a8:  ldr.w r2, [r5, r4, lsl #2]        
  173ac:  subs r0, r7, r2                   
  173ae:  movs r2, #0x10                    
  173b0:  bl #0x161ea                       -> func_0x161ea
  173b4:  str.w r0, [r8]                    
  173b8:  b #0x173c4                        -> 0x173c4 (вне списка функций)
  173ba:  subs r4, r6, #1                   
  173bc:  mov.w r0, #0x10000                
  173c0:  str.w r0, [r8]                    
  173c4:  mov r0, r4                        
  173c6:  pop.w {r4, r5, r6, r7, r8, pc}    
```
