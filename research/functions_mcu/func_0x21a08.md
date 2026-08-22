# func_0x21a08

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080021a08) | `0x00021a08` |
| размер кода | 240 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801f400 — flash-mirror @0x1f400 (r6)
- 0x0801f800 — flash-mirror @0x1f800 (r7)
- 0x20000170 — RAM (r6)
- 0x200001e8 — RAM (r4)
- 0x200001ea — RAM (r0)
- 0x200001ec — RAM (r5)
- 0x200001ee — RAM (r7)
- 0x20000241 — RAM (r5)
- 0x20000242 — RAM (r1)
- 0x20000844 — RAM (r4)
- 0x40012c40 — периферия (r0)

## Вызовы (callees)

- `func_0x221a4` (0x000221a4, bl)
- `func_0x221e6` (0x000221e6, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x21a84..0x21aa4` (32 Б); цели из: 0x21a72
- `0x21aa4..0x21abc` (24 Б); цели из: 0x21a12, 0x21a1a
- `0x21abc..0x21af6` (58 Б); цели из: 0x21ab2
- `0x21af6..0x21af8` (2 Б); цели из: 0x21aba, 0x21ac2

## Дизассембляция

```asm
  21a08:  push {r3, r4, r5, r6, r7, lr}     
  21a0a:  ldr r6, [pc, #0xec]               -> RAM
  21a0c:  movs r5, #0                       
  21a0e:  ldrb r0, [r6]                     
  21a10:  cmp r0, #1                        
  21a12:  bne #0x21aa4                      
  21a14:  ldr r0, [pc, #0xe4]               -> периферия
  21a16:  ldr r0, [r0, #0x14]               
  21a18:  lsls r0, r0, #0x10                
  21a1a:  bmi #0x21aa4                      
  21a1c:  ldr r7, [pc, #0xe0]               -> flash-mirror @0x1f800
  21a1e:  mov r0, r7                        
  21a20:  bl #0x221a4                       -> func_0x221a4
  21a24:  ldr r4, [pc, #0xdc]               -> RAM
  21a26:  lsls r0, r5, #2                   
  21a28:  ldrb r1, [r4, r5]                 
  21a2a:  adds r0, r0, r7                   
  21a2c:  bl #0x221e6                       -> func_0x221e6
  21a30:  adds r5, r5, #1                   
  21a32:  uxtb r5, r5                       
  21a34:  cmp r5, #7                        
  21a36:  blo #0x21a26                      
  21a38:  ldr r7, [pc, #0xc4]               -> flash-mirror @0x1f800
  21a3a:  movs r5, #0                       
  21a3c:  adds r7, #0x1c                    
  21a3e:  adds r0, r4, r5                   
  21a40:  ldrb r1, [r0, #7]                 
  21a42:  lsls r0, r5, #2                   
  21a44:  adds r0, r0, r7                   
  21a46:  bl #0x221e6                       -> func_0x221e6
  21a4a:  adds r5, r5, #1                   
  21a4c:  uxtb r5, r5                       
  21a4e:  cmp r5, #0x12                     
  21a50:  blo #0x21a3e                      
  21a52:  ldr r7, [pc, #0xac]               -> flash-mirror @0x1f800
  21a54:  movs r5, #0                       
  21a56:  adds r7, #0x64                    
  21a58:  adds r0, r4, r5                   
  21a5a:  ldrb r1, [r0, #0x19]              
  21a5c:  lsls r0, r5, #2                   
  21a5e:  adds r0, r0, r7                   
  21a60:  bl #0x221e6                       -> func_0x221e6
  21a64:  adds r5, r5, #1                   
  21a66:  uxtb r5, r5                       
  21a68:  cmp r5, #0x14                     
  21a6a:  blo #0x21a58                      
  21a6c:  ldr r5, [pc, #0x98]               -> RAM
  21a6e:  ldrb r0, [r5]                     
  21a70:  cmp r0, #1                        
  21a72:  bne #0x21a84                      
  21a74:  ldr r0, [pc, #0x88]               -> flash-mirror @0x1f800
  21a76:  movs r1, #1                       
  21a78:  adds r0, #0xb4                    
  21a7a:  bl #0x221e6                       -> func_0x221e6
  21a7e:  ldr r1, [pc, #0x8c]               -> RAM
  21a80:  ldrb r0, [r5]                     
  21a82:  strb r0, [r1]                     
  21a84:  ldr r7, [pc, #0x78]               -> flash-mirror @0x1f800
  21a86:  movs r5, #0                       
  21a88:  adds r7, #0xb8                    
  21a8a:  adds r0, r4, r5                   
  21a8c:  adds r0, #0x20                    
  21a8e:  ldrb r1, [r0, #0xd]               
  21a90:  lsls r0, r5, #2                   
  21a92:  adds r0, r0, r7                   
  21a94:  bl #0x221e6                       -> func_0x221e6
  21a98:  adds r5, r5, #1                   
  21a9a:  uxtb r5, r5                       
  21a9c:  cmp r5, #0x10                     
  21a9e:  blo #0x21a8a                      
  21aa0:  movs r0, #0                       
  21aa2:  strb r0, [r6]                     
  21aa4:  ldr r4, [pc, #0x68]               -> RAM
  21aa6:  ldr r0, [pc, #0x6c]               -> RAM
  21aa8:  ldrh r1, [r4]                     
  21aaa:  ldrh r0, [r0]                     
  21aac:  ldr r7, [pc, #0x68]               -> RAM
  21aae:  ldr r5, [pc, #0x6c]               -> RAM
  21ab0:  cmp r1, r0                        
  21ab2:  bne #0x21abc                      
  21ab4:  ldrh r0, [r5]                     
  21ab6:  ldrh r1, [r7]                     
  21ab8:  cmp r0, r1                        
  21aba:  beq #0x21af6                      
  21abc:  ldr r0, [pc, #0x3c]               -> периферия
  21abe:  ldr r0, [r0, #0x14]               
  21ac0:  lsls r0, r0, #0x10                
  21ac2:  bmi #0x21af6                      
  21ac4:  ldr r6, [pc, #0x58]               -> flash-mirror @0x1f400
  21ac6:  mov r0, r6                        
  21ac8:  bl #0x221a4                       -> func_0x221a4
  21acc:  cmp r0, #0                        
  21ace:  bne #0x21ac6                      
  21ad0:  ldrh r1, [r4]                     
  21ad2:  mov r0, r6                        
  21ad4:  bl #0x221e6                       -> func_0x221e6
  21ad8:  cmp r0, #0                        
  21ada:  bne #0x21ad0                      
  21adc:  ldr r6, [pc, #0x40]               -> flash-mirror @0x1f400
  21ade:  adds r6, r6, #4                   
  21ae0:  ldrh r1, [r5]                     
  21ae2:  mov r0, r6                        
  21ae4:  bl #0x221e6                       -> func_0x221e6
  21ae8:  cmp r0, #0                        
  21aea:  bne #0x21ae0                      
  21aec:  ldr r0, [pc, #0x24]               -> RAM
  21aee:  ldrh r1, [r4]                     
  21af0:  strh r1, [r0]                     
  21af2:  ldrh r0, [r5]                     
  21af4:  strh r0, [r7]                     
  21af6:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x21af8 (11 слов) — ВНЕ границ функции ---
  21af8:  .word 0x20000170  ; RAM
  21afc:  .word 0x40012c40  ; периферия
  21b00:  .word 0x0801f800  ; flash-mirror @0x1f800
  21b04:  .word 0x20000844  ; RAM
  21b08:  .word 0x20000241  ; RAM
  21b0c:  .word 0x20000242  ; RAM
  21b10:  .word 0x200001e8  ; RAM
  21b14:  .word 0x200001ea  ; RAM
  21b18:  .word 0x200001ee  ; RAM
  21b1c:  .word 0x200001ec  ; RAM
  21b20:  .word 0x0801f400  ; flash-mirror @0x1f400
```
