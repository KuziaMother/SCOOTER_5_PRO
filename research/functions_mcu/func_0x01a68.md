# func_0x01a68

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001a68) | `0x00001a68` |
| размер кода | 70 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019e5e — flash-mirror @0x19e5e (r1)
- 0x20000a40 — RAM (r0)
- 0x20000f95 — RAM (r0)

## Вызовы (callees)

- 0x01aac (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01abc` (bl @0x00001abe)


## Дизассембляция

```asm
  01a68:  ldr r0, [pc, #0x44]               -> RAM
  01a6a:  ldrb r0, [r0, #0xc]               
  01a6c:  ubfx r0, r0, #4, #1               
  01a70:  cbz r0, #0x1aac                   
  01a72:  ldr r0, [pc, #0x3c]               -> RAM
  01a74:  ldrh r0, [r0, #6]                 
  01a76:  ldr r1, [pc, #0x3c]               -> flash-mirror @0x19e5e
  01a78:  ldrh r1, [r1, #0x18]              
  01a7a:  cmp r0, r1                        
  01a7c:  blt #0x1aa6                       
  01a7e:  ldr r0, [pc, #0x38]               -> RAM
  01a80:  ldrb r0, [r0]                     
  01a82:  adds r0, r0, #1                   
  01a84:  ldr r1, [pc, #0x30]               -> RAM
  01a86:  strb r0, [r1]                     
  01a88:  ldr r0, [pc, #0x28]               -> flash-mirror @0x19e5e
  01a8a:  ldrb r0, [r0, #0x1b]              
  01a8c:  ldrb r1, [r1]                     
  01a8e:  cmp r0, r1                        
  01a90:  bgt #0x1aac                       
  01a92:  ldr r0, [pc, #0x1c]               -> RAM
  01a94:  ldrb r0, [r0, #0xc]               
  01a96:  bic r0, r0, #0x10                 
  01a9a:  ldr r1, [pc, #0x14]               -> RAM
  01a9c:  strb r0, [r1, #0xc]               
  01a9e:  movs r0, #0                       
  01aa0:  ldr r1, [pc, #0x14]               -> RAM
  01aa2:  strb r0, [r1]                     
  01aa4:  b #0x1aac                         -> 0x01aac (вне списка функций)
  01aa6:  movs r0, #0                       
  01aa8:  ldr r1, [pc, #0xc]                -> RAM
  01aaa:  strb r0, [r1]                     
  01aac:  bx lr                             
  ; --- literal-пул @0x01ab0 (3 слов) — ВНЕ границ функции ---
  01ab0:  .word 0x20000f95  ; RAM
  01ab4:  .word 0x08019e5e  ; flash-mirror @0x19e5e
  01ab8:  .word 0x20000a40  ; RAM
```
