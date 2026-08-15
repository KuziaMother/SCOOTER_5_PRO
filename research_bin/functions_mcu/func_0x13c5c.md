# func_0x13c5c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080013c5c) | `0x00013c5c` |
| размер кода | 18 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000cac — RAM (r1)
- 0x20003084 — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001dfa)


## Дизассембляция

```asm
  13c5c:  push {r4, lr}                     
  13c5e:  movs r1, #0x4b                    
  13c60:  ldr r0, [pc, #0xc]                -> RAM
  13c62:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  13c66:  movs r0, #1                       
  13c68:  ldr r1, [pc, #8]                  -> RAM
  13c6a:  strb r0, [r1]                     
  13c6c:  pop {r4, pc}                      
  ; --- literal-пул @0x13c70 (2 слов) — ВНЕ границ функции ---
  13c70:  .word 0x20003084  ; RAM
  13c74:  .word 0x20000cac  ; RAM
```
