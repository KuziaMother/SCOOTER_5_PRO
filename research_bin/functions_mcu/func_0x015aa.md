# func_0x015aa

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800015aa) | `0x000015aa` |
| размер кода | 198 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x01604 (b, вне списка функций)
- 0x0166e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x018fc` (bl @0x00001932)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x015c2..0x015ea` (40 Б); цели из: 0x015b6
- `0x015ea..0x01604` (26 Б); цели из: 0x015c4
- `0x01604..0x01628` (36 Б); цели из: 0x015e8
- `0x01628..0x0164c` (36 Б); цели из: 0x01606
- `0x0164c..0x0166e` (34 Б); цели из: 0x0162a
- `0x0166e..0x01670` (2 Б); цели из: 0x01626, 0x0164a

## Дизассембляция

```asm
  015aa:  push {r4, r5, r6, r7, lr}         
  015ac:  mov r4, r0                        
  015ae:  mov r5, r2                        
  015b0:  movs r0, #0                       
  015b2:  movs r2, #0                       
  015b4:  cmp r1, #0x12                     
  015b6:  bne #0x15c2                       
  015b8:  ldr r0, [r4, #0x5c]               
  015ba:  bic r0, r0, #7                    
  015be:  orrs r0, r3                       
  015c0:  str r0, [r4, #0x5c]               
  015c2:  cmp r1, #9                        
  015c4:  ble #0x15ea                       
  015c6:  ldr r0, [r4, #0xc]                
  015c8:  sub.w r6, r1, #0xa                
  015cc:  add.w r7, r6, r6, lsl #1          
  015d0:  movs r6, #7                       
  015d2:  lsl.w r2, r6, r7                  
  015d6:  bics r0, r2                       
  015d8:  sub.w r6, r1, #0xa                
  015dc:  add.w r6, r6, r6, lsl #1          
  015e0:  lsl.w r2, r3, r6                  
  015e4:  orrs r0, r2                       
  015e6:  str r0, [r4, #0xc]                
  015e8:  b #0x1604                         -> 0x01604 (вне списка функций)
  015ea:  ldr r0, [r4, #0x10]               
  015ec:  add.w r7, r1, r1, lsl #1          
  015f0:  movs r6, #7                       
  015f2:  lsl.w r2, r6, r7                  
  015f6:  bics r0, r2                       
  015f8:  add.w r6, r1, r1, lsl #1          
  015fc:  lsl.w r2, r3, r6                  
  01600:  orrs r0, r2                       
  01602:  str r0, [r4, #0x10]               
  01604:  cmp r5, #7                        
  01606:  bge #0x1628                       
  01608:  ldr r0, [r4, #0x34]               
  0160a:  subs r6, r5, #1                   
  0160c:  add.w r7, r6, r6, lsl #2          
  01610:  movs r6, #0x1f                    
  01612:  lsl.w r2, r6, r7                  
  01616:  bics r0, r2                       
  01618:  subs r6, r5, #1                   
  0161a:  add.w r6, r6, r6, lsl #2          
  0161e:  lsl.w r2, r1, r6                  
  01622:  orrs r0, r2                       
  01624:  str r0, [r4, #0x34]               
  01626:  b #0x166e                         -> 0x0166e (вне списка функций)
  01628:  cmp r5, #0xd                      
  0162a:  bge #0x164c                       
  0162c:  ldr r0, [r4, #0x30]               
  0162e:  subs r6, r5, #7                   
  01630:  add.w r7, r6, r6, lsl #2          
  01634:  movs r6, #0x1f                    
  01636:  lsl.w r2, r6, r7                  
  0163a:  bics r0, r2                       
  0163c:  subs r6, r5, #7                   
  0163e:  add.w r6, r6, r6, lsl #2          
  01642:  lsl.w r2, r1, r6                  
  01646:  orrs r0, r2                       
  01648:  str r0, [r4, #0x30]               
  0164a:  b #0x166e                         -> 0x0166e (вне списка функций)
  0164c:  ldr r0, [r4, #0x2c]               
  0164e:  sub.w r6, r5, #0xd                
  01652:  add.w r7, r6, r6, lsl #2          
  01656:  movs r6, #0x1f                    
  01658:  lsl.w r2, r6, r7                  
  0165c:  bics r0, r2                       
  0165e:  sub.w r6, r5, #0xd                
  01662:  add.w r6, r6, r6, lsl #2          
  01666:  lsl.w r2, r1, r6                  
  0166a:  orrs r0, r2                       
  0166c:  str r0, [r4, #0x2c]               
  0166e:  pop {r4, r5, r6, r7, pc}          
```
