# func_0x19fcc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080019fcc) | `0x00019fcc` |
| размер кода | 34 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000433 — данные @0x00433 (r3)

## Вызовы (callees)

- `func_0x1a184` (0x0001a184, bl)

## Кто вызывает (callers / xrefs)

- `func_0x22274` (bl @0x00022306)


## Дизассембляция

```asm
  19fcc:  push {r1, r2, r3, lr}             
  19fce:  asrs r2, r0, #0x1f                
  19fd0:  lsrs r1, r0, #0x1f                
  19fd2:  eors r0, r2                       
  19fd4:  lsls r2, r1, #0x1f                
  19fd6:  adds r0, r0, r1                   
  19fd8:  movs r1, #0                       
  19fda:  ldr r3, [pc, #0x14]               -> данные @0x00433
  19fdc:  str r3, [sp, #8]                  
  19fde:  str r2, [sp, #4]                  
  19fe0:  str r1, [sp]                      
  19fe2:  mov r2, r1                        
  19fe4:  mov r3, r1                        
  19fe6:  bl #0x1a184                       -> func_0x1a184
  19fea:  add sp, #0xc                      
  19fec:  pop {pc}                          
  ; --- literal-пул @0x19ff0 (1 слов) — ВНЕ границ функции ---
  19ff0:  .word 0x00000433  ; данные @0x00433
```
