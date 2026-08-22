# func_0x03a6c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003a6c) | `0x00003a6c` |
| размер кода | 22 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000142 — RAM (r0)

## Вызовы (callees)

- 0x0dd80 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  03a6c:  push {r4, lr}                     
  03a6e:  ldr r0, [pc, #0x14]               -> RAM
  03a70:  ldrb r0, [r0]                     
  03a72:  cmp r0, #1                        
  03a74:  bne #0x3a80                       
  03a76:  movs r0, #0                       
  03a78:  ldr r1, [pc, #8]                  -> RAM
  03a7a:  strb r0, [r1]                     
  03a7c:  bl #0xdd80                        -> 0x0dd80 (вне списка функций)
  03a80:  pop {r4, pc}                      
  ; --- literal-пул @0x03a84 (1 слов) — ВНЕ границ функции ---
  03a84:  .word 0x20000142  ; RAM
```
