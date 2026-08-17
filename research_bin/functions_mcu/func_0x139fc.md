# func_0x139fc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800139fc) | `0x000139fc` |
| размер кода | 226 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019575 — flash-mirror @0x19575 (r1)
- 0x0801957c — flash-mirror @0x1957c (r1)
- 0x20000098 — RAM (r0)
- 0x200000d8 — RAM (r1)
- 0x200000da — RAM (r1)
- 0x200000e1 — RAM (r0)
- 0x200000e8 — RAM (r0)
- 0x200000ef — RAM (r1)
- 0x200000f0 — RAM (r0)
- 0x200000f8 — RAM (r1)
- 0x2000106e — RAM (r0)
- 0x20001077 — RAM (r0)
- 0x20001084 — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x08a90` (0x00008a90, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e1a)


## Дизассембляция

```asm
  139fc:  push {r2, r3, r4, lr}             
  139fe:  movs r0, #0                       
  13a00:  ldr r1, [pc, #0xdc]               -> RAM
  13a02:  strb r0, [r1, #1]                 
  13a04:  movs r0, #1                       
  13a06:  strb r0, [r1]                     
  13a08:  mov r0, sp                        
  13a0a:  bl #0x8a90                        -> func_0x08a90
  13a0e:  ldr r0, [pc, #0xd4]               -> RAM
  13a10:  ldr r1, [sp]                      
  13a12:  str r1, [r0]                      
  13a14:  ldrh.w r1, [sp, #4]               
  13a18:  strh r1, [r0, #4]                 
  13a1a:  ldrb.w r1, [sp, #6]               
  13a1e:  strb r1, [r0, #6]                 
  13a20:  ldrb r0, [r0, #5]                 
  13a22:  add.w r0, r0, #0x7d0              
  13a26:  lsrs r0, r0, #8                   
  13a28:  ldr r1, [pc, #0xbc]               -> RAM
  13a2a:  strb r0, [r1]                     
  13a2c:  ldr r0, [pc, #0xb4]               -> RAM
  13a2e:  ldrb r0, [r0, #5]                 
  13a30:  add.w r0, r0, #0x7d0              
  13a34:  strb r0, [r1, #1]                 
  13a36:  ldr r0, [pc, #0xac]               -> RAM
  13a38:  ldrb r1, [r0, #4]                 
  13a3a:  ldr r0, [pc, #0xac]               -> RAM
  13a3c:  ldrb r0, [r0, #2]                 
  13a3e:  bfi r0, r1, #0, #4                
  13a42:  ldr r1, [pc, #0xa4]               -> RAM
  13a44:  strb r0, [r1, #2]                 
  13a46:  ldr r0, [pc, #0x9c]               -> RAM
  13a48:  ldrb r1, [r0, #6]                 
  13a4a:  ldr r0, [pc, #0x9c]               -> RAM
  13a4c:  ldrb r0, [r0, #2]                 
  13a4e:  bfi r0, r1, #4, #4                
  13a52:  ldr r1, [pc, #0x94]               -> RAM
  13a54:  strb r0, [r1, #2]                 
  13a56:  ldr r0, [pc, #0x8c]               -> RAM
  13a58:  ldrb r0, [r0, #3]                 
  13a5a:  strb r0, [r1, #3]                 
  13a5c:  mov r0, r1                        
  13a5e:  ldrb r0, [r0, #4]                 
  13a60:  bic r0, r0, #0x80                 
  13a64:  adds r0, #0x80                    
  13a66:  strb r0, [r1, #4]                 
  13a68:  mov r0, r1                        
  13a6a:  ldrb r0, [r0, #4]                 
  13a6c:  bic r0, r0, #0x40                 
  13a70:  strb r0, [r1, #4]                 
  13a72:  ldr r0, [pc, #0x70]               -> RAM
  13a74:  ldrb r1, [r0, #2]                 
  13a76:  ldr r0, [pc, #0x70]               -> RAM
  13a78:  ldrb r0, [r0, #4]                 
  13a7a:  bfi r0, r1, #0, #6                
  13a7e:  ldr r1, [pc, #0x68]               -> RAM
  13a80:  strb r0, [r1, #4]                 
  13a82:  ldr r0, [pc, #0x60]               -> RAM
  13a84:  ldrb r0, [r0, #1]                 
  13a86:  strb r0, [r1, #5]                 
  13a88:  ldr r0, [pc, #0x58]               -> RAM
  13a8a:  ldrb r0, [r0]                     
  13a8c:  strb r0, [r1, #6]                 
  13a8e:  ldr r0, [pc, #0x5c]               -> RAM
  13a90:  ldr r1, [pc, #0x5c]               -> flash-mirror @0x19575
  13a92:  ldr r2, [r1]                      
  13a94:  str r2, [r0]                      
  13a96:  ldrh r2, [r1, #4]                 
  13a98:  strh r2, [r0, #4]                 
  13a9a:  ldrb r1, [r1, #6]                 
  13a9c:  strb r1, [r0, #6]                 
  13a9e:  ldr r0, [pc, #0x54]               -> RAM
  13aa0:  ldr r1, [pc, #0x54]               -> flash-mirror @0x1957c
  13aa2:  ldr r2, [r1]                      
  13aa4:  str r2, [r0]                      
  13aa6:  ldrh r2, [r1, #4]                 
  13aa8:  strh r2, [r0, #4]                 
  13aaa:  ldrb r1, [r1, #6]                 
  13aac:  strb r1, [r0, #6]                 
  13aae:  ldr r0, [pc, #0x4c]               -> RAM
  13ab0:  movs r1, #0                       
  13ab2:  str r1, [r0]                      
  13ab4:  str r1, [r0, #4]                  
  13ab6:  strb r1, [r0, #8]                 
  13ab8:  movs r1, #0xd                     
  13aba:  ldr r0, [pc, #0x44]               -> RAM
  13abc:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  13ac0:  movs r0, #0                       
  13ac2:  ldr r1, [pc, #0x40]               -> RAM
  13ac4:  strb r0, [r1]                     
  13ac6:  ldr r0, [pc, #0x40]               -> RAM
  13ac8:  movs r1, #0                       
  13aca:  str r1, [r0]                      
  13acc:  str r1, [r0, #4]                  
  13ace:  strh r1, [r0, #8]                 
  13ad0:  ldr r0, [pc, #0x38]               -> RAM
  13ad2:  str r1, [r0]                      
  13ad4:  str r1, [r0, #4]                  
  13ad6:  movs r0, #0                       
  13ad8:  ldr r1, [pc, #0x34]               -> RAM
  13ada:  strb r0, [r1]                     
  13adc:  pop {r2, r3, r4, pc}              
  ; --- literal-пул @0x13ae0 (13 слов) — ВНЕ границ функции ---
  13ae0:  .word 0x200000d8  ; RAM
  13ae4:  .word 0x20000098  ; RAM
  13ae8:  .word 0x200000da  ; RAM
  13aec:  .word 0x200000e1  ; RAM
  13af0:  .word 0x08019575  ; flash-mirror @0x19575
  13af4:  .word 0x200000e8  ; RAM
  13af8:  .word 0x0801957c  ; flash-mirror @0x1957c
  13afc:  .word 0x2000106e  ; RAM
  13b00:  .word 0x20001077  ; RAM
  13b04:  .word 0x200000ef  ; RAM
  13b08:  .word 0x20001084  ; RAM
  13b0c:  .word 0x200000f0  ; RAM
  13b10:  .word 0x200000f8  ; RAM
```
