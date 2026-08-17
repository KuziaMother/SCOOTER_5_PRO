# func_0x106b8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800106b8) | `0x000106b8` |
| размер кода | 28 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40013000 — периферия (r0)

## Вызовы (callees)

- `func_0x0c6a4` (0x0000c6a4, bl)
- `func_0x106a0` (0x000106a0, bl)
- `func_0x106d8` (0x000106d8, bl)

## Кто вызывает (callers / xrefs)

- `func_0x10770` (bl @0x0001077a)


## Дизассембляция

```asm
  106b8:  push {r4, lr}                     
  106ba:  movs r1, #0                       
  106bc:  ldr r0, [pc, #0x14]               -> периферия
  106be:  bl #0x106a0                       -> func_0x106a0
  106c2:  ldr r0, [pc, #0x10]               -> периферия
  106c4:  bl #0x106d8                       -> func_0x106d8
  106c8:  movs r1, #0                       
  106ca:  mov.w r0, #0x1000                 
  106ce:  bl #0xc6a4                        -> func_0x0c6a4
  106d2:  pop {r4, pc}                      
  ; --- literal-пул @0x106d4 (1 слов) — ВНЕ границ функции ---
  106d4:  .word 0x40013000  ; периферия
```
