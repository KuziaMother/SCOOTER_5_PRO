# func_0x067a8

| | |
|---|---|
| offset в файле | `0x067a8` |
| vaddr (база 0x01800000) | `0x018067a8` |
 | размер кода | 74 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00201c50 — RAM (r5)
- 0x00201c54 — RAM (r4)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x08a72` (bl @0x01808a94)

## Дизассембляция

```asm
  018067a8:  push {r4, r5, r6, r7, lr}         
  018067aa:  ldr r5, [pc, #0x3f8]              (RAM)
  018067ac:  movs r3, #1                       
  018067ae:  lsls r3, r1                       
  018067b0:  ldr.w r2, [r5, r0, lsl #2]        
  018067b4:  tst r2, r3                        
  018067b6:  bne #0x18067f0                    
  018067b8:  ldr r4, [pc, #0x3ec]              (RAM)
  018067ba:  add.w r2, r4, r0, lsl #3          
  018067be:  ldrb r6, [r2, #7]                 
  018067c0:  ldrb r7, [r2, #4]                 
  018067c2:  cmp r6, r7                        
  018067c4:  beq #0x18067e6                    
  018067c6:  ldr.w r4, [r4, r0, lsl #3]        
  018067ca:  ldrb r6, [r2, #6]                 
  018067cc:  str.w r1, [r4, r6, lsl #2]        
  018067d0:  ldrb r1, [r2, #6]                 
  018067d2:  ldrb r4, [r2, #4]                 
  018067d4:  adds r1, r1, #1                   
  018067d6:  udiv r6, r1, r4                   
  018067da:  mls r1, r4, r6, r1                
  018067de:  strb r1, [r2, #6]                 
  018067e0:  ldrb r1, [r2, #7]                 
  018067e2:  adds r1, r1, #1                   
  018067e4:  strb r1, [r2, #7]                 
  018067e6:  ldr.w r1, [r5, r0, lsl #2]        
  018067ea:  orrs r1, r3                       
  018067ec:  str.w r1, [r5, r0, lsl #2]        
  018067f0:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x06ba4 (2 слов) — ВНЕ границ функции ---
  06ba4:  .word 0x00201c50  ; RAM
  06ba8:  .word 0x00201c54  ; RAM
```
