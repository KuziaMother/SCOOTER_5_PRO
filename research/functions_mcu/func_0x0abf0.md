# func_0x0abf0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000abf0) | `0x0000abf0` |
| размер кода | 46 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x0a8c4` (0x0000a8c4, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0d00c` (bl @0x0000d18c)
- `func_0x0d39c` (bl @0x0000d3ae)


## Дизассембляция

```asm
  0abf0:  push {r4, r5, r6, r7, lr}         
  0abf2:  sub sp, #0x24                     
  0abf4:  mov r7, r0                        
  0abf6:  movs r6, #0                       
  0abf8:  movs r4, #0                       
  0abfa:  movs r5, #0                       
  0abfc:  movs r1, #0x20                    
  0abfe:  add r0, sp, #4                    
  0ac00:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0ac04:  movs r0, #0                       
  0ac06:  bl #0xa8c4                        -> func_0x0a8c4
  0ac0a:  mov r6, r0                        
  0ac0c:  movs r0, #1                       
  0ac0e:  bl #0xa8c4                        -> func_0x0a8c4
  0ac12:  mov r4, r0                        
  0ac14:  cbnz r6, #0xac6e                  
  0ac16:  cbnz r4, #0xac1e                  
  0ac18:  movs r0, #0                       
  0ac1a:  add sp, #0x24                     
  0ac1c:  pop {r4, r5, r6, r7, pc}          
```
