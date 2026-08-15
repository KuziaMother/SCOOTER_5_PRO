# func_0x0e740

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e740) | `0x0000e740` |
| размер кода | 190 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200012ba — RAM (r1)
- 0xffff8000 — прочее (r4)

## Вызовы (callees)

- 0x0e782 (b, вне списка функций)
- 0x0e7b0 (b, вне списка функций)
- 0x0e7d4 (b, вне списка функций)
- 0x0e7d6 (b, вне списка функций)
- 0x164f8 (bl, вне списка функций)
- 0x16504 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x06978` (bl @0x000069bc)
- `func_0x06978` (bl @0x000069cc)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0e76a..0x0e76e` (4 Б); цели из: 0x0e766
- `0x0e76e..0x0e780` (18 Б); цели из: 0x0e756
- `0x0e780..0x0e782` (2 Б); цели из: 0x0e77c
- `0x0e782..0x0e7a8` (38 Б); цели из: 0x0e76c
- `0x0e7a8..0x0e7b0` (8 Б); цели из: 0x0e7a0
- `0x0e7b0..0x0e7b4` (4 Б); цели из: 0x0e7a6, 0x0e7ac
- `0x0e7b4..0x0e7cc` (24 Б); цели из: 0x0e78e
- `0x0e7cc..0x0e7d4` (8 Б); цели из: 0x0e7c4
- `0x0e7d4..0x0e7d6` (2 Б); цели из: 0x0e7ca, 0x0e7d0
- `0x0e7d6..0x0e7e2` (12 Б); цели из: 0x0e7b2
- `0x0e7e2..0x0e7fa` (24 Б); цели из: 0x0e7da
- `0x0e7fa..0x0e7fe` (4 Б); цели из: 0x0e7e0

## Дизассембляция

```asm
  0e740:  push.w {r4, r5, r6, r7, r8, lr}   
  0e744:  mov r5, r0                        
  0e746:  movs r0, #0                       
  0e748:  strb r0, [r5]                     
  0e74a:  bl #0x16504                       -> 0x16504 (вне списка функций)
  0e74e:  ldr r1, [pc, #0xb0]               -> RAM
  0e750:  ldrh.w r1, [r1, #0x50]            
  0e754:  cmp r0, r1                        
  0e756:  blt #0xe76e                       
  0e758:  bl #0x16504                       -> 0x16504 (вне списка функций)
  0e75c:  ldr r1, [pc, #0xa0]               -> RAM
  0e75e:  ldrh.w r1, [r1, #0x50]            
  0e762:  subs r4, r0, r1                   
  0e764:  cmp r4, #0                        
  0e766:  bge #0xe76a                       
  0e768:  movs r4, #0                       
  0e76a:  uxth r6, r4                       
  0e76c:  b #0xe782                         -> 0x0e782 (вне списка функций)
  0e76e:  bl #0x16504                       -> 0x16504 (вне списка функций)
  0e772:  ldr r1, [pc, #0x8c]               -> RAM
  0e774:  ldrh.w r1, [r1, #0x50]            
  0e778:  subs r4, r1, r0                   
  0e77a:  cmp r4, #0                        
  0e77c:  bge #0xe780                       
  0e77e:  movs r4, #0                       
  0e780:  uxth r6, r4                       
  0e782:  bl #0x164f8                       -> 0x164f8 (вне списка функций)
  0e786:  ldr r1, [pc, #0x78]               -> RAM
  0e788:  ldrsh.w r1, [r1, #0x48]           
  0e78c:  cmp r0, r1                        
  0e78e:  blt #0xe7b4                       
  0e790:  bl #0x164f8                       -> 0x164f8 (вне списка функций)
  0e794:  ldr r1, [pc, #0x68]               -> RAM
  0e796:  ldrsh.w r1, [r1, #0x48]           
  0e79a:  subs r4, r0, r1                   
  0e79c:  cmp.w r4, #0x8000                 
  0e7a0:  blt #0xe7a8                       
  0e7a2:  movw r4, #0x7fff                  
  0e7a6:  b #0xe7b0                         -> 0x0e7b0 (вне списка функций)
  0e7a8:  cmn.w r4, #0x8000                 
  0e7ac:  bge #0xe7b0                       
  0e7ae:  ldr r4, [pc, #0x54]               
  0e7b0:  sxth r7, r4                       
  0e7b2:  b #0xe7d6                         -> 0x0e7d6 (вне списка функций)
  0e7b4:  bl #0x164f8                       -> 0x164f8 (вне списка функций)
  0e7b8:  ldr r1, [pc, #0x44]               -> RAM
  0e7ba:  ldrsh.w r1, [r1, #0x48]           
  0e7be:  subs r4, r1, r0                   
  0e7c0:  cmp.w r4, #0x8000                 
  0e7c4:  blt #0xe7cc                       
  0e7c6:  movw r4, #0x7fff                  
  0e7ca:  b #0xe7d4                         -> 0x0e7d4 (вне списка функций)
  0e7cc:  cmn.w r4, #0x8000                 
  0e7d0:  bge #0xe7d4                       
  0e7d2:  ldr r4, [pc, #0x30]               
  0e7d4:  sxth r7, r4                       
  0e7d6:  cmp.w r6, #0x1f4                  
  0e7da:  bge #0xe7e2                       
  0e7dc:  cmp.w r7, #0x1f4                  
  0e7e0:  ble #0xe7fa                       
  0e7e2:  movs r0, #1                       
  0e7e4:  strb r0, [r5]                     
  0e7e6:  bl #0x16504                       -> 0x16504 (вне списка функций)
  0e7ea:  ldr r1, [pc, #0x14]               -> RAM
  0e7ec:  strh.w r0, [r1, #0x50]            
  0e7f0:  bl #0x164f8                       -> 0x164f8 (вне списка функций)
  0e7f4:  ldr r1, [pc, #8]                  -> RAM
  0e7f6:  strh.w r0, [r1, #0x48]            
  0e7fa:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x0e800 (2 слов) — ВНЕ границ функции ---
  0e800:  .word 0x200012ba  ; RAM
  0e804:  .word 0xffff8000
```
