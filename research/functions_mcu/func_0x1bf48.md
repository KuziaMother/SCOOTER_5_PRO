# func_0x1bf48

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001bf48) | `0x0001bf48` |
| размер кода | 78 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000154 — RAM (r0)
- 0x48000c00 — периферия (r4)

## Вызовы (callees)

- `func_0x1bedc` (0x0001bedc, bl)
- `func_0x1c0b0` (0x0001c0b0, bl)
- `func_0x1c1ac` (0x0001c1ac, bl)
- `func_0x1d640` (0x0001d640, bl)
- `func_0x22000` (0x00022000, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1bf48:  push {r2, r3, r4, r5, r6, lr}     
  1bf4a:  bl #0x1d640                       -> func_0x1d640
  1bf4e:  bl #0x1c0b0                       -> func_0x1c0b0
  1bf52:  bl #0x1c1ac                       -> func_0x1c1ac
  1bf56:  ldr r0, [pc, #0x40]               -> RAM
  1bf58:  bl #0x1bedc                       -> func_0x1bedc
  1bf5c:  movs r0, #1                       
  1bf5e:  mov r1, sp                        
  1bf60:  strb r0, [r1]                     
  1bf62:  movs r0, #0                       
  1bf64:  strb r0, [r1, #1]                 
  1bf66:  strb r0, [r1, #2]                 
  1bf68:  strb r0, [r1, #3]                 
  1bf6a:  strb r0, [r1, #4]                 
  1bf6c:  strb r0, [r1, #5]                 
  1bf6e:  ldr r4, [pc, #0x2c]               -> периферия
  1bf70:  strb r0, [r1, #6]                 
  1bf72:  ldr r0, [r4, #4]                  
  1bf74:  movs r5, #2                       
  1bf76:  bics r0, r5                       
  1bf78:  str r0, [r4, #4]                  
  1bf7a:  mov r2, sp                        
  1bf7c:  mov r1, r5                        
  1bf7e:  mov r0, r4                        
  1bf80:  bl #0x22000                       -> func_0x22000
  1bf84:  ldr r0, [r4, #4]                  
  1bf86:  bics r0, r5                       
  1bf88:  str r0, [r4, #4]                  
  1bf8a:  mov r2, sp                        
  1bf8c:  movs r1, #1                       
  1bf8e:  mov r0, r4                        
  1bf90:  bl #0x22000                       -> func_0x22000
  1bf94:  pop {r2, r3, r4, r5, r6, pc}      
  ; --- literal-пул @0x1bf98 (2 слов) — ВНЕ границ функции ---
  1bf98:  .word 0x20000154  ; RAM
  1bf9c:  .word 0x48000c00  ; периферия
```
