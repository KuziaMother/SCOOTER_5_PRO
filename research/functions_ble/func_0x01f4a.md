# func_0x01f4a

| | |
|---|---|
| offset в файле | `0x01f4a` |
| vaddr (база 0x01800000) | `0x01801f4a` |
 | размер кода | 110 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005c4 — RAM (r5)
- 0x00206958 — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01801f4a:  push.w {r4, r5, r6, r7, r8, lr}   
  01801f4e:  ldr r0, [pc, #0xbc]               (RAM)
  01801f50:  ldr r5, [r0, #4]                  
  01801f52:  ldrb r0, [r5, #2]                 
  01801f54:  lsls r1, r0, #0x1f                
  01801f56:  bne #0x1801fb0                    
  01801f58:  lsls r0, r0, #0x19                
  01801f5a:  bpl #0x1801fb0                    
  01801f5c:  movs r4, #0                       
  01801f5e:  movs r1, #0x1c                    
  01801f60:  movs r3, #0x1f                    
  01801f62:  mov r0, r4                        
  01801f64:  movs r6, #1                       
  01801f66:  lsl.w r2, r6, r0                  
  01801f6a:  tst r2, r3                        
  01801f6c:  beq #0x1801f8e                    
  01801f6e:  add.w r2, r5, r0, lsr #1          
  01801f72:  and r7, r0, #1                    
  01801f76:  ldrb.w r2, [r2, #0x50]            
  01801f7a:  rsb.w r7, r7, #1                  
  01801f7e:  lsls r7, r7, #2                   
  01801f80:  lsrs r2, r7                       
  01801f82:  and r2, r2, #0xf                  
  01801f86:  lsls r2, r1                       
  01801f88:  orrs r4, r2                       
  01801f8a:  subs r1, r1, #4                   
  01801f8c:  uxtb r1, r1                       
  01801f8e:  adds r0, r0, #1                   
  01801f90:  uxtb r0, r0                       
  01801f92:  cmp r0, #8                        
  01801f94:  blo #0x1801f66                    
  01801f96:  ldr r5, [pc, #0x88]               (RAM)
  01801f98:  movs r2, #1                       
  01801f9a:  movs r1, #0x62                    
  01801f9c:  ldr r6, [r5]                      
  01801f9e:  uxth r3, r4                       
  01801fa0:  movs r0, #3                       
  01801fa2:  blx r6                            
  01801fa4:  lsrs r3, r4, #0x10                
  01801fa6:  movs r2, #1                       
  01801fa8:  movs r1, #0x63                    
  01801faa:  ldr r4, [r5]                      
  01801fac:  movs r0, #3                       
  01801fae:  blx r4                            
  01801fb0:  pop.w {r4, r5, r6, r7, r8, lr}    
  01801fb4:  b.w #0x1802db6                    
  ; --- literal-пул @0x0200c (1 слов) — ВНЕ границ функции ---
  0200c:  .word 0x00206958  ; RAM
  ; --- literal-пул @0x02020 (1 слов) — ВНЕ границ функции ---
  02020:  .word 0x002005c4  ; RAM
```
