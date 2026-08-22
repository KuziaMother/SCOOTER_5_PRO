# func_0x0126c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000126c) | `0x0000126c` |
| размер кода | 32 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x0123e` (bl @0x00001262)
- `func_0x012aa` (bl @0x000012e8)


## Дизассембляция

```asm
  0126c:  cmp r2, #0x20                     
  0126e:  blt #0x127a                       
  01270:  subs r2, #0x20                    
  01272:  lsr.w r0, r1, r2                  
  01276:  movs r1, #0                       
  01278:  bx lr                             
  0127a:  lsr.w r3, r1, r2                  
  0127e:  lsrs r0, r2                       
  01280:  rsb.w r2, r2, #0x20               
  01284:  lsls r1, r2                       
  01286:  orrs r0, r1                       
  01288:  mov r1, r3                        
  0128a:  bx lr                             
```
