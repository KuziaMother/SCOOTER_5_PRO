# func_0x012ac

| | |
|---|---|
| offset в файле | `0x012ac` |
| vaddr (база 0x01800000) | `0x018012ac` |
 | размер кода | 174 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005bc — RAM (r7)
- 0x002005ec — RAM (r6)
- 0x00200950 — RAM (r0)
- 0x00201e20 — RAM (r0)
- 0x00206838 — RAM (r0)

## Вызовы (callees)

- 0x018012fc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0135a` (bl @0x018013de)

## Дизассембляция

```asm
  018012ac:  push.w {r4, r5, r6, r7, r8, lr}   
  018012b0:  mov r4, r0                        
  018012b2:  ldrb r0, [r0, #3]                 
  018012b4:  ldr r7, [pc, #0x38c]              (RAM)
  018012b6:  mov.w r6, #0x40000000             
  018012ba:  mov.w r8, #0x1000                 
  018012be:  cmp r0, #1                        
  018012c0:  beq #0x18012da                    
  018012c2:  ldr r2, [r7]                      
  018012c4:  mov r1, r8                        
  018012c6:  movs r0, #0                       
  018012c8:  blx r2                            
  018012ca:  ldr.w r0, [r6, #0x2e8]            
  018012ce:  bic r0, r0, #2                    
  018012d2:  str.w r0, [r6, #0x2e8]            
  018012d6:  pop.w {r4, r5, r6, r7, r8, pc}    
  018012da:  ldr r0, [pc, #0x36c]              (RAM)
  018012dc:  ldr r0, [r0]                      
  018012de:  blx r0                            
  018012e0:  ldrb r0, [r4, #2]                 
  018012e2:  movs r5, #0                       
  018012e4:  cmp r0, #4                        
  018012e6:  beq #0x18012ee                    
  018012e8:  cmp r0, #3                        
  018012ea:  beq #0x18012fa                    
  018012ec:  b #0x18012fc                      -> 0x012fc (вне списка функций)
  018012ee:  ldrb r0, [r4, #6]                 
  018012f0:  cbz r0, #0x18012fa                
  018012f2:  ldrb r0, [r4, #4]                 
  018012f4:  lsls r0, r0, #0x19                
  018012f6:  lsrs r5, r0, #0x18                
  018012f8:  b #0x18012fc                      -> 0x012fc (вне списка функций)
  018012fa:  ldrb r5, [r4, #4]                 
  018012fc:  ldrb r4, [r4, #5]                 
  018012fe:  ldr r0, [pc, #0x34c]              (RAM)
  01801300:  cbz r4, #0x1801308                
  01801302:  ldrb r1, [r0, #6]                 
  01801304:  cmp r1, r4                        
  01801306:  bhs #0x180130a                    
  01801308:  ldrb r4, [r0, #6]                 
  0180130a:  ldr.w r0, [r6, #0x2e8]            
  0180130e:  orr r0, r0, #2                    
  01801312:  str.w r0, [r6, #0x2e8]            
  01801316:  ldr r2, [r7]                      
  01801318:  mov r1, r8                        
  0180131a:  movs r0, #0                       
  0180131c:  blx r2                            
  0180131e:  ldr r6, [pc, #0x330]              (RAM)
  01801320:  movs r2, #0                       
  01801322:  movs r1, #0x80                    
  01801324:  ldr r3, [r6]                      
  01801326:  movs r0, #0x3f                    
  01801328:  blx r3                            
  0180132a:  movs r1, #0x7f                    
  0180132c:  ldr r3, [r6]                      
  0180132e:  and r2, r5, #0x7f                 
  01801332:  movs r0, #0x3f                    
  01801334:  blx r3                            
  01801336:  lsls r2, r4, #8                   
  01801338:  ldr r3, [r6]                      
  0180133a:  mov.w r1, #0xf000                 
  0180133e:  movs r0, #2                       
  01801340:  blx r3                            
  01801342:  ldr r2, [r7]                      
  01801344:  pop.w {r4, r5, r6, r7, r8, lr}    
  01801348:  mov.w r1, #0x2000                 
  0180134c:  movs r0, #0                       
  0180134e:  bx r2                             
  01801350:  ldrb r1, [r0, #3]                 
  01801352:  ldr r0, [pc, #0x2e4]              (RAM)
  01801354:  strb r1, [r0, #4]                 
  01801356:  movs r0, #0                       
  01801358:  bx lr                             
  ; --- literal-пул @0x01638 (1 слов) — ВНЕ границ функции ---
  01638:  .word 0x00206838  ; RAM
  ; --- literal-пул @0x01644 (4 слов) — ВНЕ границ функции ---
  01644:  .word 0x002005bc  ; RAM
  01648:  .word 0x00200950  ; RAM
  0164c:  .word 0x00201e20  ; RAM
  01650:  .word 0x002005ec  ; RAM
```
