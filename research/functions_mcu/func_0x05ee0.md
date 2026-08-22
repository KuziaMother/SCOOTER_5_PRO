# func_0x05ee0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005ee0) | `0x00005ee0` |
| размер кода | 146 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a7c — RAM (r1)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)
- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  05ee0:  push {r1, r2, r3, r4, r5, lr}     
  05ee2:  movs r0, #0                       
  05ee4:  str r0, [sp, #4]                  
  05ee6:  str r0, [sp, #8]                  
  05ee8:  movs r5, #0                       
  05eea:  movs r4, #1                       
  05eec:  movs r0, #0x90                    
  05eee:  bl #0x1bdc                        -> func_0x01bdc
  05ef2:  ands r4, r0                       
  05ef4:  movw r0, #0x7530                  
  05ef8:  str r0, [sp]                      
  05efa:  nop                               
  05efc:  ldr r0, [sp]                      
  05efe:  subs r1, r0, #1                   
  05f00:  str r1, [sp]                      
  05f02:  cmp r0, #0                        
  05f04:  bne #0x5efc                       
  05f06:  movs r0, #0xa1                    
  05f08:  bl #0x1bdc                        -> func_0x01bdc
  05f0c:  cbz r0, #0x5f42                   
  05f0e:  mov.w r0, #0x3e8                  
  05f12:  str r0, [sp]                      
  05f14:  nop                               
  05f16:  ldr r0, [sp]                      
  05f18:  subs r1, r0, #1                   
  05f1a:  str r1, [sp]                      
  05f1c:  cmp r0, #0                        
  05f1e:  bne #0x5f16                       
  05f20:  movs r3, #5                       
  05f22:  add r2, sp, #4                    
  05f24:  movs r1, #0x3e                    
  05f26:  movs r0, #8                       
  05f28:  bl #0x1c60                        -> func_0x01c60
  05f2c:  mov r5, r0                        
  05f2e:  mov.w r0, #0x3e8                  
  05f32:  str r0, [sp]                      
  05f34:  nop                               
  05f36:  ldr r0, [sp]                      
  05f38:  subs r1, r0, #1                   
  05f3a:  str r1, [sp]                      
  05f3c:  cmp r0, #0                        
  05f3e:  bne #0x5f36                       
  05f40:  nop                               
  05f42:  cbz r5, #0x5f72                   
  05f44:  ldrb.w r0, [sp, #6]               
  05f48:  and r0, r0, #0x80                 
  05f4c:  cbz r0, #0x5f90                   
  05f4e:  movs r0, #0x92                    
  05f50:  bl #0x1bdc                        -> func_0x01bdc
  05f54:  ands r4, r0                       
  05f56:  movw r0, #0x2710                  
  05f5a:  str r0, [sp]                      
  05f5c:  nop                               
  05f5e:  ldr r0, [sp]                      
  05f60:  subs r1, r0, #1                   
  05f62:  str r1, [sp]                      
  05f64:  cmp r0, #0                        
  05f66:  bne #0x5f5e                       
  05f68:  movs r0, #1                       
  05f6a:  ldr r1, [pc, #0x44]               -> RAM
  05f6c:  strh r0, [r1]                     
  05f6e:  movs r0, #0                       
  05f70:  pop {r1, r2, r3, r4, r5, pc}      
  ; --- literal-пул @0x05fb0 (1 слов) — ВНЕ границ функции ---
  05fb0:  .word 0x20000a7c  ; RAM
```
