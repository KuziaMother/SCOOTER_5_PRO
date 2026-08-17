# func_0x1a184

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001a184) | `0x0001a184` |
| размер кода | 164 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x1a080` (0x0001a080, bl)
- `func_0x1a0a0` (0x0001a0a0, bl)
- `func_0x1a16a` (0x0001a16a, bl)
- 0x1a19e (b, вне списка функций)
- 0x1a1e8 (b, вне списка функций)
- 0x1a1ee (b, вне списка функций)
- 0x21b24 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x19c58` (bl @0x00019d1c)
- `func_0x19dbc` (bl @0x00019e80)
- `func_0x19fcc` (bl @0x00019fe6)
- `func_0x19ff4` (bl @0x0001a004)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1a198..0x1a19e` (6 Б); цели из: 0x1a18e
- `0x1a19e..0x1a1e4` (70 Б); цели из: 0x1a196
- `0x1a1e4..0x1a1ec` (8 Б); цели из: 0x1a1b8
- `0x1a1ec..0x1a1ee` (2 Б); цели из: 0x1a1de
- `0x1a1ee..0x1a1f8` (10 Б); цели из: 0x1a1e2
- `0x1a1f8..0x1a214` (28 Б); цели из: 0x1a1be
- `0x1a214..0x1a228` (20 Б); цели из: 0x1a20c

## Дизассембляция

```asm
  1a184:  push {r4, r5, r6, r7, lr}         
  1a186:  push {r0, r1, r2, r3, r4}         
  1a188:  sub sp, #8                        
  1a18a:  mov r5, r0                        
  1a18c:  movs r4, r1                       
  1a18e:  beq #0x1a198                      
  1a190:  mov r0, r1                        
  1a192:  bl #0x21b24                       -> 0x21b24 (вне списка функций)
  1a196:  b #0x1a19e                        -> 0x1a19e (вне списка функций)
  1a198:  bl #0x21b24                       -> 0x21b24 (вне списка функций)
  1a19c:  adds r0, #0x20                    
  1a19e:  mov r2, r0                        
  1a1a0:  str r0, [sp]                      
  1a1a2:  mov r1, r4                        
  1a1a4:  mov r0, r5                        
  1a1a6:  bl #0x1a080                       -> func_0x1a080
  1a1aa:  ldr r3, [sp, #0x10]               
  1a1ac:  ldr r2, [sp, #0x14]               
  1a1ae:  mov r4, r0                        
  1a1b0:  mov r7, r1                        
  1a1b2:  orrs r0, r3                       
  1a1b4:  orrs r1, r2                       
  1a1b6:  orrs r0, r1                       
  1a1b8:  beq #0x1a1e4                      
  1a1ba:  mov r0, r3                        
  1a1bc:  orrs r0, r2                       
  1a1be:  beq #0x1a1f8                      
  1a1c0:  ldr r0, [sp]                      
  1a1c2:  movs r1, #0x40                    
  1a1c4:  subs r2, r1, r0                   
  1a1c6:  mov r0, r3                        
  1a1c8:  ldr r1, [sp, #0x14]               
  1a1ca:  bl #0x1a0a0                       -> func_0x1a0a0
  1a1ce:  mov r5, r0                        
  1a1d0:  mov r6, r1                        
  1a1d2:  ldr r2, [sp]                      
  1a1d4:  ldr r1, [sp, #0x14]               
  1a1d6:  ldr r0, [sp, #0x10]               
  1a1d8:  bl #0x1a080                       -> func_0x1a080
  1a1dc:  orrs r0, r1                       
  1a1de:  beq #0x1a1ec                      
  1a1e0:  movs r0, #1                       
  1a1e2:  b #0x1a1ee                        -> 0x1a1ee (вне списка функций)
  1a1e4:  mov r0, r4                        
  1a1e6:  mov r1, r7                        
  1a1e8:  add sp, #0x1c                     
  1a1ea:  pop {r4, r5, r6, r7, pc}          
  1a1ec:  movs r0, #0                       
  1a1ee:  asrs r1, r0, #0x1f                
  1a1f0:  orrs r5, r0                       
  1a1f2:  orrs r6, r1                       
  1a1f4:  orrs r4, r5                       
  1a1f6:  orrs r7, r6                       
  1a1f8:  ldr r1, [sp]                      
  1a1fa:  ldr r0, [sp, #0x38]               
  1a1fc:  lsls r3, r4, #0x15                
  1a1fe:  subs r0, r0, r1                   
  1a200:  lsls r1, r7, #0x15                
  1a202:  lsrs r4, r4, #0xb                 
  1a204:  movs r2, #0                       
  1a206:  orrs r4, r1                       
  1a208:  lsrs r5, r7, #0xb                 
  1a20a:  adds r0, #0xa                     
  1a20c:  bpl #0x1a214                      
  1a20e:  movs r0, #0                       
  1a210:  mov r1, r0                        
  1a212:  b #0x1a1e8                        -> 0x1a1e8 (вне списка функций)
  1a214:  lsls r1, r0, #0x14                
  1a216:  adds r0, r2, r4                   
  1a218:  adcs r1, r5                       
  1a21a:  ldr r4, [sp, #0x30]               
  1a21c:  ldr r5, [sp, #0x34]               
  1a21e:  adds r0, r0, r4                   
  1a220:  adcs r1, r5                       
  1a222:  bl #0x1a16a                       -> func_0x1a16a
  1a226:  b #0x1a1e8                        -> 0x1a1e8 (вне списка функций)
```
