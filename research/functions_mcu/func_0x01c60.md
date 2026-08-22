# func_0x01c60

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001c60) | `0x00001c60` |
| размер кода | 26 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01e52` (0x00001e52, bl)

## Кто вызывает (callers / xrefs)

- `func_0x020c4` (bl @0x000020ce)
- `func_0x02138` (bl @0x00002142)
- `func_0x021dc` (bl @0x000021e6)
- `func_0x021f0` (bl @0x000021fa)
- `func_0x02204` (bl @0x0000220e)
- `func_0x02218` (bl @0x00002222)
- `func_0x0222c` (bl @0x00002236)
- `func_0x02240` (bl @0x0000224a)
- `func_0x02254` (bl @0x0000225e)
- `func_0x02268` (bl @0x00002272)
- `func_0x0227c` (bl @0x00002286)
- `func_0x02290` (bl @0x0000229a)
- `func_0x022a4` (bl @0x000022ae)
- `func_0x022b8` (bl @0x000022c2)
- `func_0x022cc` (bl @0x000022d6)
- `func_0x022e0` (bl @0x000022ea)
- `func_0x022f4` (bl @0x000022fe)
- `func_0x02308` (bl @0x00002312)
- `func_0x0231c` (bl @0x00002326)
- `func_0x02330` (bl @0x0000233a)
- `func_0x02344` (bl @0x0000234e)
- `func_0x02358` (bl @0x00002362)
- `func_0x048f8` (bl @0x00004968)
- `func_0x05274` (bl @0x000052ba)
- `func_0x05274` (bl @0x00005304)
- `func_0x05ee0` (bl @0x00005f28)
- `func_0x0d33c` (bl @0x0000d358)
- `func_0x11de8` (bl @0x000121a4)


## Дизассембляция

```asm
  01c60:  push {r3, r4, r5, r6, r7, lr}     
  01c62:  mov r6, r0                        
  01c64:  mov r7, r1                        
  01c66:  mov r4, r2                        
  01c68:  mov r5, r3                        
  01c6a:  mov r3, r4                        
  01c6c:  movs r2, #1                       
  01c6e:  mov r1, r7                        
  01c70:  mov r0, r6                        
  01c72:  str r5, [sp]                      
  01c74:  bl #0x1e52                        -> func_0x01e52
  01c78:  pop {r3, r4, r5, r6, r7, pc}      
```
