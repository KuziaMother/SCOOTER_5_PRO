# func_0x03de4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003de4) | `0x00003de4` |
| размер кода | 252 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a84f — flash-mirror @0x1a84f (r0)
- 0x0801a863 — flash-mirror @0x1a863 (r0)
- 0x20000089 — RAM (r0)
- 0x2000008a — RAM (r0)
- 0x20000107 — RAM (r0)
- 0x200009b4 — RAM (r1)
- 0x200009b5 — RAM (r1)
- 0x20000fe7 — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x0332c` (0x0000332c, bl)
- 0x03e86 (b, вне списка функций)
- 0x03e9c (b, вне списка функций)
- 0x03ecc (b, вне списка функций)
- 0x03edc (b, вне списка функций)
- `func_0x03f00` (0x00003f00, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x03e32..0x03e34` (2 Б); цели из: 0x03e26
- `0x03e34..0x03e58` (36 Б); цели из: 0x03e14
- `0x03e58..0x03e68` (16 Б); цели из: 0x03e50
- `0x03e68..0x03e86` (30 Б); цели из: 0x03e5e
- `0x03e86..0x03e88` (2 Б); цели из: 0x03e44, 0x03e56, 0x03e66, 0x03e6e
- `0x03e88..0x03e9c` (20 Б); цели из: 0x03e18
- `0x03e9c..0x03ec8` (44 Б); цели из: 0x03e1e
- `0x03ec8..0x03ecc` (4 Б); цели из: 0x03ea8
- `0x03ecc..0x03ece` (2 Б); цели из: 0x03ec6
- `0x03ece..0x03edc` (14 Б); цели из: 0x03e1c
- `0x03edc..0x03ee0` (4 Б); цели из: 0x03e32, 0x03e86, 0x03e9a, 0x03ecc

## Дизассембляция

```asm
  03de4:  push {r4, lr}                     
  03de6:  ldr r0, [pc, #0xf8]               -> RAM
  03de8:  ldrb r0, [r0]                     
  03dea:  cbnz r0, #0x3dfe                  
  03dec:  movs r1, #0x1d                    
  03dee:  ldr r0, [pc, #0xf4]               -> RAM
  03df0:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  03df4:  movs r0, #0                       
  03df6:  ldr r1, [pc, #0xf0]               -> RAM
  03df8:  strb r0, [r1]                     
  03dfa:  ldr r1, [pc, #0xf0]               -> RAM
  03dfc:  strb r0, [r1]                     
  03dfe:  ldr r0, [pc, #0xf0]               -> RAM
  03e00:  ldrb r0, [r0]                     
  03e02:  ldr r1, [pc, #0xe0]               -> RAM
  03e04:  strb r0, [r1, #1]                 
  03e06:  ldr r0, [pc, #0xec]               -> RAM
  03e08:  ldrb r0, [r0]                     
  03e0a:  strb r0, [r1]                     
  03e0c:  ldr r0, [pc, #0xe0]               -> RAM
  03e0e:  ldrb r0, [r0]                     
  03e10:  cbz r0, #0x3e20                   
  03e12:  cmp r0, #1                        
  03e14:  beq #0x3e34                       
  03e16:  cmp r0, #2                        
  03e18:  beq #0x3e88                       
  03e1a:  cmp r0, #3                        
  03e1c:  bne #0x3ece                       
  03e1e:  b #0x3e9c                         -> 0x03e9c (вне списка функций)
  03e20:  ldr r0, [pc, #0xbc]               -> RAM
  03e22:  ldrb r0, [r0]                     
  03e24:  cmp r0, #1                        
  03e26:  bne #0x3e32                       
  03e28:  ldr r1, [pc, #0xc4]               -> RAM
  03e2a:  strb r0, [r1]                     
  03e2c:  movs r0, #0                       
  03e2e:  ldr r1, [pc, #0xb8]               -> RAM
  03e30:  strb r0, [r1]                     
  03e32:  b #0x3edc                         -> 0x03edc (вне списка функций)
  03e34:  ldr r0, [pc, #0xa8]               -> RAM
  03e36:  ldrb r0, [r0]                     
  03e38:  cbnz r0, #0x3e46                  
  03e3a:  movs r0, #0                       
  03e3c:  ldr r1, [pc, #0xb0]               -> RAM
  03e3e:  strb r0, [r1]                     
  03e40:  ldr r1, [pc, #0xa4]               -> RAM
  03e42:  strb r0, [r1]                     
  03e44:  b #0x3e86                         -> 0x03e86 (вне списка функций)
  03e46:  bl #0x3f00                        -> func_0x03f00
  03e4a:  ldr r0, [pc, #0x9c]               -> RAM
  03e4c:  ldrb r0, [r0]                     
  03e4e:  cmp r0, #3                        
  03e50:  bne #0x3e58                       
  03e52:  ldr r1, [pc, #0x9c]               -> RAM
  03e54:  strb r0, [r1]                     
  03e56:  b #0x3e86                         -> 0x03e86 (вне списка функций)
  03e58:  ldr r0, [pc, #0x8c]               -> RAM
  03e5a:  ldrb r0, [r0]                     
  03e5c:  cmp r0, #1                        
  03e5e:  bne #0x3e68                       
  03e60:  movs r0, #2                       
  03e62:  ldr r1, [pc, #0x8c]               -> RAM
  03e64:  strb r0, [r1]                     
  03e66:  b #0x3e86                         -> 0x03e86 (вне списка функций)
  03e68:  ldr r0, [pc, #0x7c]               -> RAM
  03e6a:  ldrb r0, [r0]                     
  03e6c:  cmp r0, #2                        
  03e6e:  bne #0x3e86                       
  03e70:  movs r1, #1                       
  03e72:  ldr r0, [pc, #0x84]               -> flash-mirror @0x1a863
  03e74:  bl #0x332c                        -> func_0x0332c
  03e78:  movs r1, #1                       
  03e7a:  ldr r0, [pc, #0x80]               -> flash-mirror @0x1a84f
  03e7c:  bl #0x332c                        -> func_0x0332c
  03e80:  movs r0, #1                       
  03e82:  ldr r1, [pc, #0x6c]               -> RAM
  03e84:  strb r0, [r1]                     
  03e86:  b #0x3edc                         -> 0x03edc (вне списка функций)
  03e88:  ldr r0, [pc, #0x54]               -> RAM
  03e8a:  ldrb r0, [r0]                     
  03e8c:  cbnz r0, #0x3e9a                  
  03e8e:  movs r0, #1                       
  03e90:  ldr r1, [pc, #0x5c]               -> RAM
  03e92:  strb r0, [r1]                     
  03e94:  movs r0, #0                       
  03e96:  ldr r1, [pc, #0x50]               -> RAM
  03e98:  strb r0, [r1]                     
  03e9a:  b #0x3edc                         -> 0x03edc (вне списка функций)
  03e9c:  ldr r0, [pc, #0x40]               -> RAM
  03e9e:  ldrb r0, [r0]                     
  03ea0:  cbz r0, #0x3eaa                   
  03ea2:  ldr r0, [pc, #0x44]               -> RAM
  03ea4:  ldrb r0, [r0]                     
  03ea6:  cmp r0, #2                        
  03ea8:  bne #0x3ec8                       
  03eaa:  movs r1, #1                       
  03eac:  ldr r0, [pc, #0x48]               -> flash-mirror @0x1a863
  03eae:  bl #0x332c                        -> func_0x0332c
  03eb2:  movs r1, #1                       
  03eb4:  ldr r0, [pc, #0x44]               -> flash-mirror @0x1a84f
  03eb6:  bl #0x332c                        -> func_0x0332c
  03eba:  movs r0, #1                       
  03ebc:  ldr r1, [pc, #0x30]               -> RAM
  03ebe:  strb r0, [r1]                     
  03ec0:  movs r0, #0                       
  03ec2:  ldr r1, [pc, #0x24]               -> RAM
  03ec4:  strb r0, [r1]                     
  03ec6:  b #0x3ecc                         -> 0x03ecc (вне списка функций)
  03ec8:  bl #0x3f00                        -> func_0x03f00
  03ecc:  b #0x3edc                         -> 0x03edc (вне списка функций)
  03ece:  movs r0, #1                       
  03ed0:  ldr r1, [pc, #0x1c]               -> RAM
  03ed2:  strb r0, [r1]                     
  03ed4:  movs r0, #0                       
  03ed6:  ldr r1, [pc, #0x10]               -> RAM
  03ed8:  strb r0, [r1]                     
  03eda:  nop                               
  03edc:  nop                               
  03ede:  pop {r4, pc}                      
  ; --- literal-пул @0x03ee0 (8 слов) — ВНЕ границ функции ---
  03ee0:  .word 0x20000107  ; RAM
  03ee4:  .word 0x20000fe7  ; RAM
  03ee8:  .word 0x200009b5  ; RAM
  03eec:  .word 0x200009b4  ; RAM
  03ef0:  .word 0x20000089  ; RAM
  03ef4:  .word 0x2000008a  ; RAM
  03ef8:  .word 0x0801a863  ; flash-mirror @0x1a863
  03efc:  .word 0x0801a84f  ; flash-mirror @0x1a84f
```
