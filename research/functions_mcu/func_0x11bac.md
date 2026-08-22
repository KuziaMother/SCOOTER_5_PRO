# func_0x11bac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080011bac) | `0x00011bac` |
| размер кода | 130 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00015180 — данные @0x15180 (r3)
- 0x00278d00 — прочее (r3)
- 0x01da9c00 — прочее (r2)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x06080` (bl @0x00006184)


## Дизассембляция

```asm
  11bac:  push {r2, r3, lr}                 
  11bae:  ldr r2, [pc, #0x80]               
  11bb0:  udiv r2, r1, r2                   
  11bb4:  uxtb r2, r2                       
  11bb6:  strb.w r2, [sp]                   
  11bba:  ldr r2, [pc, #0x74]               
  11bbc:  udiv r3, r1, r2                   
  11bc0:  mls r2, r2, r3, r1                
  11bc4:  ldr r3, [pc, #0x6c]               
  11bc6:  udiv r2, r2, r3                   
  11bca:  uxtb r2, r2                       
  11bcc:  strb.w r2, [sp, #1]               
  11bd0:  mov r2, r3                        
  11bd2:  udiv r3, r1, r2                   
  11bd6:  mls r2, r2, r3, r1                
  11bda:  ldr r3, [pc, #0x5c]               -> данные @0x15180
  11bdc:  udiv r2, r2, r3                   
  11be0:  uxtb r2, r2                       
  11be2:  strb.w r2, [sp, #2]               
  11be6:  mov r2, r3                        
  11be8:  udiv r3, r1, r2                   
  11bec:  mls r2, r2, r3, r1                
  11bf0:  mov.w r3, #0xe10                  
  11bf4:  udiv r2, r2, r3                   
  11bf8:  uxtb r2, r2                       
  11bfa:  strb.w r2, [sp, #3]               
  11bfe:  mov r2, r3                        
  11c00:  udiv r3, r1, r2                   
  11c04:  mls r2, r2, r3, r1                
  11c08:  movs r3, #0x3c                    
  11c0a:  udiv r2, r2, r3                   
  11c0e:  uxtb r2, r2                       
  11c10:  strb.w r2, [sp, #4]               
  11c14:  movs r2, #0x3c                    
  11c16:  udiv r3, r1, r2                   
  11c1a:  mls r2, r2, r3, r1                
  11c1e:  strb.w r2, [sp, #5]               
  11c22:  ldr r2, [sp]                      
  11c24:  str r2, [r0]                      
  11c26:  ldrh.w r2, [sp, #4]               
  11c2a:  strh r2, [r0, #4]                 
  11c2c:  pop {r2, r3, pc}                  
  ; --- literal-пул @0x11c30 (3 слов) — ВНЕ границ функции ---
  11c30:  .word 0x01da9c00
  11c34:  .word 0x00278d00
  11c38:  .word 0x00015180  ; данные @0x15180
```
