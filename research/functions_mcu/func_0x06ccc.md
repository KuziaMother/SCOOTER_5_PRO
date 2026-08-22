# func_0x06ccc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080006ccc) | `0x00006ccc` |
| размер кода | 378 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000128b — RAM (r1)
- 0x200012ba — RAM (r0)

## Вызовы (callees)

- 0x06d4c (b, вне списка функций)
- 0x06e32 (b, вне списка функций)
- 0x06e34 (b, вне списка функций)
- 0x06e36 (b, вне списка функций)
- `func_0x08e14` (0x00008e14, bl)
- 0x08e20 (bl, вне списка функций)
- `func_0x0e200` (0x0000e200, bl)
- 0x10f7c (bl, вне списка функций)
- 0x10fe0 (bl, вне списка функций)
- 0x164d4 (bl, вне списка функций)
- 0x164e0 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x06cec..0x06d26` (58 Б); цели из: 0x06cdc
- `0x06d26..0x06d4a` (36 Б); цели из: 0x06d1e
- `0x06d4a..0x06d4c` (2 Б); цели из: 0x06d2e
- `0x06d4c..0x06d6c` (32 Б); цели из: 0x06d24
- `0x06d6c..0x06d80` (20 Б); цели из: 0x06d68
- `0x06d80..0x06d82` (2 Б); цели из: 0x06d52
- `0x06d82..0x06dbe` (60 Б); цели из: 0x06d22
- `0x06dbe..0x06de6` (40 Б); цели из: 0x06d88
- `0x06de6..0x06e06` (32 Б); цели из: 0x06dc8
- `0x06e06..0x06e1c` (22 Б); цели из: 0x06e02
- `0x06e1c..0x06e2e` (18 Б); цели из: 0x06dec
- `0x06e2e..0x06e32` (4 Б); цели из: 0x06e28
- `0x06e32..0x06e34` (2 Б); цели из: 0x06dbc, 0x06de4, 0x06e1a
- `0x06e34..0x06e36` (2 Б); цели из: 0x06d4a, 0x06d80
- `0x06e36..0x06e46` (16 Б); цели из: 0x06d14

## Дизассембляция

```asm
  06ccc:  push {r2, r3, r4, r5, r6, lr}     
  06cce:  movs r0, #1                       
  06cd0:  bl #0x10fe0                       -> 0x10fe0 (вне списка функций)
  06cd4:  ldr r0, [pc, #0x170]              -> RAM
  06cd6:  ldrb.w r0, [r0, #0x64]            
  06cda:  cmp r0, #0x1f                     
  06cdc:  bhs #0x6cec                       
  06cde:  ldr r0, [pc, #0x168]              -> RAM
  06ce0:  ldrb.w r0, [r0, #0x64]            
  06ce4:  adds r0, r0, #1                   
  06ce6:  ldr r1, [pc, #0x160]              -> RAM
  06ce8:  strb.w r0, [r1, #0x64]            
  06cec:  ldr r0, [pc, #0x158]              -> RAM
  06cee:  ldrb.w r0, [r0, #0x62]            
  06cf2:  cbnz r0, #0x6d16                  
  06cf4:  movs r0, #1                       
  06cf6:  ldr r1, [pc, #0x150]              -> RAM
  06cf8:  strb.w r0, [r1, #0x62]            
  06cfc:  movs r0, #2                       
  06cfe:  strb.w r0, [r1, #0x63]            
  06d02:  movs r0, #0                       
  06d04:  ldr r1, [pc, #0x144]              -> RAM
  06d06:  strb.w r0, [r1, #0x2c]            
  06d0a:  subs r0, r0, #2                   
  06d0c:  str r0, [r1, #0x14]               
  06d0e:  movs r0, #0                       
  06d10:  ldr r1, [pc, #0x134]              -> RAM
  06d12:  str r0, [r1, #0x3c]               
  06d14:  b #0x6e36                         -> 0x06e36 (вне списка функций)
  06d16:  ldr r0, [pc, #0x130]              -> RAM
  06d18:  ldrb.w r0, [r0, #0x63]            
  06d1c:  cmp r0, #1                        
  06d1e:  beq #0x6d26                       
  06d20:  cmp r0, #2                        
  06d22:  bne #0x6d82                       
  06d24:  b #0x6d4c                         -> 0x06d4c (вне списка функций)
  06d26:  ldr r0, [pc, #0x120]              -> RAM
  06d28:  ldrb.w r0, [r0, #0x64]            
  06d2c:  cmp r0, #0x14                     
  06d2e:  blt #0x6d4a                       
  06d30:  movs r0, #2                       
  06d32:  ldr r1, [pc, #0x114]              -> RAM
  06d34:  strb.w r0, [r1, #0x63]            
  06d38:  movs r0, #0                       
  06d3a:  ldr r1, [pc, #0x110]              -> RAM
  06d3c:  strb.w r0, [r1, #0x2c]            
  06d40:  subs r0, r0, #2                   
  06d42:  str r0, [r1, #0x14]               
  06d44:  movs r0, #0                       
  06d46:  ldr r1, [pc, #0x100]              -> RAM
  06d48:  str r0, [r1, #0x3c]               
  06d4a:  b #0x6e34                         -> 0x06e34 (вне списка функций)
  06d4c:  bl #0x8e14                        -> func_0x08e14
  06d50:  cmp r0, #1                        
  06d52:  bne #0x6d80                       
  06d54:  movs r0, #3                       
  06d56:  ldr r1, [pc, #0xf0]               -> RAM
  06d58:  strb.w r0, [r1, #0x63]            
  06d5c:  movs r0, #0                       
  06d5e:  str r0, [r1, #0x3c]               
  06d60:  mvn r4, #0x1f                     
  06d64:  cmn.w r4, #2                      
  06d68:  bls #0x6d6c                       
  06d6a:  movs r4, #0                       
  06d6c:  ldr r0, [pc, #0xdc]               -> RAM
  06d6e:  str r4, [r0, #0x14]               
  06d70:  bl #0x164d4                       -> 0x164d4 (вне списка функций)
  06d74:  ldr r1, [pc, #0xd0]               -> RAM
  06d76:  str r0, [r1, #0x34]               
  06d78:  bl #0x164e0                       -> 0x164e0 (вне списка функций)
  06d7c:  ldr r1, [pc, #0xc8]               -> RAM
  06d7e:  str r0, [r1, #0x38]               
  06d80:  b #0x6e34                         -> 0x06e34 (вне списка функций)
  06d82:  bl #0x8e20                        -> 0x08e20 (вне списка функций)
  06d86:  cmp r0, #1                        
  06d88:  bne #0x6dbe                       
  06d8a:  ldr r1, [pc, #0xbc]               -> RAM
  06d8c:  strb.w r0, [r1, #0x63]            
  06d90:  movs r0, #0                       
  06d92:  strb.w r0, [r1, #0x64]            
  06d96:  bl #0x164e0                       -> 0x164e0 (вне списка функций)
  06d9a:  mov r5, r0                        
  06d9c:  bl #0x164d4                       -> 0x164d4 (вне списка функций)
  06da0:  mov r6, r0                        
  06da2:  ldr r0, [pc, #0xa8]               -> RAM
  06da4:  adds r0, #0x2c                    
  06da6:  sub.w r1, r0, #0x18               
  06daa:  ldr r2, [pc, #0x9c]               -> RAM
  06dac:  strd r1, r0, [sp]                 
  06db0:  ldr r1, [r2, #0x38]               
  06db2:  ldr r0, [r2, #0x34]               
  06db4:  mov r3, r5                        
  06db6:  mov r2, r6                        
  06db8:  bl #0xe200                        -> func_0x0e200
  06dbc:  b #0x6e32                         -> 0x06e32 (вне списка функций)
  06dbe:  ldr r0, [pc, #0x88]               -> RAM
  06dc0:  ldr r0, [r0, #0x3c]               
  06dc2:  movw r1, #0xa8c0                  
  06dc6:  cmp r0, r1                        
  06dc8:  blo #0x6de6                       
  06dca:  movs r0, #2                       
  06dcc:  ldr r1, [pc, #0x78]               -> RAM
  06dce:  strb.w r0, [r1, #0x63]            
  06dd2:  movs r0, #0                       
  06dd4:  ldr r1, [pc, #0x74]               -> RAM
  06dd6:  strb.w r0, [r1, #0x2c]            
  06dda:  subs r0, r0, #2                   
  06ddc:  str r0, [r1, #0x14]               
  06dde:  movs r0, #0                       
  06de0:  ldr r1, [pc, #0x64]               -> RAM
  06de2:  str r0, [r1, #0x3c]               
  06de4:  b #0x6e32                         -> 0x06e32 (вне списка функций)
  06de6:  bl #0x8e14                        -> func_0x08e14
  06dea:  cmp r0, #1                        
  06dec:  bne #0x6e1c                       
  06dee:  movs r0, #3                       
  06df0:  ldr r1, [pc, #0x54]               -> RAM
  06df2:  strb.w r0, [r1, #0x63]            
  06df6:  movs r0, #0                       
  06df8:  str r0, [r1, #0x3c]               
  06dfa:  mvn r4, #0x1f                     
  06dfe:  cmn.w r4, #2                      
  06e02:  bls #0x6e06                       
  06e04:  movs r4, #0                       
  06e06:  ldr r0, [pc, #0x44]               -> RAM
  06e08:  str r4, [r0, #0x14]               
  06e0a:  bl #0x164d4                       -> 0x164d4 (вне списка функций)
  06e0e:  ldr r1, [pc, #0x38]               -> RAM
  06e10:  str r0, [r1, #0x34]               
  06e12:  bl #0x164e0                       -> 0x164e0 (вне списка функций)
  06e16:  ldr r1, [pc, #0x30]               -> RAM
  06e18:  str r0, [r1, #0x38]               
  06e1a:  b #0x6e32                         -> 0x06e32 (вне списка функций)
  06e1c:  ldr r0, [pc, #0x28]               -> RAM
  06e1e:  ldr r0, [r0, #0x3c]               
  06e20:  adds r4, r0, #1                   
  06e22:  ldr r0, [pc, #0x24]               -> RAM
  06e24:  ldr r0, [r0, #0x3c]               
  06e26:  cmp r0, r4                        
  06e28:  bls #0x6e2e                       
  06e2a:  mov.w r4, #-1                     
  06e2e:  ldr r0, [pc, #0x18]               -> RAM
  06e30:  str r4, [r0, #0x3c]               
  06e32:  nop                               
  06e34:  nop                               
  06e36:  movs r0, #0                       
  06e38:  bl #0x10fe0                       -> 0x10fe0 (вне списка функций)
  06e3c:  ldr r1, [pc, #0xc]                -> RAM
  06e3e:  ldr r0, [r1, #0x14]               
  06e40:  bl #0x10f7c                       -> 0x10f7c (вне списка функций)
  06e44:  pop {r2, r3, r4, r5, r6, pc}      
  ; --- literal-пул @0x06e48 (2 слов) — ВНЕ границ функции ---
  06e48:  .word 0x200012ba  ; RAM
  06e4c:  .word 0x2000128b  ; RAM
```
