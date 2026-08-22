# func_0x01c7a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001c7a) | `0x00001c7a` |
| размер кода | 52 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01e72` (0x00001e72, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01d78` (bl @0x00001d8a)
- `func_0x01d78` (bl @0x00001db6)
- `func_0x0218c` (bl @0x0000219a)


## Дизассембляция

```asm
  01c7a:  push.w {r2, r3, r4, r5, r6, r7, r8, lr}
  01c7e:  mov r7, r0                        
  01c80:  mov r4, r1                        
  01c82:  mov r5, r2                        
  01c84:  mov r6, r3                        
  01c86:  movs r0, #0                       
  01c88:  str r0, [sp, #4]                  
  01c8a:  uxtb r0, r4                       
  01c8c:  strb.w r0, [sp, #4]               
  01c90:  lsrs r0, r4, #8                   
  01c92:  strb.w r0, [sp, #5]               
  01c96:  movs r0, #2                       
  01c98:  add r3, sp, #4                    
  01c9a:  movs r2, #1                       
  01c9c:  movs r1, #0x3e                    
  01c9e:  str r0, [sp]                      
  01ca0:  mov r0, r7                        
  01ca2:  bl #0x1e72                        -> func_0x01e72
  01ca6:  cbnz r0, #0x1cae                  
  01ca8:  movs r0, #0                       
  01caa:  pop.w {r2, r3, r4, r5, r6, r7, r8, pc}
```
