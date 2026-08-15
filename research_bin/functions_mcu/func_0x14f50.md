# func_0x14f50

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080014f50) | `0x00014f50` |
| размер кода | 1572 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000080 — RAM (r0)
- 0x2000008c — RAM (r0)
- 0x20000098 — RAM (r0)
- 0x20000c90 — RAM (r0)
- 0x20000c94 — RAM (r1)
- 0x20000c98 — RAM (r1)
- 0x20000c9a — RAM (r0)
- 0x20000c9b — RAM (r0)
- 0x20000f70 — RAM (r1)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)
- 0x20000fc7 — RAM (r0)
- 0x20000fd3 — RAM (r0)
- 0x20003024 — RAM (r1)

## Вызовы (callees)

- `func_0x08a90` (0x00008a90, bl)
- 0x0d84c (bl, вне списка функций)
- `func_0x0d938` (0x0000d938, bl)
- 0x15034 (b, вне списка функций)
- 0x15066 (b, вне списка функций)
- 0x15148 (b, вне списка функций)
- 0x151ea (b, вне списка функций)
- 0x15254 (b, вне списка функций)
- 0x1529c (b, вне списка функций)
- 0x1529e (b, вне списка функций)
- 0x152aa (b, вне списка функций)
- 0x15384 (b, вне списка функций)
- 0x153cc (b, вне списка функций)
- 0x1551a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x14f68..0x14fd8` (112 Б); цели из: 0x14f60
- `0x14fd8..0x1502e` (86 Б); цели из: 0x14f94
- `0x1502e..0x15034` (6 Б); цели из: 0x14fe8
- `0x15034..0x15036` (2 Б); цели из: 0x14ffa, 0x1502c
- `0x15036..0x15064` (46 Б); цели из: 0x14f5c
- `0x15064..0x15066` (2 Б); цели из: 0x14f64
- `0x15066..0x15144` (222 Б); цели из: 0x15062
- `0x15144..0x15146` (2 Б); цели из: 0x15046
- `0x15146..0x15148` (2 Б); цели из: 0x1505c, 0x15068, 0x15070
- `0x15148..0x151ea` (162 Б); цели из: 0x15142
- `0x151ea..0x15254` (106 Б); цели из: 0x151e6
- `0x15254..0x1529c` (72 Б); цели из: 0x15146
- `0x1529c..0x1529e` (2 Б); цели из: 0x15144, 0x1525c
- `0x1529e..0x152aa` (12 Б); цели из: 0x15064
- `0x152aa..0x15384` (218 Б); цели из: 0x15034, 0x1529c
- `0x15384..0x153cc` (72 Б); цели из: 0x1534e
- `0x153cc..0x15430` (100 Б); цели из: 0x153c8
- `0x15430..0x1551a` (234 Б); цели из: 0x15426
- `0x1551a..0x15574` (90 Б); цели из: 0x15516

## Дизассембляция

```asm
  14f50:  push {r2, r3, r4, r5, r6, lr}     
  14f52:  movs r4, #0                       
  14f54:  movs r5, #0                       
  14f56:  ldr r0, [pc, #0x3f8]              -> RAM
  14f58:  ldrb r5, [r0]                     
  14f5a:  cmp r5, #0                        
  14f5c:  beq #0x15036                      
  14f5e:  cmp r5, #1                        
  14f60:  beq #0x14f68                      
  14f62:  cmp r5, #2                        
  14f64:  bne #0x15064                      
  14f66:  nop                               
  14f68:  movs r0, #0                       
  14f6a:  ldr r1, [pc, #0x3e8]              -> RAM
  14f6c:  strh r0, [r1]                     
  14f6e:  ldr r0, [pc, #0x3e8]              -> RAM
  14f70:  ldrh r0, [r0]                     
  14f72:  orr r0, r0, #0x80                 
  14f76:  ldr r1, [pc, #0x3e0]              -> RAM
  14f78:  strh r0, [r1]                     
  14f7a:  mov r0, r1                        
  14f7c:  ldrb r0, [r0]                     
  14f7e:  ubfx r0, r0, #1, #1               
  14f82:  cbz r0, #0x14fd8                  
  14f84:  ldr r0, [pc, #0x3d4]              -> RAM
  14f86:  ldrb r0, [r0]                     
  14f88:  adds r0, r0, #1                   
  14f8a:  ldr r1, [pc, #0x3d0]              -> RAM
  14f8c:  strb r0, [r1]                     
  14f8e:  mov r0, r1                        
  14f90:  ldrb r0, [r0]                     
  14f92:  cmp r0, #5                        
  14f94:  blt #0x14fd8                      
  14f96:  movs r0, #0                       
  14f98:  strb r0, [r1]                     
  14f9a:  ldr r0, [pc, #0x3bc]              -> RAM
  14f9c:  ldrh r0, [r0]                     
  14f9e:  bic r0, r0, #2                    
  14fa2:  ldr r1, [pc, #0x3b4]              -> RAM
  14fa4:  strh r0, [r1]                     
  14fa6:  mov r0, r1                        
  14fa8:  ldrh r0, [r0]                     
  14faa:  orr r0, r0, #1                    
  14fae:  strh r0, [r1]                     
  14fb0:  mov r0, r1                        
  14fb2:  ldrh r0, [r0]                     
  14fb4:  orr r0, r0, #4                    
  14fb8:  strh r0, [r1]                     
  14fba:  movs r0, #1                       
  14fbc:  bl #0xd938                        -> func_0x0d938
  14fc0:  movs r4, #1                       
  14fc2:  ldr r0, [pc, #0x394]              -> RAM
  14fc4:  ldrb r0, [r0]                     
  14fc6:  ubfx r0, r0, #3, #1               
  14fca:  cbnz r0, #0x14fd8                 
  14fcc:  ldr r0, [pc, #0x388]              -> RAM
  14fce:  ldrh r0, [r0]                     
  14fd0:  orr r0, r0, #8                    
  14fd4:  ldr r1, [pc, #0x380]              -> RAM
  14fd6:  strh r0, [r1]                     
  14fd8:  ldr r0, [pc, #0x37c]              -> RAM
  14fda:  ldrb r0, [r0]                     
  14fdc:  ubfx r0, r0, #3, #1               
  14fe0:  cbz r0, #0x1502c                  
  14fe2:  ldr r0, [pc, #0x37c]              -> RAM
  14fe4:  ldrb r0, [r0]                     
  14fe6:  cmp r0, #0x1e                     
  14fe8:  bgt #0x1502e                      
  14fea:  ldr r0, [pc, #0x378]              -> RAM
  14fec:  ldrb r0, [r0]                     
  14fee:  adds r0, r0, #1                   
  14ff0:  ldr r1, [pc, #0x370]              -> RAM
  14ff2:  strb r0, [r1]                     
  14ff4:  mov r0, r1                        
  14ff6:  ldrb r0, [r0]                     
  14ff8:  cmp r0, #0xa                      
  14ffa:  ble #0x15034                      
  14ffc:  cbnz r4, #0x1502c                 
  14ffe:  ldr r0, [pc, #0x358]              -> RAM
  15000:  ldrh r0, [r0]                     
  15002:  bic r0, r0, #8                    
  15006:  ldr r1, [pc, #0x350]              -> RAM
  15008:  strh r0, [r1]                     
  1500a:  mov r0, r1                        
  1500c:  ldrh r0, [r0]                     
  1500e:  orr r0, r0, #1                    
  15012:  strh r0, [r1]                     
  15014:  mov r0, r1                        
  15016:  ldrh r0, [r0]                     
  15018:  orr r0, r0, #4                    
  1501c:  strh r0, [r1]                     
  1501e:  movs r0, #3                       
  15020:  bl #0xd938                        -> func_0x0d938
  15024:  movs r0, #0                       
  15026:  ldr r1, [pc, #0x33c]              -> RAM
  15028:  strb r0, [r1]                     
  1502a:  movs r4, #1                       
  1502c:  b #0x15034                        -> 0x15034 (вне списка функций)
  1502e:  movs r0, #0                       
  15030:  ldr r1, [pc, #0x330]              -> RAM
  15032:  strb r0, [r1]                     
  15034:  b #0x152aa                        -> 0x152aa (вне списка функций)
  15036:  movs r0, #0                       
  15038:  ldr r1, [pc, #0x320]              -> RAM
  1503a:  strb r0, [r1]                     
  1503c:  ldr r0, [pc, #0x318]              -> RAM
  1503e:  ldrb r0, [r0]                     
  15040:  and r0, r0, #1                    
  15044:  cmp r0, #0                        
  15046:  beq #0x15144                      
  15048:  ldr r0, [pc, #0x308]              -> RAM
  1504a:  ldrh r0, [r0]                     
  1504c:  adds r0, r0, #1                   
  1504e:  ldr r1, [pc, #0x304]              -> RAM
  15050:  strh r0, [r1]                     
  15052:  ldr r0, [pc, #0x304]              -> RAM
  15054:  ldrb r0, [r0]                     
  15056:  ubfx r0, r0, #7, #1               
  1505a:  cmp r0, #0                        
  1505c:  beq #0x15146                      
  1505e:  ldr r0, [pc, #0x308]              -> RAM
  15060:  ldr r0, [r0, #4]                  
  15062:  b #0x15066                        -> 0x15066 (вне списка функций)
  15064:  b #0x1529e                        -> 0x1529e (вне списка функций)
  15066:  cmp r0, #0x64                     
  15068:  bls #0x15146                      
  1506a:  mov r0, r1                        
  1506c:  ldrh r0, [r0]                     
  1506e:  cmp r0, #0xa                      
  15070:  blt #0x15146                      
  15072:  movs r0, #0                       
  15074:  ldr r1, [pc, #0x2f4]              -> RAM
  15076:  strh r0, [r1]                     
  15078:  mov r0, sp                        
  1507a:  bl #0x8a90                        -> func_0x08a90
  1507e:  ldr r0, [pc, #0x2f0]              -> RAM
  15080:  ldr r1, [sp]                      
  15082:  str r1, [r0]                      
  15084:  ldrh.w r1, [sp, #4]               
  15088:  strh r1, [r0, #4]                 
  1508a:  ldrb.w r1, [sp, #6]               
  1508e:  strb r1, [r0, #6]                 
  15090:  ldrb r1, [r0, #5]                 
  15092:  ldr r0, [pc, #0x2d8]              -> RAM
  15094:  strb r1, [r0, #7]                 
  15096:  ldr r0, [pc, #0x2d8]              -> RAM
  15098:  ldrb r1, [r0, #4]                 
  1509a:  ldr r0, [pc, #0x2d0]              -> RAM
  1509c:  strb r1, [r0, #6]                 
  1509e:  ldr r0, [pc, #0x2d0]              -> RAM
  150a0:  ldrb r1, [r0, #3]                 
  150a2:  ldr r0, [pc, #0x2c8]              -> RAM
  150a4:  strb r1, [r0, #5]                 
  150a6:  ldr r0, [pc, #0x2c8]              -> RAM
  150a8:  ldrb r1, [r0, #2]                 
  150aa:  ldr r0, [pc, #0x2c0]              -> RAM
  150ac:  strb r1, [r0, #4]                 
  150ae:  ldr r0, [pc, #0x2c0]              -> RAM
  150b0:  ldrb r1, [r0, #1]                 
  150b2:  ldr r0, [pc, #0x2b8]              -> RAM
  150b4:  strb r1, [r0, #3]                 
  150b6:  ldr r0, [pc, #0x2b8]              -> RAM
  150b8:  ldrb r0, [r0]                     
  150ba:  ldr r1, [pc, #0x2b0]              -> RAM
  150bc:  strb r0, [r1, #2]                 
  150be:  bl #0xd84c                        -> 0x0d84c (вне списка функций)
  150c2:  ldr r0, [pc, #0x2b0]              -> RAM
  150c4:  ldr r0, [r0]                      
  150c6:  ldr r1, [pc, #0x2a4]              -> RAM
  150c8:  str r0, [r1, #8]                  
  150ca:  ldr r0, [pc, #0x2a8]              -> RAM
  150cc:  ldrh r0, [r0, #8]                 
  150ce:  strh r0, [r1, #0xc]               
  150d0:  ldr r0, [pc, #0x2a0]              -> RAM
  150d2:  ldrh r0, [r0, #6]                 
  150d4:  strh r0, [r1, #0xe]               
  150d6:  ldr r0, [pc, #0x290]              -> RAM
  150d8:  ldr r0, [r0]                      
  150da:  str r0, [r1, #0x10]               
  150dc:  ldr r0, [pc, #0x298]              -> RAM
  150de:  ldrb r0, [r0, #2]                 
  150e0:  strb r0, [r1, #0x14]              
  150e2:  ldr r0, [pc, #0x294]              -> RAM
  150e4:  ldrb r0, [r0, #1]                 
  150e6:  strb r0, [r1, #0x15]              
  150e8:  ldr r0, [pc, #0x274]              -> RAM
  150ea:  ldrh r0, [r0, #2]                 
  150ec:  strh r0, [r1, #0x16]              
  150ee:  ldr r0, [pc, #0x270]              -> RAM
  150f0:  ldr r0, [r0, #0xc]                
  150f2:  str r0, [r1, #0x18]               
  150f4:  ldr r0, [pc, #0x268]              -> RAM
  150f6:  ldr r0, [r0, #8]                  
  150f8:  str r0, [r1, #0x1c]               
  150fa:  ldr r0, [pc, #0x278]              -> RAM
  150fc:  ldrb r0, [r0, #0xc]               
  150fe:  ubfx r1, r0, #1, #1               
  15102:  ldr r0, [pc, #0x270]              -> RAM
  15104:  ldrb r0, [r0, #0xc]               
  15106:  bfi r0, r1, #1, #0x1f             
  1510a:  ldr r1, [pc, #0x268]              -> RAM
  1510c:  ldrb r1, [r1, #0x17]              
  1510e:  and r1, r1, #1                    
  15112:  orr.w r0, r0, r1, lsl #2          
  15116:  ldr r1, [pc, #0x25c]              -> RAM
  15118:  ldrb r1, [r1, #0xc]               
  1511a:  ubfx r1, r1, #3, #1               
  1511e:  orr.w r0, r0, r1, lsl #3          
  15122:  ldr r1, [pc, #0x250]              -> RAM
  15124:  ldrb r1, [r1, #0xc]               
  15126:  ubfx r1, r1, #4, #1               
  1512a:  orr.w r0, r0, r1, lsl #4          
  1512e:  ldr r1, [pc, #0x244]              -> RAM
  15130:  ldrb r1, [r1, #0xc]               
  15132:  ubfx r1, r1, #6, #1               
  15136:  orr.w r0, r0, r1, lsl #5          
  1513a:  ldr r1, [pc, #0x240]              -> RAM
  1513c:  ldrb r1, [r1, #2]                 
  1513e:  and r1, r1, #1                    
  15142:  b #0x15148                        -> 0x15148 (вне списка функций)
  15144:  b #0x1529c                        -> 0x1529c (вне списка функций)
  15146:  b #0x15254                        -> 0x15254 (вне списка функций)
  15148:  orr.w r0, r0, r1, lsl #7          
  1514c:  ldr r1, [pc, #0x218]              -> RAM
  1514e:  ldrb r1, [r1, #8]                 
  15150:  and r1, r1, #1                    
  15154:  orr.w r0, r0, r1, lsl #8          
  15158:  ldr r1, [pc, #0x20c]              -> RAM
  1515a:  ldrb r1, [r1, #8]                 
  1515c:  ubfx r1, r1, #1, #1               
  15160:  orr.w r0, r0, r1, lsl #9          
  15164:  ldr r1, [pc, #0x200]              -> RAM
  15166:  ldrb r1, [r1, #8]                 
  15168:  ubfx r1, r1, #3, #1               
  1516c:  orr.w r0, r0, r1, lsl #10         
  15170:  ldr r1, [pc, #0x1f4]              -> RAM
  15172:  ldrb r1, [r1, #8]                 
  15174:  ubfx r1, r1, #4, #1               
  15178:  orr.w r0, r0, r1, lsl #11         
  1517c:  ldr r1, [pc, #0x1e8]              -> RAM
  1517e:  ldrb r1, [r1, #8]                 
  15180:  ubfx r1, r1, #5, #1               
  15184:  orr.w r0, r0, r1, lsl #12         
  15188:  ldr r1, [pc, #0x1dc]              -> RAM
  1518a:  ldrb r1, [r1, #8]                 
  1518c:  ubfx r1, r1, #6, #1               
  15190:  orr.w r0, r0, r1, lsl #14         
  15194:  ldr r1, [pc, #0x1e0]              -> RAM
  15196:  ldrb r1, [r1, #6]                 
  15198:  and r1, r1, #1                    
  1519c:  orr.w r0, r0, r1, lsl #15         
  151a0:  ldr r1, [pc, #0x1d4]              -> RAM
  151a2:  ldrb r1, [r1, #6]                 
  151a4:  ubfx r1, r1, #1, #1               
  151a8:  orr.w r0, r0, r1, lsl #17         
  151ac:  ldr r1, [pc, #0x1c8]              -> RAM
  151ae:  ldrb r1, [r1, #6]                 
  151b0:  ubfx r1, r1, #3, #1               
  151b4:  orr.w r0, r0, r1, lsl #19         
  151b8:  ldr r1, [pc, #0x1bc]              -> RAM
  151ba:  ldrb r1, [r1, #6]                 
  151bc:  ubfx r1, r1, #5, #1               
  151c0:  orr.w r0, r0, r1, lsl #21         
  151c4:  ldr r1, [pc, #0x1b0]              -> RAM
  151c6:  ldrb r1, [r1, #9]                 
  151c8:  ubfx r1, r1, #1, #1               
  151cc:  orr.w r0, r0, r1, lsl #23         
  151d0:  ldr r1, [pc, #0x1a4]              -> RAM
  151d2:  ldrb r1, [r1, #6]                 
  151d4:  ubfx r1, r1, #6, #1               
  151d8:  cbnz r1, #0x151e4                 
  151da:  ldr r1, [pc, #0x19c]              -> RAM
  151dc:  ldrb r1, [r1, #9]                 
  151de:  ubfx r1, r1, #3, #1               
  151e2:  cbz r1, #0x151e8                  
  151e4:  movs r1, #1                       
  151e6:  b #0x151ea                        -> 0x151ea (вне списка функций)
  151e8:  movs r1, #0                       
  151ea:  orr.w r0, r0, r1, lsl #24         
  151ee:  ldr r1, [pc, #0x184]              -> RAM
  151f0:  ldrb r1, [r1, #0xc]               
  151f2:  lsrs r1, r1, #7                   
  151f4:  orr.w r0, r0, r1, lsl #25         
  151f8:  ldr r1, [pc, #0x180]              -> RAM
  151fa:  ldrb r1, [r1, #2]                 
  151fc:  ubfx r1, r1, #1, #1               
  15200:  orr.w r0, r0, r1, lsl #26         
  15204:  ldr r1, [pc, #0x174]              -> RAM
  15206:  ldrb r1, [r1, #2]                 
  15208:  ubfx r1, r1, #2, #1               
  1520c:  orr.w r0, r0, r1, lsl #27         
  15210:  ldr r1, [pc, #0x168]              -> RAM
  15212:  ldrb r1, [r1, #2]                 
  15214:  ubfx r1, r1, #3, #1               
  15218:  orr.w r0, r0, r1, lsl #28         
  1521c:  ldr r1, [pc, #0x15c]              -> RAM
  1521e:  ldrb r1, [r1, #3]                 
  15220:  ubfx r1, r1, #4, #1               
  15224:  orr.w r0, r0, r1, lsl #29         
  15228:  ldr r1, [pc, #0x150]              -> RAM
  1522a:  ldrb r1, [r1, #3]                 
  1522c:  ubfx r1, r1, #2, #1               
  15230:  orr.w r0, r0, r1, lsl #30         
  15234:  ldr r1, [pc, #0x144]              -> RAM
  15236:  ldrb r1, [r1, #3]                 
  15238:  lsrs r1, r1, #3                   
  1523a:  orr.w r0, r0, r1, lsl #31         
  1523e:  ldr r1, [pc, #0x12c]              -> RAM
  15240:  str r0, [r1, #0x20]               
  15242:  movs r0, #0                       
  15244:  strh r0, [r1, #0x24]              
  15246:  strh r0, [r1, #0x26]              
  15248:  ldr r0, [pc, #0x10c]              -> RAM
  1524a:  ldrh r0, [r0]                     
  1524c:  bic r0, r0, #0x80                 
  15250:  ldr r1, [pc, #0x104]              -> RAM
  15252:  strh r0, [r1]                     
  15254:  ldr r0, [pc, #0xfc]               -> RAM
  15256:  ldrh r0, [r0]                     
  15258:  cmp.w r0, #0x708                  
  1525c:  blt #0x1529c                      
  1525e:  cbnz r4, #0x1529c                 
  15260:  ldr r0, [pc, #0xf4]               -> RAM
  15262:  ldrh r0, [r0]                     
  15264:  bic r0, r0, #1                    
  15268:  ldr r1, [pc, #0xec]               -> RAM
  1526a:  strh r0, [r1]                     
  1526c:  mov r0, r1                        
  1526e:  ldrh r0, [r0]                     
  15270:  orr r0, r0, #2                    
  15274:  strh r0, [r1]                     
  15276:  ldr r0, [pc, #0x108]              -> RAM
  15278:  ldr r0, [r0]                      
  1527a:  orr r0, r0, #0x200                
  1527e:  ldr r1, [pc, #0x100]              -> RAM
  15280:  str r0, [r1]                      
  15282:  ldr r0, [pc, #0xf8]               -> RAM
  15284:  ldrh.w r0, [r0, #7]               
  15288:  adds r0, r0, #1                   
  1528a:  ldr r1, [pc, #0xf0]               -> RAM
  1528c:  strh.w r0, [r1, #7]               
  15290:  movs r0, #0                       
  15292:  bl #0xd938                        -> func_0x0d938
  15296:  movs r0, #0                       
  15298:  ldr r1, [pc, #0xb8]               -> RAM
  1529a:  strh r0, [r1]                     
  1529c:  b #0x152aa                        -> 0x152aa (вне списка функций)
  1529e:  movs r0, #0                       
  152a0:  ldr r1, [pc, #0xb0]               -> RAM
  152a2:  strh r0, [r1]                     
  152a4:  ldr r1, [pc, #0xb4]               -> RAM
  152a6:  strb r0, [r1]                     
  152a8:  nop                               
  152aa:  nop                               
  152ac:  ldr r0, [pc, #0xc4]               -> RAM
  152ae:  ldrb r0, [r0, #0xc]               
  152b0:  ubfx r1, r0, #1, #1               
  152b4:  ldr r0, [pc, #0xbc]               -> RAM
  152b6:  ldrb r0, [r0, #0xc]               
  152b8:  bfi r0, r1, #1, #0x1f             
  152bc:  ldr r1, [pc, #0xb4]               -> RAM
  152be:  ldrb r1, [r1, #0x17]              
  152c0:  and r1, r1, #1                    
  152c4:  orr.w r0, r0, r1, lsl #2          
  152c8:  ldr r1, [pc, #0xa8]               -> RAM
  152ca:  ldrb r1, [r1, #0xc]               
  152cc:  ubfx r1, r1, #3, #1               
  152d0:  orr.w r0, r0, r1, lsl #3          
  152d4:  ldr r1, [pc, #0x9c]               -> RAM
  152d6:  ldrb r1, [r1, #0xc]               
  152d8:  ubfx r1, r1, #4, #1               
  152dc:  orr.w r0, r0, r1, lsl #4          
  152e0:  ldr r1, [pc, #0x90]               -> RAM
  152e2:  ldrb r1, [r1, #0xc]               
  152e4:  ubfx r1, r1, #6, #1               
  152e8:  orr.w r0, r0, r1, lsl #5          
  152ec:  ldr r1, [pc, #0x8c]               -> RAM
  152ee:  ldrb r1, [r1, #2]                 
  152f0:  and r1, r1, #1                    
  152f4:  orr.w r0, r0, r1, lsl #7          
  152f8:  ldr r1, [pc, #0x6c]               -> RAM
  152fa:  ldrb r1, [r1, #8]                 
  152fc:  and r1, r1, #1                    
  15300:  orr.w r0, r0, r1, lsl #8          
  15304:  ldr r1, [pc, #0x60]               -> RAM
  15306:  ldrb r1, [r1, #8]                 
  15308:  ubfx r1, r1, #1, #1               
  1530c:  orr.w r0, r0, r1, lsl #9          
  15310:  ldr r1, [pc, #0x54]               -> RAM
  15312:  ldrb r1, [r1, #8]                 
  15314:  ubfx r1, r1, #3, #1               
  15318:  orr.w r0, r0, r1, lsl #10         
  1531c:  ldr r1, [pc, #0x48]               -> RAM
  1531e:  ldrb r1, [r1, #8]                 
  15320:  ubfx r1, r1, #4, #1               
  15324:  orr.w r0, r0, r1, lsl #11         
  15328:  ldr r1, [pc, #0x3c]               -> RAM
  1532a:  ldrb r1, [r1, #8]                 
  1532c:  ubfx r1, r1, #5, #1               
  15330:  orr.w r0, r0, r1, lsl #12         
  15334:  ldr r1, [pc, #0x30]               -> RAM
  15336:  ldrb r1, [r1, #8]                 
  15338:  ubfx r1, r1, #6, #1               
  1533c:  orr.w r0, r0, r1, lsl #14         
  15340:  ldr r1, [pc, #0x34]               -> RAM
  15342:  ldrb r1, [r1, #6]                 
  15344:  and r1, r1, #1                    
  15348:  orr.w r0, r0, r1, lsl #15         
  1534c:  ldr r1, [pc, #0x28]               -> RAM
  1534e:  b #0x15384                        -> 0x15384 (вне списка функций)
  15350:  lsls r0, r0, #2                   
  15352:  movs r0, #0                       
  15354:  lsrs r0, r3, #0x12                
  15356:  movs r0, #0                       
  15358:  lsrs r0, r2, #0x12                
  1535a:  movs r0, #0                       
  1535c:  lsrs r2, r3, #0x12                
  1535e:  movs r0, #0                       
  15360:  lsrs r3, r2, #0x1f                
  15362:  movs r0, #0                       
  15364:  lsrs r3, r3, #0x12                
  15366:  movs r0, #0                       
  15368:  lsrs r3, r7, #0x1e                
  1536a:  movs r0, #0                       
  1536c:  adds r0, #0x24                    
  1536e:  movs r0, #0                       
  15370:  lsls r0, r3, #2                   
  15372:  movs r0, #0                       
  15374:  lsrs r5, r2, #0x1e                
  15376:  movs r0, #0                       
  15378:  lsrs r7, r0, #0x1f                
  1537a:  movs r0, #0                       
  1537c:  lsrs r0, r6, #0x1d                
  1537e:  movs r0, #0                       
  15380:  lsls r4, r1, #2                   
  15382:  movs r0, #0                       
  15384:  ldrb r1, [r1, #6]                 
  15386:  ubfx r1, r1, #1, #1               
  1538a:  orr.w r0, r0, r1, lsl #17         
  1538e:  ldr r1, [pc, #0x1e4]              -> RAM
  15390:  ldrb r1, [r1, #6]                 
  15392:  ubfx r1, r1, #3, #1               
  15396:  orr.w r0, r0, r1, lsl #19         
  1539a:  ldr r1, [pc, #0x1d8]              -> RAM
  1539c:  ldrb r1, [r1, #6]                 
  1539e:  ubfx r1, r1, #5, #1               
  153a2:  orr.w r0, r0, r1, lsl #21         
  153a6:  ldr r1, [pc, #0x1cc]              -> RAM
  153a8:  ldrb r1, [r1, #9]                 
  153aa:  ubfx r1, r1, #1, #1               
  153ae:  orr.w r0, r0, r1, lsl #23         
  153b2:  ldr r1, [pc, #0x1c0]              -> RAM
  153b4:  ldrb r1, [r1, #6]                 
  153b6:  ubfx r1, r1, #6, #1               
  153ba:  cbnz r1, #0x153c6                 
  153bc:  ldr r1, [pc, #0x1b4]              -> RAM
  153be:  ldrb r1, [r1, #9]                 
  153c0:  ubfx r1, r1, #3, #1               
  153c4:  cbz r1, #0x153ca                  
  153c6:  movs r1, #1                       
  153c8:  b #0x153cc                        -> 0x153cc (вне списка функций)
  153ca:  movs r1, #0                       
  153cc:  orr.w r0, r0, r1, lsl #24         
  153d0:  ldr r1, [pc, #0x1a4]              -> RAM
  153d2:  ldrb r1, [r1, #0xc]               
  153d4:  lsrs r1, r1, #7                   
  153d6:  orr.w r0, r0, r1, lsl #25         
  153da:  ldr r1, [pc, #0x1a0]              -> RAM
  153dc:  ldrb r1, [r1, #2]                 
  153de:  ubfx r1, r1, #1, #1               
  153e2:  orr.w r0, r0, r1, lsl #26         
  153e6:  ldr r1, [pc, #0x194]              -> RAM
  153e8:  ldrb r1, [r1, #2]                 
  153ea:  ubfx r1, r1, #2, #1               
  153ee:  orr.w r0, r0, r1, lsl #27         
  153f2:  ldr r1, [pc, #0x188]              -> RAM
  153f4:  ldrb r1, [r1, #2]                 
  153f6:  ubfx r1, r1, #3, #1               
  153fa:  orr.w r0, r0, r1, lsl #28         
  153fe:  ldr r1, [pc, #0x17c]              -> RAM
  15400:  ldrb r1, [r1, #3]                 
  15402:  ubfx r1, r1, #4, #1               
  15406:  orr.w r0, r0, r1, lsl #29         
  1540a:  ldr r1, [pc, #0x170]              -> RAM
  1540c:  ldrb r1, [r1, #3]                 
  1540e:  ubfx r1, r1, #2, #1               
  15412:  orr.w r0, r0, r1, lsl #30         
  15416:  ldr r1, [pc, #0x164]              -> RAM
  15418:  ldrb r1, [r1, #3]                 
  1541a:  lsrs r1, r1, #3                   
  1541c:  orr.w r0, r0, r1, lsl #31         
  15420:  ldr r1, [pc, #0x15c]              -> RAM
  15422:  ldr r1, [r1]                      
  15424:  cmp r0, r1                        
  15426:  bls #0x15430                      
  15428:  cbnz r4, #0x15430                 
  1542a:  movs r0, #4                       
  1542c:  bl #0xd938                        -> func_0x0d938
  15430:  ldr r0, [pc, #0x144]              -> RAM
  15432:  ldrb r0, [r0, #0xc]               
  15434:  ubfx r1, r0, #1, #1               
  15438:  ldr r0, [pc, #0x13c]              -> RAM
  1543a:  ldrb r0, [r0, #0xc]               
  1543c:  bfi r0, r1, #1, #0x1f             
  15440:  ldr r1, [pc, #0x134]              -> RAM
  15442:  ldrb r1, [r1, #0x17]              
  15444:  and r1, r1, #1                    
  15448:  orr.w r0, r0, r1, lsl #2          
  1544c:  ldr r1, [pc, #0x128]              -> RAM
  1544e:  ldrb r1, [r1, #0xc]               
  15450:  ubfx r1, r1, #3, #1               
  15454:  orr.w r0, r0, r1, lsl #3          
  15458:  ldr r1, [pc, #0x11c]              -> RAM
  1545a:  ldrb r1, [r1, #0xc]               
  1545c:  ubfx r1, r1, #4, #1               
  15460:  orr.w r0, r0, r1, lsl #4          
  15464:  ldr r1, [pc, #0x110]              -> RAM
  15466:  ldrb r1, [r1, #0xc]               
  15468:  ubfx r1, r1, #6, #1               
  1546c:  orr.w r0, r0, r1, lsl #5          
  15470:  ldr r1, [pc, #0x108]              -> RAM
  15472:  ldrb r1, [r1, #2]                 
  15474:  and r1, r1, #1                    
  15478:  orr.w r0, r0, r1, lsl #7          
  1547c:  ldr r1, [pc, #0x104]              -> RAM
  1547e:  ldrb r1, [r1, #8]                 
  15480:  and r1, r1, #1                    
  15484:  orr.w r0, r0, r1, lsl #8          
  15488:  ldr r1, [pc, #0xf8]               -> RAM
  1548a:  ldrb r1, [r1, #8]                 
  1548c:  ubfx r1, r1, #1, #1               
  15490:  orr.w r0, r0, r1, lsl #9          
  15494:  ldr r1, [pc, #0xec]               -> RAM
  15496:  ldrb r1, [r1, #8]                 
  15498:  ubfx r1, r1, #3, #1               
  1549c:  orr.w r0, r0, r1, lsl #10         
  154a0:  ldr r1, [pc, #0xe0]               -> RAM
  154a2:  ldrb r1, [r1, #8]                 
  154a4:  ubfx r1, r1, #4, #1               
  154a8:  orr.w r0, r0, r1, lsl #11         
  154ac:  ldr r1, [pc, #0xd4]               -> RAM
  154ae:  ldrb r1, [r1, #8]                 
  154b0:  ubfx r1, r1, #5, #1               
  154b4:  orr.w r0, r0, r1, lsl #12         
  154b8:  ldr r1, [pc, #0xc8]               -> RAM
  154ba:  ldrb r1, [r1, #8]                 
  154bc:  ubfx r1, r1, #6, #1               
  154c0:  orr.w r0, r0, r1, lsl #14         
  154c4:  ldr r1, [pc, #0xac]               -> RAM
  154c6:  ldrb r1, [r1, #6]                 
  154c8:  and r1, r1, #1                    
  154cc:  orr.w r0, r0, r1, lsl #15         
  154d0:  ldr r1, [pc, #0xa0]               -> RAM
  154d2:  ldrb r1, [r1, #6]                 
  154d4:  ubfx r1, r1, #1, #1               
  154d8:  orr.w r0, r0, r1, lsl #17         
  154dc:  ldr r1, [pc, #0x94]               -> RAM
  154de:  ldrb r1, [r1, #6]                 
  154e0:  ubfx r1, r1, #3, #1               
  154e4:  orr.w r0, r0, r1, lsl #19         
  154e8:  ldr r1, [pc, #0x88]               -> RAM
  154ea:  ldrb r1, [r1, #6]                 
  154ec:  ubfx r1, r1, #5, #1               
  154f0:  orr.w r0, r0, r1, lsl #21         
  154f4:  ldr r1, [pc, #0x7c]               -> RAM
  154f6:  ldrb r1, [r1, #9]                 
  154f8:  ubfx r1, r1, #1, #1               
  154fc:  orr.w r0, r0, r1, lsl #23         
  15500:  ldr r1, [pc, #0x70]               -> RAM
  15502:  ldrb r1, [r1, #6]                 
  15504:  ubfx r1, r1, #6, #1               
  15508:  cbnz r1, #0x15514                 
  1550a:  ldr r1, [pc, #0x68]               -> RAM
  1550c:  ldrb r1, [r1, #9]                 
  1550e:  ubfx r1, r1, #3, #1               
  15512:  cbz r1, #0x15518                  
  15514:  movs r1, #1                       
  15516:  b #0x1551a                        -> 0x1551a (вне списка функций)
  15518:  movs r1, #0                       
  1551a:  orr.w r0, r0, r1, lsl #24         
  1551e:  ldr r1, [pc, #0x58]               -> RAM
  15520:  ldrb r1, [r1, #0xc]               
  15522:  lsrs r1, r1, #7                   
  15524:  orr.w r0, r0, r1, lsl #25         
  15528:  ldr r1, [pc, #0x50]               -> RAM
  1552a:  ldrb r1, [r1, #2]                 
  1552c:  ubfx r1, r1, #1, #1               
  15530:  orr.w r0, r0, r1, lsl #26         
  15534:  ldr r1, [pc, #0x44]               -> RAM
  15536:  ldrb r1, [r1, #2]                 
  15538:  ubfx r1, r1, #2, #1               
  1553c:  orr.w r0, r0, r1, lsl #27         
  15540:  ldr r1, [pc, #0x38]               -> RAM
  15542:  ldrb r1, [r1, #2]                 
  15544:  ubfx r1, r1, #3, #1               
  15548:  orr.w r0, r0, r1, lsl #28         
  1554c:  ldr r1, [pc, #0x2c]               -> RAM
  1554e:  ldrb r1, [r1, #3]                 
  15550:  ubfx r1, r1, #4, #1               
  15554:  orr.w r0, r0, r1, lsl #29         
  15558:  ldr r1, [pc, #0x20]               -> RAM
  1555a:  ldrb r1, [r1, #3]                 
  1555c:  ubfx r1, r1, #2, #1               
  15560:  orr.w r0, r0, r1, lsl #30         
  15564:  ldr r1, [pc, #0x14]               -> RAM
  15566:  ldrb r1, [r1, #3]                 
  15568:  lsrs r1, r1, #3                   
  1556a:  orr.w r0, r0, r1, lsl #31         
  1556e:  ldr r1, [pc, #0x10]               -> RAM
  15570:  str r0, [r1]                      
  15572:  pop {r2, r3, r4, r5, r6, pc}      
  ; --- literal-пул @0x15350 (13 слов) ---
  15350:  .word 0x20000080  ; RAM
  15354:  .word 0x20000c98  ; RAM
  15358:  .word 0x20000c90  ; RAM
  1535c:  .word 0x20000c9a  ; RAM
  15360:  .word 0x20000fd3  ; RAM
  15364:  .word 0x20000c9b  ; RAM
  15368:  .word 0x20000fbb  ; RAM
  1536c:  .word 0x20003024  ; RAM
  15370:  .word 0x20000098  ; RAM
  15374:  .word 0x20000f95  ; RAM
  15378:  .word 0x20000fc7  ; RAM
  1537c:  .word 0x20000f70  ; RAM
  15380:  .word 0x2000008c  ; RAM
  ; --- literal-пул @0x15574 (5 слов) — ВНЕ границ функции ---
  15574:  .word 0x20000fc7  ; RAM
  15578:  .word 0x20000f95  ; RAM
  1557c:  .word 0x20000f70  ; RAM
  15580:  .word 0x20000c94  ; RAM
  15584:  .word 0x20000fbb  ; RAM
```
