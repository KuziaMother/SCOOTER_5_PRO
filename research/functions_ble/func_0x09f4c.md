# func_0x09f4c

| | |
|---|---|
| offset в файле | `0x09f4c` |
| vaddr (база 0x01800000) | `0x01809f4c` |
 | размер кода | 52 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005ec — RAM (r4)
- 0x00206958 — RAM (r0)

## Вызовы (callees)

- `func_0x09dce` (0x01809dce, bl)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01809f4c:  push {r4, lr}                     
  01809f4e:  ldr r4, [pc, #0x8c]               (RAM)
  01809f50:  movs r2, #4                       
  01809f52:  mov r1, r2                        
  01809f54:  ldr r3, [r4]                      
  01809f56:  movs r0, #0xe                     
  01809f58:  blx r3                            
  01809f5a:  movs r2, #0                       
  01809f5c:  movs r1, #0x30                    
  01809f5e:  ldr r3, [r4]                      
  01809f60:  movs r0, #0xe                     
  01809f62:  blx r3                            
  01809f64:  ldr r0, [pc, #0x78]               (RAM)
  01809f66:  movs r2, #0x10                    
  01809f68:  movs r1, #0x15                    
  01809f6a:  ldr r0, [r0, #4]                  
  01809f6c:  adds r0, r0, #7                   
  01809f6e:  bl #0x1809dce                     -> func_0x09dce
  01809f72:  ldr r3, [r4]                      
  01809f74:  movs r2, #0                       
  01809f76:  movs r1, #4                       
  01809f78:  pop.w {r4, lr}                    
  01809f7c:  movs r0, #0xe                     
  01809f7e:  bx r3                             
  ; --- literal-пул @0x09fdc (2 слов) — ВНЕ границ функции ---
  09fdc:  .word 0x002005ec  ; RAM
  09fe0:  .word 0x00206958  ; RAM
```
