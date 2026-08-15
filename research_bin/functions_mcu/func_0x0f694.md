# func_0x0f694

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f694) | `0x0000f694` |
| размер кода | 746 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f10 — RAM (r1)
- 0x20000f95 — RAM (r1)
- 0x20001264 — RAM (r1)
- 0x20001271 — RAM (r1)
- 0x2000127e — RAM (r2)

## Вызовы (callees)

- 0x0f83e (b, вне списка функций)
- 0x0f8ae (b, вне списка функций)
- 0x0f8de (b, вне списка функций)
- 0x0f8e2 (b, вне списка функций)
- 0x0f958 (b, вне списка функций)
- 0x0f97c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11978` (bl @0x0001198a)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0f708..0x0f70a` (2 Б); цели из: 0x0f6da
- `0x0f70a..0x0f762` (88 Б); цели из: 0x0f69c, 0x0f6ae, 0x0f6c2
- `0x0f762..0x0f7ba` (88 Б); цели из: 0x0f71a, 0x0f72e
- `0x0f7ba..0x0f838` (126 Б); цели из: 0x0f772, 0x0f786
- `0x0f838..0x0f83e` (6 Б); цели из: 0x0f7ca, 0x0f7dc, 0x0f7f0, 0x0f804
- `0x0f83e..0x0f87e` (64 Б); цели из: 0x0f708, 0x0f746, 0x0f760, 0x0f79e…
- `0x0f87e..0x0f8ae` (48 Б); цели из: 0x0f84a
- `0x0f8ae..0x0f8d8` (42 Б); цели из: 0x0f862, 0x0f87c, 0x0f894
- `0x0f8d8..0x0f8de` (6 Б); цели из: 0x0f8b4
- `0x0f8de..0x0f8e2` (4 Б); цели из: 0x0f8c6, 0x0f8d6
- `0x0f8e2..0x0f928` (70 Б); цели из: 0x0f698
- `0x0f928..0x0f958` (48 Б); цели из: 0x0f8f4
- `0x0f958..0x0f97c` (36 Б); цели из: 0x0f8e8, 0x0f90c, 0x0f926, 0x0f93e
- `0x0f97c..0x0f97e` (2 Б); цели из: 0x0f96e

## Дизассембляция

```asm
  0f694:  movs r0, #0                       
  0f696:  nop                               
  0f698:  b #0xf8e2                         -> 0x0f8e2 (вне списка функций)
  0f69a:  cmp r0, #0xb                      
  0f69c:  bge #0xf70a                       
  0f69e:  ldr r1, [pc, #0x2e0]              -> RAM
  0f6a0:  ldrh.w r2, [r1, r0, lsl #1]       
  0f6a4:  ldr r1, [pc, #0x2dc]              -> RAM
  0f6a6:  ldrh r1, [r1, #4]                 
  0f6a8:  sub.w r1, r1, #0x320              
  0f6ac:  cmp r2, r1                        
  0f6ae:  bge #0xf70a                       
  0f6b0:  ldr r2, [pc, #0x2cc]              -> RAM
  0f6b2:  adds r1, r0, #2                   
  0f6b4:  ldrh.w r2, [r2, r1, lsl #1]       
  0f6b8:  ldr r1, [pc, #0x2c8]              -> RAM
  0f6ba:  ldrh r1, [r1, #4]                 
  0f6bc:  add.w r1, r1, #0x2bc              
  0f6c0:  cmp r2, r1                        
  0f6c2:  ble #0xf70a                       
  0f6c4:  ldr r1, [pc, #0x2c0]              -> RAM
  0f6c6:  ldrb r1, [r1, r0]                 
  0f6c8:  adds r1, r1, #1                   
  0f6ca:  ldr r2, [pc, #0x2bc]              -> RAM
  0f6cc:  strb r1, [r2, r0]                 
  0f6ce:  movs r1, #0                       
  0f6d0:  ldr r2, [pc, #0x2b8]              -> RAM
  0f6d2:  strb r1, [r2, r0]                 
  0f6d4:  ldr r1, [pc, #0x2b0]              -> RAM
  0f6d6:  ldrb r1, [r1, r0]                 
  0f6d8:  cmp r1, #0x64                     
  0f6da:  blt #0xf708                       
  0f6dc:  ldr r1, [pc, #0x2a4]              -> RAM
  0f6de:  ldr.w r1, [r1, #0x11]             
  0f6e2:  movs r2, #1                       
  0f6e4:  lsls r2, r0                       
  0f6e6:  orrs r1, r2                       
  0f6e8:  ldr r2, [pc, #0x298]              -> RAM
  0f6ea:  str.w r1, [r2, #0x11]             
  0f6ee:  mov r1, r2                        
  0f6f0:  ldr.w r1, [r1, #0x11]             
  0f6f4:  adds r2, r0, #1                   
  0f6f6:  movs r3, #1                       
  0f6f8:  lsls r3, r2                       
  0f6fa:  orrs r1, r3                       
  0f6fc:  ldr r2, [pc, #0x284]              -> RAM
  0f6fe:  str.w r1, [r2, #0x11]             
  0f702:  movs r1, #0                       
  0f704:  ldr r2, [pc, #0x280]              -> RAM
  0f706:  strb r1, [r2, r0]                 
  0f708:  b #0xf83e                         -> 0x0f83e (вне списка функций)
  0f70a:  ldr r1, [pc, #0x274]              -> RAM
  0f70c:  ldrh.w r2, [r1, r0, lsl #1]       
  0f710:  ldr r1, [pc, #0x270]              -> RAM
  0f712:  ldrh r1, [r1, #4]                 
  0f714:  sub.w r1, r1, #0x320              
  0f718:  cmp r2, r1                        
  0f71a:  bge #0xf762                       
  0f71c:  ldr r2, [pc, #0x260]              -> RAM
  0f71e:  adds r1, r0, #1                   
  0f720:  ldrh.w r2, [r2, r1, lsl #1]       
  0f724:  ldr r1, [pc, #0x25c]              -> RAM
  0f726:  ldrh r1, [r1, #4]                 
  0f728:  add.w r1, r1, #0x2bc              
  0f72c:  cmp r2, r1                        
  0f72e:  ble #0xf762                       
  0f730:  ldr r1, [pc, #0x254]              -> RAM
  0f732:  ldrb r1, [r1, r0]                 
  0f734:  adds r1, r1, #1                   
  0f736:  ldr r2, [pc, #0x250]              -> RAM
  0f738:  strb r1, [r2, r0]                 
  0f73a:  movs r1, #0                       
  0f73c:  ldr r2, [pc, #0x24c]              -> RAM
  0f73e:  strb r1, [r2, r0]                 
  0f740:  ldr r1, [pc, #0x244]              -> RAM
  0f742:  ldrb r1, [r1, r0]                 
  0f744:  cmp r1, #0x64                     
  0f746:  blt #0xf83e                       
  0f748:  ldr r1, [pc, #0x238]              -> RAM
  0f74a:  ldr.w r1, [r1, #0x11]             
  0f74e:  movs r2, #1                       
  0f750:  lsls r2, r0                       
  0f752:  orrs r1, r2                       
  0f754:  ldr r2, [pc, #0x22c]              -> RAM
  0f756:  str.w r1, [r2, #0x11]             
  0f75a:  movs r1, #0                       
  0f75c:  ldr r2, [pc, #0x228]              -> RAM
  0f75e:  strb r1, [r2, r0]                 
  0f760:  b #0xf83e                         -> 0x0f83e (вне списка функций)
  0f762:  ldr r1, [pc, #0x21c]              -> RAM
  0f764:  ldrh.w r2, [r1, r0, lsl #1]       
  0f768:  ldr r1, [pc, #0x218]              -> RAM
  0f76a:  ldrh r1, [r1, #4]                 
  0f76c:  sub.w r1, r1, #0x320              
  0f770:  cmp r2, r1                        
  0f772:  bge #0xf7ba                       
  0f774:  ldr r2, [pc, #0x208]              -> RAM
  0f776:  adds r1, r0, #1                   
  0f778:  ldrh.w r2, [r2, r1, lsl #1]       
  0f77c:  ldr r1, [pc, #0x204]              -> RAM
  0f77e:  ldrh r1, [r1, #4]                 
  0f780:  sub.w r1, r1, #0x320              
  0f784:  cmp r2, r1                        
  0f786:  bge #0xf7ba                       
  0f788:  ldr r1, [pc, #0x1fc]              -> RAM
  0f78a:  ldrb r1, [r1, r0]                 
  0f78c:  adds r1, r1, #1                   
  0f78e:  ldr r2, [pc, #0x1f8]              -> RAM
  0f790:  strb r1, [r2, r0]                 
  0f792:  movs r1, #0                       
  0f794:  ldr r2, [pc, #0x1f4]              -> RAM
  0f796:  strb r1, [r2, r0]                 
  0f798:  ldr r1, [pc, #0x1ec]              -> RAM
  0f79a:  ldrb r1, [r1, r0]                 
  0f79c:  cmp r1, #0x64                     
  0f79e:  blt #0xf83e                       
  0f7a0:  ldr r1, [pc, #0x1e0]              -> RAM
  0f7a2:  ldr.w r1, [r1, #0x11]             
  0f7a6:  movs r2, #1                       
  0f7a8:  lsls r2, r0                       
  0f7aa:  orrs r1, r2                       
  0f7ac:  ldr r2, [pc, #0x1d4]              -> RAM
  0f7ae:  str.w r1, [r2, #0x11]             
  0f7b2:  movs r1, #0                       
  0f7b4:  ldr r2, [pc, #0x1d0]              -> RAM
  0f7b6:  strb r1, [r2, r0]                 
  0f7b8:  b #0xf83e                         -> 0x0f83e (вне списка функций)
  0f7ba:  ldr r1, [pc, #0x1c4]              -> RAM
  0f7bc:  ldrh.w r2, [r1, r0, lsl #1]       
  0f7c0:  ldr r1, [pc, #0x1c0]              -> RAM
  0f7c2:  ldrh r1, [r1, #4]                 
  0f7c4:  sub.w r1, r1, #0x12c              
  0f7c8:  cmp r2, r1                        
  0f7ca:  ble #0xf838                       
  0f7cc:  ldr r1, [pc, #0x1b0]              -> RAM
  0f7ce:  ldrh.w r2, [r1, r0, lsl #1]       
  0f7d2:  ldr r1, [pc, #0x1b0]              -> RAM
  0f7d4:  ldrh r1, [r1, #4]                 
  0f7d6:  add.w r1, r1, #0x12c              
  0f7da:  cmp r2, r1                        
  0f7dc:  bge #0xf838                       
  0f7de:  ldr r2, [pc, #0x1a0]              -> RAM
  0f7e0:  adds r1, r0, #1                   
  0f7e2:  ldrh.w r2, [r2, r1, lsl #1]       
  0f7e6:  ldr r1, [pc, #0x19c]              -> RAM
  0f7e8:  ldrh r1, [r1, #4]                 
  0f7ea:  sub.w r1, r1, #0x12c              
  0f7ee:  cmp r2, r1                        
  0f7f0:  ble #0xf838                       
  0f7f2:  ldr r2, [pc, #0x18c]              -> RAM
  0f7f4:  adds r1, r0, #1                   
  0f7f6:  ldrh.w r2, [r2, r1, lsl #1]       
  0f7fa:  ldr r1, [pc, #0x188]              -> RAM
  0f7fc:  ldrh r1, [r1, #4]                 
  0f7fe:  add.w r1, r1, #0x12c              
  0f802:  cmp r2, r1                        
  0f804:  bge #0xf838                       
  0f806:  ldr r1, [pc, #0x184]              -> RAM
  0f808:  ldrb r1, [r1, r0]                 
  0f80a:  adds r1, r1, #1                   
  0f80c:  ldr r2, [pc, #0x17c]              -> RAM
  0f80e:  strb r1, [r2, r0]                 
  0f810:  movs r1, #0                       
  0f812:  ldr r2, [pc, #0x174]              -> RAM
  0f814:  strb r1, [r2, r0]                 
  0f816:  ldr r1, [pc, #0x174]              -> RAM
  0f818:  ldrb r1, [r1, r0]                 
  0f81a:  cmp r1, #0x32                     
  0f81c:  blt #0xf83e                       
  0f81e:  ldr r1, [pc, #0x164]              -> RAM
  0f820:  ldr.w r1, [r1, #0x11]             
  0f824:  movs r2, #1                       
  0f826:  lsls r2, r0                       
  0f828:  bics r1, r2                       
  0f82a:  ldr r2, [pc, #0x158]              -> RAM
  0f82c:  str.w r1, [r2, #0x11]             
  0f830:  movs r1, #0                       
  0f832:  ldr r2, [pc, #0x158]              -> RAM
  0f834:  strb r1, [r2, r0]                 
  0f836:  b #0xf83e                         -> 0x0f83e (вне списка функций)
  0f838:  movs r1, #0                       
  0f83a:  ldr r2, [pc, #0x150]              -> RAM
  0f83c:  strb r1, [r2, r0]                 
  0f83e:  cbnz r0, #0xf8ae                  
  0f840:  ldr r1, [pc, #0x13c]              -> RAM
  0f842:  ldrh.w r1, [r1, r0, lsl #1]       
  0f846:  cmp.w r1, #0x3e8                  
  0f84a:  bge #0xf87e                       
  0f84c:  ldr r1, [pc, #0x138]              -> RAM
  0f84e:  ldrb r1, [r1, r0]                 
  0f850:  adds r1, r1, #1                   
  0f852:  ldr r2, [pc, #0x134]              -> RAM
  0f854:  strb r1, [r2, r0]                 
  0f856:  movs r1, #0                       
  0f858:  ldr r2, [pc, #0x130]              -> RAM
  0f85a:  strb r1, [r2, r0]                 
  0f85c:  ldr r1, [pc, #0x128]              -> RAM
  0f85e:  ldrb r1, [r1, r0]                 
  0f860:  cmp r1, #0x64                     
  0f862:  blt #0xf8ae                       
  0f864:  ldr r1, [pc, #0x11c]              -> RAM
  0f866:  ldr.w r2, [r1, #0x11]             
  0f86a:  movs r1, #1                       
  0f86c:  lsls r1, r0                       
  0f86e:  orrs r2, r1                       
  0f870:  ldr r1, [pc, #0x110]              -> RAM
  0f872:  str.w r2, [r1, #0x11]             
  0f876:  movs r1, #0                       
  0f878:  ldr r2, [pc, #0x10c]              -> RAM
  0f87a:  strb r1, [r2, r0]                 
  0f87c:  b #0xf8ae                         -> 0x0f8ae (вне списка функций)
  0f87e:  ldr r1, [pc, #0x10c]              -> RAM
  0f880:  ldrb r1, [r1, r0]                 
  0f882:  adds r1, r1, #1                   
  0f884:  ldr r2, [pc, #0x104]              -> RAM
  0f886:  strb r1, [r2, r0]                 
  0f888:  movs r1, #0                       
  0f88a:  ldr r2, [pc, #0xfc]               -> RAM
  0f88c:  strb r1, [r2, r0]                 
  0f88e:  ldr r1, [pc, #0xfc]               -> RAM
  0f890:  ldrb r1, [r1, r0]                 
  0f892:  cmp r1, #0x32                     
  0f894:  blt #0xf8ae                       
  0f896:  ldr r1, [pc, #0xec]               -> RAM
  0f898:  ldr.w r2, [r1, #0x11]             
  0f89c:  movs r1, #1                       
  0f89e:  lsls r1, r0                       
  0f8a0:  bics r2, r1                       
  0f8a2:  ldr r1, [pc, #0xe0]               -> RAM
  0f8a4:  str.w r2, [r1, #0x11]             
  0f8a8:  movs r1, #0                       
  0f8aa:  ldr r2, [pc, #0xe0]               -> RAM
  0f8ac:  strb r1, [r2, r0]                 
  0f8ae:  ldr r1, [pc, #0xd8]               -> RAM
  0f8b0:  ldrb r1, [r1, r0]                 
  0f8b2:  cmp r1, #1                        
  0f8b4:  blt #0xf8d8                       
  0f8b6:  ldr r1, [pc, #0xd8]               -> RAM
  0f8b8:  ldrb r1, [r1, r0]                 
  0f8ba:  adds r1, r1, #1                   
  0f8bc:  ldr r2, [pc, #0xd0]               -> RAM
  0f8be:  strb r1, [r2, r0]                 
  0f8c0:  mov r1, r2                        
  0f8c2:  ldrb r1, [r1, r0]                 
  0f8c4:  cmp r1, #0x1e                     
  0f8c6:  blt #0xf8de                       
  0f8c8:  movs r1, #0                       
  0f8ca:  strb r1, [r2, r0]                 
  0f8cc:  ldr r1, [pc, #0xb8]               -> RAM
  0f8ce:  ldrb r1, [r1, r0]                 
  0f8d0:  subs r1, r1, #1                   
  0f8d2:  ldr r2, [pc, #0xb4]               -> RAM
  0f8d4:  strb r1, [r2, r0]                 
  0f8d6:  b #0xf8de                         -> 0x0f8de (вне списка функций)
  0f8d8:  movs r1, #0                       
  0f8da:  ldr r2, [pc, #0xb4]               -> RAM
  0f8dc:  strb r1, [r2, r0]                 
  0f8de:  adds r1, r0, #1                   
  0f8e0:  uxtb r0, r1                       
  0f8e2:  cmp r0, #0xc                      
  0f8e4:  blt.w #0xf69a                     
  0f8e8:  bne #0xf958                       
  0f8ea:  ldr r1, [pc, #0x94]               -> RAM
  0f8ec:  ldrh.w r1, [r1, r0, lsl #1]       
  0f8f0:  cmp.w r1, #0x3e8                  
  0f8f4:  bge #0xf928                       
  0f8f6:  ldr r1, [pc, #0x90]               -> RAM
  0f8f8:  ldrb r1, [r1, r0]                 
  0f8fa:  adds r1, r1, #1                   
  0f8fc:  ldr r2, [pc, #0x88]               -> RAM
  0f8fe:  strb r1, [r2, r0]                 
  0f900:  movs r1, #0                       
  0f902:  ldr r2, [pc, #0x88]               -> RAM
  0f904:  strb r1, [r2, r0]                 
  0f906:  ldr r1, [pc, #0x80]               -> RAM
  0f908:  ldrb r1, [r1, r0]                 
  0f90a:  cmp r1, #0x64                     
  0f90c:  blt #0xf958                       
  0f90e:  ldr r1, [pc, #0x74]               -> RAM
  0f910:  ldr.w r1, [r1, #0x11]             
  0f914:  movs r2, #1                       
  0f916:  lsls r2, r0                       
  0f918:  orrs r1, r2                       
  0f91a:  ldr r2, [pc, #0x68]               -> RAM
  0f91c:  str.w r1, [r2, #0x11]             
  0f920:  movs r1, #0                       
  0f922:  ldr r2, [pc, #0x64]               -> RAM
  0f924:  strb r1, [r2, r0]                 
  0f926:  b #0xf958                         -> 0x0f958 (вне списка функций)
  0f928:  ldr r1, [pc, #0x60]               -> RAM
  0f92a:  ldrb r1, [r1, r0]                 
  0f92c:  adds r1, r1, #1                   
  0f92e:  ldr r2, [pc, #0x5c]               -> RAM
  0f930:  strb r1, [r2, r0]                 
  0f932:  movs r1, #0                       
  0f934:  ldr r2, [pc, #0x50]               -> RAM
  0f936:  strb r1, [r2, r0]                 
  0f938:  ldr r1, [pc, #0x50]               -> RAM
  0f93a:  ldrb r1, [r1, r0]                 
  0f93c:  cmp r1, #0x32                     
  0f93e:  blt #0xf958                       
  0f940:  ldr r1, [pc, #0x40]               -> RAM
  0f942:  ldr.w r2, [r1, #0x11]             
  0f946:  movs r1, #1                       
  0f948:  lsls r1, r0                       
  0f94a:  bics r2, r1                       
  0f94c:  ldr r1, [pc, #0x34]               -> RAM
  0f94e:  str.w r2, [r1, #0x11]             
  0f952:  movs r1, #0                       
  0f954:  ldr r2, [pc, #0x34]               -> RAM
  0f956:  strb r1, [r2, r0]                 
  0f958:  ldr r1, [pc, #0x28]               -> RAM
  0f95a:  ldr.w r1, [r1, #0x11]             
  0f95e:  cbz r1, #0xf970                   
  0f960:  ldr r1, [pc, #0x20]               -> RAM
  0f962:  ldrb r1, [r1, #0xc]               
  0f964:  bic r1, r1, #0x80                 
  0f968:  adds r1, #0x80                    
  0f96a:  ldr r2, [pc, #0x18]               -> RAM
  0f96c:  strb r1, [r2, #0xc]               
  0f96e:  b #0xf97c                         -> 0x0f97c (вне списка функций)
  0f970:  ldr r1, [pc, #0x10]               -> RAM
  0f972:  ldrb r1, [r1, #0xc]               
  0f974:  bic r1, r1, #0x80                 
  0f978:  ldr r2, [pc, #8]                  -> RAM
  0f97a:  strb r1, [r2, #0xc]               
  0f97c:  bx lr                             
  ; --- literal-пул @0x0f980 (5 слов) — ВНЕ границ функции ---
  0f980:  .word 0x20000f10  ; RAM
  0f984:  .word 0x20000f95  ; RAM
  0f988:  .word 0x20001264  ; RAM
  0f98c:  .word 0x2000127e  ; RAM
  0f990:  .word 0x20001271  ; RAM
```
