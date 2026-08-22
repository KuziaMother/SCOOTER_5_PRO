# func_0x022f4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800022f4) | `0x000022f4` |
| размер кода | 16 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000162f — RAM (r2)

## Вызовы (callees)

- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- `func_0x110fc` (bl @0x00011238)


## Дизассембляция

```asm
  022f4:  push {r4, lr}                     
  022f6:  movs r3, #2                       
  022f8:  ldr r2, [pc, #8]                  -> RAM
  022fa:  movs r1, #0x3a                    
  022fc:  movs r0, #8                       
  022fe:  bl #0x1c60                        -> func_0x01c60
  02302:  pop {r4, pc}                      
  ; --- literal-пул @0x02304 (1 слов) — ВНЕ границ функции ---
  02304:  .word 0x2000162f  ; RAM
```
