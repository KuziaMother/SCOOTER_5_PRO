# func_0x057a0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800057a0) | `0x000057a0` |
| размер кода | 80 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801d800 — flash-mirror @0x1d800 (r0)
- 0x200000d0 — RAM (r1)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x03b82` (0x00003b82, bl)
- `func_0x03c04` (0x00003c04, bl)
- 0x057dc (b, вне списка функций)
- `func_0x07fb8` (0x00007fb8, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  057a0:  push {r4, lr}                     
  057a2:  sub sp, #0x18                     
  057a4:  movs r4, #0                       
  057a6:  movs r1, #0x14                    
  057a8:  add r0, sp, #4                    
  057aa:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  057ae:  movs r2, #0x14                    
  057b0:  add r1, sp, #4                    
  057b2:  ldr r0, [pc, #0x3c]               -> flash-mirror @0x1d800
  057b4:  bl #0x7fb8                        -> func_0x07fb8
  057b8:  ldr r0, [sp, #0xc]                
  057ba:  cmp.w r0, #0x19800                
  057be:  bhs #0x57d8                       
  057c0:  movs r1, #0x12                    
  057c2:  add r0, sp, #4                    
  057c4:  bl #0x3b82                        -> func_0x03b82
  057c8:  ldr r1, [sp, #0x14]               
  057ca:  cmp.w r0, r1, lsr #16             
  057ce:  bne #0x57d8                       
  057d0:  ldr r0, [sp, #0xc]                
  057d2:  add.w r4, r0, #0x3000             
  057d6:  b #0x57dc                         -> 0x057dc (вне списка функций)
  057d8:  mov.w r4, #0x1c800                
  057dc:  movs r2, #0                       
  057de:  mov r1, r4                        
  057e0:  mov.w r0, #0x8000000              
  057e4:  bl #0x3c04                        -> func_0x03c04
  057e8:  ldr r1, [pc, #8]                  -> RAM
  057ea:  str r0, [r1]                      
  057ec:  add sp, #0x18                     
  057ee:  pop {r4, pc}                      
  ; --- literal-пул @0x057f0 (2 слов) — ВНЕ границ функции ---
  057f0:  .word 0x0801d800  ; flash-mirror @0x1d800
  057f4:  .word 0x200000d0  ; RAM
```
