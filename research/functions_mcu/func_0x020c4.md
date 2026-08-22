# func_0x020c4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800020c4) | `0x000020c4` |
| размер кода | 16 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000162d — RAM (r2)

## Вызовы (callees)

- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  020c4:  push {r4, lr}                     
  020c6:  movs r3, #2                       
  020c8:  ldr r2, [pc, #8]                  -> RAM
  020ca:  movs r1, #0x38                    
  020cc:  movs r0, #8                       
  020ce:  bl #0x1c60                        -> func_0x01c60
  020d2:  pop {r4, pc}                      
  ; --- literal-пул @0x020d4 (1 слов) — ВНЕ границ функции ---
  020d4:  .word 0x2000162d  ; RAM
```
