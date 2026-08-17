# func_0x0123e

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000123e) | `0x0000123e` |
| размер кода | 46 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0126c` (0x0000126c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0123e:  push {r4, lr}                     
  01240:  ubfx r1, r1, #0, #0x14            
  01244:  movw r3, #0x3ff                   
  01248:  orr r1, r1, #0x100000             
  0124c:  cmp r2, r3                        
  0124e:  bge #0x1254                       
  01250:  movs r0, #0                       
  01252:  pop {r4, pc}                      
  01254:  movw r3, #0x433                   
  01258:  cmp r2, r3                        
  0125a:  subw r2, r2, #0x433               
  0125e:  bgt #0x1268                       
  01260:  rsbs r2, r2, #0                   
  01262:  bl #0x126c                        -> func_0x0126c
  01266:  pop {r4, pc}                      
  01268:  lsls r0, r2                       
  0126a:  pop {r4, pc}                      
```
