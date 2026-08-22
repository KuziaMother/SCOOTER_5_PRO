# func_0x07d4c

| | |
|---|---|
| offset в файле | `0x07d4c` |
| vaddr (база 0x01800000) | `0x01807d4c` |
 | размер кода | 112 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202044 — RAM (r0)
- 0x00206838 — RAM (r1)
- 0x00fa0d1d — прочее (r0)

## Вызовы (callees)

- 0x01647e00 (bl, вне списка функций)
- `func_0x07d0c` (0x01807d0c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01807d4c:  push {r4, r5, r6, lr}             
  01807d4e:  sub sp, #0x18                     
  01807d50:  mov r6, r1                        
  01807d52:  mov r4, r0                        
  01807d54:  mov r5, r2                        
  01807d56:  cmp r2, #0xa                      
  01807d58:  bls #0x1807d6e                    
  01807d5a:  add sp, #0x18                     
  01807d5c:  mov r3, r2                        
  01807d5e:  pop.w {r4, r5, r6, lr}            
  01807d62:  movs r2, #2                       
  01807d64:  movw r1, #0xc89                   
  01807d68:  ldr r0, [pc, #0x39c]              
  01807d6a:  b.w #0x15f5fa4                    
  01807d6e:  ldrb r0, [r4]                     
  01807d70:  cmp r0, #0x12                     
  01807d72:  bne #0x1807dac                    
  01807d74:  cmp r6, #0x11                     
  01807d76:  bne #0x1807dac                    
  01807d78:  ldr r0, [pc, #0x390]              (RAM)
  01807d7a:  mov r2, sp                        
  01807d7c:  add.w r0, r0, r5, lsl #2          
  01807d80:  ldr.w r0, [r0, #0x210]            
  01807d84:  ldr r1, [r0, #0xde]!              
  01807d88:  str r1, [sp, #0x10]               
  01807d8a:  ldr r0, [r0, #4]                  
  01807d8c:  str r0, [sp, #0x14]               
  01807d8e:  add r1, sp, #0x10                 
  01807d90:  mov r0, r5                        
  01807d92:  bl #0x1807d0c                     -> func_0x07d0c
  01807d96:  movs r2, #0x10                    
  01807d98:  adds r1, r4, #1                   
  01807d9a:  mov r0, sp                        
  01807d9c:  bl #0x1647e00                     
  01807da0:  cbz r0, #0x1807dbc                
  01807da2:  movs r0, #0                       
  01807da4:  ldr r1, [pc, #0x368]              (RAM)
  01807da6:  strb r0, [r1, #1]                 
  01807da8:  cbz r0, #0x1807dac                
  01807daa:  movs r6, #1                       
  01807dac:  add sp, #0x18                     
  01807dae:  mov r2, r5                        
  01807db0:  mov r1, r6                        
  01807db2:  mov r0, r4                        
  01807db4:  pop.w {r4, r5, r6, lr}            
  01807db8:  b.w #0x1627420                    
  ; --- literal-пул @0x08108 (3 слов) — ВНЕ границ функции ---
  08108:  .word 0x00fa0d1d
  0810c:  .word 0x00202044  ; RAM
  08110:  .word 0x00206838  ; RAM
```
