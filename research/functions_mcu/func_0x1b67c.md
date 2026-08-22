# func_0x1b67c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001b67c) | `0x0001b67c` |
| размер кода | 1174 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000008 — данные @0x00008 (r5)
- 0x00000bb8 — данные @0x00bb8 (r0)
- 0x0000a8c8 — данные @0x0a8c8 (r1)
- 0x200000ac — RAM (r0)
- 0x200001e0 — RAM (r1)
- 0x200001fa — RAM (r1)
- 0x20000212 — RAM (r3)
- 0x20000214 — RAM (r2)
- 0x20000218 — RAM (r0)
- 0x2000021e — RAM (r0)
- 0x20000220 — RAM (r0)
- 0x20000224 — RAM (r0)
- 0x2000022e — RAM (r0)
- 0x20000231 — RAM (r3)
- 0x20000245 — RAM (r1)
- 0x2000024a — RAM (r0)
- 0x2000024c — RAM (r0)
- 0x2000024e — RAM (r0)
- 0x20000263 — RAM (r3)
- 0x20000264 — RAM (r3)
- 0x2000026a — RAM (r3)
- 0x2000026c — RAM (r1)
- 0x2000026e — RAM (r2)
- 0x20000280 — RAM (r3)
- 0x2000030c — RAM (r1)
- 0x20000318 — RAM (r1)
- 0x2000031a — RAM (r3)
- 0x20000339 — RAM (r3)
- 0x2000033a — RAM (r3)
- 0x20000380 — RAM (r4)
- 0x20000388 — RAM (r0)
- 0x20000394 — RAM (r1)
- 0x2000039c — RAM (r1)
- 0x200003c8 — RAM (r6)
- 0x2000169a — RAM (r0)
- 0x20001768 — RAM (r4)
- 0x20001794 — RAM (r0)
- 0x40012c40 — периферия (r0)
- 0xffffd8f0 — прочее (r4)
- 0xfffffc18 — прочее (r6)

## Вызовы (callees)

- 0x1b6d0 (b, вне списка функций)
- 0x1b718 (b, вне списка функций)
- 0x1b73c (b, вне списка функций)
- 0x1b750 (b, вне списка функций)
- 0x1b7fe (b, вне списка функций)
- 0x1b800 (b, вне списка функций)
- 0x1b844 (b, вне списка функций)
- 0x1b866 (b, вне списка функций)
- 0x1b86c (b, вне списка функций)
- 0x1b90a (b, вне списка функций)
- 0x1b910 (b, вне списка функций)
- 0x1b92c (b, вне списка функций)
- 0x1b966 (b, вне списка функций)
- 0x1b97c (b, вне списка функций)
- 0x1b994 (b, вне списка функций)
- 0x1b9ec (b, вне списка функций)
- 0x1ba4e (b, вне списка функций)
- 0x1bafc (b, вне списка функций)
- `func_0x1ce38` (0x0001ce38, bl)
- `func_0x1d898` (0x0001d898, bl)
- `func_0x1e1a0` (0x0001e1a0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1dfd8` (bl @0x0001dfda)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1b6c4..0x1b6cc` (8 Б); цели из: 0x1b6b4
- `0x1b6cc..0x1b6d0` (4 Б); цели из: 0x1b6c2
- `0x1b6d0..0x1b704` (52 Б); цели из: 0x1b6ca
- `0x1b704..0x1b712` (14 Б); цели из: 0x1b6fc
- `0x1b712..0x1b718` (6 Б); цели из: 0x1b6f6
- `0x1b718..0x1b722` (10 Б); цели из: 0x1b702, 0x1b710
- `0x1b722..0x1b732` (16 Б); цели из: 0x1b716
- `0x1b732..0x1b736` (4 Б); цели из: 0x1b72a
- `0x1b736..0x1b73c` (6 Б); цели из: 0x1b71e
- `0x1b73c..0x1b760` (36 Б); цели из: 0x1b720, 0x1b730, 0x1b734
- `0x1b760..0x1b762` (2 Б); цели из: 0x1b6a8
- `0x1b762..0x1b76e` (12 Б); цели из: 0x1b73a
- `0x1b76e..0x1b786` (24 Б); цели из: 0x1b766
- `0x1b786..0x1b78e` (8 Б); цели из: 0x1b77c
- `0x1b78e..0x1b796` (8 Б); цели из: 0x1b746
- `0x1b796..0x1b7be` (40 Б); цели из: 0x1b74e
- `0x1b7be..0x1b7d6` (24 Б); цели из: 0x1b7b2
- `0x1b7d6..0x1b7ec` (22 Б); цели из: 0x1b7c6
- `0x1b7ec..0x1b7fc` (16 Б); цели из: 0x1b7e4
- `0x1b7fc..0x1b7fe` (2 Б); цели из: 0x1b7f6
- `0x1b7fe..0x1b800` (2 Б); цели из: 0x1b7ea
- `0x1b800..0x1b84c` (76 Б); цели из: 0x1b7fa
- `0x1b84c..0x1b85e` (18 Б); цели из: 0x1b806
- `0x1b85e..0x1b866` (8 Б); цели из: 0x1b7ba
- `0x1b866..0x1b87c` (22 Б); цели из: 0x1b7bc
- `0x1b87c..0x1b8f0` (116 Б); цели из: 0x1b878
- `0x1b8f0..0x1b8f4` (4 Б); цели из: 0x1b864
- `0x1b8f4..0x1b902` (14 Б); цели из: 0x1b882, 0x1b88a
- `0x1b902..0x1b90a` (8 Б); цели из: 0x1b8fc
- `0x1b90a..0x1b90e` (4 Б); цели из: 0x1b900
- `0x1b90e..0x1b910` (2 Б); цели из: 0x1b906
- `0x1b910..0x1b926` (22 Б); цели из: 0x1b90c
- `0x1b926..0x1b934` (14 Б); цели из: 0x1b91e
- `0x1b934..0x1b970` (60 Б); цели из: 0x1b924
- `0x1b970..0x1b97c` (12 Б); цели из: 0x1b8a4
- `0x1b97c..0x1b986` (10 Б); цели из: 0x1b8d4, 0x1b8ee, 0x1b96e, 0x1b972
- `0x1b986..0x1b994` (14 Б); цели из: 0x1b97a
- `0x1b994..0x1b9ac` (24 Б); цели из: 0x1b892, 0x1b984
- `0x1b9ac..0x1b9e0` (52 Б); цели из: 0x1b9a2
- `0x1b9e0..0x1b9f6` (22 Б); цели из: 0x1b9dc
- `0x1b9f6..0x1ba58` (98 Б); цели из: 0x1b9aa
- `0x1ba58..0x1bafc` (164 Б); цели из: 0x1b99a
- `0x1bafc..0x1bb12` (22 Б); цели из: 0x1ba58

## Дизассембляция

```asm
  1b67c:  push {r3, r4, r5, r6, r7, lr}     
  1b67e:  ldr r6, [pc, #0x3dc]              -> RAM
  1b680:  ldr r0, [pc, #0x3dc]              -> RAM
  1b682:  movs r2, #0                       
  1b684:  ldrsh r2, [r0, r2]                
  1b686:  ldr r1, [r6, #0x68]               
  1b688:  ldr r0, [pc, #0x3d8]              -> RAM
  1b68a:  adds r1, r1, r2                   
  1b68c:  movs r2, #0                       
  1b68e:  ldrsh r2, [r0, r2]                
  1b690:  subs r1, r1, r2                   
  1b692:  str r1, [r6, #0x68]               
  1b694:  asrs r1, r1, #5                   
  1b696:  strh r1, [r0]                     
  1b698:  ldrb r0, [r6, #0x10]              
  1b69a:  ldr r1, [pc, #0x3cc]              -> данные @0x0a8c8
  1b69c:  lsls r0, r0, #2                   
  1b69e:  ldr r0, [r1, r0]                  
  1b6a0:  blx r0                            
  1b6a2:  ldr r0, [pc, #0x3c8]              -> RAM
  1b6a4:  ldrb r0, [r0]                     
  1b6a6:  cmp r0, #6                        
  1b6a8:  bne #0x1b760                      
  1b6aa:  ldr r1, [pc, #0x3c4]              -> RAM
  1b6ac:  movs r0, #0                       
  1b6ae:  ldrsb r0, [r1, r0]                
  1b6b0:  movs r4, #0                       
  1b6b2:  cmp r0, #0x2e                     
  1b6b4:  bhs #0x1b6c4                      
  1b6b6:  ldr r0, [pc, #0x3bc]              -> RAM
  1b6b8:  movs r1, #0xc                     
  1b6ba:  ldrsh r1, [r0, r1]                
  1b6bc:  movs r0, #0x87                    
  1b6be:  lsls r0, r0, #2                   
  1b6c0:  cmp r1, r0                        
  1b6c2:  ble #0x1b6cc                      
  1b6c4:  ldr r1, [pc, #0x3b0]              -> RAM
  1b6c6:  movs r0, #1                       
  1b6c8:  strb r0, [r1]                     
  1b6ca:  b #0x1b6d0                        -> 0x1b6d0 (вне списка функций)
  1b6cc:  ldr r0, [pc, #0x3a8]              -> RAM
  1b6ce:  strb r4, [r0]                     
  1b6d0:  bl #0x1e1a0                       -> func_0x1e1a0
  1b6d4:  bl #0x1d898                       -> func_0x1d898
  1b6d8:  ldr r1, [pc, #0x3a4]              -> RAM
  1b6da:  ldr r0, [pc, #0x3a0]              -> данные @0x00bb8
  1b6dc:  str r0, [r1]                      
  1b6de:  ldr r1, [pc, #0x3a4]              -> RAM
  1b6e0:  movs r3, #0                       
  1b6e2:  str r0, [r1]                      
  1b6e4:  ldr r1, [pc, #0x3a0]              -> RAM
  1b6e6:  movs r0, #0                       
  1b6e8:  ldrsh r0, [r1, r0]                
  1b6ea:  ldr r1, [pc, #0x3a0]              -> RAM
  1b6ec:  movs r2, #1                       
  1b6ee:  ldrsh r3, [r1, r3]                
  1b6f0:  lsls r2, r2, #0xf                 
  1b6f2:  ldr r1, [pc, #0x39c]              -> RAM
  1b6f4:  cmp r0, r3                        
  1b6f6:  ble #0x1b712                      
  1b6f8:  ldrb r0, [r6, #0xc]               
  1b6fa:  cmp r0, #0xa                      
  1b6fc:  bhs #0x1b704                      
  1b6fe:  adds r0, r0, #1                   
  1b700:  strb r0, [r6, #0xc]               
  1b702:  b #0x1b718                        -> 0x1b718 (вне списка функций)
  1b704:  movs r0, #1                       
  1b706:  strb r0, [r6, #0xb]               
  1b708:  ldr r0, [pc, #0x388]              -> периферия
  1b70a:  ldr r3, [r0, #0x14]               
  1b70c:  bics r3, r2                       
  1b70e:  str r3, [r0, #0x14]               
  1b710:  b #0x1b718                        -> 0x1b718 (вне списка функций)
  1b712:  ldrb r0, [r6, #0xb]               
  1b714:  cmp r0, #0                        
  1b716:  beq #0x1b722                      
  1b718:  strh r4, [r6, #0x32]              
  1b71a:  ldrb r0, [r6, #0xb]               
  1b71c:  cmp r0, #1                        
  1b71e:  beq #0x1b736                      
  1b720:  b #0x1b73c                        -> 0x1b73c (вне списка функций)
  1b722:  ldrh r0, [r6, #0x32]              
  1b724:  movs r3, #0x7d                    
  1b726:  lsls r3, r3, #3                   
  1b728:  cmp r0, r3                        
  1b72a:  bhs #0x1b732                      
  1b72c:  adds r0, r0, #1                   
  1b72e:  strh r0, [r6, #0x32]              
  1b730:  b #0x1b73c                        -> 0x1b73c (вне списка функций)
  1b732:  strb r4, [r6, #0xc]               
  1b734:  b #0x1b73c                        -> 0x1b73c (вне списка функций)
  1b736:  ldrb r0, [r1]                     
  1b738:  cmp r0, #0                        
  1b73a:  beq #0x1b762                      
  1b73c:  ldr r5, [pc, #0x334]              -> RAM
  1b73e:  ldrb r0, [r1]                     
  1b740:  ldr r3, [pc, #0x354]              -> RAM
  1b742:  subs r5, #0x38                    
  1b744:  cmp r0, #1                        
  1b746:  beq #0x1b78e                      
  1b748:  ldr r0, [pc, #0x350]              -> RAM
  1b74a:  ldrh r0, [r0]                     
  1b74c:  cmp r0, #0                        
  1b74e:  beq #0x1b796                      
  1b750:  ldr r0, [pc, #0x340]              -> периферия
  1b752:  ldr r1, [r0, #0x14]               
  1b754:  bics r1, r2                       
  1b756:  str r1, [r0, #0x14]               
  1b758:  ldr r0, [pc, #0x344]              -> RAM
  1b75a:  strb r4, [r0]                     
  1b75c:  strb r4, [r3]                     
  1b75e:  str r4, [r5, #8]                  
  1b760:  pop {r3, r4, r5, r6, r7, pc}      
  1b762:  ldrh r0, [r6, #0x30]              
  1b764:  cmp r0, #0x96                     
  1b766:  bhs #0x1b76e                      
  1b768:  adds r0, r0, #1                   
  1b76a:  strh r0, [r6, #0x30]              
  1b76c:  pop {r3, r4, r5, r6, r7, pc}      
  1b76e:  ldr r0, [pc, #0x334]              -> RAM
  1b770:  ldr r1, [r0]                      
  1b772:  ldr r0, [pc, #0x334]              -> RAM
  1b774:  str r1, [r0]                      
  1b776:  ldr r0, [pc, #0x328]              -> RAM
  1b778:  ldrb r0, [r0]                     
  1b77a:  cmp r0, #1                        
  1b77c:  bne #0x1b786                      
  1b77e:  ldr r0, [pc, #0x314]              -> периферия
  1b780:  ldr r1, [r0, #0x14]               
  1b782:  orrs r1, r2                       
  1b784:  str r1, [r0, #0x14]               
  1b786:  strb r4, [r6, #0xb]               
  1b788:  strh r4, [r6, #0x30]              
  1b78a:  strb r4, [r6, #0xc]               
  1b78c:  pop {r3, r4, r5, r6, r7, pc}      
  1b78e:  strb r4, [r6, #0xb]               
  1b790:  strh r4, [r6, #0x30]              
  1b792:  strb r4, [r6, #0xc]               
  1b794:  b #0x1b750                        -> 0x1b750 (вне списка функций)
  1b796:  ldr r0, [pc, #0x314]              -> RAM
  1b798:  ldrh r0, [r0]                     
  1b79a:  cmp r0, #0                        
  1b79c:  bne #0x1b750                      
  1b79e:  ldr r0, [pc, #0x310]              -> RAM
  1b7a0:  ldrb r0, [r0]                     
  1b7a2:  cmp r0, #0                        
  1b7a4:  bne #0x1b750                      
  1b7a6:  ldr r0, [pc, #0x30c]              -> RAM
  1b7a8:  ldr r1, [pc, #0x30c]              -> RAM
  1b7aa:  ldrb r6, [r0]                     
  1b7ac:  ldr r0, [pc, #0x2ac]              -> RAM
  1b7ae:  adds r0, #0x80                    
  1b7b0:  cmp r6, #1                        
  1b7b2:  beq #0x1b7be                      
  1b7b4:  ldr r3, [pc, #0x304]              -> RAM
  1b7b6:  ldrb r3, [r3]                     
  1b7b8:  cmp r3, #1                        
  1b7ba:  beq #0x1b85e                      
  1b7bc:  b #0x1b866                        -> 0x1b866 (вне списка функций)
  1b7be:  strb r4, [r3]                     
  1b7c0:  ldr r3, [pc, #0x2fc]              -> RAM
  1b7c2:  ldrb r3, [r3]                     
  1b7c4:  cmp r3, #1                        
  1b7c6:  beq #0x1b7d6                      
  1b7c8:  bl #0x1ce38                       -> func_0x1ce38
  1b7cc:  ldr r0, [pc, #0x2f4]              -> RAM
  1b7ce:  movs r1, #8                       
  1b7d0:  ldrsh r1, [r0, r1]                
  1b7d2:  str r1, [r5, #8]                  
  1b7d4:  pop {r3, r4, r5, r6, r7, pc}      
  1b7d6:  ldr r3, [pc, #0x29c]              -> RAM
  1b7d8:  str r4, [r5, #8]                  
  1b7da:  subs r3, #0x2c                    
  1b7dc:  movs r5, #8                       
  1b7de:  ldrsh r5, [r3, r5]                
  1b7e0:  mov r7, r4                        
  1b7e2:  cmp r5, #0xa7                     
  1b7e4:  ble #0x1b7ec                      
  1b7e6:  ldr r4, [pc, #0x2e0]              
  1b7e8:  ldr r3, [pc, #0x2e0]              -> RAM
  1b7ea:  b #0x1b7fe                        -> 0x1b7fe (вне списка функций)
  1b7ec:  ldr r3, [pc, #0x2dc]              -> RAM
  1b7ee:  movs r4, #0                       
  1b7f0:  ldrsh r4, [r3, r4]                
  1b7f2:  ldr r6, [pc, #0x2dc]              
  1b7f4:  cmp r4, r6                        
  1b7f6:  blt #0x1b7fc                      
  1b7f8:  strh r6, [r3]                     
  1b7fa:  b #0x1b800                        -> 0x1b800 (вне списка функций)
  1b7fc:  adds r4, #0x64                    
  1b7fe:  strh r4, [r3]                     
  1b800:  ldr r3, [pc, #0x290]              -> периферия
  1b802:  ldr r4, [r3, #0x14]               
  1b804:  lsls r4, r4, #0x10                
  1b806:  bpl #0x1b84c                      
  1b808:  cmp r5, #0x53                     
  1b80a:  bgt #0x1b844                      
  1b80c:  ldr r2, [pc, #0x2c4]              -> RAM
  1b80e:  movs r4, #0                       
  1b810:  ldrsh r4, [r2, r4]                
  1b812:  ldr r2, [pc, #0x2c4]              -> RAM
  1b814:  movs r3, #0                       
  1b816:  ldrsh r3, [r2, r3]                
  1b818:  cmp r4, r3                        
  1b81a:  bgt #0x1b844                      
  1b81c:  ldr r2, [r1]                      
  1b81e:  ldr r3, [r0, #0x40]               
  1b820:  ldr r1, [r1, #4]                  
  1b822:  ldr r4, [r0, #0x44]               
  1b824:  subs r6, r2, r3                   
  1b826:  mov r5, r1                        
  1b828:  sbcs r5, r4                       
  1b82a:  movs r4, #0x19                    
  1b82c:  lsls r4, r4, #6                   
  1b82e:  movs r3, #0                       
  1b830:  subs r4, r4, r6                   
  1b832:  sbcs r3, r5                       
  1b834:  bhs #0x1b7d4                      
  1b836:  ldr r4, [pc, #0x288]              -> RAM
  1b838:  strb r7, [r4]                     
  1b83a:  ldr r4, [pc, #0x290]              -> RAM
  1b83c:  strh r7, [r4]                     
  1b83e:  str r2, [r0, #0x40]               
  1b840:  str r1, [r0, #0x44]               
  1b842:  pop {r3, r4, r5, r6, r7, pc}      
  1b844:  ldm r1, {r1, r2}                  
  1b846:  str r2, [r0, #0x44]               
  1b848:  str r1, [r0, #0x40]               
  1b84a:  pop {r3, r4, r5, r6, r7, pc}      
  1b84c:  cmp r5, #0x53                     
  1b84e:  ble #0x1b84a                      
  1b850:  ldr r5, [pc, #0x24c]              -> RAM
  1b852:  movs r4, #1                       
  1b854:  strb r4, [r5]                     
  1b856:  ldr r4, [r3, #0x14]               
  1b858:  orrs r4, r2                       
  1b85a:  str r4, [r3, #0x14]               
  1b85c:  b #0x1b844                        -> 0x1b844 (вне списка функций)
  1b85e:  ldr r3, [pc, #0x27c]              -> RAM
  1b860:  ldrb r3, [r3]                     
  1b862:  cmp r3, #1                        
  1b864:  beq #0x1b8f0                      
  1b866:  ldr r3, [pc, #0x20c]              -> RAM
  1b868:  subs r3, #0x2c                    
  1b86a:  ldr r3, [r3, #0x18]               
  1b86c:  str r3, [r5, #8]                  
  1b86e:  mov r7, r3                        
  1b870:  ldr r3, [pc, #0x200]              -> RAM
  1b872:  movs r6, #0xa                     
  1b874:  ldrsh r6, [r3, r6]                
  1b876:  cmp r7, r6                        
  1b878:  ble #0x1b87c                      
  1b87a:  str r6, [r5, #8]                  
  1b87c:  ldr r3, [pc, #0x260]              -> RAM
  1b87e:  ldrb r3, [r3]                     
  1b880:  cmp r3, #1                        
  1b882:  beq #0x1b8f4                      
  1b884:  ldr r3, [pc, #0x238]              -> RAM
  1b886:  ldrb r3, [r3]                     
  1b888:  cmp r3, #1                        
  1b88a:  beq #0x1b8f4                      
  1b88c:  ldr r3, [pc, #0x254]              -> RAM
  1b88e:  ldrb r3, [r3]                     
  1b890:  cmp r3, #0                        
  1b892:  beq #0x1b994                      
  1b894:  movs r3, #0                       
  1b896:  str r3, [r5, #8]                  
  1b898:  ldr r3, [pc, #0x1f8]              -> периферия
  1b89a:  ldr r4, [r3, #0x14]               
  1b89c:  ldr r5, [pc, #0x24c]              -> данные @0x00008
  1b89e:  lsls r4, r4, #0x10                
  1b8a0:  ldr r4, [pc, #0x244]              -> RAM
  1b8a2:  ldrsh r5, [r4, r5]                
  1b8a4:  bpl #0x1b970                      
  1b8a6:  cmp r5, #0x14                     
  1b8a8:  bgt #0x1b966                      
  1b8aa:  ldr r4, [pc, #0x228]              -> RAM
  1b8ac:  movs r5, #0                       
  1b8ae:  ldrsh r5, [r4, r5]                
  1b8b0:  ldr r4, [pc, #0x224]              -> RAM
  1b8b2:  movs r6, #0                       
  1b8b4:  ldrsh r6, [r4, r6]                
  1b8b6:  cmp r5, r6                        
  1b8b8:  bgt #0x1b966                      
  1b8ba:  ldm r1!, {r4, r5}                 
  1b8bc:  str r5, [sp]                      
  1b8be:  ldr r7, [r0, #0x40]               
  1b8c0:  subs r1, #8                       
  1b8c2:  ldr r6, [r0, #0x44]               
  1b8c4:  subs r7, r4, r7                   
  1b8c6:  mov ip, r4                        
  1b8c8:  sbcs r5, r6                       
  1b8ca:  movs r4, #0x19                    
  1b8cc:  lsls r4, r4, #6                   
  1b8ce:  movs r6, #0                       
  1b8d0:  subs r4, r4, r7                   
  1b8d2:  sbcs r6, r5                       
  1b8d4:  bhs #0x1b97c                      
  1b8d6:  ldr r5, [pc, #0x1c8]              -> RAM
  1b8d8:  movs r4, #0                       
  1b8da:  strb r4, [r5]                     
  1b8dc:  ldr r5, [r3, #0x14]               
  1b8de:  bics r5, r2                       
  1b8e0:  str r5, [r3, #0x14]               
  1b8e2:  ldr r2, [pc, #0x1dc]              -> RAM
  1b8e4:  strb r4, [r2]                     
  1b8e6:  ldr r3, [sp]                      
  1b8e8:  mov r2, ip                        
  1b8ea:  str r3, [r0, #0x44]               
  1b8ec:  str r2, [r0, #0x40]               
  1b8ee:  b #0x1b97c                        -> 0x1b97c (вне списка функций)
  1b8f0:  ldr r3, [r5, #4]                  
  1b8f2:  b #0x1b86c                        -> 0x1b86c (вне списка функций)
  1b8f4:  ldr r3, [pc, #0x1cc]              -> RAM
  1b8f6:  movs r5, #8                       
  1b8f8:  ldrsh r5, [r3, r5]                
  1b8fa:  cmp r5, #0x64                     
  1b8fc:  ble #0x1b902                      
  1b8fe:  subs r5, #0x64                    
  1b900:  b #0x1b90a                        -> 0x1b90a (вне списка функций)
  1b902:  movs r6, #0x64                    
  1b904:  cmn r5, r6                        
  1b906:  bge #0x1b90e                      
  1b908:  adds r5, #0x64                    
  1b90a:  strh r5, [r3, #8]                 
  1b90c:  b #0x1b910                        -> 0x1b910 (вне списка функций)
  1b90e:  strh r4, [r3, #8]                 
  1b910:  ldr r5, [pc, #0x1c0]              -> RAM
  1b912:  movs r6, #0                       
  1b914:  ldrsh r6, [r5, r6]                
  1b916:  ldr r5, [pc, #0x1c0]              -> RAM
  1b918:  movs r7, #0                       
  1b91a:  ldrsh r7, [r5, r7]                
  1b91c:  cmp r6, r7                        
  1b91e:  bge #0x1b926                      
  1b920:  ldrh r5, [r3, #8]                 
  1b922:  cmp r5, #0                        
  1b924:  beq #0x1b934                      
  1b926:  ldm r1, {r1, r2}                  
  1b928:  str r2, [r0, #0x44]               
  1b92a:  str r1, [r0, #0x40]               
  1b92c:  strh r4, [r3, #8]                 
  1b92e:  strh r4, [r3, #6]                 
  1b930:  strh r4, [r3, #4]                 
  1b932:  pop {r3, r4, r5, r6, r7, pc}      
  1b934:  ldr r5, [r1]                      
  1b936:  ldr r6, [r0, #0x40]               
  1b938:  ldr r1, [r1, #4]                  
  1b93a:  ldr r0, [r0, #0x44]               
  1b93c:  subs r5, r5, r6                   
  1b93e:  sbcs r1, r0                       
  1b940:  movs r6, #0x7d                    
  1b942:  lsls r6, r6, #6                   
  1b944:  movs r0, #0                       
  1b946:  subs r5, r6, r5                   
  1b948:  sbcs r0, r1                       
  1b94a:  bhs #0x1b92c                      
  1b94c:  ldr r0, [pc, #0x190]              -> RAM
  1b94e:  strb r4, [r0]                     
  1b950:  ldr r0, [pc, #0x16c]              -> RAM
  1b952:  strb r4, [r0]                     
  1b954:  ldr r0, [pc, #0x174]              -> RAM
  1b956:  strh r4, [r0]                     
  1b958:  ldr r0, [pc, #0x144]              -> RAM
  1b95a:  strb r4, [r0]                     
  1b95c:  ldr r0, [pc, #0x134]              -> периферия
  1b95e:  ldr r1, [r0, #0x14]               
  1b960:  bics r1, r2                       
  1b962:  str r1, [r0, #0x14]               
  1b964:  b #0x1b92c                        -> 0x1b92c (вне списка функций)
  1b966:  ldm r1!, {r2, r3}                 
  1b968:  str r3, [r0, #0x44]               
  1b96a:  subs r1, #8                       
  1b96c:  str r2, [r0, #0x40]               
  1b96e:  b #0x1b97c                        -> 0x1b97c (вне списка функций)
  1b970:  cmp r5, #0x3e                     
  1b972:  ble #0x1b97c                      
  1b974:  ldr r4, [pc, #0x178]              -> RAM
  1b976:  ldrb r4, [r4]                     
  1b978:  cmp r4, #1                        
  1b97a:  beq #0x1b986                      
  1b97c:  ldm r1, {r1, r2}                  
  1b97e:  str r2, [r0, #0x4c]               
  1b980:  str r1, [r0, #0x48]               
  1b982:  pop {r3, r4, r5, r6, r7, pc}      
  1b984:  b #0x1b994                        -> 0x1b994 (вне списка функций)
  1b986:  ldr r5, [pc, #0x118]              -> RAM
  1b988:  movs r4, #1                       
  1b98a:  strb r4, [r5]                     
  1b98c:  ldr r4, [r3, #0x14]               
  1b98e:  orrs r4, r2                       
  1b990:  str r4, [r3, #0x14]               
  1b992:  b #0x1b966                        -> 0x1b966 (вне списка функций)
  1b994:  ldr r3, [pc, #0xfc]               -> периферия
  1b996:  ldr r3, [r3, #0x14]               
  1b998:  lsls r3, r3, #0x10                
  1b99a:  bpl #0x1ba58                      
  1b99c:  ldr r3, [pc, #0xd8]               -> RAM
  1b99e:  ldrb r3, [r3]                     
  1b9a0:  cmp r3, #0                        
  1b9a2:  bne #0x1b9ac                      
  1b9a4:  ldr r3, [pc, #0x14c]              -> RAM
  1b9a6:  ldrb r3, [r3]                     
  1b9a8:  cmp r3, #0                        
  1b9aa:  beq #0x1b9f6                      
  1b9ac:  ldr r3, [r5, #8]                  
  1b9ae:  cmp r3, #0                        
  1b9b0:  bgt #0x1ba4e                      
  1b9b2:  ldr r3, [pc, #0x120]              -> RAM
  1b9b4:  movs r5, #0                       
  1b9b6:  ldrsh r5, [r3, r5]                
  1b9b8:  ldr r3, [pc, #0x13c]              -> RAM
  1b9ba:  movs r6, #0                       
  1b9bc:  ldrsh r6, [r3, r6]                
  1b9be:  cmp r5, r6                        
  1b9c0:  bgt #0x1ba4e                      
  1b9c2:  ldm r1!, {r3, r5}                 
  1b9c4:  str r5, [sp]                      
  1b9c6:  ldr r7, [r0, #0x48]               
  1b9c8:  subs r1, #8                       
  1b9ca:  ldr r6, [r0, #0x4c]               
  1b9cc:  subs r7, r3, r7                   
  1b9ce:  mov ip, r3                        
  1b9d0:  sbcs r5, r6                       
  1b9d2:  movs r3, #0x19                    
  1b9d4:  lsls r3, r3, #6                   
  1b9d6:  movs r6, #0                       
  1b9d8:  subs r3, r3, r7                   
  1b9da:  sbcs r6, r5                       
  1b9dc:  blo #0x1b9e0                      
  1b9de:  b #0x1b844                        -> 0x1b844 (вне списка функций)
  1b9e0:  ldr r3, [pc, #0xbc]               -> RAM
  1b9e2:  strb r4, [r3]                     
  1b9e4:  ldr r3, [pc, #0xac]               -> периферия
  1b9e6:  ldr r4, [r3, #0x14]               
  1b9e8:  bics r4, r2                       
  1b9ea:  str r4, [r3, #0x14]               
  1b9ec:  ldr r3, [sp]                      
  1b9ee:  mov r2, ip                        
  1b9f0:  str r3, [r0, #0x4c]               
  1b9f2:  str r2, [r0, #0x48]               
  1b9f4:  b #0x1b844                        -> 0x1b844 (вне списка функций)
  1b9f6:  ldr r3, [r5, #8]                  
  1b9f8:  cmp r3, #0                        
  1b9fa:  bgt #0x1b9de                      
  1b9fc:  ldr r3, [pc, #0xe8]               -> RAM
  1b9fe:  movs r5, #8                       
  1ba00:  ldrsh r5, [r3, r5]                
  1ba02:  cmp r5, #0x3e                     
  1ba04:  bgt #0x1ba4e                      
  1ba06:  ldr r3, [pc, #0xa0]               -> RAM
  1ba08:  ldr r5, [r3]                      
  1ba0a:  movs r3, #0x32                    
  1ba0c:  cmn r5, r3                        
  1ba0e:  ble #0x1ba4e                      
  1ba10:  ldr r3, [pc, #0xc0]               -> RAM
  1ba12:  movs r5, #0                       
  1ba14:  ldrsh r5, [r3, r5]                
  1ba16:  ldr r3, [pc, #0xc0]               -> RAM
  1ba18:  movs r6, #0                       
  1ba1a:  ldrsh r6, [r3, r6]                
  1ba1c:  cmp r5, r6                        
  1ba1e:  bgt #0x1ba4e                      
  1ba20:  ldm r1!, {r3, r5}                 
  1ba22:  str r5, [sp]                      
  1ba24:  ldr r7, [r0, #0x48]               
  1ba26:  subs r1, #8                       
  1ba28:  ldr r6, [r0, #0x4c]               
  1ba2a:  subs r7, r3, r7                   
  1ba2c:  mov ip, r3                        
  1ba2e:  sbcs r5, r6                       
  1ba30:  movs r3, #0x19                    
  1ba32:  lsls r3, r3, #6                   
  1ba34:  movs r6, #0                       
  1ba36:  subs r3, r3, r7                   
  1ba38:  sbcs r6, r5                       
  1ba3a:  bhs #0x1b9de                      
  1ba3c:  ldr r3, [pc, #0x60]               -> RAM
  1ba3e:  strb r4, [r3]                     
  1ba40:  ldr r3, [pc, #0x50]               -> периферия
  1ba42:  ldr r5, [r3, #0x14]               
  1ba44:  bics r5, r2                       
  1ba46:  str r5, [r3, #0x14]               
  1ba48:  ldr r2, [pc, #0x74]               -> RAM
  1ba4a:  strb r4, [r2]                     
  1ba4c:  b #0x1b9ec                        -> 0x1b9ec (вне списка функций)
  1ba4e:  ldm r1!, {r2, r3}                 
  1ba50:  str r3, [r0, #0x4c]               
  1ba52:  subs r1, #8                       
  1ba54:  str r2, [r0, #0x48]               
  1ba56:  b #0x1b844                        -> 0x1b844 (вне списка функций)
  1ba58:  b #0x1bafc                        -> 0x1bafc (вне списка функций)
  1ba5a:  movs r0, r0                       
  1ba5c:  lsls r0, r1, #0xf                 
  1ba5e:  movs r0, #0                       
  1ba60:  lsls r2, r1, #9                   
  1ba62:  movs r0, #0                       
  1ba64:  lsls r4, r1, #9                   
  1ba66:  movs r0, #0                       
  1ba68:  add r0, sp, #0x320                
  1ba6a:  movs r0, r0                       
  1ba6c:  lsls r6, r1, #9                   
  1ba6e:  movs r0, #0                       
  1ba70:  lsls r4, r1, #0xc                 
  1ba72:  movs r0, #0                       
  1ba74:  asrs r4, r2, #0x1e                
  1ba76:  movs r0, #0                       
  1ba78:  lsls r0, r3, #0xc                 
  1ba7a:  movs r0, #0                       
  1ba7c:  lsrs r0, r7, #0xe                 
  1ba7e:  movs r0, r0                       
  1ba80:  lsls r4, r2, #0xe                 
  1ba82:  movs r0, #0                       
  1ba84:  lsls r4, r3, #0xe                 
  1ba86:  movs r0, #0                       
  1ba88:  lsls r4, r5, #9                   
  1ba8a:  movs r0, #0                       
  1ba8c:  lsls r2, r7, #7                   
  1ba8e:  movs r0, #0                       
  1ba90:  lsls r5, r0, #9                   
  1ba92:  movs r0, #0                       
  1ba94:  cmp r4, #0x40                     
  1ba96:  ands r1, r0                       
  1ba98:  lsls r0, r0, #0xa                 
  1ba9a:  movs r0, #0                       
  1ba9c:  lsls r6, r3, #8                   
  1ba9e:  movs r0, #0                       
  1baa0:  lsls r0, r3, #8                   
  1baa2:  movs r0, #0                       
  1baa4:  lsls r4, r4, #8                   
  1baa6:  movs r0, #0                       
  1baa8:  lsls r0, r1, #0xe                 
  1baaa:  movs r0, #0                       
  1baac:  lsls r0, r4, #8                   
  1baae:  movs r0, #0                       
  1bab0:  lsls r4, r5, #2                   
  1bab2:  movs r0, #0                       
  1bab4:  lsls r6, r5, #8                   
  1bab6:  movs r0, #0                       
  1bab8:  lsls r0, r4, #7                   
  1baba:  movs r0, #0                       
  1babc:  lsls r1, r7, #0xc                 
  1babe:  movs r0, #0                       
  1bac0:  lsls r2, r3, #0xc                 
  1bac2:  movs r0, #0                       
  1bac4:  asrs r2, r3, #0x1a                
  1bac6:  movs r0, #0                       
  1bac8:  bhi #0x1baac                      
  1baca:  .byte 0xff, 0xff                  
  1bacc:  lsls r4, r4, #9                   
  1bace:  movs r0, #0                       
  1bad0:  .byte 0x18, 0xfc                  
  1bad2:  .byte 0xff, 0xff                  
  1bad4:  lsls r6, r5, #9                   
  1bad6:  movs r0, #0                       
  1bad8:  lsls r4, r2, #8                   
  1bada:  movs r0, #0                       
  1badc:  lsls r2, r7, #0xc                 
  1bade:  movs r0, #0                       
  1bae0:  lsls r2, r5, #9                   
  1bae2:  movs r0, #0                       
  1bae4:  lsls r3, r4, #9                   
  1bae6:  movs r0, #0                       
  1bae8:  asrs r0, r5, #0x1d                
  1baea:  movs r0, #0                       
  1baec:  movs r0, r1                       
  1baee:  movs r0, r0                       
  1baf0:  lsls r0, r0, #0xe                 
  1baf2:  movs r0, #0                       
  1baf4:  lsls r1, r6, #8                   
  1baf6:  movs r0, #0                       
  1baf8:  lsls r2, r2, #8                   
  1bafa:  movs r0, #0                       
  1bafc:  ldr r3, [r5, #8]                  
  1bafe:  cmp r3, #0                        
  1bb00:  ble #0x1ba4e                      
  1bb02:  ldr r4, [pc, #0x10]               -> RAM
  1bb04:  movs r3, #1                       
  1bb06:  strb r3, [r4]                     
  1bb08:  ldr r3, [pc, #0xc]                -> периферия
  1bb0a:  ldr r4, [r3, #0x14]               
  1bb0c:  orrs r4, r2                       
  1bb0e:  str r4, [r3, #0x14]               
  1bb10:  b #0x1ba4e                        -> 0x1ba4e (вне списка функций)
  ; --- literal-пул @0x1ba5c (40 слов) ---
  1ba5c:  .word 0x200003c8  ; RAM
  1ba60:  .word 0x2000024a  ; RAM
  1ba64:  .word 0x2000024c  ; RAM
  1ba68:  .word 0x0000a8c8  ; данные @0x0a8c8
  1ba6c:  .word 0x2000024e  ; RAM
  1ba70:  .word 0x2000030c  ; RAM
  1ba74:  .word 0x20001794  ; RAM
  1ba78:  .word 0x20000318  ; RAM
  1ba7c:  .word 0x00000bb8  ; данные @0x00bb8
  1ba80:  .word 0x20000394  ; RAM
  1ba84:  .word 0x2000039c  ; RAM
  1ba88:  .word 0x2000026c  ; RAM
  1ba8c:  .word 0x200001fa  ; RAM
  1ba90:  .word 0x20000245  ; RAM
  1ba94:  .word 0x40012c40  ; периферия
  1ba98:  .word 0x20000280  ; RAM
  1ba9c:  .word 0x2000021e  ; RAM
  1baa0:  .word 0x20000218  ; RAM
  1baa4:  .word 0x20000224  ; RAM
  1baa8:  .word 0x20000388  ; RAM
  1baac:  .word 0x20000220  ; RAM
  1bab0:  .word 0x200000ac  ; RAM
  1bab4:  .word 0x2000022e  ; RAM
  1bab8:  .word 0x200001e0  ; RAM
  1babc:  .word 0x20000339  ; RAM
  1bac0:  .word 0x2000031a  ; RAM
  1bac4:  .word 0x2000169a  ; RAM
  1bac8:  .word 0xffffd8f0
  1bacc:  .word 0x20000264  ; RAM
  1bad0:  .word 0xfffffc18
  1bad4:  .word 0x2000026e  ; RAM
  1bad8:  .word 0x20000214  ; RAM
  1badc:  .word 0x2000033a  ; RAM
  1bae0:  .word 0x2000026a  ; RAM
  1bae4:  .word 0x20000263  ; RAM
  1bae8:  .word 0x20001768  ; RAM
  1baec:  .word 0x00000008  ; данные @0x00008
  1baf0:  .word 0x20000380  ; RAM
  1baf4:  .word 0x20000231  ; RAM
  1baf8:  .word 0x20000212  ; RAM
  ; --- literal-пул @0x1bb14 (2 слов) — ВНЕ границ функции ---
  1bb14:  .word 0x20000218  ; RAM
  1bb18:  .word 0x40012c40  ; периферия
```
