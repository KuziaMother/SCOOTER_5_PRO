# func_0x131fc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800131fc) | `0x000131fc` |
| размер кода | 130 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001743 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x12c24` (0x00012c24, bl)
- 0x1320c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04a4c` (bl @0x00004a88)
- `func_0x04a4c` (bl @0x00004ad8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x13210..0x1322c` (28 Б); цели из: 0x1320a
- `0x1322c..0x1327a` (78 Б); цели из: 0x13228
- `0x1327a..0x1327e` (4 Б); цели из: 0x1321a

## Дизассембляция

```asm
  131fc:  push.w {r4, r5, r6, r7, r8, lr}   
  13200:  mov r7, r0                        
  13202:  mov r6, r1                        
  13204:  mov r5, r2                        
  13206:  movs r4, #0                       
  13208:  cmp r5, #0x96                     
  1320a:  ble #0x13210                      
  1320c:  pop.w {r4, r5, r6, r7, r8, pc}    
  13210:  ldr r0, [pc, #0x6c]               -> RAM
  13212:  ldrb r0, [r0]                     
  13214:  and r0, r0, #7                    
  13218:  cmp r0, #7                        
  1321a:  beq #0x1327a                      
  1321c:  ldr r0, [pc, #0x60]               -> RAM
  1321e:  ldrb r4, [r0, #1]                 
  13220:  nop                               
  13222:  adds r0, r4, #1                   
  13224:  uxtb r4, r0                       
  13226:  cmp r4, #3                        
  13228:  blt #0x1322c                      
  1322a:  movs r4, #0                       
  1322c:  ldr r0, [pc, #0x50]               -> RAM
  1322e:  ldrb r0, [r0]                     
  13230:  movs r1, #1                       
  13232:  lsls r1, r4                       
  13234:  ands r0, r1                       
  13236:  cmp r0, #0                        
  13238:  bne #0x13222                      
  1323a:  ldr r0, [pc, #0x44]               -> RAM
  1323c:  ldrb r1, [r0]                     
  1323e:  movs r0, #1                       
  13240:  lsls r0, r4                       
  13242:  orrs r1, r0                       
  13244:  uxtb r0, r1                       
  13246:  ldr r1, [pc, #0x38]               -> RAM
  13248:  strb r0, [r1]                     
  1324a:  add.w r0, r4, r4, lsl #1          
  1324e:  add.w r1, r0, r4, lsl #4          
  13252:  ldr r0, [pc, #0x2c]               -> RAM
  13254:  adds r0, r0, #2                   
  13256:  add.w r0, r0, r1, lsl #3          
  1325a:  strh r5, [r0]                     
  1325c:  add.w r1, r4, r4, lsl #1          
  13260:  add.w r2, r1, r4, lsl #4          
  13264:  ldr r1, [pc, #0x18]               -> RAM
  13266:  adds r1, r1, #2                   
  13268:  add.w r1, r1, r2, lsl #3          
  1326c:  adds r0, r1, #2                   
  1326e:  mov r2, r5                        
  13270:  mov r1, r6                        
  13272:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  13276:  bl #0x12c24                       -> func_0x12c24
  1327a:  nop                               
  1327c:  b #0x1320c                        -> 0x1320c (вне списка функций)
  ; --- literal-пул @0x13280 (1 слов) — ВНЕ границ функции ---
  13280:  .word 0x20001743  ; RAM
```
