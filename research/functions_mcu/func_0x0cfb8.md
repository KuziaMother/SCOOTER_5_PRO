# func_0x0cfb8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cfb8) | `0x0000cfb8` |
| размер кода | 78 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000304c — RAM (r0)

## Вызовы (callees)

- `func_0x08380` (0x00008380, bl)
- `func_0x08a50` (0x00008a50, bl)
- 0x0d002 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0d298` (bl @0x0000d2a0)
- `func_0x0d298` (bl @0x0000d2b8)
- `func_0x0eddc` (bl @0x0000edde)
- `func_0x0eddc` (bl @0x0000edf6)


## Дизассембляция

```asm
  0cfb8:  push {r3, r4, r5, lr}             
  0cfba:  movs r4, #0                       
  0cfbc:  movs r5, #0                       
  0cfbe:  movs r2, #0x10                    
  0cfc0:  lsls r1, r2, #0xd                 
  0cfc2:  ldr r0, [pc, #0x44]               -> RAM
  0cfc4:  bl #0x8380                        -> func_0x08380
  0cfc8:  mov r4, r0                        
  0cfca:  cbnz r4, #0xcfe8                  
  0cfcc:  movs r0, #0x64                    
  0cfce:  str r0, [sp]                      
  0cfd0:  nop                               
  0cfd2:  ldr r0, [sp]                      
  0cfd4:  subs r1, r0, #1                   
  0cfd6:  str r1, [sp]                      
  0cfd8:  cmp r0, #0                        
  0cfda:  bne #0xcfd2                       
  0cfdc:  movs r2, #0x10                    
  0cfde:  lsls r1, r2, #0xd                 
  0cfe0:  ldr r0, [pc, #0x24]               -> RAM
  0cfe2:  bl #0x8380                        -> func_0x08380
  0cfe6:  mov r4, r0                        
  0cfe8:  cmp r4, #1                        
  0cfea:  bne #0xd002                       
  0cfec:  movs r1, #0xc                     
  0cfee:  ldr r0, [pc, #0x18]               -> RAM
  0cff0:  bl #0x8a50                        -> func_0x08a50
  0cff4:  mov r5, r0                        
  0cff6:  ldr r0, [pc, #0x10]               -> RAM
  0cff8:  ldr r0, [r0, #0xc]                
  0cffa:  cmp r0, r5                        
  0cffc:  bne #0xd000                       
  0cffe:  b #0xd002                         -> 0x0d002 (вне списка функций)
  0d000:  movs r4, #0                       
  0d002:  mov r0, r4                        
  0d004:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x0d008 (1 слов) — ВНЕ границ функции ---
  0d008:  .word 0x2000304c  ; RAM
```
