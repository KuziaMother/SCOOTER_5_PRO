# func_0x0c2a8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c2a8) | `0x0000c2a8` |
| размер кода | 84 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40007000 — периферия (r3)
- 0xe000ed10 — Cortex-M (NVIC/SCB/SysTick) (r3)

## Вызовы (callees)

- 0x0c2ee (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x05cd0` (bl @0x00005d2a)


## Дизассембляция

```asm
  0c2a8:  push {r4, lr}                     
  0c2aa:  mov r2, r0                        
  0c2ac:  movs r0, #0                       
  0c2ae:  nop                               
  0c2b0:  ldr r3, [pc, #0x48]               -> периферия
  0c2b2:  ldr r3, [r3, #0x10]               
  0c2b4:  and r3, r3, #2                    
  0c2b8:  cmp r3, #2                        
  0c2ba:  bne #0xc2b0                       
  0c2bc:  ldr r3, [pc, #0x3c]               -> периферия
  0c2be:  ldr r0, [r3, #8]                  
  0c2c0:  bic r0, r0, #0x3000               
  0c2c4:  orrs r0, r1                       
  0c2c6:  str r0, [r3, #8]                  
  0c2c8:  ldr r0, [r3]                      
  0c2ca:  bic r0, r0, #7                    
  0c2ce:  orr r0, r0, #2                    
  0c2d2:  str r0, [r3]                      
  0c2d4:  ldr r3, [pc, #0x28]               -> Cortex-M (NVIC/SCB/SysTick)
  0c2d6:  ldr r3, [r3]                      
  0c2d8:  orr r3, r3, #4                    
  0c2dc:  ldr r4, [pc, #0x20]               -> Cortex-M (NVIC/SCB/SysTick)
  0c2de:  str r3, [r4]                      
  0c2e0:  cmp r2, #1                        
  0c2e2:  bne #0xc2e8                       
  0c2e4:  wfi                               
  0c2e6:  b #0xc2ee                         -> 0x0c2ee (вне списка функций)
  0c2e8:  sev                               
  0c2ea:  wfe                               
  0c2ec:  wfe                               
  0c2ee:  ldr r3, [pc, #0x10]               -> Cortex-M (NVIC/SCB/SysTick)
  0c2f0:  ldr r3, [r3]                      
  0c2f2:  bic r3, r3, #4                    
  0c2f6:  ldr r4, [pc, #8]                  -> Cortex-M (NVIC/SCB/SysTick)
  0c2f8:  str r3, [r4]                      
  0c2fa:  pop {r4, pc}                      
  ; --- literal-пул @0x0c2fc (2 слов) — ВНЕ границ функции ---
  0c2fc:  .word 0x40007000  ; периферия
  0c300:  .word 0xe000ed10  ; Cortex-M (NVIC/SCB/SysTick)
```
