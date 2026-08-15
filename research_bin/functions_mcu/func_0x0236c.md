# func_0x0236c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000236c) | `0x0000236c` |
| размер кода | 42 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a73 — RAM (r1)
- 0x20000a75 — RAM (r0)
- 0x20000a76 — RAM (r1)

## Вызовы (callees)

- `func_0x021dc` (0x000021dc, bl)
- 0x023b4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  0236c:  push {r4, lr}                     
  0236e:  bl #0x21dc                        -> func_0x021dc
  02372:  cbz r0, #0x2396                   
  02374:  movs r0, #0                       
  02376:  ldr r1, [pc, #0x40]               -> RAM
  02378:  strb r0, [r1]                     
  0237a:  ldr r0, [pc, #0x40]               -> RAM
  0237c:  ldrb r0, [r0]                     
  0237e:  adds r0, r0, #1                   
  02380:  uxtb r0, r0                       
  02382:  ldr r1, [pc, #0x38]               -> RAM
  02384:  strb r0, [r1]                     
  02386:  cmp r0, #4                        
  02388:  blt #0x23b4                       
  0238a:  movs r0, #0                       
  0238c:  strb r0, [r1]                     
  0238e:  movs r0, #1                       
  02390:  ldr r1, [pc, #0x2c]               -> RAM
  02392:  strb r0, [r1]                     
  02394:  b #0x23b4                         -> 0x023b4 (вне списка функций)
  ; --- literal-пул @0x023b8 (3 слов) — ВНЕ границ функции ---
  023b8:  .word 0x20000a76  ; RAM
  023bc:  .word 0x20000a75  ; RAM
  023c0:  .word 0x20000a73  ; RAM
```
