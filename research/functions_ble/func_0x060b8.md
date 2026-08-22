# func_0x060b8

| | |
|---|---|
| offset в файле | `0x060b8` |
| vaddr (база 0x01800000) | `0x018060b8` |
 | размер кода | 44 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00206970 — RAM (r4)
- 0x20201f60 — RAM (r4)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  018060b8:  push {r4, r5, lr}                 
  018060ba:  ldr r4, [pc, #0x20]               (RAM)
  018060bc:  pop {r5}                          
  018060be:  str r5, [r4]                      
  018060c0:  pop {r5}                          
  018060c2:  str r5, [r4, #4]                  
  018060c4:  pop {r5}                          
  018060c6:  str r5, [r4, #8]                  
  018060c8:  ldr r4, [pc, #0x14]               (RAM)
  018060ca:  ldr r4, [r4, #0x10]               
  018060cc:  cbz r4, #0x18060d0                
  018060ce:  blx r4                            
  018060d0:  ldr r2, [pc, #8]                  (RAM)
  018060d2:  ldr r4, [r2]                      
  018060d4:  ldr r5, [r2, #4]                  
  018060d6:  ldr r3, [r2, #8]                  
  018060d8:  bx r3                             
  018060da:  movs r0, r0                       
  018060dc:  subs r0, r4, #5                   
  018060de:  movs r0, #0x20                    
  018060e0:  ldr r0, [r6, #0x14]               
  018060e2:  movs r0, r4                       
  ; --- literal-пул @0x060dc (2 слов) ---
  060dc:  .word 0x20201f60  ; RAM
  060e0:  .word 0x00206970  ; RAM
```
