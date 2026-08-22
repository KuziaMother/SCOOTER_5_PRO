# func_0x0c5b0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c5b0) | `0x0000c5b0` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40021000 — периферия (r5)
- 0xf7c0ffff — прочее (r5)

## Вызовы (callees)

- 0x0c5e0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0c5b0:  push {r4, r5, lr}                 
  0c5b2:  mov r3, r1                        
  0c5b4:  mov r4, r2                        
  0c5b6:  movs r1, #0                       
  0c5b8:  movs r2, #0                       
  0c5ba:  ldr r5, [pc, #0x2c]               -> периферия
  0c5bc:  ldr r1, [r5, #4]                  
  0c5be:  ldr r2, [r5, #0x40]               
  0c5c0:  ldr r5, [pc, #0x28]               
  0c5c2:  ands r1, r5                       
  0c5c4:  bic r2, r2, #3                    
  0c5c8:  cbz r0, #0xc5ce                   
  0c5ca:  cmp r0, #1                        
  0c5cc:  bne #0xc5d8                       
  0c5ce:  orrs r1, r3                       
  0c5d0:  orr.w r5, r0, r4                  
  0c5d4:  orrs r2, r5                       
  0c5d6:  b #0xc5e0                         -> 0x0c5e0 (вне списка функций)
  0c5d8:  orr.w r5, r0, r3                  
  0c5dc:  orrs r1, r5                       
  0c5de:  orrs r2, r4                       
  0c5e0:  ldr r5, [pc, #4]                  -> периферия
  0c5e2:  str r1, [r5, #4]                  
  0c5e4:  str r2, [r5, #0x40]               
  0c5e6:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x0c5e8 (2 слов) — ВНЕ границ функции ---
  0c5e8:  .word 0x40021000  ; периферия
  0c5ec:  .word 0xf7c0ffff
```
