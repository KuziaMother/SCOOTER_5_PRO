# func_0x03f00

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003f00) | `0x00003f00` |
| размер кода | 912 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000008a — RAM (r0)
- 0x200009b4 — RAM (r0)
- 0x200009b5 — RAM (r1)
- 0x200009bc — RAM (r1)
- 0x200009bd — RAM (r0)
- 0x200009be — RAM (r0)
- 0x20000c89 — RAM (r0)
- 0x20000fe7 — RAM (r1)
- 0x20001222 — RAM (r0)
- 0x20001232 — RAM (r3)

## Вызовы (callees)

- 0x01180 (bl, вне списка функций)
- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x02b2c` (0x00002b2c, bl)
- `func_0x030a6` (0x000030a6, bl)
- `func_0x03b42` (0x00003b42, bl)
- 0x03f68 (b, вне списка функций)
- 0x03fb6 (b, вне списка функций)
- 0x04004 (b, вне списка функций)
- 0x0406a (b, вне списка функций)
- 0x0407c (b, вне списка функций)
- 0x040ca (b, вне списка функций)
- 0x04154 (b, вне списка функций)
- 0x041e8 (b, вне списка функций)
- 0x041ea (b, вне списка функций)
- 0x041ec (b, вне списка функций)
- `func_0x0dd2c` (0x0000dd2c, bl)
- `func_0x13284` (0x00013284, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03de4` (bl @0x00003e46)
- `func_0x03de4` (bl @0x00003ec8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x03f62..0x03f68` (6 Б); цели из: 0x03f4a
- `0x03f68..0x03f86` (30 Б); цели из: 0x03f60
- `0x03f86..0x03fb6` (48 Б); цели из: 0x03f70
- `0x03fb6..0x03fd4` (30 Б); цели из: 0x03f84, 0x03f8c
- `0x03fd4..0x04004` (48 Б); цели из: 0x03fbe
- `0x04004..0x04022` (30 Б); цели из: 0x03fd2, 0x03fda
- `0x04022..0x04024` (2 Б); цели из: 0x03f2e
- `0x04024..0x0406a` (70 Б); цели из: 0x0400c
- `0x0406a..0x0407c` (18 Б); цели из: 0x04052
- `0x0407c..0x0409a` (30 Б); цели из: 0x04020, 0x0402a
- `0x0409a..0x040ca` (48 Б); цели из: 0x04084
- `0x040ca..0x040e8` (30 Б); цели из: 0x04098, 0x040a0
- `0x040e8..0x04126` (62 Б); цели из: 0x040d2
- `0x04126..0x04154` (46 Б); цели из: 0x0411e
- `0x04154..0x041e8` (148 Б); цели из: 0x04124
- `0x041e8..0x041ea` (2 Б); цели из: 0x040e6, 0x040ee
- `0x041ea..0x041ec` (2 Б); цели из: 0x04022
- `0x041ec..0x04220` (52 Б); цели из: 0x03f68, 0x03fb6, 0x04004, 0x0407c…
- `0x04220..0x0424c` (44 Б); цели из: 0x0421a
- `0x0424c..0x0428a` (62 Б); цели из: 0x0423c
- `0x0428a..0x04290` (6 Б); цели из: 0x041f2

## Дизассембляция

```asm
  03f00:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  03f04:  sub sp, #0x50                     
  03f06:  movs r1, #0x28                    
  03f08:  add r0, sp, #0x28                 
  03f0a:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  03f0e:  movs r4, #0                       
  03f10:  mov sb, r4                        
  03f12:  movs r6, #0                       
  03f14:  movs r7, #0                       
  03f16:  movs r1, #0x24                    
  03f18:  add r0, sp, #4                    
  03f1a:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  03f1e:  ldr r0, [pc, #0x370]              -> RAM
  03f20:  ldrh r0, [r0]                     
  03f22:  adds r0, r0, #1                   
  03f24:  ldr r1, [pc, #0x368]              -> RAM
  03f26:  strh r0, [r1]                     
  03f28:  ldr r0, [pc, #0x368]              -> RAM
  03f2a:  ldrb r0, [r0]                     
  03f2c:  cmp r0, #6                        
  03f2e:  bhs #0x4022                       
  03f30:  tbb [pc, r0]                      
  03f34:  subs r3, r0, r4                   
  03f36:  ldr r2, [r0, #0x14]               
  03f38:  ldm r4!, {r0, r2, r5, r7}         
  03f3a:  movs r0, #0                       
  03f3c:  ldr r1, [pc, #0x350]              -> RAM
  03f3e:  strh r0, [r1]                     
  03f40:  ldr r1, [pc, #0x354]              -> RAM
  03f42:  strb r0, [r1]                     
  03f44:  ldr r0, [pc, #0x354]              -> RAM
  03f46:  ldrb r0, [r0]                     
  03f48:  cmp r0, #1                        
  03f4a:  bne #0x3f62                       
  03f4c:  bl #0x30a6                        -> func_0x030a6
  03f50:  bl #0x2b2c                        -> func_0x02b2c
  03f54:  movs r0, #1                       
  03f56:  ldr r1, [pc, #0x33c]              -> RAM
  03f58:  strb r0, [r1]                     
  03f5a:  movs r0, #0                       
  03f5c:  ldr r1, [pc, #0x340]              -> RAM
  03f5e:  strb r0, [r1]                     
  03f60:  b #0x3f68                         -> 0x03f68 (вне списка функций)
  03f62:  movs r0, #1                       
  03f64:  ldr r1, [pc, #0x338]              -> RAM
  03f66:  strb r0, [r1]                     
  03f68:  b #0x41ec                         -> 0x041ec (вне списка функций)
  03f6a:  ldr r0, [pc, #0x32c]              -> RAM
  03f6c:  ldrb r0, [r0]                     
  03f6e:  cmp r0, #0xa                      
  03f70:  ble #0x3f86                       
  03f72:  movs r0, #0                       
  03f74:  ldr r1, [pc, #0x31c]              -> RAM
  03f76:  strb r0, [r1]                     
  03f78:  movs r0, #1                       
  03f7a:  ldr r1, [pc, #0x324]              -> RAM
  03f7c:  strb r0, [r1]                     
  03f7e:  movs r0, #0                       
  03f80:  ldr r1, [pc, #0x314]              -> RAM
  03f82:  strb r0, [r1]                     
  03f84:  b #0x3fb6                         -> 0x03fb6 (вне списка функций)
  03f86:  ldr r0, [pc, #0x308]              -> RAM
  03f88:  ldrh r0, [r0]                     
  03f8a:  cmp r0, #0x14                     
  03f8c:  ble #0x3fb6                       
  03f8e:  ldrb.w r0, [sp, #6]               
  03f92:  bic r1, r0, #0xf0                 
  03f96:  strb.w r1, [sp, #6]               
  03f9a:  movs r0, #2                       
  03f9c:  strb.w r0, [sp, #5]               
  03fa0:  ldrb.w r0, [sp, #6]               
  03fa4:  lsrs r0, r0, #4                   
  03fa6:  lsls r4, r0, #2                   
  03fa8:  mov.w sb, #1                      
  03fac:  movs r0, #0                       
  03fae:  ldr r1, [pc, #0x2e0]              -> RAM
  03fb0:  strh r0, [r1]                     
  03fb2:  ldr r1, [pc, #0x2ec]              -> RAM
  03fb4:  strb r0, [r1]                     
  03fb6:  b #0x41ec                         -> 0x041ec (вне списка функций)
  03fb8:  ldr r0, [pc, #0x2dc]              -> RAM
  03fba:  ldrb r0, [r0]                     
  03fbc:  cmp r0, #3                        
  03fbe:  ble #0x3fd4                       
  03fc0:  movs r0, #0                       
  03fc2:  ldr r1, [pc, #0x2d0]              -> RAM
  03fc4:  strb r0, [r1]                     
  03fc6:  movs r0, #2                       
  03fc8:  ldr r1, [pc, #0x2d4]              -> RAM
  03fca:  strb r0, [r1]                     
  03fcc:  movs r0, #0                       
  03fce:  ldr r1, [pc, #0x2c8]              -> RAM
  03fd0:  strb r0, [r1]                     
  03fd2:  b #0x4004                         -> 0x04004 (вне списка функций)
  03fd4:  ldr r0, [pc, #0x2b8]              -> RAM
  03fd6:  ldrh r0, [r0]                     
  03fd8:  cmp r0, #0x14                     
  03fda:  ble #0x4004                       
  03fdc:  ldrb.w r0, [sp, #6]               
  03fe0:  bic r1, r0, #0xf0                 
  03fe4:  strb.w r1, [sp, #6]               
  03fe8:  movs r0, #4                       
  03fea:  strb.w r0, [sp, #5]               
  03fee:  ldrb.w r0, [sp, #6]               
  03ff2:  lsrs r0, r0, #4                   
  03ff4:  lsls r4, r0, #2                   
  03ff6:  mov.w sb, #1                      
  03ffa:  movs r0, #0                       
  03ffc:  ldr r1, [pc, #0x290]              -> RAM
  03ffe:  strh r0, [r1]                     
  04000:  ldr r1, [pc, #0x29c]              -> RAM
  04002:  strb r0, [r1]                     
  04004:  b #0x41ec                         -> 0x041ec (вне списка функций)
  04006:  ldr r0, [pc, #0x290]              -> RAM
  04008:  ldrb r0, [r0]                     
  0400a:  cmp r0, #3                        
  0400c:  ble #0x4024                       
  0400e:  movs r0, #0                       
  04010:  ldr r1, [pc, #0x280]              -> RAM
  04012:  strb r0, [r1]                     
  04014:  movs r0, #2                       
  04016:  ldr r1, [pc, #0x288]              -> RAM
  04018:  strb r0, [r1]                     
  0401a:  movs r0, #0                       
  0401c:  ldr r1, [pc, #0x278]              -> RAM
  0401e:  strb r0, [r1]                     
  04020:  b #0x407c                         -> 0x0407c (вне списка функций)
  04022:  b #0x41ea                         -> 0x041ea (вне списка функций)
  04024:  ldr r0, [pc, #0x268]              -> RAM
  04026:  ldrh r0, [r0]                     
  04028:  cmp r0, #0x14                     
  0402a:  ble #0x407c                       
  0402c:  ldrb.w r0, [sp, #6]               
  04030:  bic r0, r0, #0xf0                 
  04034:  adds r0, #0x40                    
  04036:  strb.w r0, [sp, #6]               
  0403a:  movs r0, #0x1c                    
  0403c:  strb.w r0, [sp, #5]               
  04040:  ldrb.w r0, [sp, #6]               
  04044:  lsrs r0, r0, #4                   
  04046:  lsls r4, r0, #2                   
  04048:  movs r1, #0x10                    
  0404a:  ldr r0, [pc, #0x258]              -> RAM
  0404c:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  04050:  movs r5, #0                       
  04052:  b #0x406a                         -> 0x0406a (вне списка функций)
  04054:  bl #0x1180                        -> 0x01180 (вне списка функций)
  04058:  ldr r1, [pc, #0x248]              -> RAM
  0405a:  strb r0, [r1, r5]                 
  0405c:  mov r0, r1                        
  0405e:  ldrb r1, [r0, r5]                 
  04060:  add.w r0, sp, #7                  
  04064:  strb r1, [r0, r5]                 
  04066:  adds r0, r5, #1                   
  04068:  uxtb r5, r0                       
  0406a:  cmp r5, #0x10                     
  0406c:  blt #0x4054                       
  0406e:  mov.w sb, #1                      
  04072:  movs r0, #0                       
  04074:  ldr r1, [pc, #0x218]              -> RAM
  04076:  strh r0, [r1]                     
  04078:  ldr r1, [pc, #0x224]              -> RAM
  0407a:  strb r0, [r1]                     
  0407c:  b #0x41ec                         -> 0x041ec (вне списка функций)
  0407e:  ldr r0, [pc, #0x218]              -> RAM
  04080:  ldrb r0, [r0]                     
  04082:  cmp r0, #3                        
  04084:  ble #0x409a                       
  04086:  movs r0, #0                       
  04088:  ldr r1, [pc, #0x208]              -> RAM
  0408a:  strb r0, [r1]                     
  0408c:  movs r0, #2                       
  0408e:  ldr r1, [pc, #0x210]              -> RAM
  04090:  strb r0, [r1]                     
  04092:  movs r0, #0                       
  04094:  ldr r1, [pc, #0x200]              -> RAM
  04096:  strb r0, [r1]                     
  04098:  b #0x40ca                         -> 0x040ca (вне списка функций)
  0409a:  ldr r0, [pc, #0x1f4]              -> RAM
  0409c:  ldrh r0, [r0]                     
  0409e:  cmp r0, #0x14                     
  040a0:  ble #0x40ca                       
  040a2:  ldrb.w r0, [sp, #6]               
  040a6:  bic r1, r0, #0xf0                 
  040aa:  strb.w r1, [sp, #6]               
  040ae:  movs r0, #6                       
  040b0:  strb.w r0, [sp, #5]               
  040b4:  ldrb.w r0, [sp, #6]               
  040b8:  lsrs r0, r0, #4                   
  040ba:  lsls r4, r0, #2                   
  040bc:  mov.w sb, #1                      
  040c0:  movs r0, #0                       
  040c2:  ldr r1, [pc, #0x1cc]              -> RAM
  040c4:  strh r0, [r1]                     
  040c6:  ldr r1, [pc, #0x1d8]              -> RAM
  040c8:  strb r0, [r1]                     
  040ca:  b #0x41ec                         -> 0x041ec (вне списка функций)
  040cc:  ldr r0, [pc, #0x1c8]              -> RAM
  040ce:  ldrb r0, [r0]                     
  040d0:  cmp r0, #3                        
  040d2:  ble #0x40e8                       
  040d4:  movs r0, #0                       
  040d6:  ldr r1, [pc, #0x1bc]              -> RAM
  040d8:  strb r0, [r1]                     
  040da:  movs r0, #2                       
  040dc:  ldr r1, [pc, #0x1c0]              -> RAM
  040de:  strb r0, [r1]                     
  040e0:  movs r0, #0                       
  040e2:  ldr r1, [pc, #0x1b4]              -> RAM
  040e4:  strb r0, [r1]                     
  040e6:  b #0x41e8                         -> 0x041e8 (вне списка функций)
  040e8:  ldr r0, [pc, #0x1a4]              -> RAM
  040ea:  ldrh r0, [r0]                     
  040ec:  cmp r0, #0x1e                     
  040ee:  ble #0x41e8                       
  040f0:  ldrb.w r0, [sp, #6]               
  040f4:  bic r0, r0, #0xf0                 
  040f8:  adds r0, #0x10                    
  040fa:  strb.w r0, [sp, #6]               
  040fe:  movs r0, #8                       
  04100:  strb.w r0, [sp, #5]               
  04104:  ldrb.w r0, [sp, #6]               
  04108:  lsrs r0, r0, #4                   
  0410a:  lsls r4, r0, #2                   
  0410c:  movw sl, #0xd548                  
  04110:  ldr r0, [pc, #0x194]              -> RAM
  04112:  ldrh r0, [r0]                     
  04114:  movs r1, #0x64                    
  04116:  mul r8, r0, r1                    
  0411a:  cmp.w r8, #0x140                  
  0411e:  bhs #0x4126                       
  04120:  mov.w r8, #0                      
  04124:  b #0x4154                         -> 0x04154 (вне списка функций)
  04126:  ldr r3, [pc, #0x184]              -> RAM
  04128:  ldrh r3, [r3, #4]                 
  0412a:  ubfx r2, r3, #0, #0xc             
  0412e:  ldr r3, [pc, #0x17c]              -> RAM
  04130:  ldrh.w r3, [r3, #5]               
  04134:  ubfx r3, r3, #4, #6               
  04138:  add.w r3, r3, r3, lsl #2          
  0413c:  lsls r1, r3, #1                   
  0413e:  ldr r3, [pc, #0x16c]              -> RAM
  04140:  ldrh r3, [r3, #6]                 
  04142:  ubfx r3, r3, #2, #0xa             
  04146:  add.w r3, r3, r3, lsl #2          
  0414a:  lsls r0, r3, #1                   
  0414c:  mov r3, r8                        
  0414e:  bl #0xdd2c                        -> func_0x0dd2c
  04152:  mov r7, r0                        
  04154:  ldr r3, [pc, #0x154]              -> RAM
  04156:  ldrh r3, [r3, #8]                 
  04158:  ubfx r2, r3, #0, #0xa             
  0415c:  ldr r3, [pc, #0x14c]              -> RAM
  0415e:  ldrh.w r3, [r3, #9]               
  04162:  ubfx r3, r3, #2, #0xa             
  04166:  add.w r1, r3, r3, lsl #2          
  0416a:  ldr r3, [pc, #0x140]              -> RAM
  0416c:  ldrh r3, [r3, #0xa]               
  0416e:  lsrs r3, r3, #4                   
  04170:  add.w r3, r3, r3, lsl #2          
  04174:  lsls r0, r3, #1                   
  04176:  mov r3, sl                        
  04178:  bl #0xdd2c                        -> func_0x0dd2c
  0417c:  mov r6, r0                        
  0417e:  movs r1, #5                       
  04180:  udiv r0, r6, r1                   
  04184:  uxth r0, r0                       
  04186:  strh.w r0, [sp]                   
  0418a:  movs r0, #0xa                     
  0418c:  udiv r0, r7, r0                   
  04190:  ldrh.w r1, [sp, #2]               
  04194:  bfi r1, r0, #0, #0xc              
  04198:  strh.w r1, [sp, #2]               
  0419c:  ldrh.w r0, [sp]                   
  041a0:  ldr r1, [pc, #0x10c]              -> RAM
  041a2:  strh r0, [r1, #0x18]              
  041a4:  ldrh.w r0, [sp, #2]               
  041a8:  ubfx r0, r0, #0, #0xc             
  041ac:  strh r0, [r1, #0x1a]              
  041ae:  ldrb.w r0, [sp, #3]               
  041b2:  bic r0, r0, #0xf0                 
  041b6:  strb.w r0, [sp, #3]               
  041ba:  ldr r0, [sp]                      
  041bc:  lsrs r0, r0, #0x18                
  041be:  strb.w r0, [sp, #7]               
  041c2:  ldr r0, [sp]                      
  041c4:  lsrs r1, r0, #0x10                
  041c6:  strb.w r1, [sp, #8]               
  041ca:  ldr r0, [sp]                      
  041cc:  lsrs r1, r0, #8                   
  041ce:  strb.w r1, [sp, #9]               
  041d2:  ldr r0, [sp]                      
  041d4:  uxtb r1, r0                       
  041d6:  strb.w r1, [sp, #0xa]             
  041da:  mov.w sb, #1                      
  041de:  movs r0, #0                       
  041e0:  ldr r1, [pc, #0xac]               -> RAM
  041e2:  strh r0, [r1]                     
  041e4:  ldr r1, [pc, #0xb8]               -> RAM
  041e6:  strb r0, [r1]                     
  041e8:  b #0x41ec                         -> 0x041ec (вне списка функций)
  041ea:  nop                               
  041ec:  nop                               
  041ee:  cmp.w sb, #1                      
  041f2:  bne #0x428a                       
  041f4:  movs r0, #0xaa                    
  041f6:  strb.w r0, [sp, #4]               
  041fa:  ldr r0, [pc, #0xb8]               -> RAM
  041fc:  ldrb r1, [r0]                     
  041fe:  ldrb.w r0, [sp, #6]               
  04202:  bfi r0, r1, #0, #4                
  04206:  strb.w r0, [sp, #6]               
  0420a:  ldr r0, [pc, #0xa8]               -> RAM
  0420c:  ldrb r0, [r0]                     
  0420e:  adds r0, r0, #1                   
  04210:  ldr r1, [pc, #0xa0]               -> RAM
  04212:  strb r0, [r1]                     
  04214:  mov r0, r1                        
  04216:  ldrb r0, [r0]                     
  04218:  cmp r0, #7                        
  0421a:  ble #0x4220                       
  0421c:  movs r0, #0                       
  0421e:  strb r0, [r1]                     
  04220:  ldrb.w r0, [sp, #4]               
  04224:  strb.w r0, [sp, #0x28]            
  04228:  ldrh.w r0, [sp, #5]               
  0422c:  asrs r0, r0, #8                   
  0422e:  strb.w r0, [sp, #0x29]            
  04232:  ldrb.w r0, [sp, #5]               
  04236:  strb.w r0, [sp, #0x2a]            
  0423a:  cmp r4, #0                        
  0423c:  ble #0x424c                       
  0423e:  mov r2, r4                        
  04240:  add.w r1, sp, #7                  
  04244:  add.w r0, sp, #0x2b               
  04248:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0424c:  adds r1, r4, #2                   
  0424e:  add.w r0, sp, #0x29               
  04252:  bl #0x3b42                        -> func_0x03b42
  04256:  strh.w r0, [sp, #0x23]            
  0425a:  ldrh.w r0, [sp, #0x23]            
  0425e:  asrs r1, r0, #8                   
  04260:  adds r0, r4, #3                   
  04262:  add r2, sp, #0x28                 
  04264:  strb r1, [r2, r0]                 
  04266:  ldrb.w r1, [sp, #0x23]            
  0426a:  adds r0, r4, #4                   
  0426c:  strb r1, [r2, r0]                 
  0426e:  adds r0, r4, #5                   
  04270:  uxtb r2, r0                       
  04272:  add r1, sp, #0x28                 
  04274:  movs r0, #2                       
  04276:  bl #0x13284                       -> func_0x13284
  0427a:  movs r0, #0                       
  0427c:  ldr r1, [pc, #0x10]               -> RAM
  0427e:  strh r0, [r1]                     
  04280:  ldr r0, [pc, #0x14]               -> RAM
  04282:  ldrb r0, [r0]                     
  04284:  adds r0, r0, #1                   
  04286:  ldr r1, [pc, #0x10]               -> RAM
  04288:  strb r0, [r1]                     
  0428a:  add sp, #0x50                     
  0428c:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
  ; --- literal-пул @0x04290 (10 слов) — ВНЕ границ функции ---
  04290:  .word 0x200009be  ; RAM
  04294:  .word 0x200009b4  ; RAM
  04298:  .word 0x200009bc  ; RAM
  0429c:  .word 0x2000008a  ; RAM
  042a0:  .word 0x200009b5  ; RAM
  042a4:  .word 0x20001222  ; RAM
  042a8:  .word 0x20000c89  ; RAM
  042ac:  .word 0x20001232  ; RAM
  042b0:  .word 0x20000fe7  ; RAM
  042b4:  .word 0x200009bd  ; RAM
```
