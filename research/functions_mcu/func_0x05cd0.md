# func_0x05cd0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005cd0) | `0x00005cd0` |
| размер кода | 194 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019984 — flash-mirror @0x19984 (r0)
- 0x08019998 — flash-mirror @0x19998 (r0)
- 0x20000037 — RAM (r0)
- 0x2000003f — RAM (r0)
- 0x20000100 — RAM (r0)
- 0x20000103 — RAM (r0)
- 0x20000104 — RAM (r0)
- 0x20000a4c — RAM (r0)
- 0x20000de8 — RAM (r1)
- 0x40003000 — периферия (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x030e0` (0x000030e0, bl)
- `func_0x0332c` (0x0000332c, bl)
- `func_0x035ec` (0x000035ec, bl)
- `func_0x03600` (0x00003600, bl)
- 0x05d10 (b, вне списка функций)
- 0x05d62 (b, вне списка функций)
- 0x05d64 (b, вне списка функций)
- 0x0ae98 (bl, вне списка функций)
- `func_0x0af94` (0x0000af94, bl)
- `func_0x0c2a8` (0x0000c2a8, bl)
- `func_0x0c94c` (0x0000c94c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x110fc` (bl @0x0001112c)
- `func_0x110fc` (bl @0x0001122e)
- `func_0x110fc` (bl @0x00011280)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x05d24..0x05d60` (60 Б); цели из: 0x05d1e
- `0x05d60..0x05d62` (2 Б); цели из: 0x05d44, 0x05d4c
- `0x05d62..0x05d64` (2 Б); цели из: 0x05d0e
- `0x05d64..0x05d92` (46 Б); цели из: 0x05d22, 0x05d60

## Дизассембляция

```asm
  05cd0:  push {r4, r5, lr}                 
  05cd2:  sub sp, #0x24                     
  05cd4:  mov r4, r0                        
  05cd6:  movs r5, #0                       
  05cd8:  mov r0, r4                        
  05cda:  bl #0xc94c                        -> func_0x0c94c
  05cde:  movs r2, #0x24                    
  05ce0:  ldr r1, [pc, #0xb0]               -> RAM
  05ce2:  mov r0, sp                        
  05ce4:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  05ce8:  ldr r0, [pc, #0xa8]               -> RAM
  05cea:  subs r0, #0x10                    
  05cec:  ldr r3, [r0, #0xc]                
  05cee:  ldr r2, [r0, #8]                  
  05cf0:  ldr r1, [r0, #4]                  
  05cf2:  ldr r0, [r0]                      
  05cf4:  bl #0xae98                        -> 0x0ae98 (вне списка функций)
  05cf8:  ldr r0, [pc, #0x9c]               -> RAM
  05cfa:  strb r4, [r0]                     
  05cfc:  ldr r0, [pc, #0x9c]               -> RAM
  05cfe:  ldr r0, [r0]                      
  05d00:  add r0, r4                        
  05d02:  ldr r1, [pc, #0x98]               -> RAM
  05d04:  str r0, [r1]                      
  05d06:  movw r0, #0xaaaa                  
  05d0a:  ldr r1, [pc, #0x94]               -> периферия
  05d0c:  str r0, [r1]                      
  05d0e:  b #0x5d62                         -> 0x05d62 (вне списка функций)
  05d10:  bl #0x35ec                        -> func_0x035ec
  05d14:  adds r0, r5, #1                   
  05d16:  uxth r5, r0                       
  05d18:  movw r0, #0xea60                  
  05d1c:  cmp r5, r0                        
  05d1e:  ble #0x5d24                       
  05d20:  movs r5, #0                       
  05d22:  b #0x5d64                         -> 0x05d64 (вне списка функций)
  05d24:  mov.w r1, #0x1000                 
  05d28:  movs r0, #1                       
  05d2a:  bl #0xc2a8                        -> func_0x0c2a8
  05d2e:  movs r0, #0xa0                    
  05d30:  str r0, [sp, #0x20]               
  05d32:  nop                               
  05d34:  ldr r0, [sp, #0x20]               
  05d36:  subs r1, r0, #1                   
  05d38:  str r1, [sp, #0x20]               
  05d3a:  cmp r0, #0                        
  05d3c:  bne #0x5d34                       
  05d3e:  ldr r0, [pc, #0x64]               -> RAM
  05d40:  ldrb r0, [r0]                     
  05d42:  cmp r0, #1                        
  05d44:  beq #0x5d60                       
  05d46:  ldr r0, [pc, #0x5c]               -> RAM
  05d48:  ldrb r0, [r0]                     
  05d4a:  cmp r0, #2                        
  05d4c:  beq #0x5d60                       
  05d4e:  ldr r0, [pc, #0x58]               -> RAM
  05d50:  ldrb r0, [r0]                     
  05d52:  cbnz r0, #0x5d60                  
  05d54:  ldr r0, [pc, #0x54]               -> RAM
  05d56:  ldrb r0, [r0]                     
  05d58:  cbnz r0, #0x5d60                  
  05d5a:  ldr r0, [pc, #0x54]               -> RAM
  05d5c:  ldrb r0, [r0]                     
  05d5e:  cbz r0, #0x5d62                   
  05d60:  b #0x5d64                         -> 0x05d64 (вне списка функций)
  05d62:  b #0x5d10                         -> 0x05d10 (вне списка функций)
  05d64:  nop                               
  05d66:  movw r0, #0xaaaa                  
  05d6a:  ldr r1, [pc, #0x34]               -> периферия
  05d6c:  str r0, [r1]                      
  05d6e:  bl #0x30e0                        -> func_0x030e0
  05d72:  movs r1, #1                       
  05d74:  ldr r0, [pc, #0x3c]               -> flash-mirror @0x19984
  05d76:  bl #0x332c                        -> func_0x0332c
  05d7a:  movs r1, #1                       
  05d7c:  ldr r0, [pc, #0x38]               -> flash-mirror @0x19998
  05d7e:  bl #0x332c                        -> func_0x0332c
  05d82:  ldr r0, [pc, #0x10]               -> RAM
  05d84:  subs r0, #0x10                    
  05d86:  bl #0xaf94                        -> func_0x0af94
  05d8a:  bl #0x3600                        -> func_0x03600
  05d8e:  add sp, #0x24                     
  05d90:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x05d94 (10 слов) — ВНЕ границ функции ---
  05d94:  .word 0x20000de8  ; RAM
  05d98:  .word 0x2000003f  ; RAM
  05d9c:  .word 0x20000a4c  ; RAM
  05da0:  .word 0x40003000  ; периферия
  05da4:  .word 0x20000037  ; RAM
  05da8:  .word 0x20000104  ; RAM
  05dac:  .word 0x20000103  ; RAM
  05db0:  .word 0x20000100  ; RAM
  05db4:  .word 0x08019984  ; flash-mirror @0x19984
  05db8:  .word 0x08019998  ; flash-mirror @0x19998
```
