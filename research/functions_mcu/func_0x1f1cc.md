# func_0x1f1cc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001f1cc) | `0x0001f1cc` |
| размер кода | 114 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000170 — RAM (r0)
- 0x200001e0 — RAM (r1)
- 0x200002c1 — RAM (r0)
- 0x20000a43 — RAM (r3)

## Вызовы (callees)

- 0x1f544 (b, вне списка функций)
- 0x21b52 (bl, вне списка функций)
- 0xff9f27f4 (bl, вне образа — runtime/внешний)

## Кто вызывает (callers / xrefs)

- `func_0x1dfd8` (bl @0x0001e0b2)


## Дизассембляция

```asm
  1f1cc:  push {r2, r3, r4, r5, r6, r7, lr} 
  1f1ce:  ldr r0, [pc, #0x3e0]              -> RAM
  1f1d0:  ldr r1, [pc, #0x3e4]              -> RAM
  1f1d2:  ldrb r6, [r0, #0xc]               
  1f1d4:  ldr r0, [pc, #0x3dc]              -> RAM
  1f1d6:  movs r4, #0                       
  1f1d8:  ldrb r7, [r0]                     
  1f1da:  adds r0, r7, #1                   
  1f1dc:  uxtb r0, r0                       
  1f1de:  str r0, [sp, #4]                  
  1f1e0:  ldr r0, [pc, #0x3cc]              -> RAM
  1f1e2:  ldr r5, [r0, #0x3c]               
  1f1e4:  ldr r3, [r0, #0x38]               
  1f1e6:  ldm r1!, {r0, r2}                 
  1f1e8:  subs r3, r0, r3                   
  1f1ea:  mov r1, r2                        
  1f1ec:  sbcs r2, r5                       
  1f1ee:  mov r5, r2                        
  1f1f0:  mov r2, r3                        
  1f1f2:  movs r3, #0x96                    
  1f1f4:  muls r7, r3, r7                   
  1f1f6:  ldr r3, [pc, #0x3c4]              -> RAM
  1f1f8:  str r7, [sp]                      
  1f1fa:  adds r7, r7, r3                   
  1f1fc:  movs r3, r6                       
  1f1fe:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1f202:  lsls r3, r1, #0x1c                
  1f204:  subs r4, #0x1e                    
  1f206:  ldrb r3, [r3, #5]                 
  1f208:  push {r0, r1, r2, r4, r7, lr}     
  1f20a:  bl #0xff9f27f4                    
  1f20e:  lsls r2, r3, #1                   
  1f210:  ldr r2, [pc, #0x3a8]              -> RAM
  1f212:  ldr r5, [sp]                      
  1f214:  movs r4, #4                       
  1f216:  strb r4, [r2, r5]                 
  1f218:  movs r2, #0x63                    
  1f21a:  strb r2, [r7, #1]                 
  1f21c:  movs r2, #0x44                    
  1f21e:  strb r2, [r7, #2]                 
  1f220:  movs r2, #0xa7                    
  1f222:  strb r2, [r7, #3]                 
  1f224:  movs r2, #0x9c                    
  1f226:  strb r2, [r7, #4]                 
  1f228:  ldr r3, [pc, #0x388]              -> RAM
  1f22a:  ldr r2, [sp, #4]                  
  1f22c:  strb r2, [r3]                     
  1f22e:  cmp r2, #3                        
  1f230:  blo #0x1f236                      
  1f232:  movs r2, #0                       
  1f234:  strb r2, [r3]                     
  1f236:  ldr r2, [pc, #0x378]              -> RAM
  1f238:  str r1, [r2, #0x3c]               
  1f23a:  str r0, [r2, #0x38]               
  1f23c:  b #0x1f544                        -> 0x1f544 (вне списка функций)
  ; --- literal-пул @0x1f5b0 (4 слов) — ВНЕ границ функции ---
  1f5b0:  .word 0x20000170  ; RAM
  1f5b4:  .word 0x200002c1  ; RAM
  1f5b8:  .word 0x200001e0  ; RAM
  1f5bc:  .word 0x20000a43  ; RAM
```
