# func_0x0fe74

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000fe74) | `0x0000fe74` |
| размер кода | 174 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019e1c — flash-mirror @0x19e1c (r1)
- 0x20000080 — RAM (r0)
- 0x200009f0 — RAM (r0)
- 0x200009f2 — RAM (r0)
- 0x20000fc7 — RAM (r0)
- 0x40010c18 — периферия (r1)

## Вызовы (callees)

- 0x0fece (b, вне списка функций)
- 0x0ff20 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11998` (bl @0x000119aa)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0fec8..0x0fece` (6 Б); цели из: 0x0fe92
- `0x0fece..0x0ff1a` (76 Б); цели из: 0x0fea8, 0x0fec6
- `0x0ff1a..0x0ff20` (6 Б); цели из: 0x0fee6
- `0x0ff20..0x0ff22` (2 Б); цели из: 0x0fefa, 0x0ff18

## Дизассембляция

```asm
  0fe74:  ldr r0, [pc, #0xac]               -> RAM
  0fe76:  ldrb r0, [r0]                     
  0fe78:  cbnz r0, #0xfec6                  
  0fe7a:  ldr r0, [pc, #0xac]               -> RAM
  0fe7c:  ldrb r0, [r0, #6]                 
  0fe7e:  ubfx r0, r0, #1, #1               
  0fe82:  cbnz r0, #0xfec6                  
  0fe84:  ldr r0, [pc, #0xa0]               -> RAM
  0fe86:  ldrsb.w r0, [r0, #1]              
  0fe8a:  ldr r1, [pc, #0xa0]               -> flash-mirror @0x19e1c
  0fe8c:  ldrsb.w r1, [r1, #6]              
  0fe90:  cmp r0, r1                        
  0fe92:  bgt #0xfec8                       
  0fe94:  ldr r0, [pc, #0x98]               -> RAM
  0fe96:  ldrh r0, [r0]                     
  0fe98:  adds r0, r0, #1                   
  0fe9a:  ldr r1, [pc, #0x94]               -> RAM
  0fe9c:  strh r0, [r1]                     
  0fe9e:  ldr r0, [pc, #0x8c]               -> flash-mirror @0x19e1c
  0fea0:  ldrh.w r0, [r0, #7]               
  0fea4:  ldrh r1, [r1]                     
  0fea6:  cmp r0, r1                        
  0fea8:  bgt #0xfece                       
  0feaa:  mov.w r0, #0x8000                 
  0feae:  ldr r1, [pc, #0x84]               -> периферия
  0feb0:  str r0, [r1]                      
  0feb2:  ldr r0, [pc, #0x74]               -> RAM
  0feb4:  ldrb r0, [r0, #6]                 
  0feb6:  bic r0, r0, #2                    
  0feba:  adds r0, r0, #2                   
  0febc:  ldr r1, [pc, #0x68]               -> RAM
  0febe:  strb r0, [r1, #6]                 
  0fec0:  movs r0, #0                       
  0fec2:  ldr r1, [pc, #0x6c]               -> RAM
  0fec4:  strh r0, [r1]                     
  0fec6:  b #0xfece                         -> 0x0fece (вне списка функций)
  0fec8:  movs r0, #0                       
  0feca:  ldr r1, [pc, #0x64]               -> RAM
  0fecc:  strh r0, [r1]                     
  0fece:  ldr r0, [pc, #0x58]               -> RAM
  0fed0:  ldrb r0, [r0, #6]                 
  0fed2:  ubfx r0, r0, #1, #1               
  0fed6:  cbz r0, #0xff18                   
  0fed8:  ldr r0, [pc, #0x4c]               -> RAM
  0feda:  ldrsb.w r0, [r0, #1]              
  0fede:  ldr r1, [pc, #0x4c]               -> flash-mirror @0x19e1c
  0fee0:  ldrsb.w r1, [r1, #9]              
  0fee4:  cmp r0, r1                        
  0fee6:  blt #0xff1a                       
  0fee8:  ldr r0, [pc, #0x4c]               -> RAM
  0feea:  ldrh r0, [r0]                     
  0feec:  adds r0, r0, #1                   
  0feee:  ldr r1, [pc, #0x48]               -> RAM
  0fef0:  strh r0, [r1]                     
  0fef2:  ldr r0, [pc, #0x38]               -> flash-mirror @0x19e1c
  0fef4:  ldrh r0, [r0, #0xa]               
  0fef6:  ldrh r1, [r1]                     
  0fef8:  cmp r0, r1                        
  0fefa:  bgt #0xff20                       
  0fefc:  mov.w r0, #0x8000                 
  0ff00:  ldr r1, [pc, #0x30]               -> периферия
  0ff02:  adds r1, #0x10                    
  0ff04:  str r0, [r1]                      
  0ff06:  ldr r0, [pc, #0x20]               -> RAM
  0ff08:  ldrb r0, [r0, #6]                 
  0ff0a:  bic r0, r0, #2                    
  0ff0e:  ldr r1, [pc, #0x18]               -> RAM
  0ff10:  strb r0, [r1, #6]                 
  0ff12:  movs r0, #0                       
  0ff14:  ldr r1, [pc, #0x20]               -> RAM
  0ff16:  strh r0, [r1]                     
  0ff18:  b #0xff20                         -> 0x0ff20 (вне списка функций)
  0ff1a:  movs r0, #0                       
  0ff1c:  ldr r1, [pc, #0x18]               -> RAM
  0ff1e:  strh r0, [r1]                     
  0ff20:  bx lr                             
  ; --- literal-пул @0x0ff24 (6 слов) — ВНЕ границ функции ---
  0ff24:  .word 0x20000080  ; RAM
  0ff28:  .word 0x20000fc7  ; RAM
  0ff2c:  .word 0x08019e1c  ; flash-mirror @0x19e1c
  0ff30:  .word 0x200009f0  ; RAM
  0ff34:  .word 0x40010c18  ; периферия
  0ff38:  .word 0x200009f2  ; RAM
```
