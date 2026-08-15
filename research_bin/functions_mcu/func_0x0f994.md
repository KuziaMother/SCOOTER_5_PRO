# func_0x0f994

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f994) | `0x0000f994` |
| размер кода | 564 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019de4 — flash-mirror @0x19de4 (r1)
- 0x20000080 — RAM (r0)
- 0x20000107 — RAM (r0)
- 0x20000a00 — RAM (r0)
- 0x20000a02 — RAM (r0)
- 0x20000a04 — RAM (r0)
- 0x20000a06 — RAM (r0)
- 0x20000a08 — RAM (r1)
- 0x20000a0a — RAM (r0)
- 0x20000a0c — RAM (r0)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)

## Вызовы (callees)

- 0x0f9e2 (b, вне списка функций)
- 0x0fa34 (b, вне списка функций)
- 0x0fb48 (b, вне списка функций)
- 0x0fb6c (b, вне списка функций)
- 0x0fba8 (b, вне списка функций)
- 0x0fbc6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11998` (bl @0x000119ba)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0f9dc..0x0f9e2` (6 Б); цели из: 0x0f9b0
- `0x0f9e2..0x0fa22` (64 Б); цели из: 0x0f9c4, 0x0f9da
- `0x0fa22..0x0fa2a` (8 Б); цели из: 0x0f9f6
- `0x0fa2a..0x0fa34` (10 Б); цели из: 0x0f99a
- `0x0fa34..0x0fa94` (96 Б); цели из: 0x0fa0a, 0x0fa20, 0x0fa28
- `0x0fa94..0x0fab0` (28 Б); цели из: 0x0fa74
- `0x0fab0..0x0fafa` (74 Б); цели из: 0x0fa6c
- `0x0fafa..0x0fb16` (28 Б); цели из: 0x0fada
- `0x0fb16..0x0fb46` (48 Б); цели из: 0x0fad2
- `0x0fb46..0x0fb48` (2 Б); цели из: 0x0fa48
- `0x0fb48..0x0fb66` (30 Б); цели из: 0x0fb44
- `0x0fb66..0x0fb6c` (6 Б); цели из: 0x0fb1c, 0x0fb24, 0x0fb2c
- `0x0fb6c..0x0fba0` (52 Б); цели из: 0x0fb3e, 0x0fb64
- `0x0fba0..0x0fba8` (8 Б); цели из: 0x0fb78
- `0x0fba8..0x0fbc6` (30 Б); цели из: 0x0fb46
- `0x0fbc6..0x0fbc8` (2 Б); цели из: 0x0fba6, 0x0fbba

## Дизассембляция

```asm
  0f994:  ldr r0, [pc, #0x230]              -> RAM
  0f996:  ldrb r0, [r0]                     
  0f998:  cmp r0, #0                        
  0f99a:  bne #0xfa2a                       
  0f99c:  ldr r0, [pc, #0x22c]              -> RAM
  0f99e:  ldrb r0, [r0, #8]                 
  0f9a0:  and r0, r0, #1                    
  0f9a4:  cbnz r0, #0xf9e2                  
  0f9a6:  ldr r0, [pc, #0x224]              -> RAM
  0f9a8:  ldr r0, [r0, #4]                  
  0f9aa:  ldr r1, [pc, #0x224]              -> flash-mirror @0x19de4
  0f9ac:  ldr r1, [r1]                      
  0f9ae:  cmp r0, r1                        
  0f9b0:  blo #0xf9dc                       
  0f9b2:  ldr r0, [pc, #0x220]              -> RAM
  0f9b4:  ldrh r0, [r0]                     
  0f9b6:  adds r0, r0, #1                   
  0f9b8:  ldr r1, [pc, #0x218]              -> RAM
  0f9ba:  strh r0, [r1]                     
  0f9bc:  ldr r0, [pc, #0x210]              -> flash-mirror @0x19de4
  0f9be:  ldrh r0, [r0, #4]                 
  0f9c0:  ldrh r1, [r1]                     
  0f9c2:  cmp r0, r1                        
  0f9c4:  bgt #0xf9e2                       
  0f9c6:  ldr r0, [pc, #0x204]              -> RAM
  0f9c8:  ldrb r0, [r0, #8]                 
  0f9ca:  bic r0, r0, #1                    
  0f9ce:  adds r0, r0, #1                   
  0f9d0:  ldr r1, [pc, #0x1f8]              -> RAM
  0f9d2:  strb r0, [r1, #8]                 
  0f9d4:  movs r0, #0                       
  0f9d6:  ldr r1, [pc, #0x1fc]              -> RAM
  0f9d8:  strh r0, [r1]                     
  0f9da:  b #0xf9e2                         -> 0x0f9e2 (вне списка функций)
  0f9dc:  movs r0, #0                       
  0f9de:  ldr r1, [pc, #0x1f4]              -> RAM
  0f9e0:  strh r0, [r1]                     
  0f9e2:  ldr r0, [pc, #0x1e8]              -> RAM
  0f9e4:  ldrb r0, [r0, #8]                 
  0f9e6:  ubfx r0, r0, #1, #1               
  0f9ea:  cbnz r0, #0xfa34                  
  0f9ec:  ldr r0, [pc, #0x1dc]              -> RAM
  0f9ee:  ldr r0, [r0, #4]                  
  0f9f0:  ldr r1, [pc, #0x1dc]              -> flash-mirror @0x19de4
  0f9f2:  ldr r1, [r1, #0x30]               
  0f9f4:  cmp r0, r1                        
  0f9f6:  blo #0xfa22                       
  0f9f8:  ldr r0, [pc, #0x1dc]              -> RAM
  0f9fa:  ldrh r0, [r0]                     
  0f9fc:  adds r0, r0, #1                   
  0f9fe:  ldr r1, [pc, #0x1d8]              -> RAM
  0fa00:  strh r0, [r1]                     
  0fa02:  ldr r0, [pc, #0x1cc]              -> flash-mirror @0x19de4
  0fa04:  ldrh r0, [r0, #0x34]              
  0fa06:  ldrh r1, [r1]                     
  0fa08:  cmp r0, r1                        
  0fa0a:  bgt #0xfa34                       
  0fa0c:  ldr r0, [pc, #0x1bc]              -> RAM
  0fa0e:  ldrb r0, [r0, #8]                 
  0fa10:  bic r0, r0, #2                    
  0fa14:  adds r0, r0, #2                   
  0fa16:  ldr r1, [pc, #0x1b4]              -> RAM
  0fa18:  strb r0, [r1, #8]                 
  0fa1a:  movs r0, #0                       
  0fa1c:  ldr r1, [pc, #0x1b8]              -> RAM
  0fa1e:  strh r0, [r1]                     
  0fa20:  b #0xfa34                         -> 0x0fa34 (вне списка функций)
  0fa22:  movs r0, #0                       
  0fa24:  ldr r1, [pc, #0x1b0]              -> RAM
  0fa26:  strh r0, [r1]                     
  0fa28:  b #0xfa34                         -> 0x0fa34 (вне списка функций)
  0fa2a:  movs r0, #0                       
  0fa2c:  ldr r1, [pc, #0x1a4]              -> RAM
  0fa2e:  strh r0, [r1]                     
  0fa30:  ldr r1, [pc, #0x1a4]              -> RAM
  0fa32:  strh r0, [r1]                     
  0fa34:  ldr r0, [pc, #0x194]              -> RAM
  0fa36:  ldrb r0, [r0, #8]                 
  0fa38:  and r0, r0, #1                    
  0fa3c:  cbnz r0, #0xfa4a                  
  0fa3e:  ldr r0, [pc, #0x18c]              -> RAM
  0fa40:  ldrb r0, [r0, #8]                 
  0fa42:  ubfx r0, r0, #1, #1               
  0fa46:  cmp r0, #0                        
  0fa48:  beq #0xfb46                       
  0fa4a:  ldr r0, [pc, #0x180]              -> RAM
  0fa4c:  ldrb r0, [r0, #8]                 
  0fa4e:  and r0, r0, #1                    
  0fa52:  cbz r0, #0xfab0                   
  0fa54:  ldr r0, [pc, #0x184]              -> RAM
  0fa56:  ldrh r0, [r0]                     
  0fa58:  adds r0, r0, #1                   
  0fa5a:  ldr r1, [pc, #0x180]              -> RAM
  0fa5c:  strh r0, [r1]                     
  0fa5e:  ldr r0, [pc, #0x168]              -> RAM
  0fa60:  ldrb r0, [r0]                     
  0fa62:  cbz r0, #0xfab0                   
  0fa64:  ldr r0, [pc, #0x168]              -> flash-mirror @0x19de4
  0fa66:  ldrh r0, [r0, #6]                 
  0fa68:  ldrh r1, [r1]                     
  0fa6a:  cmp r0, r1                        
  0fa6c:  bgt #0xfab0                       
  0fa6e:  ldr r0, [pc, #0x170]              -> RAM
  0fa70:  ldrb r0, [r0]                     
  0fa72:  cmp r0, #3                        
  0fa74:  blt #0xfa94                       
  0fa76:  ldr r0, [pc, #0x16c]              -> RAM
  0fa78:  ldrb r0, [r0, #0xc]               
  0fa7a:  ubfx r0, r0, #3, #1               
  0fa7e:  cbnz r0, #0xfa94                  
  0fa80:  ldr r0, [pc, #0x160]              -> RAM
  0fa82:  ldrb r0, [r0, #0xc]               
  0fa84:  ubfx r0, r0, #4, #1               
  0fa88:  cbnz r0, #0xfa94                  
  0fa8a:  ldr r0, [pc, #0x158]              -> RAM
  0fa8c:  ldrb r0, [r0, #0xc]               
  0fa8e:  ubfx r0, r0, #6, #1               
  0fa92:  cbz r0, #0xfab0                   
  0fa94:  ldr r0, [pc, #0x134]              -> RAM
  0fa96:  ldrb r0, [r0, #8]                 
  0fa98:  bic r0, r0, #1                    
  0fa9c:  ldr r1, [pc, #0x12c]              -> RAM
  0fa9e:  strb r0, [r1, #8]                 
  0faa0:  ldr r0, [pc, #0x13c]              -> RAM
  0faa2:  ldrb r0, [r0]                     
  0faa4:  adds r0, r0, #1                   
  0faa6:  ldr r1, [pc, #0x138]              -> RAM
  0faa8:  strb r0, [r1]                     
  0faaa:  movs r0, #0                       
  0faac:  ldr r1, [pc, #0x12c]              -> RAM
  0faae:  strh r0, [r1]                     
  0fab0:  ldr r0, [pc, #0x118]              -> RAM
  0fab2:  ldrb r0, [r0, #8]                 
  0fab4:  ubfx r0, r0, #1, #1               
  0fab8:  cbz r0, #0xfb16                   
  0faba:  ldr r0, [pc, #0x12c]              -> RAM
  0fabc:  ldrh r0, [r0]                     
  0fabe:  adds r0, r0, #1                   
  0fac0:  ldr r1, [pc, #0x124]              -> RAM
  0fac2:  strh r0, [r1]                     
  0fac4:  ldr r0, [pc, #0x100]              -> RAM
  0fac6:  ldrb r0, [r0]                     
  0fac8:  cbz r0, #0xfb16                   
  0faca:  ldr r0, [pc, #0x104]              -> flash-mirror @0x19de4
  0facc:  ldrh r0, [r0, #0x36]              
  0face:  ldrh r1, [r1]                     
  0fad0:  cmp r0, r1                        
  0fad2:  bgt #0xfb16                       
  0fad4:  ldr r0, [pc, #0x108]              -> RAM
  0fad6:  ldrb r0, [r0]                     
  0fad8:  cmp r0, #3                        
  0fada:  blt #0xfafa                       
  0fadc:  ldr r0, [pc, #0x104]              -> RAM
  0fade:  ldrb r0, [r0, #0xc]               
  0fae0:  ubfx r0, r0, #3, #1               
  0fae4:  cbnz r0, #0xfafa                  
  0fae6:  ldr r0, [pc, #0xfc]               -> RAM
  0fae8:  ldrb r0, [r0, #0xc]               
  0faea:  ubfx r0, r0, #4, #1               
  0faee:  cbnz r0, #0xfafa                  
  0faf0:  ldr r0, [pc, #0xf0]               -> RAM
  0faf2:  ldrb r0, [r0, #0xc]               
  0faf4:  ubfx r0, r0, #6, #1               
  0faf8:  cbz r0, #0xfb16                   
  0fafa:  ldr r0, [pc, #0xd0]               -> RAM
  0fafc:  ldrb r0, [r0, #8]                 
  0fafe:  bic r0, r0, #2                    
  0fb02:  ldr r1, [pc, #0xc8]               -> RAM
  0fb04:  strb r0, [r1, #8]                 
  0fb06:  ldr r0, [pc, #0xd8]               -> RAM
  0fb08:  ldrb r0, [r0]                     
  0fb0a:  adds r0, r0, #1                   
  0fb0c:  ldr r1, [pc, #0xd0]               -> RAM
  0fb0e:  strb r0, [r1]                     
  0fb10:  movs r0, #0                       
  0fb12:  ldr r1, [pc, #0xd4]               -> RAM
  0fb14:  strh r0, [r1]                     
  0fb16:  ldr r0, [pc, #0xb0]               -> RAM
  0fb18:  ldrb r0, [r0]                     
  0fb1a:  cmp r0, #1                        
  0fb1c:  bne #0xfb66                       
  0fb1e:  ldr r0, [pc, #0xac]               -> RAM
  0fb20:  ldr r0, [r0, #4]                  
  0fb22:  cmp r0, #0x64                     
  0fb24:  blo #0xfb66                       
  0fb26:  ldr r0, [pc, #0xb8]               -> RAM
  0fb28:  ldrb r0, [r0]                     
  0fb2a:  cmp r0, #3                        
  0fb2c:  blt #0xfb66                       
  0fb2e:  ldr r0, [pc, #0xbc]               -> RAM
  0fb30:  ldrh r0, [r0]                     
  0fb32:  adds r0, r0, #1                   
  0fb34:  ldr r1, [pc, #0xb4]               -> RAM
  0fb36:  strh r0, [r1]                     
  0fb38:  mov r0, r1                        
  0fb3a:  ldrh r0, [r0]                     
  0fb3c:  cmp r0, #0x1e                     
  0fb3e:  blt #0xfb6c                       
  0fb40:  ldr r0, [pc, #0x88]               -> RAM
  0fb42:  ldrb r0, [r0, #8]                 
  0fb44:  b #0xfb48                         -> 0x0fb48 (вне списка функций)
  0fb46:  b #0xfba8                         -> 0x0fba8 (вне списка функций)
  0fb48:  bic r0, r0, #1                    
  0fb4c:  ldr r1, [pc, #0x7c]               -> RAM
  0fb4e:  strb r0, [r1, #8]                 
  0fb50:  mov r0, r1                        
  0fb52:  ldrb r0, [r0, #8]                 
  0fb54:  bic r0, r0, #2                    
  0fb58:  strb r0, [r1, #8]                 
  0fb5a:  movs r0, #0                       
  0fb5c:  ldr r1, [pc, #0x80]               -> RAM
  0fb5e:  strb r0, [r1]                     
  0fb60:  ldr r1, [pc, #0x88]               -> RAM
  0fb62:  strh r0, [r1]                     
  0fb64:  b #0xfb6c                         -> 0x0fb6c (вне списка функций)
  0fb66:  movs r0, #0                       
  0fb68:  ldr r1, [pc, #0x80]               -> RAM
  0fb6a:  strh r0, [r1]                     
  0fb6c:  ldr r0, [pc, #0x80]               -> RAM
  0fb6e:  ldrb r0, [r0]                     
  0fb70:  cbnz r0, #0xfba0                  
  0fb72:  ldr r0, [pc, #0x6c]               -> RAM
  0fb74:  ldrb r0, [r0]                     
  0fb76:  cmp r0, #3                        
  0fb78:  blt #0xfba0                       
  0fb7a:  movs r0, #0                       
  0fb7c:  ldr r1, [pc, #0x5c]               -> RAM
  0fb7e:  strh r0, [r1]                     
  0fb80:  ldr r1, [pc, #0x64]               -> RAM
  0fb82:  strh r0, [r1]                     
  0fb84:  ldr r0, [pc, #0x44]               -> RAM
  0fb86:  ldrb r0, [r0, #8]                 
  0fb88:  bic r0, r0, #1                    
  0fb8c:  ldr r1, [pc, #0x3c]               -> RAM
  0fb8e:  strb r0, [r1, #8]                 
  0fb90:  mov r0, r1                        
  0fb92:  ldrb r0, [r0, #8]                 
  0fb94:  bic r0, r0, #2                    
  0fb98:  strb r0, [r1, #8]                 
  0fb9a:  movs r0, #0                       
  0fb9c:  ldr r1, [pc, #0x40]               -> RAM
  0fb9e:  strb r0, [r1]                     
  0fba0:  movs r0, #0                       
  0fba2:  ldr r1, [pc, #0x50]               -> RAM
  0fba4:  strh r0, [r1]                     
  0fba6:  b #0xfbc6                         -> 0x0fbc6 (вне списка функций)
  0fba8:  ldr r0, [pc, #0x48]               -> RAM
  0fbaa:  ldrh r0, [r0]                     
  0fbac:  adds r0, r0, #1                   
  0fbae:  ldr r1, [pc, #0x44]               -> RAM
  0fbb0:  strh r0, [r1]                     
  0fbb2:  mov r0, r1                        
  0fbb4:  ldrh r0, [r0]                     
  0fbb6:  cmp.w r0, #0x2bc                  
  0fbba:  blt #0xfbc6                       
  0fbbc:  movs r0, #0                       
  0fbbe:  ldr r1, [pc, #0x20]               -> RAM
  0fbc0:  strb r0, [r1]                     
  0fbc2:  ldr r1, [pc, #0x30]               -> RAM
  0fbc4:  strh r0, [r1]                     
  0fbc6:  bx lr                             
  ; --- literal-пул @0x0fbc8 (12 слов) — ВНЕ границ функции ---
  0fbc8:  .word 0x20000080  ; RAM
  0fbcc:  .word 0x20000fbb  ; RAM
  0fbd0:  .word 0x08019de4  ; flash-mirror @0x19de4
  0fbd4:  .word 0x20000a00  ; RAM
  0fbd8:  .word 0x20000a02  ; RAM
  0fbdc:  .word 0x20000a06  ; RAM
  0fbe0:  .word 0x20000a0c  ; RAM
  0fbe4:  .word 0x20000f95  ; RAM
  0fbe8:  .word 0x20000a04  ; RAM
  0fbec:  .word 0x20000a0a  ; RAM
  0fbf0:  .word 0x20000107  ; RAM
  0fbf4:  .word 0x20000a08  ; RAM
```
