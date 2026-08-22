# func_0x0798e

| | |
|---|---|
| offset в файле | `0x0798e` |
| vaddr (база 0x01800000) | `0x0180798e` |
 | размер кода | 122 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00201d50 — RAM (r0)
- 0x00202044 — RAM (r7)
- 0x21600002 — прочее (r0)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x0162b5d4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  0180798e:  push {r2, r3, r4, r5, r7, lr}     
  01807990:  ldr r7, [pc, #0x330]              (RAM)
  01807992:  uxtb r5, r0                       
  01807994:  add.w r0, r7, r5, lsl #2          
  01807998:  ldr.w r4, [r0, #0x210]            
  0180799c:  ldr r0, [r4]                      
  0180799e:  lsls r1, r0, #6                   
  018079a0:  bmi #0x1807a06                    
  018079a2:  lsls r0, r0, #7                   
  018079a4:  bpl #0x1807a06                    
  018079a6:  mov r3, r5                        
  018079a8:  movs r2, #1                       
  018079aa:  mov.w r1, #0x460                  
  018079ae:  ldr r0, [pc, #0x320]              
  018079b0:  bl #0x15f5b92                     
  018079b4:  adr r0, #0x31c                    
  018079b6:  ldrd r1, r0, [r0]                 
  018079ba:  strd r1, r0, [sp]                 
  018079be:  movs r1, #0                       
  018079c0:  strb.w r1, [r4, #0x37]            
  018079c4:  ldr r2, [sp]                      
  018079c6:  str r2, [r4, #0x38]               
  018079c8:  ldrh.w r2, [sp, #4]               
  018079cc:  strh r2, [r4, #0x3c]              
  018079ce:  movs r0, #6                       
  018079d0:  strh r0, [r4, #0x2c]              
  018079d2:  strh r1, [r4, #0x30]              
  018079d4:  strh r1, [r4, #0x34]              
  018079d6:  strh r1, [r4, #0x2e]              
  018079d8:  ldrh r2, [r7, #4]                 
  018079da:  lsls r2, r2, #0x16                
  018079dc:  bpl #0x18079e0                    
  018079de:  mov r1, r0                        
  018079e0:  movw r0, #0x26f                   
  018079e4:  mov r3, r6                        
  018079e6:  bfi r3, r0, #0, #0x10             
  018079ea:  ldr r0, [pc, #0x2f0]              (RAM)
  018079ec:  str r4, [sp]                      
  018079ee:  bfi r1, r5, #5, #4                
  018079f2:  mov r2, r4                        
  018079f4:  ldr r0, [r0]                      
  018079f6:  bl #0x162b5d4                     
  018079fa:  mov r0, r5                        
  018079fc:  pop.w {r2, r3, r4, r5, r7, lr}    
  01807a00:  movs r1, #0                       
  01807a02:  b.w #0x161e8ca                    
  01807a06:  pop {r2, r3, r4, r5, r7, pc}      
  ; --- literal-пул @0x07cc4 (1 слов) — ВНЕ границ функции ---
  07cc4:  .word 0x00202044  ; RAM
  ; --- literal-пул @0x07cd0 (1 слов) — ВНЕ границ функции ---
  07cd0:  .word 0x21600002
  ; --- literal-пул @0x07cdc (1 слов) — ВНЕ границ функции ---
  07cdc:  .word 0x00201d50  ; RAM
```
