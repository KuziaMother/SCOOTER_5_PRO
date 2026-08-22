# func_0x0ef78

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ef78) | `0x0000ef78` |
| размер кода | 140 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801ad24 — flash-mirror @0x1ad24 (r1)
- 0x20002fec — RAM (r0)
- 0x20002ffa — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e2a)


## Дизассембляция

```asm
  0ef78:  push {r4, lr}                     
  0ef7a:  movs r0, #0                       
  0ef7c:  ldr r1, [pc, #0x84]               -> flash-mirror @0x1ad24
  0ef7e:  ldr r1, [r1]                      
  0ef80:  str r0, [r1]                      
  0ef82:  movs r1, #0xe                     
  0ef84:  ldr r0, [pc, #0x80]               -> RAM
  0ef86:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0ef8a:  movs r1, #0x15                    
  0ef8c:  ldr r0, [pc, #0x7c]               -> RAM
  0ef8e:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0ef92:  ldr r0, [pc, #0x78]               -> RAM
  0ef94:  ldrb r0, [r0, #4]                 
  0ef96:  bic r0, r0, #8                    
  0ef9a:  adds r0, #8                       
  0ef9c:  ldr r1, [pc, #0x6c]               -> RAM
  0ef9e:  strb r0, [r1, #4]                 
  0efa0:  mov r0, r1                        
  0efa2:  ldrb r0, [r0, #4]                 
  0efa4:  bic r0, r0, #0x10                 
  0efa8:  adds r0, #0x10                    
  0efaa:  strb r0, [r1, #4]                 
  0efac:  mov r0, r1                        
  0efae:  ldrb r0, [r0, #4]                 
  0efb0:  bic r0, r0, #0x20                 
  0efb4:  adds r0, #0x20                    
  0efb6:  strb r0, [r1, #4]                 
  0efb8:  mov r0, r1                        
  0efba:  ldrb r0, [r0, #4]                 
  0efbc:  bic r0, r0, #0x40                 
  0efc0:  adds r0, #0x40                    
  0efc2:  strb r0, [r1, #4]                 
  0efc4:  mov r0, r1                        
  0efc6:  ldrb r0, [r0, #4]                 
  0efc8:  bic r0, r0, #0x80                 
  0efcc:  adds r0, #0x80                    
  0efce:  strb r0, [r1, #4]                 
  0efd0:  mov r0, r1                        
  0efd2:  ldrb r0, [r0, #5]                 
  0efd4:  bic r0, r0, #1                    
  0efd8:  adds r0, r0, #1                   
  0efda:  strb r0, [r1, #5]                 
  0efdc:  mov r0, r1                        
  0efde:  ldrb r0, [r0, #5]                 
  0efe0:  bic r0, r0, #2                    
  0efe4:  adds r0, r0, #2                   
  0efe6:  strb r0, [r1, #5]                 
  0efe8:  mov r0, r1                        
  0efea:  ldrb r0, [r0, #5]                 
  0efec:  bic r1, r0, #4                    
  0eff0:  ldr r0, [pc, #0x18]               -> RAM
  0eff2:  strb r1, [r0, #5]                 
  0eff4:  ldrb r0, [r0, #4]                 
  0eff6:  bic r0, r0, #7                    
  0effa:  ldr r1, [pc, #0x10]               -> RAM
  0effc:  strb r0, [r1, #4]                 
  0effe:  movs r0, #0                       
  0f000:  strb r0, [r1, #0x14]              
  0f002:  pop {r4, pc}                      
  ; --- literal-пул @0x0f004 (3 слов) — ВНЕ границ функции ---
  0f004:  .word 0x0801ad24  ; flash-mirror @0x1ad24
  0f008:  .word 0x20002fec  ; RAM
  0f00c:  .word 0x20002ffa  ; RAM
```
