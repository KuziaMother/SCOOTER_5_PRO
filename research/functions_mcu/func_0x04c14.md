# func_0x04c14

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004c14) | `0x00004c14` |
| размер кода | 100 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b4c — RAM (r2)
- 0x2000164c — RAM (r0)
- 0xffc91170 — прочее (r3)

## Вызовы (callees)

- 0x04c42 (b, вне списка функций)
- 0x04c72 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11cac` (bl @0x00011cae)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x04c42..0x04c52` (16 Б); цели из: 0x04c2c
- `0x04c52..0x04c6c` (26 Б); цели из: 0x04c28
- `0x04c6c..0x04c72` (6 Б); цели из: 0x04c5c, 0x04c66
- `0x04c72..0x04c78` (6 Б); цели из: 0x04c56

## Дизассембляция

```asm
  04c14:  ldr r2, [pc, #0x60]               -> RAM
  04c16:  ldr r2, [r2]                      
  04c18:  adds r2, r2, #1                   
  04c1a:  ldr r3, [pc, #0x5c]               -> RAM
  04c1c:  str r2, [r3]                      
  04c1e:  ldr r0, [pc, #0x5c]               -> RAM
  04c20:  mov r2, r3                        
  04c22:  ldr r2, [r2]                      
  04c24:  ldr r3, [pc, #0x58]               
  04c26:  cmp r2, r3                        
  04c28:  blo #0x4c52                       
  04c2a:  movs r1, #0                       
  04c2c:  b #0x4c42                         -> 0x04c42 (вне списка функций)
  04c2e:  ldr r2, [r0, #4]                  
  04c30:  adds r2, r2, #1                   
  04c32:  cbz r2, #0x4c3c                   
  04c34:  ldr r3, [pc, #0x48]               
  04c36:  ldr r2, [r0, #4]                  
  04c38:  subs r2, r2, r3                   
  04c3a:  str r2, [r0, #4]                  
  04c3c:  adds r0, #0x10                    
  04c3e:  adds r2, r1, #1                   
  04c40:  uxtb r1, r2                       
  04c42:  cmp r1, #6                        
  04c44:  blt #0x4c2e                       
  04c46:  ldr r2, [pc, #0x30]               -> RAM
  04c48:  ldr r2, [r2]                      
  04c4a:  ldr r3, [pc, #0x34]               
  04c4c:  subs r2, r2, r3                   
  04c4e:  ldr r3, [pc, #0x28]               -> RAM
  04c50:  str r2, [r3]                      
  04c52:  ldr r0, [pc, #0x28]               -> RAM
  04c54:  movs r1, #0                       
  04c56:  b #0x4c72                         -> 0x04c72 (вне списка функций)
  04c58:  ldrb r2, [r0]                     
  04c5a:  cmp r2, #1                        
  04c5c:  bne #0x4c6c                       
  04c5e:  ldr r3, [pc, #0x18]               -> RAM
  04c60:  ldr r2, [r0, #4]                  
  04c62:  ldr r3, [r3]                      
  04c64:  cmp r2, r3                        
  04c66:  bhi #0x4c6c                       
  04c68:  movs r2, #1                       
  04c6a:  strb r2, [r0, #1]                 
  04c6c:  adds r0, #0x10                    
  04c6e:  adds r2, r1, #1                   
  04c70:  uxtb r1, r2                       
  04c72:  cmp r1, #6                        
  04c74:  blt #0x4c58                       
  04c76:  bx lr                             
  ; --- literal-пул @0x04c78 (3 слов) — ВНЕ границ функции ---
  04c78:  .word 0x20000b4c  ; RAM
  04c7c:  .word 0x2000164c  ; RAM
  04c80:  .word 0xffc91170
```
