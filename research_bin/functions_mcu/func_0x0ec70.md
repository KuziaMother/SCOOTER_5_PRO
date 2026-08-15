# func_0x0ec70

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ec70) | `0x0000ec70` |
| размер кода | 352 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a538 — flash-mirror @0x1a538 (r1)
- 0x2000128b — RAM (r0)
- 0x200012ba — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x0e3e4` (0x0000e3e4, bl)
- 0x10fa4 (bl, вне списка функций)
- 0x10fb0 (bl, вне списка функций)
- 0x10fbc (bl, вне списка функций)
- 0x10fc8 (bl, вне списка функций)
- 0x10fd4 (bl, вне списка функций)
- 0x10fe0 (bl, вне списка функций)
- 0x10fec (bl, вне списка функций)
- 0x10ff8 (bl, вне списка функций)
- 0x11004 (bl, вне списка функций)
- 0x11010 (bl, вне списка функций)
- 0x1101c (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11894` (bl @0x000118be)


## Дизассембляция

```asm
  0ec70:  push {r3, lr}                     
  0ec72:  movs r0, #0                       
  0ec74:  ldr r1, [pc, #0x158]              -> flash-mirror @0x1a538
  0ec76:  ldr r1, [r1]                      
  0ec78:  str r0, [r1]                      
  0ec7a:  movs r1, #0x2f                    
  0ec7c:  ldr r0, [pc, #0x154]              -> RAM
  0ec7e:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0ec82:  movs r1, #0x8a                    
  0ec84:  ldr r0, [pc, #0x150]              -> RAM
  0ec86:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0ec8a:  movs r0, #0                       
  0ec8c:  bl #0x10ff8                       -> 0x10ff8 (вне списка функций)
  0ec90:  mov r0, sp                        
  0ec92:  bl #0xe3e4                        -> func_0x0e3e4
  0ec96:  movs r0, #0                       
  0ec98:  ldr r1, [pc, #0x138]              -> RAM
  0ec9a:  str r0, [r1, #4]                  
  0ec9c:  str r0, [r1, #8]                  
  0ec9e:  str r0, [r1, #0xc]                
  0eca0:  strh r0, [r1, #0x22]              
  0eca2:  str r0, [r1, #0x10]               
  0eca4:  strb.w r0, [r1, #0x2b]            
  0eca8:  strh r0, [r1, #0x20]              
  0ecaa:  bl #0x10fb0                       -> 0x10fb0 (вне списка функций)
  0ecae:  movs r0, #0                       
  0ecb0:  bl #0x10fec                       -> 0x10fec (вне списка функций)
  0ecb4:  movs r0, #0                       
  0ecb6:  ldr r1, [pc, #0x120]              -> RAM
  0ecb8:  strb.w r0, [r1, #0x60]            
  0ecbc:  strb.w r0, [r1, #0x61]            
  0ecc0:  strb.w r0, [r1, #0x5e]            
  0ecc4:  strb.w r0, [r1, #0x5f]            
  0ecc8:  bl #0x10fa4                       -> 0x10fa4 (вне списка функций)
  0eccc:  movs r0, #1                       
  0ecce:  ldr r1, [pc, #0x108]              -> RAM
  0ecd0:  strb.w r0, [r1, #0x6d]            
  0ecd4:  movs r0, #0                       
  0ecd6:  strb.w r0, [r1, #0x70]            
  0ecda:  strb.w r0, [r1, #0x6e]            
  0ecde:  strb.w r0, [r1, #0x6f]            
  0ece2:  str r0, [r1, #0x44]               
  0ece4:  ldr r1, [pc, #0xec]               -> RAM
  0ece6:  str r0, [r1, #0x18]               
  0ece8:  strb.w r0, [r1, #0x2e]            
  0ecec:  strh r0, [r1, #0x28]              
  0ecee:  mov r0, sp                        
  0ecf0:  bl #0xe3e4                        -> func_0x0e3e4
  0ecf4:  movs r0, #0                       
  0ecf6:  bl #0x11010                       -> 0x11010 (вне списка функций)
  0ecfa:  movs r0, #0                       
  0ecfc:  bl #0x1101c                       -> 0x1101c (вне списка функций)
  0ed00:  movs r0, #1                       
  0ed02:  ldr r1, [pc, #0xd4]               -> RAM
  0ed04:  strb.w r0, [r1, #0x53]            
  0ed08:  movs r0, #0                       
  0ed0a:  strb.w r0, [r1, #0x54]            
  0ed0e:  strb.w r0, [r1, #0x55]            
  0ed12:  strb.w r0, [r1, #0x56]            
  0ed16:  ldr r1, [pc, #0xbc]               -> RAM
  0ed18:  strh r0, [r1, #0x1c]              
  0ed1a:  bl #0x10fd4                       -> 0x10fd4 (вне списка функций)
  0ed1e:  movs r0, #0                       
  0ed20:  ldr r1, [pc, #0xb4]               -> RAM
  0ed22:  strb.w r0, [r1, #0x65]            
  0ed26:  strb.w r0, [r1, #0x66]            
  0ed2a:  str r0, [r1, #0x40]               
  0ed2c:  strh.w r0, [r1, #0x4c]            
  0ed30:  strb.w r0, [r1, #0x67]            
  0ed34:  str r0, [r1, #0x2c]               
  0ed36:  strh.w r0, [r1, #0x4e]            
  0ed3a:  ldr r1, [pc, #0x98]               -> RAM
  0ed3c:  strh r0, [r1, #0x24]              
  0ed3e:  bl #0x10fbc                       -> 0x10fbc (вне списка функций)
  0ed42:  movs r0, #1                       
  0ed44:  ldr r1, [pc, #0x90]               -> RAM
  0ed46:  strb.w r0, [r1, #0x6a]            
  0ed4a:  movs r0, #0                       
  0ed4c:  strb.w r0, [r1, #0x6b]            
  0ed50:  strb.w r0, [r1, #0x6c]            
  0ed54:  ldr r1, [pc, #0x7c]               -> RAM
  0ed56:  strh r0, [r1, #0x26]              
  0ed58:  bl #0x10fe0                       -> 0x10fe0 (вне списка функций)
  0ed5c:  movs r0, #0                       
  0ed5e:  ldr r1, [pc, #0x78]               -> RAM
  0ed60:  strb.w r0, [r1, #0x64]            
  0ed64:  strb.w r0, [r1, #0x62]            
  0ed68:  strb.w r0, [r1, #0x63]            
  0ed6c:  str r0, [r1, #0x34]               
  0ed6e:  str r0, [r1, #0x38]               
  0ed70:  str r0, [r1, #0x3c]               
  0ed72:  ldr r1, [pc, #0x60]               -> RAM
  0ed74:  strb.w r0, [r1, #0x2c]            
  0ed78:  str r0, [r1, #0x14]               
  0ed7a:  bl #0x11004                       -> 0x11004 (вне списка функций)
  0ed7e:  movs r0, #0                       
  0ed80:  ldr r1, [pc, #0x54]               -> RAM
  0ed82:  strb.w r0, [r1, #0x59]            
  0ed86:  strb.w r0, [r1, #0x57]            
  0ed8a:  strb.w r0, [r1, #0x58]            
  0ed8e:  str r0, [r1, #0x30]               
  0ed90:  ldr r1, [pc, #0x40]               -> RAM
  0ed92:  strh r0, [r1, #0x1e]              
  0ed94:  ldr r1, [pc, #0x40]               -> RAM
  0ed96:  strb.w r0, [r1, #0x5c]            
  0ed9a:  strb.w r0, [r1, #0x5d]            
  0ed9e:  ldr r1, [pc, #0x34]               -> RAM
  0eda0:  str r0, [r1]                      
  0eda2:  ldr r1, [pc, #0x34]               -> RAM
  0eda4:  strb.w r0, [r1, #0x5a]            
  0eda8:  strb.w r0, [r1, #0x5b]            
  0edac:  strh.w r0, [r1, #0x4a]            
  0edb0:  ldr r1, [pc, #0x20]               -> RAM
  0edb2:  strb.w r0, [r1, #0x2a]            
  0edb6:  bl #0x10fc8                       -> 0x10fc8 (вне списка функций)
  0edba:  movs r0, #0                       
  0edbc:  ldr r1, [pc, #0x18]               -> RAM
  0edbe:  strb.w r0, [r1, #0x68]            
  0edc2:  strb.w r0, [r1, #0x69]            
  0edc6:  strh.w r0, [r1, #0x50]            
  0edca:  strh.w r0, [r1, #0x48]            
  0edce:  pop {r3, pc}                      
  ; --- literal-пул @0x0edd0 (3 слов) — ВНЕ границ функции ---
  0edd0:  .word 0x0801a538  ; flash-mirror @0x1a538
  0edd4:  .word 0x2000128b  ; RAM
  0edd8:  .word 0x200012ba  ; RAM
```
