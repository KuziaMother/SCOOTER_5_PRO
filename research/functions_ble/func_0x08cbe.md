# func_0x08cbe

| | |
|---|---|
| offset в файле | `0x08cbe` |
| vaddr (база 0x01800000) | `0x01808cbe` |
 | размер кода | 102 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00201994 — RAM (r0)
- 0x00201bcc — RAM (r0)
- 0x00206320 — RAM (r0)
- 0x00206838 — RAM (r1)
- 0x21600002 — прочее (r8)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x01618eec (bl, вне списка функций)
- 0x0162b5d4 (bl, вне списка функций)
- 0x01808cda (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01808cbe:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  01808cc2:  ldr r0, [pc, #0x188]              (RAM)
  01808cc4:  ldrd r6, r5, [r0, #0x2c]          
  01808cc8:  ldr r7, [r0, #0x34]               
  01808cca:  movs r0, #1                       
  01808ccc:  bl #0x1618eec                     
  01808cd0:  ldr.w r8, [pc, #0x15c]            
  01808cd4:  cbz r0, #0x1808d08                
  01808cd6:  subw r4, pc, #0x5f                
  01808cda:  ldr r0, [pc, #0x174]              (RAM)
  01808cdc:  str r7, [sp]                      
  01808cde:  mov r3, r5                        
  01808ce0:  mov r2, r6                        
  01808ce2:  mov r1, r4                        
  01808ce4:  ldr r0, [r0]                      
  01808ce6:  bl #0x162b5d4                     
  01808cea:  cmp r0, #0                        
  01808cec:  beq #0x1808d20                    
  01808cee:  ldr r1, [pc, #0x148]              (RAM)
  01808cf0:  movs r0, #0                       
  01808cf2:  strb r0, [r1, #3]                 
  01808cf4:  add sp, #4                        
  01808cf6:  mov r3, r4                        
  01808cf8:  mov r0, r8                        
  01808cfa:  pop.w {r4, r5, r6, r7, r8, sb, lr}
  01808cfe:  movs r2, #1                       
  01808d00:  movw r1, #0x44a                   
  01808d04:  b.w #0x15f5b92                    
  01808d08:  ldr r0, [pc, #0x134]              (RAM)
  01808d0a:  movs r2, #1                       
  01808d0c:  movw r1, #0x44b                   
  01808d10:  ldrsb.w r3, [r0]                  
  01808d14:  mov r0, r8                        
  01808d16:  bl #0x15f5b92                     
  01808d1a:  subw r4, pc, #0x5d                
  01808d1e:  b #0x1808cda                      -> 0x08cda (вне списка функций)
  01808d20:  pop.w {r3, r4, r5, r6, r7, r8, sb, pc}
  ; --- literal-пул @0x08e30 (1 слов) — ВНЕ границ функции ---
  08e30:  .word 0x21600002
  ; --- literal-пул @0x08e38 (1 слов) — ВНЕ границ функции ---
  08e38:  .word 0x00206838  ; RAM
  ; --- literal-пул @0x08e40 (1 слов) — ВНЕ границ функции ---
  08e40:  .word 0x00201bcc  ; RAM
  ; --- literal-пул @0x08e4c (2 слов) — ВНЕ границ функции ---
  08e4c:  .word 0x00206320  ; RAM
  08e50:  .word 0x00201994  ; RAM
```
