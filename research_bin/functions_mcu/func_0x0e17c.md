# func_0x0e17c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e17c) | `0x0000e17c` |
| размер кода | 128 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xffffd8f0 — прочее (r1)

## Вызовы (callees)

- `func_0x0e160` (0x0000e160, bl)
- 0x0e1e4 (b, вне списка функций)
- `func_0x16222` (0x00016222, bl)
- `func_0x162ce` (0x000162ce, bl)

## Кто вызывает (callers / xrefs)

- `func_0x063b8` (bl @0x0000654e)
- `func_0x06fc0` (bl @0x0000700c)


## Дизассембляция

```asm
  0e17c:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  0e180:  mov r4, r0                        
  0e182:  mov r5, r1                        
  0e184:  mov r6, r2                        
  0e186:  mov r1, sp                        
  0e188:  mov r0, r5                        
  0e18a:  bl #0xe160                        -> func_0x0e160
  0e18e:  movw r1, #0x2710                  
  0e192:  movs r0, #0                       
  0e194:  bl #0x16222                       -> func_0x16222
  0e198:  ldr r1, [sp]                      
  0e19a:  subs r7, r1, r0                   
  0e19c:  movw r1, #0x2710                  
  0e1a0:  subs r1, r1, r4                   
  0e1a2:  movw r2, #0x98b                   
  0e1a6:  mul r0, r1, r2                    
  0e1aa:  movw r1, #0x2710                  
  0e1ae:  bl #0x16222                       -> func_0x16222
  0e1b2:  ldr r1, [sp]                      
  0e1b4:  subs r0, r1, r0                   
  0e1b6:  movw r1, #0x2710                  
  0e1ba:  mul r8, r0, r1                    
  0e1be:  mov r1, r7                        
  0e1c0:  mov r0, r8                        
  0e1c2:  bl #0x162ce                       -> func_0x162ce
  0e1c6:  str r0, [sp]                      
  0e1c8:  movw r1, #0x2710                  
  0e1cc:  ldr r0, [sp]                      
  0e1ce:  cmp r0, r1                        
  0e1d0:  ble #0xe1d8                       
  0e1d2:  mov r0, r1                        
  0e1d4:  str r0, [sp]                      
  0e1d6:  b #0xe1e4                         -> 0x0e1e4 (вне списка функций)
  0e1d8:  ldr r1, [pc, #0x20]               
  0e1da:  ldr r0, [sp]                      
  0e1dc:  cmp r0, r1                        
  0e1de:  bge #0xe1e4                       
  0e1e0:  mov r0, r1                        
  0e1e2:  str r0, [sp]                      
  0e1e4:  movw r2, #0x2710                  
  0e1e8:  ldr r1, [sp]                      
  0e1ea:  mul r0, r1, r2                    
  0e1ee:  mov r1, r2                        
  0e1f0:  bl #0x16222                       -> func_0x16222
  0e1f4:  sxth r0, r0                       
  0e1f6:  strh r0, [r6]                     
  0e1f8:  pop.w {r3, r4, r5, r6, r7, r8, sb, pc}
  ; --- literal-пул @0x0e1fc (1 слов) — ВНЕ границ функции ---
  0e1fc:  .word 0xffffd8f0
```
