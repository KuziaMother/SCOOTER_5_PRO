# func_0x01e52

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001e52) | `0x00001e52` |
| размер кода | 32 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0214c` (0x0000214c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01c60` (bl @0x00001c74)


## Дизассембляция

```asm
  01e52:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  01e56:  mov r4, r0                        
  01e58:  mov r5, r1                        
  01e5a:  mov r8, r2                        
  01e5c:  mov r6, r3                        
  01e5e:  ldr r7, [sp, #0x20]               
  01e60:  uxtb r2, r5                       
  01e62:  mov r3, r6                        
  01e64:  mov r1, r4                        
  01e66:  movs r0, #0                       
  01e68:  str r7, [sp]                      
  01e6a:  bl #0x214c                        -> func_0x0214c
  01e6e:  pop.w {r3, r4, r5, r6, r7, r8, sb, pc}
```
