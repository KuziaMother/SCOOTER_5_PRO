# func_0x0e200

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e200) | `0x0000e200` |
| размер кода | 198 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019f68 — flash-mirror @0x19f68 (r2)

## Вызовы (callees)

- `func_0x08f58` (0x00008f58, bl)
- 0x0e288 (b, вне списка функций)
- 0x0e2c2 (b, вне списка функций)
- 0x16266 (bl, вне списка функций)
- 0x1638a (bl, вне списка функций)
- `func_0x16938` (0x00016938, bl)
- `func_0x17150` (0x00017150, bl)

## Кто вызывает (callers / xrefs)

- `func_0x06ccc` (bl @0x00006db8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0e220..0x0e22a` (10 Б); цели из: 0x0e21c
- `0x0e22a..0x0e242` (24 Б); цели из: 0x0e226
- `0x0e242..0x0e286` (68 Б); цели из: 0x0e23e
- `0x0e286..0x0e288` (2 Б); цели из: 0x0e280
- `0x0e288..0x0e290` (8 Б); цели из: 0x0e272, 0x0e284
- `0x0e290..0x0e2a2` (18 Б); цели из: 0x0e22c, 0x0e234
- `0x0e2a2..0x0e2aa` (8 Б); цели из: 0x0e29c
- `0x0e2aa..0x0e2bc` (18 Б); цели из: 0x0e210, 0x0e214
- `0x0e2bc..0x0e2c2` (6 Б); цели из: 0x0e2b6
- `0x0e2c2..0x0e2c6` (4 Б); цели из: 0x0e28e, 0x0e2a8

## Дизассембляция

```asm
  0e200:  push.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  0e204:  mov sl, r0                        
  0e206:  mov fp, r1                        
  0e208:  mov r8, r2                        
  0e20a:  mov sb, r3                        
  0e20c:  ldr r4, [sp, #0x30]               
  0e20e:  cmp r8, sl                        
  0e210:  blo #0xe2aa                       
  0e212:  cmp sb, fp                        
  0e214:  bls #0xe2aa                       
  0e216:  sub.w r5, sb, fp                  
  0e21a:  cmp r5, sb                        
  0e21c:  bls #0xe220                       
  0e21e:  movs r5, #0                       
  0e220:  sub.w r7, r8, sl                  
  0e224:  cmp r7, r8                        
  0e226:  bls #0xe22a                       
  0e228:  movs r7, #0                       
  0e22a:  cmp r5, r7                        
  0e22c:  bls #0xe290                       
  0e22e:  bl #0x8f58                        -> func_0x08f58
  0e232:  cmp r0, #0x1e                     
  0e234:  ble #0xe290                       
  0e236:  movw r6, #0x262c                  
  0e23a:  subs r7, r5, r7                   
  0e23c:  cmp r7, r5                        
  0e23e:  bls #0xe242                       
  0e240:  movs r7, #0                       
  0e242:  bl #0x8f58                        -> func_0x08f58
  0e246:  movs r3, #6                       
  0e248:  ldr r2, [pc, #0x7c]               -> flash-mirror @0x19f68
  0e24a:  add.w r1, r2, #0x70               
  0e24e:  str r0, [sp]                      
  0e250:  bl #0x16938                       -> func_0x16938
  0e254:  movs r1, #4                       
  0e256:  str r0, [sp, #4]                  
  0e258:  bl #0x17150                       -> func_0x17150
  0e25c:  str r0, [sp, #8]                  
  0e25e:  mul r0, r6, r7                    
  0e262:  ldr r1, [sp, #8]                  
  0e264:  bl #0x1638a                       -> 0x1638a (вне списка функций)
  0e268:  mov r5, r0                        
  0e26a:  lsls r0, r6, #1                   
  0e26c:  str r0, [r4]                      
  0e26e:  ldr r0, [r4]                      
  0e270:  cmp r0, r5                        
  0e272:  blo #0xe288                       
  0e274:  movs r1, #5                       
  0e276:  mov r0, r6                        
  0e278:  bl #0x16266                       -> 0x16266 (вне списка функций)
  0e27c:  mov r6, r0                        
  0e27e:  cmp r5, r6                        
  0e280:  bhs #0xe286                       
  0e282:  str r6, [r4]                      
  0e284:  b #0xe288                         -> 0x0e288 (вне списка функций)
  0e286:  str r5, [r4]                      
  0e288:  movs r1, #1                       
  0e28a:  ldr r0, [sp, #0x34]               
  0e28c:  strb r1, [r0]                     
  0e28e:  b #0xe2c2                         -> 0x0e2c2 (вне списка функций)
  0e290:  mvn r0, #0xb                      
  0e294:  str r0, [r4]                      
  0e296:  ldr r0, [r4]                      
  0e298:  cmn.w r0, #2                      
  0e29c:  bls #0xe2a2                       
  0e29e:  movs r0, #0                       
  0e2a0:  str r0, [r4]                      
  0e2a2:  movs r1, #0                       
  0e2a4:  ldr r0, [sp, #0x34]               
  0e2a6:  strb r1, [r0]                     
  0e2a8:  b #0xe2c2                         -> 0x0e2c2 (вне списка функций)
  0e2aa:  mvn r0, #0x15                     
  0e2ae:  str r0, [r4]                      
  0e2b0:  ldr r0, [r4]                      
  0e2b2:  cmn.w r0, #2                      
  0e2b6:  bls #0xe2bc                       
  0e2b8:  movs r0, #0                       
  0e2ba:  str r0, [r4]                      
  0e2bc:  movs r1, #0                       
  0e2be:  ldr r0, [sp, #0x34]               
  0e2c0:  strb r1, [r0]                     
  0e2c2:  pop.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x0e2c8 (1 слов) — ВНЕ границ функции ---
  0e2c8:  .word 0x08019f68  ; flash-mirror @0x19f68
```
