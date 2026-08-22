# func_0x022b8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800022b8) | `0x000022b8` |
| размер кода | 16 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000161d — RAM (r2)

## Вызовы (callees)

- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  022b8:  push {r4, lr}                     
  022ba:  movs r3, #2                       
  022bc:  ldr r2, [pc, #8]                  -> RAM
  022be:  movs r1, #0x28                    
  022c0:  movs r0, #8                       
  022c2:  bl #0x1c60                        -> func_0x01c60
  022c6:  pop {r4, pc}                      
  ; --- literal-пул @0x022c8 (1 слов) — ВНЕ границ функции ---
  022c8:  .word 0x2000161d  ; RAM
```
