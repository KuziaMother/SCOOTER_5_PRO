# func_0x1de5e

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001de5e) | `0x0001de5e` |
| размер кода | 70 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x19968 (bl, вне списка функций)
- `func_0x19ab0` (0x00019ab0, bl)
- 0x19b5a (bl, вне списка функций)
- 0x19b62 (bl, вне списка функций)
- `func_0x19bdc` (0x00019bdc, bl)
- 0x19fa8 (bl, вне списка функций)
- `func_0x19fbe` (0x00019fbe, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1a638` (bl @0x0001a660)
- `func_0x1de0c` (bl @0x0001de34)
- `func_0x1df84` (bl @0x0001dfac)


## Дизассембляция

```asm
  1de5e:  push {r3, r4, r5, r6, r7, lr}     
  1de60:  mov r5, r1                        
  1de62:  mov r6, r0                        
  1de64:  subs r1, r2, r6                   
  1de66:  subs r0, r5, r3                   
  1de68:  ldr r7, [sp, #0x18]               
  1de6a:  bl #0x19968                       -> 0x19968 (вне списка функций)
  1de6e:  bl #0x19fbe                       -> func_0x19fbe
  1de72:  mov r4, r0                        
  1de74:  mov r0, r5                        
  1de76:  bl #0x19fbe                       -> func_0x19fbe
  1de7a:  mov r5, r0                        
  1de7c:  mov r0, r6                        
  1de7e:  bl #0x19fa8                       -> 0x19fa8 (вне списка функций)
  1de82:  mov r1, r4                        
  1de84:  bl #0x19b62                       -> 0x19b62 (вне списка функций)
  1de88:  mov r1, r5                        
  1de8a:  bl #0x19ab0                       -> func_0x19ab0
  1de8e:  mov r5, r0                        
  1de90:  mov r0, r7                        
  1de92:  bl #0x19fbe                       -> func_0x19fbe
  1de96:  mov r1, r5                        
  1de98:  bl #0x19b5a                       -> 0x19b5a (вне списка функций)
  1de9c:  mov r1, r4                        
  1de9e:  bl #0x19bdc                       -> func_0x19bdc
  1dea2:  pop {r3, r4, r5, r6, r7, pc}      
```
