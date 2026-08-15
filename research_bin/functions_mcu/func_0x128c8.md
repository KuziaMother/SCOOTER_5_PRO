# func_0x128c8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800128c8) | `0x000128c8` |
| размер кода | 18 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000044 — RAM (r0)
- 0x2000004a — RAM (r2)

## Вызовы (callees)

- `func_0x050b0` (0x000050b0, bl)
- `func_0x1093c` (0x0001093c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  128c8:  push {lr}                         
  128ca:  ldr r2, [pc, #0x10]               -> RAM
  128cc:  movs r1, #2                       
  128ce:  ldr r0, [pc, #0x10]               -> RAM
  128d0:  bl #0x50b0                        -> func_0x050b0
  128d4:  bl #0x1093c                       -> func_0x1093c
  128d8:  pop {pc}                          
  ; --- literal-пул @0x128dc (2 слов) — ВНЕ границ функции ---
  128dc:  .word 0x2000004a  ; RAM
  128e0:  .word 0x20000044  ; RAM
```
