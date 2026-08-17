# func_0x110fc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800110fc) | `0x000110fc` |
| размер кода | 400 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x05fa0000 — прочее (r1)
- 0x20000002 — RAM (r1)
- 0x20000004 — RAM (r0)
- 0x20000008 — RAM (r0)
- 0x2000000c — RAM (r0)
- 0x2000002c — RAM (r1)
- 0x2000002d — RAM (r0)
- 0x2000002f — RAM (r0)
- 0x20000035 — RAM (r1)
- 0x20000037 — RAM (r0)
- 0x20000a64 — RAM (r1)
- 0xe000ed0c — Cortex-M (NVIC/SCB/SysTick) (r0)

## Вызовы (callees)

- `func_0x022f4` (0x000022f4, bl)
- `func_0x05bc4` (0x00005bc4, bl)
- `func_0x05c9c` (0x00005c9c, bl)
- `func_0x05cc0` (0x00005cc0, bl)
- `func_0x05cd0` (0x00005cd0, bl)
- `func_0x08bec` (0x00008bec, bl)
- `func_0x0c94c` (0x0000c94c, bl)
- `func_0x0d938` (0x0000d938, bl)
- 0x111ec (b, вне списка функций)
- 0x111f4 (b, вне списка функций)
- 0x111f6 (b, вне списка функций)
- 0x1124c (b, вне списка функций)
- 0x11286 (b, вне списка функций)
- 0x11288 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11de8` (bl @0x00012066)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x11132..0x1116c` (58 Б); цели из: 0x11106
- `0x1116c..0x1118c` (32 Б); цели из: 0x1113e
- `0x1118c..0x111f2` (102 Б); цели из: 0x11172
- `0x111f2..0x111f4` (2 Б); цели из: 0x1110e
- `0x111f4..0x111f6` (2 Б); цели из: 0x1116a, 0x1118a, 0x111a0
- `0x111f6..0x11232` (60 Б); цели из: 0x1110a, 0x111f0
- `0x11232..0x1124c` (26 Б); цели из: 0x1120c
- `0x1124c..0x11284` (56 Б); цели из: 0x11110
- `0x11284..0x11286` (2 Б); цели из: 0x11264
- `0x11286..0x11288` (2 Б); цели из: 0x111f2
- `0x11288..0x1128c` (4 Б); цели из: 0x11130, 0x111f4, 0x1124a, 0x11284

## Дизассембляция

```asm
  110fc:  push {r4, lr}                     
  110fe:  ldr r0, [pc, #0x18c]              -> RAM
  11100:  ldrb r0, [r0]                     
  11102:  cbz r0, #0x11112                  
  11104:  cmp r0, #1                        
  11106:  beq #0x11132                      
  11108:  cmp r0, #2                        
  1110a:  beq #0x111f6                      
  1110c:  cmp r0, #3                        
  1110e:  bne #0x111f2                      
  11110:  b #0x1124c                        -> 0x1124c (вне списка функций)
  11112:  movs r0, #0                       
  11114:  ldr r1, [pc, #0x178]              -> RAM
  11116:  strb r0, [r1]                     
  11118:  movs r0, #3                       
  1111a:  ldr r1, [pc, #0x178]              -> RAM
  1111c:  strb r0, [r1]                     
  1111e:  movs r0, #0                       
  11120:  bl #0x5bc4                        -> func_0x05bc4
  11124:  movs r0, #1                       
  11126:  ldr r1, [pc, #0x164]              -> RAM
  11128:  strb r0, [r1]                     
  1112a:  movs r0, #5                       
  1112c:  bl #0x5cd0                        -> func_0x05cd0
  11130:  b #0x11288                        -> 0x11288 (вне списка функций)
  11132:  movs r0, #3                       
  11134:  ldr r1, [pc, #0x15c]              -> RAM
  11136:  strb r0, [r1]                     
  11138:  ldr r0, [pc, #0x15c]              -> RAM
  1113a:  ldrb r0, [r0]                     
  1113c:  cmp r0, #2                        
  1113e:  bne #0x1116c                      
  11140:  movs r0, #0                       
  11142:  ldr r1, [pc, #0x154]              -> RAM
  11144:  strb r0, [r1]                     
  11146:  bl #0x5c9c                        -> func_0x05c9c
  1114a:  ldr r0, [pc, #0x150]              -> RAM
  1114c:  ldr r0, [r0]                      
  1114e:  adds r0, r0, #1                   
  11150:  ldr r1, [pc, #0x148]              -> RAM
  11152:  str r0, [r1]                      
  11154:  ldr r0, [pc, #0x148]              -> RAM
  11156:  ldr r0, [r0]                      
  11158:  adds r0, r0, #1                   
  1115a:  ldr r1, [pc, #0x144]              -> RAM
  1115c:  str r0, [r1]                      
  1115e:  movs r0, #3                       
  11160:  ldr r1, [pc, #0x128]              -> RAM
  11162:  strb r0, [r1]                     
  11164:  movs r0, #0                       
  11166:  ldr r1, [pc, #0x13c]              -> RAM
  11168:  strh r0, [r1]                     
  1116a:  b #0x111f4                        -> 0x111f4 (вне списка функций)
  1116c:  ldr r0, [pc, #0x128]              -> RAM
  1116e:  ldrb r0, [r0]                     
  11170:  cmp r0, #1                        
  11172:  bne #0x1118c                      
  11174:  movs r0, #0                       
  11176:  ldr r1, [pc, #0x120]              -> RAM
  11178:  strb r0, [r1]                     
  1117a:  bl #0x5cc0                        -> func_0x05cc0
  1117e:  movs r0, #2                       
  11180:  ldr r1, [pc, #0x108]              -> RAM
  11182:  strb r0, [r1]                     
  11184:  movs r0, #0                       
  11186:  ldr r1, [pc, #0x11c]              -> RAM
  11188:  strh r0, [r1]                     
  1118a:  b #0x111f4                        -> 0x111f4 (вне списка функций)
  1118c:  ldr r0, [pc, #0x114]              -> RAM
  1118e:  ldrh r0, [r0]                     
  11190:  adds r0, r0, #1                   
  11192:  ldr r1, [pc, #0x110]              -> RAM
  11194:  strh r0, [r1]                     
  11196:  mov r0, r1                        
  11198:  ldrh r0, [r0]                     
  1119a:  movw r1, #0x1770                  
  1119e:  cmp r0, r1                        
  111a0:  blt #0x111f4                      
  111a2:  movs r0, #0                       
  111a4:  ldr r1, [pc, #0xfc]               -> RAM
  111a6:  strh r0, [r1]                     
  111a8:  movs r0, #1                       
  111aa:  bl #0xc94c                        -> func_0x0c94c
  111ae:  movs r0, #6                       
  111b0:  bl #0xd938                        -> func_0x0d938
  111b4:  nop                               
  111b6:  nop                               
  111b8:  nop                               
  111ba:  nop                               
  111bc:  nop                               
  111be:  dsb sy                            
  111c2:  nop                               
  111c4:  nop                               
  111c6:  nop                               
  111c8:  ldr r0, [pc, #0xdc]               -> Cortex-M (NVIC/SCB/SysTick)
  111ca:  ldr r0, [r0]                      
  111cc:  and r0, r0, #0x700                
  111d0:  ldr r1, [pc, #0xd8]               
  111d2:  orrs r0, r1                       
  111d4:  adds r0, r0, #4                   
  111d6:  ldr r1, [pc, #0xd0]               -> Cortex-M (NVIC/SCB/SysTick)
  111d8:  str r0, [r1]                      
  111da:  nop                               
  111dc:  nop                               
  111de:  nop                               
  111e0:  dsb sy                            
  111e4:  nop                               
  111e6:  nop                               
  111e8:  nop                               
  111ea:  nop                               
  111ec:  nop                               
  111ee:  b #0x111ec                        -> 0x111ec (вне списка функций)
  111f0:  b #0x111f6                        -> 0x111f6 (вне списка функций)
  111f2:  b #0x11286                        -> 0x11286 (вне списка функций)
  111f4:  b #0x11288                        -> 0x11288 (вне списка функций)
  111f6:  movs r0, #2                       
  111f8:  ldr r1, [pc, #0x98]               -> RAM
  111fa:  strb r0, [r1]                     
  111fc:  ldr r0, [pc, #0xb0]               -> RAM
  111fe:  ldrb r0, [r0]                     
  11200:  adds r0, r0, #1                   
  11202:  ldr r1, [pc, #0xac]               -> RAM
  11204:  strb r0, [r1]                     
  11206:  mov r0, r1                        
  11208:  ldrb r0, [r0]                     
  1120a:  cmp r0, #5                        
  1120c:  ble #0x11232                      
  1120e:  movs r0, #2                       
  11210:  ldr r1, [pc, #0xa0]               -> RAM
  11212:  strb r0, [r1]                     
  11214:  movs r0, #0                       
  11216:  ldr r1, [pc, #0x98]               -> RAM
  11218:  strb r0, [r1]                     
  1121a:  movs r0, #3                       
  1121c:  ldr r1, [pc, #0x74]               -> RAM
  1121e:  strb r0, [r1]                     
  11220:  movs r0, #2                       
  11222:  bl #0x5bc4                        -> func_0x05bc4
  11226:  movs r0, #1                       
  11228:  ldr r1, [pc, #0x60]               -> RAM
  1122a:  strb r0, [r1]                     
  1122c:  movs r0, #5                       
  1122e:  bl #0x5cd0                        -> func_0x05cd0
  11232:  ldr r0, [pc, #0x80]               -> RAM
  11234:  ldrb r0, [r0]                     
  11236:  cbnz r0, #0x11240                 
  11238:  bl #0x22f4                        -> func_0x022f4
  1123c:  bl #0x8bec                        -> func_0x08bec
  11240:  ldr r0, [pc, #0x70]               -> RAM
  11242:  ldrb r0, [r0]                     
  11244:  subs r0, r0, #1                   
  11246:  ldr r1, [pc, #0x6c]               -> RAM
  11248:  strb r0, [r1]                     
  1124a:  b #0x11288                        -> 0x11288 (вне списка функций)
  1124c:  movs r0, #1                       
  1124e:  ldr r1, [pc, #0x44]               -> RAM
  11250:  strb r0, [r1]                     
  11252:  ldr r0, [pc, #0x64]               -> RAM
  11254:  ldrh r0, [r0]                     
  11256:  adds r0, r0, #1                   
  11258:  ldr r1, [pc, #0x5c]               -> RAM
  1125a:  strh r0, [r1]                     
  1125c:  mov r0, r1                        
  1125e:  ldrh r0, [r0]                     
  11260:  cmp.w r0, #0x2bc                  
  11264:  blt #0x11284                      
  11266:  movs r0, #3                       
  11268:  ldr r1, [pc, #0x28]               -> RAM
  1126a:  strb r0, [r1]                     
  1126c:  movs r0, #0                       
  1126e:  ldr r1, [pc, #0x48]               -> RAM
  11270:  strh r0, [r1]                     
  11272:  movs r0, #3                       
  11274:  bl #0x5bc4                        -> func_0x05bc4
  11278:  movs r0, #1                       
  1127a:  ldr r1, [pc, #0x10]               -> RAM
  1127c:  strb r0, [r1]                     
  1127e:  movs r0, #5                       
  11280:  bl #0x5cd0                        -> func_0x05cd0
  11284:  b #0x11288                        -> 0x11288 (вне списка функций)
  11286:  nop                               
  11288:  nop                               
  1128a:  pop {r4, pc}                      
  ; --- literal-пул @0x1128c (12 слов) — ВНЕ границ функции ---
  1128c:  .word 0x2000002f  ; RAM
  11290:  .word 0x20000a64  ; RAM
  11294:  .word 0x20000035  ; RAM
  11298:  .word 0x20000037  ; RAM
  1129c:  .word 0x20000008  ; RAM
  112a0:  .word 0x2000000c  ; RAM
  112a4:  .word 0x20000002  ; RAM
  112a8:  .word 0xe000ed0c  ; Cortex-M (NVIC/SCB/SysTick)
  112ac:  .word 0x05fa0000
  112b0:  .word 0x2000002d  ; RAM
  112b4:  .word 0x2000002c  ; RAM
  112b8:  .word 0x20000004  ; RAM
```
