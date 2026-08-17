# func_0x030a6

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800030a6) | `0x000030a6` |
| размер кода | 58 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x05970` (0x00005970, bl)
- 0x059a4 (bl, вне списка функций)
- `func_0x08588` (0x00008588, bl)
- `func_0x0c624` (0x0000c624, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03f00` (bl @0x00003f4c)


## Дизассембляция

```asm
  030a6:  push {r2, r3, r4, lr}             
  030a8:  movs r1, #1                       
  030aa:  mov r0, r1                        
  030ac:  bl #0xc624                        -> func_0x0c624
  030b0:  movs r1, #0xb                     
  030b2:  movs r0, #1                       
  030b4:  bl #0x8588                        -> func_0x08588
  030b8:  mov.w r0, #0x800                  
  030bc:  bl #0x5970                        -> func_0x05970
  030c0:  mov.w r0, #0x800                  
  030c4:  str r0, [sp]                      
  030c6:  movs r0, #0                       
  030c8:  strb.w r0, [sp, #4]               
  030cc:  movs r0, #8                       
  030ce:  strb.w r0, [sp, #5]               
  030d2:  movs r0, #0                       
  030d4:  strb.w r0, [sp, #6]               
  030d8:  mov r0, sp                        
  030da:  bl #0x59a4                        -> 0x059a4 (вне списка функций)
  030de:  pop {r2, r3, r4, pc}              
```
