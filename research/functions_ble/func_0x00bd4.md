# func_0x00bd4

| | |
|---|---|
| offset в файле | `0x00bd4` |
| vaddr (база 0x01800000) | `0x01800bd4` |
 | размер кода | 52 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202044 — RAM (r0)
- 0x00206838 — RAM (r1)

## Вызовы (callees)

- 0x01802bcc (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01800bd4:  push {r4, lr}                     
  01800bd6:  mov r4, r2                        
  01800bd8:  bl #0x1802bcc                     -> 0x02bcc (вне списка функций)
  01800bdc:  ldr r1, [pc, #0x17c]              (RAM)
  01800bde:  ldr r0, [pc, #0x14c]              (RAM)
  01800be0:  ldrb r1, [r1, #5]                 
  01800be2:  strb.w r1, [r0, #0x29c]           
  01800be6:  mov r3, r0                        
  01800be8:  add.w r0, r3, r4, lsl #2          
  01800bec:  ldr.w r0, [r0, #0x210]            
  01800bf0:  ldr r1, [r0]                      
  01800bf2:  orr r1, r1, #0x20000000           
  01800bf6:  str r1, [r0]                      
  01800bf8:  ldrb.w r1, [r0, #0x3e]            
  01800bfc:  ldrb.w r2, [r3, #0x29c]           
  01800c00:  ands r1, r2                       
  01800c02:  strb.w r1, [r0, #0x3e]            
  01800c06:  pop {r4, pc}                      
  ; --- literal-пул @0x00d2c (1 слов) — ВНЕ границ функции ---
  00d2c:  .word 0x00202044  ; RAM
  ; --- literal-пул @0x00d5c (1 слов) — ВНЕ границ функции ---
  00d5c:  .word 0x00206838  ; RAM
```
