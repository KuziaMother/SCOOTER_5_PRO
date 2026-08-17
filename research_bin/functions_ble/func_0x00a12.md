# func_0x00a12

| | |
|---|---|
| offset в файле | `0x00a12` |
| vaddr (база 0x01800000) | `0x01800a12` |
 | размер кода | 210 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200604 — RAM (r1)
- 0x00200b00 — RAM (r1)
- 0x00201994 — RAM (r0)
- 0x00202044 — RAM (r7)
- 0x00202d18 — RAM (sb)
- 0x00206320 — RAM (r0)
- 0x21600002 — прочее (r0)

## Вызовы (callees)

- 0x01800a5e (b, вне списка функций)
- 0x01800a7c (b, вне списка функций)
- 0x01800ac0 (b, вне списка функций)
- 0x01800aca (b, вне списка функций)
- 0x01802a50 (bl, вне списка функций)
- 0x01802adc (bl, вне списка функций)
- 0x01802ae6 (bl, вне списка функций)
- 0x01802b4a (bl, вне списка функций)
- 0x01802b54 (bl, вне списка функций)
- 0x01802b5e (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01800a12:  push.w {r2, r3, r4, r5, r6, r7, r8, sb, sl, lr}
  01800a16:  ldr.w sb, [pc, #0x318]            (RAM)
  01800a1a:  movs r6, #0                       
  01800a1c:  ldr r7, [pc, #0x30c]              (RAM)
  01800a1e:  ldrb.w r0, [sb, #4]               
  01800a22:  mov r5, r6                        
  01800a24:  mov r4, r6                        
  01800a26:  mov r8, r6                        
  01800a28:  cbz r0, #0x1800a3c                
  01800a2a:  ldr r1, [pc, #0x308]              (RAM)
  01800a2c:  movs r0, #0                       
  01800a2e:  ldr r1, [r1]                      
  01800a30:  blx r1                            
  01800a32:  movs r5, #1                       
  01800a34:  mov r8, r5                        
  01800a36:  ldrb.w r4, [sb, #0x11]            
  01800a3a:  b #0x1800a5e                      -> 0x00a5e (вне списка функций)
  01800a3c:  ldrb.w r0, [r7, #0x1b8]           
  01800a40:  lsls r0, r0, #0x1f                
  01800a42:  beq #0x1800ac4                    
  01800a44:  bl #0x1802b4a                     -> 0x02b4a (вне списка функций)
  01800a48:  cmp r0, #4                        
  01800a4a:  beq #0x1800aa8                    
  01800a4c:  ldrh.w r0, [r7, #0x1b8]           
  01800a50:  movs r5, #1                       
  01800a52:  bic r0, r0, #1                    
  01800a56:  strh.w r0, [r7, #0x1b8]           
  01800a5a:  ldrb.w r4, [r7, #0x1e2]           
  01800a5e:  add.w r0, r7, r4, lsl #2          
  01800a62:  ldr.w r0, [r0, #0x210]            
  01800a66:  ldr r0, [r0]                      
  01800a68:  lsls r0, r0, #7                   
  01800a6a:  bpl #0x1800a7c                    
  01800a6c:  movs r5, #0                       
  01800a6e:  movs r6, #0xc                     
  01800a70:  mov r2, r5                        
  01800a72:  movw r1, #0x446                   
  01800a76:  ldr r0, [pc, #0x2c0]              
  01800a78:  bl #0x1802a50                     -> 0x02a50 (вне списка функций)
  01800a7c:  add r1, sp, #4                    
  01800a7e:  movw r0, #0x200e                  
  01800a82:  bl #0x1802adc                     -> 0x02adc (вне списка функций)
  01800a86:  strb.w r6, [sp, #7]               
  01800a8a:  movs r2, #4                       
  01800a8c:  add r1, sp, #4                    
  01800a8e:  movs r0, #0xe                     
  01800a90:  bl #0x1802ae6                     -> 0x02ae6 (вне списка функций)
  01800a94:  cbz r5, #0x1800ae0                
  01800a96:  ldrh r0, [r7, #4]                 
  01800a98:  mov r3, r8                        
  01800a9a:  lsls r1, r0, #0x16                
  01800a9c:  mov.w r0, #0                      
  01800aa0:  str r0, [sp]                      
  01800aa2:  bpl #0x1800ac8                    
  01800aa4:  movs r2, #1                       
  01800aa6:  b #0x1800aca                      -> 0x00aca (вне списка функций)
  01800aa8:  ldr r0, [pc, #0x290]              (RAM)
  01800aaa:  ldr r1, [pc, #0x294]              (RAM)
  01800aac:  ldrd r2, r3, [r0, #0x1c]          
  01800ab0:  ldr r0, [r0, #0x24]               
  01800ab2:  ldr r1, [r1, #0x38]               
  01800ab4:  str r0, [sp]                      
  01800ab6:  ldr r0, [pc, #0x28c]              (RAM)
  01800ab8:  ldr r0, [r0]                      
  01800aba:  bl #0x1802b54                     -> 0x02b54 (вне списка функций)
  01800abe:  movs r0, #0x1f                    
  01800ac0:  pop.w {r2, r3, r4, r5, r6, r7, r8, sb, sl, pc}
  01800ac4:  movs r6, #0xc                     
  01800ac6:  b #0x1800a7c                      -> 0x00a7c (вне списка функций)
  01800ac8:  movs r2, #0                       
  01800aca:  movs r1, #0                       
  01800acc:  movs r0, #2                       
  01800ace:  bl #0x1802b5e                     -> 0x02b5e (вне списка функций)
  01800ad2:  ldrh.w r1, [r7, #0x1ee]           
  01800ad6:  movs r0, #1                       
  01800ad8:  lsls r0, r4                       
  01800ada:  bics r1, r0                       
  01800adc:  strh.w r1, [r7, #0x1ee]           
  01800ae0:  movs r0, #0                       
  01800ae2:  b #0x1800ac0                      -> 0x00ac0 (вне списка функций)
  ; --- literal-пул @0x00d2c (7 слов) — ВНЕ границ функции ---
  00d2c:  .word 0x00202044  ; RAM
  00d30:  .word 0x00202d18  ; RAM
  00d34:  .word 0x00200b00  ; RAM
  00d38:  .word 0x21600002
  00d3c:  .word 0x00206320  ; RAM
  00d40:  .word 0x00200604  ; RAM
  00d44:  .word 0x00201994  ; RAM
```
