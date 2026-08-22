# func_0x08bec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008bec) | `0x00008bec` |
| размер кода | 388 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000044 — RAM (r1)
- 0x20000046 — RAM (r1)
- 0x20000052 — RAM (r1)
- 0x20000a72 — RAM (r0)
- 0x20000f10 — RAM (r1)
- 0x20000f70 — RAM (r0)
- 0x20000fbb — RAM (r1)
- 0x200015f7 — RAM (r0)

## Вызовы (callees)

- `func_0x08af0` (0x00008af0, bl)
- 0x08c18 (b, вне списка функций)
- 0x08c82 (b, вне списка функций)
- 0x08cb8 (b, вне списка функций)
- 0x08ccc (b, вне списка функций)
- 0x08cf2 (b, вне списка функций)
- 0x08d54 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x110fc` (bl @0x0001123c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x08c18..0x08c82` (106 Б); цели из: 0x08c08
- `0x08c82..0x08cb8` (54 Б); цели из: 0x08c1c, 0x08c24
- `0x08cb8..0x08cc6` (14 Б); цели из: 0x08c9a
- `0x08cc6..0x08ccc` (6 Б); цели из: 0x08cbe
- `0x08ccc..0x08cd6` (10 Б); цели из: 0x08cc4
- `0x08cd6..0x08cea` (20 Б); цели из: 0x08cce
- `0x08cea..0x08cf2` (8 Б); цели из: 0x08cdc
- `0x08cf2..0x08d54` (98 Б); цели из: 0x08ce8
- `0x08d54..0x08d70` (28 Б); цели из: 0x08d16

## Дизассембляция

```asm
  08bec:  push {r4, r5, r6, lr}             
  08bee:  ldr r0, [pc, #0x180]              -> RAM
  08bf0:  ldrb r0, [r0, #3]                 
  08bf2:  ubfx r0, r0, #2, #1               
  08bf6:  cbz r0, #0x8c1e                   
  08bf8:  ldr r0, [pc, #0x178]              -> RAM
  08bfa:  ldrb r0, [r0]                     
  08bfc:  bic r0, r0, #1                    
  08c00:  adds r0, r0, #1                   
  08c02:  ldr r1, [pc, #0x170]              -> RAM
  08c04:  strb r0, [r1]                     
  08c06:  movs r4, #0                       
  08c08:  b #0x8c18                         -> 0x08c18 (вне списка функций)
  08c0a:  movw r0, #0x9c4                   
  08c0e:  ldr r1, [pc, #0x168]              -> RAM
  08c10:  strh.w r0, [r1, r4, lsl #1]       
  08c14:  adds r0, r4, #1                   
  08c16:  uxtb r4, r0                       
  08c18:  cmp r4, #0xd                      
  08c1a:  blt #0x8c0a                       
  08c1c:  b #0x8c82                         -> 0x08c82 (вне списка функций)
  08c1e:  bl #0x8af0                        -> func_0x08af0
  08c22:  cmp r0, #0                        
  08c24:  beq #0x8c82                       
  08c26:  ldr r0, [pc, #0x14c]              -> RAM
  08c28:  ldrb r0, [r0]                     
  08c2a:  bic r0, r0, #1                    
  08c2e:  ldr r1, [pc, #0x144]              -> RAM
  08c30:  strb r0, [r1]                     
  08c32:  ldr r0, [pc, #0x148]              -> RAM
  08c34:  ldrh r0, [r0, #0x12]              
  08c36:  ldr r1, [pc, #0x140]              -> RAM
  08c38:  strh r0, [r1]                     
  08c3a:  ldr r0, [pc, #0x140]              -> RAM
  08c3c:  ldrh r0, [r0, #0x14]              
  08c3e:  strh r0, [r1, #2]                 
  08c40:  ldr r0, [pc, #0x138]              -> RAM
  08c42:  ldrh r0, [r0, #0x16]              
  08c44:  strh r0, [r1, #4]                 
  08c46:  ldr r0, [pc, #0x134]              -> RAM
  08c48:  ldrh r0, [r0, #0x18]              
  08c4a:  strh r0, [r1, #6]                 
  08c4c:  ldr r0, [pc, #0x12c]              -> RAM
  08c4e:  ldrh r0, [r0, #0x1a]              
  08c50:  strh r0, [r1, #8]                 
  08c52:  ldr r0, [pc, #0x128]              -> RAM
  08c54:  ldrh r0, [r0, #0x1c]              
  08c56:  strh r0, [r1, #0xa]               
  08c58:  ldr r0, [pc, #0x120]              -> RAM
  08c5a:  ldrh r0, [r0, #0x1e]              
  08c5c:  strh r0, [r1, #0xc]               
  08c5e:  ldr r0, [pc, #0x11c]              -> RAM
  08c60:  ldrh r0, [r0, #0x20]              
  08c62:  strh r0, [r1, #0xe]               
  08c64:  ldr r0, [pc, #0x114]              -> RAM
  08c66:  ldrh r0, [r0, #0x22]              
  08c68:  strh r0, [r1, #0x10]              
  08c6a:  ldr r0, [pc, #0x110]              -> RAM
  08c6c:  ldrh r0, [r0, #0x24]              
  08c6e:  strh r0, [r1, #0x12]              
  08c70:  ldr r0, [pc, #0x108]              -> RAM
  08c72:  ldrh r0, [r0, #0x26]              
  08c74:  strh r0, [r1, #0x14]              
  08c76:  ldr r0, [pc, #0x104]              -> RAM
  08c78:  ldrh r0, [r0, #0x28]              
  08c7a:  strh r0, [r1, #0x16]              
  08c7c:  ldr r0, [pc, #0xfc]               -> RAM
  08c7e:  ldrh r0, [r0, #0x2a]              
  08c80:  strh r0, [r1, #0x18]              
  08c82:  ldr r0, [pc, #0xec]               -> RAM
  08c84:  ldrb r0, [r0, #3]                 
  08c86:  ubfx r0, r0, #2, #1               
  08c8a:  cbz r0, #0x8c9c                   
  08c8c:  ldr r0, [pc, #0xe4]               -> RAM
  08c8e:  ldrb r0, [r0]                     
  08c90:  bic r0, r0, #2                    
  08c94:  adds r0, r0, #2                   
  08c96:  ldr r1, [pc, #0xdc]               -> RAM
  08c98:  strb r0, [r1]                     
  08c9a:  b #0x8cb8                         -> 0x08cb8 (вне списка функций)
  08c9c:  ldr r0, [pc, #0xd4]               -> RAM
  08c9e:  ldrb r0, [r0]                     
  08ca0:  bic r0, r0, #2                    
  08ca4:  ldr r1, [pc, #0xcc]               -> RAM
  08ca6:  strb r0, [r1]                     
  08ca8:  ldr r0, [pc, #0xd0]               -> RAM
  08caa:  ldrh r0, [r0, #0x38]              
  08cac:  sxth r0, r0                       
  08cae:  add.w r0, r0, r0, lsl #2          
  08cb2:  lsls r0, r0, #1                   
  08cb4:  ldr r1, [pc, #0xc8]               -> RAM
  08cb6:  str r0, [r1]                      
  08cb8:  ldr r0, [pc, #0xc4]               -> RAM
  08cba:  ldr r0, [r0]                      
  08cbc:  cmp r0, #0                        
  08cbe:  ble #0x8cc6                       
  08cc0:  ldr r0, [pc, #0xbc]               -> RAM
  08cc2:  ldr r0, [r0]                      
  08cc4:  b #0x8ccc                         -> 0x08ccc (вне списка функций)
  08cc6:  ldr r0, [pc, #0xb8]               -> RAM
  08cc8:  ldr r0, [r0]                      
  08cca:  rsbs r0, r0, #0                   
  08ccc:  cmp r0, #0xa                      
  08cce:  bgt #0x8cd6                       
  08cd0:  movs r0, #0                       
  08cd2:  ldr r1, [pc, #0xac]               -> RAM
  08cd4:  str r0, [r1]                      
  08cd6:  ldr r0, [pc, #0xa8]               -> RAM
  08cd8:  ldr r0, [r0]                      
  08cda:  cmp r0, #0                        
  08cdc:  bge #0x8cea                       
  08cde:  ldr r0, [pc, #0xa0]               -> RAM
  08ce0:  ldr r0, [r0]                      
  08ce2:  rsbs r0, r0, #0                   
  08ce4:  ldr r1, [pc, #0x98]               -> RAM
  08ce6:  str r0, [r1, #4]                  
  08ce8:  b #0x8cf2                         -> 0x08cf2 (вне списка функций)
  08cea:  ldr r0, [pc, #0x94]               -> RAM
  08cec:  ldr r0, [r0]                      
  08cee:  ldr r1, [pc, #0x90]               -> RAM
  08cf0:  str r0, [r1, #4]                  
  08cf2:  ldr r0, [pc, #0x7c]               -> RAM
  08cf4:  ldrb r0, [r0, #3]                 
  08cf6:  ubfx r0, r0, #2, #1               
  08cfa:  cbz r0, #0x8d18                   
  08cfc:  ldr r0, [pc, #0x74]               -> RAM
  08cfe:  ldrb r0, [r0]                     
  08d00:  bic r0, r0, #4                    
  08d04:  adds r0, r0, #4                   
  08d06:  ldr r1, [pc, #0x6c]               -> RAM
  08d08:  strb r0, [r1]                     
  08d0a:  movs r0, #0x19                    
  08d0c:  ldr r1, [pc, #0x74]               -> RAM
  08d0e:  strb r0, [r1]                     
  08d10:  movs r0, #0xfa                    
  08d12:  ldr r1, [pc, #0x74]               -> RAM
  08d14:  strh r0, [r1]                     
  08d16:  b #0x8d54                         -> 0x08d54 (вне списка функций)
  08d18:  bl #0x8af0                        -> func_0x08af0
  08d1c:  cbz r0, #0x8d54                   
  08d1e:  ldr r0, [pc, #0x54]               -> RAM
  08d20:  ldrb r0, [r0]                     
  08d22:  bic r0, r0, #4                    
  08d26:  ldr r1, [pc, #0x4c]               -> RAM
  08d28:  strb r0, [r1]                     
  08d2a:  ldr r0, [pc, #0x50]               -> RAM
  08d2c:  ldrh.w r0, [r0, #0x48]            
  08d30:  sxth r5, r0                       
  08d32:  ldr r0, [pc, #0x48]               -> RAM
  08d34:  ldrh.w r0, [r0, #0x48]            
  08d38:  subw r0, r0, #0xaaf               
  08d3c:  sxth r0, r0                       
  08d3e:  ldr r1, [pc, #0x48]               -> RAM
  08d40:  strh r0, [r1]                     
  08d42:  subw r0, r5, #0xaaf               
  08d46:  movs r1, #0xa                     
  08d48:  sdiv r0, r0, r1                   
  08d4c:  sxth r5, r0                       
  08d4e:  sxtb r0, r5                       
  08d50:  ldr r1, [pc, #0x30]               -> RAM
  08d52:  strb r0, [r1]                     
  08d54:  ldr r0, [pc, #0x24]               -> RAM
  08d56:  ldrh.w r0, [r0, #0x40]            
  08d5a:  sxth r6, r0                       
  08d5c:  subw r0, r6, #0xaaf               
  08d60:  movs r1, #0xa                     
  08d62:  sdiv r0, r0, r1                   
  08d66:  sxth r6, r0                       
  08d68:  sxtb r0, r6                       
  08d6a:  ldr r1, [pc, #0x20]               -> RAM
  08d6c:  strb r0, [r1]                     
  08d6e:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x08d70 (8 слов) — ВНЕ границ функции ---
  08d70:  .word 0x20000f70  ; RAM
  08d74:  .word 0x20000a72  ; RAM
  08d78:  .word 0x20000f10  ; RAM
  08d7c:  .word 0x200015f7  ; RAM
  08d80:  .word 0x20000fbb  ; RAM
  08d84:  .word 0x20000044  ; RAM
  08d88:  .word 0x20000046  ; RAM
  08d8c:  .word 0x20000052  ; RAM
```
