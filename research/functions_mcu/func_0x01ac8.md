# func_0x01ac8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001ac8) | `0x00001ac8` |
| размер кода | 268 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019d3e — flash-mirror @0x19d3e (r1)
- 0x08019d7e — flash-mirror @0x19d7e (r1)

## Вызовы (callees)

- 0x01af8 (b, вне списка функций)
- 0x01b12 (b, вне списка функций)
- 0x01b4a (b, вне списка функций)
- 0x01b6a (b, вне списка функций)
- 0x01b8c (b, вне списка функций)
- 0x01bae (b, вне списка функций)
- 0x01bcc (b, вне списка функций)
- `func_0x03b42` (0x00003b42, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0de0a` (bl @0x0000de52)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x01af8..0x01b12` (26 Б); цели из: 0x01aea
- `0x01b12..0x01b4a` (56 Б); цели из: 0x01b02
- `0x01b4a..0x01b6a` (32 Б); цели из: 0x01b22
- `0x01b6a..0x01b8c` (34 Б); цели из: 0x01b54
- `0x01b8c..0x01bae` (34 Б); цели из: 0x01b76
- `0x01bae..0x01bcc` (30 Б); цели из: 0x01b98
- `0x01bcc..0x01bd4` (8 Б); цели из: 0x01bb6

## Дизассембляция

```asm
  01ac8:  push.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01acc:  mov r4, r0                        
  01ace:  mov sb, r1                        
  01ad0:  movs r7, #0                       
  01ad2:  mov fp, r7                        
  01ad4:  movs r0, #0                       
  01ad6:  str r0, [sp]                      
  01ad8:  movs r6, #0                       
  01ada:  mov r8, r0                        
  01adc:  mov sl, r0                        
  01ade:  mov r1, sb                        
  01ae0:  mov r0, r4                        
  01ae2:  bl #0x3b42                        -> func_0x03b42
  01ae6:  mov r8, r0                        
  01ae8:  movs r5, #0                       
  01aea:  b #0x1af8                         -> 0x01af8 (вне списка функций)
  01aec:  ldrb r0, [r4, r5]                 
  01aee:  add r0, sl                        
  01af0:  uxth.w sl, r0                     
  01af4:  adds r0, r5, #1                   
  01af6:  uxtb r5, r0                       
  01af8:  cmp r5, sb                        
  01afa:  blt #0x1aec                       
  01afc:  eor.w r8, r8, sl                  
  01b00:  movs r5, #0                       
  01b02:  b #0x1b12                         -> 0x01b12 (вне списка функций)
  01b04:  ldrb r0, [r4, r5]                 
  01b06:  ldr r1, [pc, #0xcc]               -> flash-mirror @0x19d7e
  01b08:  ldrb r1, [r1, r5]                 
  01b0a:  eors r0, r1                       
  01b0c:  strb r0, [r4, r5]                 
  01b0e:  adds r0, r5, #1                   
  01b10:  uxtb r5, r0                       
  01b12:  cmp r5, sb                        
  01b14:  blt #0x1b04                       
  01b16:  ubfx r6, r8, #4, #2               
  01b1a:  and r0, r8, #3                    
  01b1e:  str r0, [sp]                      
  01b20:  movs r5, #0                       
  01b22:  b #0x1b4a                         -> 0x01b4a (вне списка функций)
  01b24:  ldrb r7, [r4, r5]                 
  01b26:  lsr.w fp, r7, #4                  
  01b2a:  and r7, r7, #0xf                  
  01b2e:  ldr r1, [pc, #0xa8]               -> flash-mirror @0x19d3e
  01b30:  ldr r0, [sp]                      
  01b32:  add.w r0, r1, r0, lsl #4          
  01b36:  ldrb r0, [r0, r7]                 
  01b38:  add.w r1, r1, r6, lsl #4          
  01b3c:  ldrb.w r1, [r1, fp]               
  01b40:  add.w r0, r0, r1, lsl #4          
  01b44:  strb r0, [r4, r5]                 
  01b46:  adds r0, r5, #1                   
  01b48:  uxtb r5, r0                       
  01b4a:  cmp r5, sb                        
  01b4c:  blt #0x1b24                       
  01b4e:  asr.w r0, r8, #8                  
  01b52:  lsrs r6, r0, #6                   
  01b54:  b #0x1b6a                         -> 0x01b6a (вне списка функций)
  01b56:  ldrb r7, [r4]                     
  01b58:  ldrb r0, [r4, #1]                 
  01b5a:  strb r0, [r4]                     
  01b5c:  ldrb r0, [r4, #2]                 
  01b5e:  strb r0, [r4, #1]                 
  01b60:  ldrb r0, [r4, #3]                 
  01b62:  strb r0, [r4, #2]                 
  01b64:  strb r7, [r4, #3]                 
  01b66:  subs r0, r6, #1                   
  01b68:  uxtb r6, r0                       
  01b6a:  cmp r6, #0                        
  01b6c:  bne #0x1b56                       
  01b6e:  asr.w r0, r8, #8                  
  01b72:  ubfx r6, r0, #4, #2               
  01b76:  b #0x1b8c                         -> 0x01b8c (вне списка функций)
  01b78:  ldrb r7, [r4, #4]                 
  01b7a:  ldrb r0, [r4, #5]                 
  01b7c:  strb r0, [r4, #4]                 
  01b7e:  ldrb r0, [r4, #6]                 
  01b80:  strb r0, [r4, #5]                 
  01b82:  ldrb r0, [r4, #7]                 
  01b84:  strb r0, [r4, #6]                 
  01b86:  strb r7, [r4, #7]                 
  01b88:  subs r0, r6, #1                   
  01b8a:  uxtb r6, r0                       
  01b8c:  cmp r6, #0                        
  01b8e:  bne #0x1b78                       
  01b90:  asr.w r0, r8, #8                  
  01b94:  ubfx r6, r0, #2, #2               
  01b98:  b #0x1bae                         -> 0x01bae (вне списка функций)
  01b9a:  ldrb r7, [r4, #8]                 
  01b9c:  ldrb r0, [r4, #9]                 
  01b9e:  strb r0, [r4, #8]                 
  01ba0:  ldrb r0, [r4, #0xa]               
  01ba2:  strb r0, [r4, #9]                 
  01ba4:  ldrb r0, [r4, #0xb]               
  01ba6:  strb r0, [r4, #0xa]               
  01ba8:  strb r7, [r4, #0xb]               
  01baa:  subs r0, r6, #1                   
  01bac:  uxtb r6, r0                       
  01bae:  cmp r6, #0                        
  01bb0:  bne #0x1b9a                       
  01bb2:  ubfx r6, r8, #8, #2               
  01bb6:  b #0x1bcc                         -> 0x01bcc (вне списка функций)
  01bb8:  ldrb r7, [r4, #0xc]               
  01bba:  ldrb r0, [r4, #0xd]               
  01bbc:  strb r0, [r4, #0xc]               
  01bbe:  ldrb r0, [r4, #0xe]               
  01bc0:  strb r0, [r4, #0xd]               
  01bc2:  ldrb r0, [r4, #0xf]               
  01bc4:  strb r0, [r4, #0xe]               
  01bc6:  strb r7, [r4, #0xf]               
  01bc8:  subs r0, r6, #1                   
  01bca:  uxtb r6, r0                       
  01bcc:  cmp r6, #0                        
  01bce:  bne #0x1bb8                       
  01bd0:  pop.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x01bd4 (2 слов) — ВНЕ границ функции ---
  01bd4:  .word 0x08019d7e  ; flash-mirror @0x19d7e
  01bd8:  .word 0x08019d3e  ; flash-mirror @0x19d3e
```
