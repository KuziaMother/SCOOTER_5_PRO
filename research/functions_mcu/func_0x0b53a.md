# func_0x0b53a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b53a) | `0x0000b53a` |
| размер кода | 64 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00030001 — прочее (r1)

## Вызовы (callees)

- `func_0x09794` (0x00009794, bl)
- `func_0x097ca` (0x000097ca, bl)
- `func_0x09844` (0x00009844, bl)
- `func_0x0985c` (0x0000985c, bl)
- 0x0b564 (b, вне списка функций)
- 0x0b56a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0b53a:  push {r4, lr}                     
  0b53c:  movs r1, #1                       
  0b53e:  ldr r0, [sp, #8]                  
  0b540:  bl #0x9844                        -> func_0x09844
  0b544:  mov.w r4, #0x10000                
  0b548:  b #0xb56a                         -> 0x0b56a (вне списка функций)
  0b54a:  subs r0, r4, #0                   
  0b54c:  sub.w r4, r4, #1                  
  0b550:  bne #0xb56a                       
  0b552:  movs r1, #0                       
  0b554:  ldr r0, [sp, #8]                  
  0b556:  bl #0x97ca                        -> func_0x097ca
  0b55a:  movs r1, #1                       
  0b55c:  ldr r0, [sp, #8]                  
  0b55e:  bl #0x985c                        -> func_0x0985c
  0b562:  movs r0, #3                       
  0b564:  pop {r4}                          
  0b566:  ldr pc, [sp], #0x14               
  0b56a:  ldr r1, [pc, #0x10]               
  0b56c:  ldr r0, [sp, #8]                  
  0b56e:  bl #0x9794                        -> func_0x09794
  0b572:  cmp r0, #0                        
  0b574:  beq #0xb54a                       
  0b576:  movs r0, #0                       
  0b578:  b #0xb564                         -> 0x0b564 (вне списка функций)
  ; --- literal-пул @0x0b57c (1 слов) — ВНЕ границ функции ---
  0b57c:  .word 0x00030001
```
