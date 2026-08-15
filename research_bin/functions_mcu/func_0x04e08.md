# func_0x04e08

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004e08) | `0x00004e08` |
| размер кода | 32 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)

## Кто вызывает (callers / xrefs)

- `func_0x049b8` (bl @0x000049dc)


## Дизассембляция

```asm
  04e08:  push {r3, r4, r5, lr}             
  04e0a:  movs r4, #0                       
  04e0c:  movs r0, #0x94                    
  04e0e:  bl #0x1bdc                        -> func_0x01bdc
  04e12:  ands r4, r0                       
  04e14:  mov.w r0, #0x1f4                  
  04e18:  str r0, [sp]                      
  04e1a:  nop                               
  04e1c:  ldr r0, [sp]                      
  04e1e:  subs r1, r0, #1                   
  04e20:  str r1, [sp]                      
  04e22:  cmp r0, #0                        
  04e24:  bne #0x4e1c                       
  04e26:  pop {r3, r4, r5, pc}              
```
