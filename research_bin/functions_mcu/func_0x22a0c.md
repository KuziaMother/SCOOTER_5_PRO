# func_0x22a0c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080022a0c) | `0x00022a0c` |
| размер кода | 48 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00ffffff — прочее (r3)
- 0x20000010 — RAM (r2)
- 0xe000e000 — Cortex-M (NVIC/SCB/SysTick) (r0)

## Вызовы (callees)

- 0x22a30 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x22234` (bl @0x0002223e)
- `func_0x22234` (bl @0x00022252)
- `func_0x22234` (bl @0x00022260)


## Дизассембляция

```asm
  22a0c:  push {r4, lr}                     
  22a0e:  ldr r2, [pc, #0x2c]               -> RAM
  22a10:  ldr r3, [pc, #0x30]               
  22a12:  ldr r2, [r2]                      
  22a14:  muls r0, r2, r0                   
  22a16:  movs r2, #1                       
  22a18:  lsls r2, r2, #0x18                
  22a1a:  subs r2, r2, r0                   
  22a1c:  ldr r0, [pc, #0x20]               -> Cortex-M (NVIC/SCB/SysTick)
  22a1e:  b #0x22a30                        -> 0x22a30 (вне списка функций)
  22a20:  ldr r4, [r0, #0x18]               
  22a22:  orrs r4, r3                       
  22a24:  str r4, [r0, #0x18]               
  22a26:  ldr r4, [r0, #0x18]               
  22a28:  lsls r4, r4, #8                   
  22a2a:  lsrs r4, r4, #8                   
  22a2c:  cmp r4, r2                        
  22a2e:  bhi #0x22a26                      
  22a30:  mov r4, r1                        
  22a32:  subs r1, r1, #1                   
  22a34:  uxth r1, r1                       
  22a36:  cmp r4, #0                        
  22a38:  bne #0x22a20                      
  22a3a:  pop {r4, pc}                      
  ; --- literal-пул @0x22a3c (3 слов) — ВНЕ границ функции ---
  22a3c:  .word 0x20000010  ; RAM
  22a40:  .word 0xe000e000  ; Cortex-M (NVIC/SCB/SysTick)
  22a44:  .word 0x00ffffff
```
