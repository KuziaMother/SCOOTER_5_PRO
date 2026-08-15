# func_0x0e808

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e808) | `0x0000e808` |
| размер кода | 592 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a49a — flash-mirror @0x1a49a (r2)
- 0x200012ba — RAM (r0)
- 0x80000f3c — прочее (r1)

## Вызовы (callees)

- 0x0e8d6 (b, вне списка функций)
- 0x0e940 (b, вне списка функций)
- 0x0e968 (b, вне списка функций)
- 0x0ea1e (b, вне списка функций)
- 0x0ea36 (b, вне списка функций)
- 0x0ea4a (b, вне списка функций)
- 0x0ea54 (b, вне списка функций)
- 0x161c6 (bl, вне списка функций)
- `func_0x16328` (0x00016328, bl)
- 0x1654c (bl, вне списка функций)
- 0x16570 (bl, вне списка функций)
- `func_0x167b6` (0x000167b6, bl)
- `func_0x169f0` (0x000169f0, bl)
- `func_0x17094` (0x00017094, bl)

## Кто вызывает (callers / xrefs)

- `func_0x069e4` (bl @0x00006b84)
- `func_0x069e4` (bl @0x00006c3e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0e844..0x0e85a` (22 Б); цели из: 0x0e836
- `0x0e85a..0x0e872` (24 Б); цели из: 0x0e842
- `0x0e872..0x0e878` (6 Б); цели из: 0x0e86e
- `0x0e878..0x0e89e` (38 Б); цели из: 0x0e862
- `0x0e89e..0x0e8b4` (22 Б); цели из: 0x0e84c, 0x0e858
- `0x0e8b4..0x0e8bc` (8 Б); цели из: 0x0e8b0
- `0x0e8bc..0x0e8d0` (20 Б); цели из: 0x0e818
- `0x0e8d0..0x0e8d6` (6 Б); цели из: 0x0e8ca
- `0x0e8d6..0x0e8f6` (32 Б); цели из: 0x0e880, 0x0e888, 0x0e89c, 0x0e8ba
- `0x0e8f6..0x0e8fc` (6 Б); цели из: 0x0e8f0
- `0x0e8fc..0x0e922` (38 Б); цели из: 0x0e8e2
- `0x0e922..0x0e938` (22 Б); цели из: 0x0e91c
- `0x0e938..0x0e940` (8 Б); цели из: 0x0e932
- `0x0e940..0x0e964` (36 Б); цели из: 0x0e936
- `0x0e964..0x0e968` (4 Б); цели из: 0x0e95c
- `0x0e968..0x0e984` (28 Б); цели из: 0x0e928, 0x0e962
- `0x0e984..0x0e994` (16 Б); цели из: 0x0e97a
- `0x0e994..0x0e99a` (6 Б); цели из: 0x0e982
- `0x0e99a..0x0e9bc` (34 Б); цели из: 0x0e972, 0x0e98a, 0x0e992
- `0x0e9bc..0x0e9cc` (16 Б); цели из: 0x0e9b6
- `0x0e9cc..0x0e9ea` (30 Б); цели из: 0x0e9c6
- `0x0e9ea..0x0ea08` (30 Б); цели из: 0x0e9e2
- `0x0ea08..0x0ea18` (16 Б); цели из: 0x0ea02
- `0x0ea18..0x0ea1e` (6 Б); цели из: 0x0ea10
- `0x0ea1e..0x0ea32` (20 Б); цели из: 0x0ea06, 0x0ea16
- `0x0ea32..0x0ea36` (4 Б); цели из: 0x0e9f6
- `0x0ea36..0x0ea42` (12 Б); цели из: 0x0ea30
- `0x0ea42..0x0ea4a` (8 Б); цели из: 0x0ea3a
- `0x0ea4a..0x0ea50` (6 Б); цели из: 0x0ea40
- `0x0ea50..0x0ea54` (4 Б); цели из: 0x0e9a0
- `0x0ea54..0x0ea58` (4 Б); цели из: 0x0e998, 0x0e9e8, 0x0ea4e

## Дизассембляция

```asm
  0e808:  push.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  0e80c:  mov r7, r0                        
  0e80e:  mov sl, r1                        
  0e810:  ldr r0, [pc, #0x244]              -> RAM
  0e812:  ldr r0, [r0, #0x40]               
  0e814:  cmp.w r0, #0x1f4                  
  0e818:  bne #0xe8bc                       
  0e81a:  movs r0, #0                       
  0e81c:  ldr r1, [pc, #0x238]              -> RAM
  0e81e:  str r0, [r1, #0x40]               
  0e820:  mov r0, r1                        
  0e822:  ldrh.w r6, [r0, #0x4c]            
  0e826:  ldrh.w r0, [sl]                   
  0e82a:  strh.w r0, [r1, #0x4c]            
  0e82e:  mov r0, r1                        
  0e830:  ldrh.w r0, [r0, #0x4c]            
  0e834:  cmp r0, r6                        
  0e836:  bgt #0xe844                       
  0e838:  mov r0, r1                        
  0e83a:  ldrh.w r0, [r0, #0x4c]            
  0e83e:  subs r0, r6, r0                   
  0e840:  cmp r0, #1                        
  0e842:  ble #0xe85a                       
  0e844:  ldr r0, [pc, #0x210]              -> RAM
  0e846:  ldrh.w r0, [r0, #0x4c]            
  0e84a:  cmp r0, r6                        
  0e84c:  ble #0xe89e                       
  0e84e:  ldr r0, [pc, #0x208]              -> RAM
  0e850:  ldrh.w r0, [r0, #0x4c]            
  0e854:  subs r0, r0, r6                   
  0e856:  cmp r0, #1                        
  0e858:  bgt #0xe89e                       
  0e85a:  ldr r0, [pc, #0x1fc]              -> RAM
  0e85c:  ldrb.w r0, [r0, #0x67]            
  0e860:  cmp r0, #0xc                      
  0e862:  bge #0xe878                       
  0e864:  ldr r0, [pc, #0x1f0]              -> RAM
  0e866:  ldrb.w r0, [r0, #0x67]            
  0e86a:  adds r4, r0, #2                   
  0e86c:  cmp r4, #0xff                     
  0e86e:  ble #0xe872                       
  0e870:  movs r4, #0xff                    
  0e872:  ldr r1, [pc, #0x1e4]              -> RAM
  0e874:  strb.w r4, [r1, #0x67]            
  0e878:  ldr r0, [pc, #0x1dc]              -> RAM
  0e87a:  ldrb.w r0, [r0, #0x67]            
  0e87e:  cmp r0, #0xc                      
  0e880:  blt #0xe8d6                       
  0e882:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0e886:  cmp r0, #0xc8                     
  0e888:  bgt #0xe8d6                       
  0e88a:  movs r0, #0                       
  0e88c:  ldr r1, [pc, #0x1c8]              -> RAM
  0e88e:  strb.w r0, [r1, #0x67]            
  0e892:  mov r0, r1                        
  0e894:  ldrh.w r0, [r0, #0x4c]            
  0e898:  subs r0, #0xe                     
  0e89a:  str r0, [r1, #0x2c]               
  0e89c:  b #0xe8d6                         -> 0x0e8d6 (вне списка функций)
  0e89e:  ldr r0, [pc, #0x1b8]              -> RAM
  0e8a0:  ldrb.w r0, [r0, #0x67]            
  0e8a4:  cbz r0, #0xe8d6                   
  0e8a6:  ldr r0, [pc, #0x1b0]              -> RAM
  0e8a8:  ldrb.w r0, [r0, #0x67]            
  0e8ac:  subs r4, r0, #1                   
  0e8ae:  cmp r4, #0                        
  0e8b0:  bge #0xe8b4                       
  0e8b2:  movs r4, #0                       
  0e8b4:  ldr r1, [pc, #0x1a0]              -> RAM
  0e8b6:  strb.w r4, [r1, #0x67]            
  0e8ba:  b #0xe8d6                         -> 0x0e8d6 (вне списка функций)
  0e8bc:  ldr r0, [pc, #0x198]              -> RAM
  0e8be:  ldr r0, [r0, #0x40]               
  0e8c0:  add.w fp, r0, #1                  
  0e8c4:  ldr r0, [pc, #0x190]              -> RAM
  0e8c6:  ldr r0, [r0, #0x40]               
  0e8c8:  cmp r0, fp                        
  0e8ca:  bls #0xe8d0                       
  0e8cc:  mov.w fp, #-1                     
  0e8d0:  ldr r0, [pc, #0x184]              -> RAM
  0e8d2:  str.w fp, [r0, #0x40]             
  0e8d6:  ldr r0, [pc, #0x180]              -> RAM
  0e8d8:  ldrh.w r0, [r0, #0x4e]            
  0e8dc:  movw r1, #0xbb8                   
  0e8e0:  cmp r0, r1                        
  0e8e2:  bgt #0xe8fc                       
  0e8e4:  ldr r0, [pc, #0x170]              -> RAM
  0e8e6:  ldrh.w r0, [r0, #0x4e]            
  0e8ea:  adds r4, r0, #1                   
  0e8ec:  cmp.w r4, #0x10000                
  0e8f0:  blt #0xe8f6                       
  0e8f2:  movw r4, #0xffff                  
  0e8f6:  ldr r1, [pc, #0x160]              -> RAM
  0e8f8:  strh.w r4, [r1, #0x4e]            
  0e8fc:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0e900:  movs r1, #0x32                    
  0e902:  str r0, [sp]                      
  0e904:  bl #0x17094                       -> func_0x17094
  0e908:  mov.w r1, #0x3e8                  
  0e90c:  sdiv r0, r0, r1                   
  0e910:  ldrh.w r1, [sl]                   
  0e914:  subs r5, r1, r0                   
  0e916:  ldr r0, [pc, #0x140]              -> RAM
  0e918:  ldr r0, [r0, #0x2c]               
  0e91a:  cmp r0, r5                        
  0e91c:  bge #0xe922                       
  0e91e:  ldr r0, [pc, #0x138]              -> RAM
  0e920:  str r5, [r0, #0x2c]               
  0e922:  movw r0, #0xf3c                   
  0e926:  cmp r5, r0                        
  0e928:  ble #0xe968                       
  0e92a:  ldr r0, [pc, #0x12c]              -> RAM
  0e92c:  ldr r0, [r0, #0x2c]               
  0e92e:  ldr r1, [pc, #0x12c]              
  0e930:  cmp r0, r1                        
  0e932:  bge #0xe938                       
  0e934:  lsls r4, r1, #0x1d                
  0e936:  b #0xe940                         -> 0x0e940 (вне списка функций)
  0e938:  ldr r0, [pc, #0x11c]              -> RAM
  0e93a:  ldr r0, [r0, #0x2c]               
  0e93c:  subw r4, r0, #0xf3c               
  0e940:  subw r0, r5, #0xf3c               
  0e944:  movw r1, #0x123                   
  0e948:  bl #0x17094                       -> func_0x17094
  0e94c:  mov r1, r4                        
  0e94e:  str r0, [sp]                      
  0e950:  bl #0x16328                       -> func_0x16328
  0e954:  mov r4, r0                        
  0e956:  ldr r0, [pc, #0x104]              
  0e958:  mvns r0, r0                       
  0e95a:  cmp r4, r0                        
  0e95c:  ble #0xe964                       
  0e95e:  mvn r5, #0x80000000               
  0e962:  b #0xe968                         -> 0x0e968 (вне списка функций)
  0e964:  addw r5, r4, #0xf3c               
  0e968:  bl #0x16570                       -> 0x16570 (вне списка функций)
  0e96c:  movw r1, #0x267a                  
  0e970:  cmp r0, r1                        
  0e972:  bge #0xe99a                       
  0e974:  movw r0, #0x1059                  
  0e978:  cmp r5, r0                        
  0e97a:  ble #0xe984                       
  0e97c:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0e980:  cmp r0, #0x64                     
  0e982:  ble #0xe994                       
  0e984:  movw r0, #0x104a                  
  0e988:  cmp r5, r0                        
  0e98a:  ble #0xe99a                       
  0e98c:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0e990:  cmp r0, #0x3c                     
  0e992:  bgt #0xe99a                       
  0e994:  movs r0, #0x64                    
  0e996:  strb r0, [r7]                     
  0e998:  b #0xea54                         -> 0x0ea54 (вне списка функций)
  0e99a:  movw r0, #0xf92                   
  0e99e:  cmp r5, r0                        
  0e9a0:  ble #0xea50                       
  0e9a2:  movs r3, #0xa                     
  0e9a4:  ldr r2, [pc, #0xb8]               -> flash-mirror @0x1a49a
  0e9a6:  subw r1, r2, #0x5d6               
  0e9aa:  mov r0, r5                        
  0e9ac:  bl #0x169f0                       -> func_0x169f0
  0e9b0:  mov r6, r0                        
  0e9b2:  cmp.w r6, #0x8000                 
  0e9b6:  blt #0xe9bc                       
  0e9b8:  movw r6, #0x7fff                  
  0e9bc:  bl #0x16570                       -> 0x16570 (вне списка функций)
  0e9c0:  subs r4, r6, r0                   
  0e9c2:  cmp.w r4, #0x8000                 
  0e9c6:  blt #0xe9cc                       
  0e9c8:  movw r4, #0x7fff                  
  0e9cc:  movs r3, #2                       
  0e9ce:  ldr r2, [pc, #0x90]               -> flash-mirror @0x1a49a
  0e9d0:  adds r2, #0x52                    
  0e9d2:  subw r1, r2, #0x4c6               
  0e9d6:  sxth r0, r4                       
  0e9d8:  bl #0x167b6                       -> func_0x167b6
  0e9dc:  mov r8, r0                        
  0e9de:  cmp.w r8, #0xa                    
  0e9e2:  bgt #0xe9ea                       
  0e9e4:  strb.w r8, [r7]                   
  0e9e8:  b #0xea54                         -> 0x0ea54 (вне списка функций)
  0e9ea:  ldr r0, [pc, #0x6c]               -> RAM
  0e9ec:  ldrh.w r0, [r0, #0x4e]            
  0e9f0:  movw r1, #0xbb8                   
  0e9f4:  cmp r0, r1                        
  0e9f6:  blt #0xea32                       
  0e9f8:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0e9fc:  movw r1, #0xbb8                   
  0ea00:  cmp r0, r1                        
  0ea02:  ble #0xea08                       
  0ea04:  mov r4, r1                        
  0ea06:  b #0xea1e                         -> 0x0ea1e (вне списка функций)
  0ea08:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ea0c:  cmp.w r0, #0x1f4                  
  0ea10:  bge #0xea18                       
  0ea12:  mov.w r4, #0x1f4                  
  0ea16:  b #0xea1e                         -> 0x0ea1e (вне списка функций)
  0ea18:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ea1c:  mov r4, r0                        
  0ea1e:  sub.w r0, r4, #0x1f4              
  0ea22:  movw r1, #0x271                   
  0ea26:  bl #0x161c6                       -> 0x161c6 (вне списка функций)
  0ea2a:  adds r0, r0, #1                   
  0ea2c:  and sb, r0, #0xff                 
  0ea30:  b #0xea36                         -> 0x0ea36 (вне списка функций)
  0ea32:  mov.w sb, #5                      
  0ea36:  cmp.w sb, #0                      
  0ea3a:  bne #0xea42                       
  0ea3c:  mov.w r0, #-1                     
  0ea40:  b #0xea4a                         -> 0x0ea4a (вне списка функций)
  0ea42:  sub.w r0, r8, #0xa                
  0ea46:  udiv r0, r0, sb                   
  0ea4a:  adds r0, #0xa                     
  0ea4c:  strb r0, [r7]                     
  0ea4e:  b #0xea54                         -> 0x0ea54 (вне списка функций)
  0ea50:  movs r0, #0xa                     
  0ea52:  strb r0, [r7]                     
  0ea54:  pop.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x0ea58 (3 слов) — ВНЕ границ функции ---
  0ea58:  .word 0x200012ba  ; RAM
  0ea5c:  .word 0x80000f3c
  0ea60:  .word 0x0801a49a  ; flash-mirror @0x1a49a
```
