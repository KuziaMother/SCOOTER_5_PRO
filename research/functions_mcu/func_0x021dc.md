# func_0x021dc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800021dc) | `0x000021dc` |
| размер кода | 16 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001607 — RAM (r2)

## Вызовы (callees)

- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0236c` (bl @0x0000236e)


## Дизассембляция

```asm
  021dc:  push {r4, lr}                     
  021de:  movs r3, #2                       
  021e0:  ldr r2, [pc, #8]                  -> RAM
  021e2:  movs r1, #0x12                    
  021e4:  movs r0, #8                       
  021e6:  bl #0x1c60                        -> func_0x01c60
  021ea:  pop {r4, pc}                      
  ; --- literal-пул @0x021ec (1 слов) — ВНЕ границ функции ---
  021ec:  .word 0x20001607  ; RAM
```
