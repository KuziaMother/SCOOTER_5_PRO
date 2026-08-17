# func_0x1dfd8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001dfd8) | `0x0001dfd8` |
| размер кода | 344 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000217 — данные @0x00217 (r1)
- 0x00007530 — данные @0x07530 (r3)
- 0x0001d4ca — данные @0x1d4ca (r2)
- 0x200001e0 — RAM (r1)
- 0x2000021e — RAM (r0)
- 0x2000022d — RAM (r2)
- 0x20000278 — RAM (r1)
- 0x2000027a — RAM (r0)
- 0x20000284 — RAM (r1)
- 0x20000286 — RAM (r0)
- 0x20000288 — RAM (r2)
- 0x20000298 — RAM (r2)
- 0x2000029c — RAM (r1)
- 0x2000029e — RAM (r0)
- 0x200002a0 — RAM (r2)
- 0x200002ba — RAM (r1)
- 0x200002bc — RAM (r0)
- 0x200002be — RAM (r1)
- 0x200002c4 — RAM (r0)
- 0x200002c6 — RAM (r1)
- 0x20000306 — RAM (r6)
- 0x20000312 — RAM (r1)
- 0x20000314 — RAM (r0)
- 0x20000321 — RAM (r2)
- 0x20000339 — RAM (r0)
- 0x2000033a — RAM (r3)
- 0x20001794 — RAM (r1)
- 0x48000c00 — периферия (r0)

## Вызовы (callees)

- 0x19994 (bl, вне списка функций)
- `func_0x1b67c` (0x0001b67c, bl)
- 0x1e062 (b, вне списка функций)
- 0x1e08e (b, вне списка функций)
- 0x1e094 (b, вне списка функций)
- 0x1e0ae (b, вне списка функций)
- 0x1e0cc (b, вне списка функций)
- 0x1e102 (b, вне списка функций)
- 0x1e124 (b, вне списка функций)
- 0x1e128 (b, вне списка функций)
- `func_0x1e9e0` (0x0001e9e0, bl)
- `func_0x1f1cc` (0x0001f1cc, bl)
- `func_0x1f71c` (0x0001f71c, bl)
- `func_0x211f8` (0x000211f8, bl)
- `func_0x2186c` (0x0002186c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1e074..0x1e078` (4 Б); цели из: 0x1e046
- `0x1e078..0x1e08e` (22 Б); цели из: 0x1e06e
- `0x1e08e..0x1e092` (4 Б); цели из: 0x1e072
- `0x1e092..0x1e094` (2 Б); цели из: 0x1e07e
- `0x1e094..0x1e0ac` (24 Б); цели из: 0x1e060, 0x1e090
- `0x1e0ac..0x1e0ae` (2 Б); цели из: 0x1e0a0
- `0x1e0ae..0x1e0ca` (28 Б); цели из: 0x1e0a6, 0x1e0aa
- `0x1e0ca..0x1e0cc` (2 Б); цели из: 0x1e0be
- `0x1e0cc..0x1e0e2` (22 Б); цели из: 0x1e0c4, 0x1e0c8
- `0x1e0e2..0x1e0fe` (28 Б); цели из: 0x1e0dc
- `0x1e0fe..0x1e104` (6 Б); цели из: 0x1e0f4
- `0x1e104..0x1e114` (16 Б); цели из: 0x1e0e8
- `0x1e114..0x1e11a` (6 Б); цели из: 0x1e0fc
- `0x1e11a..0x1e128` (14 Б); цели из: 0x1e10e
- `0x1e128..0x1e130` (8 Б); цели из: 0x1e112, 0x1e11e

## Дизассембляция

```asm
  1dfd8:  push {r4, r5, r6, lr}             
  1dfda:  bl #0x1b67c                       -> func_0x1b67c
  1dfde:  ldr r1, [pc, #0x150]              -> RAM
  1dfe0:  ldrh r0, [r1]                     
  1dfe2:  adds r0, r0, #1                   
  1dfe4:  strh r0, [r1]                     
  1dfe6:  bl #0x2186c                       -> func_0x2186c
  1dfea:  ldr r2, [pc, #0x148]              -> RAM
  1dfec:  ldr r1, [pc, #0x148]              -> RAM
  1dfee:  movs r3, #0                       
  1dff0:  ldrsh r3, [r1, r3]                
  1dff2:  ldr r0, [r2]                      
  1dff4:  movs r5, #1                       
  1dff6:  adds r1, r0, r3                   
  1dff8:  ldr r0, [pc, #0x140]              -> RAM
  1dffa:  movs r3, #0                       
  1dffc:  ldrsh r3, [r0, r3]                
  1dffe:  movs r4, #0                       
  1e000:  subs r1, r1, r3                   
  1e002:  str r1, [r2]                      
  1e004:  asrs r1, r1, #5                   
  1e006:  strh r1, [r0]                     
  1e008:  ldr r2, [pc, #0x134]              -> RAM
  1e00a:  ldr r1, [pc, #0x138]              -> RAM
  1e00c:  movs r3, #0                       
  1e00e:  ldrsh r3, [r1, r3]                
  1e010:  ldr r0, [r2]                      
  1e012:  adds r1, r0, r3                   
  1e014:  ldr r0, [pc, #0x130]              -> RAM
  1e016:  movs r3, #0                       
  1e018:  ldrsh r3, [r0, r3]                
  1e01a:  subs r1, r1, r3                   
  1e01c:  str r1, [r2]                      
  1e01e:  asrs r1, r1, #5                   
  1e020:  strh r1, [r0]                     
  1e022:  ldr r2, [pc, #0x128]              -> RAM
  1e024:  ldr r1, [pc, #0x128]              -> RAM
  1e026:  movs r3, #0                       
  1e028:  ldrsh r3, [r1, r3]                
  1e02a:  ldr r0, [r2]                      
  1e02c:  adds r1, r0, r3                   
  1e02e:  ldr r0, [pc, #0x124]              -> RAM
  1e030:  movs r3, #0                       
  1e032:  ldrsh r3, [r0, r3]                
  1e034:  subs r1, r1, r3                   
  1e036:  str r1, [r2]                      
  1e038:  asrs r1, r1, #5                   
  1e03a:  strh r1, [r0]                     
  1e03c:  ldr r1, [pc, #0x118]              -> RAM
  1e03e:  ldr r3, [pc, #0x11c]              -> данные @0x07530
  1e040:  ldrh r0, [r1]                     
  1e042:  ldr r2, [pc, #0x11c]              -> RAM
  1e044:  cmp r0, r3                        
  1e046:  bhs #0x1e074                      
  1e048:  adds r0, r0, #1                   
  1e04a:  strh r0, [r1]                     
  1e04c:  ldrb r0, [r2]                     
  1e04e:  cmp r0, #1                        
  1e050:  beq #0x1e062                      
  1e052:  ldr r1, [pc, #0x110]              -> RAM
  1e054:  movs r3, #0x19                    
  1e056:  ldm r1, {r0, r1}                  
  1e058:  lsls r3, r3, #6                   
  1e05a:  movs r2, #0                       
  1e05c:  subs r0, r0, r3                   
  1e05e:  sbcs r1, r2                       
  1e060:  bhs #0x1e094                      
  1e062:  ldr r1, [pc, #0x104]              -> RAM
  1e064:  movs r0, #0xc                     
  1e066:  ldrsh r0, [r1, r0]                
  1e068:  ldr r1, [pc, #0x100]              -> данные @0x00217
  1e06a:  ldr r6, [pc, #0x104]              -> RAM
  1e06c:  cmp r0, r1                        
  1e06e:  blt #0x1e078                      
  1e070:  movs r0, #0x64                    
  1e072:  b #0x1e08e                        -> 0x1e08e (вне списка функций)
  1e074:  strb r5, [r2]                     
  1e076:  b #0x1e062                        -> 0x1e062 (вне списка функций)
  1e078:  movs r1, #0xff                    
  1e07a:  adds r1, #0xa0                    
  1e07c:  cmp r0, r1                        
  1e07e:  ble #0x1e092                      
  1e080:  subs r0, #0xff                    
  1e082:  movs r1, #0x64                    
  1e084:  subs r0, #0xa0                    
  1e086:  muls r0, r1, r0                   
  1e088:  movs r1, #0x78                    
  1e08a:  bl #0x19994                       -> 0x19994 (вне списка функций)
  1e08e:  strb r0, [r6]                     
  1e090:  b #0x1e094                        -> 0x1e094 (вне списка функций)
  1e092:  strb r4, [r6]                     
  1e094:  ldr r1, [pc, #0xdc]               -> RAM
  1e096:  movs r6, #0x19                    
  1e098:  ldrb r2, [r1]                     
  1e09a:  ldr r0, [pc, #0xdc]               -> RAM
  1e09c:  lsls r6, r6, #6                   
  1e09e:  cmp r2, #0                        
  1e0a0:  beq #0x1e0ac                      
  1e0a2:  ldrh r0, [r0]                     
  1e0a4:  cmp r0, r6                        
  1e0a6:  bls #0x1e0ae                      
  1e0a8:  strb r4, [r1]                     
  1e0aa:  b #0x1e0ae                        -> 0x1e0ae (вне списка функций)
  1e0ac:  strh r4, [r0]                     
  1e0ae:  bl #0x1e9e0                       -> func_0x1e9e0
  1e0b2:  bl #0x1f1cc                       -> func_0x1f1cc
  1e0b6:  ldr r1, [pc, #0xc4]               -> RAM
  1e0b8:  ldr r0, [pc, #0xc4]               -> RAM
  1e0ba:  ldrb r2, [r1]                     
  1e0bc:  cmp r2, #0                        
  1e0be:  beq #0x1e0ca                      
  1e0c0:  ldrh r0, [r0]                     
  1e0c2:  cmp r0, r6                        
  1e0c4:  bls #0x1e0cc                      
  1e0c6:  strb r4, [r1]                     
  1e0c8:  b #0x1e0cc                        -> 0x1e0cc (вне списка функций)
  1e0ca:  strh r4, [r0]                     
  1e0cc:  bl #0x1f71c                       -> func_0x1f71c
  1e0d0:  bl #0x211f8                       -> func_0x211f8
  1e0d4:  ldr r0, [pc, #0xac]               -> RAM
  1e0d6:  ldr r2, [pc, #0xb0]               -> данные @0x1d4ca
  1e0d8:  ldr r1, [r0]                      
  1e0da:  cmp r1, r2                        
  1e0dc:  bhs #0x1e0e2                      
  1e0de:  adds r1, r1, #1                   
  1e0e0:  str r1, [r0]                      
  1e0e2:  movs r0, #0x7d                    
  1e0e4:  lsls r0, r0, #3                   
  1e0e6:  cmp r1, r0                        
  1e0e8:  blo #0x1e104                      
  1e0ea:  ldr r0, [pc, #0xa0]               -> RAM
  1e0ec:  movs r2, #0x20                    
  1e0ee:  ldrb r3, [r0]                     
  1e0f0:  ldr r0, [pc, #0x9c]               -> RAM
  1e0f2:  cmp r3, #1                        
  1e0f4:  bne #0x1e0fe                      
  1e0f6:  ldr r3, [pc, #0x9c]               -> RAM
  1e0f8:  ldrb r3, [r3]                     
  1e0fa:  cmp r3, #1                        
  1e0fc:  beq #0x1e114                      
  1e0fe:  ldrh r3, [r0]                     
  1e100:  orrs r3, r2                       
  1e102:  strh r3, [r0]                     
  1e104:  ldr r3, [pc, #0x80]               -> данные @0x1d4ca
  1e106:  ldr r2, [pc, #0x90]               -> RAM
  1e108:  subs r3, #0xa                     
  1e10a:  ldr r0, [pc, #0x90]               -> периферия
  1e10c:  cmp r1, r3                        
  1e10e:  blo #0x1e11a                      
  1e110:  strb r4, [r2]                     
  1e112:  b #0x1e128                        -> 0x1e128 (вне списка функций)
  1e114:  ldrh r3, [r0]                     
  1e116:  bics r3, r2                       
  1e118:  b #0x1e102                        -> 0x1e102 (вне списка функций)
  1e11a:  ldrb r1, [r2]                     
  1e11c:  cmp r1, #0                        
  1e11e:  beq #0x1e128                      
  1e120:  ldr r1, [r0, #4]                  
  1e122:  orrs r1, r5                       
  1e124:  str r1, [r0, #4]                  
  1e126:  pop {r4, r5, r6, pc}              
  1e128:  ldr r1, [r0, #4]                  
  1e12a:  lsrs r1, r1, #1                   
  1e12c:  lsls r1, r1, #1                   
  1e12e:  b #0x1e124                        -> 0x1e124 (вне списка функций)
  ; --- literal-пул @0x1e130 (28 слов) — ВНЕ границ функции ---
  1e130:  .word 0x200002ba  ; RAM
  1e134:  .word 0x20000298  ; RAM
  1e138:  .word 0x20000278  ; RAM
  1e13c:  .word 0x2000027a  ; RAM
  1e140:  .word 0x20000288  ; RAM
  1e144:  .word 0x20000284  ; RAM
  1e148:  .word 0x20000286  ; RAM
  1e14c:  .word 0x200002a0  ; RAM
  1e150:  .word 0x2000029c  ; RAM
  1e154:  .word 0x2000029e  ; RAM
  1e158:  .word 0x20000312  ; RAM
  1e15c:  .word 0x00007530  ; данные @0x07530
  1e160:  .word 0x20000321  ; RAM
  1e164:  .word 0x200001e0  ; RAM
  1e168:  .word 0x20001794  ; RAM
  1e16c:  .word 0x00000217  ; данные @0x00217
  1e170:  .word 0x20000306  ; RAM
  1e174:  .word 0x200002be  ; RAM
  1e178:  .word 0x200002bc  ; RAM
  1e17c:  .word 0x200002c6  ; RAM
  1e180:  .word 0x200002c4  ; RAM
  1e184:  .word 0x20000314  ; RAM
  1e188:  .word 0x0001d4ca  ; данные @0x1d4ca
  1e18c:  .word 0x20000339  ; RAM
  1e190:  .word 0x2000021e  ; RAM
  1e194:  .word 0x2000033a  ; RAM
  1e198:  .word 0x2000022d  ; RAM
  1e19c:  .word 0x48000c00  ; периферия
```
