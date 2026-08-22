# func_0x1a628

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a628) | `0x0001a628` |
| размер кода | 12 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200016aa — RAM (r0)

## Вызовы (callees)

- `func_0x1a5f2` (0x0001a5f2, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1c838` (bl @0x0001ca08)
- `func_0x1f71c` (bl @0x000209aa)
- `func_0x1f71c` (bl @0x00020a24)


## Дизассембляция

```asm
  1a628:  push {r4, lr}                     
  1a62a:  mov r1, r0                        
  1a62c:  ldr r0, [pc, #4]                  -> RAM
  1a62e:  bl #0x1a5f2                       -> func_0x1a5f2
  1a632:  pop {r4, pc}                      
  ; --- literal-пул @0x1a634 (1 слов) — ВНЕ границ функции ---
  1a634:  .word 0x200016aa  ; RAM
```
