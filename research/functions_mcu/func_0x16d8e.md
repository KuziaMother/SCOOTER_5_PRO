# func_0x16d8e

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080016d8e) | `0x00016d8e` |
| размер кода | 436 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x161ea` (0x000161ea, bl)
- 0x16ddc (b, вне списка функций)
- 0x16de2 (b, вне списка функций)
- 0x16e16 (b, вне списка функций)
- 0x16e5e (b, вне списка функций)
- 0x16e64 (b, вне списка функций)
- 0x16e98 (b, вне списка функций)
- 0x16ed8 (b, вне списка функций)
- 0x16f10 (b, вне списка функций)
- 0x16f3a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e2cc` (bl @0x0000e2f0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x16dae..0x16dda` (44 Б); цели из: 0x16da4
- `0x16dda..0x16ddc` (2 Б); цели из: 0x16dd4
- `0x16ddc..0x16de2` (6 Б); цели из: 0x16dd8
- `0x16de2..0x16e0a` (40 Б); цели из: 0x16dca
- `0x16e0a..0x16e16` (12 Б); цели из: 0x16dba
- `0x16e16..0x16e30` (26 Б); цели из: 0x16dac, 0x16e08
- `0x16e30..0x16e5c` (44 Б); цели из: 0x16e26
- `0x16e5c..0x16e5e` (2 Б); цели из: 0x16e56
- `0x16e5e..0x16e64` (6 Б); цели из: 0x16e5a
- `0x16e64..0x16e8c` (40 Б); цели из: 0x16e4c
- `0x16e8c..0x16e98` (12 Б); цели из: 0x16e3c
- `0x16e98..0x16ec2` (42 Б); цели из: 0x16e2e, 0x16e8a
- `0x16ec2..0x16ed8` (22 Б); цели из: 0x16ea8
- `0x16ed8..0x16efc` (36 Б); цели из: 0x16ec0
- `0x16efc..0x16f10` (20 Б); цели из: 0x16ee4
- `0x16f10..0x16f28` (24 Б); цели из: 0x16efa
- `0x16f28..0x16f3a` (18 Б); цели из: 0x16f12
- `0x16f3a..0x16f42` (8 Б); цели из: 0x16f26

## Дизассембляция

```asm
  16d8e:  push.w {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  16d92:  sub sp, #0x1c                     
  16d94:  mov sb, r2                        
  16d96:  mov sl, r3                        
  16d98:  ldrd r6, r8, [sp, #0x50]          
  16d9c:  ldr.w r1, [sb]                    
  16da0:  ldr r0, [sp, #0x1c]               
  16da2:  cmp r1, r0                        
  16da4:  blt #0x16dae                      
  16da6:  movs r5, #0                       
  16da8:  movs r0, #0                       
  16daa:  str r0, [sp, #0x14]               
  16dac:  b #0x16e16                        -> 0x16e16 (вне списка функций)
  16dae:  ldr.w r0, [r8]                    
  16db2:  ldr.w r1, [sb, r0, lsl #2]        
  16db6:  ldr r0, [sp, #0x1c]               
  16db8:  cmp r1, r0                        
  16dba:  ble #0x16e0a                      
  16dbc:  ldr.w r0, [r8]                    
  16dc0:  lsrs r4, r0, #1                   
  16dc2:  movs r5, #0                       
  16dc4:  ldr.w r0, [r8]                    
  16dc8:  str r0, [sp, #4]                  
  16dca:  b #0x16de2                        -> 0x16de2 (вне списка функций)
  16dcc:  ldr.w r1, [sb, r4, lsl #2]        
  16dd0:  ldr r0, [sp, #0x1c]               
  16dd2:  cmp r1, r0                        
  16dd4:  ble #0x16dda                      
  16dd6:  str r4, [sp, #4]                  
  16dd8:  b #0x16ddc                        -> 0x16ddc (вне списка функций)
  16dda:  mov r5, r4                        
  16ddc:  ldr r0, [sp, #4]                  
  16dde:  add r0, r5                        
  16de0:  lsrs r4, r0, #1                   
  16de2:  ldr r0, [sp, #4]                  
  16de4:  subs r0, r0, r5                   
  16de6:  cmp r0, #1                        
  16de8:  bhi #0x16dcc                      
  16dea:  adds r2, r5, #1                   
  16dec:  ldr.w r2, [sb, r2, lsl #2]        
  16df0:  ldr.w r3, [sb, r5, lsl #2]        
  16df4:  subs r1, r2, r3                   
  16df6:  ldr.w r3, [sb, r5, lsl #2]        
  16dfa:  ldr r2, [sp, #0x1c]               
  16dfc:  subs r0, r2, r3                   
  16dfe:  movs r2, #8                       
  16e00:  bl #0x161ea                       -> func_0x161ea
  16e04:  uxth r0, r0                       
  16e06:  str r0, [sp, #0x14]               
  16e08:  b #0x16e16                        -> 0x16e16 (вне списка функций)
  16e0a:  ldr.w r0, [r8]                    
  16e0e:  subs r5, r0, #1                   
  16e10:  mov.w r0, #0x100                  
  16e14:  str r0, [sp, #0x14]               
  16e16:  ldr r0, [sp, #0x14]               
  16e18:  strh.w r0, [sp, #8]               
  16e1c:  str r5, [sp, #0xc]                
  16e1e:  ldr.w r1, [sl]                    
  16e22:  ldr r0, [sp, #0x20]               
  16e24:  cmp r1, r0                        
  16e26:  blt #0x16e30                      
  16e28:  movs r5, #0                       
  16e2a:  movs r0, #0                       
  16e2c:  str r0, [sp, #0x14]               
  16e2e:  b #0x16e98                        -> 0x16e98 (вне списка функций)
  16e30:  ldr.w r0, [r8, #4]                
  16e34:  ldr.w r1, [sl, r0, lsl #2]        
  16e38:  ldr r0, [sp, #0x20]               
  16e3a:  cmp r1, r0                        
  16e3c:  ble #0x16e8c                      
  16e3e:  ldr.w r0, [r8, #4]                
  16e42:  lsrs r4, r0, #1                   
  16e44:  movs r5, #0                       
  16e46:  ldr.w r0, [r8, #4]                
  16e4a:  str r0, [sp, #4]                  
  16e4c:  b #0x16e64                        -> 0x16e64 (вне списка функций)
  16e4e:  ldr.w r1, [sl, r4, lsl #2]        
  16e52:  ldr r0, [sp, #0x20]               
  16e54:  cmp r1, r0                        
  16e56:  ble #0x16e5c                      
  16e58:  str r4, [sp, #4]                  
  16e5a:  b #0x16e5e                        -> 0x16e5e (вне списка функций)
  16e5c:  mov r5, r4                        
  16e5e:  ldr r0, [sp, #4]                  
  16e60:  add r0, r5                        
  16e62:  lsrs r4, r0, #1                   
  16e64:  ldr r0, [sp, #4]                  
  16e66:  subs r0, r0, r5                   
  16e68:  cmp r0, #1                        
  16e6a:  bhi #0x16e4e                      
  16e6c:  adds r2, r5, #1                   
  16e6e:  ldr.w r2, [sl, r2, lsl #2]        
  16e72:  ldr.w r3, [sl, r5, lsl #2]        
  16e76:  subs r1, r2, r3                   
  16e78:  ldr.w r3, [sl, r5, lsl #2]        
  16e7c:  ldr r2, [sp, #0x20]               
  16e7e:  subs r0, r2, r3                   
  16e80:  movs r2, #8                       
  16e82:  bl #0x161ea                       -> func_0x161ea
  16e86:  uxth r0, r0                       
  16e88:  str r0, [sp, #0x14]               
  16e8a:  b #0x16e98                        -> 0x16e98 (вне списка функций)
  16e8c:  ldr.w r0, [r8, #4]                
  16e90:  subs r5, r0, #1                   
  16e92:  mov.w r0, #0x100                  
  16e96:  str r0, [sp, #0x14]               
  16e98:  ldr r1, [sp, #0xc]                
  16e9a:  ldr r0, [sp, #0x58]               
  16e9c:  mla r4, r5, r0, r1                
  16ea0:  adds r0, r4, #1                   
  16ea2:  ldrb r7, [r6, r0]                 
  16ea4:  ldrb r0, [r6, r4]                 
  16ea6:  cmp r0, r7                        
  16ea8:  bgt #0x16ec2                      
  16eaa:  ldrb r0, [r6, r4]                 
  16eac:  subs r0, r7, r0                   
  16eae:  uxtb r0, r0                       
  16eb0:  ldrh.w r1, [sp, #8]               
  16eb4:  muls r0, r1, r0                   
  16eb6:  ldrb r1, [r6, r4]                 
  16eb8:  add.w r0, r1, r0, lsr #8          
  16ebc:  and fp, r0, #0xff                 
  16ec0:  b #0x16ed8                        -> 0x16ed8 (вне списка функций)
  16ec2:  ldrb r0, [r6, r4]                 
  16ec4:  subs r0, r0, r7                   
  16ec6:  uxtb r0, r0                       
  16ec8:  ldrh.w r1, [sp, #8]               
  16ecc:  muls r0, r1, r0                   
  16ece:  ldrb r1, [r6, r4]                 
  16ed0:  sub.w r0, r1, r0, lsr #8          
  16ed4:  and fp, r0, #0xff                 
  16ed8:  ldr r0, [sp, #0x58]               
  16eda:  add r4, r0                        
  16edc:  adds r0, r4, #1                   
  16ede:  ldrb r7, [r6, r0]                 
  16ee0:  ldrb r0, [r6, r4]                 
  16ee2:  cmp r0, r7                        
  16ee4:  bgt #0x16efc                      
  16ee6:  ldrb r0, [r6, r4]                 
  16ee8:  subs r0, r7, r0                   
  16eea:  uxtb r0, r0                       
  16eec:  ldrh.w r1, [sp, #8]               
  16ef0:  muls r0, r1, r0                   
  16ef2:  ldrb r1, [r6, r4]                 
  16ef4:  add.w r0, r1, r0, lsr #8          
  16ef8:  uxtb r7, r0                       
  16efa:  b #0x16f10                        -> 0x16f10 (вне списка функций)
  16efc:  ldrb r0, [r6, r4]                 
  16efe:  subs r0, r0, r7                   
  16f00:  uxtb r0, r0                       
  16f02:  ldrh.w r1, [sp, #8]               
  16f06:  muls r0, r1, r0                   
  16f08:  ldrb r1, [r6, r4]                 
  16f0a:  sub.w r0, r1, r0, lsr #8          
  16f0e:  uxtb r7, r0                       
  16f10:  cmp r7, fp                        
  16f12:  blt #0x16f28                      
  16f14:  sub.w r0, r7, fp                  
  16f18:  uxtb r0, r0                       
  16f1a:  ldr r1, [sp, #0x14]               
  16f1c:  muls r0, r1, r0                   
  16f1e:  add.w r0, fp, r0, lsr #8          
  16f22:  uxtb r0, r0                       
  16f24:  str r0, [sp, #0x18]               
  16f26:  b #0x16f3a                        -> 0x16f3a (вне списка функций)
  16f28:  sub.w r0, fp, r7                  
  16f2c:  uxtb r0, r0                       
  16f2e:  ldr r1, [sp, #0x14]               
  16f30:  muls r0, r1, r0                   
  16f32:  sub.w r0, fp, r0, lsr #8          
  16f36:  uxtb r0, r0                       
  16f38:  str r0, [sp, #0x18]               
  16f3a:  ldr r0, [sp, #0x18]               
  16f3c:  add sp, #0x2c                     
  16f3e:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
```
