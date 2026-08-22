# func_0x15ce0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015ce0) | `0x00015ce0` |
| размер кода | 36 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000c7f — RAM (r0)
- 0x20000c84 — RAM (r0)

## Вызовы (callees)

- `func_0x0d878` (0x0000d878, bl)
- 0x0dd80 (bl, вне списка функций)
- 0x15d0a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  15ce0:  push {r4, lr}                     
  15ce2:  ldr r0, [pc, #0x28]               -> RAM
  15ce4:  ldrb r0, [r0]                     
  15ce6:  cbz r0, #0x15d04                  
  15ce8:  ldr r0, [pc, #0x24]               -> RAM
  15cea:  ldrb r0, [r0]                     
  15cec:  adds r0, r0, #1                   
  15cee:  ldr r1, [pc, #0x20]               -> RAM
  15cf0:  strb r0, [r1]                     
  15cf2:  mov r0, r1                        
  15cf4:  ldrb r0, [r0]                     
  15cf6:  cmp r0, #2                        
  15cf8:  ble #0x15d0a                      
  15cfa:  bl #0xd878                        -> func_0x0d878
  15cfe:  bl #0xdd80                        -> 0x0dd80 (вне списка функций)
  15d02:  b #0x15d0a                        -> 0x15d0a (вне списка функций)
  ; --- literal-пул @0x15d0c (2 слов) — ВНЕ границ функции ---
  15d0c:  .word 0x20000c7f  ; RAM
  15d10:  .word 0x20000c84  ; RAM
```
