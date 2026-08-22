# func_0x12c24

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012c24) | `0x00012c24` |
| размер кода | 56 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b76 — RAM (r0)
- 0x20000b7a — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x131fc` (bl @0x00013276)


## Дизассембляция

```asm
  12c24:  push {r4, lr}                     
  12c26:  sub sp, #0x18                     
  12c28:  movs r4, #0                       
  12c2a:  ldr r0, [pc, #0xc8]               -> RAM
  12c2c:  ldrb r0, [r0]                     
  12c2e:  and r0, r0, #1                    
  12c32:  cbz r0, #0x12c5c                  
  12c34:  ldr r0, [pc, #0xc0]               -> RAM
  12c36:  ldrh r0, [r0]                     
  12c38:  adds r0, r0, #1                   
  12c3a:  ldr r1, [pc, #0xbc]               -> RAM
  12c3c:  strh r0, [r1]                     
  12c3e:  mov r0, r1                        
  12c40:  ldrh r0, [r0]                     
  12c42:  cmp r0, #0xc8                     
  12c44:  ble #0x12c58                      
  12c46:  ldr r0, [pc, #0xac]               -> RAM
  12c48:  ldrb r0, [r0]                     
  12c4a:  bic r0, r0, #1                    
  12c4e:  ldr r1, [pc, #0xa4]               -> RAM
  12c50:  strb r0, [r1]                     
  12c52:  movs r0, #0                       
  12c54:  ldr r1, [pc, #0xa0]               -> RAM
  12c56:  strh r0, [r1]                     
  12c58:  add sp, #0x18                     
  12c5a:  pop {r4, pc}                      
  ; --- literal-пул @0x12cf4 (2 слов) — ВНЕ границ функции ---
  12cf4:  .word 0x20000b76  ; RAM
  12cf8:  .word 0x20000b7a  ; RAM
```
