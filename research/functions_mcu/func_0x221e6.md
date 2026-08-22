# func_0x221e6

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800221e6) | `0x000221e6` |
| размер кода | 78 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x2222c (b, вне списка функций)
- 0x235b0 (bl, вне списка функций)
- `func_0x2360c` (0x0002360c, bl)
- 0x23688 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1c838` (bl @0x0001c8ce)
- `func_0x1c838` (bl @0x0001c93a)
- `func_0x1c838` (bl @0x0001c954)
- `func_0x1c838` (bl @0x0001ca48)
- `func_0x1c838` (bl @0x0001ca90)
- `func_0x1c838` (bl @0x0001caa0)
- `func_0x1c838` (bl @0x0001cdb0)
- `func_0x1c838` (bl @0x0001cdc0)
- `func_0x1c838` (bl @0x0001cdd0)
- `func_0x1c838` (bl @0x0001cde0)
- `func_0x21a08` (bl @0x00021a2c)
- `func_0x21a08` (bl @0x00021a46)
- `func_0x21a08` (bl @0x00021a60)
- `func_0x21a08` (bl @0x00021a7a)
- `func_0x21a08` (bl @0x00021a94)
- `func_0x21a08` (bl @0x00021ad4)
- `func_0x21a08` (bl @0x00021ae4)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x2221c..0x2222a` (14 Б); цели из: 0x22214
- `0x2222a..0x22230` (6 Б); цели из: 0x221f6
- `0x22230..0x22234` (4 Б); цели из: 0x22228

## Дизассембляция

```asm
  221e6:  push {r4, r5, lr}                 
  221e8:  sub sp, #0x1c                     
  221ea:  mov r4, r0                        
  221ec:  movs r5, #1                       
  221ee:  mov r0, sp                        
  221f0:  strb r5, [r0]                     
  221f2:  str r1, [sp, #0x14]               
  221f4:  lsls r0, r4, #0x1e                
  221f6:  bne #0x2222a                      
  221f8:  cpsid i                           
  221fa:  bl #0x23688                       -> 0x23688 (вне списка функций)
  221fe:  mov r0, sp                        
  22200:  strh r5, [r0, #0xc]               
  22202:  add r0, sp, #0x14                 
  22204:  str r0, [sp, #0x10]               
  22206:  mvns r0, r4                       
  22208:  str r0, [sp, #8]                  
  2220a:  str r4, [sp, #4]                  
  2220c:  add r0, sp, #4                    
  2220e:  bl #0x2360c                       -> func_0x2360c
  22212:  cmp r0, #1                        
  22214:  beq #0x2221c                      
  22216:  movs r0, #0                       
  22218:  mov r1, sp                        
  2221a:  strb r0, [r1]                     
  2221c:  bl #0x235b0                       -> 0x235b0 (вне списка функций)
  22220:  cpsie i                           
  22222:  mov r0, sp                        
  22224:  ldrb r0, [r0]                     
  22226:  cmp r0, #0                        
  22228:  beq #0x22230                      
  2222a:  movs r0, #0                       
  2222c:  add sp, #0x1c                     
  2222e:  pop {r4, r5, pc}                  
  22230:  movs r0, #1                       
  22232:  b #0x2222c                        -> 0x2222c (вне списка функций)
```
