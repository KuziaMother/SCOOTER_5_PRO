# func_0x01ee0

| | |
|---|---|
| offset в файле | `0x01ee0` |
| vaddr (база 0x01800000) | `0x01801ee0` |
 | размер кода | 48 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005ec — RAM (r4)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01801ee0:  push {r4, lr}                     
  01801ee2:  ldr r0, [r0, #4]                  
  01801ee4:  ldrb r1, [r0, #1]                 
  01801ee6:  lsls r1, r1, #0x1e                
  01801ee8:  bmi #0x1801f08                    
  01801eea:  ldr r4, [pc, #0x130]              (RAM)
  01801eec:  ldrb r0, [r0, #4]                 
  01801eee:  mov.w r1, #0x3e0                  
  01801ef2:  lsls r2, r0, #5                   
  01801ef4:  ldr r3, [r4]                      
  01801ef6:  movs r0, #0x1e                    
  01801ef8:  blx r3                            
  01801efa:  ldr r3, [r4]                      
  01801efc:  movs r2, #0                       
  01801efe:  movs r1, #0x20                    
  01801f00:  pop.w {r4, lr}                    
  01801f04:  movs r0, #0x1c                    
  01801f06:  bx r3                             
  01801f08:  pop.w {r4, lr}                    
  01801f0c:  b.w #0x1802d98                    
  ; --- literal-пул @0x0201c (1 слов) — ВНЕ границ функции ---
  0201c:  .word 0x002005ec  ; RAM
```
