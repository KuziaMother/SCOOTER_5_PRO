# func_0x07dea

| | |
|---|---|
| offset в файле | `0x07dea` |
| vaddr (база 0x01800000) | `0x01807dea` |
 | размер кода | 990 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002007c4 — RAM (r1)
- 0x00202044 — RAM (r0)
- 0x00fa0d1d — прочее (r0)
- 0x00fa0ede — прочее (r0)
- 0x40051000 — периферия (r0)

## Вызовы (callees)

- 0x015f5fa4 (bl, вне списка функций)
- 0x0161484c (bl, вне списка функций)
- 0x01614866 (bl, вне списка функций)
- 0x0161fa50 (bl, вне списка функций)
- 0x0161faa2 (bl, вне списка функций)
- 0x01621dfa (bl, вне списка функций)
- 0x01807f42 (b, вне списка функций)
- 0x01807fb0 (b, вне списка функций)
- 0x01808130 (b, вне списка функций)
- 0x01808166 (b, вне списка функций)
- 0x018081a0 (b, вне списка функций)
- 0x018081c2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01807dea:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01807dee:  sub sp, #0x84                     
  01807df0:  movs r4, #0                       
  01807df2:  mov r8, r0                        
  01807df4:  ldr r0, [pc, #0x314]              (RAM)
  01807df6:  str r4, [sp, #0x70]               
  01807df8:  str r4, [sp, #0x54]               
  01807dfa:  add.w r0, r0, r8, lsl #2          
  01807dfe:  str r4, [sp, #0x10]               
  01807e00:  str r4, [sp, #0xc]                
  01807e02:  str r4, [sp, #8]                  
  01807e04:  str r4, [sp, #0x14]               
  01807e06:  str r4, [sp, #4]                  
  01807e08:  ldr.w sl, [r0, #0x210]            
  01807e0c:  sub.w r0, r8, #8                  
  01807e10:  sxtb r0, r0                       
  01807e12:  str r0, [sp, #0x3c]               
  01807e14:  rsb r0, r0, r0, lsl #4            
  01807e18:  movw r1, #0xffff                  
  01807e1c:  and.w r0, r1, r0, lsl #1          
  01807e20:  str r0, [sp]                      
  01807e22:  movs r0, #0                       
  01807e24:  mov sb, r0                        
  01807e26:  str r0, [sp, #0x24]               
  01807e28:  str r0, [sp, #0x20]               
  01807e2a:  str r0, [sp, #0x1c]               
  01807e2c:  ldr.w r0, [sl]                    
  01807e30:  movs r7, #7                       
  01807e32:  ubfx r0, r0, #0x1b, #2            
  01807e36:  str r0, [sp, #0x68]               
  01807e38:  ldr r0, [sp, #0x3c]               
  01807e3a:  mov fp, r4                        
  01807e3c:  mov r5, r4                        
  01807e3e:  cmp r0, #0                        
  01807e40:  blt #0x1807f40                    
  01807e42:  ldrb.w r0, [sl, #0xc]             
  01807e46:  lsls r0, r0, #0x1d                
  01807e48:  bpl #0x1807f40                    
  01807e4a:  ldrh.w r0, [sl, #0x2c]            
  01807e4e:  and.w r0, r1, r0, lsl #1          
  01807e52:  str r0, [sp, #0x40]               
  01807e54:  bl #0x161484c                     
  01807e58:  str r0, [sp, #0x34]               
  01807e5a:  ldr r0, [sp, #0x3c]               
  01807e5c:  lsls r1, r0, #1                   
  01807e5e:  ldr r0, [pc, #0x2bc]              (периферия)
  01807e60:  add r0, r1                        
  01807e62:  str r0, [sp, #0x48]               
  01807e64:  ldrh.w r1, [r0, #0x232]           
  01807e68:  movs r0, #1                       
  01807e6a:  cmp.w r0, r1, lsr #14             
  01807e6e:  beq #0x1807e7c                    
  01807e70:  ldr r0, [sp, #0x34]               
  01807e72:  add sp, #0x84                     
  01807e74:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01807e78:  b.w #0x1614866                    
  01807e7c:  ldr r0, [sp]                      
  01807e7e:  bl #0x161fa50                     
  01807e82:  str r0, [sp, #0x7c]               
  01807e84:  ldr r0, [sp]                      
  01807e86:  adds r0, r0, #4                   
  01807e88:  str r0, [sp, #0x38]               
  01807e8a:  uxth r0, r0                       
  01807e8c:  bl #0x161fa50                     
  01807e90:  str r0, [sp, #0x2c]               
  01807e92:  str r0, [sp, #0x30]               
  01807e94:  ldr r0, [sp]                      
  01807e96:  adds r0, #0x14                    
  01807e98:  str r0, [sp, #0x64]               
  01807e9a:  uxth r0, r0                       
  01807e9c:  bl #0x161fa50                     
  01807ea0:  str r0, [sp, #0x44]               
  01807ea2:  ldr r0, [sp]                      
  01807ea4:  adds r0, #0x15                    
  01807ea6:  str r0, [sp, #0x60]               
  01807ea8:  uxth r0, r0                       
  01807eaa:  bl #0x161fa50                     
  01807eae:  str r0, [sp, #0x28]               
  01807eb0:  ldr r0, [sp]                      
  01807eb2:  adds r0, #0x16                    
  01807eb4:  str r0, [sp, #0x58]               
  01807eb6:  uxth r0, r0                       
  01807eb8:  bl #0x161fa50                     
  01807ebc:  str r0, [sp, #0x6c]               
  01807ebe:  ldr r0, [sp, #0x30]               
  01807ec0:  lsrs r0, r0, #0x10                
  01807ec2:  str r0, [sp, #0x18]               
  01807ec4:  ldr r0, [pc, #0x244]              (RAM)
  01807ec6:  ldr r1, [sp, #0x68]               
  01807ec8:  add r0, r1                        
  01807eca:  ldrb.w r0, [r0, #0x1f6]           
  01807ece:  cmp r0, r8                        
  01807ed0:  bne #0x1807ef2                    
  01807ed2:  ldrh.w r1, [sl, #0xac]            
  01807ed6:  ldr r0, [sp, #0x18]               
  01807ed8:  cmp r1, r0                        
  01807eda:  bne #0x1807ef2                    
  01807edc:  str r0, [sp]                      
  01807ede:  ldr r0, [pc, #0x228]              
  01807ee0:  movw r3, #0xcc03                  
  01807ee4:  movs r2, #2                       
  01807ee6:  movw r1, #0x23ad                  
  01807eea:  adds r0, #0xf0                    
  01807eec:  bl #0x15f5fa4                     
  01807ef0:  b #0x1808166                      -> 0x08166 (вне списка функций)
  01807ef2:  ldr r0, [sp, #0x6c]               
  01807ef4:  ubfx r0, r0, #0, #0x12            
  01807ef8:  str r0, [sp, #8]                  
  01807efa:  ldr r0, [sp, #0x44]               
  01807efc:  ubfx r0, r0, #0xa, #0x10          
  01807f00:  str r0, [sp, #0x50]               
  01807f02:  ldr r0, [sp, #0x44]               
  01807f04:  ubfx r0, r0, #0, #0xa             
  01807f08:  str r0, [sp, #0x4c]               
  01807f0a:  ldr r0, [sp, #0x28]               
  01807f0c:  ubfx r0, r0, #0, #0xc             
  01807f10:  str r0, [sp, #0x5c]               
  01807f12:  ldr r0, [sp, #0x28]               
  01807f14:  ubfx r0, r0, #0xc, #6             
  01807f18:  str r0, [sp, #0x70]               
  01807f1a:  ldr r0, [sp, #0x28]               
  01807f1c:  ubfx r0, r0, #0x12, #3            
  01807f20:  lsls r1, r0, #6                   
  01807f22:  ldr r0, [sp, #0x44]               
  01807f24:  orr.w r6, r1, r0, lsr #26         
  01807f28:  ldr r1, [pc, #0x1f4]              (RAM)
  01807f2a:  ldr r0, [sp, #0x3c]               
  01807f2c:  ldr r1, [r1]                      
  01807f2e:  uxtb r0, r0                       
  01807f30:  blx r1                            
  01807f32:  str r0, [sp, #0x54]               
  01807f34:  ldrh.w r1, [sl, #0x66]            
  01807f38:  ldr r0, [sp, #0x18]               
  01807f3a:  cmp r1, r0                        
  01807f3c:  bne #0x1807f46                    
  01807f3e:  b #0x1807f42                      -> 0x07f42 (вне списка функций)
  01807f40:  b #0x18081c2                      -> 0x081c2 (вне списка функций)
  01807f42:  movs r7, #8                       
  01807f44:  b #0x1808166                      -> 0x08166 (вне списка функций)
  01807f46:  ldr r1, [sp, #0x54]               
  01807f48:  ldr r0, [sp, #8]                  
  01807f4a:  bl #0x1621dfa                     
  01807f4e:  lsls r1, r0, #0xe                 
  01807f50:  bpl #0x1807f56                    
  01807f52:  movs r7, #1                       
  01807f54:  b #0x1808166                      -> 0x08166 (вне списка функций)
  01807f56:  ldr r1, [sp, #0x40]               
  01807f58:  cmp r0, r1                        
  01807f5a:  bhi #0x1807f60                    
  01807f5c:  movs r7, #2                       
  01807f5e:  b #0x1808166                      -> 0x08166 (вне списка функций)
  01807f60:  ldr r2, [pc, #0x1b8]              (периферия)
  01807f62:  ldrh.w r1, [r2, #0x210]           
  01807f66:  ldrh.w r2, [r2, #0x212]           
  01807f6a:  ubfx r2, r2, #0xa, #4             
  01807f6e:  lsls r2, r2, #6                   
  01807f70:  orr.w r1, r2, r1, lsr #10         
  01807f74:  ldr r2, [sp, #0x40]               
  01807f76:  udiv r8, r0, r2                   
  01807f7a:  sub.w r2, r6, r8                  
  01807f7e:  uxth r5, r2                       
  01807f80:  ldr r2, [sp, #0x4c]               
  01807f82:  muls r2, r5, r2                   
  01807f84:  sdiv r2, r2, r6                   
  01807f88:  uxth.w fp, r2                     
  01807f8c:  ldr r2, [sp, #0x50]               
  01807f8e:  muls r2, r5, r2                   
  01807f90:  sdiv r2, r2, r6                   
  01807f94:  uxth r4, r2                       
  01807f96:  ldr r2, [sp, #0x50]               
  01807f98:  cmp r4, r2                        
  01807f9a:  bhs #0x1807fa0                    
  01807f9c:  adds r4, r4, #1                   
  01807f9e:  uxth r4, r4                       
  01807fa0:  mov r2, r4                        
  01807fa2:  add r1, fp                        
  01807fa4:  mov.w r3, #0x270                  
  01807fa8:  b #0x1807fb0                      -> 0x07fb0 (вне списка функций)
  01807faa:  subw r1, r1, #0x271               
  01807fae:  adds r2, r2, #1                   
  01807fb0:  cmp r1, r3                        
  01807fb2:  bhi #0x1807faa                    
  01807fb4:  ldr r1, [sp, #0x40]               
  01807fb6:  adds r2, r2, #3                   
  01807fb8:  udiv r3, r0, r1                   
  01807fbc:  mls r0, r1, r3, r0                
  01807fc0:  cmp r0, r2                        
  01807fc2:  bhs #0x1807ff6                    
  01807fc4:  sub.w r8, r8, #1                  
  01807fc8:  cmp.w r8, #0                      
  01807fcc:  bgt #0x1807fd2                    
  01807fce:  movs r7, #3                       
  01807fd0:  b #0x1808166                      -> 0x08166 (вне списка функций)
  01807fd2:  adds r5, r5, #1                   
  01807fd4:  ldr r0, [sp, #0x4c]               
  01807fd6:  uxth r5, r5                       
  01807fd8:  muls r0, r5, r0                   
  01807fda:  sdiv r0, r0, r6                   
  01807fde:  uxth.w fp, r0                     
  01807fe2:  ldr r0, [sp, #0x50]               
  01807fe4:  muls r0, r5, r0                   
  01807fe6:  sdiv r0, r0, r6                   
  01807fea:  uxth r4, r0                       
  01807fec:  ldr r0, [sp, #0x50]               
  01807fee:  cmp r4, r0                        
  01807ff0:  bhs #0x1807ff6                    
  01807ff2:  adds r4, r4, #1                   
  01807ff4:  uxth r4, r4                       
  01807ff6:  cmp r6, r8                        
  01807ff8:  bge #0x1807ffe                    
  01807ffa:  movs r7, #4                       
  01807ffc:  b #0x1808166                      -> 0x08166 (вне списка функций)
  01807ffe:  ldr r0, [sp, #0x70]               
  01808000:  muls r0, r5, r0                   
  01808002:  udiv r0, r0, r6                   
  01808006:  str r0, [sp, #0xc]                
  01808008:  ldr r0, [sp, #0x5c]               
  0180800a:  ldr r1, [sp, #0x5c]               
  0180800c:  muls r0, r5, r0                   
  0180800e:  udiv r0, r0, r6                   
  01808012:  str r0, [sp, #0x10]               
  01808014:  cmp r0, r1                        
  01808016:  bhs #0x180801c                    
  01808018:  adds r0, r0, #1                   
  0180801a:  str r0, [sp, #0x10]               
  0180801c:  ldr r2, [sp, #0x40]               
  0180801e:  ldr r0, [sp, #8]                  
  01808020:  mls r0, r8, r2, r0                
  01808024:  ubfx r0, r0, #0, #0x12            
  01808028:  str r0, [sp, #4]                  
  0180802a:  ldr r0, [sp, #0x18]               
  0180802c:  ldr r1, [sp, #0x7c]               
  0180802e:  sub.w r0, r0, r8                  
  01808032:  uxth r0, r0                       
  01808034:  str r0, [sp, #0x14]               
  01808036:  ldr r0, [sp, #4]                  
  01808038:  ldr r2, [sp, #0x2c]               
  0180803a:  bfi r1, r0, #4, #0x12             
  0180803e:  ldr r0, [sp, #0x14]               
  01808040:  bfi r2, r0, #0x10, #0x10          
  01808044:  ldr r0, [sp, #0x44]               
  01808046:  str r2, [sp, #0x2c]               
  01808048:  bfi r0, r5, #0x1a, #6             
  0180804c:  orr.w r2, fp, r4, lsl #10         
  01808050:  bfi r0, r2, #0, #0x1a             
  01808054:  str r0, [sp, #0x30]               
  01808056:  ldr r0, [sp, #0x28]               
  01808058:  lsrs r2, r5, #6                   
  0180805a:  bfi r0, r2, #0x12, #3             
  0180805e:  ldr r2, [sp, #0x10]               
  01808060:  bfi r0, r2, #0, #0xc              
  01808064:  ldr r2, [sp, #0xc]                
  01808066:  bfi r0, r2, #0xc, #6              
  0180806a:  str r0, [sp, #0x28]               
  0180806c:  ldr r2, [sp, #0x6c]               
  0180806e:  ldr r0, [sp, #4]                  
  01808070:  bfi r2, r0, #0, #0x12             
  01808074:  str r2, [sp, #0x44]               
  01808076:  ldr r0, [sp]                      
  01808078:  bl #0x161faa2                     
  0180807c:  cbnz r0, #0x18080f8               
  0180807e:  ldr r0, [sp, #0x38]               
  01808080:  ldr r1, [sp, #0x2c]               
  01808082:  uxth r0, r0                       
  01808084:  bl #0x161faa2                     
  01808088:  cbnz r0, #0x18080f8               
  0180808a:  ldr r0, [sp, #0x64]               
  0180808c:  ldr r1, [sp, #0x30]               
  0180808e:  uxth r0, r0                       
  01808090:  bl #0x161faa2                     
  01808094:  cbnz r0, #0x18080f8               
  01808096:  ldr r0, [sp, #0x60]               
  01808098:  ldr r1, [sp, #0x28]               
  0180809a:  uxth r0, r0                       
  0180809c:  bl #0x161faa2                     
  018080a0:  cbnz r0, #0x18080f8               
  018080a2:  ldr r0, [sp, #0x58]               
  018080a4:  ldr r1, [sp, #0x44]               
  018080a6:  uxth r0, r0                       
  018080a8:  bl #0x161faa2                     
  018080ac:  cbnz r0, #0x18080f8               
  018080ae:  ldr r0, [sp, #0x14]               
  018080b0:  strh.w r0, [sl, #0x66]            
  018080b4:  ldr r0, [sp, #0x48]               
  018080b6:  ldr.w sl, [pc, #0x64]             (периферия)
  018080ba:  ldrh.w r2, [r0, #0x232]           
  018080be:  ldrh.w r1, [r0, #0x238]           
  018080c2:  ldr r0, [sp, #0x50]               
  018080c4:  ubfx ip, r1, #0xa, #4             
  018080c8:  subs r0, r0, r4                   
  018080ca:  uxth r3, r0                       
  018080cc:  mov r7, r2                        
  018080ce:  ldr r0, [sp, #0x4c]               
  018080d0:  bfi r7, ip, #0xe, #0x12           
  018080d4:  mov ip, r8                        
  018080d6:  ldr.w r8, [sp, #0x40]             
  018080da:  str r7, [sp, #0x24]               
  018080dc:  mls r7, ip, r8, r7                
  018080e0:  add.w sb, r7, r3                  
  018080e4:  sub.w r0, r0, fp                  
  018080e8:  ubfx r3, r1, #0, #0xa             
  018080ec:  uxth r0, r0                       
  018080ee:  str r3, [sp, #0x20]               
  018080f0:  cmp r3, r0                        
  018080f2:  blo #0x1808124                    
  018080f4:  subs r0, r3, r0                   
  018080f6:  b #0x1808130                      -> 0x08130 (вне списка функций)
  018080f8:  b #0x1808166                      -> 0x08166 (вне списка функций)
  018080fa:  movs r0, r0                       
  018080fc:  ldm r7, {r1, r2, r4, r7}          
  018080fe:  movs r5, r0                       
  01808100:  strh r7, [r7, #0x3e]              
  01808102:  movs r3, #0x99                    
  01808104:  b #0x18081a0                      -> 0x081a0 (вне списка функций)
  01808106:  vmul.f32 d0, d0, d13              
  0180810a:  lsls r2, r7, #3                   
  0180810c:  movs r0, #0x44                    
  0180810e:  movs r0, r4                       
  01808110:  ldr r0, [r7]                      
  01808112:  movs r0, r4                       
  01808114:  subs r4, r1, r7                   
  01808116:  movs r0, r4                       
  01808118:  subs r0, r2, r7                   
  0180811a:  movs r0, r4                       
  0180811c:  asrs r0, r0, #0x20                
  0180811e:  ands r5, r0                       
  01808120:  lsls r4, r0, #0x1f                
  01808122:  movs r0, r4                       
  01808124:  ldr r3, [sp, #0x20]               
  01808126:  add.w sb, sb, #1                  
  0180812a:  subs r0, r3, r0                   
  0180812c:  addw r0, r0, #0x271               
  01808130:  uxth r0, r0                       
  01808132:  str r0, [sp, #0x1c]               
  01808134:  lsr.w r0, sb, #0xe                
  01808138:  bfi r1, r0, #0xa, #4              
  0180813c:  ldr r3, [sp, #0x48]               
  0180813e:  ldr r0, [sp, #0x1c]               
  01808140:  bfi r2, sb, #0, #0xe              
  01808144:  bfi r1, r0, #0, #0xa              
  01808148:  strh.w r2, [r3, #0x232]           
  0180814c:  ldr r2, [sp, #0x48]               
  0180814e:  strh.w r1, [r2, #0x238]           
  01808152:  movs r1, #1                       
  01808154:  strh.w r1, [sl, #0x254]           
  01808158:  ldr r1, [pc, #0x3e0]              (RAM)
  0180815a:  ldr r0, [sp, #0x3c]               
  0180815c:  ldr r1, [r1]                      
  0180815e:  uxtb r0, r0                       
  01808160:  blx r1                            
  01808162:  movs r7, #0                       
  01808164:  str r0, [sp, #0x54]               
  01808166:  ldr r0, [sp, #0x34]               
  01808168:  bl #0x1614866                     
  0180816c:  cbz r7, #0x1808172                
  0180816e:  cmp r7, #7                        
  01808170:  bne #0x18081c2                    
  01808172:  add r3, sp, #0x14                 
  01808174:  add.w r8, sp, #4                  
  01808178:  ldm.w r3, {r0, r1, r2}            
  0180817c:  strd r1, r0, [sp, #0x44]          
  01808180:  strd sb, r2, [sp, #0x3c]          
  01808184:  ldrd r0, r1, [sp, #0x20]          
  01808188:  strd r1, r0, [sp, #0x34]          
  0180818c:  strd r6, r5, [sp, #0x2c]          
  01808190:  ldm.w r8, {r0, r1, r2, r3}        
  01808194:  strd r1, r0, [sp, #0x24]          
  01808198:  strd r3, r2, [sp, #0x1c]          
  0180819c:  ldr r1, [sp, #0x70]               
  0180819e:  ldr r2, [sp, #0x5c]               
  018081a0:  strd r2, r1, [sp, #0x14]          
  018081a4:  strd r4, fp, [sp, #0xc]           
  018081a8:  add r3, sp, #0x4c                 
  018081aa:  ldm.w r3, {r0, r1, r2}            
  018081ae:  strd r2, r1, [sp]                 
  018081b2:  str r0, [sp, #8]                  
  018081b4:  mov r3, r7                        
  018081b6:  movs r2, #0x14                    
  018081b8:  mov.w r1, #0xd10                  
  018081bc:  ldr r0, [pc, #0x380]              
  018081be:  bl #0x15f5fa4                     
  018081c2:  add sp, #0x84                     
  018081c4:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x08108 (2 слов) ---
  08108:  .word 0x00fa0d1d
  0810c:  .word 0x00202044  ; RAM
  ; --- literal-пул @0x0811c (2 слов) ---
  0811c:  .word 0x40051000  ; периферия
  08120:  .word 0x002007c4  ; RAM
  ; --- literal-пул @0x0853c (2 слов) — ВНЕ границ функции ---
  0853c:  .word 0x002007c4  ; RAM
  08540:  .word 0x00fa0ede
```
