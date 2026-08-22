# func_0x0cf60

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cf60) | `0x0000cf60` |
| размер кода | 84 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000305c — RAM (r0)

## Вызовы (callees)

- `func_0x08380` (0x00008380, bl)
- `func_0x08a50` (0x00008a50, bl)
- 0x0cfa8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0cf60:  push {r3, r4, r5, lr}             
  0cf62:  mov r4, r0                        
  0cf64:  movs r5, #0                       
  0cf66:  movs r2, #0x28                    
  0cf68:  mov r1, r4                        
  0cf6a:  ldr r0, [pc, #0x48]               -> RAM
  0cf6c:  bl #0x8380                        -> func_0x08380
  0cf70:  mov r5, r0                        
  0cf72:  cbnz r5, #0xcf90                  
  0cf74:  movs r0, #0x64                    
  0cf76:  str r0, [sp]                      
  0cf78:  nop                               
  0cf7a:  ldr r0, [sp]                      
  0cf7c:  subs r1, r0, #1                   
  0cf7e:  str r1, [sp]                      
  0cf80:  cmp r0, #0                        
  0cf82:  bne #0xcf7a                       
  0cf84:  movs r2, #0x28                    
  0cf86:  mov r1, r4                        
  0cf88:  ldr r0, [pc, #0x28]               -> RAM
  0cf8a:  bl #0x8380                        -> func_0x08380
  0cf8e:  mov r5, r0                        
  0cf90:  movs r1, #0x26                    
  0cf92:  ldr r0, [pc, #0x20]               -> RAM
  0cf94:  bl #0x8a50                        -> func_0x08a50
  0cf98:  ldr r1, [pc, #0x18]               -> RAM
  0cf9a:  ldrh r1, [r1, #0x26]              
  0cf9c:  cmp r0, r1                        
  0cf9e:  bne #0xcfaa                       
  0cfa0:  movs r0, #1                       
  0cfa2:  ldr r1, [pc, #0x10]               -> RAM
  0cfa4:  strh r0, [r1, #0x24]              
  0cfa6:  movs r0, #0                       
  0cfa8:  pop {r3, r4, r5, pc}              
  0cfaa:  movs r0, #0                       
  0cfac:  ldr r1, [pc, #4]                  -> RAM
  0cfae:  strh r0, [r1, #0x24]              
  0cfb0:  movs r0, #1                       
  0cfb2:  b #0xcfa8                         -> 0x0cfa8 (вне списка функций)
  ; --- literal-пул @0x0cfb4 (1 слов) — ВНЕ границ функции ---
  0cfb4:  .word 0x2000305c  ; RAM
```
