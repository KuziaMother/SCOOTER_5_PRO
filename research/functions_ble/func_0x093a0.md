# func_0x093a0

| | |
|---|---|
| offset в файле | `0x093a0` |
| vaddr (база 0x01800000) | `0x018093a0` |
 | размер кода | 102 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200164 — RAM (r0)
- 0x00201240 — RAM (r6)
- 0x002012c4 — RAM (r8)
- 0x00203899 — RAM (r1)

## Вызовы (callees)

- 0x015fb4a8 (bl, вне списка функций)
- 0x015fd706 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  018093a0:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  018093a4:  mov sb, r0                        
  018093a6:  movs r4, #0                       
  018093a8:  sub.w r0, r3, #0xd500             
  018093ac:  mov r5, r2                        
  018093ae:  mov sl, r1                        
  018093b0:  subs r0, #0x37                    
  018093b2:  beq #0x18093be                    
  018093b4:  ldr r0, [pc, #0x50]               (RAM)
  018093b6:  ldrb.w r0, [r0, #0x237]           
  018093ba:  lsls r0, r0, #0x18                
  018093bc:  bpl #0x18093c0                    
  018093be:  movs r4, #1                       
  018093c0:  bl #0x15fb4a8                     
  018093c4:  ldr r6, [pc, #0x44]               (RAM)
  018093c6:  cbz r4, #0x18093d2                
  018093c8:  mov.w sb, #1                      
  018093cc:  subw r0, pc, #0x33                
  018093d0:  str r0, [r6]                      
  018093d2:  ldr.w r8, [pc, #0x3c]             (RAM)
  018093d6:  movs r7, #0                       
  018093d8:  mov r1, sl                        
  018093da:  mov r0, sb                        
  018093dc:  str.w r7, [r8]                    
  018093e0:  bl #0x15fd706                     
  018093e4:  str r0, [r5]                      
  018093e6:  cbz r4, #0x18093f8                
  018093e8:  str r7, [r6]                      
  018093ea:  ldr r0, [r5]                      
  018093ec:  cbnz r0, #0x18093f8               
  018093ee:  mov r1, sl                        
  018093f0:  movs r0, #0                       
  018093f2:  bl #0x15fd706                     
  018093f6:  str r0, [r5]                      
  018093f8:  ldr r1, [pc, #0x18]               (RAM)
  018093fa:  str.w r1, [r8]                    
  018093fe:  pop.w {r4, r5, r6, r7, r8, sb, sl, lr}
  01809402:  b.w #0x15fb3f2                    
  ; --- literal-пул @0x09408 (4 слов) — ВНЕ границ функции ---
  09408:  .word 0x00200164  ; RAM
  0940c:  .word 0x00201240  ; RAM
  09410:  .word 0x002012c4  ; RAM
  09414:  .word 0x00203899  ; RAM
```
