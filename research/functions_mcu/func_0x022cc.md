# func_0x022cc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800022cc) | `0x000022cc` |
| размер кода | 16 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000161f — RAM (r2)

## Вызовы (callees)

- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  022cc:  push {r4, lr}                     
  022ce:  movs r3, #2                       
  022d0:  ldr r2, [pc, #8]                  -> RAM
  022d2:  movs r1, #0x2a                    
  022d4:  movs r0, #8                       
  022d6:  bl #0x1c60                        -> func_0x01c60
  022da:  pop {r4, pc}                      
  ; --- literal-пул @0x022dc (1 слов) — ВНЕ границ функции ---
  022dc:  .word 0x2000161f  ; RAM
```
