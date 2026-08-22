# func_0x07a30

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007a30) | `0x00007a30` |
| размер кода | 820 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000128b — RAM (r1)
- 0x200012ba — RAM (r0)

## Вызовы (callees)

- 0x07a60 (b, вне списка функций)
- 0x07a6a (b, вне списка функций)
- 0x07b9a (b, вне списка функций)
- 0x07c84 (b, вне списка функций)
- 0x07cd2 (b, вне списка функций)
- 0x07d20 (b, вне списка функций)
- 0x07d42 (b, вне списка функций)
- 0x08d9c (bl, вне списка функций)
- `func_0x08e14` (0x00008e14, bl)
- 0x08e20 (bl, вне списка функций)
- `func_0x0e408` (0x0000e408, bl)
- `func_0x0e704` (0x0000e704, bl)
- 0x10ed0 (bl, вне списка функций)
- 0x10f18 (bl, вне списка функций)
- 0x1101c (bl, вне списка функций)
- 0x16510 (bl, вне списка функций)
- 0x16528 (bl, вне списка функций)
- 0x1654c (bl, вне списка функций)
- 0x16570 (bl, вне списка функций)
- 0x1657c (bl, вне списка функций)
- 0x004d2aae (bl, вне образа — runtime/внешний)

## Кто вызывает (callers / xrefs)

- `func_0x0e658` (bl @0x0000e6ac)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x07a5e..0x07a60` (2 Б); цели из: 0x07a58
- `0x07a60..0x07a68` (8 Б); цели из: 0x07a5c
- `0x07a68..0x07a6a` (2 Б); цели из: 0x07a62
- `0x07a6a..0x07aca` (96 Б); цели из: 0x07a66
- `0x07aca..0x07aee` (36 Б); цели из: 0x07ab0
- `0x07aee..0x07b0a` (28 Б); цели из: 0x07ae0
- `0x07b0a..0x07b18` (14 Б); цели из: 0x07aec
- `0x07b18..0x07b2c` (20 Б); цели из: 0x07b14
- `0x07b2c..0x07b36` (10 Б); цели из: 0x07b26
- `0x07b36..0x07b3a` (4 Б); цели из: 0x07afc, 0x07b08
- `0x07b3a..0x07b5c` (34 Б); цели из: 0x07ad0
- `0x07b5c..0x07b9a` (62 Б); цели из: 0x07b40
- `0x07b9a..0x07b9c` (2 Б); цели из: 0x07ac8, 0x07b2a, 0x07b34, 0x07b38…
- `0x07b9c..0x07c84` (232 Б); цели из: 0x07a9e
- `0x07c84..0x07cd2` (78 Б); цели из: 0x07c82
- `0x07cd2..0x07d20` (78 Б); цели из: 0x07b9c
- `0x07d20..0x07d42` (34 Б); цели из: 0x07b9a, 0x07bea, 0x07c38, 0x07c80…
- `0x07d42..0x07d64` (34 Б); цели из: 0x07a92

## Дизассембляция

```asm
  07a30:  push.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  07a34:  movs r7, #0                       
  07a36:  movs r0, #1                       
  07a38:  bl #0x1101c                       -> 0x1101c (вне списка функций)
  07a3c:  ldr r0, [pc, #0x324]              -> RAM
  07a3e:  ldrb.w r0, [r0, #0x53]            
  07a42:  cbz r0, #0x7a4c                   
  07a44:  bl #0x16528                       -> 0x16528 (вне списка функций)
  07a48:  ldr r1, [pc, #0x318]              -> RAM
  07a4a:  str r0, [r1]                      
  07a4c:  bl #0x16528                       -> 0x16528 (вне списка функций)
  07a50:  ldr r1, [pc, #0x310]              -> RAM
  07a52:  ldr r1, [r1]                      
  07a54:  subs r4, r0, r1                   
  07a56:  cmp r4, #0                        
  07a58:  bge #0x7a5e                       
  07a5a:  rsbs r6, r4, #0                   
  07a5c:  b #0x7a60                         -> 0x07a60 (вне списка функций)
  07a5e:  mov r6, r4                        
  07a60:  cmp r6, #0x32                     
  07a62:  blt #0x7a68                       
  07a64:  movs r5, #0                       
  07a66:  b #0x7a6a                         -> 0x07a6a (вне списка функций)
  07a68:  sxth r5, r4                       
  07a6a:  ldr r0, [pc, #0x2f8]              -> RAM
  07a6c:  ldrb.w r0, [r0, #0x54]            
  07a70:  cbnz r0, #0x7a94                  
  07a72:  movs r0, #1                       
  07a74:  ldr r1, [pc, #0x2ec]              -> RAM
  07a76:  strb.w r0, [r1, #0x54]            
  07a7a:  movs r0, #4                       
  07a7c:  strb.w r0, [r1, #0x55]            
  07a80:  bl #0x1657c                       -> 0x1657c (вне списка функций)
  07a84:  mov r8, r0                        
  07a86:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07a8a:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07a8e:  ldr r1, [pc, #0x2d8]              -> RAM
  07a90:  strh r0, [r1, #0x1c]              
  07a92:  b #0x7d42                         -> 0x07d42 (вне списка функций)
  07a94:  movs r7, #0                       
  07a96:  ldr r0, [pc, #0x2cc]              -> RAM
  07a98:  ldrb.w r0, [r0, #0x55]            
  07a9c:  cmp r0, #6                        
  07a9e:  bhs #0x7b9c                       
  07aa0:  tbb [pc, r0]                      
  07aa4:  lsls r4, r7, #0xd                 
  07aa6:  adr r4, #0x1f4                    
  07aa8:  bl #0x4d2aae                      
  07aac:  ldrsh.w r2, [sb, #0x801]          
  07ab0:  bne #0x7aca                       
  07ab2:  movs r0, #3                       
  07ab4:  ldr r1, [pc, #0x2ac]              -> RAM
  07ab6:  strb.w r0, [r1, #0x55]            
  07aba:  movs r0, #0                       
  07abc:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07ac0:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07ac4:  ldr r1, [pc, #0x2a0]              -> RAM
  07ac6:  strh r0, [r1, #0x1c]              
  07ac8:  b #0x7b9a                         -> 0x07b9a (вне списка функций)
  07aca:  bl #0x16510                       -> 0x16510 (вне списка функций)
  07ace:  cmp r0, #1                        
  07ad0:  bne #0x7b3a                       
  07ad2:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07ad6:  ldr r1, [pc, #0x290]              -> RAM
  07ad8:  ldrh r1, [r1, #0x28]              
  07ada:  add.w r1, r1, #0x1f4              
  07ade:  cmp r0, r1                        
  07ae0:  bgt #0x7aee                       
  07ae2:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07ae6:  ldr r1, [pc, #0x280]              -> RAM
  07ae8:  ldrh r1, [r1, #0x28]              
  07aea:  cmp r0, r1                        
  07aec:  bgt #0x7b0a                       
  07aee:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07af2:  add.w r0, r0, #0x3e8              
  07af6:  ldr r1, [pc, #0x270]              -> RAM
  07af8:  ldrh r1, [r1, #0x28]              
  07afa:  cmp r0, r1                        
  07afc:  blt #0x7b36                       
  07afe:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07b02:  ldr r1, [pc, #0x264]              -> RAM
  07b04:  ldrh r1, [r1, #0x28]              
  07b06:  cmp r0, r1                        
  07b08:  bge #0x7b36                       
  07b0a:  ldr r0, [pc, #0x258]              -> RAM
  07b0c:  ldrb.w r0, [r0, #0x56]            
  07b10:  adds r4, r0, #1                   
  07b12:  cmp r4, #0xff                     
  07b14:  ble #0x7b18                       
  07b16:  movs r4, #0xff                    
  07b18:  ldr r1, [pc, #0x248]              -> RAM
  07b1a:  strb.w r4, [r1, #0x56]            
  07b1e:  mov r0, r1                        
  07b20:  ldrb.w r0, [r0, #0x56]            
  07b24:  cmp r0, #0x78                     
  07b26:  blt #0x7b2c                       
  07b28:  movs r7, #1                       
  07b2a:  b #0x7b9a                         -> 0x07b9a (вне списка функций)
  07b2c:  movs r0, #6                       
  07b2e:  ldr r1, [pc, #0x234]              -> RAM
  07b30:  strb.w r0, [r1, #0x55]            
  07b34:  b #0x7b9a                         -> 0x07b9a (вне списка функций)
  07b36:  movs r7, #1                       
  07b38:  b #0x7b9a                         -> 0x07b9a (вне списка функций)
  07b3a:  bl #0x8e14                        -> func_0x08e14
  07b3e:  cmp r0, #1                        
  07b40:  bne #0x7b5c                       
  07b42:  movs r0, #2                       
  07b44:  ldr r1, [pc, #0x21c]              -> RAM
  07b46:  strb.w r0, [r1, #0x55]            
  07b4a:  movw r0, #0x2710                  
  07b4e:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07b52:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07b56:  ldr r1, [pc, #0x210]              -> RAM
  07b58:  strh r0, [r1, #0x1c]              
  07b5a:  b #0x7b9a                         -> 0x07b9a (вне списка функций)
  07b5c:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  07b60:  mov r8, r0                        
  07b62:  bl #0x16570                       -> 0x16570 (вне списка функций)
  07b66:  mov sb, r0                        
  07b68:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07b6c:  mov sl, r0                        
  07b6e:  ldr r0, [pc, #0x1f4]              -> RAM
  07b70:  adds r0, #0x71                    
  07b72:  ldr r1, [pc, #0x1f4]              -> RAM
  07b74:  adds r1, #0x1c                    
  07b76:  ldr r2, [pc, #0x1f0]              -> RAM
  07b78:  ldrb.w r2, [r2, #0x2d]            
  07b7c:  mov r3, r8                        
  07b7e:  strd r2, r1, [sp]                 
  07b82:  str r0, [sp, #8]                  
  07b84:  mov r2, r5                        
  07b86:  mov r1, sb                        
  07b88:  mov r0, sl                        
  07b8a:  bl #0xe408                        -> func_0x0e408
  07b8e:  ldr r1, [pc, #0x1d8]              -> RAM
  07b90:  ldrh r0, [r1, #0x1c]              
  07b92:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07b96:  bl #0xe704                        -> func_0x0e704
  07b9a:  b #0x7d20                         -> 0x07d20 (вне списка функций)
  07b9c:  b #0x7cd2                         -> 0x07cd2 (вне списка функций)
  07b9e:  bl #0x8e14                        -> func_0x08e14
  07ba2:  cbnz r0, #0x7bea                  
  07ba4:  movs r0, #1                       
  07ba6:  ldr r1, [pc, #0x1bc]              -> RAM
  07ba8:  strb.w r0, [r1, #0x55]            
  07bac:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  07bb0:  mov r8, r0                        
  07bb2:  bl #0x16570                       -> 0x16570 (вне списка функций)
  07bb6:  mov sb, r0                        
  07bb8:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07bbc:  mov sl, r0                        
  07bbe:  ldr r1, [pc, #0x1a4]              -> RAM
  07bc0:  adds r1, #0x71                    
  07bc2:  ldr r0, [pc, #0x1a4]              -> RAM
  07bc4:  adds r0, #0x1c                    
  07bc6:  ldr r2, [pc, #0x1a0]              -> RAM
  07bc8:  ldrb.w r2, [r2, #0x2d]            
  07bcc:  mov r3, r8                        
  07bce:  strd r2, r0, [sp]                 
  07bd2:  str r1, [sp, #8]                  
  07bd4:  mov r2, r5                        
  07bd6:  mov r1, sb                        
  07bd8:  mov r0, sl                        
  07bda:  bl #0xe408                        -> func_0x0e408
  07bde:  ldr r1, [pc, #0x188]              -> RAM
  07be0:  ldrh r0, [r1, #0x1c]              
  07be2:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07be6:  bl #0xe704                        -> func_0x0e704
  07bea:  b #0x7d20                         -> 0x07d20 (вне списка функций)
  07bec:  bl #0x8e20                        -> 0x08e20 (вне списка функций)
  07bf0:  cbnz r0, #0x7c38                  
  07bf2:  movs r0, #1                       
  07bf4:  ldr r1, [pc, #0x16c]              -> RAM
  07bf6:  strb.w r0, [r1, #0x55]            
  07bfa:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  07bfe:  mov r8, r0                        
  07c00:  bl #0x16570                       -> 0x16570 (вне списка функций)
  07c04:  mov sb, r0                        
  07c06:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07c0a:  mov sl, r0                        
  07c0c:  ldr r1, [pc, #0x154]              -> RAM
  07c0e:  adds r1, #0x71                    
  07c10:  ldr r0, [pc, #0x154]              -> RAM
  07c12:  adds r0, #0x1c                    
  07c14:  ldr r2, [pc, #0x150]              -> RAM
  07c16:  ldrb.w r2, [r2, #0x2d]            
  07c1a:  mov r3, r8                        
  07c1c:  strd r2, r0, [sp]                 
  07c20:  str r1, [sp, #8]                  
  07c22:  mov r2, r5                        
  07c24:  mov r1, sb                        
  07c26:  mov r0, sl                        
  07c28:  bl #0xe408                        -> func_0x0e408
  07c2c:  ldr r1, [pc, #0x138]              -> RAM
  07c2e:  ldrh r0, [r1, #0x1c]              
  07c30:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07c34:  bl #0xe704                        -> func_0x0e704
  07c38:  b #0x7d20                         -> 0x07d20 (вне списка функций)
  07c3a:  movs r0, #1                       
  07c3c:  ldr r1, [pc, #0x124]              -> RAM
  07c3e:  strb.w r0, [r1, #0x55]            
  07c42:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  07c46:  mov r8, r0                        
  07c48:  bl #0x16570                       -> 0x16570 (вне списка функций)
  07c4c:  mov sb, r0                        
  07c4e:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07c52:  mov sl, r0                        
  07c54:  ldr r0, [pc, #0x10c]              -> RAM
  07c56:  adds r0, #0x71                    
  07c58:  ldr r1, [pc, #0x10c]              -> RAM
  07c5a:  adds r1, #0x1c                    
  07c5c:  ldr r2, [pc, #0x108]              -> RAM
  07c5e:  ldrb.w r2, [r2, #0x2d]            
  07c62:  mov r3, r8                        
  07c64:  strd r2, r1, [sp]                 
  07c68:  str r0, [sp, #8]                  
  07c6a:  mov r2, r5                        
  07c6c:  mov r1, sb                        
  07c6e:  mov r0, sl                        
  07c70:  bl #0xe408                        -> func_0x0e408
  07c74:  ldr r1, [pc, #0xf0]               -> RAM
  07c76:  ldrh r0, [r1, #0x1c]              
  07c78:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07c7c:  bl #0xe704                        -> func_0x0e704
  07c80:  b #0x7d20                         -> 0x07d20 (вне списка функций)
  07c82:  b #0x7c84                         -> 0x07c84 (вне списка функций)
  07c84:  bl #0x16510                       -> 0x16510 (вне списка функций)
  07c88:  cbnz r0, #0x7cd0                  
  07c8a:  movs r0, #1                       
  07c8c:  ldr r1, [pc, #0xd4]               -> RAM
  07c8e:  strb.w r0, [r1, #0x55]            
  07c92:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  07c96:  mov r8, r0                        
  07c98:  bl #0x16570                       -> 0x16570 (вне списка функций)
  07c9c:  mov sb, r0                        
  07c9e:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07ca2:  mov sl, r0                        
  07ca4:  ldr r0, [pc, #0xbc]               -> RAM
  07ca6:  adds r0, #0x71                    
  07ca8:  ldr r1, [pc, #0xbc]               -> RAM
  07caa:  adds r1, #0x1c                    
  07cac:  ldr r2, [pc, #0xb8]               -> RAM
  07cae:  ldrb.w r2, [r2, #0x2d]            
  07cb2:  mov r3, r8                        
  07cb4:  strd r2, r1, [sp]                 
  07cb8:  str r0, [sp, #8]                  
  07cba:  mov r2, r5                        
  07cbc:  mov r1, sb                        
  07cbe:  mov r0, sl                        
  07cc0:  bl #0xe408                        -> func_0x0e408
  07cc4:  ldr r1, [pc, #0xa0]               -> RAM
  07cc6:  ldrh r0, [r1, #0x1c]              
  07cc8:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07ccc:  bl #0xe704                        -> func_0x0e704
  07cd0:  b #0x7d20                         -> 0x07d20 (вне списка функций)
  07cd2:  bl #0x16510                       -> 0x16510 (вне списка функций)
  07cd6:  cbnz r0, #0x7d1e                  
  07cd8:  movs r0, #1                       
  07cda:  ldr r1, [pc, #0x88]               -> RAM
  07cdc:  strb.w r0, [r1, #0x55]            
  07ce0:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  07ce4:  mov r8, r0                        
  07ce6:  bl #0x16570                       -> 0x16570 (вне списка функций)
  07cea:  mov sb, r0                        
  07cec:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07cf0:  mov sl, r0                        
  07cf2:  ldr r0, [pc, #0x70]               -> RAM
  07cf4:  adds r0, #0x71                    
  07cf6:  ldr r1, [pc, #0x70]               -> RAM
  07cf8:  adds r1, #0x1c                    
  07cfa:  ldr r2, [pc, #0x6c]               -> RAM
  07cfc:  ldrb.w r2, [r2, #0x2d]            
  07d00:  mov r3, r8                        
  07d02:  strd r2, r1, [sp]                 
  07d06:  str r0, [sp, #8]                  
  07d08:  mov r2, r5                        
  07d0a:  mov r1, sb                        
  07d0c:  mov r0, sl                        
  07d0e:  bl #0xe408                        -> func_0x0e408
  07d12:  ldr r1, [pc, #0x54]               -> RAM
  07d14:  ldrh r0, [r1, #0x1c]              
  07d16:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07d1a:  bl #0xe704                        -> func_0x0e704
  07d1e:  nop                               
  07d20:  nop                               
  07d22:  cbz r7, #0x7d42                   
  07d24:  movs r0, #5                       
  07d26:  ldr r1, [pc, #0x3c]               -> RAM
  07d28:  strb.w r0, [r1, #0x55]            
  07d2c:  movs r0, #0                       
  07d2e:  strb.w r0, [r1, #0x56]            
  07d32:  ldr r1, [pc, #0x34]               -> RAM
  07d34:  ldrh r0, [r1, #0x28]              
  07d36:  bl #0x10f18                       -> 0x10f18 (вне списка функций)
  07d3a:  bl #0x8d9c                        -> 0x08d9c (вне списка функций)
  07d3e:  ldr r1, [pc, #0x28]               -> RAM
  07d40:  strh r0, [r1, #0x1c]              
  07d42:  movs r0, #0                       
  07d44:  ldr r1, [pc, #0x1c]               -> RAM
  07d46:  strb.w r0, [r1, #0x53]            
  07d4a:  bl #0x16528                       -> 0x16528 (вне списка функций)
  07d4e:  ldr r1, [pc, #0x14]               -> RAM
  07d50:  str r0, [r1]                      
  07d52:  movs r0, #0                       
  07d54:  bl #0x1101c                       -> 0x1101c (вне списка функций)
  07d58:  ldr r1, [pc, #0xc]                -> RAM
  07d5a:  ldrh r0, [r1, #0x1c]              
  07d5c:  bl #0x10ed0                       -> 0x10ed0 (вне списка функций)
  07d60:  pop.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x07d64 (2 слов) — ВНЕ границ функции ---
  07d64:  .word 0x200012ba  ; RAM
  07d68:  .word 0x2000128b  ; RAM
```
