# func_0x0a910

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000a910) | `0x0000a910` |
| размер кода | 70 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801f000 — flash-mirror @0x1f000 (r7)
- 0x0801f800 — flash-mirror @0x1f800 (r7)

## Вызовы (callees)

- `func_0x07fd4` (0x00007fd4, bl)
- 0x0a92c (b, вне списка функций)
- 0x0a942 (b, вне списка функций)
- 0x0a94e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0ab0c` (bl @0x0000ab22)
- `func_0x0ab0c` (bl @0x0000ab2a)
- `func_0x0acce` (bl @0x0000acdc)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0a92a..0x0a92c` (2 Б); цели из: 0x0a924
- `0x0a92c..0x0a946` (26 Б); цели из: 0x0a920, 0x0a928
- `0x0a946..0x0a94e` (8 Б); цели из: 0x0a93e
- `0x0a94e..0x0a956` (8 Б); цели из: 0x0a92e

## Дизассембляция

```asm
  0a910:  push.w {r4, r5, r6, r7, r8, lr}   
  0a914:  mov r4, r0                        
  0a916:  movs r6, #0                       
  0a918:  movs r5, #0                       
  0a91a:  movs r7, #0                       
  0a91c:  cbnz r4, #0xa922                  
  0a91e:  ldr r7, [pc, #0x38]               -> flash-mirror @0x1f000
  0a920:  b #0xa92c                         -> 0x0a92c (вне списка функций)
  0a922:  cmp r4, #1                        
  0a924:  bne #0xa92a                       
  0a926:  ldr r7, [pc, #0x34]               -> flash-mirror @0x1f800
  0a928:  b #0xa92c                         -> 0x0a92c (вне списка функций)
  0a92a:  ldr r7, [pc, #0x2c]               -> flash-mirror @0x1f000
  0a92c:  movs r5, #0                       
  0a92e:  b #0xa94e                         -> 0x0a94e (вне списка функций)
  0a930:  rsb r1, r5, r5, lsl #3            
  0a934:  add.w r0, r7, r1, lsl #3          
  0a938:  bl #0x7fd4                        -> func_0x07fd4
  0a93c:  cmp r0, #0xaa                     
  0a93e:  beq #0xa946                       
  0a940:  mov r0, r6                        
  0a942:  pop.w {r4, r5, r6, r7, r8, pc}    
  0a946:  adds r0, r6, #1                   
  0a948:  uxtb r6, r0                       
  0a94a:  adds r0, r5, #1                   
  0a94c:  uxtb r5, r0                       
  0a94e:  cmp r5, #0x24                     
  0a950:  blo #0xa930                       
  0a952:  mov r0, r6                        
  0a954:  b #0xa942                         -> 0x0a942 (вне списка функций)
  ; --- literal-пул @0x0a958 (2 слов) — ВНЕ границ функции ---
  0a958:  .word 0x0801f000  ; flash-mirror @0x1f000
  0a95c:  .word 0x0801f800  ; flash-mirror @0x1f800
```
