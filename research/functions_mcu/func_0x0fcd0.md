# func_0x0fcd0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000fcd0) | `0x0000fcd0` |
| размер кода | 194 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019daa — flash-mirror @0x19daa (r1)
- 0x20000080 — RAM (r0)
- 0x200009fc — RAM (r0)
- 0x200009fe — RAM (r1)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)

## Вызовы (callees)

- 0x0fd2a (b, вне списка функций)
- 0x0fd90 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11998` (bl @0x0001199e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0fce0..0x0fd24` (68 Б); цели из: 0x0fcd6
- `0x0fd24..0x0fd2a` (6 Б); цели из: 0x0fcf4
- `0x0fd2a..0x0fd56` (44 Б); цели из: 0x0fcde, 0x0fd08, 0x0fd22
- `0x0fd56..0x0fd8a` (52 Б); цели из: 0x0fd40
- `0x0fd8a..0x0fd90` (6 Б); цели из: 0x0fd60
- `0x0fd90..0x0fd92` (2 Б); цели из: 0x0fd54, 0x0fd74, 0x0fd88

## Дизассембляция

```asm
  0fcd0:  ldr r0, [pc, #0xc0]               -> RAM
  0fcd2:  ldrb r0, [r0]                     
  0fcd4:  cmp r0, #1                        
  0fcd6:  beq #0xfce0                       
  0fcd8:  ldr r0, [pc, #0xb8]               -> RAM
  0fcda:  ldrb r0, [r0]                     
  0fcdc:  cmp r0, #2                        
  0fcde:  bne #0xfd2a                       
  0fce0:  ldr r0, [pc, #0xb4]               -> RAM
  0fce2:  ldrb r0, [r0, #0xc]               
  0fce4:  ubfx r0, r0, #3, #1               
  0fce8:  cbnz r0, #0xfd2a                  
  0fcea:  ldr r0, [pc, #0xac]               -> RAM
  0fcec:  ldrh r0, [r0, #6]                 
  0fcee:  ldr r1, [pc, #0xac]               -> flash-mirror @0x19daa
  0fcf0:  ldrh r1, [r1, #0xe]               
  0fcf2:  cmp r0, r1                        
  0fcf4:  bgt #0xfd24                       
  0fcf6:  ldr r0, [pc, #0xa8]               -> RAM
  0fcf8:  ldrh r0, [r0]                     
  0fcfa:  adds r0, r0, #1                   
  0fcfc:  ldr r1, [pc, #0xa0]               -> RAM
  0fcfe:  strh r0, [r1]                     
  0fd00:  ldr r0, [pc, #0x98]               -> flash-mirror @0x19daa
  0fd02:  ldrh r0, [r0, #0x12]              
  0fd04:  ldrh r1, [r1]                     
  0fd06:  cmp r0, r1                        
  0fd08:  bgt #0xfd2a                       
  0fd0a:  ldr r0, [pc, #0x8c]               -> RAM
  0fd0c:  ldrb r0, [r0, #0xc]               
  0fd0e:  bic r0, r0, #8                    
  0fd12:  adds r0, #8                       
  0fd14:  ldr r1, [pc, #0x80]               -> RAM
  0fd16:  strb r0, [r1, #0xc]               
  0fd18:  movs r0, #0                       
  0fd1a:  ldr r1, [pc, #0x84]               -> RAM
  0fd1c:  strh r0, [r1]                     
  0fd1e:  ldr r1, [pc, #0x84]               -> RAM
  0fd20:  strh r0, [r1]                     
  0fd22:  b #0xfd2a                         -> 0x0fd2a (вне списка функций)
  0fd24:  movs r0, #0                       
  0fd26:  ldr r1, [pc, #0x78]               -> RAM
  0fd28:  strh r0, [r1]                     
  0fd2a:  ldr r0, [pc, #0x6c]               -> RAM
  0fd2c:  ldrb r0, [r0, #0xc]               
  0fd2e:  ubfx r0, r0, #3, #1               
  0fd32:  cbz r0, #0xfd88                   
  0fd34:  ldr r0, [pc, #0x5c]               -> RAM
  0fd36:  ldrb r0, [r0]                     
  0fd38:  cbnz r0, #0xfd56                  
  0fd3a:  ldr r0, [pc, #0x6c]               -> RAM
  0fd3c:  ldr r0, [r0, #4]                  
  0fd3e:  cmp r0, #0x64                     
  0fd40:  blo #0xfd56                       
  0fd42:  ldr r0, [pc, #0x54]               -> RAM
  0fd44:  ldrb r0, [r0, #0xc]               
  0fd46:  bic r0, r0, #8                    
  0fd4a:  ldr r1, [pc, #0x4c]               -> RAM
  0fd4c:  strb r0, [r1, #0xc]               
  0fd4e:  movs r0, #0                       
  0fd50:  ldr r1, [pc, #0x50]               -> RAM
  0fd52:  strh r0, [r1]                     
  0fd54:  b #0xfd90                         -> 0x0fd90 (вне списка функций)
  0fd56:  ldr r0, [pc, #0x40]               -> RAM
  0fd58:  ldrh r0, [r0, #6]                 
  0fd5a:  ldr r1, [pc, #0x40]               -> flash-mirror @0x19daa
  0fd5c:  ldrh r1, [r1, #0x10]              
  0fd5e:  cmp r0, r1                        
  0fd60:  blt #0xfd8a                       
  0fd62:  ldr r0, [pc, #0x40]               -> RAM
  0fd64:  ldrh r0, [r0]                     
  0fd66:  adds r0, r0, #1                   
  0fd68:  ldr r1, [pc, #0x38]               -> RAM
  0fd6a:  strh r0, [r1]                     
  0fd6c:  ldr r0, [pc, #0x2c]               -> flash-mirror @0x19daa
  0fd6e:  ldrh r0, [r0, #0x14]              
  0fd70:  ldrh r1, [r1]                     
  0fd72:  cmp r0, r1                        
  0fd74:  bgt #0xfd90                       
  0fd76:  ldr r0, [pc, #0x20]               -> RAM
  0fd78:  ldrb r0, [r0, #0xc]               
  0fd7a:  bic r0, r0, #8                    
  0fd7e:  ldr r1, [pc, #0x18]               -> RAM
  0fd80:  strb r0, [r1, #0xc]               
  0fd82:  movs r0, #0                       
  0fd84:  ldr r1, [pc, #0x1c]               -> RAM
  0fd86:  strh r0, [r1]                     
  0fd88:  b #0xfd90                         -> 0x0fd90 (вне списка функций)
  0fd8a:  movs r0, #0                       
  0fd8c:  ldr r1, [pc, #0x14]               -> RAM
  0fd8e:  strh r0, [r1]                     
  0fd90:  bx lr                             
  ; --- literal-пул @0x0fd94 (6 слов) — ВНЕ границ функции ---
  0fd94:  .word 0x20000080  ; RAM
  0fd98:  .word 0x20000f95  ; RAM
  0fd9c:  .word 0x08019daa  ; flash-mirror @0x19daa
  0fda0:  .word 0x200009fc  ; RAM
  0fda4:  .word 0x200009fe  ; RAM
  0fda8:  .word 0x20000fbb  ; RAM
```
