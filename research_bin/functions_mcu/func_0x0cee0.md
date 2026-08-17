# func_0x0cee0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cee0) | `0x0000cee0` |
| размер кода | 68 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01e72` (0x00001e72, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0a788` (bl @0x0000a79c)
- `func_0x0c304` (bl @0x0000c318)
- `func_0x12aec` (bl @0x00012b00)
- `func_0x14924` (bl @0x00014938)


## Дизассембляция

```asm
  0cee0:  push.w {r2, r3, r4, r5, r6, r7, r8, lr}
  0cee4:  mov r8, r0                        
  0cee6:  mov r4, r1                        
  0cee8:  mov r5, r2                        
  0ceea:  mov r6, r3                        
  0ceec:  movs r0, #0                       
  0ceee:  str r0, [sp, #4]                  
  0cef0:  movs r7, #0                       
  0cef2:  ldrh r7, [r5]                     
  0cef4:  uxtb r0, r4                       
  0cef6:  strb.w r0, [sp, #4]               
  0cefa:  lsrs r0, r4, #8                   
  0cefc:  strb.w r0, [sp, #5]               
  0cf00:  uxtb r0, r7                       
  0cf02:  strb.w r0, [sp, #6]               
  0cf06:  lsrs r0, r7, #8                   
  0cf08:  strb.w r0, [sp, #7]               
  0cf0c:  movs r0, #2                       
  0cf0e:  add r3, sp, #4                    
  0cf10:  movs r2, #1                       
  0cf12:  movs r1, #0x3e                    
  0cf14:  str r0, [sp]                      
  0cf16:  mov r0, r8                        
  0cf18:  bl #0x1e72                        -> func_0x01e72
  0cf1c:  cbnz r0, #0xcf24                  
  0cf1e:  movs r0, #0                       
  0cf20:  pop.w {r2, r3, r4, r5, r6, r7, r8, pc}
```
