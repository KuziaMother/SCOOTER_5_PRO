# func_0x09f80

| | |
|---|---|
| offset в файле | `0x09f80` |
| vaddr (база 0x01800000) | `0x01809f80` |
 | размер кода | 488 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005c4 — RAM (r6)
- 0x00206958 — RAM (r8)
- 0x3aa8a8cf — прочее (r4)
- 0x62b88eb8 — прочее (r5)
- 0x6fe561cf — прочее (r7)
- 0xa469c2fd — прочее (r1)
- 0xf6c1d6ab — прочее (r2)

## Вызовы (callees)

- 0x015201d4 (bl, вне списка функций)
- 0x0180998c (b, вне списка функций)
- 0x01809f82 (b, вне списка функций)
- 0x0180a45e (b, вне списка функций)
- 0x0180a822 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01809f80:  push.w {r4, r5, r6, r7, r8, lr}   
  01809f84:  movs r7, #0xb                     
  01809f86:  ldr r6, [pc, #0x5c]               (RAM)
  01809f88:  ldr.w r8, [pc, #0x54]             (RAM)
  01809f8c:  mov.w r5, #0x180                  
  01809f90:  movs r4, #0                       
  01809f92:  movs r2, #1                       
  01809f94:  movs r1, #0x56                    
  01809f96:  ldr.w ip, [r6]                    
  01809f9a:  mov r3, r5                        
  01809f9c:  movs r0, #4                       
  01809f9e:  blx ip                            
  01809fa0:  ldr.w r0, [r8, #4]                
  01809fa4:  movs r2, #1                       
  01809fa6:  add.w r0, r0, r4, lsl #1          
  01809faa:  movs r1, #0x54                    
  01809fac:  ldrh.w r0, [r0, #0x39]            
  01809fb0:  ldr.w ip, [r6]                    
  01809fb4:  add.w r0, r0, #0x8000             
  01809fb8:  uxth r3, r0                       
  01809fba:  movs r0, #4                       
  01809fbc:  blx ip                            
  01809fbe:  adds r5, #8                       
  01809fc0:  adds r4, r4, #1                   
  01809fc2:  uxtb r4, r4                       
  01809fc4:  uxth r5, r5                       
  01809fc6:  cmp r4, r7                        
  01809fc8:  blo #0x1809f92                    
  01809fca:  ldr r4, [r6]                      
  01809fcc:  movs r3, #0x50                    
  01809fce:  mov ip, r4                        
  01809fd0:  pop.w {r4, r5, r6, r7, r8, lr}    
  01809fd4:  movs r2, #1                       
  01809fd6:  movs r1, #0x56                    
  01809fd8:  movs r0, #4                       
  01809fda:  bx ip                             
  01809fdc:  lsls r4, r5, #0x17                
  01809fde:  movs r0, r4                       
  01809fe0:  ldr r0, [r3, #0x14]               
  01809fe2:  movs r0, r4                       
  01809fe4:  lsls r4, r0, #0x17                
  01809fe6:  movs r0, r4                       
  01809fe8:  lsls r1, r0, #8                   
  01809fea:  lsls r3, r0, #0x10                
  01809fec:  lsls r4, r0, #0x14                
  01809fee:  lsls r5, r0, #0x18                
  01809ff0:  lsls r7, r0, #0x1c                
  01809ff2:  movs r0, r1                       
  01809ff4:  .byte 0xff, 0xff                  
  01809ff6:  .byte 0xff, 0xff                  
  01809ff8:  .byte 0xff, 0xff                  
  01809ffa:  .byte 0xff, 0xff                  
  01809ffc:  .byte 0xff, 0xff                  
  01809ffe:  .byte 0xff, 0xff                  
  0180a000:  movs r5, r0                       
  0180a002:  movs r1, #0x81                    
  0180a004:  movs r7, #0x93                    
  0180a006:  movs r0, r0                       
  0180a008:  cbz r0, #0x180a06e                
  0180a00a:  movs r1, r0                       
  0180a00c:  str r5, [r5, #0x74]               
  0180a00e:  rsbs.w r3, lr, #0x3e3e3e3e        
  0180a012:  asrs r0, r5, #7                   
  0180a014:  lsls r1, r6, #0xa                 
  0180a016:  cmp r5, #0x4d                     
  0180a018:  lsrs r4, r6, #0x13                
  0180a01a:  lsls r6, r3, #7                   
  0180a01c:  asrs r1, r4, #0x20                
  0180a01e:  .byte 0x00, 0xc0                  
  0180a020:  movs r1, r0                       
  0180a022:  movs r0, r0                       
  0180a024:  movs r4, #0xfc                    
  0180a026:  vselge.f16 s25, s18, s7           
  0180a02a:  .byte 0x1b, 0xfe                  
  0180a02c:  ldrh r3, [r7, r0]                 
  0180a02e:  .byte 0x87, 0xba                  
  0180a030:  adr r6, #0x3f0                    
  0180a032:  subs r4, r6, r1                   
  0180a034:  pop {r0, r6, r7}                  
  0180a036:  asrs r7, r3, #6                   
  0180a038:  str r6, [sp, #0x3cc]              
  0180a03a:  ldr r7, [pc, #0x2f4]              
  0180a03c:  lsrs r2, r0, #0xe                 
  0180a03e:  adds r1, #0xa0                    
  0180a040:  adds r2, r7, r2                   
  0180a042:  bvs #0x180a040                    
  0180a044:  .byte 0xff, 0xff                  
  0180a046:  .byte 0xff, 0xff                  
  0180a048:  .byte 0xff, 0xff                  
  0180a04a:  .byte 0xff, 0xff                  
  0180a04c:  .byte 0xff, 0xff                  
  0180a04e:  .byte 0xff, 0xff                  
  0180a050:  .byte 0xff, 0xff                  
  0180a052:  .byte 0xff, 0xff                  
  0180a054:  .byte 0xff, 0xff                  
  0180a056:  .byte 0xff, 0xff                  
  0180a058:  .byte 0xff, 0xff                  
  0180a05a:  .byte 0xff, 0xff                  
  0180a05c:  .byte 0xff, 0xff                  
  0180a05e:  .byte 0xff, 0xff                  
  0180a060:  .byte 0x00, 0xff                  
  0180a062:  .byte 0xfd, 0xff                  
  0180a064:  ands r0, r0                       
  0180a066:  cmp r3, #0x4d                     
  0180a068:  lsls r5, r3, #1                   
  0180a06a:  movs r0, r2                       
  0180a06c:  movs r0, r0                       
  0180a06e:  lsls r0, r0, #1                   
  0180a070:  movs r0, r0                       
  0180a072:  movs r0, r0                       
  0180a074:  movs r0, r0                       
  0180a076:  ldrb r2, [r0, #0x1c]              
  0180a078:  ldr r4, [r7, r7]                  
  0180a07a:  ldrsh r0, [r1, r1]                
  0180a07c:  lsls r1, r5, #0x10                
  0180a07e:  ldrh r6, [r7, #0x16]              
  0180a080:  str r0, [sp, #0x1fc]              
  0180a082:  strh r6, [r1, #0x24]              
  0180a084:  ldr r4, [pc, #0xc4]               
  0180a086:  .byte 0x27, 0xb8                  
  0180a088:  .byte 0x03, 0xf9                  
  0180a08a:  add r3, sp, #0x2d8                
  0180a08c:  ldrb r0, [r7, #0x16]              
  0180a08e:  str r5, [r2, r5]                  
  0180a090:  ldr r2, [sp, #0xc0]               
  0180a092:  strh r4, [r4, #0x38]              
  0180a094:  str r5, [r7, #0x64]               
  0180a096:  movs r5, #0x9e                    
  0180a098:  ldm r7!, {r1, r2, r3, r4}         
  0180a09a:  adds r1, #0xf6                    
  0180a09c:  lsrs r0, r1, #0x1d                
  0180a09e:  bvc #0x180a0dc                    
  0180a0a0:  b #0x180a822                      -> 0x0a822 (вне списка функций)
  0180a0a2:  bl #0x15201d4                     
  0180a0a6:  strb r7, [r1, r3]                 
  0180a0a8:  stm r6!, {r0, r1, r2, r4, r5}     
  0180a0aa:  .byte 0x9e, 0xb6                  
  0180a0ac:  asrs r0, r2, #0x10                
  0180a0ae:  subs r3, r0, r3                   
  0180a0b0:  ldr r7, [sp, #0x154]              
  0180a0b2:  .byte 0xe6, 0xf3                  
  0180a0b4:  movs r3, #0x92                    
  0180a0b6:  b #0x180a45e                      -> 0x0a45e (вне списка функций)
  0180a0b8:  ldrb r1, [r0, r2]                 
  0180a0ba:  ldrh r6, [r3, r4]                 
  0180a0bc:  stm r5!, {r1, r2, r3, r5, r7}     
  0180a0be:  strb r6, [r5, #0x1f]              
  0180a0c0:  ldr r5, [pc, #0x1a4]              
  0180a0c2:  ldrb r6, [r2, #0x16]              
  0180a0c4:  str r3, [r2, #0xc]                
  0180a0c6:  ldr r2, [r1, #0x18]               
  0180a0c8:  .byte 0x23, 0xb6                  
  0180a0ca:  ldrb r4, [r3, #0x1a]              
  0180a0cc:  movs r4, #0xd8                    
  0180a0ce:  udf #0x9b                         
  0180a0d0:  lsrs r4, r5, #0xc                 
  0180a0d2:  asrs r6, r1, #5                   
  0180a0d4:  adds r5, #0x28                    
  0180a0d6:  strh r4, [r4, #0x1e]              
  0180a0d8:  strh r3, [r7, #0x1e]              
  0180a0da:  movs r2, #0xd9                    
  0180a0dc:  ldm r3!, {r0, r1, r6, r7}         
  0180a0de:  cmp r5, #0xdb                     
  0180a0e0:  ldrb r0, [r6, #0xf]               
  0180a0e2:  ldr r2, [pc, #0x2dc]              
  0180a0e4:  bkpt #0xb8                        
  0180a0e6:  strh r4, [r4, #0x36]              
  0180a0e8:  ldr r5, [sp, #0x300]              
  0180a0ea:  str r6, [r2, r2]                  
  0180a0ec:  stm r5!, {r0, r1, r2, r7}         
  0180a0ee:  str r6, [sp, #0xe4]               
  0180a0f0:  .byte 0xfb, 0xf0                  
  0180a0f2:  subs r4, #0xf                     
  0180a0f4:  ldm r6!, {r1, r2, r5, r7}         
  0180a0f6:  bpl #0x180a142                    
  0180a0f8:  str r6, [sp, #0x324]              
  0180a0fa:  ldr r2, [sp, #0x2ac]              
  0180a0fc:  .byte 0x97, 0xba                  
  0180a0fe:  b #0x180998c                      -> 0x0998c (вне списка функций)
  0180a100:  .byte 0x59, 0xe8                  
  0180a102:  ble #0x180a0c6                    
  0180a104:  .byte 0x87, 0xb6                  
  0180a106:  bge #0x180a198                    
  0180a108:  cbnz r3, #0x180a10c               
  0180a10a:  strh r3, [r0, r7]                 
  0180a10c:  ldrsb r4, [r5, r4]                
  0180a10e:  bgt.w #0x18426e4                  
  0180a112:  cmp r2, r5                        
  0180a114:  str r1, [r5, #0x48]               
  0180a116:  ldr r4, [sp, #0xac]               
  0180a118:  lsrs r1, r5, #0x1c                
  0180a11a:  cmp r0, #0x95                     
  0180a11c:  str r6, [r3]                      
  0180a11e:  strh r6, [r4, #0x32]              
  0180a120:  ldrb r1, [r6, #0x1a]              
  0180a122:  subs r6, #0x6e                    
  0180a124:  itett vs                          
  0180a126:  cbz r2, #0x180a15c                
  0180a128:  addvc sp, #0x68                   
  0180a12a:  strvs r2, [sp, #0x3a8]            
  0180a12c:  bvs #0x180a070                    
  0180a12e:  bge #0x180a190                    
  0180a130:  str r3, [sp, #0x39c]              
  0180a132:  asrs r7, r3, #5                   
  0180a134:  cmp r3, #0x5b                     
  0180a136:  ldm r4, {r2, r4, r5}              
  0180a138:  smlalbb r2, r7, r5, sl            
  0180a13c:  strb r3, [r0, #6]                 
  0180a13e:  cmp r6, #0x15                     
  0180a140:  ldr r1, [pc, #0x338]              
  0180a142:  blx #0x9c4d5c                     
  0180a146:  cmp fp, r6                        
  0180a148:  lsrs r5, r6, #0x1b                
  0180a14a:  asrs r5, r0, #0xc                 
  0180a14c:  add r0, sp, #0x33c                
  0180a14e:  subs r2, #0xa8                    
  0180a150:  blt #0x180a0e4                    
  0180a152:  cmp r6, #0x38                     
  0180a154:  ldrb r1, [r7, #0x1f]              
  0180a156:  strh r7, [r2, r5]                 
  0180a158:  ldm r6, {r2, r5, r6, r7}          
  0180a15a:  ldrh r4, [r5, #0x2a]              
  0180a15c:  str r1, [sp, #0x4c]               
  0180a15e:  svc #0x8e                         
  0180a160:  adds r5, #0x85                    
  0180a162:  str r7, [sp, #0x3dc]              
  0180a164:  .byte 0xe3, 0xb7                  
  0180a166:  b #0x1809f82                      -> 0x09f82 (вне списка функций)
  ; --- literal-пул @0x09fe0 (2 слов) ---
  09fe0:  .word 0x00206958  ; RAM
  09fe4:  .word 0x002005c4  ; RAM
  ; --- literal-пул @0x0a14c (1 слов) ---
  0a14c:  .word 0x3aa8a8cf
  ; --- literal-пул @0x0a268 (1 слов) — ВНЕ границ функции ---
  0a268:  .word 0x62b88eb8
  ; --- literal-пул @0x0a330 (1 слов) — ВНЕ границ функции ---
  0a330:  .word 0x6fe561cf
  ; --- literal-пул @0x0a3c0 (1 слов) — ВНЕ границ функции ---
  0a3c0:  .word 0xf6c1d6ab
  ; --- literal-пул @0x0a47c (1 слов) — ВНЕ границ функции ---
  0a47c:  .word 0xa469c2fd
```
