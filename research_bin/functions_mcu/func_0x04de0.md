# func_0x04de0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004de0) | `0x00004de0` |
| размер кода | 40 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)

## Кто вызывает (callers / xrefs)

- `func_0x05b8c` (bl @0x00005b90)


## Дизассембляция

```asm
  04de0:  push {r3, r4, r5, lr}             
  04de2:  movs r4, #0                       
  04de4:  movs r0, #0x93                    
  04de6:  bl #0x1bdc                        -> func_0x01bdc
  04dea:  ands r4, r0                       
  04dec:  movs r0, #0x94                    
  04dee:  bl #0x1bdc                        -> func_0x01bdc
  04df2:  ands r4, r0                       
  04df4:  mov.w r0, #0x1f4                  
  04df8:  str r0, [sp]                      
  04dfa:  nop                               
  04dfc:  ldr r0, [sp]                      
  04dfe:  subs r1, r0, #1                   
  04e00:  str r1, [sp]                      
  04e02:  cmp r0, #0                        
  04e04:  bne #0x4dfc                       
  04e06:  pop {r3, r4, r5, pc}              
```
