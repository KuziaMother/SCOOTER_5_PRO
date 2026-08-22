# func_0x0cb40

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cb40) | `0x0000cb40` |
| размер кода | 116 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40002824 — периферия (r4)

## Вызовы (callees)

- 0x0cbac (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03168` (bl @0x000031c2)
- `func_0x0c94c` (bl @0x0000c97c)


## Дизассембляция

```asm
  0cb40:  push {r3, r4, lr}                 
  0cb42:  mov r1, r0                        
  0cb44:  movs r3, #0                       
  0cb46:  str r3, [sp]                      
  0cb48:  movs r2, #0                       
  0cb4a:  movs r0, #0                       
  0cb4c:  movs r3, #0xca                    
  0cb4e:  ldr r4, [pc, #0x64]               -> периферия
  0cb50:  str r3, [r4]                      
  0cb52:  movs r3, #0x53                    
  0cb54:  str r3, [r4]                      
  0cb56:  cbz r1, #0xcb6c                   
  0cb58:  ldr r3, [pc, #0x58]               -> периферия
  0cb5a:  subs r3, #0x1c                    
  0cb5c:  ldr r3, [r3]                      
  0cb5e:  orr r3, r3, #0x400                
  0cb62:  ldr r4, [pc, #0x50]               -> периферия
  0cb64:  subs r4, #0x1c                    
  0cb66:  str r3, [r4]                      
  0cb68:  movs r0, #1                       
  0cb6a:  b #0xcbac                         -> 0x0cbac (вне списка функций)
  0cb6c:  ldr r3, [pc, #0x44]               -> периферия
  0cb6e:  subs r3, #0x1c                    
  0cb70:  ldr r3, [r3]                      
  0cb72:  bic r3, r3, #0x400                
  0cb76:  ldr r4, [pc, #0x3c]               -> периферия
  0cb78:  subs r4, #0x1c                    
  0cb7a:  str r3, [r4]                      
  0cb7c:  nop                               
  0cb7e:  ldr r3, [pc, #0x34]               -> периферия
  0cb80:  subs r3, #0x18                    
  0cb82:  ldr r3, [r3]                      
  0cb84:  and r2, r3, #4                    
  0cb88:  ldr r3, [sp]                      
  0cb8a:  adds r3, r3, #1                   
  0cb8c:  str r3, [sp]                      
  0cb8e:  ldr r3, [sp]                      
  0cb90:  cmp.w r3, #0x2000                 
  0cb94:  beq #0xcb9a                       
  0cb96:  cmp r2, #0                        
  0cb98:  beq #0xcb7e                       
  0cb9a:  ldr r3, [pc, #0x18]               -> периферия
  0cb9c:  subs r3, #0x18                    
  0cb9e:  ldr r3, [r3]                      
  0cba0:  and r3, r3, #4                    
  0cba4:  cbnz r3, #0xcbaa                  
  0cba6:  movs r0, #0                       
  0cba8:  b #0xcbac                         -> 0x0cbac (вне списка функций)
  0cbaa:  movs r0, #1                       
  0cbac:  movs r3, #0xff                    
  0cbae:  ldr r4, [pc, #4]                  -> периферия
  0cbb0:  str r3, [r4]                      
  0cbb2:  pop {r3, r4, pc}                  
  ; --- literal-пул @0x0cbb4 (1 слов) — ВНЕ границ функции ---
  0cbb4:  .word 0x40002824  ; периферия
```
