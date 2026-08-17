# func_0x056bc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800056bc) | `0x000056bc` |
| размер кода | 174 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000cb3 — RAM (r0)
- 0x200030dd — RAM (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x01e34` (0x00001e34, bl)
- 0x0574a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0571a..0x05730` (22 Б); цели из: 0x056e4
- `0x05730..0x0574a` (26 Б); цели из: 0x056de
- `0x0574a..0x0576a` (32 Б); цели из: 0x05718, 0x0572e

## Дизассембляция

```asm
  056bc:  push.w {r4, r5, r6, r7, r8, lr}   
  056c0:  mov r7, r0                        
  056c2:  mov r5, r1                        
  056c4:  mov r8, r2                        
  056c6:  movs r4, #0                       
  056c8:  mov r6, r7                        
  056ca:  movs r2, #0x74                    
  056cc:  mov r1, r4                        
  056ce:  adds r4, r4, #1                   
  056d0:  strb r2, [r5, r1]                 
  056d2:  ldrb r2, [r6, #2]                 
  056d4:  mov r1, r4                        
  056d6:  adds r4, r4, #1                   
  056d8:  strb r2, [r5, r1]                 
  056da:  ldrb r0, [r6]                     
  056dc:  cmp r0, #0x10                     
  056de:  bne #0x5730                       
  056e0:  ldrb r0, [r6, #2]                 
  056e2:  cmp r0, #0x81                     
  056e4:  bne #0x571a                       
  056e6:  movs r2, #0x1b                    
  056e8:  mov r0, r4                        
  056ea:  adds r1, r4, #1                   
  056ec:  uxtb r4, r1                       
  056ee:  strb r2, [r5, r0]                 
  056f0:  ldr r0, [pc, #0x78]               -> RAM
  056f2:  ldrb r2, [r0]                     
  056f4:  mov r0, r4                        
  056f6:  adds r1, r4, #1                   
  056f8:  uxtb r4, r1                       
  056fa:  strb r2, [r5, r0]                 
  056fc:  ldr r0, [pc, #0x6c]               -> RAM
  056fe:  ldrb r2, [r0, #1]                 
  05700:  mov r0, r4                        
  05702:  adds r1, r4, #1                   
  05704:  uxtb r4, r1                       
  05706:  strb r2, [r5, r0]                 
  05708:  adds r0, r5, r4                   
  0570a:  movs r2, #0x19                    
  0570c:  ldr r1, [pc, #0x60]               -> RAM
  0570e:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  05712:  add.w r0, r4, #0x19               
  05716:  uxtb r4, r0                       
  05718:  b #0x574a                         -> 0x0574a (вне списка функций)
  0571a:  movs r2, #0x4f                    
  0571c:  mov r0, r4                        
  0571e:  adds r1, r4, #1                   
  05720:  uxtb r4, r1                       
  05722:  strb r2, [r5, r0]                 
  05724:  movs r2, #0x4b                    
  05726:  mov r0, r4                        
  05728:  adds r1, r4, #1                   
  0572a:  uxtb r4, r1                       
  0572c:  strb r2, [r5, r0]                 
  0572e:  b #0x574a                         -> 0x0574a (вне списка функций)
  05730:  ldrb r2, [r6, #4]                 
  05732:  mov r0, r4                        
  05734:  adds r1, r4, #1                   
  05736:  uxtb r4, r1                       
  05738:  strb r2, [r5, r0]                 
  0573a:  ldrb r2, [r6, #4]                 
  0573c:  adds r0, r5, r4                   
  0573e:  adds r1, r6, #5                   
  05740:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  05744:  ldrb r0, [r6, #4]                 
  05746:  add r0, r4                        
  05748:  uxtb r4, r0                       
  0574a:  mov r1, r4                        
  0574c:  mov r0, r5                        
  0574e:  bl #0x1e34                        -> func_0x01e34
  05752:  strb r0, [r5, r4]                 
  05754:  adds r0, r4, #1                   
  05756:  uxtb r4, r0                       
  05758:  movs r2, #0x8b                    
  0575a:  mov r0, r4                        
  0575c:  adds r1, r4, #1                   
  0575e:  uxtb r4, r1                       
  05760:  strb r2, [r5, r0]                 
  05762:  strb.w r4, [r8]                   
  05766:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x0576c (2 слов) — ВНЕ границ функции ---
  0576c:  .word 0x20000cb3  ; RAM
  05770:  .word 0x200030dd  ; RAM
```
