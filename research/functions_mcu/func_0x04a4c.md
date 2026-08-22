# func_0x04a4c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004a4c) | `0x00004a4c` |
| размер кода | 160 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000128 — RAM (r1)
- 0x2000012c — RAM (r0)
- 0x20000130 — RAM (r2)
- 0x20000134 — RAM (r1)
- 0x20000138 — RAM (r3)
- 0x2000013c — RAM (r1)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x04a04` (0x00004a04, bl)
- 0x04ae8 (b, вне списка функций)
- 0x0a6b0 (bl, вне списка функций)
- `func_0x131fc` (0x000131fc, bl)
- `func_0x15a60` (0x00015a60, bl)
- `func_0x15b84` (0x00015b84, bl)
- `func_0x15c94` (0x00015c94, bl)

## Кто вызывает (callers / xrefs)

- `func_0x04b04` (bl @0x00004b18)


## Дизассембляция

```asm
  04a4c:  push {r4, r5, lr}                 
  04a4e:  sub sp, #0x9c                     
  04a50:  mov r5, r0                        
  04a52:  mov r4, r1                        
  04a54:  movs r1, #0x98                    
  04a56:  add r0, sp, #4                    
  04a58:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  04a5c:  movs r0, #0                       
  04a5e:  str r0, [sp]                      
  04a60:  bl #0x4a04                        -> func_0x04a04
  04a64:  ldrb r1, [r4]                     
  04a66:  adds r0, r4, #2                   
  04a68:  bl #0x15a60                       -> func_0x15a60
  04a6c:  cmp r0, #1                        
  04a6e:  bne #0x4a9a                       
  04a70:  bl #0x15b84                       -> func_0x15b84
  04a74:  cmp r0, #1                        
  04a76:  bne #0x4ae8                       
  04a78:  mov r1, sp                        
  04a7a:  add r0, sp, #4                    
  04a7c:  bl #0x15c94                       -> func_0x15c94
  04a80:  ldrb.w r2, [sp]                   
  04a84:  add r1, sp, #4                    
  04a86:  mov r0, r5                        
  04a88:  bl #0x131fc                       -> func_0x131fc
  04a8c:  movs r0, #1                       
  04a8e:  ldr r1, [pc, #0x5c]               -> RAM
  04a90:  strb r0, [r1]                     
  04a92:  movs r0, #0                       
  04a94:  ldr r1, [pc, #0x58]               -> RAM
  04a96:  strb r0, [r1]                     
  04a98:  b #0x4ae8                         -> 0x04ae8 (вне списка функций)
  04a9a:  mov r0, r4                        
  04a9c:  bl #0xa6b0                        -> 0x0a6b0 (вне списка функций)
  04aa0:  cmp r0, #1                        
  04aa2:  bne #0x4ae8                       
  04aa4:  ldr r0, [pc, #0x4c]               -> RAM
  04aa6:  ldr r1, [r0]                      
  04aa8:  mov r0, r4                        
  04aaa:  ldr r2, [pc, #0x4c]               -> RAM
  04aac:  ldr r2, [r2]                      
  04aae:  blx r2                            
  04ab0:  cmp r0, #1                        
  04ab2:  bne #0x4ae8                       
  04ab4:  ldr r0, [pc, #0x3c]               -> RAM
  04ab6:  ldr r0, [r0]                      
  04ab8:  ldr r1, [pc, #0x40]               -> RAM
  04aba:  ldr r1, [r1]                      
  04abc:  blx r1                            
  04abe:  cmp r0, #1                        
  04ac0:  bne #0x4ae8                       
  04ac2:  mov r2, sp                        
  04ac4:  add r1, sp, #4                    
  04ac6:  ldr r0, [pc, #0x2c]               -> RAM
  04ac8:  ldr r0, [r0]                      
  04aca:  ldr r3, [pc, #0x34]               -> RAM
  04acc:  ldr r3, [r3]                      
  04ace:  blx r3                            
  04ad0:  ldrb.w r2, [sp]                   
  04ad4:  add r1, sp, #4                    
  04ad6:  mov r0, r5                        
  04ad8:  bl #0x131fc                       -> func_0x131fc
  04adc:  movs r0, #1                       
  04ade:  ldr r1, [pc, #0xc]                -> RAM
  04ae0:  strb r0, [r1]                     
  04ae2:  movs r0, #0                       
  04ae4:  ldr r1, [pc, #8]                  -> RAM
  04ae6:  strb r0, [r1]                     
  04ae8:  add sp, #0x9c                     
  04aea:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x04aec (6 слов) — ВНЕ границ функции ---
  04aec:  .word 0x20000128  ; RAM
  04af0:  .word 0x2000013c  ; RAM
  04af4:  .word 0x2000012c  ; RAM
  04af8:  .word 0x20000130  ; RAM
  04afc:  .word 0x20000134  ; RAM
  04b00:  .word 0x20000138  ; RAM
```
