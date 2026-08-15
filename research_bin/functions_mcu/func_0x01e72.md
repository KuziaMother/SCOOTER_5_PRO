# func_0x01e72

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001e72) | `0x00001e72` |
| размер кода | 32 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x02730` (0x00002730, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01bdc` (bl @0x00001bfc)
- `func_0x01c7a` (bl @0x00001ca2)
- `func_0x0cee0` (bl @0x0000cf18)
- `func_0x155ac` (bl @0x000155e2)


## Дизассембляция

```asm
  01e72:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  01e76:  mov r4, r0                        
  01e78:  mov r5, r1                        
  01e7a:  mov r8, r2                        
  01e7c:  mov r6, r3                        
  01e7e:  ldr r7, [sp, #0x20]               
  01e80:  uxtb r2, r5                       
  01e82:  mov r3, r6                        
  01e84:  mov r1, r4                        
  01e86:  movs r0, #0                       
  01e88:  str r7, [sp]                      
  01e8a:  bl #0x2730                        -> func_0x02730
  01e8e:  pop.w {r3, r4, r5, r6, r7, r8, sb, pc}
```
