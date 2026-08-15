# func_0x01cf6

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001cf6) | `0x00001cf6` |
| размер кода | 54 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x03b20` (0x00003b20, bl)
- `func_0x0c138` (0x0000c138, bl)
- `func_0x11c5e` (0x00011c5e, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e1e)


## Дизассембляция

```asm
  01cf6:  push {r3, lr}                     
  01cf8:  bl #0x11c5e                       -> func_0x11c5e
  01cfc:  mov.w r0, #0x3e8                  
  01d00:  str r0, [sp]                      
  01d02:  nop                               
  01d04:  ldr r0, [sp]                      
  01d06:  subs r1, r0, #1                   
  01d08:  str r1, [sp]                      
  01d0a:  cmp r0, #0                        
  01d0c:  bne #0x1d04                       
  01d0e:  bl #0x3b20                        -> func_0x03b20
  01d12:  movw r0, #0x2710                  
  01d16:  str r0, [sp]                      
  01d18:  nop                               
  01d1a:  ldr r0, [sp]                      
  01d1c:  subs r1, r0, #1                   
  01d1e:  str r1, [sp]                      
  01d20:  cmp r0, #0                        
  01d22:  bne #0x1d1a                       
  01d24:  bl #0xc138                        -> func_0x0c138
  01d28:  cbz r0, #0x1d2c                   
  01d2a:  pop {r3, pc}                      
```
