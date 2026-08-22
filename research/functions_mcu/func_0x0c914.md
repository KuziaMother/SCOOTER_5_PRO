# func_0x0c914

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c914) | `0x0000c914` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0c858` (0x0000c858, bl)
- 0x0c948 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0c914:  push {r3, r4, r5, lr}             
  0c916:  movs r0, #0                       
  0c918:  str r0, [sp]                      
  0c91a:  movs r4, #0                       
  0c91c:  movs r5, #0                       
  0c91e:  nop                               
  0c920:  movs r0, #0x63                    
  0c922:  bl #0xc858                        -> func_0x0c858
  0c926:  mov r5, r0                        
  0c928:  ldr r0, [sp]                      
  0c92a:  adds r0, r0, #1                   
  0c92c:  str r0, [sp]                      
  0c92e:  ldr r0, [sp]                      
  0c930:  cmp.w r0, #0x500                  
  0c934:  beq #0xc93a                       
  0c936:  cmp r5, #0                        
  0c938:  beq #0xc920                       
  0c93a:  movs r0, #0x63                    
  0c93c:  bl #0xc858                        -> func_0x0c858
  0c940:  cbz r0, #0xc946                   
  0c942:  movs r4, #1                       
  0c944:  b #0xc948                         -> 0x0c948 (вне списка функций)
  0c946:  movs r4, #0                       
  0c948:  mov r0, r4                        
  0c94a:  pop {r3, r4, r5, pc}              
```
