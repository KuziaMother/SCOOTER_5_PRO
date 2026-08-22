# func_0x12f44

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012f44) | `0x00012f44` |
| размер кода | 134 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001d38 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04a30` (bl @0x00004a3a)


## Дизассембляция

```asm
  12f44:  push {r4, r5, r6, lr}             
  12f46:  mov r5, r0                        
  12f48:  movs r4, #0                       
  12f4a:  movs r6, #0                       
  12f4c:  ldr r0, [pc, #0x7c]               -> RAM
  12f4e:  ldrb r0, [r0]                     
  12f50:  and r0, r0, #7                    
  12f54:  cbz r0, #0x12fc6                  
  12f56:  ldr r0, [pc, #0x74]               -> RAM
  12f58:  ldrb r4, [r0, #1]                 
  12f5a:  nop                               
  12f5c:  adds r0, r4, #1                   
  12f5e:  uxtb r4, r0                       
  12f60:  cmp r4, #3                        
  12f62:  blt #0x12f66                      
  12f64:  movs r4, #0                       
  12f66:  ldr r0, [pc, #0x64]               -> RAM
  12f68:  ldrb r1, [r0]                     
  12f6a:  movs r0, #1                       
  12f6c:  lsls r0, r4                       
  12f6e:  ands r1, r0                       
  12f70:  cmp r1, #0                        
  12f72:  beq #0x12f5c                      
  12f74:  ldr r0, [pc, #0x54]               -> RAM
  12f76:  strb r4, [r0, #1]                 
  12f78:  add.w r0, r4, r4, lsl #1          
  12f7c:  add.w r1, r0, r4, lsl #4          
  12f80:  ldr r0, [pc, #0x48]               -> RAM
  12f82:  adds r0, r0, #2                   
  12f84:  add.w r0, r0, r1, lsl #3          
  12f88:  ldrh r0, [r0]                     
  12f8a:  strh r0, [r5]                     
  12f8c:  add.w r0, r4, r4, lsl #1          
  12f90:  add.w r3, r0, r4, lsl #4          
  12f94:  ldr r0, [pc, #0x34]               -> RAM
  12f96:  adds r0, r0, #2                   
  12f98:  add.w r0, r0, r3, lsl #3          
  12f9c:  ldrh r2, [r0]                     
  12f9e:  add.w r0, r4, r4, lsl #1          
  12fa2:  add.w r3, r0, r4, lsl #4          
  12fa6:  ldr r0, [pc, #0x24]               -> RAM
  12fa8:  adds r0, r0, #2                   
  12faa:  add.w r0, r0, r3, lsl #3          
  12fae:  adds r1, r0, #2                   
  12fb0:  adds r0, r5, #2                   
  12fb2:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  12fb6:  ldr r0, [pc, #0x14]               -> RAM
  12fb8:  ldrb r0, [r0]                     
  12fba:  movs r1, #1                       
  12fbc:  lsls r1, r4                       
  12fbe:  bics r0, r1                       
  12fc0:  ldr r1, [pc, #8]                  -> RAM
  12fc2:  strb r0, [r1]                     
  12fc4:  movs r6, #1                       
  12fc6:  mov r0, r6                        
  12fc8:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x12fcc (1 слов) — ВНЕ границ функции ---
  12fcc:  .word 0x20001d38  ; RAM
```
