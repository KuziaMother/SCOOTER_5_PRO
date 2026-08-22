# func_0x119e4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800119e4) | `0x000119e4` |
| размер кода | 434 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b8e — RAM (r2)
- 0x20000c06 — RAM (r2)
- 0x20001fac — RAM (r1)
- 0x20001fd4 — RAM (r0)
- 0x200027e0 — RAM (r0)

## Вызовы (callees)

- `func_0x03b82` (0x00003b82, bl)
- `func_0x082f0` (0x000082f0, bl)
- `func_0x08380` (0x00008380, bl)
- `func_0x084a0` (0x000084a0, bl)
- 0x11a22 (b, вне списка функций)
- 0x11a48 (b, вне списка функций)
- 0x11b5e (b, вне списка функций)
- 0x11b76 (b, вне списка функций)
- 0x11b92 (b, вне списка функций)
- `func_0x15758` (0x00015758, bl)

## Кто вызывает (callers / xrefs)

- `func_0x15df4` (bl @0x00015e22)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x11a20..0x11a26` (6 Б); цели из: 0x11a00, 0x11a0a
- `0x11a26..0x11a48` (34 Б); цели из: 0x11a10
- `0x11a48..0x11a5e` (22 Б); цели из: 0x11a34
- `0x11a5e..0x11b04` (166 Б); цели из: 0x11a4e
- `0x11b04..0x11b5c` (88 Б); цели из: 0x11ae2, 0x11afc
- `0x11b5c..0x11b5e` (2 Б); цели из: 0x11a5c
- `0x11b5e..0x11b72` (20 Б); цели из: 0x11b5a
- `0x11b72..0x11b76` (4 Б); цели из: 0x11b4a, 0x11b68
- `0x11b76..0x11b92` (28 Б); цели из: 0x11b5c
- `0x11b92..0x11b96` (4 Б); цели из: 0x11b02

## Дизассембляция

```asm
  119e4:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  119e8:  mov r6, r0                        
  119ea:  mov r8, r1                        
  119ec:  mov r4, r2                        
  119ee:  mov r7, r3                        
  119f0:  movs r5, #0                       
  119f2:  mov sb, r5                        
  119f4:  ldr r0, [pc, #0x1a0]              -> RAM
  119f6:  ldr.w r0, [r0, #0x800]            
  119fa:  add r0, r4                        
  119fc:  cmp.w r0, #0x800                  
  11a00:  bhi #0x11a20                      
  11a02:  ldr r0, [pc, #0x194]              -> RAM
  11a04:  ldr.w r0, [r0, #0x804]            
  11a08:  cmp r0, r4                        
  11a0a:  blo #0x11a20                      
  11a0c:  cbz r4, #0x11a20                  
  11a0e:  cmp r7, #1                        
  11a10:  beq #0x11a26                      
  11a12:  mov.w r0, #0x800                  
  11a16:  udiv r1, r0, r4                   
  11a1a:  mls r0, r4, r1, r0                
  11a1e:  cbz r0, #0x11a26                  
  11a20:  movs r0, #0                       
  11a22:  pop.w {r3, r4, r5, r6, r7, r8, sb, pc}
  11a26:  ubfx r0, r6, #0, #0xb             
  11a2a:  cbnz r0, #0x11a32                 
  11a2c:  ldr r0, [pc, #0x168]              -> RAM
  11a2e:  str.w r6, [r0, #0x808]            
  11a32:  movs r5, #0                       
  11a34:  b #0x11a48                        -> 0x11a48 (вне списка функций)
  11a36:  ldrb.w r0, [r8, r5]               
  11a3a:  ldr r1, [pc, #0x15c]              -> RAM
  11a3c:  ldr.w r1, [r1, #0x800]            
  11a40:  add r1, r5                        
  11a42:  ldr r2, [pc, #0x154]              -> RAM
  11a44:  strb r0, [r2, r1]                 
  11a46:  adds r5, r5, #1                   
  11a48:  cmp r5, r4                        
  11a4a:  blo #0x11a36                      
  11a4c:  cmp r7, #1                        
  11a4e:  beq #0x11a5e                      
  11a50:  ldr r0, [pc, #0x144]              -> RAM
  11a52:  ldr.w r0, [r0, #0x800]            
  11a56:  add r0, r4                        
  11a58:  cmp.w r0, #0x800                  
  11a5c:  bne #0x11b5c                      
  11a5e:  ldr r0, [pc, #0x138]              -> RAM
  11a60:  ldrh.w r0, [r0, #0x808]           
  11a64:  ubfx r0, r0, #0, #0xc             
  11a68:  cbnz r0, #0x11a86                 
  11a6a:  ldr r1, [pc, #0x12c]              -> RAM
  11a6c:  ldr.w r0, [r1, #0x808]            
  11a70:  bl #0x82f0                        -> func_0x082f0
  11a74:  movs r0, #0x64                    
  11a76:  str r0, [sp]                      
  11a78:  nop                               
  11a7a:  ldr r0, [sp]                      
  11a7c:  subs r1, r0, #1                   
  11a7e:  str r1, [sp]                      
  11a80:  cmp r0, #0                        
  11a82:  bne #0x11a7a                      
  11a84:  nop                               
  11a86:  mov.w r1, #0x800                  
  11a8a:  ldr r0, [pc, #0x10c]              -> RAM
  11a8c:  bl #0x3b82                        -> func_0x03b82
  11a90:  ldr r1, [pc, #0x108]              -> RAM
  11a92:  ldrh r1, [r1, #0xc]               
  11a94:  subs r1, r1, #3                   
  11a96:  ldr r2, [pc, #0x108]              -> RAM
  11a98:  strh.w r0, [r2, r1, lsl #1]       
  11a9c:  ldr r0, [pc, #0xf8]               -> RAM
  11a9e:  ldrh.w r0, [r0, #0x800]           
  11aa2:  add r0, r4                        
  11aa4:  uxth r2, r0                       
  11aa6:  ldr r0, [pc, #0xf0]               -> RAM
  11aa8:  ldr.w r1, [r0, #0x808]            
  11aac:  bl #0x84a0                        -> func_0x084a0
  11ab0:  mov sb, r0                        
  11ab2:  ldr r0, [pc, #0xe4]               -> RAM
  11ab4:  ldrh.w r0, [r0, #0x800]           
  11ab8:  add r0, r4                        
  11aba:  uxth r2, r0                       
  11abc:  ldr r0, [pc, #0xd8]               -> RAM
  11abe:  ldr.w r1, [r0, #0x808]            
  11ac2:  ldr r0, [pc, #0xe0]               -> RAM
  11ac4:  bl #0x8380                        -> func_0x08380
  11ac8:  mov.w r1, #0x800                  
  11acc:  ldr r0, [pc, #0xd4]               -> RAM
  11ace:  bl #0x3b82                        -> func_0x03b82
  11ad2:  ldr r1, [pc, #0xc8]               -> RAM
  11ad4:  ldrh r1, [r1, #0xc]               
  11ad6:  subs r1, r1, #3                   
  11ad8:  ldr r2, [pc, #0xcc]               -> RAM
  11ada:  strh.w r0, [r2, r1, lsl #1]       
  11ade:  cmp.w sb, #1                      
  11ae2:  bne #0x11b04                      
  11ae4:  ldr r0, [pc, #0xb4]               -> RAM
  11ae6:  ldrh r0, [r0, #0xc]               
  11ae8:  subs r0, r0, #3                   
  11aea:  ldr r1, [pc, #0xb4]               -> RAM
  11aec:  ldrh.w r1, [r1, r0, lsl #1]       
  11af0:  ldr r0, [pc, #0xa8]               -> RAM
  11af2:  ldrh r0, [r0, #0xc]               
  11af4:  subs r0, r0, #3                   
  11af6:  ldrh.w r0, [r2, r0, lsl #1]       
  11afa:  cmp r1, r0                        
  11afc:  bne #0x11b04                      
  11afe:  bl #0x15758                       -> func_0x15758
  11b02:  b #0x11b92                        -> 0x11b92 (вне списка функций)
  11b04:  ldr r0, [pc, #0x90]               -> RAM
  11b06:  ldrh.w r0, [r0, #0x800]           
  11b0a:  add r0, r4                        
  11b0c:  uxth r2, r0                       
  11b0e:  ldr r0, [pc, #0x88]               -> RAM
  11b10:  ldr.w r1, [r0, #0x808]            
  11b14:  bl #0x84a0                        -> func_0x084a0
  11b18:  mov sb, r0                        
  11b1a:  ldr r0, [pc, #0x7c]               -> RAM
  11b1c:  ldrh.w r0, [r0, #0x800]           
  11b20:  add r0, r4                        
  11b22:  uxth r2, r0                       
  11b24:  ldr r0, [pc, #0x70]               -> RAM
  11b26:  ldr.w r1, [r0, #0x808]            
  11b2a:  ldr r0, [pc, #0x78]               -> RAM
  11b2c:  bl #0x8380                        -> func_0x08380
  11b30:  mov.w r1, #0x800                  
  11b34:  ldr r0, [pc, #0x6c]               -> RAM
  11b36:  bl #0x3b82                        -> func_0x03b82
  11b3a:  ldr r1, [pc, #0x60]               -> RAM
  11b3c:  ldrh r1, [r1, #0xc]               
  11b3e:  subs r1, r1, #3                   
  11b40:  ldr r2, [pc, #0x64]               -> RAM
  11b42:  strh.w r0, [r2, r1, lsl #1]       
  11b46:  cmp.w sb, #1                      
  11b4a:  bne #0x11b72                      
  11b4c:  ldr r0, [pc, #0x4c]               -> RAM
  11b4e:  ldrh r0, [r0, #0xc]               
  11b50:  subs r0, r0, #3                   
  11b52:  ldr r1, [pc, #0x4c]               -> RAM
  11b54:  ldrh.w r1, [r1, r0, lsl #1]       
  11b58:  ldr r0, [pc, #0x40]               -> RAM
  11b5a:  b #0x11b5e                        -> 0x11b5e (вне списка функций)
  11b5c:  b #0x11b76                        -> 0x11b76 (вне списка функций)
  11b5e:  ldrh r0, [r0, #0xc]               
  11b60:  subs r0, r0, #3                   
  11b62:  ldrh.w r0, [r2, r0, lsl #1]       
  11b66:  cmp r1, r0                        
  11b68:  bne #0x11b72                      
  11b6a:  bl #0x15758                       -> func_0x15758
  11b6e:  movs r0, #1                       
  11b70:  b #0x11a22                        -> 0x11a22 (вне списка функций)
  11b72:  movs r0, #0                       
  11b74:  b #0x11a22                        -> 0x11a22 (вне списка функций)
  11b76:  ldr r0, [pc, #0x20]               -> RAM
  11b78:  ldr.w r0, [r0, #0x800]            
  11b7c:  add r0, r4                        
  11b7e:  ldr r1, [pc, #0x18]               -> RAM
  11b80:  str.w r0, [r1, #0x800]            
  11b84:  mov r0, r1                        
  11b86:  ldr.w r0, [r0, #0x800]            
  11b8a:  rsb.w r0, r0, #0x800              
  11b8e:  str.w r0, [r1, #0x804]            
  11b92:  movs r0, #1                       
  11b94:  b #0x11a22                        -> 0x11a22 (вне списка функций)
  ; --- literal-пул @0x11b98 (5 слов) — ВНЕ границ функции ---
  11b98:  .word 0x20001fd4  ; RAM
  11b9c:  .word 0x20001fac  ; RAM
  11ba0:  .word 0x20000c06  ; RAM
  11ba4:  .word 0x200027e0  ; RAM
  11ba8:  .word 0x20000b8e  ; RAM
```
