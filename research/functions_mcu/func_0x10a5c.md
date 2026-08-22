# func_0x10a5c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080010a5c) | `0x00010a5c` |
| размер кода | 50 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0cd80` (0x0000cd80, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03740` (bl @0x00003758)
- `func_0x05448` (bl @0x000054c6)
- `func_0x1330c` (bl @0x00013370)


## Дизассембляция

```asm
  10a5c:  push {r0, r1, lr}                 
  10a5e:  sub sp, #0xc                      
  10a60:  ldrb.w r0, [sp, #0x12]            
  10a64:  strb.w r0, [sp, #4]               
  10a68:  ldrb.w r0, [sp, #0x10]            
  10a6c:  strb.w r0, [sp, #5]               
  10a70:  ldrb.w r0, [sp, #0xf]             
  10a74:  strb.w r0, [sp, #6]               
  10a78:  ldrb.w r0, [sp, #0x11]            
  10a7c:  strb.w r0, [sp, #7]               
  10a80:  add r1, sp, #4                    
  10a82:  movs r0, #0                       
  10a84:  bl #0xcd80                        -> func_0x0cd80
  10a88:  cbnz r0, #0x10a8e                 
  10a8a:  add sp, #0x14                     
  10a8c:  pop {pc}                          
```
