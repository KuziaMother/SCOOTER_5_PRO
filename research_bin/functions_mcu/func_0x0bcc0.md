# func_0x0bcc0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000bcc0) | `0x0000bcc0` |
| размер кода | 138 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200007d4 — RAM (r1)

## Вызовы (callees)

- `func_0x05dd8` (0x00005dd8, bl)
- 0x0bd2e (b, вне списка функций)
- `func_0x0befc` (0x0000befc, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0bcf8..0x0bd2c` (52 Б); цели из: 0x0bcf2
- `0x0bd2c..0x0bd32` (6 Б); цели из: 0x0bd1a
- `0x0bd32..0x0bd4a` (24 Б); цели из: 0x0bd2a

## Дизассембляция

```asm
  0bcc0:  push.w {r2, r3, r4, r5, r6, r7, r8, lr}
  0bcc4:  mov r5, r0                        
  0bcc6:  mov.w r8, #0                      
  0bcca:  movs r7, #0                       
  0bccc:  movs r0, #0                       
  0bcce:  str r0, [sp, #4]                  
  0bcd0:  mov r4, r5                        
  0bcd2:  ldrb.w r8, [r4, #2]               
  0bcd6:  ldrb r0, [r4, #3]                 
  0bcd8:  orr.w r8, r0, r8, lsl #8          
  0bcdc:  ldrb r7, [r4, #4]                 
  0bcde:  ldrb r0, [r4, #5]                 
  0bce0:  orr.w r7, r0, r7, lsl #8          
  0bce4:  movw r0, #0xffff                  
  0bce8:  and.w r0, r0, r7, lsl #1          
  0bcec:  str r0, [sp, #4]                  
  0bcee:  ldrb r0, [r4, #1]                 
  0bcf0:  cmp r0, #6                        
  0bcf2:  bne #0xbcf8                       
  0bcf4:  movs r0, #2                       
  0bcf6:  str r0, [sp, #4]                  
  0bcf8:  ldr r1, [pc, #0x50]               -> RAM
  0bcfa:  mov r0, r8                        
  0bcfc:  bl #0xbefc                        -> func_0x0befc
  0bd00:  mov r6, r0                        
  0bd02:  ldr r0, [pc, #0x48]               -> RAM
  0bd04:  ldrb r0, [r0]                     
  0bd06:  cbz r0, #0xbd2c                   
  0bd08:  ldr r0, [r6]                      
  0bd0a:  ldrb r0, [r0, #8]                 
  0bd0c:  ldr r1, [r6]                      
  0bd0e:  ldrb r1, [r1, #1]                 
  0bd10:  smulbb r0, r0, r1                 
  0bd14:  ldrh.w r1, [sp, #4]               
  0bd18:  cmp r0, r1                        
  0bd1a:  blt #0xbd2c                       
  0bd1c:  ldrb r0, [r6, #4]                 
  0bd1e:  ldr r1, [r6]                      
  0bd20:  ldrb r1, [r1, #8]                 
  0bd22:  add r0, r1                        
  0bd24:  add.w r1, r7, r8                  
  0bd28:  cmp r0, r1                        
  0bd2a:  bge #0xbd32                       
  0bd2c:  movs r0, #0                       
  0bd2e:  pop.w {r2, r3, r4, r5, r6, r7, r8, pc}
  0bd32:  str r6, [sp]                      
  0bd34:  ldrb r1, [r4, #1]                 
  0bd36:  adds r3, r4, #7                   
  0bd38:  add r2, sp, #4                    
  0bd3a:  movs r0, #1                       
  0bd3c:  bl #0x5dd8                        -> func_0x05dd8
  0bd40:  ldrh.w r0, [sp, #4]               
  0bd44:  strb r0, [r4, #6]                 
  0bd46:  movs r0, #1                       
  0bd48:  b #0xbd2e                         -> 0x0bd2e (вне списка функций)
  ; --- literal-пул @0x0bd4c (1 слов) — ВНЕ границ функции ---
  0bd4c:  .word 0x200007d4  ; RAM
```
