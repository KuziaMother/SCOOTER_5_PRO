# func_0x1e658

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001e658) | `0x0001e658` |
| размер кода | 218 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000400 — данные @0x00400 (r2)
- 0x20000030 — RAM (r1)
- 0x2000021e — RAM (r3)
- 0x200002c4 — RAM (r1)
- 0x200002c6 — RAM (r4)
- 0x200002c7 — RAM (r3)
- 0x20000c05 — RAM (r7)
- 0x40004c00 — периферия (r1)
- 0x40004c40 — периферия (r0)

## Вызовы (callees)

- 0x1e6b4 (b, вне списка функций)
- 0x21b52 (bl, вне списка функций)
- 0x00634908 (bl, вне образа — runtime/внешний)
- 0xffb3510c (bl, вне образа — runtime/внешний)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1e676..0x1e68e` (24 Б); цели из: 0x1e668, 0x1e66e
- `0x1e68e..0x1e69c` (14 Б); цели из: 0x1e674
- `0x1e69c..0x1e6b8` (28 Б); цели из: 0x1e694
- `0x1e6b8..0x1e732` (122 Б); цели из: 0x1e69a

## Дизассембляция

```asm
  1e658:  push {r4, r5, r6, r7, lr}         
  1e65a:  sub sp, #0x20                     
  1e65c:  movs r0, #0                       
  1e65e:  ldr r1, [pc, #0x358]              -> периферия
  1e660:  str r0, [sp, #8]                  
  1e662:  ldr r0, [r1, #0x3c]               
  1e664:  lsls r2, r0, #0x1f                
  1e666:  ldr r0, [pc, #0x354]              -> периферия
  1e668:  bne #0x1e676                      
  1e66a:  ldr r2, [r1, #0x3c]               
  1e66c:  lsls r2, r2, #0x1b                
  1e66e:  bmi #0x1e676                      
  1e670:  ldr r2, [r1, #0x3c]               
  1e672:  lsls r2, r2, #0x17                
  1e674:  bpl #0x1e68e                      
  1e676:  ldr r2, [r0]                      
  1e678:  movs r3, #1                       
  1e67a:  orrs r2, r3                       
  1e67c:  str r2, [r0]                      
  1e67e:  ldr r2, [r0]                      
  1e680:  movs r3, #0x10                    
  1e682:  orrs r2, r3                       
  1e684:  str r2, [r0]                      
  1e686:  ldr r2, [r0]                      
  1e688:  lsls r3, r3, #4                   
  1e68a:  orrs r2, r3                       
  1e68c:  str r2, [r0]                      
  1e68e:  ldr r2, [r1, #0x3c]               
  1e690:  lsls r3, r2, #0x13                
  1e692:  ldr r2, [pc, #0x32c]              -> данные @0x00400
  1e694:  bmi #0x1e69c                      
  1e696:  ldr r3, [r1, #0x3c]               
  1e698:  lsls r3, r3, #0x14                
  1e69a:  bpl #0x1e6b8                      
  1e69c:  ldr r1, [r0]                      
  1e69e:  orrs r1, r2                       
  1e6a0:  str r1, [r0]                      
  1e6a2:  ldr r1, [r0]                      
  1e6a4:  movs r2, #1                       
  1e6a6:  lsls r2, r2, #0xc                 
  1e6a8:  orrs r1, r2                       
  1e6aa:  str r1, [r0]                      
  1e6ac:  ldr r1, [r0]                      
  1e6ae:  asrs r2, r2, #1                   
  1e6b0:  orrs r1, r2                       
  1e6b2:  str r1, [r0]                      
  1e6b4:  add sp, #0x20                     
  1e6b6:  pop {r4, r5, r6, r7, pc}          
  1e6b8:  ldr r3, [r1, #0x3c]               
  1e6ba:  lsls r3, r3, #0x15                
  1e6bc:  bpl #0x1e6b4                      
  1e6be:  ldr r3, [r0]                      
  1e6c0:  orrs r3, r2                       
  1e6c2:  str r3, [r0]                      
  1e6c4:  ldr r0, [r1]                      
  1e6c6:  ldr r1, [pc, #0x2fc]              -> RAM
  1e6c8:  movs r2, #0                       
  1e6ca:  strh r2, [r1]                     
  1e6cc:  ldr r4, [pc, #0x2f8]              -> RAM
  1e6ce:  ldr r1, [pc, #0x2fc]              -> RAM
  1e6d0:  ldrb r6, [r4]                     
  1e6d2:  ldrh r3, [r1, #0xa]               
  1e6d4:  str r3, [sp, #0x1c]               
  1e6d6:  adds r3, r3, #1                   
  1e6d8:  uxth r5, r3                       
  1e6da:  ldr r3, [pc, #0x2f4]              -> RAM
  1e6dc:  movs r7, #0x20                    
  1e6de:  ldrb r3, [r3]                     
  1e6e0:  uxtb r0, r0                       
  1e6e2:  mov ip, r3                        
  1e6e4:  adds r3, r3, #1                   
  1e6e6:  uxtb r3, r3                       
  1e6e8:  str r3, [sp, #0x14]               
  1e6ea:  ldr r3, [pc, #0x2e8]              -> RAM
  1e6ec:  ldrh r3, [r3]                     
  1e6ee:  bics r3, r7                       
  1e6f0:  str r3, [sp, #0x18]               
  1e6f2:  mov r3, ip                        
  1e6f4:  movs r7, #0x96                    
  1e6f6:  muls r3, r7, r3                   
  1e6f8:  ldr r7, [pc, #0x2dc]              -> RAM
  1e6fa:  str r3, [sp, #0xc]                
  1e6fc:  adds r7, r3, r7                   
  1e6fe:  movs r3, r6                       
  1e700:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1e704:  asrs r1, r5, #0x1c                
  1e706:  ldm r1!, {r0, r3, r4, r5, r6}     
  1e708:  bhi #0x1e6aa                      
  1e70a:  asrs r5, r3, #0x1b                
  1e70c:  asrs r6, r2, #0x18                
  1e70e:  bl #0xffb3510c                    
  1e712:  asrs r3, r6, #0x1b                
  1e714:  asrs r6, r2, #0x18                
  1e716:  asrs r6, r2, #0x18                
  1e718:  adds r4, #0x16                    
  1e71a:  subs r6, #0x39                    
  1e71c:  strb r1, [r2, r1]                 
  1e71e:  ldrh r7, [r2, r1]                 
  1e720:  ldr r5, [r3, #0x54]               
  1e722:  bl #0x634908                      
  1e726:  cdp p6, #0xe, c1, c15, c13, #7    
  1e72a:  asrs r6, r2, #0x18                
  1e72c:  .byte 0x16, 0xec                  
  1e72e:  movs r6, r2                       
  1e730:  b #0x1e6b4                        -> 0x1e6b4 (вне списка функций)
  ; --- literal-пул @0x1e9b8 (9 слов) — ВНЕ границ функции ---
  1e9b8:  .word 0x40004c00  ; периферия
  1e9bc:  .word 0x40004c40  ; периферия
  1e9c0:  .word 0x00000400  ; данные @0x00400
  1e9c4:  .word 0x200002c4  ; RAM
  1e9c8:  .word 0x200002c6  ; RAM
  1e9cc:  .word 0x20000030  ; RAM
  1e9d0:  .word 0x200002c7  ; RAM
  1e9d4:  .word 0x2000021e  ; RAM
  1e9d8:  .word 0x20000c05  ; RAM
```
