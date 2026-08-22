# func_0x123c0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800123c0) | `0x000123c0` |
| размер кода | 10 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000dd8 — RAM (r0)

## Вызовы (callees)

- `func_0x0b854` (0x0000b854, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  123c0:  push {r4, lr}                     
  123c2:  ldr r0, [pc, #8]                  -> RAM
  123c4:  bl #0xb854                        -> func_0x0b854
  123c8:  pop {r4, pc}                      
  ; --- literal-пул @0x123cc (1 слов) — ВНЕ границ функции ---
  123cc:  .word 0x20000dd8  ; RAM
```
