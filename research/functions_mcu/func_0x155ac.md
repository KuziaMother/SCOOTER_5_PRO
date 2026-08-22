# func_0x155ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800155ac) | `0x000155ac` |
| размер кода | 64 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01e72` (0x00001e72, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03668` (bl @0x000036b2)
- `func_0x0a788` (bl @0x0000a7d2)
- `func_0x0c304` (bl @0x0000c34e)
- `func_0x12aec` (bl @0x00012b36)


## Дизассембляция

```asm
  155ac:  push {r1, r2, r3, r4, r5, r6, r7, lr}
  155ae:  mov r7, r0                        
  155b0:  mov r5, r1                        
  155b2:  mov r6, r2                        
  155b4:  mov r4, r3                        
  155b6:  movs r0, #0                       
  155b8:  str r0, [sp, #8]                  
  155ba:  str r0, [sp, #4]                  
  155bc:  uxtb r0, r5                       
  155be:  strb.w r0, [sp, #8]               
  155c2:  lsrs r0, r5, #8                   
  155c4:  strb.w r0, [sp, #9]               
  155c8:  uxtb r0, r6                       
  155ca:  strb.w r0, [sp, #0xa]             
  155ce:  lsrs r0, r6, #8                   
  155d0:  strb.w r0, [sp, #0xb]             
  155d4:  adds r0, r4, #2                   
  155d6:  uxtb r0, r0                       
  155d8:  add r3, sp, #8                    
  155da:  movs r2, #1                       
  155dc:  movs r1, #0x3e                    
  155de:  str r0, [sp]                      
  155e0:  mov r0, r7                        
  155e2:  bl #0x1e72                        -> func_0x01e72
  155e6:  cbnz r0, #0x155ec                 
  155e8:  movs r0, #0                       
  155ea:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
```
