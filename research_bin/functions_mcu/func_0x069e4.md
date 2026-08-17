# func_0x069e4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800069e4) | `0x000069e4` |
| размер кода | 722 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019f60 — flash-mirror @0x19f60 (r0)
- 0x2000128b — RAM (r1)
- 0x200012ba — RAM (r0)
- 0x7ffff37f — прочее (r0)
- 0xfffff9f2 — прочее (r1)

## Вызовы (callees)

- 0x06a18 (b, вне списка функций)
- 0x06a60 (b, вне списка функций)
- 0x06a72 (b, вне списка функций)
- 0x06a76 (b, вне списка функций)
- 0x06a8c (b, вне списка функций)
- 0x06b54 (b, вне списка функций)
- 0x06b56 (b, вне списка функций)
- 0x06b88 (b, вне списка функций)
- 0x06c50 (b, вне списка функций)
- 0x06c52 (b, вне списка функций)
- 0x06c54 (b, вне списка функций)
- 0x06c88 (b, вне списка функций)
- 0x06ca2 (b, вне списка функций)
- 0x08ecc (bl, вне списка функций)
- 0x08ee8 (bl, вне списка функций)
- `func_0x08f58` (0x00008f58, bl)
- `func_0x0e2cc` (0x0000e2cc, bl)
- `func_0x0e2fc` (0x0000e2fc, bl)
- `func_0x0e808` (0x0000e808, bl)
- 0x10fd4 (bl, вне списка функций)
- 0x11028 (bl, вне списка функций)
- `func_0x16328` (0x00016328, bl)
- 0x1654c (bl, вне списка функций)
- 0x16570 (bl, вне списка функций)
- `func_0x16bd4` (0x00016bd4, bl)
- `func_0x16f42` (0x00016f42, bl)
- `func_0x17094` (0x00017094, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0e658` (bl @0x0000e6b2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x06a0c..0x06a18` (12 Б); цели из: 0x069fc
- `0x06a18..0x06a2a` (18 Б); цели из: 0x06a0a
- `0x06a2a..0x06a36` (12 Б); цели из: 0x06a20
- `0x06a36..0x06a5c` (38 Б); цели из: 0x06a2e
- `0x06a5c..0x06a60` (4 Б); цели из: 0x06a54
- `0x06a60..0x06a68` (8 Б); цели из: 0x06a5a
- `0x06a68..0x06a72` (10 Б); цели из: 0x06a62
- `0x06a72..0x06a76` (4 Б); цели из: 0x06a66, 0x06a6c
- `0x06a76..0x06a86` (16 Б); цели из: 0x06a28, 0x06a34
- `0x06a86..0x06a8c` (6 Б); цели из: 0x06a7c
- `0x06a8c..0x06ae6` (90 Б); цели из: 0x06a84
- `0x06ae6..0x06b0a` (36 Б); цели из: 0x06ade
- `0x06b0a..0x06b20` (22 Б); цели из: 0x06aec, 0x06af4
- `0x06b20..0x06b54` (52 Б); цели из: 0x06afe, 0x06b08
- `0x06b54..0x06b56` (2 Б); цели из: 0x06b1e
- `0x06b56..0x06b6a` (20 Б); цели из: 0x06ae4
- `0x06b6a..0x06b80` (22 Б); цели из: 0x06b60
- `0x06b80..0x06b88` (8 Б); цели из: 0x06b68
- `0x06b88..0x06b8a` (2 Б); цели из: 0x06b7e
- `0x06b8a..0x06bb0` (38 Б); цели из: 0x06ae2
- `0x06bb0..0x06bee` (62 Б); цели из: 0x06ba2
- `0x06bee..0x06c04` (22 Б); цели из: 0x06bae
- `0x06c04..0x06c44` (64 Б); цели из: 0x06b90, 0x06b98
- `0x06c44..0x06c50` (12 Б); цели из: 0x06c0c, 0x06c14
- `0x06c50..0x06c52` (2 Б); цели из: 0x06bec, 0x06c02, 0x06c42
- `0x06c52..0x06c54` (2 Б); цели из: 0x06b54, 0x06b88
- `0x06c54..0x06c60` (12 Б); цели из: 0x06ad4
- `0x06c60..0x06c88` (40 Б); цели из: 0x06c5a
- `0x06c88..0x06c98` (16 Б); цели из: 0x06c5e
- `0x06c98..0x06ca2` (10 Б); цели из: 0x06c8e
- `0x06ca2..0x06cb6` (20 Б); цели из: 0x06c96

## Дизассембляция

```asm
  069e4:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  069e8:  sub sp, #0x14                     
  069ea:  movs r0, #1                       
  069ec:  bl #0x10fd4                       -> 0x10fd4 (вне списка функций)
  069f0:  bl #0x8ecc                        -> 0x08ecc (вне списка функций)
  069f4:  mov sb, r0                        
  069f6:  bl #0x8ee8                        -> 0x08ee8 (вне списка функций)
  069fa:  cmp sb, r0                        
  069fc:  blt #0x6a0c                       
  069fe:  bl #0x8ecc                        -> 0x08ecc (вне списка функций)
  06a02:  mov r4, r0                        
  06a04:  bl #0x8ee8                        -> 0x08ee8 (вне списка функций)
  06a08:  mov r5, r0                        
  06a0a:  b #0x6a18                         -> 0x06a18 (вне списка функций)
  06a0c:  bl #0x8ee8                        -> 0x08ee8 (вне списка функций)
  06a10:  mov r4, r0                        
  06a12:  bl #0x8ecc                        -> 0x08ecc (вне списка функций)
  06a16:  mov r5, r0                        
  06a18:  mov.w r8, #0x3e8                  
  06a1c:  subs r0, r4, r5                   
  06a1e:  cmp r0, r8                        
  06a20:  blt #0x6a2a                       
  06a22:  mov.w r0, #0xc80                  
  06a26:  str r0, [sp, #0xc]                
  06a28:  b #0x6a76                         -> 0x06a76 (вне списка функций)
  06a2a:  cmp.w r5, #0xc80                  
  06a2e:  bge #0x6a36                       
  06a30:  uxth r0, r5                       
  06a32:  str r0, [sp, #0xc]                
  06a34:  b #0x6a76                         -> 0x06a76 (вне списка функций)
  06a36:  sub.w r1, r5, #0xc80              
  06a3a:  mov r0, r8                        
  06a3c:  bl #0x17094                       -> func_0x17094
  06a40:  mov sb, r0                        
  06a42:  sub.w r0, r8, r4                  
  06a46:  adds r1, r0, r5                   
  06a48:  mov r0, sb                        
  06a4a:  bl #0x16328                       -> func_0x16328
  06a4e:  mov r4, r0                        
  06a50:  ldr r0, [pc, #0x264]              
  06a52:  cmp r4, r0                        
  06a54:  ble #0x6a5c                       
  06a56:  mvn r4, #0x80000000               
  06a5a:  b #0x6a60                         -> 0x06a60 (вне списка функций)
  06a5c:  add.w r4, r4, #0xc80              
  06a60:  cmp r4, #0                        
  06a62:  bge #0x6a68                       
  06a64:  movs r4, #0                       
  06a66:  b #0x6a72                         -> 0x06a72 (вне списка функций)
  06a68:  cmp.w r4, #0x10000                
  06a6c:  blt #0x6a72                       
  06a6e:  movw r4, #0xffff                  
  06a72:  uxth r0, r4                       
  06a74:  str r0, [sp, #0xc]                
  06a76:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06a7a:  cmp r0, #0                        
  06a7c:  bge #0x6a86                       
  06a7e:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06a82:  rsbs r4, r0, #0                   
  06a84:  b #0x6a8c                         -> 0x06a8c (вне списка функций)
  06a86:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06a8a:  mov r4, r0                        
  06a8c:  bl #0x8f58                        -> func_0x08f58
  06a90:  mov sb, r0                        
  06a92:  movs r2, #5                       
  06a94:  ldr r0, [pc, #0x224]              -> flash-mirror @0x19f60
  06a96:  add.w r1, r0, #0x550              
  06a9a:  sub.w r3, r0, #0xac               
  06a9e:  strd r0, r2, [sp, #4]             
  06aa2:  str r1, [sp]                      
  06aa4:  add.w r2, r0, #0xbc               
  06aa8:  mov r1, r4                        
  06aaa:  mov r0, sb                        
  06aac:  bl #0x16bd4                       -> func_0x16bd4
  06ab0:  mov r7, r0                        
  06ab2:  ldr r0, [pc, #0x20c]              -> RAM
  06ab4:  ldrb.w r0, [r0, #0x65]            
  06ab8:  cbnz r0, #0x6ad6                  
  06aba:  movs r0, #1                       
  06abc:  ldr r1, [pc, #0x200]              -> RAM
  06abe:  strb.w r0, [r1, #0x65]            
  06ac2:  movs r0, #3                       
  06ac4:  strb.w r0, [r1, #0x66]            
  06ac8:  movs r0, #0xa                     
  06aca:  str r0, [sp, #0x10]               
  06acc:  ldrh.w r0, [sp, #0xc]             
  06ad0:  ldr r1, [pc, #0x1f0]              -> RAM
  06ad2:  strh r0, [r1, #0x24]              
  06ad4:  b #0x6c54                         -> 0x06c54 (вне списка функций)
  06ad6:  ldr r0, [pc, #0x1e8]              -> RAM
  06ad8:  ldrb.w r0, [r0, #0x66]            
  06adc:  cmp r0, #1                        
  06ade:  beq #0x6ae6                       
  06ae0:  cmp r0, #2                        
  06ae2:  bne #0x6b8a                       
  06ae4:  b #0x6b56                         -> 0x06b56 (вне списка функций)
  06ae6:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06aea:  cmp r0, #0                        
  06aec:  bgt #0x6b0a                       
  06aee:  ldrh.w r0, [sp, #0xc]             
  06af2:  cmp r0, r7                        
  06af4:  bgt #0x6b0a                       
  06af6:  bl #0x8f58                        -> func_0x08f58
  06afa:  cmn.w r0, #5                      
  06afe:  bge #0x6b20                       
  06b00:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06b04:  ldr r1, [pc, #0x1c0]              
  06b06:  cmp r0, r1                        
  06b08:  bge #0x6b20                       
  06b0a:  movs r0, #3                       
  06b0c:  ldr r1, [pc, #0x1b0]              -> RAM
  06b0e:  strb.w r0, [r1, #0x66]            
  06b12:  movs r0, #0xa                     
  06b14:  str r0, [sp, #0x10]               
  06b16:  ldrh.w r0, [sp, #0xc]             
  06b1a:  ldr r1, [pc, #0x1a8]              -> RAM
  06b1c:  strh r0, [r1, #0x24]              
  06b1e:  b #0x6b54                         -> 0x06b54 (вне списка функций)
  06b20:  bl #0x8f58                        -> func_0x08f58
  06b24:  mov sb, r0                        
  06b26:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06b2a:  mov sl, r0                        
  06b2c:  bl #0x16570                       -> 0x16570 (вне списка функций)
  06b30:  mov fp, r0                        
  06b32:  ldr r3, [pc, #0x190]              -> RAM
  06b34:  adds r3, #0x24                    
  06b36:  mov r2, sb                        
  06b38:  mov r1, sl                        
  06b3a:  bl #0xe2fc                        -> func_0x0e2fc
  06b3e:  bl #0x8f58                        -> func_0x08f58
  06b42:  mov sb, r0                        
  06b44:  ldr r0, [pc, #0x17c]              -> RAM
  06b46:  ldrh r1, [r0, #0x24]              
  06b48:  add r3, sp, #0x10                 
  06b4a:  mov r2, sb                        
  06b4c:  ldrh.w r0, [sp, #0xc]             
  06b50:  bl #0xe2cc                        -> func_0x0e2cc
  06b54:  b #0x6c52                         -> 0x06c52 (вне списка функций)
  06b56:  ldrh.w r0, [sp, #0xc]             
  06b5a:  movw r1, #0xf6e                   
  06b5e:  cmp r0, r1                        
  06b60:  blt #0x6b6a                       
  06b62:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06b66:  cmp r0, #0                        
  06b68:  bge #0x6b80                       
  06b6a:  movs r0, #3                       
  06b6c:  ldr r1, [pc, #0x150]              -> RAM
  06b6e:  strb.w r0, [r1, #0x66]            
  06b72:  movs r0, #0xa                     
  06b74:  str r0, [sp, #0x10]               
  06b76:  ldrh.w r0, [sp, #0xc]             
  06b7a:  ldr r1, [pc, #0x148]              -> RAM
  06b7c:  strh r0, [r1, #0x24]              
  06b7e:  b #0x6b88                         -> 0x06b88 (вне списка функций)
  06b80:  add r1, sp, #0xc                  
  06b82:  add r0, sp, #0x10                 
  06b84:  bl #0xe808                        -> func_0x0e808
  06b88:  b #0x6c52                         -> 0x06c52 (вне списка функций)
  06b8a:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06b8e:  cmp r0, #0                        
  06b90:  bgt #0x6c04                       
  06b92:  ldrh.w r0, [sp, #0xc]             
  06b96:  cmp r0, r7                        
  06b98:  bgt #0x6c04                       
  06b9a:  bl #0x8f58                        -> func_0x08f58
  06b9e:  cmn.w r0, #5                      
  06ba2:  bge #0x6bb0                       
  06ba4:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06ba8:  ldr r1, [pc, #0x11c]              
  06baa:  adds r1, #0x32                    
  06bac:  cmp r0, r1                        
  06bae:  blt #0x6bee                       
  06bb0:  movs r0, #1                       
  06bb2:  ldr r1, [pc, #0x10c]              -> RAM
  06bb4:  strb.w r0, [r1, #0x66]            
  06bb8:  bl #0x8f58                        -> func_0x08f58
  06bbc:  mov sb, r0                        
  06bbe:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06bc2:  mov sl, r0                        
  06bc4:  bl #0x16570                       -> 0x16570 (вне списка функций)
  06bc8:  mov fp, r0                        
  06bca:  ldr r3, [pc, #0xf8]               -> RAM
  06bcc:  adds r3, #0x24                    
  06bce:  mov r2, sb                        
  06bd0:  mov r1, sl                        
  06bd2:  bl #0xe2fc                        -> func_0x0e2fc
  06bd6:  bl #0x8f58                        -> func_0x08f58
  06bda:  mov sb, r0                        
  06bdc:  ldr r0, [pc, #0xe4]               -> RAM
  06bde:  ldrh r1, [r0, #0x24]              
  06be0:  add r3, sp, #0x10                 
  06be2:  mov r2, sb                        
  06be4:  ldrh.w r0, [sp, #0xc]             
  06be8:  bl #0xe2cc                        -> func_0x0e2cc
  06bec:  b #0x6c50                         -> 0x06c50 (вне списка функций)
  06bee:  movs r0, #3                       
  06bf0:  ldr r1, [pc, #0xcc]               -> RAM
  06bf2:  strb.w r0, [r1, #0x66]            
  06bf6:  movs r0, #0xa                     
  06bf8:  str r0, [sp, #0x10]               
  06bfa:  ldrh.w r0, [sp, #0xc]             
  06bfe:  ldr r1, [pc, #0xc4]               -> RAM
  06c00:  strh r0, [r1, #0x24]              
  06c02:  b #0x6c50                         -> 0x06c50 (вне списка функций)
  06c04:  ldrh.w r0, [sp, #0xc]             
  06c08:  cmp.w r0, #0xfa0                  
  06c0c:  ble #0x6c44                       
  06c0e:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06c12:  cmp r0, #0                        
  06c14:  ble #0x6c44                       
  06c16:  movs r0, #2                       
  06c18:  ldr r1, [pc, #0xa4]               -> RAM
  06c1a:  strb.w r0, [r1, #0x66]            
  06c1e:  movs r0, #0                       
  06c20:  str r0, [r1, #0x40]               
  06c22:  strh.w r0, [r1, #0x4e]            
  06c26:  ldrh.w r0, [sp, #0xc]             
  06c2a:  strh.w r0, [r1, #0x4c]            
  06c2e:  movs r0, #0                       
  06c30:  strb.w r0, [r1, #0x67]            
  06c34:  movw r0, #0x105f                  
  06c38:  str r0, [r1, #0x2c]               
  06c3a:  add r1, sp, #0xc                  
  06c3c:  add r0, sp, #0x10                 
  06c3e:  bl #0xe808                        -> func_0x0e808
  06c42:  b #0x6c50                         -> 0x06c50 (вне списка функций)
  06c44:  movs r0, #0xa                     
  06c46:  str r0, [sp, #0x10]               
  06c48:  ldrh.w r0, [sp, #0xc]             
  06c4c:  ldr r1, [pc, #0x74]               -> RAM
  06c4e:  strh r0, [r1, #0x24]              
  06c50:  nop                               
  06c52:  nop                               
  06c54:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  06c58:  cmp r0, #0                        
  06c5a:  ble #0x6c60                       
  06c5c:  movs r6, #0x64                    
  06c5e:  b #0x6c88                         -> 0x06c88 (вне списка функций)
  06c60:  bl #0x8f58                        -> func_0x08f58
  06c64:  mov sb, r0                        
  06c66:  movs r2, #5                       
  06c68:  ldr r0, [pc, #0x50]               -> flash-mirror @0x19f60
  06c6a:  subs r0, #8                       
  06c6c:  addw r1, r0, #0x5c7               
  06c70:  add.w r3, r0, #0xd4               
  06c74:  strd r0, r2, [sp, #4]             
  06c78:  str r1, [sp]                      
  06c7a:  sub.w r2, r0, #0x28               
  06c7e:  mov r1, sb                        
  06c80:  mov r0, r4                        
  06c82:  bl #0x16f42                       -> func_0x16f42
  06c86:  mov r6, r0                        
  06c88:  ldrb.w r0, [sp, #0x10]            
  06c8c:  cmp r6, r0                        
  06c8e:  bgt #0x6c98                       
  06c90:  ldr r0, [pc, #0x30]               -> RAM
  06c92:  strb.w r6, [r0, #0x2d]            
  06c96:  b #0x6ca2                         -> 0x06ca2 (вне списка функций)
  06c98:  ldrb.w r0, [sp, #0x10]            
  06c9c:  ldr r1, [pc, #0x24]               -> RAM
  06c9e:  strb.w r0, [r1, #0x2d]            
  06ca2:  movs r0, #0                       
  06ca4:  bl #0x10fd4                       -> 0x10fd4 (вне списка функций)
  06ca8:  ldr r1, [pc, #0x18]               -> RAM
  06caa:  ldrh r0, [r1, #0x24]              
  06cac:  bl #0x11028                       -> 0x11028 (вне списка функций)
  06cb0:  add sp, #0x14                     
  06cb2:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x06cb8 (5 слов) — ВНЕ границ функции ---
  06cb8:  .word 0x7ffff37f
  06cbc:  .word 0x08019f60  ; flash-mirror @0x19f60
  06cc0:  .word 0x200012ba  ; RAM
  06cc4:  .word 0x2000128b  ; RAM
  06cc8:  .word 0xfffff9f2
```
