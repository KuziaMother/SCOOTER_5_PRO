# func_0x08e5c

| | |
|---|---|
| offset в файле | `0x08e5c` |
| vaddr (база 0x01800000) | `0x01808e5c` |
 | размер кода | 90 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202000 — RAM (r2)
- 0x00fa1b59 — прочее (r0)

## Вызовы (callees)

- 0x015f5fa4 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08eb6` (bl @0x01808f5c)

## Дизассембляция

```asm
  01808e5c:  push {r1, r2, r3, r4, r5, r6, r7, lr}
  01808e5e:  mov r6, r1                        
  01808e60:  mov r5, r0                        
  01808e62:  ldrh r1, [r0]                     
  01808e64:  movs r0, #2                       
  01808e66:  add.w r0, r0, r1, lsr #8          
  01808e6a:  uxtb r0, r0                       
  01808e6c:  lsls r2, r0, #0x1f                
  01808e6e:  beq #0x1808e74                    
  01808e70:  adds r0, r0, #1                   
  01808e72:  uxtb r0, r0                       
  01808e74:  ldr r2, [pc, #0x3e4]              (RAM)
  01808e76:  adds r0, r0, #6                   
  01808e78:  and r3, r1, #0xf                  
  01808e7c:  ldrb r2, [r2]                     
  01808e7e:  movw r1, #0xc91                   
  01808e82:  add.w r4, r0, r2, lsl #1          
  01808e86:  movs r2, #2                       
  01808e88:  ldr r0, [pc, #0x3d4]              
  01808e8a:  str r4, [sp]                      
  01808e8c:  bl #0x15f5fa4                     
  01808e90:  cmp r4, r6                        
  01808e92:  bls #0x1808eb2                    
  01808e94:  ldrh r0, [r5]                     
  01808e96:  movs r2, #4                       
  01808e98:  lsrs r1, r0, #8                   
  01808e9a:  and r3, r0, #0xf                  
  01808e9e:  stm.w sp, {r1, r4, r6}            
  01808ea2:  ldr r0, [pc, #0x3bc]              
  01808ea4:  movw r1, #0xc8f                   
  01808ea8:  adds r0, r0, #4                   
  01808eaa:  bl #0x15f5fa4                     
  01808eae:  mov r0, r6                        
  01808eb0:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  01808eb2:  mov r0, r4                        
  01808eb4:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  ; --- literal-пул @0x0925c (2 слов) — ВНЕ границ функции ---
  0925c:  .word 0x00202000  ; RAM
  09260:  .word 0x00fa1b59
```
