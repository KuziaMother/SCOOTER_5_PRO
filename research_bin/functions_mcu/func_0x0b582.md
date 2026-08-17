# func_0x0b582

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b582) | `0x0000b582` |
| размер кода | 72 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x097ca` (0x000097ca, bl)
- `func_0x097e2` (0x000097e2, bl)
- `func_0x0985c` (0x0000985c, bl)
- 0x0b8c8 (bl, вне списка функций)
- 0x0b968 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0b582:  push {r4, lr}                     
  0b584:  movs r1, #0                       
  0b586:  ldr r0, [sp, #8]                  
  0b588:  bl #0x97ca                        -> func_0x097ca
  0b58c:  movs r1, #1                       
  0b58e:  ldr r0, [sp, #8]                  
  0b590:  bl #0x985c                        -> func_0x0985c
  0b594:  movs r0, #0                       
  0b596:  pop {r4}                          
  0b598:  ldr pc, [sp], #0x14               
  0b59c:  push {r4, lr}                     
  0b59e:  mov r4, r0                        
  0b5a0:  mov r0, r4                        
  0b5a2:  bl #0xb8c8                        -> 0x0b8c8 (вне списка функций)
  0b5a6:  mov r0, r4                        
  0b5a8:  bl #0xb968                        -> 0x0b968 (вне списка функций)
  0b5ac:  cbnz r0, #0xb5ca                  
  0b5ae:  movs r1, #0                       
  0b5b0:  ldr r0, [r4]                      
  0b5b2:  bl #0x97ca                        -> func_0x097ca
  0b5b6:  movs r0, #0                       
  0b5b8:  strb.w r0, [r4, #0x10c]           
  0b5bc:  movs r2, #0                       
  0b5be:  mov.w r1, #0x700                  
  0b5c2:  ldr r0, [r4]                      
  0b5c4:  bl #0x97e2                        -> func_0x097e2
  0b5c8:  pop {r4, pc}                      
```
