# func_0x02d70

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002d70) | `0x00002d70` |
| размер кода | 130 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000186a0 — данные @0x186a0 (r0)
- 0x0801a780 — flash-mirror @0x1a780 (r0)
- 0x0801a794 — flash-mirror @0x1a794 (r0)
- 0x20000b64 — RAM (r0)
- 0x20000b72 — RAM (r0)
- 0x40005800 — периферия (r0)

## Вызовы (callees)

- `func_0x02e0c` (0x00002e0c, bl)
- `func_0x0332c` (0x0000332c, bl)
- `func_0x097f4` (0x000097f4, bl)
- `func_0x09874` (0x00009874, bl)

## Кто вызывает (callers / xrefs)

- `func_0x173cc` (bl @0x000174ec)


## Дизассембляция

```asm
  02d70:  push {lr}                         
  02d72:  sub sp, #0x14                     
  02d74:  movs r0, #0                       
  02d76:  strh.w r0, [sp, #8]               
  02d7a:  movw r0, #0xbfff                  
  02d7e:  strh.w r0, [sp, #0xa]             
  02d82:  movs r0, #0x30                    
  02d84:  strh.w r0, [sp, #0xc]             
  02d88:  mov.w r0, #0x400                  
  02d8c:  strh.w r0, [sp, #0xe]             
  02d90:  lsls r0, r0, #4                   
  02d92:  strh.w r0, [sp, #0x10]            
  02d96:  ldr r0, [pc, #0x5c]               -> данные @0x186a0
  02d98:  str r0, [sp, #4]                  
  02d9a:  ldr r0, [pc, #0x5c]               -> периферия
  02d9c:  bl #0x97f4                        -> func_0x097f4
  02da0:  movs r1, #1                       
  02da2:  ldr r0, [pc, #0x58]               -> flash-mirror @0x1a780
  02da4:  bl #0x332c                        -> func_0x0332c
  02da8:  movs r1, #1                       
  02daa:  ldr r0, [pc, #0x54]               -> flash-mirror @0x1a794
  02dac:  bl #0x332c                        -> func_0x0332c
  02db0:  mov.w r0, #0x3e8                  
  02db4:  str r0, [sp]                      
  02db6:  nop                               
  02db8:  ldr r0, [sp]                      
  02dba:  subs r1, r0, #1                   
  02dbc:  str r1, [sp]                      
  02dbe:  cmp r0, #0                        
  02dc0:  bne #0x2db8                       
  02dc2:  add r1, sp, #4                    
  02dc4:  ldr r0, [pc, #0x30]               -> периферия
  02dc6:  bl #0x2e0c                        -> func_0x02e0c
  02dca:  ldr r0, [pc, #0x38]               -> RAM
  02dcc:  ldrb r0, [r0]                     
  02dce:  bic r0, r0, #0xf0                 
  02dd2:  adds r0, #0x10                    
  02dd4:  ldr r1, [pc, #0x2c]               -> RAM
  02dd6:  strb r0, [r1]                     
  02dd8:  mov.w r1, #0x20000                
  02ddc:  ldr r0, [pc, #0x18]               -> периферия
  02dde:  bl #0x9874                        -> func_0x09874
  02de2:  cbz r0, #0x2dee                   
  02de4:  ldr r0, [pc, #0x20]               -> RAM
  02de6:  ldrb r0, [r0]                     
  02de8:  adds r0, r0, #1                   
  02dea:  ldr r1, [pc, #0x1c]               -> RAM
  02dec:  strb r0, [r1]                     
  02dee:  add sp, #0x14                     
  02df0:  pop {pc}                          
  ; --- literal-пул @0x02df4 (6 слов) — ВНЕ границ функции ---
  02df4:  .word 0x000186a0  ; данные @0x186a0
  02df8:  .word 0x40005800  ; периферия
  02dfc:  .word 0x0801a780  ; flash-mirror @0x1a780
  02e00:  .word 0x0801a794  ; flash-mirror @0x1a794
  02e04:  .word 0x20000b64  ; RAM
  02e08:  .word 0x20000b72  ; RAM
```
