# func_0x058b0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800058b0) | `0x000058b0` |
| размер кода | 70 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x05970` (0x00005970, bl)
- 0x059a4 (bl, вне списка функций)
- `func_0x0c0b4` (0x0000c0b4, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0c94c` (bl @0x0000c95e)


## Дизассембляция

```asm
  058b0:  push {r1, r2, r3, r4, r5, lr}     
  058b2:  mov r4, r0                        
  058b4:  mov.w r0, #0x100000               
  058b8:  bl #0x5970                        -> func_0x05970
  058bc:  mov.w r0, #0x100000               
  058c0:  str r0, [sp, #4]                  
  058c2:  movs r0, #0                       
  058c4:  strb.w r0, [sp, #8]               
  058c8:  movs r0, #8                       
  058ca:  strb.w r0, [sp, #9]               
  058ce:  movs r0, #1                       
  058d0:  strb.w r0, [sp, #0xa]             
  058d4:  add r0, sp, #4                    
  058d6:  bl #0x59a4                        -> 0x059a4 (вне списка функций)
  058da:  movs r0, #3                       
  058dc:  strb.w r0, [sp]                   
  058e0:  movs r0, #0                       
  058e2:  strb.w r0, [sp, #1]               
  058e6:  strb.w r0, [sp, #2]               
  058ea:  strb.w r4, [sp, #3]               
  058ee:  mov r0, sp                        
  058f0:  bl #0xc0b4                        -> func_0x0c0b4
  058f4:  pop {r1, r2, r3, r4, r5, pc}      
```
