# func_0x0fdac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000fdac) | `0x0000fdac` |
| размер кода | 174 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019e1c — flash-mirror @0x19e1c (r1)
- 0x20000080 — RAM (r0)
- 0x200009f4 — RAM (r0)
- 0x200009f6 — RAM (r0)
- 0x20000fc7 — RAM (r0)
- 0x40010c18 — периферия (r1)

## Вызовы (callees)

- 0x0fe06 (b, вне списка функций)
- 0x0fe58 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11998` (bl @0x000119a6)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0fe00..0x0fe06` (6 Б); цели из: 0x0fdca
- `0x0fe06..0x0fe52` (76 Б); цели из: 0x0fde0, 0x0fdfe
- `0x0fe52..0x0fe58` (6 Б); цели из: 0x0fe1e
- `0x0fe58..0x0fe5a` (2 Б); цели из: 0x0fe32, 0x0fe50

## Дизассембляция

```asm
  0fdac:  ldr r0, [pc, #0xac]               -> RAM
  0fdae:  ldrb r0, [r0]                     
  0fdb0:  cbnz r0, #0xfdfe                  
  0fdb2:  ldr r0, [pc, #0xac]               -> RAM
  0fdb4:  ldrb r0, [r0, #6]                 
  0fdb6:  and r0, r0, #1                    
  0fdba:  cbnz r0, #0xfdfe                  
  0fdbc:  ldr r0, [pc, #0xa0]               -> RAM
  0fdbe:  ldrsb.w r0, [r0, #2]              
  0fdc2:  ldr r1, [pc, #0xa0]               -> flash-mirror @0x19e1c
  0fdc4:  ldrsb.w r1, [r1]                  
  0fdc8:  cmp r0, r1                        
  0fdca:  blt #0xfe00                       
  0fdcc:  ldr r0, [pc, #0x98]               -> RAM
  0fdce:  ldrh r0, [r0]                     
  0fdd0:  adds r0, r0, #1                   
  0fdd2:  ldr r1, [pc, #0x94]               -> RAM
  0fdd4:  strh r0, [r1]                     
  0fdd6:  ldr r0, [pc, #0x8c]               -> flash-mirror @0x19e1c
  0fdd8:  ldrh.w r0, [r0, #1]               
  0fddc:  ldrh r1, [r1]                     
  0fdde:  cmp r0, r1                        
  0fde0:  bgt #0xfe06                       
  0fde2:  mov.w r0, #0x8000                 
  0fde6:  ldr r1, [pc, #0x84]               -> периферия
  0fde8:  str r0, [r1]                      
  0fdea:  ldr r0, [pc, #0x74]               -> RAM
  0fdec:  ldrb r0, [r0, #6]                 
  0fdee:  bic r0, r0, #1                    
  0fdf2:  adds r0, r0, #1                   
  0fdf4:  ldr r1, [pc, #0x68]               -> RAM
  0fdf6:  strb r0, [r1, #6]                 
  0fdf8:  movs r0, #0                       
  0fdfa:  ldr r1, [pc, #0x6c]               -> RAM
  0fdfc:  strh r0, [r1]                     
  0fdfe:  b #0xfe06                         -> 0x0fe06 (вне списка функций)
  0fe00:  movs r0, #0                       
  0fe02:  ldr r1, [pc, #0x64]               -> RAM
  0fe04:  strh r0, [r1]                     
  0fe06:  ldr r0, [pc, #0x58]               -> RAM
  0fe08:  ldrb r0, [r0, #6]                 
  0fe0a:  and r0, r0, #1                    
  0fe0e:  cbz r0, #0xfe50                   
  0fe10:  ldr r0, [pc, #0x4c]               -> RAM
  0fe12:  ldrsb.w r0, [r0, #2]              
  0fe16:  ldr r1, [pc, #0x4c]               -> flash-mirror @0x19e1c
  0fe18:  ldrsb.w r1, [r1, #3]              
  0fe1c:  cmp r0, r1                        
  0fe1e:  bgt #0xfe52                       
  0fe20:  ldr r0, [pc, #0x4c]               -> RAM
  0fe22:  ldrh r0, [r0]                     
  0fe24:  adds r0, r0, #1                   
  0fe26:  ldr r1, [pc, #0x48]               -> RAM
  0fe28:  strh r0, [r1]                     
  0fe2a:  ldr r0, [pc, #0x38]               -> flash-mirror @0x19e1c
  0fe2c:  ldrh r0, [r0, #4]                 
  0fe2e:  ldrh r1, [r1]                     
  0fe30:  cmp r0, r1                        
  0fe32:  bgt #0xfe58                       
  0fe34:  mov.w r0, #0x8000                 
  0fe38:  ldr r1, [pc, #0x30]               -> периферия
  0fe3a:  adds r1, #0x10                    
  0fe3c:  str r0, [r1]                      
  0fe3e:  ldr r0, [pc, #0x20]               -> RAM
  0fe40:  ldrb r0, [r0, #6]                 
  0fe42:  bic r0, r0, #1                    
  0fe46:  ldr r1, [pc, #0x18]               -> RAM
  0fe48:  strb r0, [r1, #6]                 
  0fe4a:  movs r0, #0                       
  0fe4c:  ldr r1, [pc, #0x20]               -> RAM
  0fe4e:  strh r0, [r1]                     
  0fe50:  b #0xfe58                         -> 0x0fe58 (вне списка функций)
  0fe52:  movs r0, #0                       
  0fe54:  ldr r1, [pc, #0x18]               -> RAM
  0fe56:  strh r0, [r1]                     
  0fe58:  bx lr                             
  ; --- literal-пул @0x0fe5c (6 слов) — ВНЕ границ функции ---
  0fe5c:  .word 0x20000080  ; RAM
  0fe60:  .word 0x20000fc7  ; RAM
  0fe64:  .word 0x08019e1c  ; flash-mirror @0x19e1c
  0fe68:  .word 0x200009f4  ; RAM
  0fe6c:  .word 0x40010c18  ; периферия
  0fe70:  .word 0x200009f6  ; RAM
```
