# func_0x0df10

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000df10) | `0x0000df10` |
| размер кода | 338 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200009b4 — RAM (r0)
- 0x200009bc — RAM (r1)
- 0x4302eb03 — периферия (r5)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x03b42` (0x00003b42, bl)
- 0x0de08 (bl, вне списка функций)
- 0x0dea4 (bl, вне списка функций)
- `func_0x0ded4` (0x0000ded4, bl)
- 0x0df40 (b, вне списка функций)
- 0x0e052 (b, вне списка функций)
- 0x0e06c (bl, вне списка функций)
- 0x0e0b4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04a30` (bl @0x00004a42)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0df44..0x0df4e` (10 Б); цели из: 0x0df3e
- `0x0df4e..0x0df5e` (16 Б); цели из: 0x0df4a
- `0x0df5e..0x0df86` (40 Б); цели из: 0x0df50
- `0x0df86..0x0dfbc` (54 Б); цели из: 0x0df82
- `0x0dfbc..0x0dfe2` (38 Б); цели из: 0x0dfac
- `0x0dfe2..0x0e050` (110 Б); цели из: 0x0dfd2
- `0x0e050..0x0e052` (2 Б); цели из: 0x0df8c
- `0x0e052..0x0e05e` (12 Б); цели из: 0x0dfbc, 0x0dfe2, 0x0e006, 0x0e02a…
- `0x0e05e..0x0e062` (4 Б); цели из: 0x0e056

## Дизассембляция

```asm
  0df10:  push {r4, r5, r6, r7, lr}         
  0df12:  sub sp, #0x3c                     
  0df14:  mov r4, r0                        
  0df16:  movs r6, #0                       
  0df18:  movs r5, #0                       
  0df1a:  movs r7, #0                       
  0df1c:  ldrb r0, [r4, #2]                 
  0df1e:  strb.w r0, [sp, #0x18]            
  0df22:  ldrb r1, [r4, #4]                 
  0df24:  ldrb r0, [r4, #3]                 
  0df26:  add.w r0, r1, r0, lsl #8          
  0df2a:  uxth r0, r0                       
  0df2c:  strh.w r0, [sp, #0x19]            
  0df30:  ldrb.w r0, [sp, #0x1a]            
  0df34:  lsrs r0, r0, #4                   
  0df36:  lsls r5, r0, #2                   
  0df38:  ldrb.w r0, [sp, #0x18]            
  0df3c:  cmp r0, #0xaa                     
  0df3e:  beq #0xdf44                       
  0df40:  add sp, #0x3c                     
  0df42:  pop {r4, r5, r6, r7, pc}          
  0df44:  ldrh r1, [r4]                     
  0df46:  adds r0, r5, #5                   
  0df48:  cmp r1, r0                        
  0df4a:  bge #0xdf4e                       
  0df4c:  b #0xdf40                         -> 0x0df40 (вне списка функций)
  0df4e:  cmp r5, #0                        
  0df50:  ble #0xdf5e                       
  0df52:  mov r2, r5                        
  0df54:  adds r1, r4, #5                   
  0df56:  add.w r0, sp, #0x1b               
  0df5a:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0df5e:  adds r0, r5, #4                   
  0df60:  adds r1, r4, #2                   
  0df62:  ldrb r2, [r1, r0]                 
  0df64:  adds r0, r5, #3                   
  0df66:  ldrb r0, [r1, r0]                 
  0df68:  add.w r0, r2, r0, lsl #8          
  0df6c:  uxth r0, r0                       
  0df6e:  strh.w r0, [sp, #0x37]            
  0df72:  adds r1, r5, #2                   
  0df74:  adds r0, r4, #3                   
  0df76:  bl #0x3b42                        -> func_0x03b42
  0df7a:  mov r7, r0                        
  0df7c:  ldrh.w r0, [sp, #0x37]            
  0df80:  cmp r0, r7                        
  0df82:  beq #0xdf86                       
  0df84:  b #0xdf40                         -> 0x0df40 (вне списка функций)
  0df86:  ldr r0, [pc, #0xdc]               -> RAM
  0df88:  ldrb r0, [r0]                     
  0df8a:  cmp r0, #6                        
  0df8c:  bhs #0xe050                       
  0df8e:  tbb [pc, r0]                      
  0df92:  lsls r7, r3, #0xd                 
  0df94:  cmp r1, #0x16                     
  0df96:  ldr r5, [pc, #0xec]               -> периферия
  0df98:  movs r2, #0x11                    
  0df9a:  add r1, sp, #0x28                 
  0df9c:  mov r0, sp                        
  0df9e:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0dfa2:  add r0, sp, #0x18                 
  0dfa4:  ldm r0, {r0, r1, r2, r3}          
  0dfa6:  bl #0xded4                        -> func_0x0ded4
  0dfaa:  cmp r0, #1                        
  0dfac:  bne #0xdfbc                       
  0dfae:  movs r0, #2                       
  0dfb0:  ldr r1, [pc, #0xb0]               -> RAM
  0dfb2:  strb r0, [r1]                     
  0dfb4:  movs r6, #1                       
  0dfb6:  movs r0, #0                       
  0dfb8:  ldr r1, [pc, #0xac]               -> RAM
  0dfba:  strb r0, [r1]                     
  0dfbc:  b #0xe052                         -> 0x0e052 (вне списка функций)
  0dfbe:  movs r2, #0x11                    
  0dfc0:  add r1, sp, #0x28                 
  0dfc2:  mov r0, sp                        
  0dfc4:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0dfc8:  add r0, sp, #0x18                 
  0dfca:  ldm r0, {r0, r1, r2, r3}          
  0dfcc:  bl #0xe06c                        -> 0x0e06c (вне списка функций)
  0dfd0:  cmp r0, #1                        
  0dfd2:  bne #0xdfe2                       
  0dfd4:  movs r0, #3                       
  0dfd6:  ldr r1, [pc, #0x8c]               -> RAM
  0dfd8:  strb r0, [r1]                     
  0dfda:  movs r6, #1                       
  0dfdc:  movs r0, #0                       
  0dfde:  ldr r1, [pc, #0x88]               -> RAM
  0dfe0:  strb r0, [r1]                     
  0dfe2:  b #0xe052                         -> 0x0e052 (вне списка функций)
  0dfe4:  movs r2, #0x11                    
  0dfe6:  add r1, sp, #0x28                 
  0dfe8:  mov r0, sp                        
  0dfea:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0dfee:  add r0, sp, #0x18                 
  0dff0:  ldm r0, {r0, r1, r2, r3}          
  0dff2:  bl #0xde08                        -> 0x0de08 (вне списка функций)
  0dff6:  cbz r0, #0xe006                   
  0dff8:  movs r0, #4                       
  0dffa:  ldr r1, [pc, #0x68]               -> RAM
  0dffc:  strb r0, [r1]                     
  0dffe:  movs r6, #1                       
  0e000:  movs r0, #0                       
  0e002:  ldr r1, [pc, #0x64]               -> RAM
  0e004:  strb r0, [r1]                     
  0e006:  b #0xe052                         -> 0x0e052 (вне списка функций)
  0e008:  movs r2, #0x11                    
  0e00a:  add r1, sp, #0x28                 
  0e00c:  mov r0, sp                        
  0e00e:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0e012:  add r0, sp, #0x18                 
  0e014:  ldm r0, {r0, r1, r2, r3}          
  0e016:  bl #0xe0b4                        -> 0x0e0b4 (вне списка функций)
  0e01a:  cbz r0, #0xe02a                   
  0e01c:  movs r0, #5                       
  0e01e:  ldr r1, [pc, #0x44]               -> RAM
  0e020:  strb r0, [r1]                     
  0e022:  movs r6, #1                       
  0e024:  movs r0, #0                       
  0e026:  ldr r1, [pc, #0x40]               -> RAM
  0e028:  strb r0, [r1]                     
  0e02a:  b #0xe052                         -> 0x0e052 (вне списка функций)
  0e02c:  movs r2, #0x11                    
  0e02e:  add r1, sp, #0x28                 
  0e030:  mov r0, sp                        
  0e032:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0e036:  add r0, sp, #0x18                 
  0e038:  ldm r0, {r0, r1, r2, r3}          
  0e03a:  bl #0xdea4                        -> 0x0dea4 (вне списка функций)
  0e03e:  cbz r0, #0xe04e                   
  0e040:  movs r0, #5                       
  0e042:  ldr r1, [pc, #0x20]               -> RAM
  0e044:  strb r0, [r1]                     
  0e046:  movs r6, #1                       
  0e048:  movs r0, #0                       
  0e04a:  ldr r1, [pc, #0x1c]               -> RAM
  0e04c:  strb r0, [r1]                     
  0e04e:  b #0xe052                         -> 0x0e052 (вне списка функций)
  0e050:  nop                               
  0e052:  nop                               
  0e054:  cmp r6, #1                        
  0e056:  bne #0xe05e                       
  0e058:  movs r0, #0                       
  0e05a:  ldr r1, [pc, #0xc]                -> RAM
  0e05c:  strb r0, [r1]                     
  0e05e:  nop                               
  0e060:  b #0xdf40                         -> 0x0df40 (вне списка функций)
  ; --- literal-пул @0x0e064 (2 слов) — ВНЕ границ функции ---
  0e064:  .word 0x200009b4  ; RAM
  0e068:  .word 0x200009bc  ; RAM
  ; --- literal-пул @0x0e084 (1 слов) — ВНЕ границ функции ---
  0e084:  .word 0x4302eb03  ; периферия
```
