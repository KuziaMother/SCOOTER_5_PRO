# func_0x0bc5c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000bc5c) | `0x0000bc5c` |
| размер кода | 40 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0c0b4` (0x0000c0b4, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0ae9a` (bl @0x0000aeb4)
- `func_0x0ae9a` (bl @0x0000aec2)
- `func_0x0ae9a` (bl @0x0000b01a)
- `func_0x0ae9a` (bl @0x0000b028)
- `func_0x0aece` (bl @0x0000b01a)
- `func_0x0aece` (bl @0x0000b028)
- `func_0x0af94` (bl @0x0000b01a)
- `func_0x0af94` (bl @0x0000b028)


## Дизассембляция

```asm
  0bc5c:  push {r3, r4, r5, r6, r7, lr}     
  0bc5e:  mov r7, r0                        
  0bc60:  mov r4, r1                        
  0bc62:  mov r5, r2                        
  0bc64:  mov r6, r3                        
  0bc66:  uxtb r0, r7                       
  0bc68:  strb.w r0, [sp]                   
  0bc6c:  uxtb r0, r4                       
  0bc6e:  strb.w r0, [sp, #1]               
  0bc72:  uxtb r0, r5                       
  0bc74:  strb.w r0, [sp, #2]               
  0bc78:  strb.w r6, [sp, #3]               
  0bc7c:  mov r0, sp                        
  0bc7e:  bl #0xc0b4                        -> func_0x0c0b4
  0bc82:  pop {r3, r4, r5, r6, r7, pc}      
```
