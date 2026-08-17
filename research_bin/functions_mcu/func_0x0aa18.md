# func_0x0aa18

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000aa18) | `0x0000aa18` |
| размер кода | 170 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801c800 — flash-mirror @0x1c800 (r1)
- 0x0801cfff — flash-mirror @0x1cfff (r2)
- 0x0801d7ff — flash-mirror @0x1d7ff (r2)

## Вызовы (callees)

- `func_0x062d4` (0x000062d4, bl)
- `func_0x06304` (0x00006304, bl)
- `func_0x06378` (0x00006378, bl)
- 0x0aa68 (b, вне списка функций)
- 0x0aab0 (b, вне списка функций)
- 0x0aab4 (b, вне списка функций)
- 0x0aab8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0acce` (bl @0x0000ae16)
- `func_0x0acce` (bl @0x0000ae22)
- `func_0x0ad9e` (bl @0x0000ae16)
- `func_0x0ad9e` (bl @0x0000ae22)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0aa56..0x0aa66` (16 Б); цели из: 0x0aa4e
- `0x0aa66..0x0aa6c` (6 Б); цели из: 0x0aa38, 0x0aa5c
- `0x0aa6c..0x0aaaa` (62 Б); цели из: 0x0aa54, 0x0aa64
- `0x0aaaa..0x0aab0` (6 Б); цели из: 0x0aa9e
- `0x0aab0..0x0aab4` (4 Б); цели из: 0x0aaa8
- `0x0aab4..0x0aab8` (4 Б); цели из: 0x0aa72
- `0x0aab8..0x0aac2` (10 Б); цели из: 0x0aaae

## Дизассембляция

```asm
  0aa18:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, lr}
  0aa1c:  mov r5, r0                        
  0aa1e:  mov r6, r1                        
  0aa20:  mov r4, r2                        
  0aa22:  mov.w r8, #0                      
  0aa26:  mov sb, r8                        
  0aa28:  mov sl, r8                        
  0aa2a:  mov fp, r8                        
  0aa2c:  movs r7, #0                       
  0aa2e:  mov sb, r5                        
  0aa30:  cbz r6, #0xaa66                   
  0aa32:  cbz r4, #0xaa66                   
  0aa34:  cmp.w r4, #0x800                  
  0aa38:  bgt #0xaa66                       
  0aa3a:  asrs r1, r4, #0x1f                
  0aa3c:  add.w r1, r4, r1, lsr #30         
  0aa40:  asrs r1, r1, #2                   
  0aa42:  sub.w r1, r4, r1, lsl #2          
  0aa46:  cbnz r1, #0xaa66                  
  0aa48:  adds r1, r5, r4                   
  0aa4a:  ldr r2, [pc, #0x78]               -> flash-mirror @0x1cfff
  0aa4c:  cmp r1, r2                        
  0aa4e:  bhs #0xaa56                       
  0aa50:  ldr r1, [pc, #0x74]               -> flash-mirror @0x1c800
  0aa52:  cmp r5, r1                        
  0aa54:  bhs #0xaa6c                       
  0aa56:  adds r1, r5, r4                   
  0aa58:  ldr r2, [pc, #0x70]               -> flash-mirror @0x1d7ff
  0aa5a:  cmp r1, r2                        
  0aa5c:  bhs #0xaa66                       
  0aa5e:  ldr r1, [pc, #0x64]               -> flash-mirror @0x1cfff
  0aa60:  adds r1, r1, #1                   
  0aa62:  cmp r5, r1                        
  0aa64:  bhs #0xaa6c                       
  0aa66:  movs r0, #0                       
  0aa68:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, pc}
  0aa6c:  bl #0x6378                        -> func_0x06378
  0aa70:  movs r7, #0                       
  0aa72:  b #0xaab4                         -> 0x0aab4 (вне списка функций)
  0aa74:  adds r0, r7, #3                   
  0aa76:  ldrb.w r8, [r6, r0]               
  0aa7a:  adds r0, r7, #2                   
  0aa7c:  ldrb r0, [r6, r0]                 
  0aa7e:  add.w r8, r0, r8, lsl #8          
  0aa82:  adds r0, r7, #1                   
  0aa84:  ldrb r0, [r6, r0]                 
  0aa86:  add.w r8, r0, r8, lsl #8          
  0aa8a:  ldrb r0, [r6, r7]                 
  0aa8c:  add.w r8, r0, r8, lsl #8          
  0aa90:  mov r1, r8                        
  0aa92:  mov r0, sb                        
  0aa94:  bl #0x6304                        -> func_0x06304
  0aa98:  mov sl, r0                        
  0aa9a:  cmp.w sl, #6                      
  0aa9e:  bne #0xaaaa                       
  0aaa0:  add.w sb, sb, #4                  
  0aaa4:  mov.w fp, #1                      
  0aaa8:  b #0xaab0                         -> 0x0aab0 (вне списка функций)
  0aaaa:  mov.w fp, #0                      
  0aaae:  b #0xaab8                         -> 0x0aab8 (вне списка функций)
  0aab0:  adds r0, r7, #4                   
  0aab2:  uxtb r7, r0                       
  0aab4:  cmp r7, r4                        
  0aab6:  blt #0xaa74                       
  0aab8:  nop                               
  0aaba:  bl #0x62d4                        -> func_0x062d4
  0aabe:  mov r0, fp                        
  0aac0:  b #0xaa68                         -> 0x0aa68 (вне списка функций)
  ; --- literal-пул @0x0aac4 (3 слов) — ВНЕ границ функции ---
  0aac4:  .word 0x0801cfff  ; flash-mirror @0x1cfff
  0aac8:  .word 0x0801c800  ; flash-mirror @0x1c800
  0aacc:  .word 0x0801d7ff  ; flash-mirror @0x1d7ff
```
