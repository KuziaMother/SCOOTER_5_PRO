# func_0x0799c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000799c) | `0x0000799c` |
| размер кода | 144 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xffffd8f0 — прочее (r1)

## Вызовы (callees)

- 0x07a12 (b, вне списка функций)
- `func_0x08f58` (0x00008f58, bl)
- `func_0x0e160` (0x0000e160, bl)
- 0x11010 (bl, вне списка функций)
- 0x110cc (bl, вне списка функций)
- `func_0x16222` (0x00016222, bl)
- `func_0x162ce` (0x000162ce, bl)
- 0x164f8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e658` (bl @0x0000e6a6)


## Дизассембляция

```asm
  0799c:  push {r3, r4, r5, r6, r7, lr}     
  0799e:  movs r0, #1                       
  079a0:  bl #0x11010                       -> 0x11010 (вне списка функций)
  079a4:  bl #0x8f58                        -> func_0x08f58
  079a8:  mov r4, r0                        
  079aa:  mov r1, sp                        
  079ac:  bl #0xe160                        -> func_0x0e160
  079b0:  movs r0, #0                       
  079b2:  bl #0x11010                       -> 0x11010 (вне списка функций)
  079b6:  movw r1, #0x2710                  
  079ba:  movs r0, #0                       
  079bc:  bl #0x16222                       -> func_0x16222
  079c0:  ldr r1, [sp]                      
  079c2:  subs r4, r1, r0                   
  079c4:  bl #0x164f8                       -> 0x164f8 (вне списка функций)
  079c8:  movw r1, #0x2710                  
  079cc:  subs r0, r1, r0                   
  079ce:  movw r1, #0x98b                   
  079d2:  mul r6, r0, r1                    
  079d6:  movw r1, #0x2710                  
  079da:  mov r0, r6                        
  079dc:  bl #0x16222                       -> func_0x16222
  079e0:  ldr r1, [sp]                      
  079e2:  subs r0, r1, r0                   
  079e4:  movw r1, #0x2710                  
  079e8:  mul r5, r0, r1                    
  079ec:  mov r1, r4                        
  079ee:  mov r0, r5                        
  079f0:  bl #0x162ce                       -> func_0x162ce
  079f4:  str r0, [sp]                      
  079f6:  movw r1, #0x2710                  
  079fa:  ldr r0, [sp]                      
  079fc:  cmp r0, r1                        
  079fe:  ble #0x7a06                       
  07a00:  mov r0, r1                        
  07a02:  str r0, [sp]                      
  07a04:  b #0x7a12                         -> 0x07a12 (вне списка функций)
  07a06:  ldr r1, [pc, #0x24]               
  07a08:  ldr r0, [sp]                      
  07a0a:  cmp r0, r1                        
  07a0c:  bge #0x7a12                       
  07a0e:  mov r0, r1                        
  07a10:  str r0, [sp]                      
  07a12:  movw r2, #0x2710                  
  07a16:  ldr r1, [sp]                      
  07a18:  mul r0, r1, r2                    
  07a1c:  mov r1, r2                        
  07a1e:  bl #0x16222                       -> func_0x16222
  07a22:  sxth r4, r0                       
  07a24:  mov r0, r4                        
  07a26:  bl #0x110cc                       -> 0x110cc (вне списка функций)
  07a2a:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x07a2c (1 слов) — ВНЕ границ функции ---
  07a2c:  .word 0xffffd8f0
```
