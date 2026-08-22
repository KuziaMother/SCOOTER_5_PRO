# func_0x1de0c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001de0c) | `0x0001de0c` |
| размер кода | 66 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000610 — RAM (r4)
- 0x430c0000 — периферия (r0)
- 0xc2200000 — прочее (r1)

## Вызовы (callees)

- `func_0x1de5e` (0x0001de5e, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1d898` (bl @0x0001d8fa)


## Дизассембляция

```asm
  1de0c:  push {r3, r4, r5, r6, r7, lr}     
  1de0e:  ldr r4, [pc, #0x40]               -> RAM
  1de10:  movs r1, #0                       
  1de12:  lsls r2, r1, #2                   
  1de14:  adds r2, r2, r4                   
  1de16:  ldr r2, [r2, #4]                  
  1de18:  cmp r2, r0                        
  1de1a:  bhs #0x1de42                      
  1de1c:  str r0, [sp]                      
  1de1e:  lsls r0, r1, #2                   
  1de20:  ldr r5, [pc, #0x2c]               -> RAM
  1de22:  adds r2, r0, r4                   
  1de24:  lsls r6, r1, #1                   
  1de26:  subs r5, #0x5c                    
  1de28:  ldr r3, [r2, #4]                  
  1de2a:  adds r1, r6, r5                   
  1de2c:  movs r2, #2                       
  1de2e:  ldrsh r2, [r1, r2]                
  1de30:  ldr r1, [r4, r0]                  
  1de32:  ldrsh r0, [r5, r6]                
  1de34:  bl #0x1de5e                       -> func_0x1de5e
  1de38:  ldr r1, [pc, #0x18]               
  1de3a:  cmp r0, r1                        
  1de3c:  bls #0x1de40                      
  1de3e:  mov r0, r1                        
  1de40:  pop {r3, r4, r5, r6, r7, pc}      
  1de42:  adds r1, r1, #1                   
  1de44:  uxtb r1, r1                       
  1de46:  cmp r1, #0x2d                     
  1de48:  blo #0x1de12                      
  1de4a:  ldr r0, [pc, #0xc]                -> периферия
  1de4c:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1de50 (3 слов) — ВНЕ границ функции ---
  1de50:  .word 0x20000610  ; RAM
  1de54:  .word 0xc2200000
  1de58:  .word 0x430c0000  ; периферия
```
