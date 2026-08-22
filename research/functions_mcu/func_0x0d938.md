# func_0x0d938

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d938) | `0x0000d938` |
| размер кода | 970 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000098 — RAM (r0)
- 0x20000f70 — RAM (r1)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r1)
- 0x20000fc7 — RAM (r1)
- 0x20000fd3 — RAM (r0)
- 0x20001344 — RAM (r0)
- 0x20001359 — RAM (r0)
- 0x20003024 — RAM (r1)
- 0x2000305c — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x08a90` (0x00008a90, bl)
- 0x0da52 (b, вне списка функций)
- 0x0dac8 (b, вне списка функций)
- 0x0db28 (b, вне списка функций)
- 0x0dc92 (b, вне списка функций)
- 0x0dcf0 (b, вне списка функций)
- `func_0x157e0` (0x000157e0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x110fc` (bl @0x000111b0)
- `func_0x14f50` (bl @0x00014fbc)
- `func_0x14f50` (bl @0x00015020)
- `func_0x14f50` (bl @0x00015292)
- `func_0x14f50` (bl @0x0001542c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d952..0x0da50` (254 Б); цели из: 0x0d94c
- `0x0da50..0x0da52` (2 Б); цели из: 0x0d950
- `0x0da52..0x0dac8` (118 Б); цели из: 0x0da4e
- `0x0dac8..0x0db28` (96 Б); цели из: 0x0dac4
- `0x0db28..0x0dc92` (362 Б); цели из: 0x0da50
- `0x0dc92..0x0dcf0` (94 Б); цели из: 0x0dc8e
- `0x0dcf0..0x0dd02` (18 Б); цели из: 0x0d948, 0x0db26

## Дизассембляция

```asm
  0d938:  push {r2, r3, r4, lr}             
  0d93a:  mov r4, r0                        
  0d93c:  cbnz r4, #0xd94a                  
  0d93e:  movs r2, #0x28                    
  0d940:  ldr r1, [pc, #0x3c0]              -> RAM
  0d942:  ldr r0, [pc, #0x3c4]              -> RAM
  0d944:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0d948:  b #0xdcf0                         -> 0x0dcf0 (вне списка функций)
  0d94a:  cmp r4, #8                        
  0d94c:  beq #0xd952                       
  0d94e:  cmp r4, #9                        
  0d950:  bne #0xda50                       
  0d952:  ldr r0, [pc, #0x3b4]              -> RAM
  0d954:  strh r4, [r0]                     
  0d956:  mov r0, sp                        
  0d958:  bl #0x8a90                        -> func_0x08a90
  0d95c:  ldr r0, [pc, #0x3ac]              -> RAM
  0d95e:  ldr r1, [sp]                      
  0d960:  str r1, [r0]                      
  0d962:  ldrh.w r1, [sp, #4]               
  0d966:  strh r1, [r0, #4]                 
  0d968:  ldrb.w r1, [sp, #6]               
  0d96c:  strb r1, [r0, #6]                 
  0d96e:  ldrb r1, [r0, #5]                 
  0d970:  ldr r0, [pc, #0x394]              -> RAM
  0d972:  strb r1, [r0, #7]                 
  0d974:  ldr r0, [pc, #0x394]              -> RAM
  0d976:  ldrb r1, [r0, #4]                 
  0d978:  ldr r0, [pc, #0x38c]              -> RAM
  0d97a:  strb r1, [r0, #6]                 
  0d97c:  ldr r0, [pc, #0x38c]              -> RAM
  0d97e:  ldrb r1, [r0, #3]                 
  0d980:  ldr r0, [pc, #0x384]              -> RAM
  0d982:  strb r1, [r0, #5]                 
  0d984:  ldr r0, [pc, #0x384]              -> RAM
  0d986:  ldrb r1, [r0, #2]                 
  0d988:  ldr r0, [pc, #0x37c]              -> RAM
  0d98a:  strb r1, [r0, #4]                 
  0d98c:  ldr r0, [pc, #0x37c]              -> RAM
  0d98e:  ldrb r1, [r0, #1]                 
  0d990:  ldr r0, [pc, #0x374]              -> RAM
  0d992:  strb r1, [r0, #3]                 
  0d994:  ldr r0, [pc, #0x374]              -> RAM
  0d996:  ldrb r0, [r0]                     
  0d998:  ldr r1, [pc, #0x36c]              -> RAM
  0d99a:  strb r0, [r1, #2]                 
  0d99c:  ldr r0, [pc, #0x370]              -> RAM
  0d99e:  ldr r0, [r0, #8]                  
  0d9a0:  str r0, [r1, #8]                  
  0d9a2:  ldr r0, [pc, #0x370]              -> RAM
  0d9a4:  ldrh.w r0, [r0, #1]               
  0d9a8:  strh r0, [r1, #0xc]               
  0d9aa:  ldr r0, [pc, #0x368]              -> RAM
  0d9ac:  ldrh.w r0, [r0, #3]               
  0d9b0:  strh r0, [r1, #0xe]               
  0d9b2:  ldr r0, [pc, #0x35c]              -> RAM
  0d9b4:  ldr r0, [r0, #0xc]                
  0d9b6:  str r0, [r1, #0x10]               
  0d9b8:  ldr r0, [pc, #0x358]              -> RAM
  0d9ba:  ldrb r0, [r0, #0x10]              
  0d9bc:  sxtb r0, r0                       
  0d9be:  strb r0, [r1, #0x14]              
  0d9c0:  ldr r0, [pc, #0x350]              -> RAM
  0d9c2:  ldrb r0, [r0, #0x17]              
  0d9c4:  sxtb r0, r0                       
  0d9c6:  strb r0, [r1, #0x15]              
  0d9c8:  ldr r0, [pc, #0x34c]              -> RAM
  0d9ca:  ldrh r0, [r0, #2]                 
  0d9cc:  strh r0, [r1, #0x16]              
  0d9ce:  ldr r0, [pc, #0x348]              -> RAM
  0d9d0:  ldr r0, [r0, #0xc]                
  0d9d2:  str r0, [r1, #0x18]               
  0d9d4:  ldr r0, [pc, #0x340]              -> RAM
  0d9d6:  ldr r0, [r0, #8]                  
  0d9d8:  str r0, [r1, #0x1c]               
  0d9da:  ldr r0, [pc, #0x340]              -> RAM
  0d9dc:  ldrb r0, [r0, #0xc]               
  0d9de:  ubfx r1, r0, #1, #1               
  0d9e2:  ldr r0, [pc, #0x338]              -> RAM
  0d9e4:  ldrb r0, [r0, #0xc]               
  0d9e6:  bfi r0, r1, #1, #0x1f             
  0d9ea:  ldr r1, [pc, #0x330]              -> RAM
  0d9ec:  ldrb r1, [r1, #0x17]              
  0d9ee:  and r1, r1, #1                    
  0d9f2:  orr.w r0, r0, r1, lsl #2          
  0d9f6:  ldr r1, [pc, #0x324]              -> RAM
  0d9f8:  ldrb r1, [r1, #0xc]               
  0d9fa:  ubfx r1, r1, #3, #1               
  0d9fe:  orr.w r0, r0, r1, lsl #3          
  0da02:  ldr r1, [pc, #0x318]              -> RAM
  0da04:  ldrb r1, [r1, #0xc]               
  0da06:  ubfx r1, r1, #4, #1               
  0da0a:  orr.w r0, r0, r1, lsl #4          
  0da0e:  ldr r1, [pc, #0x30c]              -> RAM
  0da10:  ldrb r1, [r1, #0xc]               
  0da12:  ubfx r1, r1, #6, #1               
  0da16:  orr.w r0, r0, r1, lsl #5          
  0da1a:  ldr r1, [pc, #0x304]              -> RAM
  0da1c:  ldrb r1, [r1, #2]                 
  0da1e:  and r1, r1, #1                    
  0da22:  orr.w r0, r0, r1, lsl #7          
  0da26:  ldr r1, [pc, #0x2fc]              -> RAM
  0da28:  ldrb r1, [r1, #8]                 
  0da2a:  and r1, r1, #1                    
  0da2e:  orr.w r0, r0, r1, lsl #8          
  0da32:  ldr r1, [pc, #0x2f0]              -> RAM
  0da34:  ldrb r1, [r1, #8]                 
  0da36:  ubfx r1, r1, #1, #1               
  0da3a:  orr.w r0, r0, r1, lsl #9          
  0da3e:  ldr r1, [pc, #0x2e4]              -> RAM
  0da40:  ldrb r1, [r1, #8]                 
  0da42:  ubfx r1, r1, #3, #1               
  0da46:  orr.w r0, r0, r1, lsl #10         
  0da4a:  ldr r1, [pc, #0x2d8]              -> RAM
  0da4c:  ldrb r1, [r1, #8]                 
  0da4e:  b #0xda52                         -> 0x0da52 (вне списка функций)
  0da50:  b #0xdb28                         -> 0x0db28 (вне списка функций)
  0da52:  ubfx r1, r1, #4, #1               
  0da56:  orr.w r0, r0, r1, lsl #11         
  0da5a:  ldr r1, [pc, #0x2c8]              -> RAM
  0da5c:  ldrb r1, [r1, #8]                 
  0da5e:  ubfx r1, r1, #5, #1               
  0da62:  orr.w r0, r0, r1, lsl #12         
  0da66:  ldr r1, [pc, #0x2bc]              -> RAM
  0da68:  ldrb r1, [r1, #8]                 
  0da6a:  ubfx r1, r1, #6, #1               
  0da6e:  orr.w r0, r0, r1, lsl #14         
  0da72:  ldr r1, [pc, #0x2b4]              -> RAM
  0da74:  ldrb r1, [r1, #6]                 
  0da76:  and r1, r1, #1                    
  0da7a:  orr.w r0, r0, r1, lsl #15         
  0da7e:  ldr r1, [pc, #0x2a8]              -> RAM
  0da80:  ldrb r1, [r1, #6]                 
  0da82:  ubfx r1, r1, #1, #1               
  0da86:  orr.w r0, r0, r1, lsl #17         
  0da8a:  ldr r1, [pc, #0x29c]              -> RAM
  0da8c:  ldrb r1, [r1, #6]                 
  0da8e:  ubfx r1, r1, #3, #1               
  0da92:  orr.w r0, r0, r1, lsl #19         
  0da96:  ldr r1, [pc, #0x290]              -> RAM
  0da98:  ldrb r1, [r1, #6]                 
  0da9a:  ubfx r1, r1, #5, #1               
  0da9e:  orr.w r0, r0, r1, lsl #21         
  0daa2:  ldr r1, [pc, #0x284]              -> RAM
  0daa4:  ldrb r1, [r1, #9]                 
  0daa6:  ubfx r1, r1, #1, #1               
  0daaa:  orr.w r0, r0, r1, lsl #23         
  0daae:  ldr r1, [pc, #0x278]              -> RAM
  0dab0:  ldrb r1, [r1, #6]                 
  0dab2:  ubfx r1, r1, #6, #1               
  0dab6:  cbnz r1, #0xdac2                  
  0dab8:  ldr r1, [pc, #0x26c]              -> RAM
  0daba:  ldrb r1, [r1, #9]                 
  0dabc:  ubfx r1, r1, #3, #1               
  0dac0:  cbz r1, #0xdac6                   
  0dac2:  movs r1, #1                       
  0dac4:  b #0xdac8                         -> 0x0dac8 (вне списка функций)
  0dac6:  movs r1, #0                       
  0dac8:  orr.w r0, r0, r1, lsl #24         
  0dacc:  ldr r1, [pc, #0x24c]              -> RAM
  0dace:  ldrb r1, [r1, #0xc]               
  0dad0:  lsrs r1, r1, #7                   
  0dad2:  orr.w r0, r0, r1, lsl #25         
  0dad6:  ldr r1, [pc, #0x248]              -> RAM
  0dad8:  ldrb r1, [r1, #2]                 
  0dada:  ubfx r1, r1, #1, #1               
  0dade:  orr.w r0, r0, r1, lsl #26         
  0dae2:  ldr r1, [pc, #0x23c]              -> RAM
  0dae4:  ldrb r1, [r1, #2]                 
  0dae6:  ubfx r1, r1, #2, #1               
  0daea:  orr.w r0, r0, r1, lsl #27         
  0daee:  ldr r1, [pc, #0x230]              -> RAM
  0daf0:  ldrb r1, [r1, #2]                 
  0daf2:  ubfx r1, r1, #3, #1               
  0daf6:  orr.w r0, r0, r1, lsl #28         
  0dafa:  ldr r1, [pc, #0x224]              -> RAM
  0dafc:  ldrb r1, [r1, #3]                 
  0dafe:  ubfx r1, r1, #4, #1               
  0db02:  orr.w r0, r0, r1, lsl #29         
  0db06:  ldr r1, [pc, #0x218]              -> RAM
  0db08:  ldrb r1, [r1, #3]                 
  0db0a:  ubfx r1, r1, #2, #1               
  0db0e:  orr.w r0, r0, r1, lsl #30         
  0db12:  ldr r1, [pc, #0x20c]              -> RAM
  0db14:  ldrb r1, [r1, #3]                 
  0db16:  lsrs r1, r1, #3                   
  0db18:  orr.w r0, r0, r1, lsl #31         
  0db1c:  ldr r1, [pc, #0x1e8]              -> RAM
  0db1e:  str r0, [r1, #0x20]               
  0db20:  movs r0, #0                       
  0db22:  strh r0, [r1, #0x24]              
  0db24:  strh r0, [r1, #0x26]              
  0db26:  b #0xdcf0                         -> 0x0dcf0 (вне списка функций)
  0db28:  ldr r0, [pc, #0x1dc]              -> RAM
  0db2a:  strh r4, [r0]                     
  0db2c:  mov r0, sp                        
  0db2e:  bl #0x8a90                        -> func_0x08a90
  0db32:  ldr r0, [pc, #0x1d8]              -> RAM
  0db34:  ldr r1, [sp]                      
  0db36:  str r1, [r0]                      
  0db38:  ldrh.w r1, [sp, #4]               
  0db3c:  strh r1, [r0, #4]                 
  0db3e:  ldrb.w r1, [sp, #6]               
  0db42:  strb r1, [r0, #6]                 
  0db44:  ldrb r1, [r0, #5]                 
  0db46:  ldr r0, [pc, #0x1c0]              -> RAM
  0db48:  strb r1, [r0, #7]                 
  0db4a:  ldr r0, [pc, #0x1c0]              -> RAM
  0db4c:  ldrb r1, [r0, #4]                 
  0db4e:  ldr r0, [pc, #0x1b8]              -> RAM
  0db50:  strb r1, [r0, #6]                 
  0db52:  ldr r0, [pc, #0x1b8]              -> RAM
  0db54:  ldrb r1, [r0, #3]                 
  0db56:  ldr r0, [pc, #0x1b0]              -> RAM
  0db58:  strb r1, [r0, #5]                 
  0db5a:  ldr r0, [pc, #0x1b0]              -> RAM
  0db5c:  ldrb r1, [r0, #2]                 
  0db5e:  ldr r0, [pc, #0x1a8]              -> RAM
  0db60:  strb r1, [r0, #4]                 
  0db62:  ldr r0, [pc, #0x1a8]              -> RAM
  0db64:  ldrb r1, [r0, #1]                 
  0db66:  ldr r0, [pc, #0x1a0]              -> RAM
  0db68:  strb r1, [r0, #3]                 
  0db6a:  ldr r0, [pc, #0x1a0]              -> RAM
  0db6c:  ldrb r0, [r0]                     
  0db6e:  ldr r1, [pc, #0x198]              -> RAM
  0db70:  strb r0, [r1, #2]                 
  0db72:  ldr r0, [pc, #0x1a8]              -> RAM
  0db74:  ldr r0, [r0]                      
  0db76:  str r0, [r1, #8]                  
  0db78:  ldr r0, [pc, #0x1a0]              -> RAM
  0db7a:  ldrh r0, [r0, #8]                 
  0db7c:  strh r0, [r1, #0xc]               
  0db7e:  ldr r0, [pc, #0x19c]              -> RAM
  0db80:  ldrh r0, [r0, #6]                 
  0db82:  strh r0, [r1, #0xe]               
  0db84:  ldr r0, [pc, #0x19c]              -> RAM
  0db86:  ldr r0, [r0]                      
  0db88:  str r0, [r1, #0x10]               
  0db8a:  ldr r0, [pc, #0x19c]              -> RAM
  0db8c:  ldrb r0, [r0, #2]                 
  0db8e:  strb r0, [r1, #0x14]              
  0db90:  ldr r0, [pc, #0x194]              -> RAM
  0db92:  ldrb r0, [r0, #1]                 
  0db94:  strb r0, [r1, #0x15]              
  0db96:  ldr r0, [pc, #0x180]              -> RAM
  0db98:  ldrh r0, [r0, #2]                 
  0db9a:  strh r0, [r1, #0x16]              
  0db9c:  ldr r0, [pc, #0x178]              -> RAM
  0db9e:  ldr r0, [r0, #0xc]                
  0dba0:  str r0, [r1, #0x18]               
  0dba2:  ldr r0, [pc, #0x174]              -> RAM
  0dba4:  ldr r0, [r0, #8]                  
  0dba6:  str r0, [r1, #0x1c]               
  0dba8:  ldr r0, [pc, #0x170]              -> RAM
  0dbaa:  ldrb r0, [r0, #0xc]               
  0dbac:  ubfx r1, r0, #1, #1               
  0dbb0:  ldr r0, [pc, #0x168]              -> RAM
  0dbb2:  ldrb r0, [r0, #0xc]               
  0dbb4:  bfi r0, r1, #1, #0x1f             
  0dbb8:  ldr r1, [pc, #0x160]              -> RAM
  0dbba:  ldrb r1, [r1, #0x17]              
  0dbbc:  and r1, r1, #1                    
  0dbc0:  orr.w r0, r0, r1, lsl #2          
  0dbc4:  ldr r1, [pc, #0x154]              -> RAM
  0dbc6:  ldrb r1, [r1, #0xc]               
  0dbc8:  ubfx r1, r1, #3, #1               
  0dbcc:  orr.w r0, r0, r1, lsl #3          
  0dbd0:  ldr r1, [pc, #0x148]              -> RAM
  0dbd2:  ldrb r1, [r1, #0xc]               
  0dbd4:  ubfx r1, r1, #4, #1               
  0dbd8:  orr.w r0, r0, r1, lsl #4          
  0dbdc:  ldr r1, [pc, #0x13c]              -> RAM
  0dbde:  ldrb r1, [r1, #0xc]               
  0dbe0:  ubfx r1, r1, #6, #1               
  0dbe4:  orr.w r0, r0, r1, lsl #5          
  0dbe8:  ldr r1, [pc, #0x134]              -> RAM
  0dbea:  ldrb r1, [r1, #2]                 
  0dbec:  and r1, r1, #1                    
  0dbf0:  orr.w r0, r0, r1, lsl #7          
  0dbf4:  ldr r1, [pc, #0x12c]              -> RAM
  0dbf6:  ldrb r1, [r1, #8]                 
  0dbf8:  and r1, r1, #1                    
  0dbfc:  orr.w r0, r0, r1, lsl #8          
  0dc00:  ldr r1, [pc, #0x120]              -> RAM
  0dc02:  ldrb r1, [r1, #8]                 
  0dc04:  ubfx r1, r1, #1, #1               
  0dc08:  orr.w r0, r0, r1, lsl #9          
  0dc0c:  ldr r1, [pc, #0x114]              -> RAM
  0dc0e:  ldrb r1, [r1, #8]                 
  0dc10:  ubfx r1, r1, #3, #1               
  0dc14:  orr.w r0, r0, r1, lsl #10         
  0dc18:  ldr r1, [pc, #0x108]              -> RAM
  0dc1a:  ldrb r1, [r1, #8]                 
  0dc1c:  ubfx r1, r1, #4, #1               
  0dc20:  orr.w r0, r0, r1, lsl #11         
  0dc24:  ldr r1, [pc, #0xfc]               -> RAM
  0dc26:  ldrb r1, [r1, #8]                 
  0dc28:  ubfx r1, r1, #5, #1               
  0dc2c:  orr.w r0, r0, r1, lsl #12         
  0dc30:  ldr r1, [pc, #0xf0]               -> RAM
  0dc32:  ldrb r1, [r1, #8]                 
  0dc34:  ubfx r1, r1, #6, #1               
  0dc38:  orr.w r0, r0, r1, lsl #14         
  0dc3c:  ldr r1, [pc, #0xe8]               -> RAM
  0dc3e:  ldrb r1, [r1, #6]                 
  0dc40:  and r1, r1, #1                    
  0dc44:  orr.w r0, r0, r1, lsl #15         
  0dc48:  ldr r1, [pc, #0xdc]               -> RAM
  0dc4a:  ldrb r1, [r1, #6]                 
  0dc4c:  ubfx r1, r1, #1, #1               
  0dc50:  orr.w r0, r0, r1, lsl #17         
  0dc54:  ldr r1, [pc, #0xd0]               -> RAM
  0dc56:  ldrb r1, [r1, #6]                 
  0dc58:  ubfx r1, r1, #3, #1               
  0dc5c:  orr.w r0, r0, r1, lsl #19         
  0dc60:  ldr r1, [pc, #0xc4]               -> RAM
  0dc62:  ldrb r1, [r1, #6]                 
  0dc64:  ubfx r1, r1, #5, #1               
  0dc68:  orr.w r0, r0, r1, lsl #21         
  0dc6c:  ldr r1, [pc, #0xb8]               -> RAM
  0dc6e:  ldrb r1, [r1, #9]                 
  0dc70:  ubfx r1, r1, #1, #1               
  0dc74:  orr.w r0, r0, r1, lsl #23         
  0dc78:  ldr r1, [pc, #0xac]               -> RAM
  0dc7a:  ldrb r1, [r1, #6]                 
  0dc7c:  ubfx r1, r1, #6, #1               
  0dc80:  cbnz r1, #0xdc8c                  
  0dc82:  ldr r1, [pc, #0xa4]               -> RAM
  0dc84:  ldrb r1, [r1, #9]                 
  0dc86:  ubfx r1, r1, #3, #1               
  0dc8a:  cbz r1, #0xdc90                   
  0dc8c:  movs r1, #1                       
  0dc8e:  b #0xdc92                         -> 0x0dc92 (вне списка функций)
  0dc90:  movs r1, #0                       
  0dc92:  orr.w r0, r0, r1, lsl #24         
  0dc96:  ldr r1, [pc, #0x84]               -> RAM
  0dc98:  ldrb r1, [r1, #0xc]               
  0dc9a:  lsrs r1, r1, #7                   
  0dc9c:  orr.w r0, r0, r1, lsl #25         
  0dca0:  ldr r1, [pc, #0x7c]               -> RAM
  0dca2:  ldrb r1, [r1, #2]                 
  0dca4:  ubfx r1, r1, #1, #1               
  0dca8:  orr.w r0, r0, r1, lsl #26         
  0dcac:  ldr r1, [pc, #0x70]               -> RAM
  0dcae:  ldrb r1, [r1, #2]                 
  0dcb0:  ubfx r1, r1, #2, #1               
  0dcb4:  orr.w r0, r0, r1, lsl #27         
  0dcb8:  ldr r1, [pc, #0x64]               -> RAM
  0dcba:  ldrb r1, [r1, #2]                 
  0dcbc:  ubfx r1, r1, #3, #1               
  0dcc0:  orr.w r0, r0, r1, lsl #28         
  0dcc4:  ldr r1, [pc, #0x58]               -> RAM
  0dcc6:  ldrb r1, [r1, #3]                 
  0dcc8:  ubfx r1, r1, #4, #1               
  0dccc:  orr.w r0, r0, r1, lsl #29         
  0dcd0:  ldr r1, [pc, #0x4c]               -> RAM
  0dcd2:  ldrb r1, [r1, #3]                 
  0dcd4:  ubfx r1, r1, #2, #1               
  0dcd8:  orr.w r0, r0, r1, lsl #30         
  0dcdc:  ldr r1, [pc, #0x40]               -> RAM
  0dcde:  ldrb r1, [r1, #3]                 
  0dce0:  lsrs r1, r1, #3                   
  0dce2:  orr.w r0, r0, r1, lsl #31         
  0dce6:  ldr r1, [pc, #0x20]               -> RAM
  0dce8:  str r0, [r1, #0x20]               
  0dcea:  movs r0, #0                       
  0dcec:  strh r0, [r1, #0x24]              
  0dcee:  strh r0, [r1, #0x26]              
  0dcf0:  movs r1, #0x26                    
  0dcf2:  ldr r0, [pc, #0x14]               -> RAM
  0dcf4:  bl #0x8a50                        -> func_0x08a50
  0dcf8:  ldr r1, [pc, #0xc]                -> RAM
  0dcfa:  strh r0, [r1, #0x26]              
  0dcfc:  bl #0x157e0                       -> func_0x157e0
  0dd00:  pop {r2, r3, r4, pc}              
  ; --- literal-пул @0x0dd04 (10 слов) — ВНЕ границ функции ---
  0dd04:  .word 0x20003024  ; RAM
  0dd08:  .word 0x2000305c  ; RAM
  0dd0c:  .word 0x20000098  ; RAM
  0dd10:  .word 0x20001344  ; RAM
  0dd14:  .word 0x20001359  ; RAM
  0dd18:  .word 0x20000fd3  ; RAM
  0dd1c:  .word 0x20000f95  ; RAM
  0dd20:  .word 0x20000f70  ; RAM
  0dd24:  .word 0x20000fbb  ; RAM
  0dd28:  .word 0x20000fc7  ; RAM
```
