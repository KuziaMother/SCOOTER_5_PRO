# func_0x1f600

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001f600) | `0x0001f600` |
| размер кода | 156 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000170 — RAM (r4)
- 0x200001e0 — RAM (r1)
- 0x200002c1 — RAM (r1)
- 0x200002c2 — RAM (r7)
- 0x20000a43 — RAM (r2)
- 0x40004800 — периферия (r0)

## Вызовы (callees)

- `func_0x1f1c0` (0x0001f1c0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a518)


## Дизассембляция

```asm
  1f600:  push {r3, r4, r5, r6, r7, lr}     
  1f602:  ldr r7, [pc, #0x98]               -> RAM
  1f604:  ldr r1, [pc, #0x98]               -> RAM
  1f606:  ldrb r0, [r7]                     
  1f608:  ldrb r1, [r1]                     
  1f60a:  cmp r0, r1                        
  1f60c:  beq #0x1f660                      
  1f60e:  ldr r1, [pc, #0x94]               -> RAM
  1f610:  ldr r4, [pc, #0x94]               -> RAM
  1f612:  ldr r3, [r1]                      
  1f614:  ldr r1, [r1, #4]                  
  1f616:  ldr r2, [r4, #0x28]               
  1f618:  ldr r4, [r4, #0x2c]               
  1f61a:  mov r5, r1                        
  1f61c:  subs r2, r3, r2                   
  1f61e:  sbcs r5, r4                       
  1f620:  movs r6, #0xff                    
  1f622:  adds r6, #0xb1                    
  1f624:  movs r4, #0                       
  1f626:  subs r2, r6, r2                   
  1f628:  sbcs r4, r5                       
  1f62a:  bhs #0x1f660                      
  1f62c:  movs r2, #0x96                    
  1f62e:  mov r6, r0                        
  1f630:  muls r6, r2, r6                   
  1f632:  ldr r2, [pc, #0x78]               -> RAM
  1f634:  ldr r4, [pc, #0x70]               -> RAM
  1f636:  ldrb r5, [r2, r6]                 
  1f638:  strb r5, [r4, #0xa]               
  1f63a:  ldrb r2, [r4, #0xb]               
  1f63c:  adds r5, r5, #1                   
  1f63e:  cmp r2, r5                        
  1f640:  blo #0x1f662                      
  1f642:  movs r2, #1                       
  1f644:  strb r2, [r4, #0xb]               
  1f646:  movs r5, #0xb                     
  1f648:  movs r2, #0                       
  1f64a:  str r5, [r4, #0x30]               
  1f64c:  adds r0, r0, #1                   
  1f64e:  str r3, [r4, #0x28]               
  1f650:  uxtb r0, r0                       
  1f652:  str r2, [r4, #0x34]               
  1f654:  str r1, [r4, #0x2c]               
  1f656:  strb r0, [r7]                     
  1f658:  cmp r0, #3                        
  1f65a:  blo #0x1f660                      
  1f65c:  movs r0, #0                       
  1f65e:  strb r0, [r7]                     
  1f660:  pop {r3, r4, r5, r6, r7, pc}      
  1f662:  ldr r1, [r4, #0x30]               
  1f664:  movs r5, #8                       
  1f666:  ldr r0, [r4, #0x34]               
  1f668:  movs r3, #0                       
  1f66a:  subs r5, r5, r1                   
  1f66c:  sbcs r3, r0                       
  1f66e:  bhs #0x1f690                      
  1f670:  ldr r0, [pc, #0x3c]               -> периферия
  1f672:  ldr r0, [r0, #0x28]               
  1f674:  lsls r0, r0, #0x11                
  1f676:  bmi #0x1f660                      
  1f678:  ldr r0, [pc, #0x30]               -> RAM
  1f67a:  adds r0, r6, r0                   
  1f67c:  ldrb r0, [r0, r2]                 
  1f67e:  bl #0x1f1c0                       -> func_0x1f1c0
  1f682:  ldrb r0, [r4, #0xb]               
  1f684:  adds r0, r0, #1                   
  1f686:  strb r0, [r4, #0xb]               
  1f688:  movs r0, #0                       
  1f68a:  str r0, [r4, #0x30]               
  1f68c:  str r0, [r4, #0x34]               
  1f68e:  pop {r3, r4, r5, r6, r7, pc}      
  1f690:  adds r1, r1, #1                   
  1f692:  movs r2, #0                       
  1f694:  adcs r0, r2                       
  1f696:  str r1, [r4, #0x30]               
  1f698:  str r0, [r4, #0x34]               
  1f69a:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1f69c (6 слов) — ВНЕ границ функции ---
  1f69c:  .word 0x200002c2  ; RAM
  1f6a0:  .word 0x200002c1  ; RAM
  1f6a4:  .word 0x200001e0  ; RAM
  1f6a8:  .word 0x20000170  ; RAM
  1f6ac:  .word 0x20000a43  ; RAM
  1f6b0:  .word 0x40004800  ; периферия
```
