# func_0x0fbf8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000fbf8) | `0x0000fbf8` |
| размер кода | 190 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019daa — flash-mirror @0x19daa (r1)
- 0x20000080 — RAM (r0)
- 0x200009e0 — RAM (r0)
- 0x200009e2 — RAM (r1)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)

## Вызовы (callees)

- 0x0fc4c (b, вне списка функций)
- 0x0fcb4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11998` (bl @0x0001199a)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0fc46..0x0fc4c` (6 Б); цели из: 0x0fc1a
- `0x0fc4c..0x0fc7a` (46 Б); цели из: 0x0fc04, 0x0fc2e, 0x0fc44
- `0x0fc7a..0x0fcae` (52 Б); цели из: 0x0fc5c, 0x0fc64
- `0x0fcae..0x0fcb4` (6 Б); цели из: 0x0fc84
- `0x0fcb4..0x0fcb6` (2 Б); цели из: 0x0fc78, 0x0fc98, 0x0fcac

## Дизассембляция

```asm
  0fbf8:  ldr r0, [pc, #0xbc]               -> RAM
  0fbfa:  ldrb r0, [r0]                     
  0fbfc:  cbz r0, #0xfc06                   
  0fbfe:  ldr r0, [pc, #0xb8]               -> RAM
  0fc00:  ldrb r0, [r0]                     
  0fc02:  cmp r0, #2                        
  0fc04:  bne #0xfc4c                       
  0fc06:  ldr r0, [pc, #0xb4]               -> RAM
  0fc08:  ldrb r0, [r0, #0xc]               
  0fc0a:  and r0, r0, #1                    
  0fc0e:  cbnz r0, #0xfc4c                  
  0fc10:  ldr r0, [pc, #0xa8]               -> RAM
  0fc12:  ldrh r0, [r0, #8]                 
  0fc14:  ldr r1, [pc, #0xa8]               -> flash-mirror @0x19daa
  0fc16:  ldrh r1, [r1]                     
  0fc18:  cmp r0, r1                        
  0fc1a:  blt #0xfc46                       
  0fc1c:  ldr r0, [pc, #0xa4]               -> RAM
  0fc1e:  ldrh r0, [r0]                     
  0fc20:  adds r0, r0, #1                   
  0fc22:  ldr r1, [pc, #0xa0]               -> RAM
  0fc24:  strh r0, [r1]                     
  0fc26:  ldr r0, [pc, #0x98]               -> flash-mirror @0x19daa
  0fc28:  ldrh r0, [r0, #4]                 
  0fc2a:  ldrh r1, [r1]                     
  0fc2c:  cmp r0, r1                        
  0fc2e:  bgt #0xfc4c                       
  0fc30:  ldr r0, [pc, #0x88]               -> RAM
  0fc32:  ldrb r0, [r0, #0xc]               
  0fc34:  bic r0, r0, #1                    
  0fc38:  adds r0, r0, #1                   
  0fc3a:  ldr r1, [pc, #0x80]               -> RAM
  0fc3c:  strb r0, [r1, #0xc]               
  0fc3e:  movs r0, #0                       
  0fc40:  ldr r1, [pc, #0x80]               -> RAM
  0fc42:  strh r0, [r1]                     
  0fc44:  b #0xfc4c                         -> 0x0fc4c (вне списка функций)
  0fc46:  movs r0, #0                       
  0fc48:  ldr r1, [pc, #0x78]               -> RAM
  0fc4a:  strh r0, [r1]                     
  0fc4c:  ldr r0, [pc, #0x6c]               -> RAM
  0fc4e:  ldrb r0, [r0, #0xc]               
  0fc50:  and r0, r0, #1                    
  0fc54:  cbz r0, #0xfcac                   
  0fc56:  ldr r0, [pc, #0x60]               -> RAM
  0fc58:  ldrb r0, [r0]                     
  0fc5a:  cmp r0, #1                        
  0fc5c:  bne #0xfc7a                       
  0fc5e:  ldr r0, [pc, #0x68]               -> RAM
  0fc60:  ldr r0, [r0, #4]                  
  0fc62:  cmp r0, #0x64                     
  0fc64:  blo #0xfc7a                       
  0fc66:  ldr r0, [pc, #0x54]               -> RAM
  0fc68:  ldrb r0, [r0, #0xc]               
  0fc6a:  bic r0, r0, #1                    
  0fc6e:  ldr r1, [pc, #0x4c]               -> RAM
  0fc70:  strb r0, [r1, #0xc]               
  0fc72:  movs r0, #0                       
  0fc74:  ldr r1, [pc, #0x54]               -> RAM
  0fc76:  strh r0, [r1]                     
  0fc78:  b #0xfcb4                         -> 0x0fcb4 (вне списка функций)
  0fc7a:  ldr r0, [pc, #0x40]               -> RAM
  0fc7c:  ldrh r0, [r0, #8]                 
  0fc7e:  ldr r1, [pc, #0x40]               -> flash-mirror @0x19daa
  0fc80:  ldrh r1, [r1, #2]                 
  0fc82:  cmp r0, r1                        
  0fc84:  bgt #0xfcae                       
  0fc86:  ldr r0, [pc, #0x44]               -> RAM
  0fc88:  ldrh r0, [r0]                     
  0fc8a:  adds r0, r0, #1                   
  0fc8c:  ldr r1, [pc, #0x3c]               -> RAM
  0fc8e:  strh r0, [r1]                     
  0fc90:  ldr r0, [pc, #0x2c]               -> flash-mirror @0x19daa
  0fc92:  ldrh r0, [r0, #6]                 
  0fc94:  ldrh r1, [r1]                     
  0fc96:  cmp r0, r1                        
  0fc98:  bgt #0xfcb4                       
  0fc9a:  ldr r0, [pc, #0x20]               -> RAM
  0fc9c:  ldrb r0, [r0, #0xc]               
  0fc9e:  bic r0, r0, #1                    
  0fca2:  ldr r1, [pc, #0x18]               -> RAM
  0fca4:  strb r0, [r1, #0xc]               
  0fca6:  movs r0, #0                       
  0fca8:  ldr r1, [pc, #0x20]               -> RAM
  0fcaa:  strh r0, [r1]                     
  0fcac:  b #0xfcb4                         -> 0x0fcb4 (вне списка функций)
  0fcae:  movs r0, #0                       
  0fcb0:  ldr r1, [pc, #0x18]               -> RAM
  0fcb2:  strh r0, [r1]                     
  0fcb4:  bx lr                             
  ; --- literal-пул @0x0fcb8 (6 слов) — ВНЕ границ функции ---
  0fcb8:  .word 0x20000080  ; RAM
  0fcbc:  .word 0x20000f95  ; RAM
  0fcc0:  .word 0x08019daa  ; flash-mirror @0x19daa
  0fcc4:  .word 0x200009e0  ; RAM
  0fcc8:  .word 0x20000fbb  ; RAM
  0fccc:  .word 0x200009e2  ; RAM
```
