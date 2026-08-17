# func_0x08afc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008afc) | `0x00008afc` |
| размер кода | 14 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f95 — RAM (r1)

## Вызовы (callees)

- `func_0x0218c` (0x0000218c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03668` (bl @0x0000366c)


## Дизассембляция

```asm
  08afc:  push {r4, lr}                     
  08afe:  bl #0x218c                        -> func_0x0218c
  08b02:  ldr r1, [pc, #8]                  -> RAM
  08b04:  str.w r0, [r1, #0xd]              
  08b08:  pop {r4, pc}                      
  ; --- literal-пул @0x08b0c (1 слов) — ВНЕ границ функции ---
  08b0c:  .word 0x20000f95  ; RAM
```
