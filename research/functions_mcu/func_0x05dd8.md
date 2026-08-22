# func_0x05dd8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005dd8) | `0x00005dd8` |
| размер кода | 262 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x05a68` (0x00005a68, bl)
- 0x05e08 (b, вне списка функций)
- 0x05e10 (b, вне списка функций)
- 0x05e2e (b, вне списка функций)
- 0x05e36 (b, вне списка функций)
- 0x05e54 (b, вне списка функций)
- 0x05e5c (b, вне списка функций)
- 0x05e5e (b, вне списка функций)
- 0x05e9c (b, вне списка функций)
- 0x05eca (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03700` (bl @0x0000372e)
- `func_0x053fc` (bl @0x00005438)
- `func_0x0bcc0` (bl @0x0000bd3c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x05e06..0x05e08` (2 Б); цели из: 0x05df8
- `0x05e08..0x05e0e` (6 Б); цели из: 0x05dfe
- `0x05e0e..0x05e10` (2 Б); цели из: 0x05dfc
- `0x05e10..0x05e12` (2 Б); цели из: 0x05e04, 0x05e06, 0x05e0c
- `0x05e12..0x05e28` (22 Б); цели из: 0x05dee
- `0x05e28..0x05e2e` (6 Б); цели из: 0x05e1e
- `0x05e2e..0x05e34` (6 Б); цели из: 0x05e24
- `0x05e34..0x05e36` (2 Б); цели из: 0x05e22
- `0x05e36..0x05e38` (2 Б); цели из: 0x05e26, 0x05e2c, 0x05e32
- `0x05e38..0x05e4e` (22 Б); цели из: 0x05e14
- `0x05e4e..0x05e54` (6 Б); цели из: 0x05e44
- `0x05e54..0x05e5a` (6 Б); цели из: 0x05e4a
- `0x05e5a..0x05e5c` (2 Б); цели из: 0x05e48
- `0x05e5c..0x05e5e` (2 Б); цели из: 0x05e4c, 0x05e52, 0x05e58
- `0x05e5e..0x05e90` (50 Б); цели из: 0x05e10, 0x05e36, 0x05e3a
- `0x05e90..0x05e9c` (12 Б); цели из: 0x05e7e
- `0x05e9c..0x05ebe` (34 Б); цели из: 0x05e62, 0x05e78, 0x05e8e
- `0x05ebe..0x05eca` (12 Б); цели из: 0x05eac
- `0x05eca..0x05eda` (16 Б); цели из: 0x05ea6, 0x05ebc
- `0x05eda..0x05ede` (4 Б); цели из: 0x05ea0

## Дизассембляция

```asm
  05dd8:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  05ddc:  mov r8, r0                        
  05dde:  mov r6, r1                        
  05de0:  mov r5, r2                        
  05de2:  mov r7, r3                        
  05de4:  ldr r4, [sp, #0x20]               
  05de6:  mov.w sb, #0                      
  05dea:  mov sl, sb                        
  05dec:  cmp r6, #3                        
  05dee:  bne #0x5e12                       
  05df0:  ldr r0, [r4]                      
  05df2:  ldrb r0, [r0]                     
  05df4:  cbz r0, #0x5e00                   
  05df6:  cmp r0, #1                        
  05df8:  beq #0x5e06                       
  05dfa:  cmp r0, #2                        
  05dfc:  bne #0x5e0e                       
  05dfe:  b #0x5e08                         -> 0x05e08 (вне списка функций)
  05e00:  mov.w sb, #1                      
  05e04:  b #0x5e10                         -> 0x05e10 (вне списка функций)
  05e06:  b #0x5e10                         -> 0x05e10 (вне списка функций)
  05e08:  mov.w sb, #1                      
  05e0c:  b #0x5e10                         -> 0x05e10 (вне списка функций)
  05e0e:  nop                               
  05e10:  b #0x5e5e                         -> 0x05e5e (вне списка функций)
  05e12:  cmp r6, #6                        
  05e14:  bne #0x5e38                       
  05e16:  ldr r0, [r4]                      
  05e18:  ldrb r0, [r0]                     
  05e1a:  cbz r0, #0x5e26                   
  05e1c:  cmp r0, #1                        
  05e1e:  beq #0x5e28                       
  05e20:  cmp r0, #2                        
  05e22:  bne #0x5e34                       
  05e24:  b #0x5e2e                         -> 0x05e2e (вне списка функций)
  05e26:  b #0x5e36                         -> 0x05e36 (вне списка функций)
  05e28:  mov.w sl, #1                      
  05e2c:  b #0x5e36                         -> 0x05e36 (вне списка функций)
  05e2e:  mov.w sl, #1                      
  05e32:  b #0x5e36                         -> 0x05e36 (вне списка функций)
  05e34:  nop                               
  05e36:  b #0x5e5e                         -> 0x05e5e (вне списка функций)
  05e38:  cmp r6, #0x10                     
  05e3a:  bne #0x5e5e                       
  05e3c:  ldr r0, [r4]                      
  05e3e:  ldrb r0, [r0]                     
  05e40:  cbz r0, #0x5e4c                   
  05e42:  cmp r0, #1                        
  05e44:  beq #0x5e4e                       
  05e46:  cmp r0, #2                        
  05e48:  bne #0x5e5a                       
  05e4a:  b #0x5e54                         -> 0x05e54 (вне списка функций)
  05e4c:  b #0x5e5c                         -> 0x05e5c (вне списка функций)
  05e4e:  mov.w sl, #1                      
  05e52:  b #0x5e5c                         -> 0x05e5c (вне списка функций)
  05e54:  mov.w sl, #1                      
  05e58:  b #0x5e5c                         -> 0x05e5c (вне списка функций)
  05e5a:  nop                               
  05e5c:  nop                               
  05e5e:  cmp.w sb, #1                      
  05e62:  bne #0x5e9c                       
  05e64:  ldr r0, [r4]                      
  05e66:  ldr r0, [r0, #0x10]               
  05e68:  cbz r0, #0x5e70                   
  05e6a:  ldr r1, [r4]                      
  05e6c:  ldr r0, [r1, #0x10]               
  05e6e:  blx r0                            
  05e70:  movs r0, #0                       
  05e72:  strb r0, [r7]                     
  05e74:  ldrb r0, [r5]                     
  05e76:  cmp r0, #0                        
  05e78:  ble #0x5e9c                       
  05e7a:  cmp.w r8, #1                      
  05e7e:  bne #0x5e90                       
  05e80:  ldrb r3, [r5]                     
  05e82:  ldr r0, [r4]                      
  05e84:  ldrb r2, [r0, #1]                 
  05e86:  ldr r1, [r0, #4]                  
  05e88:  mov r0, r7                        
  05e8a:  bl #0x5a68                        -> func_0x05a68
  05e8e:  b #0x5e9c                         -> 0x05e9c (вне списка функций)
  05e90:  ldrb r2, [r5]                     
  05e92:  ldr r0, [r4]                      
  05e94:  ldr r1, [r0, #4]                  
  05e96:  mov r0, r7                        
  05e98:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  05e9c:  cmp.w sl, #1                      
  05ea0:  bne #0x5eda                       
  05ea2:  ldrb r0, [r5]                     
  05ea4:  cmp r0, #0                        
  05ea6:  ble #0x5eca                       
  05ea8:  cmp.w r8, #1                      
  05eac:  bne #0x5ebe                       
  05eae:  ldrb r3, [r5]                     
  05eb0:  ldr r1, [r4]                      
  05eb2:  ldrb r2, [r1, #1]                 
  05eb4:  ldr r0, [r1, #4]                  
  05eb6:  mov r1, r7                        
  05eb8:  bl #0x5a68                        -> func_0x05a68
  05ebc:  b #0x5eca                         -> 0x05eca (вне списка функций)
  05ebe:  ldrb r2, [r5]                     
  05ec0:  ldr r1, [r4]                      
  05ec2:  ldr r0, [r1, #4]                  
  05ec4:  mov r1, r7                        
  05ec6:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  05eca:  ldr r0, [r4]                      
  05ecc:  ldr r0, [r0, #0xc]                
  05ece:  cbz r0, #0x5ed6                   
  05ed0:  ldr r1, [r4]                      
  05ed2:  ldr r0, [r1, #0xc]                
  05ed4:  blx r0                            
  05ed6:  movs r0, #0                       
  05ed8:  strb r0, [r5]                     
  05eda:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
```
