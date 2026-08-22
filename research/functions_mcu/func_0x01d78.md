# func_0x01d78

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001d78) | `0x00001d78` |
| размер кода | 112 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a7c — RAM (r1)

## Вызовы (callees)

- `func_0x01c7a` (0x00001c7a, bl)
- 0x01de0 (b, вне списка функций)
- 0x01de4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0c138` (bl @0x0000c13a)


## Дизассембляция

```asm
  01d78:  push {r3, r4, r5, lr}             
  01d7a:  movs r0, #0                       
  01d7c:  str r0, [sp]                      
  01d7e:  movs r4, #0                       
  01d80:  movs r5, #0                       
  01d82:  movs r3, #2                       
  01d84:  mov r2, sp                        
  01d86:  movs r1, #5                       
  01d88:  movs r0, #8                       
  01d8a:  bl #0x1c7a                        -> func_0x01c7a
  01d8e:  mov r4, r0                        
  01d90:  cbz r4, #0x1da8                   
  01d92:  ldrb.w r0, [sp, #1]               
  01d96:  lsls r0, r0, #8                   
  01d98:  ldr r1, [pc, #0x4c]               -> RAM
  01d9a:  strh r0, [r1]                     
  01d9c:  ldrb.w r0, [sp]                   
  01da0:  ldrh r1, [r1]                     
  01da2:  orrs r0, r1                       
  01da4:  ldr r1, [pc, #0x40]               -> RAM
  01da6:  strh r0, [r1]                     
  01da8:  cbnz r4, #0x1de6                  
  01daa:  movs r5, #0                       
  01dac:  b #0x1de0                         -> 0x01de0 (вне списка функций)
  01dae:  movs r3, #2                       
  01db0:  mov r2, sp                        
  01db2:  movs r1, #5                       
  01db4:  movs r0, #8                       
  01db6:  bl #0x1c7a                        -> func_0x01c7a
  01dba:  mov r4, r0                        
  01dbc:  cbz r4, #0x1dd6                   
  01dbe:  ldrb.w r0, [sp, #1]               
  01dc2:  lsls r0, r0, #8                   
  01dc4:  ldr r1, [pc, #0x20]               -> RAM
  01dc6:  strh r0, [r1]                     
  01dc8:  ldrb.w r0, [sp]                   
  01dcc:  ldrh r1, [r1]                     
  01dce:  orrs r0, r1                       
  01dd0:  ldr r1, [pc, #0x14]               -> RAM
  01dd2:  strh r0, [r1]                     
  01dd4:  b #0x1de4                         -> 0x01de4 (вне списка функций)
  01dd6:  movs r0, #0                       
  01dd8:  ldr r1, [pc, #0xc]                -> RAM
  01dda:  strh r0, [r1]                     
  01ddc:  adds r0, r5, #1                   
  01dde:  uxtb r5, r0                       
  01de0:  cmp r5, #3                        
  01de2:  blt #0x1dae                       
  01de4:  nop                               
  01de6:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x01de8 (1 слов) — ВНЕ границ функции ---
  01de8:  .word 0x20000a7c  ; RAM
```
