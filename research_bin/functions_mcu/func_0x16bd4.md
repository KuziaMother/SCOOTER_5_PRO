# func_0x16bd4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080016bd4) | `0x00016bd4` |
| размер кода | 442 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x161ea` (0x000161ea, bl)
- 0x16c1e (b, вне списка функций)
- 0x16c22 (b, вне списка функций)
- 0x16c50 (b, вне списка функций)
- 0x16c90 (b, вне списка функций)
- 0x16c94 (b, вне списка функций)
- 0x16cc2 (b, вне списка функций)
- 0x16d0e (b, вне списка функций)
- 0x16d56 (b, вне списка функций)
- 0x16d86 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x069e4` (bl @0x00006aac)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x16bf2..0x16c1c` (42 Б); цели из: 0x16bea
- `0x16c1c..0x16c1e` (2 Б); цели из: 0x16c16
- `0x16c1e..0x16c22` (4 Б); цели из: 0x16c1a
- `0x16c22..0x16c46` (36 Б); цели из: 0x16c0c
- `0x16c46..0x16c50` (10 Б); цели из: 0x16bfe
- `0x16c50..0x16c64` (20 Б); цели из: 0x16bf0, 0x16c44
- `0x16c64..0x16c8e` (42 Б); цели из: 0x16c5c
- `0x16c8e..0x16c90` (2 Б); цели из: 0x16c88
- `0x16c90..0x16c94` (4 Б); цели из: 0x16c8c
- `0x16c94..0x16cb8` (36 Б); цели из: 0x16c7e
- `0x16cb8..0x16cc2` (10 Б); цели из: 0x16c70
- `0x16cc2..0x16cf4` (50 Б); цели из: 0x16c62, 0x16cb6
- `0x16cf4..0x16d0e` (26 Б); цели из: 0x16cd6
- `0x16d0e..0x16d3c` (46 Б); цели из: 0x16cf2
- `0x16d3c..0x16d56` (26 Б); цели из: 0x16d1e
- `0x16d56..0x16d72` (28 Б); цели из: 0x16d3a
- `0x16d72..0x16d86` (20 Б); цели из: 0x16d5a
- `0x16d86..0x16d8e` (8 Б); цели из: 0x16d70

## Дизассембляция

```asm
  16bd4:  push.w {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  16bd8:  sub sp, #0x1c                     
  16bda:  mov sl, r2                        
  16bdc:  mov fp, r3                        
  16bde:  ldrd r6, sb, [sp, #0x50]          
  16be2:  ldrsh.w r1, [sl]                  
  16be6:  ldr r0, [sp, #0x1c]               
  16be8:  cmp r1, r0                        
  16bea:  blt #0x16bf2                      
  16bec:  movs r5, #0                       
  16bee:  movs r7, #0                       
  16bf0:  b #0x16c50                        -> 0x16c50 (вне списка функций)
  16bf2:  ldr.w r0, [sb]                    
  16bf6:  ldrsh.w r1, [sl, r0, lsl #1]      
  16bfa:  ldr r0, [sp, #0x1c]               
  16bfc:  cmp r1, r0                        
  16bfe:  ble #0x16c46                      
  16c00:  ldr.w r0, [sb]                    
  16c04:  lsrs r4, r0, #1                   
  16c06:  movs r5, #0                       
  16c08:  ldr.w r7, [sb]                    
  16c0c:  b #0x16c22                        -> 0x16c22 (вне списка функций)
  16c0e:  ldrsh.w r1, [sl, r4, lsl #1]      
  16c12:  ldr r0, [sp, #0x1c]               
  16c14:  cmp r1, r0                        
  16c16:  ble #0x16c1c                      
  16c18:  mov r7, r4                        
  16c1a:  b #0x16c1e                        -> 0x16c1e (вне списка функций)
  16c1c:  mov r5, r4                        
  16c1e:  adds r0, r7, r5                   
  16c20:  lsrs r4, r0, #1                   
  16c22:  subs r0, r7, r5                   
  16c24:  cmp r0, #1                        
  16c26:  bhi #0x16c0e                      
  16c28:  adds r0, r5, #1                   
  16c2a:  ldrh.w r0, [sl, r0, lsl #1]       
  16c2e:  ldrh.w r1, [sl, r5, lsl #1]       
  16c32:  subs r0, r0, r1                   
  16c34:  uxth r1, r0                       
  16c36:  ldrh.w r2, [sl, r5, lsl #1]       
  16c3a:  ldr r0, [sp, #0x1c]               
  16c3c:  subs r0, r0, r2                   
  16c3e:  lsls r0, r0, #0x10                
  16c40:  udiv r7, r0, r1                   
  16c44:  b #0x16c50                        -> 0x16c50 (вне списка функций)
  16c46:  ldr.w r0, [sb]                    
  16c4a:  subs r5, r0, #1                   
  16c4c:  mov.w r7, #0x10000                
  16c50:  str r7, [sp, #8]                  
  16c52:  str r5, [sp, #0x10]               
  16c54:  ldr.w r1, [fp]                    
  16c58:  ldr r0, [sp, #0x20]               
  16c5a:  cmp r1, r0                        
  16c5c:  blt #0x16c64                      
  16c5e:  movs r5, #0                       
  16c60:  movs r7, #0                       
  16c62:  b #0x16cc2                        -> 0x16cc2 (вне списка функций)
  16c64:  ldr.w r0, [sb, #4]                
  16c68:  ldr.w r1, [fp, r0, lsl #2]        
  16c6c:  ldr r0, [sp, #0x20]               
  16c6e:  cmp r1, r0                        
  16c70:  ble #0x16cb8                      
  16c72:  ldr.w r0, [sb, #4]                
  16c76:  lsrs r4, r0, #1                   
  16c78:  movs r5, #0                       
  16c7a:  ldr.w r7, [sb, #4]                
  16c7e:  b #0x16c94                        -> 0x16c94 (вне списка функций)
  16c80:  ldr.w r1, [fp, r4, lsl #2]        
  16c84:  ldr r0, [sp, #0x20]               
  16c86:  cmp r1, r0                        
  16c88:  ble #0x16c8e                      
  16c8a:  mov r7, r4                        
  16c8c:  b #0x16c90                        -> 0x16c90 (вне списка функций)
  16c8e:  mov r5, r4                        
  16c90:  adds r0, r7, r5                   
  16c92:  lsrs r4, r0, #1                   
  16c94:  subs r0, r7, r5                   
  16c96:  cmp r0, #1                        
  16c98:  bhi #0x16c80                      
  16c9a:  adds r2, r5, #1                   
  16c9c:  ldr.w r2, [fp, r2, lsl #2]        
  16ca0:  ldr.w r3, [fp, r5, lsl #2]        
  16ca4:  subs r1, r2, r3                   
  16ca6:  ldr.w r3, [fp, r5, lsl #2]        
  16caa:  ldr r2, [sp, #0x20]               
  16cac:  subs r0, r2, r3                   
  16cae:  movs r2, #0x10                    
  16cb0:  bl #0x161ea                       -> func_0x161ea
  16cb4:  mov r7, r0                        
  16cb6:  b #0x16cc2                        -> 0x16cc2 (вне списка функций)
  16cb8:  ldr.w r0, [sb, #4]                
  16cbc:  subs r5, r0, #1                   
  16cbe:  mov.w r7, #0x10000                
  16cc2:  ldr r1, [sp, #0x10]               
  16cc4:  ldr r0, [sp, #0x58]               
  16cc6:  mla r4, r5, r0, r1                
  16cca:  adds r0, r4, #1                   
  16ccc:  ldrh.w r8, [r6, r0, lsl #1]       
  16cd0:  ldrh.w r0, [r6, r4, lsl #1]       
  16cd4:  cmp r0, r8                        
  16cd6:  bgt #0x16cf4                      
  16cd8:  ldrh.w r0, [r6, r4, lsl #1]       
  16cdc:  sub.w r0, r8, r0                  
  16ce0:  uxth r0, r0                       
  16ce2:  ldr r1, [sp, #8]                  
  16ce4:  muls r0, r1, r0                   
  16ce6:  ldrh.w r1, [r6, r4, lsl #1]       
  16cea:  add.w r0, r1, r0, lsr #16         
  16cee:  uxth r0, r0                       
  16cf0:  str r0, [sp, #4]                  
  16cf2:  b #0x16d0e                        -> 0x16d0e (вне списка функций)
  16cf4:  ldrh.w r0, [r6, r4, lsl #1]       
  16cf8:  sub.w r0, r0, r8                  
  16cfc:  uxth r0, r0                       
  16cfe:  ldr r1, [sp, #8]                  
  16d00:  muls r0, r1, r0                   
  16d02:  ldrh.w r1, [r6, r4, lsl #1]       
  16d06:  sub.w r0, r1, r0, lsr #16         
  16d0a:  uxth r0, r0                       
  16d0c:  str r0, [sp, #4]                  
  16d0e:  ldr r0, [sp, #0x58]               
  16d10:  add r4, r0                        
  16d12:  adds r0, r4, #1                   
  16d14:  ldrh.w r8, [r6, r0, lsl #1]       
  16d18:  ldrh.w r0, [r6, r4, lsl #1]       
  16d1c:  cmp r0, r8                        
  16d1e:  bgt #0x16d3c                      
  16d20:  ldrh.w r0, [r6, r4, lsl #1]       
  16d24:  sub.w r0, r8, r0                  
  16d28:  uxth r0, r0                       
  16d2a:  ldr r1, [sp, #8]                  
  16d2c:  muls r0, r1, r0                   
  16d2e:  ldrh.w r1, [r6, r4, lsl #1]       
  16d32:  add.w r0, r1, r0, lsr #16         
  16d36:  uxth.w r8, r0                     
  16d3a:  b #0x16d56                        -> 0x16d56 (вне списка функций)
  16d3c:  ldrh.w r0, [r6, r4, lsl #1]       
  16d40:  sub.w r0, r0, r8                  
  16d44:  uxth r0, r0                       
  16d46:  ldr r1, [sp, #8]                  
  16d48:  muls r0, r1, r0                   
  16d4a:  ldrh.w r1, [r6, r4, lsl #1]       
  16d4e:  sub.w r0, r1, r0, lsr #16         
  16d52:  uxth.w r8, r0                     
  16d56:  ldr r0, [sp, #4]                  
  16d58:  cmp r8, r0                        
  16d5a:  blt #0x16d72                      
  16d5c:  ldr r0, [sp, #4]                  
  16d5e:  sub.w r0, r8, r0                  
  16d62:  uxth r0, r0                       
  16d64:  muls r0, r7, r0                   
  16d66:  ldr r1, [sp, #4]                  
  16d68:  add.w r0, r1, r0, lsr #16         
  16d6c:  uxth r0, r0                       
  16d6e:  str r0, [sp, #0x18]               
  16d70:  b #0x16d86                        -> 0x16d86 (вне списка функций)
  16d72:  ldr r0, [sp, #4]                  
  16d74:  sub.w r0, r0, r8                  
  16d78:  uxth r0, r0                       
  16d7a:  muls r0, r7, r0                   
  16d7c:  ldr r1, [sp, #4]                  
  16d7e:  sub.w r0, r1, r0, lsr #16         
  16d82:  uxth r0, r0                       
  16d84:  str r0, [sp, #0x18]               
  16d86:  ldr r0, [sp, #0x18]               
  16d88:  add sp, #0x2c                     
  16d8a:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
```
