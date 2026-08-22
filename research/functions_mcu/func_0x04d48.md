# func_0x04d48

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004d48) | `0x00004d48` |
| размер кода | 138 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000007a — RAM (r2)
- 0x2000007b — RAM (r2)
- 0x20000f3c — RAM (r2)

## Вызовы (callees)

- 0x04d78 (b, вне списка функций)
- 0x04d88 (b, вне списка функций)
- 0x04dac (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1337c` (bl @0x000133e6)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x04d78..0x04d8a` (18 Б); цели из: 0x04d6a
- `0x04d8a..0x04dac` (34 Б); цели из: 0x04d54
- `0x04dac..0x04dce` (34 Б); цели из: 0x04d9e
- `0x04dce..0x04dd2` (4 Б); цели из: 0x04dc6

## Дизассембляция

```asm
  04d48:  push {r4, lr}                     
  04d4a:  mov r1, r0                        
  04d4c:  movs r0, #0                       
  04d4e:  ldr r2, [pc, #0x84]               -> RAM
  04d50:  ldrb r2, [r2]                     
  04d52:  cmp r2, #0xa                      
  04d54:  bge #0x4d8a                       
  04d56:  ldr r2, [pc, #0x7c]               -> RAM
  04d58:  ldrb r3, [r2]                     
  04d5a:  ldrb r2, [r2]                     
  04d5c:  adds r2, r2, #1                   
  04d5e:  ldr r4, [pc, #0x74]               -> RAM
  04d60:  strb r2, [r4]                     
  04d62:  ldr r2, [pc, #0x74]               -> RAM
  04d64:  str.w r1, [r2, r3, lsl #2]        
  04d68:  movs r2, #0                       
  04d6a:  b #0x4d78                         -> 0x04d78 (вне списка функций)
  04d6c:  ldr r3, [pc, #0x68]               -> RAM
  04d6e:  ldr.w r3, [r3, r2, lsl #2]        
  04d72:  add r0, r3                        
  04d74:  adds r3, r2, #1                   
  04d76:  uxtb r2, r3                       
  04d78:  ldr r3, [pc, #0x58]               -> RAM
  04d7a:  ldrb r3, [r3]                     
  04d7c:  cmp r2, r3                        
  04d7e:  blt #0x4d6c                       
  04d80:  ldr r2, [pc, #0x50]               -> RAM
  04d82:  ldrb r2, [r2]                     
  04d84:  sdiv r0, r0, r2                   
  04d88:  pop {r4, pc}                      
  04d8a:  ldr r2, [pc, #0x50]               -> RAM
  04d8c:  ldrb r3, [r2]                     
  04d8e:  ldrb r2, [r2]                     
  04d90:  adds r2, r2, #1                   
  04d92:  ldr r4, [pc, #0x48]               -> RAM
  04d94:  strb r2, [r4]                     
  04d96:  ldr r2, [pc, #0x40]               -> RAM
  04d98:  str.w r1, [r2, r3, lsl #2]        
  04d9c:  movs r2, #0                       
  04d9e:  b #0x4dac                         -> 0x04dac (вне списка функций)
  04da0:  ldr r3, [pc, #0x34]               -> RAM
  04da2:  ldr.w r3, [r3, r2, lsl #2]        
  04da6:  add r0, r3                        
  04da8:  adds r3, r2, #1                   
  04daa:  uxtb r2, r3                       
  04dac:  ldr r3, [pc, #0x24]               -> RAM
  04dae:  ldrb r3, [r3]                     
  04db0:  cmp r2, r3                        
  04db2:  blt #0x4da0                       
  04db4:  ldr r2, [pc, #0x1c]               -> RAM
  04db6:  ldrb r2, [r2]                     
  04db8:  sdiv r0, r0, r2                   
  04dbc:  ldr r2, [pc, #0x1c]               -> RAM
  04dbe:  ldrb r2, [r2]                     
  04dc0:  ldr r3, [pc, #0x10]               -> RAM
  04dc2:  ldrb r3, [r3]                     
  04dc4:  cmp r2, r3                        
  04dc6:  bne #0x4dce                       
  04dc8:  movs r2, #0                       
  04dca:  ldr r3, [pc, #0x10]               -> RAM
  04dcc:  strb r2, [r3]                     
  04dce:  nop                               
  04dd0:  b #0x4d88                         -> 0x04d88 (вне списка функций)
  ; --- literal-пул @0x04dd4 (3 слов) — ВНЕ границ функции ---
  04dd4:  .word 0x2000007a  ; RAM
  04dd8:  .word 0x20000f3c  ; RAM
  04ddc:  .word 0x2000007b  ; RAM
```
