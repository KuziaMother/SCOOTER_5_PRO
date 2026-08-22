# func_0x15b84

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015b84) | `0x00015b84` |
| размер кода | 236 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000c7e — RAM (r1)
- 0x20000c7f — RAM (r0)
- 0x20001fac — RAM (r0)

## Вызовы (callees)

- `func_0x158f8` (0x000158f8, bl)
- `func_0x15918` (0x00015918, bl)
- 0x15c24 (b, вне списка функций)
- 0x15c44 (b, вне списка функций)
- 0x15c5e (b, вне списка функций)
- 0x15c6c (b, вне списка функций)
- `func_0x15d14` (0x00015d14, bl)
- `func_0x15df4` (0x00015df4, bl)
- `func_0x15f00` (0x00015f00, bl)
- 0x15fc8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04a4c` (bl @0x00004a70)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x15bb0..0x15bc0` (16 Б); цели из: 0x15ba6
- `0x15bc0..0x15bd6` (22 Б); цели из: 0x15bb6
- `0x15bd6..0x15be6` (16 Б); цели из: 0x15bc6
- `0x15be6..0x15bf6` (16 Б); цели из: 0x15bdc
- `0x15bf6..0x15c06` (16 Б); цели из: 0x15bec
- `0x15c06..0x15c0e` (8 Б); цели из: 0x15bfc
- `0x15c0e..0x15c38` (42 Б); цели из: 0x15b90
- `0x15c38..0x15c3e` (6 Б); цели из: 0x15c2c
- `0x15c3e..0x15c44` (6 Б); цели из: 0x15c30
- `0x15c44..0x15c54` (16 Б); цели из: 0x15c36
- `0x15c54..0x15c56` (2 Б); цели из: 0x15c4e
- `0x15c56..0x15c5e` (8 Б); цели из: 0x15c34
- `0x15c5e..0x15c66` (8 Б); цели из: 0x15c3c, 0x15c42, 0x15c54
- `0x15c66..0x15c6c` (6 Б); цели из: 0x15c14
- `0x15c6c..0x15c70` (4 Б); цели из: 0x15b9e, 0x15bae, 0x15bbe, 0x15bd4…

## Дизассембляция

```asm
  15b84:  push {r4, lr}                     
  15b86:  bl #0x158f8                       -> func_0x158f8
  15b8a:  ldr r0, [pc, #0xe4]               -> RAM
  15b8c:  ldrb r0, [r0, #1]                 
  15b8e:  cmp r0, #0                        
  15b90:  bne #0x15c0e                      
  15b92:  ldr r0, [pc, #0xdc]               -> RAM
  15b94:  ldrb r0, [r0, #2]                 
  15b96:  cbnz r0, #0x15ba0                 
  15b98:  movs r0, #4                       
  15b9a:  ldr r1, [pc, #0xd4]               -> RAM
  15b9c:  strb r0, [r1, #3]                 
  15b9e:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15ba0:  ldr r0, [pc, #0xcc]               -> RAM
  15ba2:  ldrb r0, [r0, #2]                 
  15ba4:  cmp r0, #2                        
  15ba6:  bne #0x15bb0                      
  15ba8:  movs r0, #0                       
  15baa:  ldr r1, [pc, #0xc4]               -> RAM
  15bac:  strb r0, [r1, #3]                 
  15bae:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15bb0:  ldr r0, [pc, #0xbc]               -> RAM
  15bb2:  ldrb r0, [r0, #2]                 
  15bb4:  cmp r0, #1                        
  15bb6:  bne #0x15bc0                      
  15bb8:  movs r0, #5                       
  15bba:  ldr r1, [pc, #0xb4]               -> RAM
  15bbc:  strb r0, [r1, #3]                 
  15bbe:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15bc0:  ldr r0, [pc, #0xac]               -> RAM
  15bc2:  ldrb r0, [r0, #2]                 
  15bc4:  cmp r0, #3                        
  15bc6:  bne #0x15bd6                      
  15bc8:  movs r0, #0                       
  15bca:  ldr r1, [pc, #0xa4]               -> RAM
  15bcc:  strb r0, [r1, #3]                 
  15bce:  movs r0, #1                       
  15bd0:  ldr r1, [pc, #0xa0]               -> RAM
  15bd2:  strb r0, [r1]                     
  15bd4:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15bd6:  ldr r0, [pc, #0x98]               -> RAM
  15bd8:  ldrb r0, [r0, #2]                 
  15bda:  cmp r0, #4                        
  15bdc:  bne #0x15be6                      
  15bde:  movs r0, #0                       
  15be0:  ldr r1, [pc, #0x8c]               -> RAM
  15be2:  strb r0, [r1, #3]                 
  15be4:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15be6:  ldr r0, [pc, #0x88]               -> RAM
  15be8:  ldrb r0, [r0, #2]                 
  15bea:  cmp r0, #5                        
  15bec:  bne #0x15bf6                      
  15bee:  movs r0, #0                       
  15bf0:  ldr r1, [pc, #0x7c]               -> RAM
  15bf2:  strb r0, [r1, #3]                 
  15bf4:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15bf6:  ldr r0, [pc, #0x78]               -> RAM
  15bf8:  ldrb r0, [r0, #2]                 
  15bfa:  cmp r0, #6                        
  15bfc:  bne #0x15c06                      
  15bfe:  movs r0, #2                       
  15c00:  ldr r1, [pc, #0x6c]               -> RAM
  15c02:  strb r0, [r1, #3]                 
  15c04:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15c06:  movs r0, #6                       
  15c08:  ldr r1, [pc, #0x64]               -> RAM
  15c0a:  strb r0, [r1, #3]                 
  15c0c:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15c0e:  ldr r0, [pc, #0x60]               -> RAM
  15c10:  ldrb r0, [r0, #1]                 
  15c12:  cmp r0, #1                        
  15c14:  bne #0x15c66                      
  15c16:  movs r0, #0                       
  15c18:  ldr r1, [pc, #0x58]               -> RAM
  15c1a:  strb r0, [r1]                     
  15c1c:  bl #0x15f00                       -> func_0x15f00
  15c20:  cbnz r0, #0x15c26                 
  15c22:  movs r0, #1                       
  15c24:  pop {r4, pc}                      
  15c26:  ldr r0, [pc, #0x48]               -> RAM
  15c28:  ldrb r0, [r0]                     
  15c2a:  cmp r0, #1                        
  15c2c:  beq #0x15c38                      
  15c2e:  cmp r0, #2                        
  15c30:  beq #0x15c3e                      
  15c32:  cmp r0, #3                        
  15c34:  bne #0x15c56                      
  15c36:  b #0x15c44                        -> 0x15c44 (вне списка функций)
  15c38:  bl #0x15d14                       -> func_0x15d14
  15c3c:  b #0x15c5e                        -> 0x15c5e (вне списка функций)
  15c3e:  bl #0x15918                       -> func_0x15918
  15c42:  b #0x15c5e                        -> 0x15c5e (вне списка функций)
  15c44:  bl #0x15df4                       -> func_0x15df4
  15c48:  ldr r0, [pc, #0x2c]               -> RAM
  15c4a:  ldrb r0, [r0]                     
  15c4c:  cmp r0, #1                        
  15c4e:  bne #0x15c54                      
  15c50:  movs r0, #0                       
  15c52:  b #0x15c24                        -> 0x15c24 (вне списка функций)
  15c54:  b #0x15c5e                        -> 0x15c5e (вне списка функций)
  15c56:  movs r0, #0                       
  15c58:  ldr r1, [pc, #0x14]               -> RAM
  15c5a:  strb r0, [r1]                     
  15c5c:  nop                               
  15c5e:  nop                               
  15c60:  bl #0x15fc8                       -> 0x15fc8 (вне списка функций)
  15c64:  b #0x15c6c                        -> 0x15c6c (вне списка функций)
  15c66:  movs r0, #3                       
  15c68:  ldr r1, [pc, #4]                  -> RAM
  15c6a:  strb r0, [r1, #3]                 
  15c6c:  movs r0, #1                       
  15c6e:  b #0x15c24                        -> 0x15c24 (вне списка функций)
  ; --- literal-пул @0x15c70 (3 слов) — ВНЕ границ функции ---
  15c70:  .word 0x20001fac  ; RAM
  15c74:  .word 0x20000c7e  ; RAM
  15c78:  .word 0x20000c7f  ; RAM
```
