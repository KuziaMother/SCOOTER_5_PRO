# func_0x0d00c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d00c) | `0x0000d00c` |
| размер кода | 534 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000098 — RAM (r0)
- 0x2000011c — RAM (r1)
- 0x20000f64 — RAM (r0)
- 0x20000f70 — RAM (r1)
- 0x20000f95 — RAM (r1)
- 0x20000fbb — RAM (r1)
- 0x20000fc7 — RAM (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x08a90` (0x00008a90, bl)
- `func_0x0ab0c` (0x0000ab0c, bl)
- `func_0x0abf0` (0x0000abf0, bl)
- 0x0accc (bl, вне списка функций)
- 0x0ad9c (bl, вне списка функций)
- 0x0d02a (b, вне списка функций)
- 0x0d02e (b, вне списка функций)
- 0x0d052 (b, вне списка функций)
- 0x0d0d4 (b, вне списка функций)
- 0x0d0f0 (b, вне списка функций)
- 0x0d152 (b, вне списка функций)
- 0x0d170 (b, вне списка функций)
- 0x0d19c (b, вне списка функций)
- 0x0d1a0 (b, вне списка функций)
- 0x0d1be (b, вне списка функций)
- 0x0d21e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e12)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d026..0x0d02a` (4 Б); цели из: 0x0d022
- `0x0d02a..0x0d02e` (4 Б); цели из: 0x0d016
- `0x0d02e..0x0d050` (34 Б); цели из: 0x0d024
- `0x0d050..0x0d052` (2 Б); цели из: 0x0d046, 0x0d04a
- `0x0d052..0x0d068` (22 Б); цели из: 0x0d04e
- `0x0d068..0x0d0d4` (108 Б); цели из: 0x0d056
- `0x0d0d4..0x0d0ee` (26 Б); цели из: 0x0d066
- `0x0d0ee..0x0d0f0` (2 Б); цели из: 0x0d0e4, 0x0d0e8
- `0x0d0f0..0x0d11e` (46 Б); цели из: 0x0d0ec
- `0x0d11e..0x0d152` (52 Б); цели из: 0x0d0f4
- `0x0d152..0x0d16e` (28 Б); цели из: 0x0d11c
- `0x0d16e..0x0d170` (2 Б); цели из: 0x0d164, 0x0d168
- `0x0d170..0x0d186` (22 Б); цели из: 0x0d16c
- `0x0d186..0x0d198` (18 Б); цели из: 0x0d174
- `0x0d198..0x0d19c` (4 Б); цели из: 0x0d194
- `0x0d19c..0x0d1a0` (4 Б); цели из: 0x0d188
- `0x0d1a0..0x0d1bc` (28 Б); цели из: 0x0d196
- `0x0d1bc..0x0d1be` (2 Б); цели из: 0x0d1b2, 0x0d1b6
- `0x0d1be..0x0d1ee` (48 Б); цели из: 0x0d1ba
- `0x0d1ee..0x0d21e` (48 Б); цели из: 0x0d1c2
- `0x0d21e..0x0d222` (4 Б); цели из: 0x0d1ec

## Дизассембляция

```asm
  0d00c:  push {r4, r5, r6, r7, lr}         
  0d00e:  sub sp, #0x6c                     
  0d010:  movs r6, #0                       
  0d012:  movs r7, #0                       
  0d014:  nop                               
  0d016:  b #0xd02a                         -> 0x0d02a (вне списка функций)
  0d018:  add r0, sp, #0x3c                 
  0d01a:  bl #0xab0c                        -> func_0x0ab0c
  0d01e:  mov r4, r0                        
  0d020:  cmp r4, #1                        
  0d022:  bne #0xd026                       
  0d024:  b #0xd02e                         -> 0x0d02e (вне списка функций)
  0d026:  adds r0, r7, #1                   
  0d028:  uxtb r7, r0                       
  0d02a:  cmp r7, #3                        
  0d02c:  blt #0xd018                       
  0d02e:  nop                               
  0d030:  movs r0, #0                       
  0d032:  ldr r1, [pc, #0x1f0]              -> RAM
  0d034:  strb r0, [r1]                     
  0d036:  movs r1, #0xa                     
  0d038:  add r0, sp, #0x54                 
  0d03a:  bl #0x8a50                        -> func_0x08a50
  0d03e:  mov r6, r0                        
  0d040:  add r0, sp, #0x3c                 
  0d042:  ldrh r0, [r0, #0x22]              
  0d044:  cmp r0, r6                        
  0d046:  bne #0xd050                       
  0d048:  cmp r4, #1                        
  0d04a:  bne #0xd050                       
  0d04c:  movs r0, #1                       
  0d04e:  b #0xd052                         -> 0x0d052 (вне списка функций)
  0d050:  movs r0, #0                       
  0d052:  mov r5, r0                        
  0d054:  cmp r5, #1                        
  0d056:  bne #0xd068                       
  0d058:  ldr r0, [pc, #0x1cc]              -> RAM
  0d05a:  ldr r1, [sp, #0x54]               
  0d05c:  str r1, [r0]                      
  0d05e:  ldr r1, [sp, #0x58]               
  0d060:  str r1, [r0, #4]                  
  0d062:  ldr r1, [sp, #0x5c]               
  0d064:  str r1, [r0, #8]                  
  0d066:  b #0xd0d4                         -> 0x0d0d4 (вне списка функций)
  0d068:  add r0, sp, #0x1c                 
  0d06a:  bl #0x8a90                        -> func_0x08a90
  0d06e:  ldr r0, [pc, #0x1bc]              -> RAM
  0d070:  ldr r1, [sp, #0x1c]               
  0d072:  str r1, [r0]                      
  0d074:  ldrh.w r1, [sp, #0x20]            
  0d078:  strh r1, [r0, #4]                 
  0d07a:  ldrb.w r1, [sp, #0x22]            
  0d07e:  strb r1, [r0, #6]                 
  0d080:  ldrb r0, [r0, #5]                 
  0d082:  add.w r0, r0, #0x7d0              
  0d086:  strh.w r0, [sp, #0x54]            
  0d08a:  ldr r0, [pc, #0x1a0]              -> RAM
  0d08c:  ldrb r1, [r0, #4]                 
  0d08e:  add r0, sp, #0x3c                 
  0d090:  strb r1, [r0, #0x1a]              
  0d092:  ldr r0, [pc, #0x198]              -> RAM
  0d094:  ldrb r1, [r0, #3]                 
  0d096:  add r0, sp, #0x3c                 
  0d098:  strb r1, [r0, #0x1b]              
  0d09a:  ldr r0, [pc, #0x190]              -> RAM
  0d09c:  ldrb r1, [r0, #2]                 
  0d09e:  add r0, sp, #0x3c                 
  0d0a0:  strb r1, [r0, #0x1c]              
  0d0a2:  movs r1, #0                       
  0d0a4:  str.w r1, [sp, #0x5a]             
  0d0a8:  movs r1, #0xa                     
  0d0aa:  add r0, sp, #0x54                 
  0d0ac:  bl #0x8a50                        -> func_0x08a50
  0d0b0:  add r1, sp, #0x3c                 
  0d0b2:  strh r0, [r1, #0x22]              
  0d0b4:  movs r2, #0x20                    
  0d0b6:  add r1, sp, #0x4c                 
  0d0b8:  mov r0, sp                        
  0d0ba:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0d0be:  add r0, sp, #0x3c                 
  0d0c0:  ldm r0, {r0, r1, r2, r3}          
  0d0c2:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  0d0c6:  ldr r0, [pc, #0x160]              -> RAM
  0d0c8:  ldr r1, [sp, #0x54]               
  0d0ca:  str r1, [r0]                      
  0d0cc:  ldr r1, [sp, #0x58]               
  0d0ce:  str r1, [r0, #4]                  
  0d0d0:  ldr r1, [sp, #0x5c]               
  0d0d2:  str r1, [r0, #8]                  
  0d0d4:  movs r1, #7                       
  0d0d6:  add r0, sp, #0x60                 
  0d0d8:  bl #0x8a50                        -> func_0x08a50
  0d0dc:  mov r6, r0                        
  0d0de:  ldrh.w r0, [sp, #0x67]            
  0d0e2:  cmp r0, r6                        
  0d0e4:  bne #0xd0ee                       
  0d0e6:  cmp r4, #1                        
  0d0e8:  bne #0xd0ee                       
  0d0ea:  movs r0, #1                       
  0d0ec:  b #0xd0f0                         -> 0x0d0f0 (вне списка функций)
  0d0ee:  movs r0, #0                       
  0d0f0:  mov r5, r0                        
  0d0f2:  cmp r5, #1                        
  0d0f4:  bne #0xd11e                       
  0d0f6:  ldrh.w r0, [sp, #0x60]            
  0d0fa:  ldr r1, [pc, #0x134]              -> RAM
  0d0fc:  strh.w r0, [r1, #7]               
  0d100:  add r0, sp, #0x3c                 
  0d102:  ldrh r0, [r0, #0x26]              
  0d104:  ldr r1, [pc, #0x12c]              -> RAM
  0d106:  strh.w r0, [r1, #0x15]            
  0d10a:  add r0, sp, #0x3c                 
  0d10c:  ldrh r0, [r0, #0x28]              
  0d10e:  ldr r1, [pc, #0x128]              -> RAM
  0d110:  strh.w r0, [r1, #9]               
  0d114:  ldrb.w r0, [sp, #0x66]            
  0d118:  ldr r1, [pc, #0x120]              -> RAM
  0d11a:  strb r0, [r1, #5]                 
  0d11c:  b #0xd152                         -> 0x0d152 (вне списка функций)
  0d11e:  movs r0, #0                       
  0d120:  strh.w r0, [sp, #0x60]            
  0d124:  movs r1, #0                       
  0d126:  add r0, sp, #0x3c                 
  0d128:  strh r1, [r0, #0x28]              
  0d12a:  strh r1, [r0, #0x26]              
  0d12c:  movs r1, #0x19                    
  0d12e:  strb.w r1, [sp, #0x66]            
  0d132:  movs r1, #7                       
  0d134:  add r0, sp, #0x60                 
  0d136:  bl #0x8a50                        -> func_0x08a50
  0d13a:  add r1, sp, #0x3c                 
  0d13c:  strh.w r0, [sp, #0x67]            
  0d140:  movs r2, #0x20                    
  0d142:  add r1, sp, #0x4c                 
  0d144:  mov r0, sp                        
  0d146:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0d14a:  add r0, sp, #0x3c                 
  0d14c:  ldm r0, {r0, r1, r2, r3}          
  0d14e:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  0d152:  movs r1, #1                       
  0d154:  add.w r0, sp, #0x69               
  0d158:  bl #0x8a50                        -> func_0x08a50
  0d15c:  mov r6, r0                        
  0d15e:  ldrh.w r0, [sp, #0x6a]            
  0d162:  cmp r0, r6                        
  0d164:  bne #0xd16e                       
  0d166:  cmp r4, #1                        
  0d168:  bne #0xd16e                       
  0d16a:  movs r0, #1                       
  0d16c:  b #0xd170                         -> 0x0d170 (вне списка функций)
  0d16e:  movs r0, #0                       
  0d170:  mov r5, r0                        
  0d172:  cmp r5, #1                        
  0d174:  bne #0xd186                       
  0d176:  ldrb.w r1, [sp, #0x69]            
  0d17a:  ldr r0, [pc, #0xb4]               -> RAM
  0d17c:  ldrb r0, [r0, #2]                 
  0d17e:  bfi r0, r1, #1, #1                
  0d182:  ldr r1, [pc, #0xac]               -> RAM
  0d184:  strb r0, [r1, #2]                 
  0d186:  movs r7, #0                       
  0d188:  b #0xd19c                         -> 0x0d19c (вне списка функций)
  0d18a:  add r0, sp, #0x24                 
  0d18c:  bl #0xabf0                        -> func_0x0abf0
  0d190:  mov r4, r0                        
  0d192:  cmp r4, #1                        
  0d194:  bne #0xd198                       
  0d196:  b #0xd1a0                         -> 0x0d1a0 (вне списка функций)
  0d198:  adds r0, r7, #1                   
  0d19a:  uxtb r7, r0                       
  0d19c:  cmp r7, #3                        
  0d19e:  blt #0xd18a                       
  0d1a0:  nop                               
  0d1a2:  movs r1, #0x16                    
  0d1a4:  add r0, sp, #0x24                 
  0d1a6:  bl #0x8a50                        -> func_0x08a50
  0d1aa:  mov r6, r0                        
  0d1ac:  ldrh.w r0, [sp, #0x3a]            
  0d1b0:  cmp r0, r6                        
  0d1b2:  bne #0xd1bc                       
  0d1b4:  cmp r4, #1                        
  0d1b6:  bne #0xd1bc                       
  0d1b8:  movs r0, #1                       
  0d1ba:  b #0xd1be                         -> 0x0d1be (вне списка функций)
  0d1bc:  movs r0, #0                       
  0d1be:  mov r5, r0                        
  0d1c0:  cmp r5, #1                        
  0d1c2:  bne #0xd1ee                       
  0d1c4:  ldr r1, [pc, #0x68]               -> RAM
  0d1c6:  ldr r0, [sp, #0x24]               
  0d1c8:  str.w r0, [r1, #9]                
  0d1cc:  ldr r0, [sp, #0x28]               
  0d1ce:  str.w r0, [r1, #0xd]              
  0d1d2:  ldr r0, [sp, #0x2c]               
  0d1d4:  str.w r0, [r1, #0x11]             
  0d1d8:  ldr r0, [sp, #0x30]               
  0d1da:  str.w r0, [r1, #0x15]             
  0d1de:  ldr r0, [sp, #0x34]               
  0d1e0:  str.w r0, [r1, #0x1f]             
  0d1e4:  ldrh.w r0, [sp, #0x38]            
  0d1e8:  strh.w r0, [r1, #0x23]            
  0d1ec:  b #0xd21e                         -> 0x0d21e (вне списка функций)
  0d1ee:  movs r0, #0                       
  0d1f0:  str r0, [sp, #0x24]               
  0d1f2:  str r0, [sp, #0x28]               
  0d1f4:  movs r0, #0x78                    
  0d1f6:  str r0, [sp, #0x2c]               
  0d1f8:  movs r0, #0                       
  0d1fa:  str r0, [sp, #0x30]               
  0d1fc:  str r0, [sp, #0x34]               
  0d1fe:  strh.w r0, [sp, #0x38]            
  0d202:  movs r1, #0x2e                    
  0d204:  add r0, sp, #0x3c                 
  0d206:  bl #0x8a50                        -> func_0x08a50
  0d20a:  strh.w r0, [sp, #0x3a]            
  0d20e:  ldrd r0, r1, [sp, #0x34]          
  0d212:  strd r0, r1, [sp]                 
  0d216:  add r0, sp, #0x24                 
  0d218:  ldm r0, {r0, r1, r2, r3}          
  0d21a:  bl #0xad9c                        -> 0x0ad9c (вне списка функций)
  0d21e:  add sp, #0x6c                     
  0d220:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x0d224 (7 слов) — ВНЕ границ функции ---
  0d224:  .word 0x2000011c  ; RAM
  0d228:  .word 0x20000f64  ; RAM
  0d22c:  .word 0x20000098  ; RAM
  0d230:  .word 0x20000f70  ; RAM
  0d234:  .word 0x20000f95  ; RAM
  0d238:  .word 0x20000fbb  ; RAM
  0d23c:  .word 0x20000fc7  ; RAM
```
