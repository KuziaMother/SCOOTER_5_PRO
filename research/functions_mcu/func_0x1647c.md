# func_0x1647c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001647c) | `0x0001647c` |
| размер кода | 86 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x16410` (0x00016410, bl)
- 0x164b2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08938` (bl @0x00008a0a)
- `func_0x08938` (bl @0x00008a24)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1649c..0x164b0` (20 Б); цели из: 0x16492
- `0x164b0..0x164b6` (6 Б); цели из: 0x1649a, 0x1649e, 0x164a2, 0x164a6…
- `0x164b6..0x164d2` (28 Б); цели из: 0x164ae

## Дизассембляция

```asm
  1647c:  push.w {r4, r5, r6, r7, r8, sb, lr}
  16480:  mov r4, r0                        
  16482:  mov r5, r1                        
  16484:  mov r6, r2                        
  16486:  mov r7, r3                        
  16488:  mov.w r8, #0                      
  1648c:  mov sb, r8                        
  1648e:  cmp.w r4, #0x7d0                  
  16492:  bge #0x1649c                      
  16494:  movw r0, #0xbb8                   
  16498:  cmp r4, r0                        
  1649a:  bge #0x164b0                      
  1649c:  cmp r5, #1                        
  1649e:  blt #0x164b0                      
  164a0:  cmp r5, #0xc                      
  164a2:  bgt #0x164b0                      
  164a4:  cmp r6, #1                        
  164a6:  blt #0x164b0                      
  164a8:  cmp r6, #0x1f                     
  164aa:  bgt #0x164b0                      
  164ac:  cmp r7, #0x17                     
  164ae:  ble #0x164b6                      
  164b0:  movs r0, #0                       
  164b2:  pop.w {r4, r5, r6, r7, r8, sb, pc}
  164b6:  mov r2, r6                        
  164b8:  mov r1, r5                        
  164ba:  mov r0, r4                        
  164bc:  bl #0x16410                       -> func_0x16410
  164c0:  mov sb, r0                        
  164c2:  sub.w r0, sb, #1                  
  164c6:  add.w r0, r0, r0, lsl #1          
  164ca:  add.w r8, r7, r0, lsl #3          
  164ce:  mov r0, r8                        
  164d0:  b #0x164b2                        -> 0x164b2 (вне списка функций)
```
