# func_0x1a688

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a688) | `0x0001a688` |
| размер кода | 266 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00002710 — данные @0x02710 (r3)
- 0x200000ac — RAM (r1)
- 0x20000218 — RAM (r0)
- 0x20000269 — RAM (r5)
- 0x20001768 — RAM (r5)
- 0x40012c40 — периферия (r4)

## Вызовы (callees)

- 0x1a69c (b, вне списка функций)
- 0x1a6c6 (b, вне списка функций)
- 0x1a76c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a404)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1a698..0x1a69c` (4 Б); цели из: 0x1a692
- `0x1a69c..0x1a6b4` (24 Б); цели из: 0x1a696
- `0x1a6b4..0x1a6c2` (14 Б); цели из: 0x1a6ac
- `0x1a6c2..0x1a6c6` (4 Б); цели из: 0x1a6b2, 0x1a6bc
- `0x1a6c6..0x1a70c` (70 Б); цели из: 0x1a6c0
- `0x1a70c..0x1a726` (26 Б); цели из: 0x1a6ec
- `0x1a726..0x1a734` (14 Б); цели из: 0x1a712
- `0x1a734..0x1a73a` (6 Б); цели из: 0x1a72a
- `0x1a73a..0x1a754` (26 Б); цели из: 0x1a6f0
- `0x1a754..0x1a762` (14 Б); цели из: 0x1a740
- `0x1a762..0x1a768` (6 Б); цели из: 0x1a758
- `0x1a768..0x1a76c` (4 Б); цели из: 0x1a6f6
- `0x1a76c..0x1a780` (20 Б); цели из: 0x1a70a, 0x1a732, 0x1a738, 0x1a760…
- `0x1a780..0x1a790` (16 Б); цели из: 0x1a770
- `0x1a790..0x1a792` (2 Б); цели из: 0x1a6a0, 0x1a784, 0x1a78a

## Дизассембляция

```asm
  1a688:  push {r4, r5, r6, r7, lr}         
  1a68a:  ldr r1, [pc, #0x108]              -> RAM
  1a68c:  ldr r3, [pc, #0x108]              -> данные @0x02710
  1a68e:  ldr r2, [r1, #0x40]               
  1a690:  cmp r2, r3                        
  1a692:  bls #0x1a698                      
  1a694:  str r3, [r1, #0x40]               
  1a696:  b #0x1a69c                        -> 0x1a69c (вне списка функций)
  1a698:  adds r2, r2, #1                   
  1a69a:  str r2, [r1, #0x40]               
  1a69c:  ldrh r3, [r1, #0xe]               
  1a69e:  cmp r3, r0                        
  1a6a0:  beq #0x1a790                      
  1a6a2:  ldr r5, [r1, #0x3c]               
  1a6a4:  ldr r4, [r1, #0x40]               
  1a6a6:  lsls r6, r5, #1                   
  1a6a8:  movs r2, #0                       
  1a6aa:  cmp r6, r4                        
  1a6ac:  blo #0x1a6b4                      
  1a6ae:  lsrs r5, r5, #1                   
  1a6b0:  cmp r5, r4                        
  1a6b2:  bls #0x1a6c2                      
  1a6b4:  ldr r5, [pc, #0xe4]               -> RAM
  1a6b6:  movs r6, #8                       
  1a6b8:  ldrsh r6, [r5, r6]                
  1a6ba:  cmp r6, #0x1e                     
  1a6bc:  blt #0x1a6c2                      
  1a6be:  mov r0, r3                        
  1a6c0:  b #0x1a6c6                        -> 0x1a6c6 (вне списка функций)
  1a6c2:  str r4, [r1, #0x3c]               
  1a6c4:  str r2, [r1, #0x40]               
  1a6c6:  ldrh r3, [r1, #6]                 
  1a6c8:  ldr r4, [pc, #0xd4]               -> периферия
  1a6ca:  ands r3, r0                       
  1a6cc:  strh r3, [r1, #6]                 
  1a6ce:  ldrh r7, [r1, #0x10]              
  1a6d0:  mov ip, r3                        
  1a6d2:  orrs r7, r0                       
  1a6d4:  strh r7, [r1, #0x10]              
  1a6d6:  strh r0, [r1, #0xe]               
  1a6d8:  ldrb r3, [r1, #1]                 
  1a6da:  ldr r5, [pc, #0xc8]               -> RAM
  1a6dc:  adds r3, r3, #1                   
  1a6de:  uxtb r3, r3                       
  1a6e0:  strb r3, [r1, #1]                 
  1a6e2:  mov lr, r3                        
  1a6e4:  ldr r3, [pc, #0xac]               -> RAM
  1a6e6:  ldrb r6, [r3, #3]                 
  1a6e8:  movs r3, #1                       
  1a6ea:  cmp r0, #7                        
  1a6ec:  beq #0x1a70c                      
  1a6ee:  cmp r0, #0                        
  1a6f0:  beq #0x1a73a                      
  1a6f2:  ldrh r0, [r1, #0x16]              
  1a6f4:  cmp r0, #5                        
  1a6f6:  bls #0x1a768                      
  1a6f8:  strh r2, [r1, #0x12]              
  1a6fa:  strh r2, [r1, #0x14]              
  1a6fc:  strh r2, [r1, #0x18]              
  1a6fe:  strb r2, [r1, #2]                 
  1a700:  strb r2, [r1]                     
  1a702:  strh r2, [r1, #0xc]               
  1a704:  strb r2, [r5]                     
  1a706:  strh r2, [r1, #8]                 
  1a708:  strb r2, [r1, #3]                 
  1a70a:  b #0x1a76c                        -> 0x1a76c (вне списка функций)
  1a70c:  strh r2, [r1, #0x16]              
  1a70e:  strh r2, [r1, #0x14]              
  1a710:  cmp r6, #0                        
  1a712:  bne #0x1a726                      
  1a714:  ldr r0, [r4, #0x14]               
  1a716:  movs r6, #1                       
  1a718:  lsls r6, r6, #0xf                 
  1a71a:  bics r0, r6                       
  1a71c:  str r0, [r4, #0x14]               
  1a71e:  ldr r0, [pc, #0x88]               -> RAM
  1a720:  strb r2, [r0]                     
  1a722:  strb r3, [r5]                     
  1a724:  strb r3, [r1, #3]                 
  1a726:  ldrh r0, [r1, #0x12]              
  1a728:  cmp r0, #0                        
  1a72a:  beq #0x1a734                      
  1a72c:  strb r3, [r1]                     
  1a72e:  strh r2, [r1, #0xc]               
  1a730:  cmp r0, #0xa                      
  1a732:  bhs #0x1a76c                      
  1a734:  adds r0, r0, #1                   
  1a736:  strh r0, [r1, #0x12]              
  1a738:  b #0x1a76c                        -> 0x1a76c (вне списка функций)
  1a73a:  strh r2, [r1, #0x16]              
  1a73c:  strh r2, [r1, #0x12]              
  1a73e:  cmp r6, #0                        
  1a740:  bne #0x1a754                      
  1a742:  ldr r0, [r4, #0x14]               
  1a744:  movs r6, #1                       
  1a746:  lsls r6, r6, #0xf                 
  1a748:  bics r0, r6                       
  1a74a:  str r0, [r4, #0x14]               
  1a74c:  ldr r0, [pc, #0x58]               -> RAM
  1a74e:  strb r2, [r0]                     
  1a750:  strb r3, [r5]                     
  1a752:  strb r3, [r1, #3]                 
  1a754:  ldrh r0, [r1, #0x14]              
  1a756:  cmp r0, #0                        
  1a758:  beq #0x1a762                      
  1a75a:  strb r3, [r1]                     
  1a75c:  strh r3, [r1, #0xc]               
  1a75e:  cmp r0, #0xa                      
  1a760:  bhs #0x1a76c                      
  1a762:  adds r0, r0, #1                   
  1a764:  strh r0, [r1, #0x14]              
  1a766:  b #0x1a76c                        -> 0x1a76c (вне списка функций)
  1a768:  adds r0, r0, #1                   
  1a76a:  strh r0, [r1, #0x16]              
  1a76c:  mov r0, lr                        
  1a76e:  cmp r0, #4                        
  1a770:  bne #0x1a780                      
  1a772:  mov r0, ip                        
  1a774:  strh r0, [r1, #8]                 
  1a776:  strh r7, [r1, #0xa]               
  1a778:  strh r2, [r1, #0x10]              
  1a77a:  movs r0, #0xff                    
  1a77c:  strh r0, [r1, #6]                 
  1a77e:  strb r2, [r1, #1]                 
  1a780:  ldrb r0, [r1]                     
  1a782:  cmp r0, #0                        
  1a784:  beq #0x1a790                      
  1a786:  ldrb r0, [r1, #2]                 
  1a788:  cmp r0, #0x64                     
  1a78a:  bhs #0x1a790                      
  1a78c:  adds r0, r0, #1                   
  1a78e:  strb r0, [r1, #2]                 
  1a790:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1a794 (6 слов) — ВНЕ границ функции ---
  1a794:  .word 0x200000ac  ; RAM
  1a798:  .word 0x00002710  ; данные @0x02710
  1a79c:  .word 0x20001768  ; RAM
  1a7a0:  .word 0x40012c40  ; периферия
  1a7a4:  .word 0x20000269  ; RAM
  1a7a8:  .word 0x20000218  ; RAM
```
