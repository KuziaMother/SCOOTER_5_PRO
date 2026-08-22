# func_0x01e94

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001e94) | `0x00001e94` |
| размер кода | 324 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000ad4 — RAM (r0)
- 0x200015f7 — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x029e8` (bl @0x00002a00)


## Дизассембляция

```asm
  01e94:  push {r2, r3, lr}                 
  01e96:  movs r1, #0                       
  01e98:  str r1, [sp]                      
  01e9a:  str r1, [sp, #4]                  
  01e9c:  ldr r0, [pc, #0x138]              -> RAM
  01e9e:  ldrb r0, [r0, #2]                 
  01ea0:  lsrs r0, r0, #7                   
  01ea2:  cbz r0, #0x1eb4                   
  01ea4:  movs r1, #1                       
  01ea6:  ldrb.w r0, [sp]                   
  01eaa:  bfi r0, r1, #0, #1                
  01eae:  uxtb r0, r0                       
  01eb0:  strb.w r0, [sp]                   
  01eb4:  ldr r0, [pc, #0x120]              -> RAM
  01eb6:  ldrb r0, [r0, #2]                 
  01eb8:  ubfx r0, r0, #5, #1               
  01ebc:  cbz r0, #0x1ece                   
  01ebe:  movs r1, #1                       
  01ec0:  ldrb.w r0, [sp]                   
  01ec4:  bfi r0, r1, #1, #1                
  01ec8:  uxtb r0, r0                       
  01eca:  strb.w r0, [sp]                   
  01ece:  ldr r0, [pc, #0x108]              -> RAM
  01ed0:  ldrb r0, [r0, #2]                 
  01ed2:  ubfx r0, r0, #6, #1               
  01ed6:  cbz r0, #0x1ee8                   
  01ed8:  movs r1, #1                       
  01eda:  ldrb.w r0, [sp]                   
  01ede:  bfi r0, r1, #2, #1                
  01ee2:  uxtb r0, r0                       
  01ee4:  strb.w r0, [sp]                   
  01ee8:  ldr r0, [pc, #0xec]               -> RAM
  01eea:  ldrb r0, [r0, #7]                 
  01eec:  lsrs r0, r0, #7                   
  01eee:  cbz r0, #0x1f00                   
  01ef0:  movs r1, #1                       
  01ef2:  ldrb.w r0, [sp, #1]               
  01ef6:  bfi r0, r1, #5, #1                
  01efa:  uxtb r0, r0                       
  01efc:  strb.w r0, [sp, #1]               
  01f00:  ldr r0, [pc, #0xd4]               -> RAM
  01f02:  ldrb r0, [r0, #2]                 
  01f04:  ubfx r0, r0, #4, #1               
  01f08:  cbz r0, #0x1f1a                   
  01f0a:  movs r1, #1                       
  01f0c:  ldrb.w r0, [sp]                   
  01f10:  bfi r0, r1, #3, #1                
  01f14:  uxtb r0, r0                       
  01f16:  strb.w r0, [sp]                   
  01f1a:  ldr r0, [pc, #0xbc]               -> RAM
  01f1c:  ldrb r0, [r0, #2]                 
  01f1e:  ubfx r0, r0, #3, #1               
  01f22:  cbz r0, #0x1f34                   
  01f24:  movs r1, #1                       
  01f26:  ldrb.w r0, [sp]                   
  01f2a:  bfi r0, r1, #4, #1                
  01f2e:  uxtb r0, r0                       
  01f30:  strb.w r0, [sp]                   
  01f34:  ldr r0, [pc, #0xa0]               -> RAM
  01f36:  ldrb r0, [r0, #2]                 
  01f38:  ubfx r0, r0, #2, #1               
  01f3c:  cbz r0, #0x1f4e                   
  01f3e:  movs r1, #1                       
  01f40:  ldrb.w r0, [sp]                   
  01f44:  bfi r0, r1, #5, #1                
  01f48:  uxtb r0, r0                       
  01f4a:  strb.w r0, [sp]                   
  01f4e:  ldr r0, [pc, #0x88]               -> RAM
  01f50:  ldrb r0, [r0, #4]                 
  01f52:  ubfx r0, r0, #5, #1               
  01f56:  cbz r0, #0x1f68                   
  01f58:  movs r1, #1                       
  01f5a:  ldrb.w r0, [sp, #1]               
  01f5e:  bfi r0, r1, #0, #1                
  01f62:  uxtb r0, r0                       
  01f64:  strb.w r0, [sp, #1]               
  01f68:  ldr r0, [pc, #0x6c]               -> RAM
  01f6a:  ldrb r0, [r0, #4]                 
  01f6c:  ubfx r0, r0, #1, #1               
  01f70:  cbz r0, #0x1f82                   
  01f72:  movs r1, #1                       
  01f74:  ldrb.w r0, [sp, #1]               
  01f78:  bfi r0, r1, #3, #1                
  01f7c:  uxtb r0, r0                       
  01f7e:  strb.w r0, [sp, #1]               
  01f82:  ldr r0, [pc, #0x54]               -> RAM
  01f84:  ldrb r0, [r0, #4]                 
  01f86:  ubfx r0, r0, #4, #1               
  01f8a:  cbz r0, #0x1f9c                   
  01f8c:  movs r1, #1                       
  01f8e:  ldrb.w r0, [sp, #1]               
  01f92:  bfi r0, r1, #1, #1                
  01f96:  uxtb r0, r0                       
  01f98:  strb.w r0, [sp, #1]               
  01f9c:  ldr r0, [pc, #0x38]               -> RAM
  01f9e:  ldrb r0, [r0, #4]                 
  01fa0:  and r0, r0, #1                    
  01fa4:  cbz r0, #0x1fb6                   
  01fa6:  movs r1, #1                       
  01fa8:  ldrb.w r0, [sp, #1]               
  01fac:  bfi r0, r1, #4, #1                
  01fb0:  uxtb r0, r0                       
  01fb2:  strb.w r0, [sp, #1]               
  01fb6:  ldr r0, [pc, #0x20]               -> RAM
  01fb8:  ldrb r0, [r0, #4]                 
  01fba:  lsrs r0, r0, #7                   
  01fbc:  cbz r0, #0x1fce                   
  01fbe:  movs r1, #1                       
  01fc0:  ldrb.w r0, [sp]                   
  01fc4:  bfi r0, r1, #6, #1                
  01fc8:  uxtb r0, r0                       
  01fca:  strb.w r0, [sp]                   
  01fce:  ldr r0, [pc, #0xc]                -> RAM
  01fd0:  ldrd r1, r2, [sp]                 
  01fd4:  stm r0!, {r1, r2}                 
  01fd6:  pop {r2, r3, pc}                  
  ; --- literal-пул @0x01fd8 (2 слов) — ВНЕ границ функции ---
  01fd8:  .word 0x200015f7  ; RAM
  01fdc:  .word 0x20000ad4  ; RAM
```
