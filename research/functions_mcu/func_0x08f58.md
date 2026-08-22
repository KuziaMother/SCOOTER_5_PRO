# func_0x08f58

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008f58) | `0x00008f58` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000fc7 — RAM (r0)
- 0x20001359 — RAM (r2)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x063b8` (bl @0x00006540)
- `func_0x069e4` (bl @0x00006a8c)
- `func_0x069e4` (bl @0x00006af6)
- `func_0x069e4` (bl @0x00006b20)
- `func_0x069e4` (bl @0x00006b3e)
- `func_0x069e4` (bl @0x00006b9a)
- `func_0x069e4` (bl @0x00006bb8)
- `func_0x069e4` (bl @0x00006bd6)
- `func_0x069e4` (bl @0x00006c60)
- `func_0x06fc0` (bl @0x00006ffe)
- `func_0x0799c` (bl @0x000079a4)
- `func_0x0e200` (bl @0x0000e22e)
- `func_0x0e200` (bl @0x0000e242)


## Дизассембляция

```asm
  08f58:  movs r1, #0                       
  08f5a:  ldr r0, [pc, #0x18]               -> RAM
  08f5c:  ldrsb.w r0, [r0, #1]              
  08f60:  uxth r1, r0                       
  08f62:  sxth r0, r1                       
  08f64:  ldr r2, [pc, #0x10]               -> RAM
  08f66:  strh.w r0, [r2, #5]               
  08f6a:  mov r0, r2                        
  08f6c:  ldrsh.w r0, [r0, #5]              
  08f70:  bx lr                             
  ; --- literal-пул @0x08f74 (2 слов) — ВНЕ границ функции ---
  08f74:  .word 0x20000fc7  ; RAM
  08f78:  .word 0x20001359  ; RAM
```
