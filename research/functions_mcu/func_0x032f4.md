# func_0x032f4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800032f4) | `0x000032f4` |
| размер кода | 54 Б |
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

- `func_0x05908` (bl @0x00005928)
- `func_0x11de8` (bl @0x00012006)


## Дизассембляция

```asm
  032f4:  push {r2, r3, r4, lr}             
  032f6:  movs r1, #1                       
  032f8:  mov r0, r1                        
  032fa:  bl #0xc624                        -> func_0x0c624
  032fe:  movs r1, #7                       
  03300:  movs r0, #1                       
  03302:  bl #0x8588                        -> func_0x08588
  03306:  movs r0, #0x80                    
  03308:  bl #0x5970                        -> func_0x05970
  0330c:  movs r0, #0x80                    
  0330e:  str r0, [sp]                      
  03310:  movs r0, #0                       
  03312:  strb.w r0, [sp, #4]               
  03316:  movs r0, #0xc                     
  03318:  strb.w r0, [sp, #5]               
  0331c:  movs r0, #0                       
  0331e:  strb.w r0, [sp, #6]               
  03322:  mov r0, sp                        
  03324:  bl #0x59a4                        -> 0x059a4 (вне списка функций)
  03328:  pop {r2, r3, r4, pc}              
```
