# func_0x21c0c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080021c0c) | `0x00021c0c` |
| размер кода | 6 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000028 — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x225f4` (bl @0x00022688)
- `func_0x225f4` (bl @0x000226ac)
- `func_0x225f4` (bl @0x000226ca)
- `func_0x225f4` (bl @0x000226d2)
- `func_0x225f4` (bl @0x00022714)
- `func_0x225f4` (bl @0x0002271c)
- `func_0x225f4` (bl @0x00022760)
- `func_0x225f4` (bl @0x00022776)
- `func_0x225f4` (bl @0x00022788)
- `func_0x225f4` (bl @0x00022796)
- `func_0x225f4` (bl @0x000227a0)


## Дизассембляция

```asm
  21c0c:  ldr r0, [pc, #4]                  -> RAM
  21c0e:  ldr r0, [r0, #4]                  
  21c10:  bx lr                             
  ; --- literal-пул @0x21c14 (1 слов) — ВНЕ границ функции ---
  21c14:  .word 0x20000028  ; RAM
```
