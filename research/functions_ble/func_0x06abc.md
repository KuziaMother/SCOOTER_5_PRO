# func_0x06abc

| | |
|---|---|
| offset в файле | `0x06abc` |
| vaddr (база 0x01800000) | `0x01806abc` |
 | размер кода | 42 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202044 — RAM (r2)

## Вызовы (callees)

- 0x0161fba2 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x06ae6` (bl @0x01806b10)

## Дизассембляция

```asm
  01806abc:  push {r4, lr}                     
  01806abe:  ldr r2, [pc, #0xf4]               (RAM)
  01806ac0:  ldrh r1, [r0, #0xc]               
  01806ac2:  ldrh.w r3, [r2, #0x2a8]           
  01806ac6:  add.w r2, r2, #0x2a4              
  01806aca:  cmp r1, r3                        
  01806acc:  bne #0x1806ad6                    
  01806ace:  ldr r0, [r0, #8]                  
  01806ad0:  ldr r1, [r2]                      
  01806ad2:  cmp r0, r1                        
  01806ad4:  beq #0x1806ada                    
  01806ad6:  movs r0, #0                       
  01806ad8:  pop {r4, pc}                      
  01806ada:  ldrb r1, [r2, #7]                 
  01806adc:  ldrb r0, [r2, #6]                 
  01806ade:  bl #0x161fba2                     
  01806ae2:  movs r0, #1                       
  01806ae4:  pop {r4, pc}                      
  ; --- literal-пул @0x06bb4 (1 слов) — ВНЕ границ функции ---
  06bb4:  .word 0x00202044  ; RAM
```
