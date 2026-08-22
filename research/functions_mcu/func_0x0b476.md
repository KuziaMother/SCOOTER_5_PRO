# func_0x0b476

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b476) | `0x0000b476` |
| размер кода | 80 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00070084 — прочее (r1)

## Вызовы (callees)

- `func_0x09794` (0x00009794, bl)
- `func_0x097ca` (0x000097ca, bl)
- `func_0x0985c` (0x0000985c, bl)
- `func_0x099ce` (0x000099ce, bl)
- 0x0b4ac (b, вне списка функций)
- 0x0b4b2 (b, вне списка функций)
- 0x0b4be (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0b476:  push {r4, r5, r6, lr}             
  0b478:  ldrd r4, r5, [sp, #0x44]          
  0b47c:  b #0xb4be                         -> 0x0b4be (вне списка функций)
  0b47e:  ldrb r1, [r4]                     
  0b480:  ldr r0, [sp, #0x10]               
  0b482:  bl #0x99ce                        -> func_0x099ce
  0b486:  adds r4, r4, #1                   
  0b488:  subs r0, r5, #1                   
  0b48a:  uxtb r5, r0                       
  0b48c:  mov.w r6, #0x10000                
  0b490:  b #0xb4b2                         -> 0x0b4b2 (вне списка функций)
  0b492:  subs r0, r6, #0                   
  0b494:  sub.w r6, r6, #1                  
  0b498:  bne #0xb4b2                       
  0b49a:  movs r1, #0                       
  0b49c:  ldr r0, [sp, #0x10]               
  0b49e:  bl #0x97ca                        -> func_0x097ca
  0b4a2:  movs r1, #1                       
  0b4a4:  ldr r0, [sp, #0x10]               
  0b4a6:  bl #0x985c                        -> func_0x0985c
  0b4aa:  movs r0, #3                       
  0b4ac:  pop {r4, r5, r6}                  
  0b4ae:  ldr pc, [sp], #0x14               
  0b4b2:  ldr r1, [pc, #0x14]               
  0b4b4:  ldr r0, [sp, #0x10]               
  0b4b6:  bl #0x9794                        -> func_0x09794
  0b4ba:  cmp r0, #0                        
  0b4bc:  beq #0xb492                       
  0b4be:  cmp r5, #0                        
  0b4c0:  bgt #0xb47e                       
  0b4c2:  movs r0, #0                       
  0b4c4:  b #0xb4ac                         -> 0x0b4ac (вне списка функций)
  ; --- literal-пул @0x0b4c8 (1 слов) — ВНЕ границ функции ---
  0b4c8:  .word 0x00070084
```
