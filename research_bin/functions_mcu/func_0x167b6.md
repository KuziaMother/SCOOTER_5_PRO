# func_0x167b6

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800167b6) | `0x000167b6` |
| размер кода | 202 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x167ec (b, вне списка функций)
- 0x167f4 (b, вне списка функций)
- 0x16832 (b, вне списка функций)
- 0x1687c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e808` (bl @0x0000e9d8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x167cc..0x167ea` (30 Б); цели из: 0x167c4
- `0x167ea..0x167ec` (2 Б); цели из: 0x167e4
- `0x167ec..0x167f4` (8 Б); цели из: 0x167e8
- `0x167f4..0x1682c` (56 Б); цели из: 0x167dc
- `0x1682c..0x16832` (6 Б); цели из: 0x167d2
- `0x16832..0x16860` (46 Б); цели из: 0x167ca, 0x1682a
- `0x16860..0x1687c` (28 Б); цели из: 0x16840
- `0x1687c..0x16880` (4 Б); цели из: 0x1685e

## Дизассембляция

```asm
  167b6:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  167ba:  mov r5, r0                        
  167bc:  mov r4, r1                        
  167be:  ldrsh.w sb, [r4]                  
  167c2:  cmp sb, r5                        
  167c4:  blt #0x167cc                      
  167c6:  movs r1, #0                       
  167c8:  movs r6, #0                       
  167ca:  b #0x16832                        -> 0x16832 (вне списка функций)
  167cc:  ldrsh.w sb, [r4, r3, lsl #1]      
  167d0:  cmp sb, r5                        
  167d2:  ble #0x1682c                      
  167d4:  lsr.w r8, r3, #1                  
  167d8:  movs r1, #0                       
  167da:  mov ip, r3                        
  167dc:  b #0x167f4                        -> 0x167f4 (вне списка функций)
  167de:  ldrsh.w sb, [r4, r8, lsl #1]      
  167e2:  cmp sb, r5                        
  167e4:  ble #0x167ea                      
  167e6:  mov ip, r8                        
  167e8:  b #0x167ec                        -> 0x167ec (вне списка функций)
  167ea:  mov r1, r8                        
  167ec:  add.w sb, ip, r1                  
  167f0:  lsr.w r8, sb, #1                  
  167f4:  sub.w sb, ip, r1                  
  167f8:  cmp.w sb, #1                      
  167fc:  bhi #0x167de                      
  167fe:  add.w sb, r1, #1                  
  16802:  ldrh.w sb, [r4, sb, lsl #1]       
  16806:  ldrh.w sl, [r4, r1, lsl #1]       
  1680a:  sub.w sb, sb, sl                  
  1680e:  uxth.w sb, sb                     
  16812:  ldrh.w sl, [r4, r1, lsl #1]       
  16816:  sub.w sl, r5, sl                  
  1681a:  lsl.w sl, sl, #0x10               
  1681e:  lsr.w sl, sl, #8                  
  16822:  udiv sb, sl, sb                   
  16826:  uxth.w r6, sb                     
  1682a:  b #0x16832                        -> 0x16832 (вне списка функций)
  1682c:  subs r1, r3, #1                   
  1682e:  mov.w r6, #0x100                  
  16832:  add.w sb, r1, #1                  
  16836:  ldrb.w r7, [r2, sb]               
  1683a:  ldrb.w sb, [r2, r1]               
  1683e:  cmp sb, r7                        
  16840:  bgt #0x16860                      
  16842:  ldrb.w sb, [r2, r1]               
  16846:  sub.w sb, r7, sb                  
  1684a:  and sb, sb, #0xff                 
  1684e:  mul sb, sb, r6                    
  16852:  ldrb.w sl, [r2, r1]               
  16856:  add.w sb, sl, sb, lsr #8          
  1685a:  and r0, sb, #0xff                 
  1685e:  b #0x1687c                        -> 0x1687c (вне списка функций)
  16860:  ldrb.w sl, [r2, r1]               
  16864:  ldrb.w sb, [r2, r1]               
  16868:  sub.w sb, sb, r7                  
  1686c:  and sb, sb, #0xff                 
  16870:  mul sb, sb, r6                    
  16874:  sub.w sb, sl, sb, lsr #8          
  16878:  and r0, sb, #0xff                 
  1687c:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
```
