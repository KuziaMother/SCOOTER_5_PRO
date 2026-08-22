# func_0x1a052

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a052) | `0x0001a052` |
| размер кода | 36 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000003ff — данные @0x003ff (r3)
- 0xfffffbcd — прочее (r1)

## Вызовы (callees)

- `func_0x1a0a0` (0x0001a0a0, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1a052:  push {r4, lr}                     
  1a054:  lsrs r2, r2, #0x15                
  1a056:  cmp r2, r3                        
  1a058:  bge #0x1a05e                      
  1a05a:  movs r0, #0                       
  1a05c:  pop {r4, pc}                      
  1a05e:  ldr r3, [pc, #0x18]               -> данные @0x003ff
  1a060:  adds r3, #0x34                    
  1a062:  cmp r2, r3                        
  1a064:  bgt #0x1a06e                      
  1a066:  subs r2, r3, r2                   
  1a068:  bl #0x1a0a0                       -> func_0x1a0a0
  1a06c:  pop {r4, pc}                      
  1a06e:  ldr r1, [pc, #0xc]                
  1a070:  adds r1, r2, r1                   
  1a072:  lsls r0, r1                       
  1a074:  pop {r4, pc}                      
  ; --- literal-пул @0x1a078 (2 слов) — ВНЕ границ функции ---
  1a078:  .word 0x000003ff  ; данные @0x003ff
  1a07c:  .word 0xfffffbcd
```
