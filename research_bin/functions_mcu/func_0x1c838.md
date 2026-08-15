# func_0x1c838

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001c838) | `0x0001c838` |
| размер кода | 1466 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000003e7 — данные @0x003e7 (r0)
- 0x000006ed — данные @0x006ed (r0)
- 0x000008c9 — данные @0x008c9 (r1)
- 0x0000094e — данные @0x0094e (r1)
- 0x00007ff8 — данные @0x07ff8 (r2)
- 0x0801f400 — flash-mirror @0x1f400 (r6)
- 0x0801f600 — func_0x1f600 (r0)
- 0x0801f800 — flash-mirror @0x1f800 (r3)
- 0x20000110 — RAM (r7)
- 0x200001e0 — RAM (r0)
- 0x200001e8 — RAM (r7)
- 0x200001ea — RAM (r1)
- 0x200001ec — RAM (r1)
- 0x200001ee — RAM (r1)
- 0x200001f2 — RAM (r0)
- 0x200001f4 — RAM (r1)
- 0x200001f6 — RAM (r1)
- 0x200001f8 — RAM (r0)
- 0x200001fa — RAM (r1)
- 0x200001fc — RAM (r1)
- 0x200001fe — RAM (r1)
- 0x20000200 — RAM (r1)
- 0x20000202 — RAM (r1)
- 0x20000204 — RAM (r1)
- 0x20000206 — RAM (r0)
- 0x20000208 — RAM (r1)
- 0x2000020a — RAM (r1)
- 0x2000020c — RAM (r1)
- 0x2000020e — RAM (r1)
- 0x20000210 — RAM (r1)
- 0x20000212 — RAM (r1)
- 0x20000214 — RAM (r0)
- 0x20000216 — RAM (r1)
- 0x20000241 — RAM (r1)
- 0x20000242 — RAM (r1)
- 0x20000248 — RAM (r0)
- 0x2000024c — RAM (r1)
- 0x2000024e — RAM (r5)
- 0x20000254 — RAM (r3)
- 0x20000258 — RAM (r3)
- 0x2000025c — RAM (r3)
- 0x20000266 — RAM (r1)
- 0x20000324 — RAM (r1)
- 0x20000326 — RAM (r2)
- 0x2000032d — RAM (r1)
- 0x20000337 — RAM (r3)
- 0x20000338 — RAM (r1)
- 0x20000448 — RAM (r1)
- 0x20000828 — RAM (r2)
- 0x20000844 — RAM (r1)
- 0x20001794 — RAM (r1)
- 0x40012c40 — периферия (r3)
- 0x8fb28b71 — прочее (r3)
- 0xfffff9db — прочее (r1)
- 0xfffff9f3 — прочее (r3)

## Вызовы (callees)

- 0x19968 (bl, вне списка функций)
- `func_0x19a68` (0x00019a68, bl)
- `func_0x1a628` (0x0001a628, bl)
- 0x1c8f6 (b, вне списка функций)
- 0x1c97e (b, вне списка функций)
- 0x1c994 (b, вне списка функций)
- 0x1ca72 (b, вне списка функций)
- 0x1cbb0 (b, вне списка функций)
- 0x1cbc2 (b, вне списка функций)
- 0x1cbd0 (b, вне списка функций)
- 0x1cbea (b, вне списка функций)
- 0x1cbec (b, вне списка функций)
- 0x1cbf0 (b, вне списка функций)
- 0x1ccf4 (b, вне списка функций)
- 0x1cd2a (b, вне списка функций)
- 0x1cd48 (b, вне списка функций)
- 0x1cd6a (b, вне списка функций)
- 0x1cd7a (b, вне списка функций)
- 0x1cd8a (b, вне списка функций)
- 0x1cd96 (b, вне списка функций)
- 0x1cde8 (b, вне списка функций)
- 0x1cdf2 (b, вне списка функций)
- 0x1cdf6 (b, вне списка функций)
- `func_0x1dea4` (0x0001dea4, bl)
- 0x21b52 (bl, вне списка функций)
- `func_0x221a4` (0x000221a4, bl)
- `func_0x221e6` (0x000221e6, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1c894..0x1c8da` (70 Б); цели из: 0x1c88e
- `0x1c8da..0x1c918` (62 Б); цели из: 0x1c89e
- `0x1c918..0x1c962` (74 Б); цели из: 0x1c8ec
- `0x1c962..0x1c97a` (24 Б); цели из: 0x1c90c
- `0x1c97a..0x1c97e` (4 Б); цели из: 0x1c910, 0x1c914
- `0x1c97e..0x1c986` (8 Б); цели из: 0x1c916
- `0x1c986..0x1c994` (14 Б); цели из: 0x1c980
- `0x1c994..0x1c99a` (6 Б); цели из: 0x1c978
- `0x1c99a..0x1c9de` (68 Б); цели из: 0x1c992
- `0x1c9de..0x1ca04` (38 Б); цели из: 0x1c9d8
- `0x1ca04..0x1ca52` (78 Б); цели из: 0x1c9e8
- `0x1ca52..0x1ca72` (32 Б); цели из: 0x1ca30
- `0x1ca72..0x1caaa` (56 Б); цели из: 0x1ca62
- `0x1caaa..0x1cbae` (260 Б); цели из: 0x1ca78
- `0x1cbae..0x1cbb0` (2 Б); цели из: 0x1cba6
- `0x1cbb0..0x1cbc0` (16 Б); цели из: 0x1cbac
- `0x1cbc0..0x1cbc2` (2 Б); цели из: 0x1cbb8
- `0x1cbc2..0x1cbce` (12 Б); цели из: 0x1cbbe
- `0x1cbce..0x1cbd0` (2 Б); цели из: 0x1cbc6
- `0x1cbd0..0x1cbe6` (22 Б); цели из: 0x1cbcc
- `0x1cbe6..0x1cbe8` (2 Б); цели из: 0x1cbd8
- `0x1cbe8..0x1cbf0` (8 Б); цели из: 0x1cbe2
- `0x1cbf0..0x1ccf4` (260 Б); цели из: 0x1ca70
- `0x1ccf4..0x1ccfc` (8 Б); цели из: 0x1ca6e
- `0x1ccfc..0x1cd2a` (46 Б); цели из: 0x1ccf8
- `0x1cd2a..0x1cd48` (30 Б); цели из: 0x1ca6c
- `0x1cd48..0x1cd68` (32 Б); цели из: 0x1ca6a
- `0x1cd68..0x1cd6a` (2 Б); цели из: 0x1cd62
- `0x1cd6a..0x1cd78` (14 Б); цели из: 0x1cd66
- `0x1cd78..0x1cd7a` (2 Б); цели из: 0x1cd72
- `0x1cd7a..0x1cd88` (14 Б); цели из: 0x1cd76
- `0x1cd88..0x1cd8a` (2 Б); цели из: 0x1cd80
- `0x1cd8a..0x1cd96` (12 Б); цели из: 0x1cd86
- `0x1cd96..0x1cda0` (10 Б); цели из: 0x1cbe8, 0x1cd8e
- `0x1cda0..0x1cde8` (72 Б); цели из: 0x1cd94
- `0x1cde8..0x1cdf2` (10 Б); цели из: 0x1cbe4

## Дизассембляция

```asm
  1c838:  push {r4, r5, r6, r7, lr}         
  1c83a:  movs r4, #0                       
  1c83c:  sub sp, #0x4c                     
  1c83e:  mov r6, r4                        
  1c840:  mov r7, r4                        
  1c842:  movs r2, #0x14                    
  1c844:  adr r1, #0x3c0                    
  1c846:  add r0, sp, #0x34                 
  1c848:  bl #0x19a68                       -> func_0x19a68
  1c84c:  movs r2, #0x14                    
  1c84e:  adr r1, #0x3cc                    
  1c850:  add r0, sp, #0x14                 
  1c852:  bl #0x19a68                       -> func_0x19a68
  1c856:  adr r1, #0x3d8                    
  1c858:  ldm r1, {r0, r1}                  
  1c85a:  str r0, [sp, #4]                  
  1c85c:  ldr r5, [pc, #0x3d8]              -> RAM
  1c85e:  str r1, [sp, #8]                  
  1c860:  ldr r0, [pc, #0x3d8]              -> RAM
  1c862:  ldrb r1, [r5]                     
  1c864:  ldrb r0, [r0]                     
  1c866:  str r0, [sp, #0x2c]               
  1c868:  ldr r0, [pc, #0x3d4]              -> RAM
  1c86a:  movs r3, r1                       
  1c86c:  ldr r2, [r0]                      
  1c86e:  ldr r0, [r0, #4]                  
  1c870:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1c874:  lsls r7, r0, #0x14                
  1c876:  ldc2l p11, c15, [lr, #0x3f0]!     
  1c87a:  .byte 0xfa, 0xf9                  
  1c87c:  lsls r0, r7, #3                   
  1c87e:  ldr r3, [pc, #0x3c4]              -> flash-mirror @0x1f800
  1c880:  ldr r0, [pc, #0x3c0]              -> flash-mirror @0x1f800
  1c882:  lsls r1, r6, #2                   
  1c884:  adds r0, r1, r0                   
  1c886:  ldrb r0, [r0]                     
  1c888:  ldr r1, [pc, #0x3bc]              -> RAM
  1c88a:  cmp r0, #0xff                     
  1c88c:  strb r0, [r1, r6]                 
  1c88e:  bne #0x1c894                      
  1c890:  adds r7, r7, #1                   
  1c892:  uxtb r7, r7                       
  1c894:  adds r6, r6, #1                   
  1c896:  uxtb r6, r6                       
  1c898:  cmp r6, #7                        
  1c89a:  blo #0x1c880                      
  1c89c:  cmp r7, #7                        
  1c89e:  blo #0x1c8da                      
  1c8a0:  ldr r0, [pc, #0x3a4]              -> RAM
  1c8a2:  movs r1, #1                       
  1c8a4:  strb r1, [r0]                     
  1c8a6:  movs r2, #0                       
  1c8a8:  strb r2, [r0, #1]                 
  1c8aa:  strb r1, [r0, #2]                 
  1c8ac:  movs r1, #0x30                    
  1c8ae:  strb r1, [r0, #3]                 
  1c8b0:  movs r1, #0x17                    
  1c8b2:  strb r1, [r0, #4]                 
  1c8b4:  movs r1, #5                       
  1c8b6:  strb r1, [r0, #5]                 
  1c8b8:  movs r1, #0x19                    
  1c8ba:  strb r1, [r0, #6]                 
  1c8bc:  mov r7, r3                        
  1c8be:  mov r0, r3                        
  1c8c0:  bl #0x221a4                       -> func_0x221a4
  1c8c4:  movs r6, #0                       
  1c8c6:  ldr r0, [pc, #0x380]              -> RAM
  1c8c8:  ldrb r1, [r0, r6]                 
  1c8ca:  lsls r0, r6, #2                   
  1c8cc:  adds r0, r0, r7                   
  1c8ce:  bl #0x221e6                       -> func_0x221e6
  1c8d2:  adds r6, r6, #1                   
  1c8d4:  uxtb r6, r6                       
  1c8d6:  cmp r6, #7                        
  1c8d8:  blo #0x1c8c6                      
  1c8da:  ldr r6, [pc, #0x36c]              -> RAM
  1c8dc:  movs r0, #0                       
  1c8de:  ldr r1, [pc, #0x364]              -> flash-mirror @0x1f800
  1c8e0:  lsls r2, r0, #2                   
  1c8e2:  adds r2, r2, r1                   
  1c8e4:  ldrb r2, [r2, #0x1c]              
  1c8e6:  adds r3, r6, r0                   
  1c8e8:  strb r2, [r3, #7]                 
  1c8ea:  cmp r2, #0xff                     
  1c8ec:  beq #0x1c918                      
  1c8ee:  adds r0, r0, #1                   
  1c8f0:  uxtb r0, r0                       
  1c8f2:  cmp r0, #0x12                     
  1c8f4:  blo #0x1c8de                      
  1c8f6:  movs r0, #0                       
  1c8f8:  ldr r3, [pc, #0x350]              -> RAM
  1c8fa:  mov r1, r0                        
  1c8fc:  ldr r2, [pc, #0x344]              -> flash-mirror @0x1f800
  1c8fe:  lsls r7, r1, #2                   
  1c900:  adds r2, r7, r2                   
  1c902:  ldr r2, [r2, #0x64]               
  1c904:  adds r7, r6, r1                   
  1c906:  uxtb r2, r2                       
  1c908:  strb r2, [r7, #0x19]              
  1c90a:  cmp r2, #0xff                     
  1c90c:  beq #0x1c962                      
  1c90e:  cmp r2, #0x30                     
  1c910:  beq #0x1c97a                      
  1c912:  cmp r2, #0x2f                     
  1c914:  beq #0x1c97a                      
  1c916:  b #0x1c97e                        -> 0x1c97e (вне списка функций)
  1c918:  movs r0, #0                       
  1c91a:  add r7, sp, #0x34                 
  1c91c:  ldrb r2, [r7, r0]                 
  1c91e:  adds r3, r6, r0                   
  1c920:  adds r0, r0, #1                   
  1c922:  uxtb r0, r0                       
  1c924:  strb r2, [r3, #7]                 
  1c926:  cmp r0, #0x12                     
  1c928:  blo #0x1c91c                      
  1c92a:  ldr r0, [pc, #0x318]              -> flash-mirror @0x1f800
  1c92c:  bl #0x221a4                       -> func_0x221a4
  1c930:  movs r7, #0                       
  1c932:  ldr r0, [pc, #0x310]              -> flash-mirror @0x1f800
  1c934:  lsls r2, r7, #2                   
  1c936:  ldrb r1, [r6, r7]                 
  1c938:  adds r0, r2, r0                   
  1c93a:  bl #0x221e6                       -> func_0x221e6
  1c93e:  adds r7, r7, #1                   
  1c940:  uxtb r7, r7                       
  1c942:  cmp r7, #7                        
  1c944:  blo #0x1c932                      
  1c946:  movs r7, #0                       
  1c948:  adds r0, r6, r7                   
  1c94a:  ldrb r1, [r0, #7]                 
  1c94c:  ldr r0, [pc, #0x2f4]              -> flash-mirror @0x1f800
  1c94e:  lsls r2, r7, #2                   
  1c950:  adds r0, #0x1c                    
  1c952:  adds r0, r2, r0                   
  1c954:  bl #0x221e6                       -> func_0x221e6
  1c958:  adds r7, r7, #1                   
  1c95a:  uxtb r7, r7                       
  1c95c:  cmp r7, #0x12                     
  1c95e:  blo #0x1c948                      
  1c960:  b #0x1c8f6                        -> 0x1c8f6 (вне списка функций)
  1c962:  movs r0, #0                       
  1c964:  add r7, sp, #0x14                 
  1c966:  ldrb r1, [r7, r0]                 
  1c968:  adds r2, r6, r0                   
  1c96a:  adds r0, r0, #1                   
  1c96c:  uxtb r0, r0                       
  1c96e:  strb r1, [r2, #0x19]              
  1c970:  cmp r0, #0x14                     
  1c972:  blo #0x1c966                      
  1c974:  movs r0, #1                       
  1c976:  strb r0, [r3]                     
  1c978:  b #0x1c994                        -> 0x1c994 (вне списка функций)
  1c97a:  adds r0, r0, #1                   
  1c97c:  uxtb r0, r0                       
  1c97e:  cmp r0, #0x14                     
  1c980:  bne #0x1c986                      
  1c982:  movs r2, #1                       
  1c984:  strb r2, [r3]                     
  1c986:  adds r1, r1, #1                   
  1c988:  uxtb r1, r1                       
  1c98a:  cmp r1, #0x14                     
  1c98c:  blo #0x1c8fc                      
  1c98e:  ldrb r0, [r3]                     
  1c990:  cmp r0, #1                        
  1c992:  bne #0x1c99a                      
  1c994:  ldr r1, [pc, #0x2b8]              -> RAM
  1c996:  movs r0, #1                       
  1c998:  strb r0, [r1]                     
  1c99a:  ldr r7, [pc, #0x2a8]              -> flash-mirror @0x1f800
  1c99c:  ldr r1, [pc, #0x2b4]              -> RAM
  1c99e:  adds r7, #0x80                    
  1c9a0:  ldrh r0, [r7, #0x34]              
  1c9a2:  strb r0, [r1]                     
  1c9a4:  ldr r1, [pc, #0x2b0]              -> RAM
  1c9a6:  strb r0, [r1]                     
  1c9a8:  movs r0, #0                       
  1c9aa:  add r1, sp, #4                    
  1c9ac:  adds r2, r6, r0                   
  1c9ae:  ldrb r2, [r2, #0x19]              
  1c9b0:  strb r2, [r1, r0]                 
  1c9b2:  adds r0, r0, #1                   
  1c9b4:  uxtb r0, r0                       
  1c9b6:  cmp r0, #5                        
  1c9b8:  blo #0x1c9ac                      
  1c9ba:  ldr r2, [pc, #0x2a0]              -> RAM
  1c9bc:  ldr r1, [pc, #0x2a0]              -> RAM
  1c9be:  add r0, sp, #4                    
  1c9c0:  bl #0x1dea4                       -> func_0x1dea4
  1c9c4:  movs r1, #0                       
  1c9c6:  mov r0, r1                        
  1c9c8:  lsls r2, r0, #2                   
  1c9ca:  adds r2, r2, r7                   
  1c9cc:  ldrh r2, [r2, #0x38]              
  1c9ce:  adds r3, r6, r0                   
  1c9d0:  uxtb r2, r2                       
  1c9d2:  adds r3, #0x20                    
  1c9d4:  strb r2, [r3, #0xd]               
  1c9d6:  cmp r2, #0xff                     
  1c9d8:  bne #0x1c9de                      
  1c9da:  adds r1, r1, #1                   
  1c9dc:  uxtb r1, r1                       
  1c9de:  adds r0, r0, #1                   
  1c9e0:  uxtb r0, r0                       
  1c9e2:  cmp r0, #0x10                     
  1c9e4:  blo #0x1c9c8                      
  1c9e6:  cmp r1, #0x10                     
  1c9e8:  blo #0x1ca04                      
  1c9ea:  ldr r2, [pc, #0x278]              -> RAM
  1c9ec:  movs r0, #0                       
  1c9ee:  adds r1, r6, r0                   
  1c9f0:  ldrb r3, [r2, r0]                 
  1c9f2:  adds r1, #0x20                    
  1c9f4:  adds r0, r0, #1                   
  1c9f6:  uxtb r0, r0                       
  1c9f8:  strb r3, [r1, #0xd]               
  1c9fa:  cmp r0, #0x10                     
  1c9fc:  blo #0x1c9ee                      
  1c9fe:  ldr r1, [pc, #0x268]              -> RAM
  1ca00:  movs r0, #1                       
  1ca02:  strb r0, [r1]                     
  1ca04:  ldr r0, [pc, #0x240]              -> RAM
  1ca06:  adds r0, #0x2d                    
  1ca08:  bl #0x1a628                       -> func_0x1a628
  1ca0c:  ldr r6, [pc, #0x25c]              -> flash-mirror @0x1f400
  1ca0e:  ldr r7, [pc, #0x260]              -> RAM
  1ca10:  ldrb r1, [r6, #1]                 
  1ca12:  ldrb r0, [r6]                     
  1ca14:  lsls r1, r1, #8                   
  1ca16:  adds r0, r1, r0                   
  1ca18:  uxth r0, r0                       
  1ca1a:  strh r0, [r7]                     
  1ca1c:  ldrb r3, [r6, #5]                 
  1ca1e:  ldrb r2, [r6, #4]                 
  1ca20:  ldr r1, [pc, #0x250]              -> RAM
  1ca22:  lsls r3, r3, #8                   
  1ca24:  adds r2, r3, r2                   
  1ca26:  strh r2, [r1]                     
  1ca28:  movs r1, #0xff                    
  1ca2a:  adds r1, #0x92                    
  1ca2c:  subs r0, #0xd9                    
  1ca2e:  cmp r0, r1                        
  1ca30:  blo #0x1ca52                      
  1ca32:  movs r0, #0xff                    
  1ca34:  adds r0, #0xa2                    
  1ca36:  strh r0, [r7]                     
  1ca38:  cpsid i                           
  1ca3a:  mov r0, r6                        
  1ca3c:  bl #0x221a4                       -> func_0x221a4
  1ca40:  cmp r0, #0                        
  1ca42:  bne #0x1ca3a                      
  1ca44:  ldrh r1, [r7]                     
  1ca46:  mov r0, r6                        
  1ca48:  bl #0x221e6                       -> func_0x221e6
  1ca4c:  cmp r0, #0                        
  1ca4e:  bne #0x1ca44                      
  1ca50:  cpsie i                           
  1ca52:  ldr r0, [pc, #0x21c]              -> RAM
  1ca54:  ldr r1, [pc, #0x220]              -> RAM
  1ca56:  ldrh r0, [r0]                     
  1ca58:  strh r0, [r1]                     
  1ca5a:  ldr r7, [pc, #0x218]              -> RAM
  1ca5c:  ldr r1, [pc, #0x21c]              
  1ca5e:  ldrh r0, [r7]                     
  1ca60:  adds r1, r0, r1                   
  1ca62:  b #0x1ca72                        -> 0x1ca72 (вне списка функций)
  1ca64:  b #0x1cbec                        -> 0x1cbec (вне списка функций)
  1ca66:  b #0x1cdf6                        -> 0x1cdf6 (вне списка функций)
  1ca68:  b #0x1cdf2                        -> 0x1cdf2 (вне списка функций)
  1ca6a:  b #0x1cd48                        -> 0x1cd48 (вне списка функций)
  1ca6c:  b #0x1cd2a                        -> 0x1cd2a (вне списка функций)
  1ca6e:  b #0x1ccf4                        -> 0x1ccf4 (вне списка функций)
  1ca70:  b #0x1cbf0                        -> 0x1cbf0 (вне списка функций)
  1ca72:  movs r0, #0xff                    
  1ca74:  adds r0, #0x92                    
  1ca76:  cmp r1, r0                        
  1ca78:  blo #0x1caaa                      
  1ca7a:  ldr r0, [pc, #0x204]              -> данные @0x006ed
  1ca7c:  strh r0, [r7]                     
  1ca7e:  cpsid i                           
  1ca80:  mov r0, r6                        
  1ca82:  bl #0x221a4                       -> func_0x221a4
  1ca86:  cmp r0, #0                        
  1ca88:  bne #0x1ca80                      
  1ca8a:  ldr r6, [pc, #0x1e4]              -> RAM
  1ca8c:  ldr r0, [pc, #0x1dc]              -> flash-mirror @0x1f400
  1ca8e:  ldrh r1, [r6]                     
  1ca90:  bl #0x221e6                       -> func_0x221e6
  1ca94:  cmp r0, #0                        
  1ca96:  bne #0x1ca8c                      
  1ca98:  ldr r6, [pc, #0x1d0]              -> flash-mirror @0x1f400
  1ca9a:  adds r6, r6, #4                   
  1ca9c:  ldrh r1, [r7]                     
  1ca9e:  mov r0, r6                        
  1caa0:  bl #0x221e6                       -> func_0x221e6
  1caa4:  cmp r0, #0                        
  1caa6:  bne #0x1ca9c                      
  1caa8:  cpsie i                           
  1caaa:  ldrh r0, [r7]                     
  1caac:  ldr r1, [pc, #0x1d4]              -> RAM
  1caae:  str r0, [sp, #0x28]               
  1cab0:  strh r0, [r1]                     
  1cab2:  ldr r0, [pc, #0x1bc]              -> RAM
  1cab4:  movs r1, #0xa                     
  1cab6:  ldrh r7, [r0]                     
  1cab8:  movs r0, #0x12                    
  1caba:  muls r0, r7, r0                   
  1cabc:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1cac0:  ldr r1, [pc, #0x1c4]              -> RAM
  1cac2:  strh r0, [r1]                     
  1cac4:  movs r0, #0x13                    
  1cac6:  muls r0, r7, r0                   
  1cac8:  movs r1, #0xa                     
  1caca:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1cace:  ldr r1, [pc, #0x1bc]              -> RAM
  1cad0:  strh r0, [r1]                     
  1cad2:  ldr r0, [pc, #0x1bc]              -> RAM
  1cad4:  movs r1, #0xa                     
  1cad6:  strh r7, [r0]                     
  1cad8:  lsls r0, r7, #3                   
  1cada:  subs r0, r0, r7                   
  1cadc:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1cae0:  ldr r1, [pc, #0x1b0]              -> RAM
  1cae2:  rsbs r0, r0, #0                   
  1cae4:  strh r0, [r1]                     
  1cae6:  movs r1, #0xa                     
  1cae8:  mov r0, r7                        
  1caea:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1caee:  sxth r6, r0                       
  1caf0:  ldr r0, [pc, #0x1a4]              -> RAM
  1caf2:  ldr r1, [pc, #0x1a8]              -> RAM
  1caf4:  strh r6, [r0]                     
  1caf6:  movs r0, #0x1e                    
  1caf8:  muls r0, r6, r0                   
  1cafa:  strh r0, [r1]                     
  1cafc:  movs r0, #0x19                    
  1cafe:  ldr r1, [pc, #0x1a0]              -> RAM
  1cb00:  muls r0, r6, r0                   
  1cb02:  strh r0, [r1]                     
  1cb04:  lsls r0, r6, #4                   
  1cb06:  ldr r1, [pc, #0x19c]              -> RAM
  1cb08:  subs r0, r0, r6                   
  1cb0a:  strh r0, [r1]                     
  1cb0c:  movs r0, #0xc                     
  1cb0e:  ldr r1, [pc, #0x198]              -> RAM
  1cb10:  muls r0, r6, r0                   
  1cb12:  strh r0, [r1]                     
  1cb14:  str r0, [sp]                      
  1cb16:  ldr r0, [pc, #0x194]              -> RAM
  1cb18:  ldr r1, [pc, #0x194]              -> RAM
  1cb1a:  strh r7, [r0]                     
  1cb1c:  lsls r0, r6, #3                   
  1cb1e:  strh r0, [r1]                     
  1cb20:  lsls r0, r6, #3                   
  1cb22:  ldr r1, [pc, #0x190]              -> RAM
  1cb24:  subs r0, r0, r6                   
  1cb26:  strh r0, [r1]                     
  1cb28:  lsls r0, r6, #2                   
  1cb2a:  ldr r1, [pc, #0x18c]              -> RAM
  1cb2c:  adds r0, r6, r0                   
  1cb2e:  strh r0, [r1]                     
  1cb30:  ldr r1, [pc, #0x188]              -> RAM
  1cb32:  lsls r0, r6, #1                   
  1cb34:  strh r0, [r1]                     
  1cb36:  movs r1, #0xc8                    
  1cb38:  mov r0, r7                        
  1cb3a:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1cb3e:  ldr r1, [pc, #0x180]              -> RAM
  1cb40:  strh r0, [r1]                     
  1cb42:  asrs r0, r6, #2                   
  1cb44:  ldr r1, [pc, #0x17c]              -> RAM
  1cb46:  asrs r6, r6, #1                   
  1cb48:  strh r0, [r1]                     
  1cb4a:  ldr r0, [pc, #0x17c]              -> RAM
  1cb4c:  movs r1, #0x64                    
  1cb4e:  strh r6, [r0]                     
  1cb50:  lsls r0, r7, #3                   
  1cb52:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1cb56:  ldr r1, [pc, #0x174]              -> RAM
  1cb58:  strh r0, [r1]                     
  1cb5a:  ldr r0, [sp]                      
  1cb5c:  ldr r1, [pc, #0x170]              -> RAM
  1cb5e:  adds r0, r0, r6                   
  1cb60:  strh r0, [r1]                     
  1cb62:  ldr r0, [sp, #0x28]               
  1cb64:  movs r1, #0x36                    
  1cb66:  muls r0, r1, r0                   
  1cb68:  movs r1, #0x29                    
  1cb6a:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1cb6e:  ldr r1, [pc, #0x164]              -> RAM
  1cb70:  strh r0, [r1]                     
  1cb72:  ldr r0, [pc, #0x164]              -> func_0x1f600
  1cb74:  ldrb r2, [r0, #1]                 
  1cb76:  ldrb r1, [r0]                     
  1cb78:  lsls r2, r2, #8                   
  1cb7a:  adds r1, r2, r1                   
  1cb7c:  ldrb r3, [r0, #5]                 
  1cb7e:  ldrb r2, [r0, #4]                 
  1cb80:  lsls r3, r3, #8                   
  1cb82:  adds r2, r3, r2                   
  1cb84:  uxth r6, r2                       
  1cb86:  ldrb r3, [r0, #9]                 
  1cb88:  ldrb r2, [r0, #8]                 
  1cb8a:  lsls r3, r3, #8                   
  1cb8c:  adds r2, r3, r2                   
  1cb8e:  ldrb r3, [r0, #0xc]               
  1cb90:  ldrb r0, [r0, #0xd]               
  1cb92:  uxth r1, r1                       
  1cb94:  lsls r0, r0, #8                   
  1cb96:  adds r0, r0, r3                   
  1cb98:  uxth r3, r0                       
  1cb9a:  ldr r0, [pc, #0xe0]               
  1cb9c:  uxth r2, r2                       
  1cb9e:  adds r0, #0x18                    
  1cba0:  adds r7, r1, r0                   
  1cba2:  ldr r0, [pc, #0x138]              -> данные @0x003e7
  1cba4:  cmp r7, r0                        
  1cba6:  bhs #0x1cbae                      
  1cba8:  ldr r7, [pc, #0x134]              -> RAM
  1cbaa:  strh r1, [r7, #0x18]              
  1cbac:  b #0x1cbb0                        -> 0x1cbb0 (вне списка функций)
  1cbae:  movs r4, #1                       
  1cbb0:  ldr r1, [pc, #0xc8]               
  1cbb2:  adds r1, #0x18                    
  1cbb4:  adds r7, r6, r1                   
  1cbb6:  cmp r7, r0                        
  1cbb8:  bhs #0x1cbc0                      
  1cbba:  ldr r7, [pc, #0x124]              -> RAM
  1cbbc:  strh r6, [r7, #0x1a]              
  1cbbe:  b #0x1cbc2                        -> 0x1cbc2 (вне списка функций)
  1cbc0:  movs r4, #1                       
  1cbc2:  adds r6, r2, r1                   
  1cbc4:  cmp r6, r0                        
  1cbc6:  bhs #0x1cbce                      
  1cbc8:  ldr r6, [pc, #0x114]              -> RAM
  1cbca:  strh r2, [r6, #0x1c]              
  1cbcc:  b #0x1cbd0                        -> 0x1cbd0 (вне списка функций)
  1cbce:  movs r4, #1                       
  1cbd0:  adds r6, r3, r1                   
  1cbd2:  ldr r2, [pc, #0x110]              -> данные @0x07ff8
  1cbd4:  ldr r1, [pc, #0x110]              -> RAM
  1cbd6:  cmp r6, r0                        
  1cbd8:  bhs #0x1cbe6                      
  1cbda:  ldr r0, [pc, #0x104]              -> RAM
  1cbdc:  cmp r4, #0                        
  1cbde:  strh r3, [r0, #0x3c]              
  1cbe0:  strh r2, [r1, #0xa]               
  1cbe2:  bne #0x1cbe8                      
  1cbe4:  b #0x1cde8                        -> 0x1cde8 (вне списка функций)
  1cbe6:  strh r2, [r1, #0xa]               
  1cbe8:  b #0x1cd96                        -> 0x1cd96 (вне списка функций)
  1cbea:  strb r0, [r5]                     
  1cbec:  add sp, #0x4c                     
  1cbee:  pop {r4, r5, r6, r7, pc}          
  1cbf0:  ldr r1, [pc, #0xf8]               -> RAM
  1cbf2:  movs r0, #0                       
  1cbf4:  ldrsh r0, [r1, r0]                
  1cbf6:  ldr r1, [pc, #0xf8]               -> данные @0x0094e
  1cbf8:  cmp r0, r1                        
  1cbfa:  ble #0x1cbec                      
  1cbfc:  ldr r1, [pc, #0x3c]               -> RAM
  1cbfe:  movs r0, #1                       
  1cc00:  strb r0, [r1]                     
  1cc02:  movs r0, #2                       
  1cc04:  b #0x1cbea                        -> 0x1cbea (вне списка функций)
  1cc06:  movs r0, r0                       
  1cc08:  ldr r3, [pc, #0x150]              
  1cc0a:  adds r0, #0x30                    
  1cc0c:  adds r2, #0x33                    
  1cc0e:  ldr r0, [pc, #0xcc]               -> данные @0x003e7
  1cc10:  adds r0, #0x30                    
  1cc12:  adds r0, #0x30                    
  1cc14:  adds r0, #0x30                    
  1cc16:  strh r1, [r6, r4]                 
  1cc18:  adds r3, #0x37                    
  1cc1a:  movs r0, r0                       
  1cc1c:  adds r0, #0x30                    
  1cc1e:  adds r0, #0x30                    
  1cc20:  cmp r7, #0x30                     
  1cc22:  adds r0, #0x30                    
  1cc24:  adds r0, #0x30                    
  1cc26:  adds r0, #0x30                    
  1cc28:  adds r0, #0x30                    
  1cc2a:  adds r0, #0x30                    
  1cc2c:  adds r0, #0x30                    
  1cc2e:  adds r0, #0x30                    
  1cc30:  adds r0, #0x30                    
  1cc32:  adds r0, #0x30                    
  1cc34:  movs r0, r6                       
  1cc36:  movs r0, r0                       
  1cc38:  lsls r6, r1, #9                   
  1cc3a:  movs r0, #0                       
  1cc3c:  lsls r0, r1, #9                   
  1cc3e:  movs r0, #0                       
  1cc40:  lsls r0, r4, #7                   
  1cc42:  movs r0, #0                       
  1cc44:  .byte 0x00, 0xf8                  
  1cc46:  lsrs r1, r0, #0x20                
  1cc48:  lsrs r4, r0, #1                   
  1cc4a:  movs r0, #0                       
  1cc4c:  lsls r7, r6, #0xc                 
  1cc4e:  movs r0, #0                       
  1cc50:  lsls r5, r5, #0xc                 
  1cc52:  movs r0, #0                       
  1cc54:  lsls r1, r0, #9                   
  1cc56:  movs r0, #0                       
  1cc58:  lsls r2, r0, #9                   
  1cc5a:  movs r0, #0                       
  1cc5c:  lsls r6, r4, #0xc                 
  1cc5e:  movs r0, #0                       
  1cc60:  lsls r4, r4, #0xc                 
  1cc62:  movs r0, #0                       
  1cc64:  lsrs r0, r5, #0x20                
  1cc66:  movs r0, #0                       
  1cc68:  lsls r0, r7, #0xc                 
  1cc6a:  movs r0, #0                       
  1cc6c:  and r8, r0, #0x810000             
  1cc70:  lsls r0, r5, #7                   
  1cc72:  movs r0, #0                       
  1cc74:  lsls r4, r5, #7                   
  1cc76:  movs r0, #0                       
  1cc78:  lsls r2, r5, #7                   
  1cc7a:  movs r0, #0                       
  1cc7c:  .byte 0xdb, 0xf9                  
  1cc7e:  .byte 0xff, 0xff                  
  1cc80:  lsls r5, r5, #0x1b                
  1cc82:  movs r0, r0                       
  1cc84:  lsls r6, r5, #7                   
  1cc86:  movs r0, #0                       
  1cc88:  lsls r6, r6, #7                   
  1cc8a:  movs r0, #0                       
  1cc8c:  lsls r6, r7, #7                   
  1cc8e:  movs r0, #0                       
  1cc90:  lsls r2, r6, #7                   
  1cc92:  movs r0, #0                       
  1cc94:  lsls r4, r6, #7                   
  1cc96:  movs r0, #0                       
  1cc98:  lsls r0, r7, #7                   
  1cc9a:  movs r0, #0                       
  1cc9c:  lsls r2, r7, #7                   
  1cc9e:  movs r0, #0                       
  1cca0:  lsls r4, r7, #7                   
  1cca2:  movs r0, #0                       
  1cca4:  lsls r0, r0, #8                   
  1cca6:  movs r0, #0                       
  1cca8:  lsls r4, r0, #8                   
  1ccaa:  movs r0, #0                       
  1ccac:  lsls r6, r0, #8                   
  1ccae:  movs r0, #0                       
  1ccb0:  lsls r0, r1, #8                   
  1ccb2:  movs r0, #0                       
  1ccb4:  lsls r2, r1, #8                   
  1ccb6:  movs r0, #0                       
  1ccb8:  lsls r4, r1, #8                   
  1ccba:  movs r0, #0                       
  1ccbc:  lsls r6, r1, #8                   
  1ccbe:  movs r0, #0                       
  1ccc0:  lsls r0, r2, #8                   
  1ccc2:  movs r0, #0                       
  1ccc4:  lsls r2, r2, #8                   
  1ccc6:  movs r0, #0                       
  1ccc8:  lsls r4, r2, #8                   
  1ccca:  movs r0, #0                       
  1cccc:  lsls r6, r2, #8                   
  1ccce:  movs r0, #0                       
  1ccd0:  lsls r2, r0, #8                   
  1ccd2:  movs r0, #0                       
  1ccd4:  lsls r6, r4, #9                   
  1ccd6:  movs r0, #0                       
  1ccd8:  addw r8, r0, #0x801               
  1ccdc:  lsls r7, r4, #0xf                 
  1ccde:  movs r0, r0                       
  1cce0:  lsls r0, r2, #4                   
  1cce2:  movs r0, #0                       
  1cce4:  ldrb r0, [r7, #0x1f]              
  1cce6:  movs r0, r0                       
  1cce8:  asrs r4, r2, #0x1e                
  1ccea:  movs r0, #0                       
  1ccec:  lsls r4, r1, #9                   
  1ccee:  movs r0, #0                       
  1ccf0:  lsrs r6, r1, #5                   
  1ccf2:  movs r0, r0                       
  1ccf4:  ldr r1, [sp, #0x2c]               
  1ccf6:  cmp r1, #2                        
  1ccf8:  beq #0x1ccfc                      
  1ccfa:  b #0x1cbec                        -> 0x1cbec (вне списка функций)
  1ccfc:  ldr r3, [pc, #0x100]              -> RAM
  1ccfe:  movs r1, #0                       
  1cd00:  str r1, [r3]                      
  1cd02:  ldr r3, [pc, #0x100]              -> RAM
  1cd04:  str r1, [r3]                      
  1cd06:  ldr r3, [pc, #0x100]              -> RAM
  1cd08:  str r1, [r3]                      
  1cd0a:  ldr r3, [pc, #0x100]              -> периферия
  1cd0c:  str r1, [r3, #4]                  
  1cd0e:  str r1, [r3, #8]                  
  1cd10:  str r1, [r3, #0xc]                
  1cd12:  ldr r1, [pc, #0xfc]               -> данные @0x008c9
  1cd14:  str r1, [r3, #0x10]               
  1cd16:  ldr r1, [r3, #0x14]               
  1cd18:  movs r4, #1                       
  1cd1a:  lsls r4, r4, #0xf                 
  1cd1c:  orrs r1, r4                       
  1cd1e:  str r1, [r3, #0x14]               
  1cd20:  ldr r1, [pc, #0xf0]               -> RAM
  1cd22:  str r2, [r1, #0x10]               
  1cd24:  str r0, [r1, #0x14]               
  1cd26:  movs r0, #3                       
  1cd28:  b #0x1cbea                        -> 0x1cbea (вне списка функций)
  1cd2a:  ldr r3, [pc, #0xe8]               -> RAM
  1cd2c:  ldr r1, [r3, #0x10]               
  1cd2e:  ldr r3, [r3, #0x14]               
  1cd30:  subs r1, r2, r1                   
  1cd32:  sbcs r0, r3                       
  1cd34:  movs r2, #0x64                    
  1cd36:  movs r3, #0                       
  1cd38:  subs r1, r2, r1                   
  1cd3a:  sbcs r3, r0                       
  1cd3c:  bhs #0x1ccfa                      
  1cd3e:  ldr r1, [pc, #0xd8]               -> RAM
  1cd40:  movs r0, #3                       
  1cd42:  strb r0, [r1]                     
  1cd44:  movs r0, #4                       
  1cd46:  b #0x1cbea                        -> 0x1cbea (вне списка функций)
  1cd48:  ldr r0, [sp, #0x2c]               
  1cd4a:  cmp r0, #4                        
  1cd4c:  bne #0x1ccfa                      
  1cd4e:  ldr r6, [pc, #0xcc]               -> RAM
  1cd50:  ldr r3, [pc, #0xcc]               
  1cd52:  ldrh r0, [r6, #0x18]              
  1cd54:  ldrh r2, [r6, #0x1c]              
  1cd56:  adds r7, r0, r3                   
  1cd58:  mov ip, r2                        
  1cd5a:  ldr r3, [pc, #0xc8]               -> данные @0x003e7
  1cd5c:  ldrh r1, [r6, #0x1a]              
  1cd5e:  ldrh r2, [r6, #0x3c]              
  1cd60:  cmp r7, r3                        
  1cd62:  bhs #0x1cd68                      
  1cd64:  strh r0, [r6, #0x18]              
  1cd66:  b #0x1cd6a                        -> 0x1cd6a (вне списка функций)
  1cd68:  movs r4, #1                       
  1cd6a:  ldr r3, [pc, #0xb4]               
  1cd6c:  ldr r0, [pc, #0xb4]               -> данные @0x003e7
  1cd6e:  adds r7, r1, r3                   
  1cd70:  cmp r7, r0                        
  1cd72:  bhs #0x1cd78                      
  1cd74:  strh r1, [r6, #0x1a]              
  1cd76:  b #0x1cd7a                        -> 0x1cd7a (вне списка функций)
  1cd78:  movs r4, #1                       
  1cd7a:  mov r1, ip                        
  1cd7c:  adds r1, r1, r3                   
  1cd7e:  cmp r1, r0                        
  1cd80:  bhs #0x1cd88                      
  1cd82:  mov r1, ip                        
  1cd84:  strh r1, [r6, #0x1c]              
  1cd86:  b #0x1cd8a                        -> 0x1cd8a (вне списка функций)
  1cd88:  movs r4, #1                       
  1cd8a:  adds r1, r2, r3                   
  1cd8c:  cmp r1, r0                        
  1cd8e:  bhs #0x1cd96                      
  1cd90:  strh r2, [r6, #0x3c]              
  1cd92:  cmp r4, #0                        
  1cd94:  beq #0x1cda0                      
  1cd96:  ldr r1, [pc, #0x80]               -> RAM
  1cd98:  movs r0, #0                       
  1cd9a:  strb r0, [r1]                     
  1cd9c:  movs r0, #1                       
  1cd9e:  b #0x1cbea                        -> 0x1cbea (вне списка функций)
  1cda0:  ldr r4, [pc, #0x84]               -> func_0x1f600
  1cda2:  mov r0, r4                        
  1cda4:  bl #0x221a4                       -> func_0x221a4
  1cda8:  cmp r0, #0                        
  1cdaa:  bne #0x1cda2                      
  1cdac:  ldrh r1, [r6, #0x18]              
  1cdae:  mov r0, r4                        
  1cdb0:  bl #0x221e6                       -> func_0x221e6
  1cdb4:  cmp r0, #0                        
  1cdb6:  bne #0x1cdac                      
  1cdb8:  ldr r4, [pc, #0x6c]               -> func_0x1f600
  1cdba:  adds r4, r4, #4                   
  1cdbc:  ldrh r1, [r6, #0x1a]              
  1cdbe:  mov r0, r4                        
  1cdc0:  bl #0x221e6                       -> func_0x221e6
  1cdc4:  cmp r0, #0                        
  1cdc6:  bne #0x1cdbc                      
  1cdc8:  ldr r4, [pc, #0x5c]               -> func_0x1f600
  1cdca:  adds r4, #8                       
  1cdcc:  ldrh r1, [r6, #0x1c]              
  1cdce:  mov r0, r4                        
  1cdd0:  bl #0x221e6                       -> func_0x221e6
  1cdd4:  cmp r0, #0                        
  1cdd6:  bne #0x1cdcc                      
  1cdd8:  ldr r4, [pc, #0x4c]               -> func_0x1f600
  1cdda:  adds r4, #0xc                     
  1cddc:  ldrh r1, [r6, #0x3c]              
  1cdde:  mov r0, r4                        
  1cde0:  bl #0x221e6                       -> func_0x221e6
  1cde4:  cmp r0, #0                        
  1cde6:  bne #0x1cddc                      
  1cde8:  ldr r1, [pc, #0x2c]               -> RAM
  1cdea:  movs r0, #5                       
  1cdec:  strb r0, [r1]                     
  1cdee:  movs r0, #6                       
  1cdf0:  b #0x1cbea                        -> 0x1cbea (вне списка функций)
  ; --- literal-пул @0x1cc38 (47 слов) ---
  1cc38:  .word 0x2000024e  ; RAM
  1cc3c:  .word 0x20000248  ; RAM
  1cc40:  .word 0x200001e0  ; RAM
  1cc44:  .word 0x0801f800  ; flash-mirror @0x1f800
  1cc48:  .word 0x20000844  ; RAM
  1cc4c:  .word 0x20000337  ; RAM
  1cc50:  .word 0x2000032d  ; RAM
  1cc54:  .word 0x20000241  ; RAM
  1cc58:  .word 0x20000242  ; RAM
  1cc5c:  .word 0x20000326  ; RAM
  1cc60:  .word 0x20000324  ; RAM
  1cc64:  .word 0x20000828  ; RAM
  1cc68:  .word 0x20000338  ; RAM
  1cc6c:  .word 0x0801f400  ; flash-mirror @0x1f400
  1cc70:  .word 0x200001e8  ; RAM
  1cc74:  .word 0x200001ec  ; RAM
  1cc78:  .word 0x200001ea  ; RAM
  1cc7c:  .word 0xfffff9db
  1cc80:  .word 0x000006ed  ; данные @0x006ed
  1cc84:  .word 0x200001ee  ; RAM
  1cc88:  .word 0x200001f6  ; RAM
  1cc8c:  .word 0x200001fe  ; RAM
  1cc90:  .word 0x200001f2  ; RAM
  1cc94:  .word 0x200001f4  ; RAM
  1cc98:  .word 0x200001f8  ; RAM
  1cc9c:  .word 0x200001fa  ; RAM
  1cca0:  .word 0x200001fc  ; RAM
  1cca4:  .word 0x20000200  ; RAM
  1cca8:  .word 0x20000204  ; RAM
  1ccac:  .word 0x20000206  ; RAM
  1ccb0:  .word 0x20000208  ; RAM
  1ccb4:  .word 0x2000020a  ; RAM
  1ccb8:  .word 0x2000020c  ; RAM
  1ccbc:  .word 0x2000020e  ; RAM
  1ccc0:  .word 0x20000210  ; RAM
  1ccc4:  .word 0x20000212  ; RAM
  1ccc8:  .word 0x20000214  ; RAM
  1cccc:  .word 0x20000216  ; RAM
  1ccd0:  .word 0x20000202  ; RAM
  1ccd4:  .word 0x20000266  ; RAM
  1ccd8:  .word 0x0801f600  ; func_0x1f600
  1ccdc:  .word 0x000003e7  ; данные @0x003e7
  1cce0:  .word 0x20000110  ; RAM
  1cce4:  .word 0x00007ff8  ; данные @0x07ff8
  1cce8:  .word 0x20001794  ; RAM
  1ccec:  .word 0x2000024c  ; RAM
  1ccf0:  .word 0x0000094e  ; данные @0x0094e
  ; --- literal-пул @0x1cd5c (1 слов) ---
  1cd5c:  .word 0x8fb28b71
  ; --- literal-пул @0x1ce00 (11 слов) — ВНЕ границ функции ---
  1ce00:  .word 0x20000254  ; RAM
  1ce04:  .word 0x20000258  ; RAM
  1ce08:  .word 0x2000025c  ; RAM
  1ce0c:  .word 0x40012c40  ; периферия
  1ce10:  .word 0x000008c9  ; данные @0x008c9
  1ce14:  .word 0x20000448  ; RAM
  1ce18:  .word 0x20000248  ; RAM
  1ce1c:  .word 0x20000110  ; RAM
  1ce20:  .word 0xfffff9f3
  1ce24:  .word 0x000003e7  ; данные @0x003e7
  1ce28:  .word 0x0801f600  ; func_0x1f600
```
