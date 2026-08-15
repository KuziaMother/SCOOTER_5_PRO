# func_0x00ce8

| | |
|---|---|
| offset в файле | `0x00ce8` |
| vaddr (база 0x01800000) | `0x01800ce8` |
 | размер кода | 62 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200164 — RAM (r0)

## Вызовы (callees)

- `func_0x00c8c` (0x01800c8c, bl)
- 0x01802bf4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01800ce8:  push {r3, r4, r5, lr}             
  01800cea:  mov r4, r0                        
  01800cec:  ldrb r0, [r1]                     
  01800cee:  cmp r0, #3                        
  01800cf0:  bne #0x1800d22                    
  01800cf2:  ldrh r0, [r4]                     
  01800cf4:  movw r5, #0xc7c                   
  01800cf8:  cmp r0, r5                        
  01800cfa:  bne #0x1800d22                    
  01800cfc:  ldr r0, [pc, #0x60]               (RAM)
  01800cfe:  ldrh.w r0, [r0, #0x70]            
  01800d02:  lsls r0, r0, #0x12                
  01800d04:  bpl #0x1800d22                    
  01800d06:  mov r0, r4                        
  01800d08:  bl #0x1800c8c                     -> func_0x00c8c
  01800d0c:  mov r1, r0                        
  01800d0e:  ldrh.w r2, [r4, #3]               
  01800d12:  movs r0, #2                       
  01800d14:  str r0, [sp]                      
  01800d16:  movs r3, #0                       
  01800d18:  mov r0, r5                        
  01800d1a:  bl #0x1802bf4                     -> 0x02bf4 (вне списка функций)
  01800d1e:  movs r0, #1                       
  01800d20:  pop {r3, r4, r5, pc}              
  01800d22:  movs r0, #0                       
  01800d24:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x00d60 (1 слов) — ВНЕ границ функции ---
  00d60:  .word 0x00200164  ; RAM
```
