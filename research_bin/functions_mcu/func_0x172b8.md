# func_0x172b8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800172b8) | `0x000172b8` |
| размер кода | 78 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1712c` (bl @0x0001713c)
- `func_0x17150` (bl @0x0001715e)


## Дизассембляция

```asm
  172b8:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  172bc:  mov r4, r0                        
  172be:  mov r5, r1                        
  172c0:  mov r6, r2                        
  172c2:  lsr.w sb, r4, #0x10               
  172c6:  uxth r0, r4                       
  172c8:  lsrs r7, r5, #0x10                
  172ca:  uxth r2, r5                       
  172cc:  mul ip, sb, r2                    
  172d0:  mul r8, r0, r7                    
  172d4:  muls r0, r2, r0                   
  172d6:  movs r2, #0                       
  172d8:  add.w r1, r0, r8, lsl #16         
  172dc:  cmp r1, r0                        
  172de:  bhs #0x172e2                      
  172e0:  movs r2, #1                       
  172e2:  mov r0, r1                        
  172e4:  add.w r1, r1, ip, lsl #16         
  172e8:  cmp r1, r0                        
  172ea:  bhs #0x172ee                      
  172ec:  adds r2, r2, #1                   
  172ee:  lsr.w sl, r8, #0x10               
  172f2:  add.w sl, sl, ip, lsr #16         
  172f6:  mla sl, sb, r7, sl                
  172fa:  add sl, r2                        
  172fc:  str.w sl, [r6]                    
  17300:  str r1, [r3]                      
  17302:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
```
