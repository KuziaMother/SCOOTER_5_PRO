# func_0x12d04

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012d04) | `0x00012d04` |
| размер кода | 134 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000190d — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04b04` (bl @0x00004b0e)


## Дизассембляция

```asm
  12d04:  push {r4, r5, r6, lr}             
  12d06:  mov r5, r0                        
  12d08:  movs r4, #0                       
  12d0a:  movs r6, #0                       
  12d0c:  ldr r0, [pc, #0x7c]               -> RAM
  12d0e:  ldrb r0, [r0]                     
  12d10:  and r0, r0, #7                    
  12d14:  cbz r0, #0x12d86                  
  12d16:  ldr r0, [pc, #0x74]               -> RAM
  12d18:  ldrb r4, [r0, #1]                 
  12d1a:  nop                               
  12d1c:  adds r0, r4, #1                   
  12d1e:  uxtb r4, r0                       
  12d20:  cmp r4, #3                        
  12d22:  blt #0x12d26                      
  12d24:  movs r4, #0                       
  12d26:  ldr r0, [pc, #0x64]               -> RAM
  12d28:  ldrb r1, [r0]                     
  12d2a:  movs r0, #1                       
  12d2c:  lsls r0, r4                       
  12d2e:  ands r1, r0                       
  12d30:  cmp r1, #0                        
  12d32:  beq #0x12d1c                      
  12d34:  ldr r0, [pc, #0x54]               -> RAM
  12d36:  strb r4, [r0, #1]                 
  12d38:  add.w r0, r4, r4, lsl #1          
  12d3c:  add.w r1, r0, r4, lsl #4          
  12d40:  ldr r0, [pc, #0x48]               -> RAM
  12d42:  adds r0, r0, #2                   
  12d44:  add.w r0, r0, r1, lsl #3          
  12d48:  ldrh r0, [r0]                     
  12d4a:  strh r0, [r5]                     
  12d4c:  add.w r0, r4, r4, lsl #1          
  12d50:  add.w r3, r0, r4, lsl #4          
  12d54:  ldr r0, [pc, #0x34]               -> RAM
  12d56:  adds r0, r0, #2                   
  12d58:  add.w r0, r0, r3, lsl #3          
  12d5c:  ldrh r2, [r0]                     
  12d5e:  add.w r0, r4, r4, lsl #1          
  12d62:  add.w r3, r0, r4, lsl #4          
  12d66:  ldr r0, [pc, #0x24]               -> RAM
  12d68:  adds r0, r0, #2                   
  12d6a:  add.w r0, r0, r3, lsl #3          
  12d6e:  adds r1, r0, #2                   
  12d70:  adds r0, r5, #2                   
  12d72:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  12d76:  ldr r0, [pc, #0x14]               -> RAM
  12d78:  ldrb r0, [r0]                     
  12d7a:  movs r1, #1                       
  12d7c:  lsls r1, r4                       
  12d7e:  bics r0, r1                       
  12d80:  ldr r1, [pc, #8]                  -> RAM
  12d82:  strb r0, [r1]                     
  12d84:  movs r6, #1                       
  12d86:  mov r0, r6                        
  12d88:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x12d8c (1 слов) — ВНЕ границ функции ---
  12d8c:  .word 0x2000190d  ; RAM
```
