# func_0x09ec8

| | |
|---|---|
| offset в файле | `0x09ec8` |
| vaddr (база 0x01800000) | `0x01809ec8` |
 | размер кода | 132 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005ec — RAM (r4)
- 0x00206958 — RAM (r0)

## Вызовы (callees)

- `func_0x09dce` (0x01809dce, bl)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01809ec8:  push {r4, lr}                     
  01809eca:  ldr r4, [pc, #0x54]               (RAM)
  01809ecc:  movs r2, #4                       
  01809ece:  mov r1, r2                        
  01809ed0:  ldr r3, [r4]                      
  01809ed2:  movs r0, #0xe                     
  01809ed4:  blx r3                            
  01809ed6:  movs r2, #0x10                    
  01809ed8:  movs r1, #0x30                    
  01809eda:  ldr r3, [r4]                      
  01809edc:  movs r0, #0xe                     
  01809ede:  blx r3                            
  01809ee0:  ldr r0, [pc, #0x20]               (RAM)
  01809ee2:  movs r2, #0x10                    
  01809ee4:  movs r1, #0x15                    
  01809ee6:  ldr r0, [r0, #4]                  
  01809ee8:  adds r0, #0x1f                    
  01809eea:  bl #0x1809dce                     -> func_0x09dce
  01809eee:  ldr r3, [r4]                      
  01809ef0:  movs r2, #0                       
  01809ef2:  movs r1, #4                       
  01809ef4:  pop.w {r4, lr}                    
  01809ef8:  movs r0, #0xe                     
  01809efa:  bx r3                             
  01809efc:  lsls r4, r4, #5                   
  01809efe:  movs r0, r4                       
  01809f00:  cmp r0, #0x33                     
  01809f02:  movs r0, r4                       
  01809f04:  ldr r0, [r3, #0x14]               
  01809f06:  movs r0, r4                       
  01809f08:  lsrs r4, r4, #5                   
  01809f0a:  movs r0, r4                       
  01809f0c:  subs r4, r2, #0                   
  01809f0e:  movs r0, r4                       
  01809f10:  subs r0, r4, #0                   
  01809f12:  movs r0, r4                       
  01809f14:  movs r0, r0                       
  01809f16:  cmn r0, r1                        
  01809f18:  movs r0, r0                       
  01809f1a:  add r2, pc                        
  01809f1c:  str r4, [r4, #0x50]               
  01809f1e:  movs r0, r4                       
  01809f20:  lsls r4, r5, #0x17                
  01809f22:  movs r0, r4                       
  01809f24:  lsrs r0, r2, #5                   
  01809f26:  movs r0, r4                       
  01809f28:  lsrs r0, r0, #5                   
  01809f2a:  movs r0, r4                       
  01809f2c:  lsrs r4, r5, #6                   
  01809f2e:  movs r0, r4                       
  01809f30:  lsrs r4, r3, #5                   
  01809f32:  movs r0, r4                       
  01809f34:  lsls r4, r7, #0x16                
  01809f36:  movs r0, r4                       
  01809f38:  subs r0, r2, #0                   
  01809f3a:  movs r0, r4                       
  01809f3c:  lsls r4, r0, #0x17                
  01809f3e:  movs r0, r4                       
  01809f40:  ldr r4, [r7, #0xc]                
  01809f42:  movs r0, r4                       
  01809f44:  lsrs r4, r1, #5                   
  01809f46:  movs r0, r4                       
  01809f48:  lsrs r7, r0, #0xc                 
  01809f4a:  movs r7, r1                       
  ; --- literal-пул @0x09f04 (1 слов) ---
  09f04:  .word 0x00206958  ; RAM
  ; --- literal-пул @0x09f20 (1 слов) ---
  09f20:  .word 0x002005ec  ; RAM
```
