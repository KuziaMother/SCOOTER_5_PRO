# func_0x06ae6

| | |
|---|---|
| offset в файле | `0x06ae6` |
| vaddr (база 0x01800000) | `0x01806ae6` |
 | размер кода | 548 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202044 — RAM (r3)
- 0x00202ab0 — RAM (r0)
- 0x00202ad4 — RAM (r0)
- 0x00202d18 — RAM (r0)

## Вызовы (callees)

- 0x0161fba2 (bl, вне списка функций)
- 0x01624172 (bl, вне списка функций)
- `func_0x06a12` (0x01806a12, bl)
- `func_0x06abc` (0x01806abc, bl)
- 0x01806b6e (b, вне списка функций)
- 0x01806bf0 (b, вне списка функций)
- 0x01806bfe (b, вне списка функций)
- 0x01806c82 (b, вне списка функций)
- 0x01806caa (b, вне списка функций)
- 0x01806cac (b, вне списка функций)
- 0x01806cf8 (b, вне списка функций)
- 0x01809334 (bl, вне списка функций)
- 0x01809348 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01806ae6:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, lr}
  01806aea:  movs r5, #0                       
  01806aec:  mov r4, r0                        
  01806aee:  strb.w r5, [r0, #0x21]            
  01806af2:  movw r0, #0x777                   
  01806af6:  str r0, [r4, #4]                  
  01806af8:  ldrb r0, [r4, #0x10]              
  01806afa:  mov r6, r5                        
  01806afc:  mov.w r8, #-1                     
  01806b00:  mov fp, r5                        
  01806b02:  cmp r0, #0                        
  01806b04:  beq #0x1806bec                    
  01806b06:  ldrb.w r0, [r4, #0x20]            
  01806b0a:  cmp r0, #0                        
  01806b0c:  beq #0x1806b04                    
  01806b0e:  mov r0, r4                        
  01806b10:  bl #0x1806abc                     -> func_0x06abc
  01806b14:  cbz r0, #0x1806b20                
  01806b16:  ldrb r0, [r4, #0x21]!             
  01806b1a:  orr r0, r0, #4                    
  01806b1e:  b #0x1806caa                      -> 0x06caa (вне списка функций)
  01806b20:  mov r0, r4                        
  01806b22:  bl #0x1624172                     
  01806b26:  cbz r0, #0x1806b34                
  01806b28:  ldrb.w r0, [r4, #0x21]            
  01806b2c:  orr r0, r0, #0x40                 
  01806b30:  strb.w r0, [r4, #0x21]            
  01806b34:  ldr r3, [pc, #0x7c]               (RAM)
  01806b36:  ldrh r0, [r4, #0xc]               
  01806b38:  strh.w r0, [r3, #0x2a8]           
  01806b3c:  ldr r0, [r4, #8]                  
  01806b3e:  str.w r0, [r3, #0x2a4]            
  01806b42:  ldrb.w r0, [r3, #0x1ec]           
  01806b46:  lsls r0, r0, #0x1f                
  01806b48:  beq #0x1806b72                    
  01806b4a:  ldrh.w r0, [r3, #0x1ee]           
  01806b4e:  b #0x1806b6e                      -> 0x06b6e (вне списка функций)
  01806b50:  lsls r1, r0, #0x1f                
  01806b52:  beq #0x1806b68                    
  01806b54:  ldrb r1, [r4, #0xe]               
  01806b56:  cmp r1, r5                        
  01806b58:  beq #0x1806b68                    
  01806b5a:  add.w r1, r3, r5, lsl #4          
  01806b5e:  ldrh.w r2, [r1, #0x2b4]           
  01806b62:  adds r2, r2, #1                   
  01806b64:  strh.w r2, [r1, #0x2b4]           
  01806b68:  lsrs r0, r0, #1                   
  01806b6a:  adds r5, r5, #1                   
  01806b6c:  uxtb r5, r5                       
  01806b6e:  cmp r0, #0                        
  01806b70:  bne #0x1806b50                    
  01806b72:  ldrb.w r0, [r3, #0x28]            
  01806b76:  lsls r0, r0, #0x1f                
  01806b78:  bne #0x1806b82                    
  01806b7a:  ldr r0, [pc, #0x64]               (RAM)
  01806b7c:  ldrb r0, [r0]                     
  01806b7e:  lsls r0, r0, #0x1f                
  01806b80:  beq #0x1806b92                    
  01806b82:  ldrb r0, [r4, #0xe]               
  01806b84:  cmp r0, #0xb                      
  01806b86:  beq #0x1806b92                    
  01806b88:  ldrh.w r0, [r3, #0x364]           
  01806b8c:  adds r0, r0, #1                   
  01806b8e:  strh.w r0, [r3, #0x364]           
  01806b92:  ldrb.w r0, [r3, #0x1b8]           
  01806b96:  lsls r0, r0, #0x1f                
  01806b98:  bne #0x1806ba0                    
  01806b9a:  ldr r0, [pc, #0x38]               (RAM)
  01806b9c:  ldrb r0, [r0, #4]                 
  01806b9e:  cbz r0, #0x1806bee                
  01806ba0:  ldrb r0, [r4, #0xe]               
  01806ba2:  b #0x1806bf0                      -> 0x06bf0 (вне списка функций)
  01806ba4:  adds r0, r2, #1                   
  01806ba6:  movs r0, r4                       
  01806ba8:  adds r4, r2, #1                   
  01806baa:  movs r0, r4                       
  01806bac:  asrs r0, r0, #0x20                
  01806bae:  ands r5, r0                       
  01806bb0:  lsls r4, r6, #2                   
  01806bb2:  lsls r2, r7, #3                   
  01806bb4:  movs r0, #0x44                    
  01806bb6:  movs r0, r4                       
  01806bb8:  adds r4, r4, #2                   
  01806bba:  movs r0, r4                       
  01806bbc:  movs r4, #0x6e                    
  01806bbe:  movs r0, r4                       
  01806bc0:  ldr r0, [r4, #8]                  
  01806bc2:  movs r0, r4                       
  01806bc4:  movs r2, r0                       
  01806bc6:  movs r1, #0x60                    
  01806bc8:  subs r4, r2, r2                   
  01806bca:  movs r0, r4                       
  01806bcc:  lsls r4, r3, #0x1f                
  01806bce:  movs r0, r4                       
  01806bd0:  cmp r2, #0xd4                     
  01806bd2:  movs r0, r4                       
  01806bd4:  cmp r5, #0x18                     
  01806bd6:  movs r0, r4                       
  01806bd8:  adds r0, r5, #2                   
  01806bda:  movs r0, r4                       
  01806bdc:  cmp r5, #0x38                     
  01806bde:  movs r0, r4                       
  01806be0:  cmp r2, #0xb0                     
  01806be2:  movs r0, r4                       
  01806be4:  lsls r0, r6, #0x16                
  01806be6:  movs r0, r4                       
  01806be8:  .byte 0xff, 0xff                  
  01806bea:  movs r3, r0                       
  01806bec:  b #0x1806cf8                      -> 0x06cf8 (вне списка функций)
  01806bee:  b #0x1806bfe                      -> 0x06bfe (вне списка функций)
  01806bf0:  cmp r0, #0xc                      
  01806bf2:  beq #0x1806bfe                    
  01806bf4:  ldrh.w r0, [r3, #0x374]           
  01806bf8:  adds r0, r0, #1                   
  01806bfa:  strh.w r0, [r3, #0x374]           
  01806bfe:  ldrb.w r0, [r3, #0x5c]            
  01806c02:  lsls r0, r0, #0x1f                
  01806c04:  bne #0x1806c0c                    
  01806c06:  ldr r0, [pc, #0x3f8]              (RAM)
  01806c08:  ldrb r0, [r0, #4]                 
  01806c0a:  cbz r0, #0x1806c1c                
  01806c0c:  ldrb r0, [r4, #0xe]               
  01806c0e:  cmp r0, #0xd                      
  01806c10:  beq #0x1806c1c                    
  01806c12:  ldrh.w r0, [r3, #0x384]           
  01806c16:  adds r0, r0, #1                   
  01806c18:  strh.w r0, [r3, #0x384]           
  01806c1c:  movs r7, #0                       
  01806c1e:  mov.w sl, #0x400                  
  01806c22:  mov sb, r3                        
  01806c24:  b #0x1806c82                      -> 0x06c82 (вне списка функций)
  01806c26:  adds r0, r4, r7                   
  01806c28:  ldrb r5, [r0, #0x12]              
  01806c2a:  cmp r5, #0xa                      
  01806c2c:  bhi #0x1806c5e                    
  01806c2e:  mov r0, r5                        
  01806c30:  bl #0x1809334                     -> 0x09334 (вне списка функций)
  01806c34:  cbz r0, #0x1806c56                
  01806c36:  add.w r0, sb, r5, lsl #2          
  01806c3a:  ldr.w r0, [r0, #0x210]            
  01806c3e:  ldr r0, [r0]                      
  01806c40:  ubfx r0, r0, #0x1b, #2            
  01806c44:  add r0, sb                        
  01806c46:  ldrb.w r0, [r0, #0x1f6]           
  01806c4a:  cmp r0, r5                        
  01806c4c:  beq #0x1806c56                    
  01806c4e:  mov r0, r5                        
  01806c50:  bl #0x1809348                     -> 0x09348 (вне списка функций)
  01806c54:  cbnz r0, #0x1806c5e               
  01806c56:  add.w r1, sb, r5, lsl #4          
  01806c5a:  strh.w sl, [r1, #0x2b4]           
  01806c5e:  add.w r0, sb, r5, lsl #4          
  01806c62:  ldrb.w r1, [r0, #0x2b8]           
  01806c66:  adds r1, r1, #1                   
  01806c68:  strb.w r1, [r0, #0x2b8]           
  01806c6c:  ldr r1, [r4, #8]                  
  01806c6e:  str.w r1, [r0, #0x2c0]            
  01806c72:  ldrsh.w r0, [r0, #0x2b4]          
  01806c76:  cmp r0, r8                        
  01806c78:  ble #0x1806c7e                    
  01806c7a:  mov r6, r5                        
  01806c7c:  mov r8, r0                        
  01806c7e:  adds r7, r7, #1                   
  01806c80:  uxtb r7, r7                       
  01806c82:  ldrb.w r0, [r4, #0x20]            
  01806c86:  cmp r0, r7                        
  01806c88:  bhi #0x1806c26                    
  01806c8a:  add.w r5, sb, r6, lsl #4          
  01806c8e:  mov r7, sb                        
  01806c90:  ldrsh.w r0, [r5, #0x2b4]          
  01806c94:  cmp r0, sl                        
  01806c96:  bge #0x1806cb0                    
  01806c98:  mov r1, r6                        
  01806c9a:  mov r0, r4                        
  01806c9c:  bl #0x1806a12                     -> func_0x06a12
  01806ca0:  cbz r0, #0x1806cb0                
  01806ca2:  ldrb r0, [r4, #0x21]!             
  01806ca6:  orr r0, r0, #8                    
  01806caa:  strb r0, [r4]                     
  01806cac:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, pc}
  01806cb0:  ldrb.w r0, [r5, #0x2b8]           
  01806cb4:  strb.w r0, [r7, #0x2ac]           
  01806cb8:  ldrh.w r0, [r5, #0x2b4]           
  01806cbc:  strh.w r0, [r7, #0x2ae]           
  01806cc0:  ldr.w r0, [r5, #0x2bc]            
  01806cc4:  str.w r0, [r7, #0x2b0]            
  01806cc8:  strb.w r6, [r7, #0x2aa]           
  01806ccc:  movs r0, #2                       
  01806cce:  strb.w r0, [r7, #0x2ab]           
  01806cd2:  strb.w fp, [r5, #0x2b8]           
  01806cd6:  ldrh.w r0, [r5, #0x2b6]           
  01806cda:  strh.w r0, [r5, #0x2b4]           
  01806cde:  ldr r0, [r4, #8]!                 
  01806ce2:  str.w r0, [r5, #0x2bc]            
  01806ce6:  movs r1, #2                       
  01806ce8:  mov r0, r6                        
  01806cea:  bl #0x161fba2                     
  01806cee:  ldrb r0, [r4, #0x19]              
  01806cf0:  orr r0, r0, #0x10                 
  01806cf4:  strb r0, [r4, #0x19]              
  01806cf6:  b #0x1806cac                      -> 0x06cac (вне списка функций)
  01806cf8:  movs r1, #0                       
  01806cfa:  movs r0, #0xf                     
  01806cfc:  bl #0x161fba2                     
  01806d00:  ldrb r0, [r4, #0x21]!             
  01806d04:  orr r0, r0, #0x20                 
  01806d08:  b #0x1806caa                      -> 0x06caa (вне списка функций)
  ; --- literal-пул @0x06bb4 (1 слов) ---
  06bb4:  .word 0x00202044  ; RAM
  ; --- literal-пул @0x06bd4 (1 слов) ---
  06bd4:  .word 0x00202d18  ; RAM
  ; --- literal-пул @0x06be0 (1 слов) ---
  06be0:  .word 0x00202ab0  ; RAM
  ; --- literal-пул @0x07000 (1 слов) — ВНЕ границ функции ---
  07000:  .word 0x00202ad4  ; RAM
```
