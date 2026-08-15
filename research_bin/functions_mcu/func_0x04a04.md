# func_0x04a04

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004a04) | `0x00004a04` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000129 — RAM (r1)
- 0x2000012c — RAM (r1)
- 0x20000130 — RAM (r1)
- 0x20000134 — RAM (r1)
- 0x20000138 — RAM (r1)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x04a30` (bl @0x00004a34)
- `func_0x04a4c` (bl @0x00004a60)
- `func_0x04b04` (bl @0x00004b08)


## Дизассембляция

```asm
  04a04:  movs r0, #0                       
  04a06:  ldr r1, [pc, #0x14]               -> RAM
  04a08:  strb r0, [r1]                     
  04a0a:  ldr r1, [pc, #0x14]               -> RAM
  04a0c:  str r0, [r1]                      
  04a0e:  ldr r1, [pc, #0x14]               -> RAM
  04a10:  str r0, [r1]                      
  04a12:  ldr r1, [pc, #0x14]               -> RAM
  04a14:  str r0, [r1]                      
  04a16:  ldr r1, [pc, #0x14]               -> RAM
  04a18:  str r0, [r1]                      
  04a1a:  bx lr                             
  ; --- literal-пул @0x04a1c (5 слов) — ВНЕ границ функции ---
  04a1c:  .word 0x20000129  ; RAM
  04a20:  .word 0x2000012c  ; RAM
  04a24:  .word 0x20000130  ; RAM
  04a28:  .word 0x20000134  ; RAM
  04a2c:  .word 0x20000138  ; RAM
```
