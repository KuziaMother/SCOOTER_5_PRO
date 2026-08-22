# func_0x12e64

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012e64) | `0x00012e64` |
| размер кода | 56 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b76 — RAM (r0)
- 0x20000b7c — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x13284` (bl @0x000132fe)


## Дизассембляция

```asm
  12e64:  push {r4, lr}                     
  12e66:  sub sp, #0x18                     
  12e68:  movs r4, #0                       
  12e6a:  ldr r0, [pc, #0xc8]               -> RAM
  12e6c:  ldrb r0, [r0]                     
  12e6e:  ubfx r0, r0, #2, #1               
  12e72:  cbz r0, #0x12e9c                  
  12e74:  ldr r0, [pc, #0xc0]               -> RAM
  12e76:  ldrh r0, [r0]                     
  12e78:  adds r0, r0, #1                   
  12e7a:  ldr r1, [pc, #0xbc]               -> RAM
  12e7c:  strh r0, [r1]                     
  12e7e:  mov r0, r1                        
  12e80:  ldrh r0, [r0]                     
  12e82:  cmp r0, #0xc8                     
  12e84:  ble #0x12e98                      
  12e86:  ldr r0, [pc, #0xac]               -> RAM
  12e88:  ldrb r0, [r0]                     
  12e8a:  bic r0, r0, #4                    
  12e8e:  ldr r1, [pc, #0xa4]               -> RAM
  12e90:  strb r0, [r1]                     
  12e92:  movs r0, #0                       
  12e94:  ldr r1, [pc, #0xa0]               -> RAM
  12e96:  strh r0, [r1]                     
  12e98:  add sp, #0x18                     
  12e9a:  pop {r4, pc}                      
  ; --- literal-пул @0x12f34 (2 слов) — ВНЕ границ функции ---
  12f34:  .word 0x20000b76  ; RAM
  12f38:  .word 0x20000b7c  ; RAM
```
