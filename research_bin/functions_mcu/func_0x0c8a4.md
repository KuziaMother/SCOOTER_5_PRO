# func_0x0c8a4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c8a4) | `0x0000c8a4` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0c858` (0x0000c858, bl)
- 0x0c8d8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x10ba0` (bl @0x00010bb4)


## Дизассембляция

```asm
  0c8a4:  push {r3, r4, r5, lr}             
  0c8a6:  movs r0, #0                       
  0c8a8:  str r0, [sp]                      
  0c8aa:  movs r4, #0                       
  0c8ac:  movs r5, #0                       
  0c8ae:  nop                               
  0c8b0:  movs r0, #0x31                    
  0c8b2:  bl #0xc858                        -> func_0x0c858
  0c8b6:  mov r5, r0                        
  0c8b8:  ldr r0, [sp]                      
  0c8ba:  adds r0, r0, #1                   
  0c8bc:  str r0, [sp]                      
  0c8be:  ldr r0, [sp]                      
  0c8c0:  cmp.w r0, #0x2000                 
  0c8c4:  beq #0xc8ca                       
  0c8c6:  cmp r5, #0                        
  0c8c8:  beq #0xc8b0                       
  0c8ca:  movs r0, #0x31                    
  0c8cc:  bl #0xc858                        -> func_0x0c858
  0c8d0:  cbz r0, #0xc8d6                   
  0c8d2:  movs r4, #1                       
  0c8d4:  b #0xc8d8                         -> 0x0c8d8 (вне списка функций)
  0c8d6:  movs r4, #0                       
  0c8d8:  mov r0, r4                        
  0c8da:  pop {r3, r4, r5, pc}              
```
