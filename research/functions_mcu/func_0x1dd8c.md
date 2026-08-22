# func_0x1dd8c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001dd8c) | `0x0001dd8c` |
| размер кода | 128 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1a7ac` (bl @0x0001a814)


## Дизассембляция

```asm
  1dd8c:  push {r4, r5, r6, r7, lr}         
  1dd8e:  mov ip, r0                        
  1dd90:  movs r5, #0                       
  1dd92:  lsls r7, r5, #2                   
  1dd94:  mov r1, ip                        
  1dd96:  adds r2, r7, r1                   
  1dd98:  mov r0, ip                        
  1dd9a:  ldrb r0, [r0, r7]                 
  1dd9c:  ldrb r1, [r2, #1]                 
  1dd9e:  mov lr, r0                        
  1dda0:  ldrb r3, [r2, #2]                 
  1dda2:  ldrb r6, [r2, #3]                 
  1dda4:  mov r4, lr                        
  1dda6:  eors r4, r1                       
  1dda8:  eors r3, r6                       
  1ddaa:  mov r1, r4                        
  1ddac:  eors r1, r3                       
  1ddae:  lsls r3, r4, #1                   
  1ddb0:  lsrs r4, r4, #7                   
  1ddb2:  movs r6, #0x1b                    
  1ddb4:  muls r4, r6, r4                   
  1ddb6:  eors r3, r4                       
  1ddb8:  eors r3, r1                       
  1ddba:  eors r0, r3                       
  1ddbc:  mov r3, ip                        
  1ddbe:  strb r0, [r3, r7]                 
  1ddc0:  ldrb r3, [r2, #1]                 
  1ddc2:  ldrb r4, [r2, #2]                 
  1ddc4:  mov r7, r3                        
  1ddc6:  eors r3, r4                       
  1ddc8:  lsls r0, r3, #1                   
  1ddca:  lsrs r3, r3, #7                   
  1ddcc:  muls r3, r6, r3                   
  1ddce:  eors r0, r3                       
  1ddd0:  eors r0, r1                       
  1ddd2:  eors r7, r0                       
  1ddd4:  strb r7, [r2, #1]                 
  1ddd6:  ldrb r3, [r2, #3]                 
  1ddd8:  mov r0, r4                        
  1ddda:  eors r0, r3                       
  1dddc:  lsls r6, r0, #1                   
  1ddde:  lsrs r7, r0, #7                   
  1dde0:  movs r0, #0x1b                    
  1dde2:  muls r7, r0, r7                   
  1dde4:  eors r6, r7                       
  1dde6:  eors r6, r1                       
  1dde8:  eors r4, r6                       
  1ddea:  mov r0, lr                        
  1ddec:  mov r6, r3                        
  1ddee:  eors r6, r0                       
  1ddf0:  strb r4, [r2, #2]                 
  1ddf2:  lsls r0, r6, #1                   
  1ddf4:  lsrs r4, r6, #7                   
  1ddf6:  movs r6, #0x1b                    
  1ddf8:  muls r4, r6, r4                   
  1ddfa:  eors r0, r4                       
  1ddfc:  eors r0, r1                       
  1ddfe:  eors r3, r0                       
  1de00:  adds r5, r5, #1                   
  1de02:  uxtb r5, r5                       
  1de04:  strb r3, [r2, #3]                 
  1de06:  cmp r5, #4                        
  1de08:  blo #0x1dd92                      
  1de0a:  pop {r4, r5, r6, r7, pc}          
```
