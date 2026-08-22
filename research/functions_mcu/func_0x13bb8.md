# func_0x13bb8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080013bb8) | `0x00013bb8` |
| размер кода | 48 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200030cf — RAM (r0)

## Вызовы (callees)

- `func_0x13b60` (0x00013b60, bl)

## Кто вызывает (callers / xrefs)

- `func_0x057f8` (bl @0x0000580c)
- `func_0x05818` (bl @0x0000581e)


## Дизассембляция

```asm
  13bb8:  push {r3, r4, r5, r6, r7, lr}     
  13bba:  mov r5, r0                        
  13bbc:  mov r4, r1                        
  13bbe:  movs r6, #0                       
  13bc0:  movs r7, #0                       
  13bc2:  cbnz r5, #0x13be0                 
  13bc4:  bl #0x13b60                       -> func_0x13b60
  13bc8:  cbnz r0, #0x13be0                 
  13bca:  mov.w r0, #0x1f4                  
  13bce:  str r0, [sp]                      
  13bd0:  nop                               
  13bd2:  ldr r0, [sp]                      
  13bd4:  subs r1, r0, #1                   
  13bd6:  str r1, [sp]                      
  13bd8:  cmp r0, #0                        
  13bda:  bne #0x13bd2                      
  13bdc:  bl #0x13b60                       -> func_0x13b60
  13be0:  ldr r0, [pc, #0x74]               -> RAM
  13be2:  ldrh r0, [r0]                     
  13be4:  cbnz r0, #0x13be8                 
  13be6:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x13c58 (1 слов) — ВНЕ границ функции ---
  13c58:  .word 0x200030cf  ; RAM
```
