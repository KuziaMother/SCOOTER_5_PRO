# func_0x1a894

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a894) | `0x0001a894` |
| размер кода | 140 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000008ca — данные @0x008ca (r5)
- 0x00001388 — данные @0x01388 (r7)
- 0x20000102 — RAM (r1)
- 0x20000218 — RAM (r4)
- 0x20000246 — RAM (r0)
- 0x40012c40 — периферия (r0)

## Вызовы (callees)

- 0x1e3e4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a338)


## Дизассембляция

```asm
  1a894:  push {r4, r5, r6, r7, lr}         
  1a896:  bl #0x1e3e4                       -> 0x1e3e4 (вне списка функций)
  1a89a:  ldr r0, [pc, #0x84]               -> периферия
  1a89c:  movs r2, #0                       
  1a89e:  str r2, [r0, #4]                  
  1a8a0:  str r2, [r0, #8]                  
  1a8a2:  str r2, [r0, #0xc]                
  1a8a4:  ldr r1, [pc, #0x7c]               -> RAM
  1a8a6:  movs r5, #1                       
  1a8a8:  strb r2, [r1]                     
  1a8aa:  strb r5, [r1, #1]                 
  1a8ac:  ldr r4, [r0, #0x14]               
  1a8ae:  lsls r3, r5, #0xf                 
  1a8b0:  orrs r4, r3                       
  1a8b2:  str r4, [r0, #0x14]               
  1a8b4:  ldr r4, [pc, #0x70]               -> RAM
  1a8b6:  strb r5, [r4]                     
  1a8b8:  ldrh r5, [r1, #4]                 
  1a8ba:  subs r5, r5, #1                   
  1a8bc:  strh r5, [r1, #4]                 
  1a8be:  bhs #0x1a8b8                      
  1a8c0:  movs r5, #0xff                    
  1a8c2:  adds r5, #0xf5                    
  1a8c4:  strh r5, [r1, #4]                 
  1a8c6:  ldr r5, [r0, #0x14]               
  1a8c8:  bics r5, r3                       
  1a8ca:  str r5, [r0, #0x14]               
  1a8cc:  strb r2, [r4]                     
  1a8ce:  ldrh r5, [r1, #4]                 
  1a8d0:  subs r5, r5, #1                   
  1a8d2:  strh r5, [r1, #4]                 
  1a8d4:  bhs #0x1a8ce                      
  1a8d6:  ldr r7, [pc, #0x54]               -> данные @0x01388
  1a8d8:  strh r7, [r1, #4]                 
  1a8da:  ldr r5, [pc, #0x54]               -> данные @0x008ca
  1a8dc:  str r5, [r0, #4]                  
  1a8de:  str r5, [r0, #8]                  
  1a8e0:  str r5, [r0, #0xc]                
  1a8e2:  movs r5, #2                       
  1a8e4:  strb r5, [r1]                     
  1a8e6:  movs r5, #3                       
  1a8e8:  strb r5, [r1, #1]                 
  1a8ea:  ldr r5, [r0, #0x14]               
  1a8ec:  orrs r5, r3                       
  1a8ee:  str r5, [r0, #0x14]               
  1a8f0:  movs r5, #1                       
  1a8f2:  strb r5, [r4]                     
  1a8f4:  ldrh r5, [r1, #4]                 
  1a8f6:  subs r5, r5, #1                   
  1a8f8:  strh r5, [r1, #4]                 
  1a8fa:  bhs #0x1a8f4                      
  1a8fc:  movs r5, #0xff                    
  1a8fe:  adds r5, #0xf5                    
  1a900:  strh r5, [r1, #4]                 
  1a902:  ldr r5, [r0, #0x14]               
  1a904:  bics r5, r3                       
  1a906:  str r5, [r0, #0x14]               
  1a908:  strb r2, [r4]                     
  1a90a:  ldrh r0, [r1, #4]                 
  1a90c:  subs r3, r0, #1                   
  1a90e:  strh r3, [r1, #4]                 
  1a910:  bhs #0x1a90a                      
  1a912:  strh r7, [r1, #4]                 
  1a914:  movs r0, #4                       
  1a916:  strb r0, [r1]                     
  1a918:  strb r0, [r1, #1]                 
  1a91a:  ldr r0, [pc, #0x18]               -> RAM
  1a91c:  strb r2, [r0]                     
  1a91e:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1a920 (6 слов) — ВНЕ границ функции ---
  1a920:  .word 0x40012c40  ; периферия
  1a924:  .word 0x20000102  ; RAM
  1a928:  .word 0x20000218  ; RAM
  1a92c:  .word 0x00001388  ; данные @0x01388
  1a930:  .word 0x000008ca  ; данные @0x008ca
  1a934:  .word 0x20000246  ; RAM
```
