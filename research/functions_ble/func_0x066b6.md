# func_0x066b6

| | |
|---|---|
| offset в файле | `0x066b6` |
| vaddr (база 0x01800000) | `0x018066b6` |
 | размер кода | 56 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200164 — RAM (r0)

## Вызовы (callees)

- 0x015ff3d8 (bl, вне списка функций)
- `func_0x065f6` (0x018065f6, b)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  018066b6:  push {r2, r3, r4, lr}             
  018066b8:  ldr r0, [pc, #0xd8]               (RAM)
  018066ba:  ldrb.w r0, [r0, #0x1e8]           
  018066be:  and r0, r0, #3                    
  018066c2:  cmp r0, #2                        
  018066c4:  bne #0x18066e8                    
  018066c6:  movs r4, #0                       
  018066c8:  movs r3, #1                       
  018066ca:  str r4, [sp]                      
  018066cc:  mov r2, r3                        
  018066ce:  mov r1, r3                        
  018066d0:  movs r0, #0xb                     
  018066d2:  str r4, [sp, #4]                  
  018066d4:  bl #0x15ff3d8                     
  018066d8:  movs r3, #1                       
  018066da:  str r4, [sp]                      
  018066dc:  mov r2, r3                        
  018066de:  mov r1, r3                        
  018066e0:  movs r0, #0xc                     
  018066e2:  str r4, [sp, #4]                  
  018066e4:  bl #0x15ff3d8                     
  018066e8:  pop.w {r2, r3, r4, lr}            
  018066ec:  b #0x18065f6                      -> func_0x065f6
  ; --- literal-пул @0x06794 (1 слов) — ВНЕ границ функции ---
  06794:  .word 0x00200164  ; RAM
```
