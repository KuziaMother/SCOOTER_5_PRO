# func_0x12d90

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012d90) | `0x00012d90` |
| размер кода | 190 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a8b0 — flash-mirror @0x1a8b0 (r1)
- 0x20000b78 — RAM (r1)
- 0x20001ad8 — RAM (r1)
- 0x20001d38 — RAM (r0)
- 0x40004800 — периферия (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x04f38` (0x00004f38, bl)
- `func_0x04f50` (0x00004f50, bl)
- `func_0x04fba` (0x00004fba, bl)
- `func_0x130f2` (0x000130f2, bl)

## Кто вызывает (callers / xrefs)

- `func_0x12fd8` (bl @0x00012fda)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x12dea..0x12e32` (72 Б); цели из: 0x12de6
- `0x12e32..0x12e4c` (26 Б); цели из: 0x12dcc, 0x12dd8
- `0x12e4c..0x12e4e` (2 Б); цели из: 0x12da2

## Дизассембляция

```asm
  12d90:  push {r4, r5, r6, lr}             
  12d92:  movs r5, #0                       
  12d94:  movs r4, #0                       
  12d96:  movw r1, #0x424                   
  12d9a:  ldr r0, [pc, #0xb4]               -> периферия
  12d9c:  bl #0x130f2                       -> func_0x130f2
  12da0:  cmp r0, #0                        
  12da2:  beq #0x12e4c                      
  12da4:  ldr r0, [pc, #0xa8]               -> периферия
  12da6:  ldrh r0, [r0]                     
  12da8:  uxtb r4, r0                       
  12daa:  ldr r0, [pc, #0xa4]               -> периферия
  12dac:  adds r0, r0, #4                   
  12dae:  ldrh r0, [r0]                     
  12db0:  uxtb r4, r0                       
  12db2:  ldr r1, [pc, #0xa0]               -> flash-mirror @0x1a8b0
  12db4:  ldr r0, [r1, #0x10]               
  12db6:  movs r1, #0                       
  12db8:  bl #0x4f38                        -> func_0x04f38
  12dbc:  ldr r1, [pc, #0x94]               -> flash-mirror @0x1a8b0
  12dbe:  ldr r0, [r1, #0x10]               
  12dc0:  bl #0x4f50                        -> func_0x04f50
  12dc4:  rsb.w r0, r0, #0x96               
  12dc8:  uxth r5, r0                       
  12dca:  cmp r5, #0                        
  12dcc:  ble #0x12e32                      
  12dce:  ldr r0, [pc, #0x88]               -> RAM
  12dd0:  ldrb r0, [r0]                     
  12dd2:  and r0, r0, #7                    
  12dd6:  cmp r0, #7                        
  12dd8:  bge #0x12e32                      
  12dda:  ldr r0, [pc, #0x7c]               -> RAM
  12ddc:  ldrb r4, [r0, #1]                 
  12dde:  nop                               
  12de0:  adds r0, r4, #1                   
  12de2:  uxtb r4, r0                       
  12de4:  cmp r4, #3                        
  12de6:  blt #0x12dea                      
  12de8:  movs r4, #0                       
  12dea:  ldr r0, [pc, #0x6c]               -> RAM
  12dec:  ldrb r0, [r0]                     
  12dee:  movs r1, #1                       
  12df0:  lsls r1, r4                       
  12df2:  ands r0, r1                       
  12df4:  cmp r0, #0                        
  12df6:  bne #0x12de0                      
  12df8:  ldr r0, [pc, #0x5c]               -> RAM
  12dfa:  ldrb r0, [r0]                     
  12dfc:  movs r1, #1                       
  12dfe:  lsls r1, r4                       
  12e00:  orrs r0, r1                       
  12e02:  ldr r1, [pc, #0x54]               -> RAM
  12e04:  strb r0, [r1]                     
  12e06:  add.w r1, r4, r4, lsl #1          
  12e0a:  add.w r2, r1, r4, lsl #4          
  12e0e:  ldr r1, [pc, #0x48]               -> RAM
  12e10:  adds r1, r1, #2                   
  12e12:  add.w r1, r1, r2, lsl #3          
  12e16:  adds r0, r1, #2                   
  12e18:  mov r2, r5                        
  12e1a:  ldr r1, [pc, #0x40]               -> RAM
  12e1c:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  12e20:  add.w r0, r4, r4, lsl #1          
  12e24:  add.w r1, r0, r4, lsl #4          
  12e28:  ldr r0, [pc, #0x2c]               -> RAM
  12e2a:  adds r0, r0, #2                   
  12e2c:  add.w r0, r0, r1, lsl #3          
  12e30:  strh r5, [r0]                     
  12e32:  ldr r1, [pc, #0x20]               -> flash-mirror @0x1a8b0
  12e34:  ldr r0, [r1, #0x10]               
  12e36:  movs r1, #0x96                    
  12e38:  bl #0x4fba                        -> func_0x04fba
  12e3c:  ldr r1, [pc, #0x14]               -> flash-mirror @0x1a8b0
  12e3e:  ldr r0, [r1, #0x10]               
  12e40:  movs r1, #1                       
  12e42:  bl #0x4f38                        -> func_0x04f38
  12e46:  movs r0, #0                       
  12e48:  ldr r1, [pc, #0x14]               -> RAM
  12e4a:  strh r0, [r1]                     
  12e4c:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x12e50 (5 слов) — ВНЕ границ функции ---
  12e50:  .word 0x40004800  ; периферия
  12e54:  .word 0x0801a8b0  ; flash-mirror @0x1a8b0
  12e58:  .word 0x20001d38  ; RAM
  12e5c:  .word 0x20001ad8  ; RAM
  12e60:  .word 0x20000b78  ; RAM
```
