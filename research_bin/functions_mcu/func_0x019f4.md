# func_0x019f4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800019f4) | `0x000019f4` |
| размер кода | 100 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019e5e — flash-mirror @0x19e5e (r0)
- 0x20000a41 — RAM (r0)
- 0x20000f95 — RAM (r0)
- 0x200015f7 — RAM (r0)

## Вызовы (callees)

- 0x01a36 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01abc` (bl @0x00001ac2)


## Дизассембляция

```asm
  019f4:  ldr r0, [pc, #0x60]               -> RAM
  019f6:  ldrb r0, [r0, #0xc]               
  019f8:  ubfx r0, r0, #1, #1               
  019fc:  cbz r0, #0x1a36                   
  019fe:  ldr r0, [pc, #0x5c]               -> RAM
  01a00:  ldrb r0, [r0, #0x11]              
  01a02:  ubfx r0, r0, #2, #1               
  01a06:  cbnz r0, #0x1a30                  
  01a08:  ldr r0, [pc, #0x54]               -> RAM
  01a0a:  ldrb r0, [r0]                     
  01a0c:  adds r0, r0, #1                   
  01a0e:  ldr r1, [pc, #0x50]               -> RAM
  01a10:  strb r0, [r1]                     
  01a12:  ldr r0, [pc, #0x50]               -> flash-mirror @0x19e5e
  01a14:  ldrb r0, [r0, #0xd]               
  01a16:  ldrb r1, [r1]                     
  01a18:  cmp r0, r1                        
  01a1a:  bgt #0x1a36                       
  01a1c:  ldr r0, [pc, #0x38]               -> RAM
  01a1e:  ldrb r0, [r0, #0xc]               
  01a20:  bic r0, r0, #2                    
  01a24:  ldr r1, [pc, #0x30]               -> RAM
  01a26:  strb r0, [r1, #0xc]               
  01a28:  movs r0, #0                       
  01a2a:  ldr r1, [pc, #0x34]               -> RAM
  01a2c:  strb r0, [r1]                     
  01a2e:  b #0x1a36                         -> 0x01a36 (вне списка функций)
  01a30:  movs r0, #0                       
  01a32:  ldr r1, [pc, #0x2c]               -> RAM
  01a34:  strb r0, [r1]                     
  01a36:  ldr r0, [pc, #0x20]               -> RAM
  01a38:  ldrb r0, [r0, #0x17]              
  01a3a:  and r0, r0, #1                    
  01a3e:  cbz r0, #0x1a56                   
  01a40:  ldr r0, [pc, #0x18]               -> RAM
  01a42:  ldrb r0, [r0, #3]                 
  01a44:  ubfx r0, r0, #3, #1               
  01a48:  cbnz r0, #0x1a56                  
  01a4a:  ldr r0, [pc, #0xc]                -> RAM
  01a4c:  ldrb r0, [r0, #0x17]              
  01a4e:  bic r0, r0, #1                    
  01a52:  ldr r1, [pc, #4]                  -> RAM
  01a54:  strb r0, [r1, #0x17]              
  01a56:  bx lr                             
  ; --- literal-пул @0x01a58 (4 слов) — ВНЕ границ функции ---
  01a58:  .word 0x20000f95  ; RAM
  01a5c:  .word 0x200015f7  ; RAM
  01a60:  .word 0x20000a41  ; RAM
  01a64:  .word 0x08019e5e  ; flash-mirror @0x19e5e
```
