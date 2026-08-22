# func_0x0bc86

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000bc86) | `0x0000bc86` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x085c8` (0x000085c8, bl)
- `func_0x087b0` (0x000087b0, bl)
- 0x0bcbc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0bc86:  push {r0, r1, r2, r3, r4, lr}     
  0bc88:  mov r0, sp                        
  0bc8a:  bl #0x87b0                        -> func_0x087b0
  0bc8e:  ldrh.w r0, [sp, #0x24]            
  0bc92:  ldrh.w r1, [sp, #0x26]            
  0bc96:  orrs r0, r1                       
  0bc98:  strh.w r0, [sp]                   
  0bc9c:  movs r0, #0                       
  0bc9e:  strb.w r0, [sp, #4]               
  0bca2:  movs r0, #3                       
  0bca4:  str r0, [sp, #8]                  
  0bca6:  movs r0, #1                       
  0bca8:  strb.w r0, [sp, #3]               
  0bcac:  mov r1, sp                        
  0bcae:  ldr r0, [sp, #0x1c]               
  0bcb0:  bl #0x85c8                        -> func_0x085c8
  0bcb4:  pop {r0, r1, r2, r3, r4}          
  0bcb6:  ldr pc, [sp], #0x14               
  0bcba:  nop                               
  0bcbc:  b #0xbcbc                         -> 0x0bcbc (вне списка функций)
```
