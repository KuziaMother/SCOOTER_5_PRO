# func_0x156ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800156ac) | `0x000156ac` |
| размер кода | 92 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f70 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x0ab0c` (0x0000ab0c, bl)
- 0x0accc (bl, вне списка функций)
- 0x156ca (b, вне списка функций)
- 0x156ce (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x055c8` (bl @0x000055f8)
- `func_0x0f1ec` (bl @0x0000f22c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x156c6..0x156ca` (4 Б); цели из: 0x156c2
- `0x156ca..0x156ce` (4 Б); цели из: 0x156b8
- `0x156ce..0x15708` (58 Б); цели из: 0x156c4

## Дизассембляция

```asm
  156ac:  push {r4, r5, r6, lr}             
  156ae:  sub sp, #0x50                     
  156b0:  movs r4, #0                       
  156b2:  movs r5, #0                       
  156b4:  movs r6, #0                       
  156b6:  nop                               
  156b8:  b #0x156ca                        -> 0x156ca (вне списка функций)
  156ba:  add r0, sp, #0x20                 
  156bc:  bl #0xab0c                        -> func_0x0ab0c
  156c0:  cmp r0, #1                        
  156c2:  bne #0x156c6                      
  156c4:  b #0x156ce                        -> 0x156ce (вне списка функций)
  156c6:  adds r0, r4, #1                   
  156c8:  uxtb r4, r0                       
  156ca:  cmp r4, #3                        
  156cc:  blt #0x156ba                      
  156ce:  nop                               
  156d0:  ldr r0, [pc, #0x34]               -> RAM
  156d2:  ldrb r0, [r0, #2]                 
  156d4:  ubfx r0, r0, #1, #1               
  156d8:  strb.w r0, [sp, #0x4d]            
  156dc:  movs r1, #1                       
  156de:  add.w r0, sp, #0x4d               
  156e2:  bl #0x8a50                        -> func_0x08a50
  156e6:  mov r5, r0                        
  156e8:  add r0, sp, #0x20                 
  156ea:  strh.w r5, [sp, #0x4e]            
  156ee:  movs r2, #0x20                    
  156f0:  add r1, sp, #0x30                 
  156f2:  mov r0, sp                        
  156f4:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  156f8:  add r0, sp, #0x20                 
  156fa:  ldm r0, {r0, r1, r2, r3}          
  156fc:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  15700:  mov r6, r0                        
  15702:  mov r0, r6                        
  15704:  add sp, #0x50                     
  15706:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x15708 (1 слов) — ВНЕ границ функции ---
  15708:  .word 0x20000f70  ; RAM
```
