# func_0x055c8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800055c8) | `0x000055c8` |
| размер кода | 218 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000086 — RAM (r1)
- 0x2000008c — RAM (r0)
- 0x200000f8 — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r1)
- 0x20001058 — RAM (r1)

## Вызовы (callees)

- `func_0x0d534` (0x0000d534, bl)
- `func_0x14368` (0x00014368, bl)
- `func_0x156ac` (0x000156ac, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  055c8:  push {r4, lr}                     
  055ca:  ldr r0, [pc, #0xd8]               -> RAM
  055cc:  ldrb r0, [r0]                     
  055ce:  cmp r0, #1                        
  055d0:  bne #0x56a0                       
  055d2:  movs r0, #0                       
  055d4:  ldr r1, [pc, #0xcc]               -> RAM
  055d6:  strb r0, [r1]                     
  055d8:  ldr r1, [pc, #0xcc]               -> RAM
  055da:  str r0, [r1, #4]                  
  055dc:  mov.w r0, #0x3e8                  
  055e0:  strh r0, [r1, #0x10]              
  055e2:  movs r0, #1                       
  055e4:  ldr r1, [pc, #0xc4]               -> RAM
  055e6:  strh r0, [r1]                     
  055e8:  bl #0xd534                        -> func_0x0d534
  055ec:  ldr r0, [pc, #0xc0]               -> RAM
  055ee:  ldrb r0, [r0, #2]                 
  055f0:  bic r0, r0, #2                    
  055f4:  ldr r1, [pc, #0xb8]               -> RAM
  055f6:  strb r0, [r1, #2]                 
  055f8:  bl #0x156ac                       -> func_0x156ac
  055fc:  bl #0x14368                       -> func_0x14368
  05600:  movs r0, #0                       
  05602:  ldr r1, [pc, #0xb0]               -> RAM
  05604:  strh.w r0, [r1, #0x15]            
  05608:  ldr r0, [pc, #0xac]               -> RAM
  0560a:  ldr r0, [r0]                      
  0560c:  orr r0, r0, #0x400                
  05610:  ldr r1, [pc, #0xa4]               -> RAM
  05612:  str r0, [r1]                      
  05614:  movs r0, #0                       
  05616:  ldr r1, [pc, #0x98]               -> RAM
  05618:  str.w r0, [r1, #9]                
  0561c:  ldr r0, [pc, #0x98]               -> RAM
  0561e:  ldr r0, [r0]                      
  05620:  orr r0, r0, #0x2000               
  05624:  ldr r1, [pc, #0x90]               -> RAM
  05626:  str r0, [r1]                      
  05628:  movs r0, #0                       
  0562a:  ldr r1, [pc, #0x84]               -> RAM
  0562c:  str.w r0, [r1, #0xd]              
  05630:  ldr r0, [pc, #0x84]               -> RAM
  05632:  ldr r0, [r0]                      
  05634:  orr r0, r0, #0x4000               
  05638:  ldr r1, [pc, #0x7c]               -> RAM
  0563a:  str r0, [r1]                      
  0563c:  movs r0, #0x78                    
  0563e:  ldr r1, [pc, #0x70]               -> RAM
  05640:  str.w r0, [r1, #0x11]             
  05644:  ldr r0, [pc, #0x70]               -> RAM
  05646:  ldr r0, [r0]                      
  05648:  orr r0, r0, #0x8000               
  0564c:  ldr r1, [pc, #0x68]               -> RAM
  0564e:  str r0, [r1]                      
  05650:  movs r0, #0                       
  05652:  ldr r1, [pc, #0x5c]               -> RAM
  05654:  str.w r0, [r1, #0x15]             
  05658:  ldr r0, [pc, #0x5c]               -> RAM
  0565a:  ldr r0, [r0]                      
  0565c:  orr r0, r0, #0x10000              
  05660:  ldr r1, [pc, #0x54]               -> RAM
  05662:  str r0, [r1]                      
  05664:  movs r0, #0                       
  05666:  ldr r1, [pc, #0x48]               -> RAM
  05668:  str.w r0, [r1, #0x1f]             
  0566c:  ldr r0, [pc, #0x48]               -> RAM
  0566e:  ldr r0, [r0]                      
  05670:  orr r0, r0, #0x20000              
  05674:  ldr r1, [pc, #0x40]               -> RAM
  05676:  str r0, [r1]                      
  05678:  ldr r0, [pc, #0x34]               -> RAM
  0567a:  ldrh.w r0, [r0, #0x23]            
  0567e:  movw r1, #0xea60                  
  05682:  cmp r0, r1                        
  05684:  bge #0x5694                       
  05686:  ldr r0, [pc, #0x28]               -> RAM
  05688:  ldrh.w r0, [r0, #0x23]            
  0568c:  adds r0, r0, #1                   
  0568e:  ldr r1, [pc, #0x20]               -> RAM
  05690:  strh.w r0, [r1, #0x23]            
  05694:  ldr r0, [pc, #0x20]               -> RAM
  05696:  ldr r0, [r0]                      
  05698:  orr r0, r0, #0x40000              
  0569c:  ldr r1, [pc, #0x18]               -> RAM
  0569e:  str r0, [r1]                      
  056a0:  pop {r4, pc}                      
  ; --- literal-пул @0x056a4 (6 слов) — ВНЕ границ функции ---
  056a4:  .word 0x200000f8  ; RAM
  056a8:  .word 0x20001058  ; RAM
  056ac:  .word 0x20000086  ; RAM
  056b0:  .word 0x20000f70  ; RAM
  056b4:  .word 0x20000f95  ; RAM
  056b8:  .word 0x2000008c  ; RAM
```
