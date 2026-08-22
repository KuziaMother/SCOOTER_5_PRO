# func_0x0b618

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b618) | `0x0000b618` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x097ca` (0x000097ca, bl)
- `func_0x097e2` (0x000097e2, bl)
- 0x0b8c8 (bl, вне списка функций)
- 0x0b968 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0b618:  push.w {r4, r5, r6, r7, r8, lr}   
  0b61c:  mov r4, r0                        
  0b61e:  movs r7, #0                       
  0b620:  movs r5, #0                       
  0b622:  mov r8, r5                        
  0b624:  mov r0, r4                        
  0b626:  bl #0xb8c8                        -> 0x0b8c8 (вне списка функций)
  0b62a:  mov r0, r4                        
  0b62c:  bl #0xb968                        -> 0x0b968 (вне списка функций)
  0b630:  cbnz r0, #0xb650                  
  0b632:  movs r1, #0                       
  0b634:  ldr r0, [r4]                      
  0b636:  bl #0x97ca                        -> func_0x097ca
  0b63a:  movs r0, #0                       
  0b63c:  strb.w r0, [r4, #0x10c]           
  0b640:  movs r2, #0                       
  0b642:  mov.w r1, #0x700                  
  0b646:  ldr r0, [r4]                      
  0b648:  bl #0x97e2                        -> func_0x097e2
  0b64c:  pop.w {r4, r5, r6, r7, r8, pc}    
```
