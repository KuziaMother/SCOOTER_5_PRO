# func_0x13c78

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080013c78) | `0x00013c78` |
| размер кода | 392 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019575 — flash-mirror @0x19575 (r0)
- 0x20000044 — RAM (r0)
- 0x20000098 — RAM (r0)
- 0x20000cb0 — RAM (r1)
- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)
- 0x20000fc7 — RAM (r0)
- 0x20000fd3 — RAM (r0)
- 0x200015f7 — RAM (r0)
- 0x2000309d — RAM (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x08a90` (0x00008a90, bl)
- 0x13d24 (b, вне списка функций)
- 0x13d48 (b, вне списка функций)
- 0x13d6c (b, вне списка функций)
- 0x13d9a (b, вне списка функций)
- 0x142aa (b, вне списка функций)
- 0x142cc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1395c` (bl @0x0001397a)
- `func_0x139ac` (bl @0x000139b4)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x13d18..0x13d24` (12 Б); цели из: 0x13d0e
- `0x13d24..0x13d3c` (24 Б); цели из: 0x13d16
- `0x13d3c..0x13d48` (12 Б); цели из: 0x13d32
- `0x13d48..0x13d60` (24 Б); цели из: 0x13d3a
- `0x13d60..0x13d6c` (12 Б); цели из: 0x13d56
- `0x13d6c..0x13d8a` (30 Б); цели из: 0x13d5e
- `0x13d8a..0x13d9a` (16 Б); цели из: 0x13d7e
- `0x13d9a..0x13df4` (90 Б); цели из: 0x13d88
- `0x13df4..0x13e00` (12 Б); цели из: 0x13dd4

## Дизассембляция

```asm
  13c78:  push {r4, r5, lr}                 
  13c7a:  sub sp, #0x2c                     
  13c7c:  mov r4, r0                        
  13c7e:  nop                               
  13c80:  add r0, sp, #0x24                 
  13c82:  bl #0x8a90                        -> func_0x08a90
  13c86:  ldr r0, [pc, #0x3f8]              -> RAM
  13c88:  ldr r1, [sp, #0x24]               
  13c8a:  str r1, [r0]                      
  13c8c:  ldrh.w r1, [sp, #0x28]            
  13c90:  strh r1, [r0, #4]                 
  13c92:  ldrb.w r1, [sp, #0x2a]            
  13c96:  strb r1, [r0, #6]                 
  13c98:  movs r2, #0x19                    
  13c9a:  ldr r1, [pc, #0x3e8]              -> RAM
  13c9c:  add.w r0, r1, #0x19               
  13ca0:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  13ca4:  movs r2, #0x19                    
  13ca6:  ldr r1, [pc, #0x3dc]              -> RAM
  13ca8:  subs r1, #0x19                    
  13caa:  ldr r0, [pc, #0x3d8]              -> RAM
  13cac:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  13cb0:  ldr r0, [pc, #0x3cc]              -> RAM
  13cb2:  ldrb r0, [r0, #5]                 
  13cb4:  ldr r1, [pc, #0x3cc]              -> RAM
  13cb6:  subs r1, #0x19                    
  13cb8:  strb r0, [r1]                     
  13cba:  ldr r0, [pc, #0x3c4]              -> RAM
  13cbc:  ldrb r0, [r0, #4]                 
  13cbe:  strb r0, [r1, #1]                 
  13cc0:  ldr r0, [pc, #0x3bc]              -> RAM
  13cc2:  ldrb r0, [r0, #3]                 
  13cc4:  strb r0, [r1, #2]                 
  13cc6:  ldr r0, [pc, #0x3b8]              -> RAM
  13cc8:  ldrb r0, [r0, #2]                 
  13cca:  strb r0, [r1, #3]                 
  13ccc:  ldr r0, [pc, #0x3b0]              -> RAM
  13cce:  ldrb r0, [r0, #1]                 
  13cd0:  strb r0, [r1, #4]                 
  13cd2:  ldr r0, [pc, #0x3ac]              -> RAM
  13cd4:  ldrb r0, [r0]                     
  13cd6:  strb r0, [r1, #5]                 
  13cd8:  movs r0, #0                       
  13cda:  strb r0, [r1, #6]                 
  13cdc:  strb r0, [r1, #7]                 
  13cde:  ldr r0, [pc, #0x3a8]              -> RAM
  13ce0:  ldrb r0, [r0, #0xb]               
  13ce2:  strb r0, [r1, #8]                 
  13ce4:  ldr r0, [pc, #0x3a0]              -> RAM
  13ce6:  ldrh r0, [r0, #8]                 
  13ce8:  asrs r0, r0, #8                   
  13cea:  strb r0, [r1, #9]                 
  13cec:  ldr r0, [pc, #0x398]              -> RAM
  13cee:  ldrb r0, [r0, #8]                 
  13cf0:  strb r0, [r1, #0xa]               
  13cf2:  ldr r0, [pc, #0x394]              -> RAM
  13cf4:  ldrb r0, [r0, #0xa]               
  13cf6:  strb r0, [r1, #0xb]               
  13cf8:  ldr r0, [pc, #0x38c]              -> RAM
  13cfa:  ldrh r0, [r0, #6]                 
  13cfc:  asrs r0, r0, #8                   
  13cfe:  strb r0, [r1, #0xc]               
  13d00:  ldr r0, [pc, #0x384]              -> RAM
  13d02:  ldrb r0, [r0, #6]                 
  13d04:  strb r0, [r1, #0xd]               
  13d06:  ldr r0, [pc, #0x384]              -> RAM
  13d08:  ldrsb.w r0, [r0]                  
  13d0c:  cmp r0, #0                        
  13d0e:  blt #0x13d18                      
  13d10:  ldr r0, [pc, #0x378]              -> RAM
  13d12:  ldrsb.w r0, [r0]                  
  13d16:  b #0x13d24                        -> 0x13d24 (вне списка функций)
  13d18:  ldr r0, [pc, #0x370]              -> RAM
  13d1a:  ldrsb.w r0, [r0]                  
  13d1e:  rsbs r0, r0, #0                   
  13d20:  orr r0, r0, #0x80                 
  13d24:  ldr r1, [pc, #0x35c]              -> RAM
  13d26:  subs r1, #0x19                    
  13d28:  strb r0, [r1, #0xe]               
  13d2a:  ldr r0, [pc, #0x360]              -> RAM
  13d2c:  ldrsb.w r0, [r0, #1]              
  13d30:  cmp r0, #0                        
  13d32:  blt #0x13d3c                      
  13d34:  ldr r0, [pc, #0x354]              -> RAM
  13d36:  ldrsb.w r0, [r0, #1]              
  13d3a:  b #0x13d48                        -> 0x13d48 (вне списка функций)
  13d3c:  ldr r0, [pc, #0x34c]              -> RAM
  13d3e:  ldrsb.w r0, [r0, #1]              
  13d42:  rsbs r0, r0, #0                   
  13d44:  orr r0, r0, #0x80                 
  13d48:  ldr r1, [pc, #0x338]              -> RAM
  13d4a:  subs r1, #0x19                    
  13d4c:  strb r0, [r1, #0xf]               
  13d4e:  ldr r0, [pc, #0x340]              -> RAM
  13d50:  ldrsb.w r0, [r0, #8]              
  13d54:  cmp r0, #0                        
  13d56:  blt #0x13d60                      
  13d58:  ldr r0, [pc, #0x334]              -> RAM
  13d5a:  ldrsb.w r0, [r0, #8]              
  13d5e:  b #0x13d6c                        -> 0x13d6c (вне списка функций)
  13d60:  ldr r0, [pc, #0x32c]              -> RAM
  13d62:  ldrsb.w r0, [r0, #8]              
  13d66:  rsbs r0, r0, #0                   
  13d68:  orr r0, r0, #0x80                 
  13d6c:  ldr r1, [pc, #0x314]              -> RAM
  13d6e:  subs r1, #0x19                    
  13d70:  strb r0, [r1, #0x10]              
  13d72:  ldr r0, [pc, #0x320]              -> RAM
  13d74:  ldr r0, [r0]                      
  13d76:  movs r1, #0xa                     
  13d78:  sdiv r0, r0, r1                   
  13d7c:  cmp r0, #0                        
  13d7e:  blt #0x13d8a                      
  13d80:  ldr r0, [pc, #0x310]              -> RAM
  13d82:  ldr r0, [r0]                      
  13d84:  sdiv r0, r0, r1                   
  13d88:  b #0x13d9a                        -> 0x13d9a (вне списка функций)
  13d8a:  ldr r0, [pc, #0x308]              -> RAM
  13d8c:  ldr r0, [r0]                      
  13d8e:  rsbs r0, r0, #0                   
  13d90:  movs r1, #0xa                     
  13d92:  sdiv r0, r0, r1                   
  13d96:  orr r0, r0, #0x8000               
  13d9a:  uxth r5, r0                       
  13d9c:  asrs r0, r5, #8                   
  13d9e:  ldr r1, [pc, #0x2e4]              -> RAM
  13da0:  subs r1, #0x19                    
  13da2:  strb r0, [r1, #0x11]              
  13da4:  strb r5, [r1, #0x12]              
  13da6:  ldr r0, [pc, #0x2f0]              -> RAM
  13da8:  ldrb r0, [r0]                     
  13daa:  strb r0, [r1, #0x13]              
  13dac:  ldr r0, [pc, #0x2ec]              -> RAM
  13dae:  ldrh r0, [r0, #0x34]              
  13db0:  add.w r0, r0, r0, lsl #2          
  13db4:  lsls r0, r0, #0x11                
  13db6:  lsrs r5, r0, #0x10                
  13db8:  asrs r0, r5, #8                   
  13dba:  strb r0, [r1, #0x14]              
  13dbc:  strb r5, [r1, #0x15]              
  13dbe:  ldr r0, [pc, #0x2e0]              -> flash-mirror @0x19575
  13dc0:  ldrb r0, [r0, #2]                 
  13dc2:  strb r0, [r1, #0x16]              
  13dc4:  ldr r0, [pc, #0x2d8]              -> flash-mirror @0x19575
  13dc6:  ldrb r1, [r0, #3]                 
  13dc8:  ldr r0, [pc, #0x2b8]              -> RAM
  13dca:  subs r0, #0x19                    
  13dcc:  strb r1, [r0, #0x17]              
  13dce:  ldrb r0, [r4]                     
  13dd0:  cbz r0, #0x13de0                  
  13dd2:  cmp r0, #1                        
  13dd4:  beq #0x13df4                      
  13dd6:  cmp r0, #2                        
  13dd8:  beq #0x13ed2                      
  13dda:  cmp r0, #3                        
  13ddc:  bne #0x13ed4                      
  13dde:  b #0x142aa                        -> 0x142aa (вне списка функций)
  13de0:  movs r0, #1                       
  13de2:  ldr r1, [pc, #0x2c0]              -> RAM
  13de4:  strb r0, [r1]                     
  13de6:  movs r0, #2                       
  13de8:  ldr r1, [pc, #0x298]              -> RAM
  13dea:  subs r1, #0x19                    
  13dec:  strb r0, [r1, #6]                 
  13dee:  movs r0, #0                       
  13df0:  strb r0, [r1, #7]                 
  13df2:  b #0x142cc                        -> 0x142cc (вне списка функций)
  13df4:  movs r0, #3                       
  13df6:  ldr r1, [pc, #0x2ac]              -> RAM
  13df8:  strb r0, [r1]                     
  13dfa:  ldr r0, [pc, #0x2ac]              -> RAM
  13dfc:  ldrb r0, [r0, #2]                 
  13dfe:  .byte 0xc0, 0xf3                  
  ; --- literal-пул @0x14080 (11 слов) — ВНЕ границ функции ---
  14080:  .word 0x20000098  ; RAM
  14084:  .word 0x2000309d  ; RAM
  14088:  .word 0x20000f95  ; RAM
  1408c:  .word 0x20000044  ; RAM
  14090:  .word 0x20000fc7  ; RAM
  14094:  .word 0x20000fbb  ; RAM
  14098:  .word 0x20000fd3  ; RAM
  1409c:  .word 0x200015f7  ; RAM
  140a0:  .word 0x08019575  ; flash-mirror @0x19575
  140a4:  .word 0x20000cb0  ; RAM
  140a8:  .word 0x20000f70  ; RAM
```
