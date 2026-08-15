# func_0x04cbc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004cbc) | `0x00004cbc` |
| размер кода | 122 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b4c — RAM (r1)
- 0x20000b50 — RAM (r0)
- 0x20000b54 — RAM (r0)
- 0x2000164c — RAM (r4)

## Вызовы (callees)

- `func_0x02d1c` (0x00002d1c, bl)
- `func_0x02d34` (0x00002d34, bl)
- 0x04d20 (b, вне списка функций)
- 0x04d2a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x04cfa..0x04d24` (42 Б); цели из: 0x04cf4
- `0x04d24..0x04d2a` (6 Б); цели из: 0x04cde, 0x04ce4
- `0x04d2a..0x04d36` (12 Б); цели из: 0x04cd8

## Дизассембляция

```asm
  04cbc:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  04cc0:  mov sb, r0                        
  04cc2:  movs r7, #0                       
  04cc4:  mov r8, r7                        
  04cc6:  ldr r4, [pc, #0x70]               -> RAM
  04cc8:  ldr r0, [pc, #0x70]               -> RAM
  04cca:  ldr r0, [r0]                      
  04ccc:  adds r0, r0, #1                   
  04cce:  ldr r1, [pc, #0x6c]               -> RAM
  04cd0:  str r0, [r1]                      
  04cd2:  bl #0x2d1c                        -> func_0x02d1c
  04cd6:  movs r6, #0                       
  04cd8:  b #0x4d2a                         -> 0x04d2a (вне списка функций)
  04cda:  ldrb r0, [r4, #1]                 
  04cdc:  cmp r0, #1                        
  04cde:  bne #0x4d24                       
  04ce0:  ldrb r0, [r4]                     
  04ce2:  cmp r0, #1                        
  04ce4:  bne #0x4d24                       
  04ce6:  ldr r1, [pc, #0x58]               -> RAM
  04ce8:  ldr r0, [r4, #4]                  
  04cea:  ldr r1, [r1]                      
  04cec:  subs r5, r1, r0                   
  04cee:  ldr r0, [pc, #0x54]               -> RAM
  04cf0:  ldr r0, [r0]                      
  04cf2:  cmp r5, r0                        
  04cf4:  bls #0x4cfa                       
  04cf6:  ldr r0, [pc, #0x4c]               -> RAM
  04cf8:  str r5, [r0]                      
  04cfa:  ldr r7, [r4, #8]                  
  04cfc:  ldr.w r8, [r4, #0xc]              
  04d00:  mov.w r0, #-1                     
  04d04:  str r0, [r4, #4]                  
  04d06:  movs r0, #2                       
  04d08:  strb r0, [r4]                     
  04d0a:  movs r0, #0                       
  04d0c:  strb r0, [r4, #1]                 
  04d0e:  cbz r7, #0x4d1c                   
  04d10:  bl #0x2d34                        -> func_0x02d34
  04d14:  mov r0, r8                        
  04d16:  blx r7                            
  04d18:  bl #0x2d1c                        -> func_0x02d1c
  04d1c:  bl #0x2d34                        -> func_0x02d34
  04d20:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
  04d24:  adds r4, #0x10                    
  04d26:  adds r0, r6, #1                   
  04d28:  uxtb r6, r0                       
  04d2a:  cmp r6, #6                        
  04d2c:  blt #0x4cda                       
  04d2e:  bl #0x2d34                        -> func_0x02d34
  04d32:  nop                               
  04d34:  b #0x4d20                         -> 0x04d20 (вне списка функций)
  ; --- literal-пул @0x04d38 (4 слов) — ВНЕ границ функции ---
  04d38:  .word 0x2000164c  ; RAM
  04d3c:  .word 0x20000b50  ; RAM
  04d40:  .word 0x20000b4c  ; RAM
  04d44:  .word 0x20000b54  ; RAM
```
