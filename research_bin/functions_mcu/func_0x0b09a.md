# func_0x0b09a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b09a) | `0x0000b09a` |
| размер кода | 244 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40005400 — периферия (r1)

## Вызовы (callees)

- `func_0x097ca` (0x000097ca, bl)
- `func_0x0982c` (0x0000982c, bl)
- `func_0x0985c` (0x0000985c, bl)
- `func_0x098c8` (0x000098c8, bl)
- 0x0b0c0 (b, вне списка функций)
- 0x0b126 (b, вне списка функций)
- 0x0b188 (b, вне списка функций)
- 0x0b2ec (b, вне списка функций)
- 0x0c664 (bl, вне списка функций)
- `func_0x0c6a4` (0x0000c6a4, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0b0b8..0x0b0c0` (8 Б); цели из: 0x0b0a2
- `0x0b0c0..0x0b116` (86 Б); цели из: 0x0b0b6
- `0x0b116..0x0b126` (16 Б); цели из: 0x0b102
- `0x0b126..0x0b15e` (56 Б); цели из: 0x0b114
- `0x0b15e..0x0b180` (34 Б); цели из: 0x0b142
- `0x0b180..0x0b188` (8 Б); цели из: 0x0b160
- `0x0b188..0x0b18e` (6 Б); цели из: 0x0b15c, 0x0b17e

## Дизассембляция

```asm
  0b09a:  push {r0, r1, r2, r3, r4, lr}     
  0b09c:  ldrb.w r0, [sp, #0x2b]            
  0b0a0:  cmp r0, #2                        
  0b0a2:  beq #0xb0b8                       
  0b0a4:  movs r0, #0                       
  0b0a6:  strh.w r0, [sp, #8]               
  0b0aa:  ldr r0, [sp, #0x18]               
  0b0ac:  ldrh r0, [r0]                     
  0b0ae:  bic r0, r0, #0x800                
  0b0b2:  ldr r1, [sp, #0x18]               
  0b0b4:  strh r0, [r1]                     
  0b0b6:  b #0xb0c0                         -> 0x0b0c0 (вне списка функций)
  0b0b8:  ldrb.w r0, [sp, #0x2a]            
  0b0bc:  strh.w r0, [sp, #8]               
  0b0c0:  movs r0, #0                       
  0b0c2:  strh.w r0, [sp, #4]               
  0b0c6:  movw r0, #0xbfff                  
  0b0ca:  strh.w r0, [sp, #6]               
  0b0ce:  mov.w r0, #0x400                  
  0b0d2:  strh.w r0, [sp, #0xa]             
  0b0d6:  ldrh.w r0, [sp, #0x48]            
  0b0da:  strh.w r0, [sp, #0xc]             
  0b0de:  ldr r0, [sp, #0x2c]               
  0b0e0:  str r0, [sp]                      
  0b0e2:  mov r1, sp                        
  0b0e4:  ldr r0, [sp, #0x18]               
  0b0e6:  bl #0x98c8                        -> func_0x098c8
  0b0ea:  movs r1, #1                       
  0b0ec:  ldr r0, [sp, #0x18]               
  0b0ee:  bl #0x982c                        -> func_0x0982c
  0b0f2:  pop {r0, r1, r2, r3, r4}          
  0b0f4:  ldr pc, [sp], #0x14               
  0b0f8:  push {r0, r1, r2, r3}             
  0b0fa:  push {r4, lr}                     
  0b0fc:  ldr r1, [pc, #0x34]               -> периферия
  0b0fe:  ldr r0, [sp, #8]                  
  0b100:  cmp r0, r1                        
  0b102:  bne #0xb116                       
  0b104:  movs r1, #1                       
  0b106:  movs r0, #8                       
  0b108:  bl #0xc6a4                        -> func_0x0c6a4
  0b10c:  movs r1, #1                       
  0b10e:  lsls r0, r1, #0x15                
  0b110:  bl #0xc664                        -> 0x0c664 (вне списка функций)
  0b114:  b #0xb126                         -> 0x0b126 (вне списка функций)
  0b116:  movs r1, #1                       
  0b118:  movs r0, #4                       
  0b11a:  bl #0xc6a4                        -> func_0x0c6a4
  0b11e:  movs r1, #1                       
  0b120:  lsls r0, r1, #0x16                
  0b122:  bl #0xc664                        -> 0x0c664 (вне списка функций)
  0b126:  movs r1, #1                       
  0b128:  mov r0, r1                        
  0b12a:  bl #0xc6a4                        -> func_0x0c6a4
  0b12e:  pop {r4}                          
  0b130:  ldr pc, [sp], #0x14               
  0b134:  strb r0, [r0, r0]                 
  0b136:  ands r0, r0                       
  0b138:  push {r0, r1, r2, r3}             
  0b13a:  push {r4, r5, r6, lr}             
  0b13c:  ldrd r4, r5, [sp, #0x44]          
  0b140:  cmp r5, #1                        
  0b142:  bne #0xb15e                       
  0b144:  movs r1, #0                       
  0b146:  ldr r0, [sp, #0x10]               
  0b148:  bl #0x97ca                        -> func_0x097ca
  0b14c:  ldr r0, [sp, #0x10]               
  0b14e:  ldrh r0, [r0, #0x14]              
  0b150:  ldr r0, [sp, #0x10]               
  0b152:  ldrh r0, [r0, #0x18]              
  0b154:  movs r1, #1                       
  0b156:  ldr r0, [sp, #0x10]               
  0b158:  bl #0x985c                        -> func_0x0985c
  0b15c:  b #0xb188                         -> 0x0b188 (вне списка функций)
  0b15e:  cmp r5, #2                        
  0b160:  bne #0xb180                       
  0b162:  ldr r0, [sp, #0x10]               
  0b164:  ldrh r0, [r0]                     
  0b166:  orr r0, r0, #0x800                
  0b16a:  ldr r1, [sp, #0x10]               
  0b16c:  strh r0, [r1]                     
  0b16e:  ldr r0, [sp, #0x10]               
  0b170:  ldrh r0, [r0, #0x14]              
  0b172:  ldr r0, [sp, #0x10]               
  0b174:  ldrh r0, [r0, #0x18]              
  0b176:  movs r1, #0                       
  0b178:  ldr r0, [sp, #0x10]               
  0b17a:  bl #0x97ca                        -> func_0x097ca
  0b17e:  b #0xb188                         -> 0x0b188 (вне списка функций)
  0b180:  ldr r0, [sp, #0x10]               
  0b182:  ldrh r0, [r0, #0x14]              
  0b184:  ldr r0, [sp, #0x10]               
  0b186:  ldrh r0, [r0, #0x18]              
  0b188:  mov.w r6, #0x10000                
  0b18c:  b #0xb2ec                         -> 0x0b2ec (вне списка функций)
  ; --- literal-пул @0x0b134 (1 слов) ---
  0b134:  .word 0x40005400  ; периферия
```
