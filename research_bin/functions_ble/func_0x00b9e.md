# func_0x00b9e

| | |
|---|---|
| offset в файле | `0x00b9e` |
| vaddr (база 0x01800000) | `0x01800b9e` |
 | размер кода | 44 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202044 — RAM (r0)

## Вызовы (callees)

- 0x01802bae (bl, вне списка функций)
- 0x01802bb8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01800b9e:  push {r2, r3, r4, r5, r6, lr}     
  01800ba0:  mov r4, r0                        
  01800ba2:  ldrb r2, [r0, #0xf]               
  01800ba4:  movs r0, #0                       
  01800ba6:  movs r5, #0x12                    
  01800ba8:  str r0, [sp]                      
  01800baa:  str r0, [sp, #4]                  
  01800bac:  cmp r2, #1                        
  01800bae:  bne #0x1800bbe                    
  01800bb0:  ldr r0, [pc, #0x178]              (RAM)
  01800bb2:  movs r2, #6                       
  01800bb4:  mov r1, sp                        
  01800bb6:  adds r0, #0x1c                    
  01800bb8:  bl #0x1802bae                     -> 0x02bae (вне списка функций)
  01800bbc:  cbz r0, #0x1800bca                
  01800bbe:  mov r0, r4                        
  01800bc0:  bl #0x1802bb8                     -> 0x02bb8 (вне списка функций)
  01800bc4:  mov r5, r0                        
  01800bc6:  mov r0, r5                        
  01800bc8:  pop {r2, r3, r4, r5, r6, pc}      
  ; --- literal-пул @0x00d2c (1 слов) — ВНЕ границ функции ---
  00d2c:  .word 0x00202044  ; RAM
```
