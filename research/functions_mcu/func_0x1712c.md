# func_0x1712c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001712c) | `0x0001712c` |
| размер кода | 36 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x172b8` (0x000172b8, bl)

## Кто вызывает (callers / xrefs)

- `func_0x16880` (bl @0x0001690c)
- `func_0x16880` (bl @0x00016926)
- `func_0x16938` (bl @0x000169c4)
- `func_0x16938` (bl @0x000169de)


## Дизассембляция

```asm
  1712c:  push {r2, r3, r4, r5, r6, lr}     
  1712e:  mov r5, r0                        
  17130:  mov r6, r1                        
  17132:  mov r4, r2                        
  17134:  add r3, sp, #4                    
  17136:  mov r2, sp                        
  17138:  mov r1, r6                        
  1713a:  mov r0, r5                        
  1713c:  bl #0x172b8                       -> func_0x172b8
  17140:  rsb.w r1, r4, #0x20               
  17144:  ldr r0, [sp]                      
  17146:  lsls r0, r1                       
  17148:  ldr r1, [sp, #4]                  
  1714a:  lsrs r1, r4                       
  1714c:  orrs r0, r1                       
  1714e:  pop {r2, r3, r4, r5, r6, pc}      
```
