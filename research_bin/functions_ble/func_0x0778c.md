# func_0x0778c

| | |
|---|---|
| offset в файле | `0x0778c` |
| vaddr (база 0x01800000) | `0x0180778c` |
 | размер кода | 132 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200814 — RAM (r0)
- 0x00200815 — RAM (r0)
- 0x0020672c — RAM (r0)
- 0x00206854 — RAM (r3)

## Вызовы (callees)

- 0x015f1b04 (bl, вне списка функций)
- 0x0161fdc0 (bl, вне списка функций)
- 0x0161fdde (bl, вне списка функций)
- `func_0x06d16` (0x01806d16, bl)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  0180778c:  push {r4, r5, r6, lr}             
  0180778e:  mov r4, r0                        
  01807790:  bl #0x15f1b04                     
  01807794:  cmp r4, #1                        
  01807796:  bne #0x180780e                    
  01807798:  ldr r0, [pc, #0x114]              (RAM)
  0180779a:  ldrb r0, [r0]                     
  0180779c:  cmp r0, #0                        
  0180779e:  bne #0x180780e                    
  018077a0:  ldr r0, [pc, #0x110]              (RAM)
  018077a2:  ldrb r4, [r0]                     
  018077a4:  cmp r4, #0xb                      
  018077a6:  beq #0x180780e                    
  018077a8:  sub.w r0, r4, #8                  
  018077ac:  uxtb r5, r0                       
  018077ae:  movs r1, #0x17                    
  018077b0:  mov r0, r4                        
  018077b2:  bl #0x161fdc0                     
  018077b6:  ldr r3, [pc, #0xcc]               (RAM)
  018077b8:  bic r2, r0, #0x2000               
  018077bc:  adds r3, #0x94                    
  018077be:  ldr.w r1, [r3, r5, lsl #2]        
  018077c2:  lsls r0, r1, #0xe                 
  018077c4:  bmi #0x18077ca                    
  018077c6:  lsls r0, r1, #0xf                 
  018077c8:  bpl #0x18077e2                    
  018077ca:  lsrs r0, r1, #0x11                
  018077cc:  bfi r2, r0, #0xe, #1              
  018077d0:  lsrs r0, r1, #0x10                
  018077d2:  bfi r2, r0, #0xf, #1              
  018077d6:  bic r0, r1, #0x30000              
  018077da:  bfi r2, r1, #0x10, #0x10          
  018077de:  str.w r0, [r3, r5, lsl #2]        
  018077e2:  movs r1, #0x17                    
  018077e4:  mov r0, r4                        
  018077e6:  bl #0x161fdde                     
  018077ea:  ldr r0, [pc, #0xcc]               (RAM)
  018077ec:  movs r1, #1                       
  018077ee:  lsls r1, r4                       
  018077f0:  ldrh r2, [r0]                     
  018077f2:  bics r2, r1                       
  018077f4:  strh r2, [r0]                     
  018077f6:  mov r0, r4                        
  018077f8:  bl #0x1806d16                     -> func_0x06d16
  018077fc:  ldr r0, [pc, #0x84]               (RAM)
  018077fe:  subs r0, #0x11                    
  01807800:  ldrb r0, [r0, r5]                 
  01807802:  cmp r0, #0                        
  01807804:  beq #0x180780e                    
  01807806:  pop.w {r4, r5, r6, lr}            
  0180780a:  b.w #0x1621bc6                    
  0180780e:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x07884 (1 слов) — ВНЕ границ функции ---
  07884:  .word 0x00206854  ; RAM
  ; --- literal-пул @0x078b0 (3 слов) — ВНЕ границ функции ---
  078b0:  .word 0x00200814  ; RAM
  078b4:  .word 0x00200815  ; RAM
  078b8:  .word 0x0020672c  ; RAM
```
