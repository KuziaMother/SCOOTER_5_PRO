# func_0x15d14

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015d14) | `0x00015d14` |
| размер кода | 216 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001f10 — RAM (r2)
- 0x20001fac — RAM (r3)

## Вызовы (callees)

- 0x15d28 (b, вне списка функций)
- 0x15dc6 (b, вне списка функций)
- 0x15dca (b, вне списка функций)
- 0x15de8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x15b84` (bl @0x00015c38)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x15d2a..0x15db0` (134 Б); цели из: 0x15d20
- `0x15db0..0x15dc6` (22 Б); цели из: 0x15da4
- `0x15dc6..0x15dca` (4 Б); цели из: 0x15d9a
- `0x15dca..0x15de2` (24 Б); цели из: 0x15dae
- `0x15de2..0x15de8` (6 Б); цели из: 0x15dd8
- `0x15de8..0x15dec` (4 Б); цели из: 0x15de0

## Дизассембляция

```asm
  15d14:  push {r4, lr}                     
  15d16:  movs r0, #0xc                     
  15d18:  movs r1, #0                       
  15d1a:  ldr r2, [pc, #0xd0]               -> RAM
  15d1c:  ldrb r2, [r2, #1]                 
  15d1e:  cmp r2, #1                        
  15d20:  beq #0x15d2a                      
  15d22:  movs r2, #2                       
  15d24:  ldr r3, [pc, #0xc8]               -> RAM
  15d26:  strb r2, [r3, #3]                 
  15d28:  pop {r4, pc}                      
  15d2a:  ldr r2, [pc, #0xc0]               -> RAM
  15d2c:  adds r2, r2, #3                   
  15d2e:  ldrb r2, [r2, r0]                 
  15d30:  mov.w r3, #-0x1000000             
  15d34:  and.w r2, r3, r2, lsl #24         
  15d38:  ldr r3, [pc, #0xb0]               -> RAM
  15d3a:  adds r3, r3, #3                   
  15d3c:  adds r4, r0, #1                   
  15d3e:  ldrb r3, [r3, r4]                 
  15d40:  mov.w r4, #0xff0000               
  15d44:  and.w r3, r4, r3, lsl #16         
  15d48:  orrs r2, r3                       
  15d4a:  ldr r3, [pc, #0xa0]               -> RAM
  15d4c:  adds r3, r3, #3                   
  15d4e:  adds r4, r0, #2                   
  15d50:  ldrb r3, [r3, r4]                 
  15d52:  mov.w r4, #0xff00                 
  15d56:  and.w r3, r4, r3, lsl #8          
  15d5a:  orrs r2, r3                       
  15d5c:  ldr r3, [pc, #0x8c]               -> RAM
  15d5e:  adds r3, r3, #3                   
  15d60:  adds r4, r0, #3                   
  15d62:  ldrb r3, [r3, r4]                 
  15d64:  orrs r2, r3                       
  15d66:  ldr r3, [pc, #0x88]               -> RAM
  15d68:  str r2, [r3, #0x10]               
  15d6a:  mov r2, r3                        
  15d6c:  ldr r2, [r2, #0x10]               
  15d6e:  ubfx r2, r2, #0xb, #0x10          
  15d72:  strh r2, [r3, #0xa]               
  15d74:  adds r2, r0, #4                   
  15d76:  uxth r0, r2                       
  15d78:  ldr r2, [pc, #0x70]               -> RAM
  15d7a:  adds r2, r2, #3                   
  15d7c:  ldrb r2, [r2, r0]                 
  15d7e:  mov.w r3, #0xff00                 
  15d82:  and.w r3, r3, r2, lsl #8          
  15d86:  ldr r2, [pc, #0x64]               -> RAM
  15d88:  adds r2, r2, #3                   
  15d8a:  adds r4, r0, #1                   
  15d8c:  ldrb r2, [r2, r4]                 
  15d8e:  orrs r3, r2                       
  15d90:  ldr r2, [pc, #0x5c]               -> RAM
  15d92:  strh r3, [r2, #0x14]              
  15d94:  adds r2, r0, #2                   
  15d96:  uxth r0, r2                       
  15d98:  movs r1, #0                       
  15d9a:  b #0x15dc6                        -> 0x15dc6 (вне списка функций)
  15d9c:  ldr r2, [pc, #0x4c]               -> RAM
  15d9e:  adds r2, r2, #3                   
  15da0:  ldrb r2, [r2, r0]                 
  15da2:  cmp r2, #0xff                     
  15da4:  bne #0x15db0                      
  15da6:  movs r3, #0                       
  15da8:  ldr r2, [pc, #0x44]               -> RAM
  15daa:  adds r2, #0x1e                    
  15dac:  strb r3, [r2, r1]                 
  15dae:  b #0x15dca                        -> 0x15dca (вне списка функций)
  15db0:  mov r2, r0                        
  15db2:  adds r3, r0, #1                   
  15db4:  uxth r0, r3                       
  15db6:  ldr r3, [pc, #0x34]               -> RAM
  15db8:  adds r3, r3, #3                   
  15dba:  ldrb r3, [r3, r2]                 
  15dbc:  ldr r2, [pc, #0x30]               -> RAM
  15dbe:  adds r2, #0x1e                    
  15dc0:  strb r3, [r2, r1]                 
  15dc2:  adds r2, r1, #1                   
  15dc4:  uxtb r1, r2                       
  15dc6:  cmp r1, #0xa                      
  15dc8:  blt #0x15d9c                      
  15dca:  nop                               
  15dcc:  ldr r2, [pc, #0x20]               -> RAM
  15dce:  ldrh r2, [r2, #0xa]               
  15dd0:  cbnz r2, #0x15de2                 
  15dd2:  ldr r2, [pc, #0x1c]               -> RAM
  15dd4:  ldrh r2, [r2, #0xa]               
  15dd6:  cmp r2, #0x66                     
  15dd8:  ble #0x15de2                      
  15dda:  movs r2, #6                       
  15ddc:  ldr r3, [pc, #0x10]               -> RAM
  15dde:  strb r2, [r3, #3]                 
  15de0:  b #0x15de8                        -> 0x15de8 (вне списка функций)
  15de2:  movs r2, #2                       
  15de4:  ldr r3, [pc, #8]                  -> RAM
  15de6:  strb r2, [r3, #3]                 
  15de8:  nop                               
  15dea:  b #0x15d28                        -> 0x15d28 (вне списка функций)
  ; --- literal-пул @0x15dec (2 слов) — ВНЕ границ функции ---
  15dec:  .word 0x20001f10  ; RAM
  15df0:  .word 0x20001fac  ; RAM
```
