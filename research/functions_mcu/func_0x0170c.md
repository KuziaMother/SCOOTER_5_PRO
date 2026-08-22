# func_0x0170c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000170c) | `0x0000170c` |
| размер кода | 68 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b7e — RAM (r0)
- 0x20000b84 — RAM (r0)
- 0x20001f02 — RAM (r1)

## Вызовы (callees)

- 0x0171a (b, вне списка функций)
- 0x01730 (b, вне списка функций)
- `func_0x05044` (0x00005044, bl)
- `func_0x0506a` (0x0000506a, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03780` (bl @0x00003798)
- `func_0x08b10` (bl @0x00008b14)
- `func_0x08b58` (bl @0x00008b5c)


## Дизассембляция

```asm
  0170c:  push {r4, r5, r6, lr}             
  0170e:  mov r4, r0                        
  01710:  movs r5, #0                       
  01712:  cmp r4, #2                        
  01714:  blt #0x171c                       
  01716:  ldr r0, [pc, #0x38]               -> RAM
  01718:  ldrh r0, [r0]                     
  0171a:  pop {r4, r5, r6, pc}              
  0171c:  movs r5, #0                       
  0171e:  b #0x1730                         -> 0x01730 (вне списка функций)
  01720:  ldr r0, [pc, #0x30]               -> RAM
  01722:  ldrh.w r0, [r0, r4, lsl #1]       
  01726:  ldr r1, [pc, #0x30]               -> RAM
  01728:  strh.w r0, [r1, r5, lsl #1]       
  0172c:  adds r0, r5, #1                   
  0172e:  uxtb r5, r0                       
  01730:  cmp r5, #7                        
  01732:  blt #0x1720                       
  01734:  movs r1, #5                       
  01736:  ldr r0, [pc, #0x20]               -> RAM
  01738:  bl #0x506a                        -> func_0x0506a
  0173c:  movs r2, #3                       
  0173e:  movs r1, #2                       
  01740:  ldr r0, [pc, #0x14]               -> RAM
  01742:  bl #0x5044                        -> func_0x05044
  01746:  ldr r1, [pc, #8]                  -> RAM
  01748:  strh r0, [r1]                     
  0174a:  mov r0, r1                        
  0174c:  ldrh r0, [r0]                     
  0174e:  b #0x171a                         -> 0x0171a (вне списка функций)
  ; --- literal-пул @0x01750 (3 слов) — ВНЕ границ функции ---
  01750:  .word 0x20000b84  ; RAM
  01754:  .word 0x20000b7e  ; RAM
  01758:  .word 0x20001f02  ; RAM
```
