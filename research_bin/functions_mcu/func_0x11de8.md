# func_0x11de8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080011de8) | `0x00011de8` |
| размер кода | 1410 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x004c4b40 — прочее (r0)
- 0x080199ac — flash-mirror @0x199ac (r0)
- 0x20000000 — RAM (r0)
- 0x20000001 — RAM (r0)
- 0x20000014 — RAM (r1)
- 0x20000018 — RAM (r1)
- 0x2000001a — RAM (r1)
- 0x2000001c — RAM (r0)
- 0x2000001e — RAM (r1)
- 0x20000020 — RAM (r1)
- 0x20000022 — RAM (r1)
- 0x20000024 — RAM (r0)
- 0x20000026 — RAM (r0)
- 0x20000028 — RAM (r0)
- 0x2000002a — RAM (r0)
- 0x2000002e — RAM (r0)
- 0x2000002f — RAM (r1)
- 0x20000030 — RAM (r1)
- 0x20000035 — RAM (r1)
- 0x20000080 — RAM (r0)
- 0x200000d8 — RAM (r0)
- 0x200000ef — RAM (r0)
- 0x20000100 — RAM (r0)
- 0x20000103 — RAM (r1)
- 0x20000104 — RAM (r0)
- 0x20000107 — RAM (r0)
- 0x20000a64 — RAM (r1)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)
- 0x2000162d — RAM (r2)
- 0x40003000 — периферия (r1)
- 0x40010800 — периферия (r0)
- 0x40010c00 — периферия (r0)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)
- `func_0x01c60` (0x00001c60, bl)
- `func_0x032f4` (0x000032f4, bl)
- `func_0x0332c` (0x0000332c, bl)
- `func_0x04994` (0x00004994, bl)
- `func_0x05b98` (0x00005b98, bl)
- `func_0x05dbc` (0x00005dbc, bl)
- `func_0x087c8` (0x000087c8, bl)
- `func_0x08834` (0x00008834, bl)
- `func_0x08878` (0x00008878, bl)
- `func_0x0d878` (0x0000d878, bl)
- `func_0x110f0` (0x000110f0, bl)
- `func_0x110fc` (0x000110fc, bl)
- 0x11e2c (b, вне списка функций)
- 0x11e50 (b, вне списка функций)
- 0x11ef2 (b, вне списка функций)
- 0x11f08 (b, вне списка функций)
- 0x11fc4 (b, вне списка функций)
- 0x11ff2 (b, вне списка функций)
- 0x12060 (b, вне списка функций)
- 0x1206a (b, вне списка функций)
- 0x1206c (b, вне списка функций)
- 0x12102 (b, вне списка функций)
- 0x12114 (b, вне списка функций)
- 0x12168 (b, вне списка функций)
- 0x1216a (b, вне списка функций)
- 0x1225c (b, вне списка функций)
- 0x12294 (b, вне списка функций)
- 0x122ca (b, вне списка функций)
- 0x12346 (b, вне списка функций)
- 0x12348 (b, вне списка функций)
- 0x1235e (b, вне списка функций)
- 0x12366 (b, вне списка функций)
- `func_0x139ac` (0x000139ac, bl)
- 0x15c7c (bl, вне списка функций)
- 0x174fc (bl, вне списка функций)
- 0x17524 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x11e2c..0x11e4a` (30 Б); цели из: 0x11e28
- `0x11e4a..0x11e50` (6 Б); цели из: 0x11e1a, 0x11e2e
- `0x11e50..0x11eb0` (96 Б); цели из: 0x11e40, 0x11e48
- `0x11eb0..0x11ed6` (38 Б); цели из: 0x11e8e, 0x11e96
- `0x11ed6..0x11eee` (24 Б); цели из: 0x11ec4, 0x11ecc
- `0x11eee..0x11ef2` (4 Б); цели из: 0x11df0
- `0x11ef2..0x11f08` (22 Б); цели из: 0x11eec
- `0x11f08..0x11f5c` (84 Б); цели из: 0x11ea4, 0x11ef0
- `0x11f5c..0x11fa8` (76 Б); цели из: 0x11f28
- `0x11fa8..0x11fc4` (28 Б); цели из: 0x11f74
- `0x11fc4..0x11ff2` (46 Б); цели из: 0x11e86, 0x11ed4, 0x11f06, 0x11f3e…
- `0x11ff2..0x11ffa` (8 Б); цели из: 0x11fea
- `0x11ffa..0x1200c` (18 Б); цели из: 0x11fd0, 0x11fd8, 0x11fe0, 0x11fe8
- `0x1200c..0x1203a` (46 Б); цели из: 0x11ff8
- `0x1203a..0x1205a` (32 Б); цели из: 0x12030
- `0x1205a..0x12060` (6 Б); цели из: 0x1201c
- `0x12060..0x1206a` (10 Б); цели из: 0x12038, 0x12058
- `0x1206a..0x1206c` (2 Б); цели из: 0x1200a
- `0x1206c..0x120a8` (60 Б); цели из: 0x11ff0
- `0x120a8..0x120c0` (24 Б); цели из: 0x12084
- `0x120c0..0x120fc` (60 Б); цели из: 0x120ae, 0x120b6
- `0x120fc..0x12102` (6 Б); цели из: 0x120be
- `0x12102..0x12114` (18 Б); цели из: 0x120d0, 0x120fa
- `0x12114..0x12120` (12 Б); цели из: 0x12110
- `0x12120..0x12162` (66 Б); цели из: 0x12116
- `0x12162..0x12168` (6 Б); цели из: 0x1211e
- `0x12168..0x1216a` (2 Б); цели из: 0x120a6, 0x12130, 0x12160
- `0x1216a..0x1225c` (242 Б); цели из: 0x11fee
- `0x1225c..0x1228e` (50 Б); цели из: 0x121e2
- `0x1228e..0x12294` (6 Б); цели из: 0x121c2
- `0x12294..0x122b8` (36 Б); цели из: 0x121d6, 0x1228c
- `0x122b8..0x122ca` (18 Б); цели из: 0x122ae
- `0x122ca..0x12334` (106 Б); цели из: 0x122c6
- `0x12334..0x1233c` (8 Б); цели из: 0x122cc
- `0x1233c..0x12346` (10 Б); цели из: 0x1229a
- `0x12346..0x12348` (2 Б); цели из: 0x122de, 0x12332, 0x1233a
- `0x12348..0x1235e` (22 Б); цели из: 0x11fec
- `0x1235e..0x12366` (8 Б); цели из: 0x11eee
- `0x12366..0x1236a` (4 Б); цели из: 0x11e12, 0x11fc4, 0x1206a, 0x12168…

## Дизассембляция

```asm
  11de8:  push {r3, lr}                     
  11dea:  ldr r0, [pc, #0x3f8]              -> RAM
  11dec:  ldrb r0, [r0]                     
  11dee:  cmp r0, #5                        
  11df0:  bhs #0x11eee                      
  11df2:  tbb [pc, r0]                      
  11df6:  .byte 0x03, 0xe8                  
  11df8:  ldc2l p0, c0, [sp], #0x3ec        
  11dfc:  movs r0, #0                       
  11dfe:  ldr r1, [pc, #0x3e8]              -> RAM
  11e00:  strb r0, [r1]                     
  11e02:  bl #0x174fc                       -> 0x174fc (вне списка функций)
  11e06:  bl #0x15c7c                       -> 0x15c7c (вне списка функций)
  11e0a:  cbz r0, #0x11e14                  
  11e0c:  movs r0, #4                       
  11e0e:  ldr r1, [pc, #0x3d4]              -> RAM
  11e10:  strb r0, [r1]                     
  11e12:  b #0x12366                        -> 0x12366 (вне списка функций)
  11e14:  ldr r0, [pc, #0x3d4]              -> RAM
  11e16:  ldrb r0, [r0]                     
  11e18:  cmp r0, #1                        
  11e1a:  bne #0x11e4a                      
  11e1c:  lsls r1, r0, #8                   
  11e1e:  ldr r0, [pc, #0x3d0]              -> периферия
  11e20:  bl #0x87c8                        -> func_0x087c8
  11e24:  cbz r0, #0x11e2a                  
  11e26:  movs r0, #1                       
  11e28:  b #0x11e2c                        -> 0x11e2c (вне списка функций)
  11e2a:  movs r0, #0                       
  11e2c:  cmp r0, #1                        
  11e2e:  bne #0x11e4a                      
  11e30:  ldr r0, [pc, #0x3c0]              -> RAM
  11e32:  ldrh r0, [r0]                     
  11e34:  adds r0, r0, #1                   
  11e36:  ldr r1, [pc, #0x3bc]              -> RAM
  11e38:  strh r0, [r1]                     
  11e3a:  mov r0, r1                        
  11e3c:  ldrh r0, [r0]                     
  11e3e:  cmp r0, #4                        
  11e40:  ble #0x11e50                      
  11e42:  movs r0, #0                       
  11e44:  ldr r1, [pc, #0x3a4]              -> RAM
  11e46:  strb r0, [r1]                     
  11e48:  b #0x11e50                        -> 0x11e50 (вне списка функций)
  11e4a:  movs r0, #0                       
  11e4c:  ldr r1, [pc, #0x3a4]              -> RAM
  11e4e:  strh r0, [r1]                     
  11e50:  ldr r0, [pc, #0x3a4]              -> RAM
  11e52:  ldrb r0, [r0]                     
  11e54:  cbz r0, #0x11e88                  
  11e56:  ldr r0, [pc, #0x3a4]              -> RAM
  11e58:  ldrb r0, [r0, #1]                 
  11e5a:  cbnz r0, #0x11e88                 
  11e5c:  ldr r0, [pc, #0x39c]              -> RAM
  11e5e:  ldrb r0, [r0]                     
  11e60:  cbnz r0, #0x11e88                 
  11e62:  movs r0, #1                       
  11e64:  ldr r1, [pc, #0x394]              -> RAM
  11e66:  strb r0, [r1]                     
  11e68:  movs r0, #0                       
  11e6a:  ldr r1, [pc, #0x394]              -> RAM
  11e6c:  str r0, [r1]                      
  11e6e:  ldr r1, [pc, #0x394]              -> RAM
  11e70:  strh r0, [r1]                     
  11e72:  ldr r1, [pc, #0x394]              -> RAM
  11e74:  strh r0, [r1]                     
  11e76:  movs r0, #1                       
  11e78:  ldr r1, [pc, #0x368]              -> RAM
  11e7a:  strb r0, [r1]                     
  11e7c:  movs r0, #0                       
  11e7e:  ldr r1, [pc, #0x38c]              -> RAM
  11e80:  strb r0, [r1]                     
  11e82:  ldr r1, [pc, #0x38c]              -> RAM
  11e84:  strb r0, [r1]                     
  11e86:  b #0x11fc4                        -> 0x11fc4 (вне списка функций)
  11e88:  ldr r0, [pc, #0x388]              -> RAM
  11e8a:  ldrb r0, [r0]                     
  11e8c:  cmp r0, #1                        
  11e8e:  beq #0x11eb0                      
  11e90:  ldr r0, [pc, #0x384]              -> RAM
  11e92:  ldrb r0, [r0]                     
  11e94:  cmp r0, #1                        
  11e96:  beq #0x11eb0                      
  11e98:  ldr r0, [pc, #0x380]              -> RAM
  11e9a:  ldrb r0, [r0]                     
  11e9c:  cbnz r0, #0x11ef0                 
  11e9e:  ldr r0, [pc, #0x358]              -> RAM
  11ea0:  ldrb r0, [r0]                     
  11ea2:  cmp r0, #2                        
  11ea4:  bne #0x11f08                      
  11ea6:  ldr r0, [pc, #0x378]              -> RAM
  11ea8:  ldrb r0, [r0, #0xc]               
  11eaa:  ubfx r0, r0, #4, #1               
  11eae:  cbz r0, #0x11ef0                  
  11eb0:  ldr r0, [pc, #0x354]              -> RAM
  11eb2:  ldrh r0, [r0]                     
  11eb4:  adds r0, r0, #1                   
  11eb6:  ldr r1, [pc, #0x350]              -> RAM
  11eb8:  strh r0, [r1]                     
  11eba:  mov r0, r1                        
  11ebc:  ldrh r0, [r0]                     
  11ebe:  movw r1, #0xbb8                   
  11ec2:  cmp r0, r1                        
  11ec4:  bge #0x11ed6                      
  11ec6:  ldr r0, [pc, #0x34c]              -> RAM
  11ec8:  ldrb r0, [r0]                     
  11eca:  cmp r0, #1                        
  11ecc:  beq #0x11ed6                      
  11ece:  ldr r0, [pc, #0x348]              -> RAM
  11ed0:  ldrb r0, [r0]                     
  11ed2:  cmp r0, #1                        
  11ed4:  bne #0x11fc4                      
  11ed6:  movs r0, #0                       
  11ed8:  ldr r1, [pc, #0x324]              -> RAM
  11eda:  str r0, [r1]                      
  11edc:  ldr r1, [pc, #0x324]              -> RAM
  11ede:  strh r0, [r1]                     
  11ee0:  ldr r1, [pc, #0x324]              -> RAM
  11ee2:  strh r0, [r1]                     
  11ee4:  ldr r1, [pc, #0x32c]              -> RAM
  11ee6:  strb r0, [r1]                     
  11ee8:  ldr r1, [pc, #0x32c]              -> RAM
  11eea:  strb r0, [r1]                     
  11eec:  b #0x11ef2                        -> 0x11ef2 (вне списка функций)
  11eee:  b #0x1235e                        -> 0x1235e (вне списка функций)
  11ef0:  b #0x11f08                        -> 0x11f08 (вне списка функций)
  11ef2:  bl #0x139ac                       -> func_0x139ac
  11ef6:  bl #0xd878                        -> func_0x0d878
  11efa:  movs r0, #3                       
  11efc:  ldr r1, [pc, #0x2e4]              -> RAM
  11efe:  strb r0, [r1]                     
  11f00:  movs r0, #0                       
  11f02:  ldr r1, [pc, #0x320]              -> RAM
  11f04:  strb r0, [r1]                     
  11f06:  b #0x11fc4                        -> 0x11fc4 (вне списка функций)
  11f08:  ldr r0, [pc, #0x314]              -> RAM
  11f0a:  ldrb r0, [r0, #0xc]               
  11f0c:  ubfx r0, r0, #3, #1               
  11f10:  cbnz r0, #0x11f1c                 
  11f12:  ldr r0, [pc, #0x30c]              -> RAM
  11f14:  ldrb r0, [r0, #0xc]               
  11f16:  ubfx r0, r0, #6, #1               
  11f1a:  cbz r0, #0x11f5c                  
  11f1c:  ldr r0, [pc, #0x2fc]              -> RAM
  11f1e:  ldrb r0, [r0]                     
  11f20:  cbnz r0, #0x11f5c                 
  11f22:  ldr r0, [pc, #0x2d4]              -> RAM
  11f24:  ldrb r0, [r0]                     
  11f26:  cmp r0, #2                        
  11f28:  bne #0x11f5c                      
  11f2a:  ldr r0, [pc, #0x2d8]              -> RAM
  11f2c:  ldrh r0, [r0]                     
  11f2e:  adds r0, r0, #1                   
  11f30:  ldr r1, [pc, #0x2d0]              -> RAM
  11f32:  strh r0, [r1]                     
  11f34:  mov r0, r1                        
  11f36:  ldrh r0, [r0]                     
  11f38:  movw r1, #0x2ee0                  
  11f3c:  cmp r0, r1                        
  11f3e:  blt #0x11fc4                      
  11f40:  movs r0, #0                       
  11f42:  ldr r1, [pc, #0x2bc]              -> RAM
  11f44:  str r0, [r1]                      
  11f46:  ldr r1, [pc, #0x2bc]              -> RAM
  11f48:  strh r0, [r1]                     
  11f4a:  ldr r1, [pc, #0x2bc]              -> RAM
  11f4c:  strh r0, [r1]                     
  11f4e:  movs r0, #1                       
  11f50:  ldr r1, [pc, #0x290]              -> RAM
  11f52:  strb r0, [r1]                     
  11f54:  movs r0, #0                       
  11f56:  ldr r1, [pc, #0x2b4]              -> RAM
  11f58:  strb r0, [r1]                     
  11f5a:  b #0x11fc4                        -> 0x11fc4 (вне списка функций)
  11f5c:  bl #0x8878                        -> func_0x08878
  11f60:  cbnz r0, #0x11fa8                 
  11f62:  ldr r0, [pc, #0x298]              -> RAM
  11f64:  ldrb r0, [r0, #1]                 
  11f66:  cbnz r0, #0x11fa8                 
  11f68:  ldr r0, [pc, #0x2b0]              -> RAM
  11f6a:  ldrb r0, [r0]                     
  11f6c:  cbnz r0, #0x11fa8                 
  11f6e:  ldr r0, [pc, #0x288]              -> RAM
  11f70:  ldrb r0, [r0]                     
  11f72:  cmp r0, #2                        
  11f74:  bne #0x11fa8                      
  11f76:  ldr r0, [pc, #0x288]              -> RAM
  11f78:  ldr r0, [r0]                      
  11f7a:  adds r0, r0, #1                   
  11f7c:  ldr r1, [pc, #0x280]              -> RAM
  11f7e:  str r0, [r1]                      
  11f80:  mov r0, r1                        
  11f82:  ldr r0, [r0]                      
  11f84:  movw r1, #0xbb8                   
  11f88:  cmp r0, r1                        
  11f8a:  blo #0x11fc4                      
  11f8c:  movs r0, #0                       
  11f8e:  ldr r1, [pc, #0x270]              -> RAM
  11f90:  str r0, [r1]                      
  11f92:  ldr r1, [pc, #0x270]              -> RAM
  11f94:  strh r0, [r1]                     
  11f96:  ldr r1, [pc, #0x270]              -> RAM
  11f98:  strh r0, [r1]                     
  11f9a:  movs r0, #1                       
  11f9c:  ldr r1, [pc, #0x244]              -> RAM
  11f9e:  strb r0, [r1]                     
  11fa0:  movs r0, #0                       
  11fa2:  ldr r1, [pc, #0x268]              -> RAM
  11fa4:  strb r0, [r1]                     
  11fa6:  b #0x11fc4                        -> 0x11fc4 (вне списка функций)
  11fa8:  movs r0, #1                       
  11faa:  ldr r1, [pc, #0x250]              -> RAM
  11fac:  strb r0, [r1]                     
  11fae:  movs r0, #0                       
  11fb0:  ldr r1, [pc, #0x268]              -> RAM
  11fb2:  strb r0, [r1]                     
  11fb4:  ldr r1, [pc, #0x258]              -> RAM
  11fb6:  strb r0, [r1]                     
  11fb8:  ldr r1, [pc, #0x24c]              -> RAM
  11fba:  strh r0, [r1]                     
  11fbc:  ldr r1, [pc, #0x240]              -> RAM
  11fbe:  str r0, [r1]                      
  11fc0:  ldr r1, [pc, #0x240]              -> RAM
  11fc2:  strh r0, [r1]                     
  11fc4:  b #0x12366                        -> 0x12366 (вне списка функций)
  11fc6:  bl #0x4994                        -> func_0x04994
  11fca:  bl #0x8834                        -> func_0x08834
  11fce:  cmp r0, #1                        
  11fd0:  beq #0x11ffa                      
  11fd2:  ldr r0, [pc, #0x248]              -> RAM
  11fd4:  ldrb r0, [r0]                     
  11fd6:  cmp r0, #1                        
  11fd8:  beq #0x11ffa                      
  11fda:  ldr r0, [pc, #0x234]              -> RAM
  11fdc:  ldrb r0, [r0]                     
  11fde:  cmp r0, #1                        
  11fe0:  beq #0x11ffa                      
  11fe2:  ldr r0, [pc, #0x244]              -> RAM
  11fe4:  ldrb r0, [r0]                     
  11fe6:  cmp r0, #3                        
  11fe8:  bge #0x11ffa                      
  11fea:  b #0x11ff2                        -> 0x11ff2 (вне списка функций)
  11fec:  b #0x12348                        -> 0x12348 (вне списка функций)
  11fee:  b #0x1216a                        -> 0x1216a (вне списка функций)
  11ff0:  b #0x1206c                        -> 0x1206c (вне списка функций)
  11ff2:  ldr r0, [pc, #0x238]              -> RAM
  11ff4:  ldr r0, [r0, #4]                  
  11ff6:  cmp r0, #0xc8                     
  11ff8:  bls #0x1200c                      
  11ffa:  movs r0, #0                       
  11ffc:  ldr r1, [pc, #0x230]              -> RAM
  11ffe:  strh r0, [r1]                     
  12000:  movs r0, #2                       
  12002:  ldr r1, [pc, #0x1e0]              -> RAM
  12004:  strb r0, [r1]                     
  12006:  bl #0x32f4                        -> func_0x032f4
  1200a:  b #0x1206a                        -> 0x1206a (вне списка функций)
  1200c:  ldr r0, [pc, #0x210]              -> RAM
  1200e:  ldrb r0, [r0, #0xc]               
  12010:  ubfx r0, r0, #4, #1               
  12014:  cbnz r0, #0x1201e                 
  12016:  bl #0x17524                       -> 0x17524 (вне списка функций)
  1201a:  cmp r0, #1                        
  1201c:  bne #0x1205a                      
  1201e:  ldr r0, [pc, #0x210]              -> RAM
  12020:  ldrh r0, [r0]                     
  12022:  adds r0, r0, #1                   
  12024:  ldr r1, [pc, #0x208]              -> RAM
  12026:  strh r0, [r1]                     
  12028:  mov r0, r1                        
  1202a:  ldrh r0, [r0]                     
  1202c:  cmp.w r0, #0x1f4                  
  12030:  bge #0x1203a                      
  12032:  bl #0x17524                       -> 0x17524 (вне списка функций)
  12036:  cmp r0, #1                        
  12038:  bne #0x12060                      
  1203a:  bl #0x5b98                        -> func_0x05b98
  1203e:  movs r0, #0                       
  12040:  ldr r1, [pc, #0x1ec]              -> RAM
  12042:  strh r0, [r1]                     
  12044:  bl #0x139ac                       -> func_0x139ac
  12048:  bl #0xd878                        -> func_0x0d878
  1204c:  movs r0, #3                       
  1204e:  ldr r1, [pc, #0x194]              -> RAM
  12050:  strb r0, [r1]                     
  12052:  movs r0, #0                       
  12054:  ldr r1, [pc, #0x1cc]              -> RAM
  12056:  strb r0, [r1]                     
  12058:  b #0x12060                        -> 0x12060 (вне списка функций)
  1205a:  movs r0, #0                       
  1205c:  ldr r1, [pc, #0x1d0]              -> RAM
  1205e:  strh r0, [r1]                     
  12060:  movs r0, #0                       
  12062:  ldr r1, [pc, #0x1c4]              -> RAM
  12064:  strb r0, [r1]                     
  12066:  bl #0x110fc                       -> func_0x110fc
  1206a:  b #0x12366                        -> 0x12366 (вне списка функций)
  1206c:  movs r0, #2                       
  1206e:  ldr r1, [pc, #0x178]              -> RAM
  12070:  strb r0, [r1]                     
  12072:  ldr r0, [pc, #0x1c0]              -> RAM
  12074:  ldrh r0, [r0]                     
  12076:  adds r0, r0, #1                   
  12078:  ldr r1, [pc, #0x1b8]              -> RAM
  1207a:  strh r0, [r1]                     
  1207c:  mov r0, r1                        
  1207e:  ldrh r0, [r0]                     
  12080:  cmp.w r0, #0x1f4                  
  12084:  blt #0x120a8                      
  12086:  movs r0, #0                       
  12088:  strh r0, [r1]                     
  1208a:  ldr r1, [pc, #0x1ac]              -> RAM
  1208c:  strh r0, [r1]                     
  1208e:  ldr r1, [pc, #0x1ac]              -> RAM
  12090:  strh r0, [r1]                     
  12092:  movs r0, #1                       
  12094:  ldr r1, [pc, #0x14c]              -> RAM
  12096:  strb r0, [r1]                     
  12098:  movs r0, #0                       
  1209a:  ldr r1, [pc, #0x170]              -> RAM
  1209c:  strb r0, [r1]                     
  1209e:  ldr r1, [pc, #0x17c]              -> RAM
  120a0:  strb r0, [r1]                     
  120a2:  ldr r1, [pc, #0x184]              -> RAM
  120a4:  strb r0, [r1]                     
  120a6:  b #0x12168                        -> 0x12168 (вне списка функций)
  120a8:  ldr r0, [pc, #0x164]              -> RAM
  120aa:  ldrb r0, [r0]                     
  120ac:  cmp r0, #1                        
  120ae:  beq #0x120c0                      
  120b0:  ldr r0, [pc, #0x174]              -> RAM
  120b2:  ldrb r0, [r0]                     
  120b4:  cmp r0, #3                        
  120b6:  bge #0x120c0                      
  120b8:  ldr r0, [pc, #0x170]              -> RAM
  120ba:  ldr r0, [r0, #4]                  
  120bc:  cmp r0, #0xc8                     
  120be:  bls #0x120fc                      
  120c0:  ldr r0, [pc, #0x174]              -> RAM
  120c2:  ldrh r0, [r0]                     
  120c4:  adds r0, r0, #1                   
  120c6:  ldr r1, [pc, #0x170]              -> RAM
  120c8:  strh r0, [r1]                     
  120ca:  mov r0, r1                        
  120cc:  ldrh r0, [r0]                     
  120ce:  cmp r0, #4                        
  120d0:  blt #0x12102                      
  120d2:  movs r0, #0                       
  120d4:  ldr r1, [pc, #0x114]              -> RAM
  120d6:  strb r0, [r1]                     
  120d8:  ldr r1, [pc, #0x158]              -> RAM
  120da:  strh r0, [r1]                     
  120dc:  ldr r1, [pc, #0x158]              -> RAM
  120de:  strh r0, [r1]                     
  120e0:  ldr r1, [pc, #0x158]              -> RAM
  120e2:  strh r0, [r1]                     
  120e4:  bl #0x5dbc                        -> func_0x05dbc
  120e8:  movs r0, #0                       
  120ea:  ldr r1, [pc, #0x124]              -> RAM
  120ec:  strb r0, [r1]                     
  120ee:  ldr r1, [pc, #0x12c]              -> RAM
  120f0:  strb r0, [r1]                     
  120f2:  ldr r1, [pc, #0x134]              -> RAM
  120f4:  strb r0, [r1]                     
  120f6:  ldr r1, [pc, #0xec]               -> RAM
  120f8:  strb r0, [r1]                     
  120fa:  b #0x12102                        -> 0x12102 (вне списка функций)
  120fc:  movs r0, #0                       
  120fe:  ldr r1, [pc, #0x138]              -> RAM
  12100:  strh r0, [r1]                     
  12102:  mov.w r1, #0x200                  
  12106:  ldr r0, [pc, #0x138]              -> периферия
  12108:  bl #0x87c8                        -> func_0x087c8
  1210c:  cbnz r0, #0x12112                 
  1210e:  movs r0, #1                       
  12110:  b #0x12114                        -> 0x12114 (вне списка функций)
  12112:  movs r0, #0                       
  12114:  cmp r0, #1                        
  12116:  beq #0x12120                      
  12118:  ldr r0, [pc, #0x128]              -> RAM
  1211a:  ldrb r0, [r0]                     
  1211c:  cmp r0, #1                        
  1211e:  bne #0x12162                      
  12120:  ldr r0, [pc, #0x118]              -> RAM
  12122:  ldrh r0, [r0]                     
  12124:  adds r0, r0, #1                   
  12126:  ldr r1, [pc, #0x114]              -> RAM
  12128:  strh r0, [r1]                     
  1212a:  mov r0, r1                        
  1212c:  ldrh r0, [r0]                     
  1212e:  cmp r0, #5                        
  12130:  blt #0x12168                      
  12132:  movs r0, #1                       
  12134:  ldr r1, [pc, #0x110]              -> RAM
  12136:  strb r0, [r1]                     
  12138:  ldr r1, [pc, #0xb0]               -> RAM
  1213a:  strb r0, [r1]                     
  1213c:  movs r0, #0                       
  1213e:  ldr r1, [pc, #0xf4]               -> RAM
  12140:  strh r0, [r1]                     
  12142:  ldr r1, [pc, #0xf4]               -> RAM
  12144:  strh r0, [r1]                     
  12146:  ldr r1, [pc, #0xf4]               -> RAM
  12148:  strh r0, [r1]                     
  1214a:  bl #0x5dbc                        -> func_0x05dbc
  1214e:  movs r0, #0                       
  12150:  ldr r1, [pc, #0xbc]               -> RAM
  12152:  strb r0, [r1]                     
  12154:  ldr r1, [pc, #0xc4]               -> RAM
  12156:  strb r0, [r1]                     
  12158:  ldr r1, [pc, #0xcc]               -> RAM
  1215a:  strb r0, [r1]                     
  1215c:  ldr r1, [pc, #0x84]               -> RAM
  1215e:  strb r0, [r1]                     
  12160:  b #0x12168                        -> 0x12168 (вне списка функций)
  12162:  movs r0, #0                       
  12164:  ldr r1, [pc, #0xd4]               -> RAM
  12166:  strh r0, [r1]                     
  12168:  b #0x12366                        -> 0x12366 (вне списка функций)
  1216a:  movs r0, #5                       
  1216c:  ldr r1, [pc, #0x78]               -> RAM
  1216e:  strb r0, [r1]                     
  12170:  bl #0x110f0                       -> func_0x110f0
  12174:  movw r0, #0xaaaa                  
  12178:  ldr r1, [pc, #0xd0]               -> периферия
  1217a:  str r0, [r1]                      
  1217c:  movs r1, #2                       
  1217e:  ldr r0, [pc, #0xd0]               -> flash-mirror @0x199ac
  12180:  bl #0x332c                        -> func_0x0332c
  12184:  movs r0, #0x9f                    
  12186:  bl #0x1bdc                        -> func_0x01bdc
  1218a:  movw r0, #0x2710                  
  1218e:  str r0, [sp]                      
  12190:  nop                               
  12192:  ldr r0, [sp]                      
  12194:  subs r1, r0, #1                   
  12196:  str r1, [sp]                      
  12198:  cmp r0, #0                        
  1219a:  bne #0x12192                      
  1219c:  movs r3, #2                       
  1219e:  ldr r2, [pc, #0xb4]               -> RAM
  121a0:  movs r1, #0x38                    
  121a2:  movs r0, #8                       
  121a4:  bl #0x1c60                        -> func_0x01c60
  121a8:  movw r0, #0x2710                  
  121ac:  str r0, [sp]                      
  121ae:  nop                               
  121b0:  ldr r0, [sp]                      
  121b2:  subs r1, r0, #1                   
  121b4:  str r1, [sp]                      
  121b6:  cmp r0, #0                        
  121b8:  bne #0x121b0                      
  121ba:  ldr r0, [pc, #0x98]               -> RAM
  121bc:  subs r0, #0x36                    
  121be:  ldrh r0, [r0, #0x36]              
  121c0:  cmp r0, #0x28                     
  121c2:  bge #0x1228e                      
  121c4:  ldr r0, [pc, #0x90]               -> RAM
  121c6:  ldrh r0, [r0]                     
  121c8:  adds r0, r0, #1                   
  121ca:  ldr r1, [pc, #0x8c]               -> RAM
  121cc:  strh r0, [r1]                     
  121ce:  mov r0, r1                        
  121d0:  ldrh r0, [r0]                     
  121d2:  cmp.w r0, #0x1f4                  
  121d6:  ble #0x12294                      
  121d8:  movs r0, #0                       
  121da:  strh r0, [r1]                     
  121dc:  movs r0, #2                       
  121de:  ldr r1, [pc, #0x60]               -> периферия
  121e0:  adds r1, #0x18                    
  121e2:  b #0x1225c                        -> 0x1225c (вне списка функций)
  121e4:  movs r6, r5                       
  121e6:  movs r0, #0                       
  121e8:  movs r5, r6                       
  121ea:  movs r0, #0                       
  121ec:  movs r1, r0                       
  121ee:  movs r0, #0                       
  121f0:  lsrs r0, r0, #0x20                
  121f2:  ands r1, r0                       
  121f4:  movs r4, r4                       
  121f6:  movs r0, #0                       
  121f8:  lsls r0, r0, #2                   
  121fa:  movs r0, #0                       
  121fc:  lsls r0, r3, #3                   
  121fe:  movs r0, #0                       
  12200:  movs r4, r2                       
  12202:  movs r0, #0                       
  12204:  movs r0, r3                       
  12206:  movs r0, #0                       
  12208:  movs r2, r3                       
  1220a:  movs r0, #0                       
  1220c:  movs r7, r5                       
  1220e:  movs r0, #0                       
  12210:  lsls r3, r0, #4                   
  12212:  movs r0, #0                       
  12214:  movs r0, r0                       
  12216:  movs r0, #0                       
  12218:  lsls r7, r5, #3                   
  1221a:  movs r0, #0                       
  1221c:  lsls r0, r0, #4                   
  1221e:  movs r0, #0                       
  12220:  lsrs r5, r2, #0x1e                
  12222:  movs r0, #0                       
  12224:  movs r0, r6                       
  12226:  movs r0, #0                       
  12228:  lsls r4, r0, #4                   
  1222a:  movs r0, #0                       
  1222c:  lsrs r3, r7, #0x1e                
  1222e:  movs r0, #0                       
  12230:  movs r6, r3                       
  12232:  movs r0, #0                       
  12234:  movs r4, r3                       
  12236:  movs r0, #0                       
  12238:  movs r0, r4                       
  1223a:  movs r0, #0                       
  1223c:  movs r2, r4                       
  1223e:  movs r0, #0                       
  12240:  lsrs r0, r0, #0x10                
  12242:  ands r1, r0                       
  12244:  lsls r7, r0, #4                   
  12246:  movs r0, #0                       
  12248:  lsrs r4, r4, #9                   
  1224a:  movs r0, #0                       
  1224c:  adds r0, #0                       
  1224e:  ands r0, r0                       
  12250:  ldr r1, [sp, #0x2b0]              
  12252:  lsrs r1, r0, #0x20                
  12254:  asrs r5, r5, #0x18                
  12256:  movs r0, #0                       
  12258:  movs r6, r4                       
  1225a:  movs r0, #0                       
  1225c:  str r0, [r1]                      
  1225e:  ldr r0, [pc, #0x10c]              
  12260:  str r0, [sp]                      
  12262:  nop                               
  12264:  ldr r0, [sp]                      
  12266:  subs r1, r0, #1                   
  12268:  str r1, [sp]                      
  1226a:  cmp r0, #0                        
  1226c:  bne #0x12264                      
  1226e:  movs r0, #0x10                    
  12270:  bl #0x1bdc                        -> func_0x01bdc
  12274:  movw r0, #0x2710                  
  12278:  str r0, [sp]                      
  1227a:  nop                               
  1227c:  ldr r0, [sp]                      
  1227e:  subs r1, r0, #1                   
  12280:  str r1, [sp]                      
  12282:  cmp r0, #0                        
  12284:  bne #0x1227c                      
  12286:  movs r0, #0x10                    
  12288:  bl #0x1bdc                        -> func_0x01bdc
  1228c:  b #0x12294                        -> 0x12294 (вне списка функций)
  1228e:  movs r0, #0                       
  12290:  ldr r1, [pc, #0xdc]               -> RAM
  12292:  strh r0, [r1]                     
  12294:  ldr r0, [pc, #0xdc]               -> RAM
  12296:  ldrb r0, [r0]                     
  12298:  cmp r0, #1                        
  1229a:  bne #0x1233c                      
  1229c:  ldr r0, [pc, #0xd8]               -> RAM
  1229e:  ldrh r0, [r0]                     
  122a0:  adds r0, r0, #1                   
  122a2:  ldr r1, [pc, #0xd4]               -> RAM
  122a4:  strh r0, [r1]                     
  122a6:  mov r0, r1                        
  122a8:  ldrh r0, [r0]                     
  122aa:  cmp.w r0, #0x1f4                  
  122ae:  ble #0x122b8                      
  122b0:  movs r0, #0                       
  122b2:  strh r0, [r1]                     
  122b4:  ldr r1, [pc, #0xbc]               -> RAM
  122b6:  strb r0, [r1]                     
  122b8:  mov.w r1, #0x200                  
  122bc:  ldr r0, [pc, #0xbc]               -> периферия
  122be:  bl #0x87c8                        -> func_0x087c8
  122c2:  cbnz r0, #0x122c8                 
  122c4:  movs r0, #1                       
  122c6:  b #0x122ca                        -> 0x122ca (вне списка функций)
  122c8:  movs r0, #0                       
  122ca:  cmp r0, #1                        
  122cc:  bne #0x12334                      
  122ce:  ldr r0, [pc, #0xb0]               -> RAM
  122d0:  ldrh r0, [r0]                     
  122d2:  adds r0, r0, #1                   
  122d4:  ldr r1, [pc, #0xa8]               -> RAM
  122d6:  strh r0, [r1]                     
  122d8:  mov r0, r1                        
  122da:  ldrh r0, [r0]                     
  122dc:  cmp r0, #5                        
  122de:  blt #0x12346                      
  122e0:  movs r0, #0                       
  122e2:  strh r0, [r1]                     
  122e4:  ldr r1, [pc, #0x8c]               -> RAM
  122e6:  strb r0, [r1]                     
  122e8:  bl #0x5dbc                        -> func_0x05dbc
  122ec:  movs r0, #0                       
  122ee:  ldr r1, [pc, #0x94]               -> RAM
  122f0:  strb r0, [r1]                     
  122f2:  movs r0, #2                       
  122f4:  ldr r1, [pc, #0x84]               -> периферия
  122f6:  adds r1, #0x18                    
  122f8:  str r0, [r1]                      
  122fa:  movw r0, #0x2710                  
  122fe:  str r0, [sp]                      
  12300:  nop                               
  12302:  ldr r0, [sp]                      
  12304:  subs r1, r0, #1                   
  12306:  str r1, [sp]                      
  12308:  cmp r0, #0                        
  1230a:  bne #0x12302                      
  1230c:  movs r0, #2                       
  1230e:  ldr r1, [pc, #0x6c]               -> периферия
  12310:  adds r1, #0x28                    
  12312:  str r0, [r1]                      
  12314:  movs r0, #0x12                    
  12316:  bl #0x1bdc                        -> func_0x01bdc
  1231a:  movw r0, #0x2710                  
  1231e:  str r0, [sp]                      
  12320:  nop                               
  12322:  ldr r0, [sp]                      
  12324:  subs r1, r0, #1                   
  12326:  str r1, [sp]                      
  12328:  cmp r0, #0                        
  1232a:  bne #0x12322                      
  1232c:  movs r0, #0x12                    
  1232e:  bl #0x1bdc                        -> func_0x01bdc
  12332:  b #0x12346                        -> 0x12346 (вне списка функций)
  12334:  movs r0, #0                       
  12336:  ldr r1, [pc, #0x48]               -> RAM
  12338:  strh r0, [r1]                     
  1233a:  b #0x12346                        -> 0x12346 (вне списка функций)
  1233c:  movs r0, #0                       
  1233e:  ldr r1, [pc, #0x38]               -> RAM
  12340:  strh r0, [r1]                     
  12342:  ldr r1, [pc, #0x3c]               -> RAM
  12344:  strh r0, [r1]                     
  12346:  b #0x12366                        -> 0x12366 (вне списка функций)
  12348:  movs r0, #4                       
  1234a:  ldr r1, [pc, #0x3c]               -> RAM
  1234c:  strb r0, [r1]                     
  1234e:  bl #0x15c7c                       -> 0x15c7c (вне списка функций)
  12352:  cbnz r0, #0x1235c                 
  12354:  movs r0, #0                       
  12356:  ldr r1, [pc, #0x2c]               -> RAM
  12358:  strb r0, [r1]                     
  1235a:  b #0x12366                        -> 0x12366 (вне списка функций)
  1235c:  b #0x12366                        -> 0x12366 (вне списка функций)
  1235e:  movs r0, #0                       
  12360:  ldr r1, [pc, #0x20]               -> RAM
  12362:  strb r0, [r1]                     
  12364:  nop                               
  12366:  nop                               
  12368:  pop {r3, pc}                      
  ; --- literal-пул @0x121e4 (30 слов) ---
  121e4:  .word 0x2000002e  ; RAM
  121e8:  .word 0x20000035  ; RAM
  121ec:  .word 0x20000001  ; RAM
  121f0:  .word 0x40010800  ; периферия
  121f4:  .word 0x20000024  ; RAM
  121f8:  .word 0x20000080  ; RAM
  121fc:  .word 0x200000d8  ; RAM
  12200:  .word 0x20000014  ; RAM
  12204:  .word 0x20000018  ; RAM
  12208:  .word 0x2000001a  ; RAM
  1220c:  .word 0x2000002f  ; RAM
  12210:  .word 0x20000103  ; RAM
  12214:  .word 0x20000000  ; RAM
  12218:  .word 0x200000ef  ; RAM
  1221c:  .word 0x20000100  ; RAM
  12220:  .word 0x20000f95  ; RAM
  12224:  .word 0x20000030  ; RAM
  12228:  .word 0x20000104  ; RAM
  1222c:  .word 0x20000fbb  ; RAM
  12230:  .word 0x2000001e  ; RAM
  12234:  .word 0x2000001c  ; RAM
  12238:  .word 0x20000020  ; RAM
  1223c:  .word 0x20000022  ; RAM
  12240:  .word 0x40010c00  ; периферия
  12244:  .word 0x20000107  ; RAM
  12248:  .word 0x20000a64  ; RAM
  1224c:  .word 0x40003000  ; периферия
  12250:  .word 0x080199ac  ; flash-mirror @0x199ac
  12254:  .word 0x2000162d  ; RAM
  12258:  .word 0x20000026  ; RAM
  ; --- literal-пул @0x1236c (8 слов) — ВНЕ границ функции ---
  1236c:  .word 0x004c4b40
  12370:  .word 0x20000026  ; RAM
  12374:  .word 0x20000100  ; RAM
  12378:  .word 0x2000002a  ; RAM
  1237c:  .word 0x40010c00  ; периферия
  12380:  .word 0x20000028  ; RAM
  12384:  .word 0x2000002e  ; RAM
  12388:  .word 0x20000035  ; RAM
```
