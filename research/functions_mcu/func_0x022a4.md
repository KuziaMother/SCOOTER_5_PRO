# func_0x022a4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800022a4) | `0x000022a4` |
| размер кода | 16 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000161b — RAM (r2)

## Вызовы (callees)

- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  022a4:  push {r4, lr}                     
  022a6:  movs r3, #2                       
  022a8:  ldr r2, [pc, #8]                  -> RAM
  022aa:  movs r1, #0x26                    
  022ac:  movs r0, #8                       
  022ae:  bl #0x1c60                        -> func_0x01c60
  022b2:  pop {r4, pc}                      
  ; --- literal-пул @0x022b4 (1 слов) — ВНЕ границ функции ---
  022b4:  .word 0x2000161b  ; RAM
```
