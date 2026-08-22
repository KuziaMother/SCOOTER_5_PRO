# func_0x157e0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800157e0) | `0x000157e0` |
| размер кода | 266 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00025e20 — прочее (r1)
- 0x2000304c — RAM (r0)
- 0x2000305c — RAM (r0)

## Вызовы (callees)

- `func_0x082f0` (0x000082f0, bl)
- `func_0x084a0` (0x000084a0, bl)
- `func_0x1570c` (0x0001570c, bl)
- 0x1586a (b, вне списка функций)
- 0x1586c (b, вне списка функций)
- 0x15876 (b, вне списка функций)
- 0x158be (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0d938` (bl @0x0000dcfc)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1580e..0x1581c` (14 Б); цели из: 0x157f0, 0x157fa, 0x15804
- `0x1581c..0x15856` (58 Б); цели из: 0x1580c
- `0x15856..0x1586c` (22 Б); цели из: 0x15852
- `0x1586c..0x15876` (10 Б); цели из: 0x15842
- `0x15876..0x158aa` (52 Б); цели из: 0x15854
- `0x158aa..0x158be` (20 Б); цели из: 0x158a0
- `0x158be..0x158c6` (8 Б); цели из: 0x158ae
- `0x158c6..0x158e2` (28 Б); цели из: 0x1588a
- `0x158e2..0x158ea` (8 Б); цели из: 0x158d8

## Дизассембляция

```asm
  157e0:  push {r3, r4, r5, r6, r7, lr}     
  157e2:  movs r4, #0                       
  157e4:  movs r6, #0                       
  157e6:  movs r5, #3                       
  157e8:  ldr r0, [pc, #0x100]              -> RAM
  157ea:  ldr r0, [r0, #4]                  
  157ec:  cmp.w r0, #0x21000                
  157f0:  blo #0x1580e                      
  157f2:  ldr r0, [pc, #0xf8]               -> RAM
  157f4:  ldr r0, [r0, #4]                  
  157f6:  ldr r1, [pc, #0xf8]               
  157f8:  cmp r0, r1                        
  157fa:  bhi #0x1580e                      
  157fc:  ldr r0, [pc, #0xec]               -> RAM
  157fe:  ldr r0, [r0, #8]                  
  15800:  cmp.w r0, #0x21000                
  15804:  blo #0x1580e                      
  15806:  ldr r0, [pc, #0xe4]               -> RAM
  15808:  ldr r0, [r0, #8]                  
  1580a:  cmp r0, r1                        
  1580c:  bls #0x1581c                      
  1580e:  movs r0, #0                       
  15810:  ldr r1, [pc, #0xd8]               -> RAM
  15812:  str r0, [r1]                      
  15814:  mov.w r0, #0x21000                
  15818:  str r0, [r1, #4]                  
  1581a:  str r0, [r1, #8]                  
  1581c:  ldr r0, [pc, #0xcc]               -> RAM
  1581e:  ldrh r0, [r0, #8]                 
  15820:  ubfx r0, r0, #0, #0xc             
  15824:  cbnz r0, #0x15842                 
  15826:  ldr r1, [pc, #0xc4]               -> RAM
  15828:  ldr r0, [r1, #8]                  
  1582a:  bl #0x82f0                        -> func_0x082f0
  1582e:  mov.w r0, #0x3e8                  
  15832:  str r0, [sp]                      
  15834:  nop                               
  15836:  ldr r0, [sp]                      
  15838:  subs r1, r0, #1                   
  1583a:  str r1, [sp]                      
  1583c:  cmp r0, #0                        
  1583e:  bne #0x15836                      
  15840:  nop                               
  15842:  b #0x1586c                        -> 0x1586c (вне списка функций)
  15844:  ldr r0, [pc, #0xa4]               -> RAM
  15846:  movs r2, #0x28                    
  15848:  ldr r1, [r0, #8]                  
  1584a:  ldr r0, [pc, #0xa8]               -> RAM
  1584c:  bl #0x84a0                        -> func_0x084a0
  15850:  cmp r0, #1                        
  15852:  bne #0x15856                      
  15854:  b #0x15876                        -> 0x15876 (вне списка функций)
  15856:  mov.w r0, #0x1f4                  
  1585a:  str r0, [sp]                      
  1585c:  nop                               
  1585e:  ldr r0, [sp]                      
  15860:  subs r1, r0, #1                   
  15862:  str r1, [sp]                      
  15864:  cmp r0, #0                        
  15866:  bne #0x1585e                      
  15868:  cbnz r5, #0x1586c                 
  1586a:  pop {r3, r4, r5, r6, r7, pc}      
  1586c:  subs r0, r5, #0                   
  1586e:  sub.w r1, r5, #1                  
  15872:  uxtb r5, r1                       
  15874:  bne #0x15844                      
  15876:  nop                               
  15878:  ldr r0, [pc, #0x70]               -> RAM
  1587a:  ldr r0, [r0]                      
  1587c:  adds r0, r0, #1                   
  1587e:  ldr r1, [pc, #0x6c]               -> RAM
  15880:  str r0, [r1]                      
  15882:  mov r0, r1                        
  15884:  ldr r0, [r0]                      
  15886:  cmp.w r0, #0x1f4                  
  1588a:  bls #0x158c6                      
  1588c:  movs r0, #0                       
  1588e:  str r0, [r1]                      
  15890:  mov r0, r1                        
  15892:  ldr r0, [r0, #4]                  
  15894:  adds r0, #0x28                    
  15896:  str r0, [r1, #4]                  
  15898:  mov r0, r1                        
  1589a:  ldr r0, [r0, #4]                  
  1589c:  ldr r1, [pc, #0x50]               
  1589e:  cmp r0, r1                        
  158a0:  blo #0x158aa                      
  158a2:  mov.w r0, #0x21000                
  158a6:  ldr r1, [pc, #0x44]               -> RAM
  158a8:  str r0, [r1, #4]                  
  158aa:  movs r6, #1                       
  158ac:  movs r4, #0                       
  158ae:  b #0x158be                        -> 0x158be (вне списка функций)
  158b0:  lsls r1, r4, #0xc                 
  158b2:  add.w r0, r1, #0x21000            
  158b6:  bl #0x82f0                        -> func_0x082f0
  158ba:  adds r0, r4, #1                   
  158bc:  uxth r4, r0                       
  158be:  add.w r0, r6, #0x25               
  158c2:  cmp r0, r4                        
  158c4:  bhi #0x158b0                      
  158c6:  ldr r0, [pc, #0x24]               -> RAM
  158c8:  ldr r0, [r0, #8]                  
  158ca:  adds r0, #0x28                    
  158cc:  ldr r1, [pc, #0x1c]               -> RAM
  158ce:  str r0, [r1, #8]                  
  158d0:  mov r0, r1                        
  158d2:  ldr r0, [r0, #8]                  
  158d4:  ldr r1, [pc, #0x18]               
  158d6:  cmp r0, r1                        
  158d8:  blo #0x158e2                      
  158da:  mov.w r0, #0x21000                
  158de:  ldr r1, [pc, #0xc]                -> RAM
  158e0:  str r0, [r1, #8]                  
  158e2:  bl #0x1570c                       -> func_0x1570c
  158e6:  movs r0, #1                       
  158e8:  b #0x1586a                        -> 0x1586a (вне списка функций)
  ; --- literal-пул @0x158ec (3 слов) — ВНЕ границ функции ---
  158ec:  .word 0x2000304c  ; RAM
  158f0:  .word 0x00025e20
  158f4:  .word 0x2000305c  ; RAM
```
