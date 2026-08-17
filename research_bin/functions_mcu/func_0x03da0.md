# func_0x03da0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003da0) | `0x00003da0` |
| размер кода | 58 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200000a6 — RAM (r1)
- 0x20000c9c — RAM (r0)

## Вызовы (callees)

- `func_0x08a50` (0x00008a50, bl)
- `func_0x15790` (0x00015790, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03780` (bl @0x000037c0)


## Дизассембляция

```asm
  03da0:  push {r3, r4, r5, lr}             
  03da2:  movs r4, #0                       
  03da4:  bl #0x15790                       -> func_0x15790
  03da8:  cbnz r0, #0x3dc0                  
  03daa:  mov.w r0, #0x3e8                  
  03dae:  str r0, [sp]                      
  03db0:  nop                               
  03db2:  ldr r0, [sp]                      
  03db4:  subs r1, r0, #1                   
  03db6:  str r1, [sp]                      
  03db8:  cmp r0, #0                        
  03dba:  bne #0x3db2                       
  03dbc:  bl #0x15790                       -> func_0x15790
  03dc0:  movs r1, #4                       
  03dc2:  ldr r0, [pc, #0x18]               -> RAM
  03dc4:  bl #0x8a50                        -> func_0x08a50
  03dc8:  mov r4, r0                        
  03dca:  ldr r0, [pc, #0x10]               -> RAM
  03dcc:  ldr r0, [r0, #4]                  
  03dce:  cmp r0, r4                        
  03dd0:  beq #0x3dd8                       
  03dd2:  movs r0, #0                       
  03dd4:  ldr r1, [pc, #8]                  -> RAM
  03dd6:  strb r0, [r1]                     
  03dd8:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x03ddc (2 слов) — ВНЕ границ функции ---
  03ddc:  .word 0x20000c9c  ; RAM
  03de0:  .word 0x200000a6  ; RAM
```
