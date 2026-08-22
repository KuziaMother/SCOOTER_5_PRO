# func_0x1be1c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001be1c) | `0x0001be1c` |
| размер кода | 174 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000838 — RAM (r1)
- 0x40012440 — периферия (r1)
- 0x40012c40 — периферия (r1)
- 0xffff8ad0 — прочее (r2)

## Вызовы (callees)

- 0x1be8c (b, вне списка функций)
- 0x1beac (b, вне списка функций)
- 0x1beba (b, вне списка функций)
- 0x21b52 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a938` (bl @0x0001a94a)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1be8c..0x1bea6` (26 Б); цели из: 0x1be24, 0x1be54, 0x1be70
- `0x1bea6..0x1beac` (6 Б); цели из: 0x1bea0
- `0x1beac..0x1beb4` (8 Б); цели из: 0x1bea4, 0x1bea8
- `0x1beb4..0x1beba` (6 Б); цели из: 0x1beae
- `0x1beba..0x1bec2` (8 Б); цели из: 0x1beb2, 0x1beb6
- `0x1bec2..0x1beca` (8 Б); цели из: 0x1bebc

## Дизассембляция

```asm
  1be1c:  push {r4, r5, lr}                 
  1be1e:  ldr r1, [pc, #0xac]               -> периферия
  1be20:  ldr r1, [r1, #0x14]               
  1be22:  lsls r1, r1, #0x10                
  1be24:  bpl #0x1be8c                      
  1be26:  ldrh r2, [r0, #2]                 
  1be28:  ldr r1, [pc, #0xa4]               -> периферия
  1be2a:  movs r3, r2                       
  1be2c:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1be30:  cmp r6, #7                        
  1be32:  movs r1, #0x13                    
  1be34:  lsls r1, r4, #0x14                
  1be36:  asrs r5, r0, #0xc                 
  1be38:  movs r6, r5                       
  1be3a:  ldr r2, [r1, #0x28]               
  1be3c:  ldrh r3, [r0, #0x18]              
  1be3e:  subs r2, r2, r3                   
  1be40:  lsls r2, r2, #4                   
  1be42:  str r2, [r0, #0xc]                
  1be44:  ldr r1, [r1, #0x2c]               
  1be46:  ldrh r3, [r0, #0x1a]              
  1be48:  subs r1, r1, r3                   
  1be4a:  lsls r1, r1, #4                   
  1be4c:  str r1, [r0, #0x10]               
  1be4e:  adds r1, r2, r1                   
  1be50:  rsbs r1, r1, #0                   
  1be52:  str r1, [r0, #0x14]               
  1be54:  b #0x1be8c                        -> 0x1be8c (вне списка функций)
  1be56:  ldr r2, [r1, #0x2c]               
  1be58:  ldrh r3, [r0, #0x1a]              
  1be5a:  subs r2, r2, r3                   
  1be5c:  lsls r2, r2, #4                   
  1be5e:  str r2, [r0, #0x10]               
  1be60:  ldr r1, [r1, #0x30]               
  1be62:  ldrh r3, [r0, #0x1c]              
  1be64:  subs r1, r1, r3                   
  1be66:  lsls r1, r1, #4                   
  1be68:  str r1, [r0, #0x14]               
  1be6a:  adds r1, r2, r1                   
  1be6c:  rsbs r1, r1, #0                   
  1be6e:  str r1, [r0, #0xc]                
  1be70:  b #0x1be8c                        -> 0x1be8c (вне списка функций)
  1be72:  ldr r2, [r1, #0x28]               
  1be74:  ldrh r3, [r0, #0x18]              
  1be76:  subs r2, r2, r3                   
  1be78:  lsls r2, r2, #4                   
  1be7a:  str r2, [r0, #0xc]                
  1be7c:  ldr r1, [r1, #0x30]               
  1be7e:  ldrh r3, [r0, #0x1c]              
  1be80:  subs r1, r1, r3                   
  1be82:  lsls r1, r1, #4                   
  1be84:  str r1, [r0, #0x14]               
  1be86:  adds r1, r2, r1                   
  1be88:  rsbs r1, r1, #0                   
  1be8a:  str r1, [r0, #0x10]               
  1be8c:  ldr r1, [pc, #0x44]               -> RAM
  1be8e:  ldr r3, [r0, #0xc]                
  1be90:  str r3, [r1]                      
  1be92:  ldr r4, [r0, #0x10]               
  1be94:  str r4, [r1, #4]                  
  1be96:  ldr r5, [r0, #0x14]               
  1be98:  ldr r2, [pc, #0x3c]               
  1be9a:  str r5, [r1, #8]                  
  1be9c:  rsbs r0, r2, #0                   
  1be9e:  cmp r3, r2                        
  1bea0:  bge #0x1bea6                      
  1bea2:  str r2, [r1]                      
  1bea4:  b #0x1beac                        -> 0x1beac (вне списка функций)
  1bea6:  cmp r3, r0                        
  1bea8:  ble #0x1beac                      
  1beaa:  str r0, [r1]                      
  1beac:  cmp r4, r2                        
  1beae:  bge #0x1beb4                      
  1beb0:  str r2, [r1, #4]                  
  1beb2:  b #0x1beba                        -> 0x1beba (вне списка функций)
  1beb4:  cmp r4, r0                        
  1beb6:  ble #0x1beba                      
  1beb8:  str r0, [r1, #4]                  
  1beba:  cmp r5, r2                        
  1bebc:  bge #0x1bec2                      
  1bebe:  str r2, [r1, #8]                  
  1bec0:  pop {r4, r5, pc}                  
  1bec2:  cmp r5, r0                        
  1bec4:  ble #0x1bec0                      
  1bec6:  str r0, [r1, #8]                  
  1bec8:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x1becc (4 слов) — ВНЕ границ функции ---
  1becc:  .word 0x40012c40  ; периферия
  1bed0:  .word 0x40012440  ; периферия
  1bed4:  .word 0x20000838  ; RAM
  1bed8:  .word 0xffff8ad0
```
