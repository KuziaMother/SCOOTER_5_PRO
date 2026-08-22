# func_0x0128c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000128c) | `0x0000128c` |
| размер кода | 30 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x012aa` (b @0x00001344)
- `func_0x01346` (b.w @0x00001462)


## Дизассембляция

```asm
  0128c:  push {r4, lr}                     
  0128e:  subs r4, r2, #0                   
  01290:  sbcs r4, r3, #0                   
  01294:  bge #0x12a8                       
  01296:  adds r0, r0, #1                   
  01298:  adc r1, r1, #0                    
  0129c:  adds r2, r2, r2                   
  0129e:  adcs r3, r3                       
  012a0:  orrs r2, r3                       
  012a2:  bne #0x12a8                       
  012a4:  bic r0, r0, #1                    
  012a8:  pop {r4, pc}                      
```
