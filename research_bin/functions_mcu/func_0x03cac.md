# func_0x03cac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003cac) | `0x00003cac` |
| размер кода | 232 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000084 — RAM (r0)
- 0x20001058 — RAM (r1)
- 0x20001344 — RAM (r2)

## Вызовы (callees)

- `func_0x11668` (0x00011668, bl)
- `func_0x11674` (0x00011674, bl)
- `func_0x11724` (0x00011724, bl)
- `func_0x117d4` (0x000117d4, bl)
- `func_0x11888` (0x00011888, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  03cac:  push {r4, lr}                     
  03cae:  ldr r0, [pc, #0xe4]               -> RAM
  03cb0:  ldrb r0, [r0]                     
  03cb2:  and r0, r0, #1                    
  03cb6:  cbz r0, #0x3ccc                   
  03cb8:  ldr r0, [pc, #0xd8]               -> RAM
  03cba:  ldrh r0, [r0]                     
  03cbc:  bic r0, r0, #1                    
  03cc0:  ldr r1, [pc, #0xd0]               -> RAM
  03cc2:  strh r0, [r1]                     
  03cc4:  ldr r1, [pc, #0xd0]               -> RAM
  03cc6:  ldr r0, [r1]                      
  03cc8:  bl #0x11668                       -> func_0x11668
  03ccc:  ldr r0, [pc, #0xc4]               -> RAM
  03cce:  ldrb r0, [r0]                     
  03cd0:  ubfx r0, r0, #1, #1               
  03cd4:  cbz r0, #0x3cea                   
  03cd6:  ldr r0, [pc, #0xbc]               -> RAM
  03cd8:  ldrh r0, [r0]                     
  03cda:  bic r0, r0, #2                    
  03cde:  ldr r1, [pc, #0xb4]               -> RAM
  03ce0:  strh r0, [r1]                     
  03ce2:  ldr r1, [pc, #0xb4]               -> RAM
  03ce4:  ldr r0, [r1, #4]                  
  03ce6:  bl #0x11674                       -> func_0x11674
  03cea:  ldr r0, [pc, #0xa8]               -> RAM
  03cec:  ldrb r0, [r0]                     
  03cee:  ubfx r0, r0, #2, #1               
  03cf2:  cbz r0, #0x3d0c                   
  03cf4:  ldr r0, [pc, #0x9c]               -> RAM
  03cf6:  ldrh r0, [r0]                     
  03cf8:  bic r0, r0, #4                    
  03cfc:  ldr r1, [pc, #0x94]               -> RAM
  03cfe:  strh r0, [r1]                     
  03d00:  ldr r2, [pc, #0x98]               -> RAM
  03d02:  ldr r1, [r2, #0xc]                
  03d04:  ldr r2, [pc, #0x90]               -> RAM
  03d06:  ldr r0, [r2, #8]                  
  03d08:  bl #0x11724                       -> func_0x11724
  03d0c:  ldr r0, [pc, #0x84]               -> RAM
  03d0e:  ldrb r0, [r0]                     
  03d10:  ubfx r0, r0, #3, #1               
  03d14:  cbz r0, #0x3d2e                   
  03d16:  ldr r0, [pc, #0x7c]               -> RAM
  03d18:  ldrh r0, [r0]                     
  03d1a:  bic r0, r0, #8                    
  03d1e:  ldr r1, [pc, #0x74]               -> RAM
  03d20:  strh r0, [r1]                     
  03d22:  ldr r2, [pc, #0x74]               -> RAM
  03d24:  ldr r1, [r2, #0xc]                
  03d26:  ldr r2, [pc, #0x74]               -> RAM
  03d28:  ldr r0, [r2, #8]                  
  03d2a:  bl #0x11724                       -> func_0x11724
  03d2e:  ldr r0, [pc, #0x64]               -> RAM
  03d30:  ldrb r0, [r0]                     
  03d32:  ubfx r0, r0, #4, #1               
  03d36:  cbz r0, #0x3d50                   
  03d38:  ldr r0, [pc, #0x58]               -> RAM
  03d3a:  ldrh r0, [r0]                     
  03d3c:  bic r0, r0, #0x10                 
  03d40:  ldr r1, [pc, #0x50]               -> RAM
  03d42:  strh r0, [r1]                     
  03d44:  ldr r2, [pc, #0x54]               -> RAM
  03d46:  ldrb r1, [r2, #0x12]              
  03d48:  ldr r2, [pc, #0x4c]               -> RAM
  03d4a:  ldrh r0, [r2, #0x10]              
  03d4c:  bl #0x117d4                       -> func_0x117d4
  03d50:  ldr r0, [pc, #0x40]               -> RAM
  03d52:  ldrb r0, [r0]                     
  03d54:  ubfx r0, r0, #5, #1               
  03d58:  cbz r0, #0x3d72                   
  03d5a:  ldr r0, [pc, #0x38]               -> RAM
  03d5c:  ldrh r0, [r0]                     
  03d5e:  bic r0, r0, #0x20                 
  03d62:  ldr r1, [pc, #0x30]               -> RAM
  03d64:  strh r0, [r1]                     
  03d66:  ldr r2, [pc, #0x30]               -> RAM
  03d68:  ldrb r1, [r2, #0x12]              
  03d6a:  ldr r2, [pc, #0x30]               -> RAM
  03d6c:  ldrh r0, [r2, #0x10]              
  03d6e:  bl #0x117d4                       -> func_0x117d4
  03d72:  ldr r0, [pc, #0x20]               -> RAM
  03d74:  ldrb r0, [r0]                     
  03d76:  ubfx r0, r0, #6, #1               
  03d7a:  cbz r0, #0x3d92                   
  03d7c:  ldr r0, [pc, #0x14]               -> RAM
  03d7e:  ldrh r0, [r0]                     
  03d80:  bic r0, r0, #0x40                 
  03d84:  ldr r1, [pc, #0xc]                -> RAM
  03d86:  strh r0, [r1]                     
  03d88:  ldr r1, [pc, #0xc]                -> RAM
  03d8a:  ldrh.w r0, [r1, #0x13]            
  03d8e:  bl #0x11888                       -> func_0x11888
  03d92:  pop {r4, pc}                      
  ; --- literal-пул @0x03d94 (3 слов) — ВНЕ границ функции ---
  03d94:  .word 0x20000084  ; RAM
  03d98:  .word 0x20001058  ; RAM
  03d9c:  .word 0x20001344  ; RAM
```
