# func_0x012aa

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800012aa) | `0x000012aa` |
| размер кода | 156 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0126c` (0x0000126c, bl)
- `func_0x0128c` (0x0000128c, b)
- 0x012c0 (b, вне списка функций)
- 0x01306 (b, вне списка функций)
- 0x0130c (b, вне списка функций)
- 0x014e8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01218` (bl @0x00001232)
- `func_0x01346` (bl @0x00001400)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x012c0..0x01302` (66 Б); цели из: 0x012b8
- `0x01302..0x0130a` (8 Б); цели из: 0x012d8
- `0x0130a..0x0130c` (2 Б); цели из: 0x012fc
- `0x0130c..0x01316` (10 Б); цели из: 0x01300
- `0x01316..0x01332` (28 Б); цели из: 0x012e0
- `0x01332..0x01346` (20 Б); цели из: 0x0132a

## Дизассембляция

```asm
  012aa:  push.w {r4, r5, r6, r7, r8, sl, fp, lr}
  012ae:  mov sl, r2                        
  012b0:  mov fp, r3                        
  012b2:  cbz r1, #0x12ba                   
  012b4:  clz r2, r1                        
  012b8:  b #0x12c0                         -> 0x012c0 (вне списка функций)
  012ba:  clz r2, r0                        
  012be:  adds r2, #0x20                    
  012c0:  mov r8, r2                        
  012c2:  bl #0x14e8                        -> 0x014e8 (вне списка функций)
  012c6:  mov r4, r0                        
  012c8:  mov r7, r1                        
  012ca:  orr.w r0, r0, sl                  
  012ce:  orr.w r1, r1, fp                  
  012d2:  mov r3, sl                        
  012d4:  mov r2, fp                        
  012d6:  orrs r0, r1                       
  012d8:  beq #0x1302                       
  012da:  mov r1, r2                        
  012dc:  orrs.w r0, r3, r1                 
  012e0:  beq #0x1316                       
  012e2:  rsb.w r2, r8, #0x40               
  012e6:  mov r0, sl                        
  012e8:  bl #0x126c                        -> func_0x0126c
  012ec:  mov r5, r0                        
  012ee:  mov r6, r1                        
  012f0:  mov r0, sl                        
  012f2:  mov r1, fp                        
  012f4:  mov r2, r8                        
  012f6:  bl #0x14e8                        -> 0x014e8 (вне списка функций)
  012fa:  orrs r0, r1                       
  012fc:  beq #0x130a                       
  012fe:  movs r0, #1                       
  01300:  b #0x130c                         -> 0x0130c (вне списка функций)
  01302:  mov r0, r4                        
  01304:  mov r1, r7                        
  01306:  pop.w {r4, r5, r6, r7, r8, sl, fp, pc}
  0130a:  movs r0, #0                       
  0130c:  orrs r5, r0                       
  0130e:  orr.w r6, r6, r0, asr #31         
  01312:  orrs r4, r5                       
  01314:  orrs r7, r6                       
  01316:  ldr r0, [sp, #0x28]               
  01318:  lsls r3, r4, #0x15                
  0131a:  lsrs r4, r4, #0xb                 
  0131c:  sub.w r0, r0, r8                  
  01320:  movs r2, #0                       
  01322:  lsrs r5, r7, #0xb                 
  01324:  orr.w r4, r4, r7, lsl #21         
  01328:  adds r0, #0xa                     
  0132a:  bpl #0x1332                       
  0132c:  movs r0, #0                       
  0132e:  mov r1, r0                        
  01330:  b #0x1306                         -> 0x01306 (вне списка функций)
  01332:  lsls r1, r0, #0x14                
  01334:  adds r0, r2, r4                   
  01336:  adcs r1, r5                       
  01338:  ldrd r4, r5, [sp, #0x20]          
  0133c:  adds r0, r0, r4                   
  0133e:  adcs r1, r5                       
  01340:  pop.w {r4, r5, r6, r7, r8, sl, fp, lr}
  01344:  b #0x128c                         -> func_0x0128c
```
