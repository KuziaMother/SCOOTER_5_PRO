# func_0x0c20c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c20c) | `0x0000c20c` |
| размер кода | 134 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00186a00 — прочее (r0)
- 0x20000dd8 — RAM (r0)

## Вызовы (callees)

- `func_0x016d4` (0x000016d4, bl)
- `func_0x0175c` (0x0000175c, bl)
- `func_0x0178c` (0x0000178c, bl)
- `func_0x01bdc` (0x00001bdc, bl)
- `func_0x02a94` (0x00002a94, bl)
- `func_0x08468` (0x00008468, bl)
- `func_0x0af94` (0x0000af94, bl)
- 0x0c28e (b, вне списка функций)
- `func_0x10780` (0x00010780, bl)

## Кто вызывает (callers / xrefs)

- `func_0x05b98` (bl @0x00005bb0)
- `func_0x05c9c` (bl @0x00005cb0)
- `func_0x05dbc` (bl @0x00005dcc)


## Дизассембляция

```asm
  0c20c:  push {r3, r4, r5, lr}             
  0c20e:  mov r4, r0                        
  0c210:  cmp r4, #5                        
  0c212:  bhs #0xc28c                       
  0c214:  tbb [pc, r4]                      
  0c218:  lsls r3, r0, #0x14                
  0c21a:  subs r4, r0, #0                   
  0c21c:  movs r7, r3                       
  0c21e:  nop                               
  0c220:  b #0xc28e                         -> 0x0c28e (вне списка функций)
  0c222:  ldr r0, [pc, #0x70]               -> RAM
  0c224:  bl #0xaf94                        -> func_0x0af94
  0c228:  movs r0, #0x9a                    
  0c22a:  bl #0x1bdc                        -> func_0x01bdc
  0c22e:  bl #0x16d4                        -> func_0x016d4
  0c232:  ldr r0, [pc, #0x64]               
  0c234:  str r0, [sp]                      
  0c236:  nop                               
  0c238:  ldr r0, [sp]                      
  0c23a:  subs r1, r0, #1                   
  0c23c:  str r1, [sp]                      
  0c23e:  cmp r0, #0                        
  0c240:  bne #0xc238                       
  0c242:  bl #0x175c                        -> func_0x0175c
  0c246:  bl #0x178c                        -> func_0x0178c
  0c24a:  bl #0x10780                       -> func_0x10780
  0c24e:  bl #0x8468                        -> func_0x08468
  0c252:  b #0xc28e                         -> 0x0c28e (вне списка функций)
  0c254:  nop                               
  0c256:  ldr r0, [pc, #0x3c]               -> RAM
  0c258:  bl #0xaf94                        -> func_0x0af94
  0c25c:  movs r0, #0x9a                    
  0c25e:  bl #0x1bdc                        -> func_0x01bdc
  0c262:  bl #0x16d4                        -> func_0x016d4
  0c266:  ldr r0, [pc, #0x30]               
  0c268:  str r0, [sp]                      
  0c26a:  nop                               
  0c26c:  ldr r0, [sp]                      
  0c26e:  subs r1, r0, #1                   
  0c270:  str r1, [sp]                      
  0c272:  cmp r0, #0                        
  0c274:  bne #0xc26c                       
  0c276:  bl #0x175c                        -> func_0x0175c
  0c27a:  bl #0x178c                        -> func_0x0178c
  0c27e:  bl #0x10780                       -> func_0x10780
  0c282:  bl #0x2a94                        -> func_0x02a94
  0c286:  bl #0x8468                        -> func_0x08468
  0c28a:  b #0xc28e                         -> 0x0c28e (вне списка функций)
  0c28c:  nop                               
  0c28e:  nop                               
  0c290:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x0c294 (2 слов) — ВНЕ границ функции ---
  0c294:  .word 0x20000dd8  ; RAM
  0c298:  .word 0x00186a00
```
