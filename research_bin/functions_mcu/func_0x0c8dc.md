# func_0x0c8dc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c8dc) | `0x0000c8dc` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0c858` (0x0000c858, bl)
- 0x0c910 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x10cdc` (bl @0x00010cee)


## Дизассембляция

```asm
  0c8dc:  push {r3, r4, r5, lr}             
  0c8de:  movs r0, #0                       
  0c8e0:  str r0, [sp]                      
  0c8e2:  movs r4, #0                       
  0c8e4:  movs r5, #0                       
  0c8e6:  nop                               
  0c8e8:  movs r0, #0x21                    
  0c8ea:  bl #0xc858                        -> func_0x0c858
  0c8ee:  mov r5, r0                        
  0c8f0:  ldr r0, [sp]                      
  0c8f2:  adds r0, r0, #1                   
  0c8f4:  str r0, [sp]                      
  0c8f6:  ldr r0, [sp]                      
  0c8f8:  cmp.w r0, #0x500                  
  0c8fc:  beq #0xc902                       
  0c8fe:  cmp r5, #0                        
  0c900:  beq #0xc8e8                       
  0c902:  movs r0, #0x21                    
  0c904:  bl #0xc858                        -> func_0x0c858
  0c908:  cbz r0, #0xc90e                   
  0c90a:  movs r4, #1                       
  0c90c:  b #0xc910                         -> 0x0c910 (вне списка функций)
  0c90e:  movs r4, #0                       
  0c910:  mov r0, r4                        
  0c912:  pop {r3, r4, r5, pc}              
```
