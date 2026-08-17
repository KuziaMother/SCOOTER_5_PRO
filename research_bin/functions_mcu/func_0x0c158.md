# func_0x0c158

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c158) | `0x0000c158` |
| размер кода | 164 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a80 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x01bdc` (0x00001bdc, bl)
- `func_0x0280c` (0x0000280c, bl)
- 0x0c1f2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0c158:  push {r4, r5, lr}                 
  0c15a:  sub sp, #0x24                     
  0c15c:  movs r1, #0x20                    
  0c15e:  add r0, sp, #4                    
  0c160:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0c164:  movs r5, #1                       
  0c166:  movs r4, #0                       
  0c168:  b #0xc1f2                         -> 0x0c1f2 (вне списка функций)
  0c16a:  ldr r0, [pc, #0x90]               -> RAM
  0c16c:  add.w r0, r0, r4, lsl #3          
  0c170:  movs r2, #0x20                    
  0c172:  ldr r1, [r0, #4]                  
  0c174:  add r0, sp, #4                    
  0c176:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0c17a:  movs r0, #0x90                    
  0c17c:  bl #0x1bdc                        -> func_0x01bdc
  0c180:  ands r5, r0                       
  0c182:  mov.w r0, #0x3e8                  
  0c186:  str r0, [sp]                      
  0c188:  nop                               
  0c18a:  ldr r0, [sp]                      
  0c18c:  subs r1, r0, #1                   
  0c18e:  str r1, [sp]                      
  0c190:  cmp r0, #0                        
  0c192:  bne #0xc18a                       
  0c194:  movs r0, #0x1e                    
  0c196:  str r0, [sp]                      
  0c198:  ldr r0, [pc, #0x60]               -> RAM
  0c19a:  ldrh.w r2, [r0, r4, lsl #3]       
  0c19e:  add r3, sp, #4                    
  0c1a0:  movs r1, #8                       
  0c1a2:  movs r0, #0                       
  0c1a4:  bl #0x280c                        -> func_0x0280c
  0c1a8:  mov r5, r0                        
  0c1aa:  cmp r5, #1                        
  0c1ac:  beq #0xc1d4                       
  0c1ae:  mov.w r0, #0x3e8                  
  0c1b2:  str r0, [sp]                      
  0c1b4:  nop                               
  0c1b6:  ldr r0, [sp]                      
  0c1b8:  subs r1, r0, #1                   
  0c1ba:  str r1, [sp]                      
  0c1bc:  cmp r0, #0                        
  0c1be:  bne #0xc1b6                       
  0c1c0:  movs r0, #0x1e                    
  0c1c2:  str r0, [sp]                      
  0c1c4:  ldr r0, [pc, #0x34]               -> RAM
  0c1c6:  ldrh.w r2, [r0, r4, lsl #3]       
  0c1ca:  add r3, sp, #4                    
  0c1cc:  movs r1, #8                       
  0c1ce:  movs r0, #0                       
  0c1d0:  bl #0x280c                        -> func_0x0280c
  0c1d4:  movs r0, #0x92                    
  0c1d6:  bl #0x1bdc                        -> func_0x01bdc
  0c1da:  ands r5, r0                       
  0c1dc:  mov.w r0, #0x3e8                  
  0c1e0:  str r0, [sp]                      
  0c1e2:  nop                               
  0c1e4:  ldr r0, [sp]                      
  0c1e6:  subs r1, r0, #1                   
  0c1e8:  str r1, [sp]                      
  0c1ea:  cmp r0, #0                        
  0c1ec:  bne #0xc1e4                       
  0c1ee:  adds r0, r4, #1                   
  0c1f0:  uxtb r4, r0                       
  0c1f2:  cmp r4, #9                        
  0c1f4:  blo #0xc16a                       
  0c1f6:  movs r0, #1                       
  0c1f8:  add sp, #0x24                     
  0c1fa:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x0c1fc (1 слов) — ВНЕ границ функции ---
  0c1fc:  .word 0x20000a80  ; RAM
```
