# func_0x01bdc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001bdc) | `0x00001bdc` |
| размер кода | 42 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01e72` (0x00001e72, bl)

## Кто вызывает (callers / xrefs)

- `func_0x02a5c` (bl @0x00002a62)
- `func_0x03b20` (bl @0x00003b24)
- `func_0x048f8` (bl @0x00004946)
- `func_0x049b8` (bl @0x000049f2)
- `func_0x04de0` (bl @0x00004de6)
- `func_0x04de0` (bl @0x00004dee)
- `func_0x04e08` (bl @0x00004e0e)
- `func_0x05274` (bl @0x000052e4)
- `func_0x05ee0` (bl @0x00005eee)
- `func_0x05ee0` (bl @0x00005f08)
- `func_0x05ee0` (bl @0x00005f50)
- `func_0x09134` (bl @0x00009188)
- `func_0x09134` (bl @0x000091a6)
- `func_0x09134` (bl @0x000091e6)
- `func_0x09134` (bl @0x0000922e)
- `func_0x09134` (bl @0x00009284)
- `func_0x0a7ec` (bl @0x0000a80a)
- `func_0x0a7ec` (bl @0x0000a88e)
- `func_0x0c158` (bl @0x0000c17c)
- `func_0x0c158` (bl @0x0000c1d6)
- `func_0x0c20c` (bl @0x0000c22a)
- `func_0x0c20c` (bl @0x0000c25e)
- `func_0x11de8` (bl @0x00012186)
- `func_0x11de8` (bl @0x00012270)
- `func_0x11de8` (bl @0x00012288)
- `func_0x11de8` (bl @0x00012316)
- `func_0x11de8` (bl @0x0001232e)


## Дизассембляция

```asm
  01bdc:  push {r2, r3, r4, lr}             
  01bde:  mov r4, r0                        
  01be0:  movs r0, #0                       
  01be2:  str r0, [sp, #4]                  
  01be4:  uxtb r0, r4                       
  01be6:  strb.w r0, [sp, #4]               
  01bea:  lsrs r0, r4, #8                   
  01bec:  strb.w r0, [sp, #5]               
  01bf0:  movs r0, #2                       
  01bf2:  add r3, sp, #4                    
  01bf4:  movs r2, #1                       
  01bf6:  movs r1, #0x3e                    
  01bf8:  str r0, [sp]                      
  01bfa:  movs r0, #8                       
  01bfc:  bl #0x1e72                        -> func_0x01e72
  01c00:  cbnz r0, #0x1c06                  
  01c02:  movs r0, #0                       
  01c04:  pop {r2, r3, r4, pc}              
```
