# func_0x1a838

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a838) | `0x0001a838` |
| размер кода | 32 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x04c11db7 — прочее (r1)

## Вызовы (callees)

- 0x1a84e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1f71c` (bl @0x00020fc6)
- `func_0x1f71c` (bl @0x00020fe8)
- `func_0x1f71c` (bl @0x00021006)


## Дизассембляция

```asm
  1a838:  mov r3, r0                        
  1a83a:  lsls r0, r1, #0x18                
  1a83c:  movs r2, #0                       
  1a83e:  ldr r1, [pc, #0x18]               
  1a840:  eors r0, r3                       
  1a842:  cmp r0, #0                        
  1a844:  bge #0x1a84c                      
  1a846:  lsls r0, r0, #1                   
  1a848:  eors r0, r1                       
  1a84a:  b #0x1a84e                        -> 0x1a84e (вне списка функций)
  1a84c:  lsls r0, r0, #1                   
  1a84e:  adds r2, r2, #1                   
  1a850:  uxtb r2, r2                       
  1a852:  cmp r2, #8                        
  1a854:  blo #0x1a842                      
  1a856:  bx lr                             
  ; --- literal-пул @0x1a858 (1 слов) — ВНЕ границ функции ---
  1a858:  .word 0x04c11db7
```
