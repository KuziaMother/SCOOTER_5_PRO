# func_0x1d898

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001d898) | `0x0001d898` |
| размер кода | 1254 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000013ec — данные @0x013ec (r2)
- 0x00002710 — данные @0x02710 (r2)
- 0x002bf200 — прочее (r1)
- 0x00927c00 — прочее (r3)
- 0x00be6e00 — прочее (r0)
- 0x200001e0 — RAM (r5)
- 0x200001f0 — RAM (r0)
- 0x200001f6 — RAM (r0)
- 0x20000202 — RAM (r1)
- 0x20000204 — RAM (r0)
- 0x20000206 — RAM (r0)
- 0x20000208 — RAM (r1)
- 0x2000020c — RAM (r1)
- 0x2000021c — RAM (r0)
- 0x2000021e — RAM (r7)
- 0x20000229 — RAM (r0)
- 0x2000026e — RAM (r0)
- 0x2000027a — RAM (r1)
- 0x20000286 — RAM (r0)
- 0x2000028c — RAM (r1)
- 0x20000290 — RAM (r0)
- 0x20000292 — RAM (r1)
- 0x20000294 — RAM (r1)
- 0x2000029e — RAM (r0)
- 0x200002a4 — RAM (r1)
- 0x200002a8 — RAM (r1)
- 0x200002aa — RAM (r0)
- 0x200002ac — RAM (r0)
- 0x20000306 — RAM (r0)
- 0x2000030c — RAM (r1)
- 0x2000030e — RAM (r0)
- 0x20000311 — RAM (r0)
- 0x2000031c — RAM (r1)
- 0x20000321 — RAM (r0)
- 0x20000328 — RAM (r0)
- 0x2000032a — RAM (r0)
- 0x20000339 — RAM (r0)
- 0x200003c8 — RAM (r4)
- 0x20000448 — RAM (r7)
- 0x20001768 — RAM (r0)

## Вызовы (callees)

- 0x19994 (bl, вне списка функций)
- `func_0x1a010` (0x0001a010, bl)
- `func_0x1a638` (0x0001a638, bl)
- 0x1d998 (b, вне списка функций)
- 0x1d9ba (b, вне списка функций)
- 0x1d9e4 (b, вне списка функций)
- 0x1d9e6 (b, вне списка функций)
- 0x1da10 (b, вне списка функций)
- 0x1da2a (b, вне списка функций)
- 0x1da2c (b, вне списка функций)
- 0x1dab2 (b, вне списка функций)
- 0x1dae2 (b, вне списка функций)
- 0x1db1e (b, вне списка функций)
- 0x1db28 (b, вне списка функций)
- 0x1db68 (b, вне списка функций)
- 0x1db6e (b, вне списка функций)
- 0x1db74 (b, вне списка функций)
- 0x1db82 (b, вне списка функций)
- 0x1db8c (b, вне списка функций)
- 0x1dbc0 (b, вне списка функций)
- 0x1dbd0 (b, вне списка функций)
- 0x1dbe6 (b, вне списка функций)
- 0x1dc28 (b, вне списка функций)
- 0x1dc34 (b, вне списка функций)
- 0x1dc56 (b, вне списка функций)
- 0x1dc70 (b, вне списка функций)
- 0x1dc72 (b, вне списка функций)
- 0x1dd38 (b, вне списка функций)
- 0x1dd4c (b, вне списка функций)
- `func_0x1de0c` (0x0001de0c, bl)
- `func_0x1df84` (0x0001df84, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1b67c` (bl @0x0001b6d4)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1d98a..0x1d99c` (18 Б); цели из: 0x1d968
- `0x1d99c..0x1d9be` (34 Б); цели из: 0x1d980
- `0x1d9be..0x1d9e4` (38 Б); цели из: 0x1d9ac
- `0x1d9e4..0x1d9e6` (2 Б); цели из: 0x1d99a, 0x1d9c8
- `0x1d9e6..0x1d9f4` (14 Б); цели из: 0x1d996, 0x1d9e2
- `0x1d9f4..0x1da10` (28 Б); цели из: 0x1d9b8
- `0x1da10..0x1da2a` (26 Б); цели из: 0x1d9bc
- `0x1da2a..0x1da58` (46 Б); цели из: 0x1d9f2
- `0x1da58..0x1da5c` (4 Б); цели из: 0x1d9f6
- `0x1da5c..0x1da82` (38 Б); цели из: 0x1da18
- `0x1da82..0x1dab0` (46 Б); цели из: 0x1da60
- `0x1dab0..0x1dab2` (2 Б); цели из: 0x1daa8
- `0x1dab2..0x1dabc` (10 Б); цели из: 0x1daae
- `0x1dabc..0x1dae2` (38 Б); цели из: 0x1da8e
- `0x1dae2..0x1daec` (10 Б); цели из: 0x1daba, 0x1dad8
- `0x1daec..0x1db22` (54 Б); цели из: 0x1da7c
- `0x1db22..0x1db24` (2 Б); цели из: 0x1da38
- `0x1db24..0x1db26` (2 Б); цели из: 0x1da3e
- `0x1db26..0x1db28` (2 Б); цели из: 0x1db1c
- `0x1db28..0x1db52` (42 Б); цели из: 0x1db20
- `0x1db52..0x1db5a` (8 Б); цели из: 0x1db4e
- `0x1db5a..0x1db60` (6 Б); цели из: 0x1daf6
- `0x1db60..0x1db68` (8 Б); цели из: 0x1db36
- `0x1db68..0x1db6e` (6 Б); цели из: 0x1daea
- `0x1db6e..0x1db74` (6 Б); цели из: 0x1db24
- `0x1db74..0x1db80` (12 Б); цели из: 0x1db22
- `0x1db80..0x1db82` (2 Б); цели из: 0x1db72
- `0x1db82..0x1db8c` (10 Б); цели из: 0x1da56
- `0x1db8c..0x1db9a` (14 Б); цели из: 0x1db7e
- `0x1db9a..0x1dbbe` (36 Б); цели из: 0x1db92
- `0x1dbbe..0x1dbc0` (2 Б); цели из: 0x1db9c
- `0x1dbc0..0x1dbf0` (48 Б); цели из: 0x1db98, 0x1dbbc
- `0x1dbf0..0x1dc0a` (26 Б); цели из: 0x1dbc8
- `0x1dc0a..0x1dc26` (28 Б); цели из: 0x1dbfa
- `0x1dc26..0x1dc28` (2 Б); цели из: 0x1dc0c
- `0x1dc28..0x1dc34` (12 Б); цели из: 0x1dc24
- `0x1dc34..0x1dc46` (18 Б); цели из: 0x1dc08
- `0x1dc46..0x1dc56` (16 Б); цели из: 0x1dc38
- `0x1dc56..0x1dc62` (12 Б); цели из: 0x1dc44
- `0x1dc62..0x1dc66` (4 Б); цели из: 0x1dbec
- `0x1dc66..0x1dc70` (10 Б); цели из: 0x1dbdc
- `0x1dc70..0x1dc72` (2 Б); цели из: 0x1dbee, 0x1dc60
- `0x1dc72..0x1dd2c` (186 Б); цели из: 0x1dc64
- `0x1dd2c..0x1dd38` (12 Б); цели из: 0x1dc8c
- `0x1dd38..0x1dd56` (30 Б); цели из: 0x1d992, 0x1dc7c, 0x1dc92, 0x1dd34
- `0x1dd56..0x1dd74` (30 Б); цели из: 0x1dd46
- `0x1dd74..0x1dd7e` (10 Б); цели из: 0x1dd58

## Дизассембляция

```asm
  1d898:  push {r1, r2, r3, r4, r5, r6, r7, lr}
  1d89a:  ldr r1, [pc, #0x3f8]              -> RAM
  1d89c:  movs r0, #0                       
  1d89e:  ldrsh r0, [r1, r0]                
  1d8a0:  movs r1, #0x7d                    
  1d8a2:  lsls r1, r1, #6                   
  1d8a4:  muls r0, r1, r0                   
  1d8a6:  lsrs r0, r0, #0x10                
  1d8a8:  ldr r4, [pc, #0x3ec]              -> RAM
  1d8aa:  asrs r1, r1, #4                   
  1d8ac:  ldr r2, [pc, #0x3ec]              -> данные @0x02710
  1d8ae:  strh r0, [r4, #0x20]              
  1d8b0:  subs r1, r1, r0                   
  1d8b2:  muls r0, r2, r0                   
  1d8b4:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1d8b8:  mov r1, r4                        
  1d8ba:  str r0, [r1, #0x40]               
  1d8bc:  bl #0x1df84                       -> func_0x1df84
  1d8c0:  bl #0x1a010                       -> func_0x1a010
  1d8c4:  ldr r1, [pc, #0x3d8]              -> RAM
  1d8c6:  movs r2, #0                       
  1d8c8:  strh r0, [r1]                     
  1d8ca:  mov r0, r4                        
  1d8cc:  ldr r1, [r0, #0x3c]               
  1d8ce:  ldr r0, [pc, #0x3d4]              -> RAM
  1d8d0:  ldrsh r2, [r0, r2]                
  1d8d2:  adds r0, r1, r2                   
  1d8d4:  mov r1, r4                        
  1d8d6:  movs r2, #0x14                    
  1d8d8:  ldrsh r2, [r1, r2]                
  1d8da:  subs r0, r0, r2                   
  1d8dc:  str r0, [r1, #0x3c]               
  1d8de:  asrs r0, r0, #0xa                 
  1d8e0:  strh r0, [r1, #0x14]              
  1d8e2:  ldr r0, [pc, #0x3c4]              -> RAM
  1d8e4:  movs r1, #1                       
  1d8e6:  ldrh r0, [r0]                     
  1d8e8:  lsls r1, r1, #0xc                 
  1d8ea:  uxth r0, r0                       
  1d8ec:  ldr r2, [pc, #0x3bc]              -> данные @0x013ec
  1d8ee:  subs r1, r1, r0                   
  1d8f0:  muls r0, r2, r0                   
  1d8f2:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1d8f6:  ldr r1, [pc, #0x3b8]              -> RAM
  1d8f8:  str r0, [r1]                      
  1d8fa:  bl #0x1de0c                       -> func_0x1de0c
  1d8fe:  bl #0x1a010                       -> func_0x1a010
  1d902:  ldr r1, [pc, #0x3b0]              -> RAM
  1d904:  sxth r0, r0                       
  1d906:  strh r0, [r1]                     
  1d908:  ldr r1, [pc, #0x3ac]              -> RAM
  1d90a:  movs r2, #0                       
  1d90c:  ldr r1, [r1]                      
  1d90e:  adds r1, r1, r0                   
  1d910:  ldr r0, [pc, #0x3a8]              -> RAM
  1d912:  ldrsh r2, [r0, r2]                
  1d914:  subs r0, r1, r2                   
  1d916:  ldr r1, [pc, #0x3a0]              -> RAM
  1d918:  ldr r2, [pc, #0x380]              -> данные @0x02710
  1d91a:  str r0, [r1]                      
  1d91c:  ldr r1, [pc, #0x39c]              -> RAM
  1d91e:  asrs r0, r0, #6                   
  1d920:  strh r0, [r1]                     
  1d922:  ldr r0, [pc, #0x39c]              -> RAM
  1d924:  movs r1, #1                       
  1d926:  ldrh r0, [r0]                     
  1d928:  lsls r1, r1, #0xc                 
  1d92a:  uxth r0, r0                       
  1d92c:  subs r1, r1, r0                   
  1d92e:  muls r0, r2, r0                   
  1d930:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1d934:  ldr r1, [pc, #0x38c]              -> RAM
  1d936:  str r0, [r1]                      
  1d938:  bl #0x1a638                       -> func_0x1a638
  1d93c:  bl #0x1a010                       -> func_0x1a010
  1d940:  sxth r1, r0                       
  1d942:  ldr r0, [pc, #0x384]              -> RAM
  1d944:  movs r3, #0                       
  1d946:  strh r1, [r0]                     
  1d948:  ldr r0, [pc, #0x380]              -> RAM
  1d94a:  ldr r5, [pc, #0x38c]              -> RAM
  1d94c:  ldr r2, [r0]                      
  1d94e:  movs r6, #0                       
  1d950:  adds r2, r2, r1                   
  1d952:  ldr r1, [pc, #0x37c]              -> RAM
  1d954:  ldrsh r3, [r1, r3]                
  1d956:  subs r2, r2, r3                   
  1d958:  str r2, [r0]                      
  1d95a:  asrs r0, r2, #6                   
  1d95c:  sxth r0, r0                       
  1d95e:  strh r0, [r1]                     
  1d960:  str r0, [sp, #8]                  
  1d962:  ldr r0, [pc, #0x370]              -> RAM
  1d964:  ldrb r0, [r0]                     
  1d966:  cmp r0, #1                        
  1d968:  beq #0x1d98a                      
  1d96a:  ldr r0, [pc, #0x370]              -> RAM
  1d96c:  ldr r1, [pc, #0x374]              -> RAM
  1d96e:  ldrh r2, [r0]                     
  1d970:  movs r0, #0xb                     
  1d972:  lsls r0, r0, #0xa                 
  1d974:  ands r2, r0                       
  1d976:  ldr r0, [pc, #0x368]              -> RAM
  1d978:  ldr r7, [pc, #0x370]              -> RAM
  1d97a:  ldrb r0, [r0]                     
  1d97c:  orrs r2, r0                       
  1d97e:  ldr r0, [pc, #0x368]              -> RAM
  1d980:  beq #0x1d99c                      
  1d982:  ldrb r0, [r0]                     
  1d984:  cmp r0, #0xb                      
  1d986:  beq #0x1d994                      
  1d988:  b #0x1d998                        -> 0x1d998 (вне списка функций)
  1d98a:  ldr r0, [pc, #0x364]              -> RAM
  1d98c:  ldrh r1, [r0]                     
  1d98e:  ldr r0, [pc, #0x364]              -> RAM
  1d990:  strh r1, [r0]                     
  1d992:  b #0x1dd38                        -> 0x1dd38 (вне списка функций)
  1d994:  ldrh r0, [r1]                     
  1d996:  b #0x1d9e6                        -> 0x1d9e6 (вне списка функций)
  1d998:  ldr r0, [pc, #0x35c]              -> RAM
  1d99a:  b #0x1d9e4                        -> 0x1d9e4 (вне списка функций)
  1d99c:  ldrb r2, [r0]                     
  1d99e:  cmp r2, #0xb                      
  1d9a0:  beq #0x1d994                      
  1d9a2:  movs r3, #5                       
  1d9a4:  mvns r3, r3                       
  1d9a6:  ldr r0, [pc, #0x354]              -> RAM
  1d9a8:  ldr r1, [pc, #0x354]              -> RAM
  1d9aa:  cmp r2, #2                        
  1d9ac:  beq #0x1d9be                      
  1d9ae:  cmp r2, #3                        
  1d9b0:  bne #0x1d998                      
  1d9b2:  movs r2, #0                       
  1d9b4:  ldrsb r2, [r1, r2]                
  1d9b6:  cmp r2, r3                        
  1d9b8:  bgt #0x1d9f4                      
  1d9ba:  ldrh r0, [r0]                     
  1d9bc:  b #0x1da10                        -> 0x1da10 (вне списка функций)
  1d9be:  movs r2, #0                       
  1d9c0:  ldrsb r2, [r1, r2]                
  1d9c2:  cmp r2, r3                        
  1d9c4:  ble #0x1d998                      
  1d9c6:  cmp r2, #2                        
  1d9c8:  bge #0x1d9e4                      
  1d9ca:  movs r1, #2                       
  1d9cc:  subs r1, r1, r2                   
  1d9ce:  ldr r2, [pc, #0x328]              -> RAM
  1d9d0:  movs r3, #0                       
  1d9d2:  ldrsh r3, [r2, r3]                
  1d9d4:  ldrh r0, [r0]                     
  1d9d6:  muls r1, r3, r1                   
  1d9d8:  asrs r2, r1, #0x1f                
  1d9da:  lsrs r2, r2, #0x1d                
  1d9dc:  adds r1, r2, r1                   
  1d9de:  asrs r1, r1, #3                   
  1d9e0:  subs r0, r0, r1                   
  1d9e2:  b #0x1d9e6                        -> 0x1d9e6 (вне списка функций)
  1d9e4:  ldrh r0, [r0]                     
  1d9e6:  strh r0, [r4, #0x1e]              
  1d9e8:  strb r6, [r4]                     
  1d9ea:  ldm r5!, {r0, r1}                 
  1d9ec:  str r1, [r4, #0x7c]               
  1d9ee:  str r0, [r4, #0x78]               
  1d9f0:  stm r7!, {r0, r1}                 
  1d9f2:  b #0x1da2a                        -> 0x1da2a (вне списка функций)
  1d9f4:  cmp r2, #2                        
  1d9f6:  bge #0x1da58                      
  1d9f8:  movs r1, #2                       
  1d9fa:  subs r1, r1, r2                   
  1d9fc:  movs r2, #0                       
  1d9fe:  ldrsh r2, [r0, r2]                
  1da00:  muls r1, r2, r1                   
  1da02:  asrs r0, r1, #0x1f                
  1da04:  lsrs r0, r0, #0x1d                
  1da06:  adds r0, r0, r1                   
  1da08:  asrs r1, r0, #3                   
  1da0a:  ldr r0, [pc, #0x2e4]              -> RAM
  1da0c:  ldrh r0, [r0]                     
  1da0e:  subs r0, r0, r1                   
  1da10:  strh r0, [r4, #0x1e]              
  1da12:  ldr r0, [pc, #0x2f0]              -> RAM
  1da14:  ldrb r0, [r0]                     
  1da16:  cmp r0, #1                        
  1da18:  beq #0x1da5c                      
  1da1a:  ldrh r0, [r4, #0x1e]              
  1da1c:  strh r0, [r4, #0x1e]              
  1da1e:  strb r6, [r4]                     
  1da20:  ldm r5!, {r0, r1}                 
  1da22:  str r1, [r4, #0x7c]               
  1da24:  str r0, [r4, #0x78]               
  1da26:  str r1, [r7, #0xc]                
  1da28:  str r0, [r7, #8]                  
  1da2a:  subs r5, #8                       
  1da2c:  ldr r0, [pc, #0x270]              -> RAM
  1da2e:  movs r1, #0                       
  1da30:  ldrsh r1, [r0, r1]                
  1da32:  ldr r7, [pc, #0x2d4]              -> RAM
  1da34:  str r1, [sp]                      
  1da36:  cmp r1, #0x6e                     
  1da38:  bgt #0x1db22                      
  1da3a:  mov r0, r1                        
  1da3c:  cmp r1, #0x5a                     
  1da3e:  ble #0x1db24                      
  1da40:  movs r0, #0x1e                    
  1da42:  ldrsh r0, [r4, r0]                
  1da44:  movs r1, #0x14                    
  1da46:  str r0, [sp, #4]                  
  1da48:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1da4c:  ldr r1, [sp]                      
  1da4e:  subs r1, #0x5a                    
  1da50:  muls r0, r1, r0                   
  1da52:  ldr r1, [sp, #4]                  
  1da54:  subs r0, r1, r0                   
  1da56:  b #0x1db82                        -> 0x1db82 (вне списка функций)
  1da58:  ldr r0, [pc, #0x294]              -> RAM
  1da5a:  b #0x1d9ba                        -> 0x1d9ba (вне списка функций)
  1da5c:  ldrb r0, [r4]                     
  1da5e:  cmp r0, #0                        
  1da60:  beq #0x1da82                      
  1da62:  ldr r2, [r5]                      
  1da64:  ldr r0, [r5, #4]                  
  1da66:  str r2, [sp]                      
  1da68:  str r0, [sp, #4]                  
  1da6a:  ldr r1, [r4, #0x78]               
  1da6c:  ldr r3, [r4, #0x7c]               
  1da6e:  subs r2, r2, r1                   
  1da70:  sbcs r0, r3                       
  1da72:  ldr r3, [pc, #0x298]              
  1da74:  mov ip, r0                        
  1da76:  movs r1, #0                       
  1da78:  subs r3, r2, r3                   
  1da7a:  sbcs r0, r1                       
  1da7c:  bhs #0x1daec                      
  1da7e:  ldrh r0, [r4, #0x1e]              
  1da80:  b #0x1db1e                        -> 0x1db1e (вне списка функций)
  1da82:  ldr r1, [pc, #0x28c]              -> RAM
  1da84:  movs r0, #0x14                    
  1da86:  movs r2, #0                       
  1da88:  ldrsh r0, [r4, r0]                
  1da8a:  ldrsh r2, [r1, r2]                
  1da8c:  cmp r0, r2                        
  1da8e:  ble #0x1dabc                      
  1da90:  ldm r5!, {r0, r1}                 
  1da92:  str r1, [sp]                      
  1da94:  ldr r2, [r4, #0x78]               
  1da96:  subs r5, #8                       
  1da98:  ldr r3, [r4, #0x7c]               
  1da9a:  subs r2, r0, r2                   
  1da9c:  mov ip, r0                        
  1da9e:  sbcs r1, r3                       
  1daa0:  ldr r0, [pc, #0x268]              
  1daa2:  movs r3, #0                       
  1daa4:  subs r2, r0, r2                   
  1daa6:  sbcs r3, r1                       
  1daa8:  bhs #0x1dab0                      
  1daaa:  movs r0, #1                       
  1daac:  strb r0, [r4]                     
  1daae:  b #0x1dab2                        -> 0x1dab2 (вне списка функций)
  1dab0:  strb r6, [r4]                     
  1dab2:  mov r0, ip                        
  1dab4:  ldr r1, [sp]                      
  1dab6:  stm r7!, {r0, r1}                 
  1dab8:  subs r7, #8                       
  1daba:  b #0x1dae2                        -> 0x1dae2 (вне списка функций)
  1dabc:  strb r6, [r4]                     
  1dabe:  ldm r5!, {r0, r1}                 
  1dac0:  str r1, [sp]                      
  1dac2:  ldm r7!, {r2, r3}                 
  1dac4:  subs r5, #8                       
  1dac6:  subs r7, #8                       
  1dac8:  subs r2, r0, r2                   
  1daca:  mov ip, r0                        
  1dacc:  sbcs r1, r3                       
  1dace:  movs r0, #0x7d                    
  1dad0:  lsls r0, r0, #7                   
  1dad2:  movs r3, #0                       
  1dad4:  subs r2, r0, r2                   
  1dad6:  sbcs r3, r1                       
  1dad8:  bhs #0x1dae2                      
  1dada:  ldr r1, [sp]                      
  1dadc:  mov r0, ip                        
  1dade:  str r1, [r4, #0x7c]               
  1dae0:  str r0, [r4, #0x78]               
  1dae2:  ldrh r0, [r4, #0x1e]              
  1dae4:  strh r0, [r4, #0x1e]              
  1dae6:  mov r0, ip                        
  1dae8:  ldr r1, [r5, #4]                  
  1daea:  b #0x1db68                        -> 0x1db68 (вне списка функций)
  1daec:  ldr r0, [pc, #0x224]              
  1daee:  mov r1, ip                        
  1daf0:  movs r3, #0                       
  1daf2:  subs r0, r2, r0                   
  1daf4:  sbcs r1, r3                       
  1daf6:  bhs #0x1db5a                      
  1daf8:  ldr r0, [pc, #0x210]              
  1dafa:  ldr r1, [pc, #0x21c]              -> RAM
  1dafc:  rsbs r0, r0, #0                   
  1dafe:  adds r0, r2, r0                   
  1db00:  ldrsh r2, [r1, r3]                
  1db02:  ldr r1, [pc, #0x218]              
  1db04:  muls r0, r2, r0                   
  1db06:  str r0, [r4, #0x44]               
  1db08:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1db0c:  ldr r1, [pc, #0x1e0]              -> RAM
  1db0e:  ldrh r1, [r1]                     
  1db10:  subs r0, r1, r0                   
  1db12:  sxth r0, r0                       
  1db14:  strh r0, [r4, #0x12]              
  1db16:  movs r1, #0x1e                    
  1db18:  ldrsh r1, [r4, r1]                
  1db1a:  cmp r1, r0                        
  1db1c:  ble #0x1db26                      
  1db1e:  strh r0, [r4, #0x1e]              
  1db20:  b #0x1db28                        -> 0x1db28 (вне списка функций)
  1db22:  b #0x1db74                        -> 0x1db74 (вне списка функций)
  1db24:  b #0x1db6e                        -> 0x1db6e (вне списка функций)
  1db26:  strh r1, [r4, #0x1e]              
  1db28:  ldr r0, [pc, #0x178]              -> RAM
  1db2a:  movs r1, #0                       
  1db2c:  ldrsh r1, [r0, r1]                
  1db2e:  ldr r0, [pc, #0x1e8]              -> RAM
  1db30:  movs r2, #0                       
  1db32:  ldrsh r2, [r0, r2]                
  1db34:  cmp r1, r2                        
  1db36:  bge #0x1db60                      
  1db38:  ldr r1, [sp]                      
  1db3a:  ldr r2, [r7, #8]                  
  1db3c:  ldr r0, [sp, #4]                  
  1db3e:  ldr r3, [r7, #0xc]                
  1db40:  subs r1, r1, r2                   
  1db42:  sbcs r0, r3                       
  1db44:  movs r3, #0x7d                    
  1db46:  lsls r3, r3, #7                   
  1db48:  movs r2, #0                       
  1db4a:  subs r1, r3, r1                   
  1db4c:  sbcs r2, r0                       
  1db4e:  blo #0x1db52                      
  1db50:  b #0x1da2c                        -> 0x1da2c (вне списка функций)
  1db52:  strb r6, [r4]                     
  1db54:  ldrh r0, [r4, #0x1e]              
  1db56:  strh r0, [r4, #0x1e]              
  1db58:  b #0x1da2c                        -> 0x1da2c (вне списка функций)
  1db5a:  ldr r0, [pc, #0x19c]              -> RAM
  1db5c:  ldrh r0, [r0]                     
  1db5e:  b #0x1db1e                        -> 0x1db1e (вне списка функций)
  1db60:  movs r0, #1                       
  1db62:  strb r0, [r4]                     
  1db64:  ldr r1, [sp, #4]                  
  1db66:  ldr r0, [sp]                      
  1db68:  str r1, [r7, #0xc]                
  1db6a:  str r0, [r7, #8]                  
  1db6c:  b #0x1da2c                        -> 0x1da2c (вне списка функций)
  1db6e:  movs r1, #0x28                    
  1db70:  cmn r0, r1                        
  1db72:  bgt #0x1db80                      
  1db74:  strh r6, [r4, #0x18]              
  1db76:  ldrh r0, [r7]                     
  1db78:  movs r1, #0x40                    
  1db7a:  orrs r0, r1                       
  1db7c:  strh r0, [r7]                     
  1db7e:  b #0x1db8c                        -> 0x1db8c (вне списка функций)
  1db80:  ldrh r0, [r4, #0x1e]              
  1db82:  strh r0, [r4, #0x18]              
  1db84:  ldrh r1, [r7]                     
  1db86:  movs r0, #0x40                    
  1db88:  bics r1, r0                       
  1db8a:  strh r1, [r7]                     
  1db8c:  ldr r0, [pc, #0x190]              -> RAM
  1db8e:  ldrb r1, [r0]                     
  1db90:  cmp r1, #0xa                      
  1db92:  bhs #0x1db9a                      
  1db94:  ldr r0, [pc, #0x160]              -> RAM
  1db96:  ldrh r0, [r0]                     
  1db98:  b #0x1dbc0                        -> 0x1dbc0 (вне списка функций)
  1db9a:  cmp r1, #0x14                     
  1db9c:  bhs #0x1dbbe                      
  1db9e:  movs r2, #0x1e                    
  1dba0:  ldrsh r2, [r4, r2]                
  1dba2:  ldr r0, [pc, #0x154]              -> RAM
  1dba4:  movs r3, #0                       
  1dba6:  str r2, [sp]                      
  1dba8:  ldrsh r3, [r0, r3]                
  1dbaa:  subs r0, r2, r3                   
  1dbac:  movs r2, #0x14                    
  1dbae:  subs r1, r2, r1                   
  1dbb0:  muls r0, r1, r0                   
  1dbb2:  movs r1, #0xa                     
  1dbb4:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1dbb8:  ldr r2, [sp]                      
  1dbba:  subs r0, r2, r0                   
  1dbbc:  b #0x1dbc0                        -> 0x1dbc0 (вне списка функций)
  1dbbe:  ldrh r0, [r4, #0x1e]              
  1dbc0:  strh r0, [r4, #0x16]              
  1dbc2:  ldr r0, [pc, #0x160]              -> RAM
  1dbc4:  ldrb r0, [r0]                     
  1dbc6:  cmp r0, #1                        
  1dbc8:  beq #0x1dbf0                      
  1dbca:  ldrh r0, [r4, #0x1e]              
  1dbcc:  strh r0, [r4, #0x1a]              
  1dbce:  strh r0, [r4, #0x1c]              
  1dbd0:  movs r1, #0x18                    
  1dbd2:  movs r2, #0x16                    
  1dbd4:  ldrsh r1, [r4, r1]                
  1dbd6:  ldrsh r2, [r4, r2]                
  1dbd8:  ldr r0, [pc, #0x14c]              -> RAM
  1dbda:  cmp r1, r2                        
  1dbdc:  bge #0x1dc66                      
  1dbde:  movs r2, #0x1a                    
  1dbe0:  ldrsh r2, [r4, r2]                
  1dbe2:  cmp r1, r2                        
  1dbe4:  bge #0x1dc5a                      
  1dbe6:  movs r2, #0x1c                    
  1dbe8:  ldrsh r2, [r4, r2]                
  1dbea:  cmp r1, r2                        
  1dbec:  blt #0x1dc62                      
  1dbee:  b #0x1dc70                        -> 0x1dc70 (вне списка функций)
  1dbf0:  ldr r0, [pc, #0xc8]               -> RAM
  1dbf2:  movs r1, #0                       
  1dbf4:  ldrsh r1, [r0, r1]                
  1dbf6:  str r1, [sp]                      
  1dbf8:  cmp r1, #0x82                     
  1dbfa:  ble #0x1dc0a                      
  1dbfc:  strh r6, [r4, #0x1a]              
  1dbfe:  ldrh r0, [r7]                     
  1dc00:  movs r1, #1                       
  1dc02:  lsls r1, r1, #9                   
  1dc04:  orrs r0, r1                       
  1dc06:  strh r0, [r7]                     
  1dc08:  b #0x1dc34                        -> 0x1dc34 (вне списка функций)
  1dc0a:  cmp r1, #0x78                     
  1dc0c:  ble #0x1dc26                      
  1dc0e:  movs r0, #0x1e                    
  1dc10:  ldrsh r0, [r4, r0]                
  1dc12:  movs r1, #0xa                     
  1dc14:  str r0, [sp, #4]                  
  1dc16:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1dc1a:  ldr r1, [sp]                      
  1dc1c:  subs r1, #0x78                    
  1dc1e:  muls r0, r1, r0                   
  1dc20:  ldr r1, [sp, #4]                  
  1dc22:  subs r0, r1, r0                   
  1dc24:  b #0x1dc28                        -> 0x1dc28 (вне списка функций)
  1dc26:  ldrh r0, [r4, #0x1e]              
  1dc28:  strh r0, [r4, #0x1a]              
  1dc2a:  ldrh r1, [r7]                     
  1dc2c:  movs r0, #1                       
  1dc2e:  lsls r0, r0, #9                   
  1dc30:  bics r1, r0                       
  1dc32:  strh r1, [r7]                     
  1dc34:  ldr r0, [sp, #8]                  
  1dc36:  cmp r0, #0x46                     
  1dc38:  ble #0x1dc46                      
  1dc3a:  strh r6, [r4, #0x1c]              
  1dc3c:  ldrh r0, [r7]                     
  1dc3e:  movs r1, #1                       
  1dc40:  lsls r1, r1, #0xf                 
  1dc42:  orrs r0, r1                       
  1dc44:  b #0x1dc56                        -> 0x1dc56 (вне списка функций)
  1dc46:  ldrh r0, [r4, #0x1e]              
  1dc48:  strh r0, [r4, #0x1c]              
  1dc4a:  ldr r0, [sp, #8]                  
  1dc4c:  cmp r0, #0x41                     
  1dc4e:  bge #0x1dbd0                      
  1dc50:  ldrh r0, [r7]                     
  1dc52:  lsls r0, r0, #0x11                
  1dc54:  lsrs r0, r0, #0x11                
  1dc56:  strh r0, [r7]                     
  1dc58:  b #0x1dbd0                        -> 0x1dbd0 (вне списка функций)
  1dc5a:  movs r1, #0x1c                    
  1dc5c:  ldrsh r1, [r4, r1]                
  1dc5e:  cmp r2, r1                        
  1dc60:  blt #0x1dc70                      
  1dc62:  strh r1, [r0]                     
  1dc64:  b #0x1dc72                        -> 0x1dc72 (вне списка функций)
  1dc66:  movs r1, #0x1a                    
  1dc68:  ldrsh r1, [r4, r1]                
  1dc6a:  cmp r2, r1                        
  1dc6c:  blt #0x1dc5a                      
  1dc6e:  b #0x1dbe6                        -> 0x1dbe6 (вне списка функций)
  1dc70:  strh r2, [r0]                     
  1dc72:  ldrb r1, [r4, #1]                 
  1dc74:  adds r1, r1, #1                   
  1dc76:  uxtb r1, r1                       
  1dc78:  strb r1, [r4, #1]                 
  1dc7a:  cmp r1, #5                        
  1dc7c:  blo #0x1dd38                      
  1dc7e:  strb r6, [r4, #1]                 
  1dc80:  ldr r1, [pc, #0x70]               -> RAM
  1dc82:  movs r2, #0                       
  1dc84:  movs r3, #0                       
  1dc86:  ldrsh r2, [r1, r2]                
  1dc88:  ldrsh r3, [r0, r3]                
  1dc8a:  cmp r2, r3                        
  1dc8c:  bge #0x1dd2c                      
  1dc8e:  adds r2, r2, #1                   
  1dc90:  strh r2, [r1]                     
  1dc92:  b #0x1dd38                        -> 0x1dd38 (вне списка функций)
  1dc94:  lsls r2, r7, #9                   
  1dc96:  movs r0, #0                       
  1dc98:  lsls r0, r1, #0xf                 
  1dc9a:  movs r0, #0                       
  1dc9c:  movs r7, #0x10                    
  1dc9e:  movs r0, r0                       
  1dca0:  lsls r4, r3, #0xc                 
  1dca2:  movs r0, #0                       
  1dca4:  lsls r6, r5, #9                   
  1dca6:  movs r0, #0                       
  1dca8:  lsls r6, r0, #0xa                 
  1dcaa:  movs r0, #0                       
  1dcac:  asrs r4, r5, #0xf                 
  1dcae:  movs r0, r0                       
  1dcb0:  lsls r4, r1, #0xa                 
  1dcb2:  movs r0, #0                       
  1dcb4:  lsls r2, r2, #0xa                 
  1dcb6:  movs r0, #0                       
  1dcb8:  lsls r4, r2, #0xa                 
  1dcba:  movs r0, #0                       
  1dcbc:  lsls r0, r2, #0xa                 
  1dcbe:  movs r0, #0                       
  1dcc0:  lsls r6, r3, #0xa                 
  1dcc2:  movs r0, #0                       
  1dcc4:  lsls r4, r4, #0xa                 
  1dcc6:  movs r0, #0                       
  1dcc8:  lsls r2, r5, #0xa                 
  1dcca:  movs r0, #0                       
  1dccc:  lsls r4, r5, #0xa                 
  1dcce:  movs r0, #0                       
  1dcd0:  lsls r0, r5, #0xa                 
  1dcd2:  movs r0, #0                       
  1dcd4:  lsls r1, r7, #0xc                 
  1dcd6:  movs r0, #0                       
  1dcd8:  lsls r0, r4, #7                   
  1dcda:  movs r0, #0                       
  1dcdc:  lsls r6, r1, #0xc                 
  1dcde:  movs r0, #0                       
  1dce0:  lsls r1, r4, #0xc                 
  1dce2:  movs r0, #0                       
  1dce4:  lsls r4, r1, #8                   
  1dce6:  movs r0, #0                       
  1dce8:  lsls r1, r5, #8                   
  1dcea:  movs r0, #0                       
  1dcec:  lsls r0, r1, #0x11                
  1dcee:  movs r0, #0                       
  1dcf0:  lsls r6, r6, #7                   
  1dcf2:  movs r0, #0                       
  1dcf4:  lsls r4, r3, #8                   
  1dcf6:  movs r0, #0                       
  1dcf8:  lsls r6, r0, #8                   
  1dcfa:  movs r0, #0                       
  1dcfc:  lsls r4, r0, #8                   
  1dcfe:  movs r0, #0                       
  1dd00:  lsls r4, r1, #0xc                 
  1dd02:  movs r0, #0                       
  1dd04:  lsls r0, r5, #0xc                 
  1dd06:  movs r0, #0                       
  1dd08:  lsls r6, r3, #8                   
  1dd0a:  movs r0, #0                       
  1dd0c:  ldrb r0, [r0, #0x10]              
  1dd0e:  lsls r2, r2, #2                   
  1dd10:  lsls r2, r0, #8                   
  1dd12:  movs r0, #0                       
  1dd14:  ldr r0, [r0, #0x60]               
  1dd16:  lsls r6, r7, #2                   
  1dd18:  lsls r0, r1, #8                   
  1dd1a:  movs r0, #0                       
  1dd1c:  addw r0, r0, #0x2b                
  1dd20:  lsls r6, r0, #0xc                 
  1dd22:  movs r0, #0                       
  1dd24:  lsls r2, r5, #0xc                 
  1dd26:  movs r0, #0                       
  1dd28:  lsls r0, r6, #7                   
  1dd2a:  movs r0, #0                       
  1dd2c:  subs r2, r2, #1                   
  1dd2e:  sxth r0, r2                       
  1dd30:  strh r0, [r1]                     
  1dd32:  cmp r0, #0                        
  1dd34:  bge #0x1dd38                      
  1dd36:  strh r6, [r1]                     
  1dd38:  ldr r0, [pc, #0x44]               -> RAM
  1dd3a:  movs r1, #8                       
  1dd3c:  ldrsh r1, [r0, r1]                
  1dd3e:  ldr r0, [pc, #0x44]               -> RAM
  1dd40:  cmp r1, #0x68                     
  1dd42:  ldr r1, [pc, #0x44]               -> RAM
  1dd44:  ldrb r1, [r1]                     
  1dd46:  bge #0x1dd56                      
  1dd48:  lsls r1, r1, #0x1a                
  1dd4a:  bpl #0x1dd52                      
  1dd4c:  movs r1, #1                       
  1dd4e:  strb r1, [r0]                     
  1dd50:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  1dd52:  strb r6, [r0]                     
  1dd54:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  1dd56:  lsls r1, r1, #0x1a                
  1dd58:  bpl #0x1dd74                      
  1dd5a:  ldr r2, [r5]                      
  1dd5c:  ldr r3, [r4, #0x70]               
  1dd5e:  ldr r1, [r5, #4]                  
  1dd60:  ldr r4, [r4, #0x74]               
  1dd62:  subs r3, r2, r3                   
  1dd64:  sbcs r1, r4                       
  1dd66:  movs r4, #0x7d                    
  1dd68:  lsls r4, r4, #7                   
  1dd6a:  movs r2, #0                       
  1dd6c:  subs r3, r4, r3                   
  1dd6e:  sbcs r2, r1                       
  1dd70:  bhs #0x1dd52                      
  1dd72:  b #0x1dd4c                        -> 0x1dd4c (вне списка функций)
  1dd74:  strb r6, [r0]                     
  1dd76:  ldm r5!, {r0, r1}                 
  1dd78:  str r1, [r4, #0x74]               
  1dd7a:  str r0, [r4, #0x70]               
  1dd7c:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  ; --- literal-пул @0x1dc94 (38 слов) ---
  1dc94:  .word 0x2000027a  ; RAM
  1dc98:  .word 0x200003c8  ; RAM
  1dc9c:  .word 0x00002710  ; данные @0x02710
  1dca0:  .word 0x2000031c  ; RAM
  1dca4:  .word 0x2000026e  ; RAM
  1dca8:  .word 0x20000286  ; RAM
  1dcac:  .word 0x000013ec  ; данные @0x013ec
  1dcb0:  .word 0x2000028c  ; RAM
  1dcb4:  .word 0x20000292  ; RAM
  1dcb8:  .word 0x20000294  ; RAM
  1dcbc:  .word 0x20000290  ; RAM
  1dcc0:  .word 0x2000029e  ; RAM
  1dcc4:  .word 0x200002a4  ; RAM
  1dcc8:  .word 0x200002aa  ; RAM
  1dccc:  .word 0x200002ac  ; RAM
  1dcd0:  .word 0x200002a8  ; RAM
  1dcd4:  .word 0x20000339  ; RAM
  1dcd8:  .word 0x200001e0  ; RAM
  1dcdc:  .word 0x2000030e  ; RAM
  1dce0:  .word 0x20000321  ; RAM
  1dce4:  .word 0x2000020c  ; RAM
  1dce8:  .word 0x20000229  ; RAM
  1dcec:  .word 0x20000448  ; RAM
  1dcf0:  .word 0x200001f6  ; RAM
  1dcf4:  .word 0x2000021c  ; RAM
  1dcf8:  .word 0x20000206  ; RAM
  1dcfc:  .word 0x20000204  ; RAM
  1dd00:  .word 0x2000030c  ; RAM
  1dd04:  .word 0x20000328  ; RAM
  1dd08:  .word 0x2000021e  ; RAM
  1dd0c:  .word 0x00927c00
  1dd10:  .word 0x20000202  ; RAM
  1dd14:  .word 0x00be6e00
  1dd18:  .word 0x20000208  ; RAM
  1dd1c:  .word 0x002bf200
  1dd20:  .word 0x20000306  ; RAM
  1dd24:  .word 0x2000032a  ; RAM
  1dd28:  .word 0x200001f0  ; RAM
  ; --- literal-пул @0x1dd80 (3 слов) — ВНЕ границ функции ---
  1dd80:  .word 0x20001768  ; RAM
  1dd84:  .word 0x20000311  ; RAM
  1dd88:  .word 0x2000030e  ; RAM
```
