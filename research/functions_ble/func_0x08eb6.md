# func_0x08eb6

| | |
|---|---|
| offset в файле | `0x08eb6` |
| vaddr (база 0x01800000) | `0x01808eb6` |
 | размер кода | 172 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200784 — RAM (r1)
- 0x00202044 — RAM (r8)
- 0x00202ad4 — RAM (r0)
- 0x00206838 — RAM (r0)
- 0x00fa1b59 — прочее (r0)

## Вызовы (callees)

- 0x015f5fa4 (bl, вне списка функций)
- 0x0161d25c (bl, вне списка функций)
- 0x0163212a (bl, вне списка функций)
- `func_0x08da0` (0x01808da0, bl)
- `func_0x08e5c` (0x01808e5c, bl)
- 0x01808f08 (b, вне списка функций)
- 0x01808f1c (b, вне списка функций)
- 0x01808f40 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01808eb6:  push.w {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01808eba:  sub sp, #0xc                      
  01808ebc:  mov r7, r1                        
  01808ebe:  ldrd fp, sl, [sp, #0x40]          
  01808ec2:  mov sb, r0                        
  01808ec4:  movs r6, #0                       
  01808ec6:  ldr.w r8, [pc, #0x39c]            (RAM)
  01808eca:  b #0x1808f40                      -> 0x08f40 (вне списка функций)
  01808ecc:  add.w r0, sb, r6                  
  01808ed0:  mov r5, r0                        
  01808ed2:  ldrb r1, [r0]                     
  01808ed4:  and r4, r1, #0xf                  
  01808ed8:  mov r2, r4                        
  01808eda:  mov r1, r7                        
  01808edc:  bl #0x1808da0                     -> func_0x08da0
  01808ee0:  ldr r0, [pc, #0x384]              (RAM)
  01808ee2:  ldrb r0, [r0, #3]                 
  01808ee4:  cbnz r0, #0x1808f44               
  01808ee6:  cmp r4, #8                        
  01808ee8:  bhi #0x1808f58                    
  01808eea:  ldr r0, [pc, #0x380]              (RAM)
  01808eec:  ldrb r0, [r0, #4]                 
  01808eee:  cbz r0, #0x1808ef8                
  01808ef0:  bl #0x163212a                     
  01808ef4:  cbz r0, #0x1808f04                
  01808ef6:  b #0x1808f08                      -> 0x08f08 (вне списка функций)
  01808ef8:  ldrb.w r0, [r8, #0x5c]            
  01808efc:  sbfx r0, r0, #6, #1               
  01808f00:  adds r0, r0, #1                   
  01808f02:  beq #0x1808f08                    
  01808f04:  cmp r4, #4                        
  01808f06:  beq #0x1808f58                    
  01808f08:  ldr r1, [pc, #0x364]              (RAM)
  01808f0a:  strd fp, sl, [sp]                 
  01808f0e:  mov r0, r5                        
  01808f10:  ldr.w r5, [r1, r4, lsl #2]        
  01808f14:  ldrd r2, r3, [sp, #0x14]          
  01808f18:  mov r1, r7                        
  01808f1a:  blx r5                            
  01808f1c:  mov r5, r0                        
  01808f1e:  cmp r4, #3                        
  01808f20:  beq #0x1808f38                    
  01808f22:  ldr r0, [pc, #0x33c]              
  01808f24:  strd r6, r5, [sp]                 
  01808f28:  mov r3, r4                        
  01808f2a:  movs r2, #4                       
  01808f2c:  movw r1, #0xca6                   
  01808f30:  adds r0, #0x50                    
  01808f32:  str r7, [sp, #8]                  
  01808f34:  bl #0x15f5fa4                     
  01808f38:  adds r0, r6, r5                   
  01808f3a:  uxth r6, r0                       
  01808f3c:  subs r0, r7, r5                   
  01808f3e:  uxth r7, r0                       
  01808f40:  cmp r7, #0                        
  01808f42:  bne #0x1808ecc                    
  01808f44:  ldrb.w r0, [r8, #0x5c]            
  01808f48:  lsls r0, r0, #0x1f                
  01808f4a:  beq #0x1808f50                    
  01808f4c:  bl #0x161d25c                     
  01808f50:  add sp, #0x1c                     
  01808f52:  movs r0, #1                       
  01808f54:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
  01808f58:  mov r0, r5                        
  01808f5a:  mov r1, r7                        
  01808f5c:  bl #0x1808e5c                     -> func_0x08e5c
  01808f60:  b #0x1808f1c                      -> 0x08f1c (вне списка функций)
  ; --- literal-пул @0x09260 (5 слов) — ВНЕ границ функции ---
  09260:  .word 0x00fa1b59
  09264:  .word 0x00202044  ; RAM
  09268:  .word 0x00206838  ; RAM
  0926c:  .word 0x00202ad4  ; RAM
  09270:  .word 0x00200784  ; RAM
```
