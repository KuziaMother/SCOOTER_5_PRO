# func_0x13b60

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080013b60) | `0x00013b60` |
| размер кода | 84 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200030cf — RAM (r0)

## Вызовы (callees)

- `func_0x08380` (0x00008380, bl)
- `func_0x08a50` (0x00008a50, bl)
- 0x13bb0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x13bb8` (bl @0x00013bc4)
- `func_0x13bb8` (bl @0x00013bdc)


## Дизассембляция

```asm
  13b60:  push {r3, r4, r5, lr}             
  13b62:  movs r4, #0                       
  13b64:  movs r5, #0                       
  13b66:  movs r2, #0xe                     
  13b68:  mov.w r1, #0x40000                
  13b6c:  ldr r0, [pc, #0x44]               -> RAM
  13b6e:  bl #0x8380                        -> func_0x08380
  13b72:  mov r4, r0                        
  13b74:  cbnz r4, #0x13b94                 
  13b76:  movs r0, #0x64                    
  13b78:  str r0, [sp]                      
  13b7a:  nop                               
  13b7c:  ldr r0, [sp]                      
  13b7e:  subs r1, r0, #1                   
  13b80:  str r1, [sp]                      
  13b82:  cmp r0, #0                        
  13b84:  bne #0x13b7c                      
  13b86:  movs r2, #0xe                     
  13b88:  mov.w r1, #0x40000                
  13b8c:  ldr r0, [pc, #0x24]               -> RAM
  13b8e:  bl #0x8380                        -> func_0x08380
  13b92:  mov r4, r0                        
  13b94:  cmp r4, #1                        
  13b96:  bne #0x13bb0                      
  13b98:  movs r1, #0xa                     
  13b9a:  ldr r0, [pc, #0x18]               -> RAM
  13b9c:  bl #0x8a50                        -> func_0x08a50
  13ba0:  mov r5, r0                        
  13ba2:  ldr r0, [pc, #0x10]               -> RAM
  13ba4:  ldr.w r0, [r0, #0xa]              
  13ba8:  cmp r0, r5                        
  13baa:  bne #0x13bae                      
  13bac:  b #0x13bb0                        -> 0x13bb0 (вне списка функций)
  13bae:  movs r4, #0                       
  13bb0:  mov r0, r4                        
  13bb2:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x13bb4 (1 слов) — ВНЕ границ функции ---
  13bb4:  .word 0x200030cf  ; RAM
```
