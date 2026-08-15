# func_0x05bc4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005bc4) | `0x00005bc4` |
| размер кода | 202 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x080199d4 — flash-mirror @0x199d4 (r0)
- 0x20000f70 — RAM (r0)
- 0x40010c00 — периферия (r0)

## Вызовы (callees)

- `func_0x0332c` (0x0000332c, bl)
- `func_0x049b8` (0x000049b8, bl)
- 0x05bf8 (b, вне списка функций)
- 0x05c32 (b, вне списка функций)
- 0x05c4e (b, вне списка функций)
- 0x05c6e (b, вне списка функций)
- 0x05c8a (b, вне списка функций)
- `func_0x087c8` (0x000087c8, bl)

## Кто вызывает (callers / xrefs)

- `func_0x110fc` (bl @0x00011120)
- `func_0x110fc` (bl @0x00011222)
- `func_0x110fc` (bl @0x00011274)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x05bf8..0x05c12` (26 Б); цели из: 0x05bf4
- `0x05c12..0x05c32` (32 Б); цели из: 0x05bcc
- `0x05c32..0x05c4c` (26 Б); цели из: 0x05c2e
- `0x05c4c..0x05c4e` (2 Б); цели из: 0x05bd0
- `0x05c4e..0x05c6e` (32 Б); цели из: 0x05bd6
- `0x05c6e..0x05c88` (26 Б); цели из: 0x05c6a
- `0x05c88..0x05c8a` (2 Б); цели из: 0x05bd4
- `0x05c8a..0x05c8e` (4 Б); цели из: 0x05c10, 0x05c4a, 0x05c4c, 0x05c86

## Дизассембляция

```asm
  05bc4:  push {r4, lr}                     
  05bc6:  mov r4, r0                        
  05bc8:  cbz r4, #0x5bd8                   
  05bca:  cmp r4, #1                        
  05bcc:  beq #0x5c12                       
  05bce:  cmp r4, #2                        
  05bd0:  beq #0x5c4c                       
  05bd2:  cmp r4, #3                        
  05bd4:  bne #0x5c88                       
  05bd6:  b #0x5c4e                         -> 0x05c4e (вне списка функций)
  05bd8:  movs r0, #2                       
  05bda:  bl #0x49b8                        -> func_0x049b8
  05bde:  movs r1, #0x10                    
  05be0:  ldr r0, [pc, #0xac]               -> flash-mirror @0x199d4
  05be2:  bl #0x332c                        -> func_0x0332c
  05be6:  mov.w r1, #0x4000                 
  05bea:  ldr r0, [pc, #0xa8]               -> периферия
  05bec:  bl #0x87c8                        -> func_0x087c8
  05bf0:  cbz r0, #0x5bf6                   
  05bf2:  movs r0, #1                       
  05bf4:  b #0x5bf8                         -> 0x05bf8 (вне списка функций)
  05bf6:  movs r0, #0                       
  05bf8:  cbz r0, #0x5c10                   
  05bfa:  ldr r0, [pc, #0x9c]               -> RAM
  05bfc:  ldrb r0, [r0, #1]                 
  05bfe:  bic r0, r0, #4                    
  05c02:  ldr r1, [pc, #0x94]               -> RAM
  05c04:  strb r0, [r1, #1]                 
  05c06:  mov.w r0, #0x4000                 
  05c0a:  ldr r1, [pc, #0x88]               -> периферия
  05c0c:  adds r1, #0x28                    
  05c0e:  str r0, [r1]                      
  05c10:  b #0x5c8a                         -> 0x05c8a (вне списка функций)
  05c12:  movs r0, #2                       
  05c14:  bl #0x49b8                        -> func_0x049b8
  05c18:  movs r1, #0x10                    
  05c1a:  ldr r0, [pc, #0x74]               -> flash-mirror @0x199d4
  05c1c:  bl #0x332c                        -> func_0x0332c
  05c20:  mov.w r1, #0x4000                 
  05c24:  ldr r0, [pc, #0x6c]               -> периферия
  05c26:  bl #0x87c8                        -> func_0x087c8
  05c2a:  cbz r0, #0x5c30                   
  05c2c:  movs r0, #1                       
  05c2e:  b #0x5c32                         -> 0x05c32 (вне списка функций)
  05c30:  movs r0, #0                       
  05c32:  cbz r0, #0x5c4a                   
  05c34:  ldr r0, [pc, #0x60]               -> RAM
  05c36:  ldrb r0, [r0, #1]                 
  05c38:  bic r0, r0, #4                    
  05c3c:  ldr r1, [pc, #0x58]               -> RAM
  05c3e:  strb r0, [r1, #1]                 
  05c40:  mov.w r0, #0x4000                 
  05c44:  ldr r1, [pc, #0x4c]               -> периферия
  05c46:  adds r1, #0x28                    
  05c48:  str r0, [r1]                      
  05c4a:  b #0x5c8a                         -> 0x05c8a (вне списка функций)
  05c4c:  b #0x5c8a                         -> 0x05c8a (вне списка функций)
  05c4e:  movs r0, #1                       
  05c50:  bl #0x49b8                        -> func_0x049b8
  05c54:  movs r1, #0x10                    
  05c56:  ldr r0, [pc, #0x38]               -> flash-mirror @0x199d4
  05c58:  bl #0x332c                        -> func_0x0332c
  05c5c:  mov.w r1, #0x4000                 
  05c60:  ldr r0, [pc, #0x30]               -> периферия
  05c62:  bl #0x87c8                        -> func_0x087c8
  05c66:  cbz r0, #0x5c6c                   
  05c68:  movs r0, #1                       
  05c6a:  b #0x5c6e                         -> 0x05c6e (вне списка функций)
  05c6c:  movs r0, #0                       
  05c6e:  cbz r0, #0x5c86                   
  05c70:  ldr r0, [pc, #0x24]               -> RAM
  05c72:  ldrb r0, [r0, #1]                 
  05c74:  bic r0, r0, #4                    
  05c78:  ldr r1, [pc, #0x1c]               -> RAM
  05c7a:  strb r0, [r1, #1]                 
  05c7c:  mov.w r0, #0x4000                 
  05c80:  ldr r1, [pc, #0x10]               -> периферия
  05c82:  adds r1, #0x28                    
  05c84:  str r0, [r1]                      
  05c86:  b #0x5c8a                         -> 0x05c8a (вне списка функций)
  05c88:  nop                               
  05c8a:  nop                               
  05c8c:  pop {r4, pc}                      
  ; --- literal-пул @0x05c90 (3 слов) — ВНЕ границ функции ---
  05c90:  .word 0x080199d4  ; flash-mirror @0x199d4
  05c94:  .word 0x40010c00  ; периферия
  05c98:  .word 0x20000f70  ; RAM
```
