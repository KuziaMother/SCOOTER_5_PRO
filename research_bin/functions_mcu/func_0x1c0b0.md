# func_0x1c0b0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001c0b0) | `0x0001c0b0` |
| размер кода | 238 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x04040403 — прочее (r1)
- 0x0e1c6104 — прочее (r2)
- 0x40012400 — периферия (r4)

## Вызовы (callees)

- 0x19a9a (bl, вне списка функций)
- 0x21c74 (bl, вне списка функций)
- `func_0x21ca8` (0x00021ca8, bl)
- `func_0x21e18` (0x00021e18, bl)
- 0x21fb8 (bl, вне списка функций)
- `func_0x23544` (0x00023544, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1bf48` (bl @0x0001bf4e)


## Дизассембляция

```asm
  1c0b0:  push {r4, r5, r6, r7, lr}         
  1c0b2:  sub sp, #0x64                     
  1c0b4:  movs r1, #0x50                    
  1c0b6:  mov r0, sp                        
  1c0b8:  bl #0x19a9a                       -> 0x19a9a (вне списка функций)
  1c0bc:  ldr r4, [pc, #0xe0]               -> периферия
  1c0be:  movs r5, #0                       
  1c0c0:  mov r0, sp                        
  1c0c2:  str r4, [sp]                      
  1c0c4:  strb r5, [r0, #4]                 
  1c0c6:  strb r5, [r0, #5]                 
  1c0c8:  strb r5, [r0, #8]                 
  1c0ca:  movs r6, #3                       
  1c0cc:  strb r6, [r0, #0xa]               
  1c0ce:  strb r6, [r0, #0xb]               
  1c0d0:  bl #0x21fb8                       -> 0x21fb8 (вне списка функций)
  1c0d4:  mov r0, sp                        
  1c0d6:  bl #0x21ca8                       -> func_0x21ca8
  1c0da:  str r5, [sp, #0x50]               
  1c0dc:  str r5, [sp, #0x58]               
  1c0de:  str r5, [sp, #0x5c]               
  1c0e0:  movs r1, #0xc                     
  1c0e2:  add r0, sp, #0x40                 
  1c0e4:  strb r1, [r0, #0x10]              
  1c0e6:  strb r6, [r0, #0x1c]              
  1c0e8:  movs r7, #1                       
  1c0ea:  strb r7, [r0, #0x11]              
  1c0ec:  movs r5, #4                       
  1c0ee:  add r1, sp, #0x50                 
  1c0f0:  mov r0, sp                        
  1c0f2:  str r5, [sp, #0x54]               
  1c0f4:  bl #0x21e18                       -> func_0x21e18
  1c0f8:  movs r1, #0xb                     
  1c0fa:  add r0, sp, #0x40                 
  1c0fc:  strb r1, [r0, #0x10]              
  1c0fe:  movs r1, #2                       
  1c100:  strb r1, [r0, #0x11]              
  1c102:  add r1, sp, #0x50                 
  1c104:  mov r0, sp                        
  1c106:  str r5, [sp, #0x54]               
  1c108:  bl #0x21e18                       -> func_0x21e18
  1c10c:  movs r1, #0xa                     
  1c10e:  add r0, sp, #0x40                 
  1c110:  strb r1, [r0, #0x10]              
  1c112:  strb r6, [r0, #0x11]              
  1c114:  add r1, sp, #0x50                 
  1c116:  mov r0, sp                        
  1c118:  str r5, [sp, #0x54]               
  1c11a:  bl #0x21e18                       -> func_0x21e18
  1c11e:  movs r1, #0xf                     
  1c120:  add r0, sp, #0x40                 
  1c122:  strb r1, [r0, #0x10]              
  1c124:  strb r5, [r0, #0x11]              
  1c126:  add r1, sp, #0x50                 
  1c128:  mov r0, sp                        
  1c12a:  str r5, [sp, #0x54]               
  1c12c:  bl #0x21e18                       -> func_0x21e18
  1c130:  ldr r0, [r4, #0x20]               
  1c132:  ldr r1, [pc, #0x70]               
  1c134:  orrs r0, r1                       
  1c136:  str r0, [r4, #0x20]               
  1c138:  ldr r1, [r4, #0x24]               
  1c13a:  ldr r0, [pc, #0x68]               
  1c13c:  adds r0, r0, #1                   
  1c13e:  orrs r1, r0                       
  1c140:  str r1, [r4, #0x24]               
  1c142:  ldr r1, [r4, #0x28]               
  1c144:  orrs r1, r0                       
  1c146:  str r1, [r4, #0x28]               
  1c148:  ldr r1, [r4, #0x2c]               
  1c14a:  orrs r1, r0                       
  1c14c:  str r1, [r4, #0x2c]               
  1c14e:  ldr r0, [pc, #0x50]               -> периферия
  1c150:  adds r0, #0x40                    
  1c152:  ldr r1, [r0]                      
  1c154:  ldr r2, [pc, #0x50]               
  1c156:  orrs r1, r2                       
  1c158:  str r1, [r0]                      
  1c15a:  ldr r1, [r0, #4]                  
  1c15c:  movs r2, #9                       
  1c15e:  orrs r1, r2                       
  1c160:  str r1, [r0, #4]                  
  1c162:  ldr r1, [r4, #0x1c]               
  1c164:  orrs r1, r7                       
  1c166:  str r1, [r4, #0x1c]               
  1c168:  ldr r2, [r0, #0x14]               
  1c16a:  movs r1, #0x40                    
  1c16c:  orrs r2, r1                       
  1c16e:  str r2, [r0, #0x14]               
  1c170:  ldr r0, [r4]                      
  1c172:  orrs r0, r1                       
  1c174:  str r0, [r4]                      
  1c176:  movs r2, #1                       
  1c178:  mov r1, r2                        
  1c17a:  movs r0, #0xc                     
  1c17c:  bl #0x23544                       -> func_0x23544
  1c180:  movs r1, #0x20                    
  1c182:  mov r0, sp                        
  1c184:  bl #0x21c74                       -> 0x21c74 (вне списка функций)
  1c188:  movs r1, #4                       
  1c18a:  mov r0, sp                        
  1c18c:  bl #0x21c74                       -> 0x21c74 (вне списка функций)
  1c190:  ldr r0, [sp]                      
  1c192:  ldr r0, [r0, #0x18]               
  1c194:  ldr r1, [sp]                      
  1c196:  orrs r0, r7                       
  1c198:  str r0, [r1, #0x18]               
  1c19a:  add sp, #0x64                     
  1c19c:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1c1a0 (3 слов) — ВНЕ границ функции ---
  1c1a0:  .word 0x40012400  ; периферия
  1c1a4:  .word 0x04040403
  1c1a8:  .word 0x0e1c6104
```
