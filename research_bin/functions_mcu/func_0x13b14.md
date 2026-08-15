# func_0x13b14

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080013b14) | `0x00013b14` |
| размер кода | 72 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200030dd — RAM (r0)

## Вызовы (callees)

- `func_0x08380` (0x00008380, bl)
- `func_0x087f8` (0x000087f8, bl)
- 0x13b58 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  13b14:  push {r3, r4, r5, lr}             
  13b16:  mov r4, r0                        
  13b18:  movs r5, #0                       
  13b1a:  movs r2, #0x20                    
  13b1c:  mov r1, r4                        
  13b1e:  ldr r0, [pc, #0x3c]               -> RAM
  13b20:  bl #0x8380                        -> func_0x08380
  13b24:  mov r5, r0                        
  13b26:  cbnz r5, #0x13b42                 
  13b28:  movs r0, #0x64                    
  13b2a:  str r0, [sp]                      
  13b2c:  nop                               
  13b2e:  ldr r0, [sp]                      
  13b30:  subs r1, r0, #1                   
  13b32:  str r1, [sp]                      
  13b34:  cmp r0, #0                        
  13b36:  bne #0x13b2e                      
  13b38:  movs r2, #0x20                    
  13b3a:  mov r1, r4                        
  13b3c:  ldr r0, [pc, #0x1c]               -> RAM
  13b3e:  bl #0x8380                        -> func_0x08380
  13b42:  movs r1, #0x18                    
  13b44:  ldr r0, [pc, #0x14]               -> RAM
  13b46:  bl #0x87f8                        -> func_0x087f8
  13b4a:  ldr r1, [pc, #0x10]               -> RAM
  13b4c:  ldrb r1, [r1, #0x18]              
  13b4e:  cmp r0, r1                        
  13b50:  bne #0x13b56                      
  13b52:  movs r5, #0                       
  13b54:  b #0x13b58                        -> 0x13b58 (вне списка функций)
  13b56:  movs r5, #1                       
  13b58:  mov r0, r5                        
  13b5a:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x13b5c (1 слов) — ВНЕ границ функции ---
  13b5c:  .word 0x200030dd  ; RAM
```
