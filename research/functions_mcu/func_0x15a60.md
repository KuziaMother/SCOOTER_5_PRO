# func_0x15a60

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015a60) | `0x00015a60` |
| размер кода | 280 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a93c — flash-mirror @0x1a93c (r2)
- 0x20001f10 — RAM (r0)
- 0x20001fac — RAM (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- 0x011ec (bl, вне списка функций)
- 0x011fa (bl, вне списка функций)
- `func_0x03b82` (0x00003b82, bl)
- 0x15a7a (b, вне списка функций)
- 0x15ac4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04a4c` (bl @0x00004a68)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x15a7e..0x15ac4` (70 Б); цели из: 0x15a76
- `0x15ac4..0x15ac8` (4 Б); цели из: 0x15a84
- `0x15ac8..0x15ae8` (32 Б); цели из: 0x15a80
- `0x15ae8..0x15b32` (74 Б); цели из: 0x15ae2
- `0x15b32..0x15b6a` (56 Б); цели из: 0x15b2c
- `0x15b6a..0x15b6e` (4 Б); цели из: 0x15b5e
- `0x15b6e..0x15b78` (10 Б); цели из: 0x15b68

## Дизассембляция

```asm
  15a60:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  15a64:  mov r4, r0                        
  15a66:  mov r6, r1                        
  15a68:  movs r7, #0                       
  15a6a:  mov.w r8, #0xaa                   
  15a6e:  movs r5, #0                       
  15a70:  mov.w sb, #0xbb                   
  15a74:  cmp r6, #0xff                     
  15a76:  ble #0x15a7e                      
  15a78:  movs r0, #0                       
  15a7a:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
  15a7e:  cmp r6, #0x32                     
  15a80:  bgt #0x15ac8                      
  15a82:  movs r7, #0                       
  15a84:  b #0x15ac4                        -> 0x15ac4 (вне списка функций)
  15a86:  add.w r1, r7, r7, lsl #3          
  15a8a:  add.w r1, r1, r7, lsl #4          
  15a8e:  ldr r2, [pc, #0xe8]               -> flash-mirror @0x1a93c
  15a90:  add.w r0, r2, r1, lsl #1          
  15a94:  bl #0x11ec                        -> 0x011ec (вне списка функций)
  15a98:  mov sl, r0                        
  15a9a:  add.w r0, r7, r7, lsl #3          
  15a9e:  add.w r0, r0, r7, lsl #4          
  15aa2:  ldr r2, [pc, #0xd4]               -> flash-mirror @0x1a93c
  15aa4:  add.w r1, r2, r0, lsl #1          
  15aa8:  mov r2, sl                        
  15aaa:  mov r0, r4                        
  15aac:  bl #0x11fa                        -> 0x011fa (вне списка функций)
  15ab0:  cbnz r0, #0x15ac0                 
  15ab2:  movs r0, #0                       
  15ab4:  ldr r1, [pc, #0xc4]               -> RAM
  15ab6:  strb r0, [r1, #1]                 
  15ab8:  mov r0, r1                        
  15aba:  strb r7, [r0, #2]                 
  15abc:  movs r0, #1                       
  15abe:  b #0x15a7a                        -> 0x15a7a (вне списка функций)
  15ac0:  adds r0, r7, #1                   
  15ac2:  uxtb r7, r0                       
  15ac4:  cmp r7, #7                        
  15ac6:  blt #0x15a86                      
  15ac8:  movs r1, #0x9c                    
  15aca:  ldr r0, [pc, #0xb4]               -> RAM
  15acc:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  15ad0:  mov r0, r5                        
  15ad2:  adds r1, r5, #1                   
  15ad4:  uxth r5, r1                       
  15ad6:  ldrb r0, [r4, r0]                 
  15ad8:  ldr r1, [pc, #0xa4]               -> RAM
  15ada:  strb r0, [r1]                     
  15adc:  mov r0, r1                        
  15ade:  ldrb r0, [r0]                     
  15ae0:  cmp r0, #1                        
  15ae2:  beq #0x15ae8                      
  15ae4:  movs r0, #0                       
  15ae6:  b #0x15a7a                        -> 0x15a7a (вне списка функций)
  15ae8:  mov r0, r5                        
  15aea:  adds r1, r5, #1                   
  15aec:  uxth r5, r1                       
  15aee:  ldrb r0, [r4, r0]                 
  15af0:  ldr r1, [pc, #0x8c]               -> RAM
  15af2:  strb r0, [r1, #1]                 
  15af4:  mov r0, r5                        
  15af6:  adds r1, r5, #1                   
  15af8:  uxth r5, r1                       
  15afa:  ldrb r0, [r4, r0]                 
  15afc:  ldr r1, [pc, #0x80]               -> RAM
  15afe:  strb r0, [r1, #2]                 
  15b00:  subs r0, r6, r5                   
  15b02:  adds r0, r0, #1                   
  15b04:  ldrb r0, [r4, r0]                 
  15b06:  mov.w r1, #0xff00                 
  15b0a:  and.w r0, r1, r0, lsl #8          
  15b0e:  subs r1, r6, r5                   
  15b10:  adds r1, r1, #2                   
  15b12:  ldrb r1, [r4, r1]                 
  15b14:  orrs r0, r1                       
  15b16:  ldr r1, [pc, #0x68]               -> RAM
  15b18:  strh.w r0, [r1, #0x9a]            
  15b1c:  subs r0, r6, #2                   
  15b1e:  subs r0, r0, r5                   
  15b20:  strb.w r0, [r1, #0x99]            
  15b24:  mov r0, r1                        
  15b26:  ldrb.w r0, [r0, #0x99]            
  15b2a:  cmp r0, #0x96                     
  15b2c:  blt #0x15b32                      
  15b2e:  movs r0, #0                       
  15b30:  b #0x15a7a                        -> 0x15a7a (вне списка функций)
  15b32:  ldr r0, [pc, #0x4c]               -> RAM
  15b34:  ldrb.w r2, [r0, #0x99]            
  15b38:  adds r1, r4, r5                   
  15b3a:  adds r0, r0, #3                   
  15b3c:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  15b40:  ldr r0, [pc, #0x3c]               -> RAM
  15b42:  ldrb.w r1, [r0, #0x99]            
  15b46:  adds r0, r0, #3                   
  15b48:  bl #0x3b82                        -> func_0x03b82
  15b4c:  mov r8, r0                        
  15b4e:  ldr r0, [pc, #0x30]               -> RAM
  15b50:  ldrb r0, [r0, #2]                 
  15b52:  mvns r0, r0                       
  15b54:  and sb, r0, #0xff                 
  15b58:  ldr r0, [pc, #0x24]               -> RAM
  15b5a:  ldrb r0, [r0, #1]                 
  15b5c:  cmp r0, sb                        
  15b5e:  bne #0x15b6a                      
  15b60:  ldr r0, [pc, #0x1c]               -> RAM
  15b62:  ldrh.w r0, [r0, #0x9a]            
  15b66:  cmp r0, r8                        
  15b68:  beq #0x15b6e                      
  15b6a:  movs r0, #0                       
  15b6c:  b #0x15a7a                        -> 0x15a7a (вне списка функций)
  15b6e:  movs r0, #1                       
  15b70:  ldr r1, [pc, #8]                  -> RAM
  15b72:  strb r0, [r1, #1]                 
  15b74:  nop                               
  15b76:  b #0x15a7a                        -> 0x15a7a (вне списка функций)
  ; --- literal-пул @0x15b78 (3 слов) — ВНЕ границ функции ---
  15b78:  .word 0x0801a93c  ; flash-mirror @0x1a93c
  15b7c:  .word 0x20001fac  ; RAM
  15b80:  .word 0x20001f10  ; RAM
```
