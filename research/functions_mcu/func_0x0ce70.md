# func_0x0ce70

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ce70) | `0x0000ce70` |
| размер кода | 92 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40002824 — периферия (r3)

## Вызовы (callees)

- 0x0cec4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0310c` (bl @0x0000314a)


## Дизассембляция

```asm
  0ce70:  push {r3, lr}                     
  0ce72:  movs r2, #0                       
  0ce74:  str r2, [sp]                      
  0ce76:  movs r0, #0                       
  0ce78:  movs r1, #0                       
  0ce7a:  movs r2, #0xca                    
  0ce7c:  ldr r3, [pc, #0x4c]               -> периферия
  0ce7e:  str r2, [r3]                      
  0ce80:  movs r2, #0x53                    
  0ce82:  str r2, [r3]                      
  0ce84:  ldr r2, [pc, #0x44]               -> периферия
  0ce86:  subs r2, #0x18                    
  0ce88:  ldr r2, [r2]                      
  0ce8a:  bic r2, r2, #0x20                 
  0ce8e:  ldr r3, [pc, #0x3c]               -> периферия
  0ce90:  subs r3, #0x18                    
  0ce92:  str r2, [r3]                      
  0ce94:  nop                               
  0ce96:  ldr r2, [pc, #0x34]               -> периферия
  0ce98:  subs r2, #0x18                    
  0ce9a:  ldr r2, [r2]                      
  0ce9c:  and r1, r2, #0x20                 
  0cea0:  ldr r2, [sp]                      
  0cea2:  adds r2, r2, #1                   
  0cea4:  str r2, [sp]                      
  0cea6:  ldr r2, [sp]                      
  0cea8:  cmp.w r2, #0x8000                 
  0ceac:  beq #0xceb2                       
  0ceae:  cmp r1, #0                        
  0ceb0:  beq #0xce96                       
  0ceb2:  ldr r2, [pc, #0x18]               -> периферия
  0ceb4:  subs r2, #0x18                    
  0ceb6:  ldr r2, [r2]                      
  0ceb8:  and r2, r2, #0x20                 
  0cebc:  cbz r2, #0xcec2                   
  0cebe:  movs r0, #1                       
  0cec0:  b #0xcec4                         -> 0x0cec4 (вне списка функций)
  0cec2:  movs r0, #0                       
  0cec4:  movs r2, #0xff                    
  0cec6:  ldr r3, [pc, #4]                  -> периферия
  0cec8:  str r2, [r3]                      
  0ceca:  pop {r3, pc}                      
  ; --- literal-пул @0x0cecc (1 слов) — ВНЕ границ функции ---
  0cecc:  .word 0x40002824  ; периферия
```
