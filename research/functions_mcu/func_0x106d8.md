# func_0x106d8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800106d8) | `0x000106d8` |
| размер кода | 54 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40013000 — периферия (r0)
- 0x40013c00 — периферия (r0)

## Вызовы (callees)

- `func_0x0c6c4` (0x0000c6c4, bl)
- 0x1070c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x106b8` (bl @0x000106c4)


## Дизассембляция

```asm
  106d8:  push {r4, lr}                     
  106da:  mov r4, r0                        
  106dc:  ldr r0, [pc, #0x30]               -> периферия
  106de:  cmp r4, r0                        
  106e0:  bne #0x106f4                      
  106e2:  movs r1, #1                       
  106e4:  asrs r0, r0, #0x12                
  106e6:  bl #0xc6c4                        -> func_0x0c6c4
  106ea:  movs r1, #0                       
  106ec:  asrs r0, r4, #0x12                
  106ee:  bl #0xc6c4                        -> func_0x0c6c4
  106f2:  b #0x1070c                        -> 0x1070c (вне списка функций)
  106f4:  ldr r0, [pc, #0x1c]               -> периферия
  106f6:  cmp r4, r0                        
  106f8:  bne #0x1070c                      
  106fa:  movs r1, #1                       
  106fc:  lsls r0, r1, #0x13                
  106fe:  bl #0xc6c4                        -> func_0x0c6c4
  10702:  movs r1, #0                       
  10704:  mov.w r0, #0x80000                
  10708:  bl #0xc6c4                        -> func_0x0c6c4
  1070c:  pop {r4, pc}                      
  ; --- literal-пул @0x10710 (2 слов) — ВНЕ границ функции ---
  10710:  .word 0x40013000  ; периферия
  10714:  .word 0x40013c00  ; периферия
```
