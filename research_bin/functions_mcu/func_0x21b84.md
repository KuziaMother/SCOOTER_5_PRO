# func_0x21b84

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080021b84) | `0x00021b84` |
| размер кода | 60 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xe000e400 — Cortex-M (NVIC/SCB/SysTick) (r0)
- 0xe000ed00 — Cortex-M (NVIC/SCB/SysTick) (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1e2ca` (bl @0x0001e2de)
- `func_0x21c18` (bl @0x00021c34)
- `func_0x23544` (bl @0x0002357c)


## Дизассембляция

```asm
  21b84:  lsls r3, r0, #0x1e                
  21b86:  movs r2, #0xff                    
  21b88:  lsrs r3, r3, #0x1b                
  21b8a:  lsls r2, r3                       
  21b8c:  lsls r1, r1, #0x1e                
  21b8e:  lsrs r1, r1, #0x18                
  21b90:  lsls r1, r3                       
  21b92:  cmp r0, #0                        
  21b94:  blt #0x21ba8                      
  21b96:  lsrs r3, r0, #2                   
  21b98:  ldr r0, [pc, #0x24]               -> Cortex-M (NVIC/SCB/SysTick)
  21b9a:  lsls r3, r3, #2                   
  21b9c:  adds r3, r3, r0                   
  21b9e:  ldr r0, [r3]                      
  21ba0:  bics r0, r2                       
  21ba2:  orrs r0, r1                       
  21ba4:  str r0, [r3]                      
  21ba6:  bx lr                             
  21ba8:  lsls r0, r0, #0x1c                
  21baa:  lsrs r0, r0, #0x1c                
  21bac:  subs r0, #8                       
  21bae:  lsrs r3, r0, #2                   
  21bb0:  ldr r0, [pc, #0x10]               -> Cortex-M (NVIC/SCB/SysTick)
  21bb2:  lsls r3, r3, #2                   
  21bb4:  adds r3, r3, r0                   
  21bb6:  ldr r0, [r3, #0x1c]               
  21bb8:  bics r0, r2                       
  21bba:  orrs r0, r1                       
  21bbc:  str r0, [r3, #0x1c]               
  21bbe:  bx lr                             
  ; --- literal-пул @0x21bc0 (2 слов) — ВНЕ границ функции ---
  21bc0:  .word 0xe000e400  ; Cortex-M (NVIC/SCB/SysTick)
  21bc4:  .word 0xe000ed00  ; Cortex-M (NVIC/SCB/SysTick)
```
