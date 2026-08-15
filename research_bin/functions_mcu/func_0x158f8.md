# func_0x158f8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800158f8) | `0x000158f8` |
| размер кода | 22 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b8c — RAM (r1)
- 0x20001fac — RAM (r1)

## Вызовы (callees)

- `func_0x15ffc` (0x00015ffc, bl)

## Кто вызывает (callers / xrefs)

- `func_0x15b84` (bl @0x00015b86)


## Дизассембляция

```asm
  158f8:  push {r4, lr}                     
  158fa:  movs r0, #1                       
  158fc:  ldr r1, [pc, #0x10]               -> RAM
  158fe:  strb r0, [r1]                     
  15900:  movs r0, #0xa                     
  15902:  bl #0x15ffc                       -> func_0x15ffc
  15906:  movs r0, #1                       
  15908:  ldr r1, [pc, #8]                  -> RAM
  1590a:  strb r0, [r1, #3]                 
  1590c:  pop {r4, pc}                      
  ; --- literal-пул @0x15910 (2 слов) — ВНЕ границ функции ---
  15910:  .word 0x20000b8c  ; RAM
  15914:  .word 0x20001fac  ; RAM
```
