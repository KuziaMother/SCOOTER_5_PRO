# func_0x0218c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000218c) | `0x0000218c` |
| размер кода | 76 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b42 — RAM (r0)

## Вызовы (callees)

- `func_0x01c7a` (0x00001c7a, bl)
- 0x021b6 (b, вне списка функций)
- 0x021d4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08afc` (bl @0x00008afe)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x021b2..0x021b8` (6 Б); цели из: 0x021a8
- `0x021b8..0x021d4` (28 Б); цели из: 0x021b0
- `0x021d4..0x021d8` (4 Б); цели из: 0x021d0

## Дизассембляция

```asm
  0218c:  push {r3, r4, r5, lr}             
  0218e:  movs r5, #1                       
  02190:  movs r4, #0                       
  02192:  movs r3, #2                       
  02194:  mov r2, sp                        
  02196:  movs r1, #0x83                    
  02198:  movs r0, #8                       
  0219a:  bl #0x1c7a                        -> func_0x01c7a
  0219e:  ands r5, r0                       
  021a0:  cbz r5, #0x21d2                   
  021a2:  ldrb.w r0, [sp]                   
  021a6:  cmp r0, #0xff                     
  021a8:  beq #0x21b2                       
  021aa:  ldrb.w r0, [sp, #1]               
  021ae:  cmp r0, #0xff                     
  021b0:  bne #0x21b8                       
  021b2:  ldr r0, [pc, #0x24]               -> RAM
  021b4:  ldrh r0, [r0]                     
  021b6:  pop {r3, r4, r5, pc}              
  021b8:  ldrb.w r0, [sp]                   
  021bc:  orrs r4, r0                       
  021be:  ldrb.w r0, [sp, #1]               
  021c2:  mov.w r1, #0xff00                 
  021c6:  and.w r0, r1, r0, lsl #8          
  021ca:  orrs r4, r0                       
  021cc:  ldr r0, [pc, #8]                  -> RAM
  021ce:  strh r4, [r0]                     
  021d0:  b #0x21d4                         -> 0x021d4 (вне списка функций)
  021d2:  movs r4, #0                       
  021d4:  mov r0, r4                        
  021d6:  b #0x21b6                         -> 0x021b6 (вне списка функций)
  ; --- literal-пул @0x021d8 (1 слов) — ВНЕ границ функции ---
  021d8:  .word 0x20000b42  ; RAM
```
