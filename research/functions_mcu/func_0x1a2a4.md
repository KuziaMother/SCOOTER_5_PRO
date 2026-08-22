# func_0x1a2a4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a2a4) | `0x0001a2a4` |
| размер кода | 90 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000102 — RAM (r0)
- 0x20000218 — RAM (r2)
- 0x2000021e — RAM (r1)
- 0x20000245 — RAM (r0)
- 0x20000246 — RAM (r0)
- 0x20000247 — RAM (r0)
- 0x40012c00 — периферия (r0)

## Вызовы (callees)

- 0x1a2f0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1a2a4:  push {r4, r5, lr}                 
  1a2a6:  ldr r0, [pc, #0x58]               -> периферия
  1a2a8:  ldr r1, [r0, #0x1c]               
  1a2aa:  lsls r1, r1, #0x18                
  1a2ac:  bpl #0x1a2f4                      
  1a2ae:  ldr r1, [pc, #0x50]               -> периферия
  1a2b0:  adds r1, #0x40                    
  1a2b2:  ldr r2, [r1, #0x14]               
  1a2b4:  movs r3, #1                       
  1a2b6:  lsls r3, r3, #0xf                 
  1a2b8:  bics r2, r3                       
  1a2ba:  str r2, [r1, #0x14]               
  1a2bc:  ldr r2, [pc, #0x44]               -> RAM
  1a2be:  movs r1, #0                       
  1a2c0:  strb r1, [r2]                     
  1a2c2:  ldr r2, [r0, #0x20]               
  1a2c4:  movs r3, #0x80                    
  1a2c6:  orrs r2, r3                       
  1a2c8:  str r2, [r0, #0x20]               
  1a2ca:  ldr r0, [pc, #0x3c]               -> RAM
  1a2cc:  movs r4, #1                       
  1a2ce:  strb r4, [r0]                     
  1a2d0:  ldr r0, [pc, #0x38]               -> RAM
  1a2d2:  strb r1, [r0]                     
  1a2d4:  ldr r0, [pc, #0x38]               -> RAM
  1a2d6:  ldr r1, [pc, #0x40]               -> RAM
  1a2d8:  ldrb r5, [r0]                     
  1a2da:  ldr r0, [pc, #0x38]               -> RAM
  1a2dc:  ldrh r2, [r1]                     
  1a2de:  ldrb r3, [r0]                     
  1a2e0:  cmp r5, #0                        
  1a2e2:  beq #0x1a2f6                      
  1a2e4:  cmp r5, #2                        
  1a2e6:  bne #0x1a2f4                      
  1a2e8:  movs r4, #2                       
  1a2ea:  orrs r3, r4                       
  1a2ec:  strb r3, [r0]                     
  1a2ee:  lsls r0, r4, #0xc                 
  1a2f0:  orrs r2, r0                       
  1a2f2:  strh r2, [r1]                     
  1a2f4:  pop {r4, r5, pc}                  
  1a2f6:  orrs r3, r4                       
  1a2f8:  strb r3, [r0]                     
  1a2fa:  movs r0, #8                       
  1a2fc:  b #0x1a2f0                        -> 0x1a2f0 (вне списка функций)
  ; --- literal-пул @0x1a300 (7 слов) — ВНЕ границ функции ---
  1a300:  .word 0x40012c00  ; периферия
  1a304:  .word 0x20000218  ; RAM
  1a308:  .word 0x20000245  ; RAM
  1a30c:  .word 0x20000246  ; RAM
  1a310:  .word 0x20000102  ; RAM
  1a314:  .word 0x20000247  ; RAM
  1a318:  .word 0x2000021e  ; RAM
```
