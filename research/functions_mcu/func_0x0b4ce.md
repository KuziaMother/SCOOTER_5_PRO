# func_0x0b4ce

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b4ce) | `0x0000b4ce` |
| размер кода | 96 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00030002 — прочее (r7)
- 0x00070082 — прочее (r7)

## Вызовы (callees)

- `func_0x09794` (0x00009794, bl)
- `func_0x097ca` (0x000097ca, bl)
- `func_0x0985c` (0x0000985c, bl)
- `func_0x099bc` (0x000099bc, bl)
- 0x0b4e6 (b, вне списка функций)
- 0x0b4ea (b, вне списка функций)
- 0x0b516 (b, вне списка функций)
- 0x0b51e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0b4e6..0x0b4ea` (4 Б); цели из: 0x0b4e0
- `0x0b4ea..0x0b51e` (52 Б); цели из: 0x0b4de, 0x0b4e4
- `0x0b51e..0x0b52e` (16 Б); цели из: 0x0b4fa, 0x0b502

## Дизассембляция

```asm
  0b4ce:  push.w {r4, r5, r6, r7, r8, lr}   
  0b4d2:  ldrd r5, r4, [sp, #0x4c]          
  0b4d6:  movs r6, #0                       
  0b4d8:  movs r7, #0                       
  0b4da:  cbz r4, #0xb4e2                   
  0b4dc:  cmp r4, #1                        
  0b4de:  bne #0xb4ea                       
  0b4e0:  b #0xb4e6                         -> 0x0b4e6 (вне списка функций)
  0b4e2:  ldr r7, [pc, #0x4c]               
  0b4e4:  b #0xb4ea                         -> 0x0b4ea (вне списка функций)
  0b4e6:  ldr r7, [pc, #0x4c]               
  0b4e8:  nop                               
  0b4ea:  nop                               
  0b4ec:  mov r2, r4                        
  0b4ee:  mov r1, r5                        
  0b4f0:  ldr r0, [sp, #0x18]               
  0b4f2:  bl #0x99bc                        -> func_0x099bc
  0b4f6:  mov.w r6, #0x10000                
  0b4fa:  b #0xb51e                         -> 0x0b51e (вне списка функций)
  0b4fc:  subs r0, r6, #0                   
  0b4fe:  sub.w r6, r6, #1                  
  0b502:  bne #0xb51e                       
  0b504:  movs r1, #0                       
  0b506:  ldr r0, [sp, #0x18]               
  0b508:  bl #0x97ca                        -> func_0x097ca
  0b50c:  movs r1, #1                       
  0b50e:  ldr r0, [sp, #0x18]               
  0b510:  bl #0x985c                        -> func_0x0985c
  0b514:  movs r0, #3                       
  0b516:  pop.w {r4, r5, r6, r7, r8}        
  0b51a:  ldr pc, [sp], #0x14               
  0b51e:  mov r1, r7                        
  0b520:  ldr r0, [sp, #0x18]               
  0b522:  bl #0x9794                        -> func_0x09794
  0b526:  cmp r0, #0                        
  0b528:  beq #0xb4fc                       
  0b52a:  movs r0, #0                       
  0b52c:  b #0xb516                         -> 0x0b516 (вне списка функций)
  ; --- literal-пул @0x0b530 (2 слов) — ВНЕ границ функции ---
  0b530:  .word 0x00070082
  0b534:  .word 0x00030002
```
