# func_0x15df4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015df4) | `0x00015df4` |
| размер кода | 242 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801d800 — flash-mirror @0x1d800 (r0)
- 0x20000b8e — RAM (r0)
- 0x20000c06 — RAM (r0)
- 0x20000c7f — RAM (r1)
- 0x20001f10 — RAM (r0)
- 0x20001fac — RAM (r1)

## Вызовы (callees)

- `func_0x03b82` (0x00003b82, bl)
- `func_0x03bc4` (0x00003bc4, bl)
- `func_0x07fb8` (0x00007fb8, bl)
- `func_0x080ac` (0x000080ac, bl)
- `func_0x119e4` (0x000119e4, bl)
- 0x15ece (b, вне списка функций)
- 0x15ee2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x15b84` (bl @0x00015c44)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x15e8a..0x15e92` (8 Б); цели из: 0x15e84
- `0x15e92..0x15ee0` (78 Б); цели из: 0x15e88
- `0x15ee0..0x15ee2` (2 Б); цели из: 0x15e28
- `0x15ee2..0x15ee6` (4 Б); цели из: 0x15e50, 0x15e58, 0x15e90, 0x15ede

## Дизассембляция

```asm
  15df4:  push {r4, r5, r6, lr}             
  15df6:  sub sp, #0x18                     
  15df8:  movs r4, #0                       
  15dfa:  movs r5, #0xff                    
  15dfc:  movs r6, #0xff                    
  15dfe:  movs r0, #3                       
  15e00:  ldr r1, [pc, #0xe4]               -> RAM
  15e02:  strb r0, [r1, #3]                 
  15e04:  mov r0, r1                        
  15e06:  ldrh r0, [r0, #0xc]               
  15e08:  subs r0, r0, #2                   
  15e0a:  lsls r1, r0, #0xb                 
  15e0c:  ldr r0, [pc, #0xd8]               -> RAM
  15e0e:  ldrh r0, [r0, #6]                 
  15e10:  subs r0, r0, #1                   
  15e12:  add.w r4, r1, r0, lsl #7          
  15e16:  ldr r0, [pc, #0xd4]               -> RAM
  15e18:  ldrb.w r2, [r0, #0x99]            
  15e1c:  movs r3, #0                       
  15e1e:  adds r1, r0, #3                   
  15e20:  mov r0, r4                        
  15e22:  bl #0x119e4                       -> func_0x119e4
  15e26:  cmp r0, #1                        
  15e28:  bne #0x15ee0                      
  15e2a:  movs r0, #2                       
  15e2c:  ldr r1, [pc, #0xb8]               -> RAM
  15e2e:  strb r0, [r1, #3]                 
  15e30:  ldr r1, [pc, #0xb8]               -> RAM
  15e32:  ldrb.w r2, [r1, #0x99]            
  15e36:  ldr r1, [pc, #0xb0]               -> RAM
  15e38:  ldrh r0, [r1, #4]                 
  15e3a:  ldr r1, [pc, #0xb0]               -> RAM
  15e3c:  adds r1, r1, #3                   
  15e3e:  bl #0x3bc4                        -> func_0x03bc4
  15e42:  ldr r1, [pc, #0xa4]               -> RAM
  15e44:  strh r0, [r1, #4]                 
  15e46:  mov r0, r1                        
  15e48:  ldrh r1, [r0, #0xc]               
  15e4a:  ldrh r0, [r0, #0xa]               
  15e4c:  adds r0, r0, #1                   
  15e4e:  cmp r1, r0                        
  15e50:  bne #0x15ee2                      
  15e52:  ldr r0, [pc, #0x94]               -> RAM
  15e54:  ldrh r0, [r0, #6]                 
  15e56:  cmp r0, #0x10                     
  15e58:  bne #0x15ee2                      
  15e5a:  ldr r0, [pc, #0x8c]               -> RAM
  15e5c:  ldrh r0, [r0, #0xc]               
  15e5e:  subs r0, r0, #2                   
  15e60:  lsls r1, r0, #1                   
  15e62:  ldr r0, [pc, #0x8c]               -> RAM
  15e64:  bl #0x3b82                        -> func_0x03b82
  15e68:  mov r5, r0                        
  15e6a:  ldr r0, [pc, #0x7c]               -> RAM
  15e6c:  ldrh r0, [r0, #0xc]               
  15e6e:  subs r0, r0, #2                   
  15e70:  lsls r1, r0, #1                   
  15e72:  ldr r0, [pc, #0x80]               -> RAM
  15e74:  bl #0x3b82                        -> func_0x03b82
  15e78:  mov r6, r0                        
  15e7a:  ldr r0, [pc, #0x6c]               -> RAM
  15e7c:  ldrh r0, [r0, #4]                 
  15e7e:  ldr r1, [pc, #0x68]               -> RAM
  15e80:  ldrh r1, [r1, #0x14]              
  15e82:  cmp r0, r1                        
  15e84:  bne #0x15e8a                      
  15e86:  cmp r5, r6                        
  15e88:  beq #0x15e92                      
  15e8a:  movs r0, #1                       
  15e8c:  ldr r1, [pc, #0x58]               -> RAM
  15e8e:  strb r0, [r1, #3]                 
  15e90:  b #0x15ee2                        -> 0x15ee2 (вне списка функций)
  15e92:  movs r2, #0x14                    
  15e94:  add r1, sp, #4                    
  15e96:  ldr r0, [pc, #0x60]               -> flash-mirror @0x1d800
  15e98:  bl #0x7fb8                        -> func_0x07fb8
  15e9c:  strh.w r5, [sp, #8]               
  15ea0:  ldr r0, [pc, #0x44]               -> RAM
  15ea2:  ldr r0, [r0, #0x18]               
  15ea4:  str r0, [sp, #0x10]               
  15ea6:  movs r0, #1                       
  15ea8:  strh.w r0, [sp, #4]               
  15eac:  movs r1, #0x12                    
  15eae:  add r0, sp, #4                    
  15eb0:  bl #0x3b82                        -> func_0x03b82
  15eb4:  ldr r1, [sp, #0x14]               
  15eb6:  bfi r1, r0, #0x10, #0x10          
  15eba:  str r1, [sp, #0x14]               
  15ebc:  movs r2, #0x14                    
  15ebe:  add r1, sp, #4                    
  15ec0:  ldr r0, [pc, #0x34]               -> flash-mirror @0x1d800
  15ec2:  bl #0x80ac                        -> func_0x080ac
  15ec6:  cbnz r0, #0x15ed2                 
  15ec8:  movs r0, #1                       
  15eca:  ldr r1, [pc, #0x1c]               -> RAM
  15ecc:  strb r0, [r1, #3]                 
  15ece:  add sp, #0x18                     
  15ed0:  pop {r4, r5, r6, pc}              
  15ed2:  movs r0, #1                       
  15ed4:  ldr r1, [pc, #0x24]               -> RAM
  15ed6:  strb r0, [r1]                     
  15ed8:  movs r0, #7                       
  15eda:  ldr r1, [pc, #0xc]                -> RAM
  15edc:  strb r0, [r1, #3]                 
  15ede:  b #0x15ee2                        -> 0x15ee2 (вне списка функций)
  15ee0:  nop                               
  15ee2:  nop                               
  15ee4:  b #0x15ece                        -> 0x15ece (вне списка функций)
  ; --- literal-пул @0x15ee8 (6 слов) — ВНЕ границ функции ---
  15ee8:  .word 0x20001fac  ; RAM
  15eec:  .word 0x20001f10  ; RAM
  15ef0:  .word 0x20000b8e  ; RAM
  15ef4:  .word 0x20000c06  ; RAM
  15ef8:  .word 0x0801d800  ; flash-mirror @0x1d800
  15efc:  .word 0x20000c7f  ; RAM
```
