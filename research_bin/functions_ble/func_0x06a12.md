# func_0x06a12

| | |
|---|---|
| offset в файле | `0x06a12` |
| vaddr (база 0x01800000) | `0x01806a12` |
 | размер кода | 170 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0003ffff — прочее (r0)
- 0x002005b0 — RAM (r2)
- 0x00202044 — RAM (r7)

## Вызовы (callees)

- 0x01618366 (bl, вне списка функций)
- 0x0161fba2 (bl, вне списка функций)
- 0x01806978 (b, вне списка функций)
- `func_0x0697c` (0x0180697c, bl)
- 0x01806a9e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x06ae6` (bl @0x01806c9c)

## Дизассембляция

```asm
  01806a12:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  01806a16:  movs r6, #0                       
  01806a18:  mov r4, r0                        
  01806a1a:  str r6, [r0]                      
  01806a1c:  ldrb r0, [r0, #0xe]               
  01806a1e:  mov r8, r1                        
  01806a20:  cmp r0, #0xf                      
  01806a22:  beq #0x1806ab8                    
  01806a24:  ldr r7, [pc, #0x18c]              (RAM)
  01806a26:  ldr r2, [pc, #0x1bc]              (RAM)
  01806a28:  add.w r0, r7, r0, lsl #4          
  01806a2c:  movs r1, #0                       
  01806a2e:  ldr.w r5, [r0, #0x2bc]            
  01806a32:  ldr r2, [r2]                      
  01806a34:  mov r0, sp                        
  01806a36:  blx r2                            
  01806a38:  ldr r0, [sp]                      
  01806a3a:  movs r2, #0xa                     
  01806a3c:  ubfx r0, r0, #1, #0x12            
  01806a40:  mov r1, r5                        
  01806a42:  str r0, [sp]                      
  01806a44:  bl #0x1618366                     
  01806a48:  mov r5, r0                        
  01806a4a:  ldr r0, [sp]                      
  01806a4c:  str r0, [r4]                      
  01806a4e:  ldrb r0, [r4, #0xf]               
  01806a50:  cmp r0, #2                        
  01806a52:  beq #0x1806a5a                    
  01806a54:  ldr r0, [pc, #0x190]              
  01806a56:  cmp r5, r0                        
  01806a58:  bne #0x1806a5c                    
  01806a5a:  movs r5, #0                       
  01806a5c:  ldrb r0, [r4, #0xe]               
  01806a5e:  ldrb.w r1, [r7, #0x2aa]           
  01806a62:  cmp r0, r1                        
  01806a64:  bne #0x1806a6e                    
  01806a66:  bl #0x180697c                     -> func_0x0697c
  01806a6a:  cmp r0, r5                        
  01806a6c:  blo #0x1806ab8                    
  01806a6e:  ldrb r0, [r4, #0xe]               
  01806a70:  ldrb.w r2, [r7, #0x2aa]           
  01806a74:  ldr r3, [pc, #0x13c]              (RAM)
  01806a76:  cmp r0, r2                        
  01806a78:  add.w r1, r3, r8, lsl #4          
  01806a7c:  bne #0x1806a8e                    
  01806a7e:  ldrsh.w r3, [r1, #0x2b4]          
  01806a82:  ldrsh.w r1, [r7, #0x2ae]          
  01806a86:  adds r1, r1, #1                   
  01806a88:  cmp r3, r1                        
  01806a8a:  bgt #0x1806ab8                    
  01806a8c:  b #0x1806a9e                      -> 0x06a9e (вне списка функций)
  01806a8e:  add.w r3, r7, r0, lsl #4          
  01806a92:  ldrsh.w r1, [r1, #0x2b6]          
  01806a96:  ldrsh.w r3, [r3, #0x2b6]          
  01806a9a:  cmp r1, r3                        
  01806a9c:  bgt #0x1806ab8                    
  01806a9e:  movs r6, #1                       
  01806aa0:  cmp r2, r0                        
  01806aa2:  beq #0x1806aaa                    
  01806aa4:  movs r0, #0xf                     
  01806aa6:  strb.w r0, [r7, #0x2aa]           
  01806aaa:  movs r0, #1                       
  01806aac:  strb.w r0, [r7, #0x2ab]           
  01806ab0:  mov r1, r0                        
  01806ab2:  movs r0, #0xf                     
  01806ab4:  bl #0x161fba2                     
  01806ab8:  mov r0, r6                        
  01806aba:  b #0x1806978                      -> 0x06978 (вне списка функций)
  ; --- literal-пул @0x06bb4 (1 слов) — ВНЕ границ функции ---
  06bb4:  .word 0x00202044  ; RAM
  ; --- literal-пул @0x06be4 (2 слов) — ВНЕ границ функции ---
  06be4:  .word 0x002005b0  ; RAM
  06be8:  .word 0x0003ffff
```
