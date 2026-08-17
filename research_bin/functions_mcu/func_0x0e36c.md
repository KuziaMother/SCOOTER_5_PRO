# func_0x0e36c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e36c) | `0x0000e36c` |
| размер кода | 114 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xffff8000 — прочее (r4)

## Вызовы (callees)

- 0x0e384 (b, вне списка функций)
- 0x0e3d6 (b, вне списка функций)
- 0x0e3da (b, вне списка функций)
- `func_0x16328` (0x00016328, bl)

## Кто вызывает (callers / xrefs)

- `func_0x063b8` (bl @0x00006520)
- `func_0x06fc0` (bl @0x00006ff2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0e380..0x0e384` (4 Б); цели из: 0x0e378
- `0x0e384..0x0e394` (16 Б); цели из: 0x0e37e
- `0x0e394..0x0e3a2` (14 Б); цели из: 0x0e38c
- `0x0e3a2..0x0e3ac` (10 Б); цели из: 0x0e39a
- `0x0e3ac..0x0e3ce` (34 Б); цели из: 0x0e3a4
- `0x0e3ce..0x0e3d6` (8 Б); цели из: 0x0e3c6
- `0x0e3d6..0x0e3da` (4 Б); цели из: 0x0e3cc, 0x0e3d2
- `0x0e3da..0x0e3de` (4 Б); цели из: 0x0e392, 0x0e3a0, 0x0e3aa

## Дизассембляция

```asm
  0e36c:  push.w {r4, r5, r6, r7, r8, lr}   
  0e370:  mov r7, r0                        
  0e372:  mov r8, r1                        
  0e374:  mov r6, r2                        
  0e376:  cmp r7, r8                        
  0e378:  blt #0xe380                       
  0e37a:  mov r4, r7                        
  0e37c:  mov r5, r8                        
  0e37e:  b #0xe384                         -> 0x0e384 (вне списка функций)
  0e380:  mov r4, r8                        
  0e382:  mov r5, r7                        
  0e384:  subs r0, r4, r5                   
  0e386:  movw r1, #0x2710                  
  0e38a:  cmp r0, r1                        
  0e38c:  blt #0xe394                       
  0e38e:  movs r0, #0                       
  0e390:  strh r0, [r6]                     
  0e392:  b #0xe3da                         -> 0x0e3da (вне списка функций)
  0e394:  movw r0, #0x2710                  
  0e398:  cmp r4, r0                        
  0e39a:  ble #0xe3a2                       
  0e39c:  sxth r0, r4                       
  0e39e:  strh r0, [r6]                     
  0e3a0:  b #0xe3da                         -> 0x0e3da (вне списка функций)
  0e3a2:  cmp r5, #0                        
  0e3a4:  bge #0xe3ac                       
  0e3a6:  sxth r0, r5                       
  0e3a8:  strh r0, [r6]                     
  0e3aa:  b #0xe3da                         -> 0x0e3da (вне списка функций)
  0e3ac:  movw r2, #0x2710                  
  0e3b0:  subs r2, r2, r4                   
  0e3b2:  adds r1, r2, r5                   
  0e3b4:  movw r2, #0x2710                  
  0e3b8:  mul r0, r5, r2                    
  0e3bc:  bl #0x16328                       -> func_0x16328
  0e3c0:  mov r4, r0                        
  0e3c2:  cmp.w r4, #0x8000                 
  0e3c6:  blt #0xe3ce                       
  0e3c8:  movw r4, #0x7fff                  
  0e3cc:  b #0xe3d6                         -> 0x0e3d6 (вне списка функций)
  0e3ce:  cmn.w r4, #0x8000                 
  0e3d2:  bge #0xe3d6                       
  0e3d4:  ldr r4, [pc, #8]                  
  0e3d6:  sxth r0, r4                       
  0e3d8:  strh r0, [r6]                     
  0e3da:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x0e3e0 (1 слов) — ВНЕ границ функции ---
  0e3e0:  .word 0xffff8000
```
