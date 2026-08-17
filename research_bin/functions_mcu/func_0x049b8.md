# func_0x049b8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800049b8) | `0x000049b8` |
| размер кода | 70 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00186a00 — прочее (r0)

## Вызовы (callees)

- `func_0x016d4` (0x000016d4, bl)
- `func_0x01bdc` (0x00001bdc, bl)
- `func_0x02a6c` (0x00002a6c, bl)
- 0x049cc (b, вне списка функций)
- 0x049fa (b, вне списка функций)
- `func_0x04e08` (0x00004e08, bl)
- `func_0x08348` (0x00008348, bl)
- `func_0x10770` (0x00010770, bl)

## Кто вызывает (callers / xrefs)

- `func_0x05bc4` (bl @0x00005bda)
- `func_0x05bc4` (bl @0x00005c14)
- `func_0x05bc4` (bl @0x00005c50)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x049ca..0x049cc` (2 Б); цели из: 0x049c0
- `0x049cc..0x049f8` (44 Б); цели из: 0x049c6
- `0x049f8..0x049fa` (2 Б); цели из: 0x049c4
- `0x049fa..0x049fe` (4 Б); цели из: 0x049c8, 0x049f6

## Дизассембляция

```asm
  049b8:  push {r3, r4, r5, lr}             
  049ba:  mov r4, r0                        
  049bc:  cbz r4, #0x49c8                   
  049be:  cmp r4, #1                        
  049c0:  beq #0x49ca                       
  049c2:  cmp r4, #2                        
  049c4:  bne #0x49f8                       
  049c6:  b #0x49cc                         -> 0x049cc (вне списка функций)
  049c8:  b #0x49fa                         -> 0x049fa (вне списка функций)
  049ca:  nop                               
  049cc:  bl #0x16d4                        -> func_0x016d4
  049d0:  bl #0x8348                        -> func_0x08348
  049d4:  bl #0x10770                       -> func_0x10770
  049d8:  bl #0x2a6c                        -> func_0x02a6c
  049dc:  bl #0x4e08                        -> func_0x04e08
  049e0:  ldr r0, [pc, #0x1c]               
  049e2:  str r0, [sp]                      
  049e4:  nop                               
  049e6:  ldr r0, [sp]                      
  049e8:  subs r1, r0, #1                   
  049ea:  str r1, [sp]                      
  049ec:  cmp r0, #0                        
  049ee:  bne #0x49e6                       
  049f0:  movs r0, #0x99                    
  049f2:  bl #0x1bdc                        -> func_0x01bdc
  049f6:  b #0x49fa                         -> 0x049fa (вне списка функций)
  049f8:  nop                               
  049fa:  nop                               
  049fc:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x04a00 (1 слов) — ВНЕ границ функции ---
  04a00:  .word 0x00186a00
```
