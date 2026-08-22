# func_0x09d40

| | |
|---|---|
| offset в файле | `0x09d40` |
| vaddr (база 0x01800000) | `0x01809d40` |
 | размер кода | 142 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005bc — RAM (r2)
- 0x002005c4 — RAM (r4)
- 0x002005ec — RAM (r4)
- 0x00200940 — RAM (r0)
- 0x0020094c — RAM (r0)
- 0x00200950 — RAM (r0)
- 0x0020095c — RAM (r5)
- 0x002009ac — RAM (r0)
- 0x00201e10 — RAM (r0)
- 0x00202833 — RAM (r0)
- 0x00206524 — RAM (r0)
- 0x002068fc — RAM (r1)
- 0x00206958 — RAM (r6)

## Вызовы (callees)

- 0x01809d16 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01809d40:  push {r4, r5, r6, lr}             
  01809d42:  ldr r0, [pc, #0x1e0]              (RAM)
  01809d44:  ldr r0, [r0]                      
  01809d46:  blx r0                            
  01809d48:  ldr r0, [pc, #0x1dc]              (RAM)
  01809d4a:  ldr r5, [pc, #0x1e4]              (RAM)
  01809d4c:  ldrh r1, [r0]                     
  01809d4e:  ldr r0, [pc, #0x1dc]              (RAM)
  01809d50:  ldr r2, [r5]                      
  01809d52:  ldr r0, [r0]                      
  01809d54:  blx r2                            
  01809d56:  ldr r0, [pc, #0x1a8]              (RAM)
  01809d58:  subs r0, #0x7f                    
  01809d5a:  ldrb.w r0, [r0, #0x13f]           
  01809d5e:  cmp r0, #0x29                     
  01809d60:  bne #0x1809d6e                    
  01809d62:  ldr r2, [pc, #0x1d0]              (RAM)
  01809d64:  movw r1, #0x3a14                  
  01809d68:  movs r0, #0x26                    
  01809d6a:  ldr r2, [r2]                      
  01809d6c:  blx r2                            
  01809d6e:  ldr r6, [pc, #0x194]              (RAM)
  01809d70:  ldr r4, [pc, #0x1ac]              (RAM)
  01809d72:  movs r1, #0x38                    
  01809d74:  ldrb r0, [r6, #1]                 
  01809d76:  ldr r3, [r4]                      
  01809d78:  lsls r2, r0, #3                   
  01809d7a:  movs r0, #0x27                    
  01809d7c:  blx r3                            
  01809d7e:  ldrb r0, [r6]                     
  01809d80:  movw r1, #0xffff                  
  01809d84:  and.w r2, r1, r0, lsl #12         
  01809d88:  ldr r3, [r4]                      
  01809d8a:  mov.w r1, #0xf000                 
  01809d8e:  movs r0, #0x28                    
  01809d90:  blx r3                            
  01809d92:  bl #0x1809d16                     -> 0x09d16 (вне списка функций)
  01809d96:  ldr r0, [pc, #0x184]              (RAM)
  01809d98:  movs r1, #0xa                     
  01809d9a:  ldr r2, [r5]                      
  01809d9c:  subs r0, #0x64                    
  01809d9e:  blx r2                            
  01809da0:  ldr r0, [pc, #0x194]              (RAM)
  01809da2:  ldr r4, [pc, #0x198]              (RAM)
  01809da4:  movs r2, #1                       
  01809da6:  ldrh r3, [r0, #2]                 
  01809da8:  movs r1, #0x6f                    
  01809daa:  ldr r4, [r4]                      
  01809dac:  movs r0, #3                       
  01809dae:  blx r4                            
  01809db0:  ldr r1, [pc, #0x18c]              (RAM)
  01809db2:  movs r0, #0x10                    
  01809db4:  ldr r1, [r1]                      
  01809db6:  blx r1                            
  01809db8:  ldr r0, [pc, #0x188]              (RAM)
  01809dba:  ldr r0, [r0]                      
  01809dbc:  pop.w {r4, r5, r6, lr}            
  01809dc0:  bx r0                             
  01809dc2:  ldr r1, [pc, #0x17c]              (RAM)
  01809dc4:  movs r0, #4                       
  01809dc6:  ldr r1, [r1]                      
  01809dc8:  bx r1                             
  01809dca:  movs r0, #0                       
  01809dcc:  bx lr                             
  ; --- literal-пул @0x09f00 (2 слов) — ВНЕ границ функции ---
  09f00:  .word 0x00202833  ; RAM
  09f04:  .word 0x00206958  ; RAM
  ; --- literal-пул @0x09f1c (11 слов) — ВНЕ границ функции ---
  09f1c:  .word 0x00206524  ; RAM
  09f20:  .word 0x002005ec  ; RAM
  09f24:  .word 0x00200950  ; RAM
  09f28:  .word 0x00200940  ; RAM
  09f2c:  .word 0x002009ac  ; RAM
  09f30:  .word 0x0020095c  ; RAM
  09f34:  .word 0x002005bc  ; RAM
  09f38:  .word 0x00201e10  ; RAM
  09f3c:  .word 0x002005c4  ; RAM
  09f40:  .word 0x002068fc  ; RAM
  09f44:  .word 0x0020094c  ; RAM
```
