# func_0x0b8dc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b8dc) | `0x0000b8dc` |
| размер кода | 128 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000ef9 — RAM (r0)
- 0x20000efa — RAM (r1)
- 0x20000efc — RAM (r1)

## Вызовы (callees)

- `func_0x09844` (0x00009844, bl)
- `func_0x09874` (0x00009874, bl)
- 0x0b91a (b, вне списка функций)
- 0x0b91c (b, вне списка функций)
- 0x0b94a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0b8fc..0x0b91c` (32 Б); цели из: 0x0b8ec
- `0x0b91c..0x0b94a` (46 Б); цели из: 0x0b904
- `0x0b94a..0x0b95c` (18 Б); цели из: 0x0b932

## Дизассембляция

```asm
  0b8dc:  push {r4, lr}                     
  0b8de:  mov r4, r0                        
  0b8e0:  movs r0, #0                       
  0b8e2:  ldr r1, [pc, #0x78]               -> RAM
  0b8e4:  strb r0, [r1]                     
  0b8e6:  ldrb.w r0, [r4, #0x10c]           
  0b8ea:  cmp r0, #1                        
  0b8ec:  bne #0xb8fc                       
  0b8ee:  movs r0, #2                       
  0b8f0:  strb.w r0, [r4, #0x10c]           
  0b8f4:  movs r1, #1                       
  0b8f6:  ldr r0, [r4]                      
  0b8f8:  bl #0x9844                        -> func_0x09844
  0b8fc:  mov.w r0, #0x10000                
  0b900:  ldr r1, [pc, #0x5c]               -> RAM
  0b902:  str r0, [r1]                      
  0b904:  b #0xb91c                         -> 0x0b91c (вне списка функций)
  0b906:  ldr r1, [pc, #0x58]               -> RAM
  0b908:  ldr r0, [r1]                      
  0b90a:  subs r1, r0, #1                   
  0b90c:  ldr r2, [pc, #0x50]               -> RAM
  0b90e:  str r1, [r2]                      
  0b910:  cbz r0, #0xb918                   
  0b912:  ldrb.w r1, [r4, #0x10c]           
  0b916:  cbnz r1, #0xb91c                  
  0b918:  movs r0, #3                       
  0b91a:  pop {r4, pc}                      
  0b91c:  ldrb.w r0, [r4, #0x10c]           
  0b920:  cmp r0, #4                        
  0b922:  bne #0xb906                       
  0b924:  ldr r0, [pc, #0x3c]               -> RAM
  0b926:  ldrb r0, [r0]                     
  0b928:  cbnz r0, #0xb958                  
  0b92a:  mov.w r0, #0x10000                
  0b92e:  ldr r1, [pc, #0x30]               -> RAM
  0b930:  str r0, [r1]                      
  0b932:  b #0xb94a                         -> 0x0b94a (вне списка функций)
  0b934:  ldr r1, [pc, #0x28]               -> RAM
  0b936:  ldr r0, [r1]                      
  0b938:  subs r1, r0, #1                   
  0b93a:  ldr r2, [pc, #0x24]               -> RAM
  0b93c:  str r1, [r2]                      
  0b93e:  cbz r0, #0xb946                   
  0b940:  ldrb.w r1, [r4, #0x10c]           
  0b944:  cbnz r1, #0xb94a                  
  0b946:  movs r0, #3                       
  0b948:  b #0xb91a                         -> 0x0b91a (вне списка функций)
  0b94a:  mov.w r1, #0x20000                
  0b94e:  ldr r0, [r4]                      
  0b950:  bl #0x9874                        -> func_0x09874
  0b954:  cmp r0, #0                        
  0b956:  bne #0xb934                       
  0b958:  movs r0, #0                       
  0b95a:  b #0xb91a                         -> 0x0b91a (вне списка функций)
  ; --- literal-пул @0x0b95c (3 слов) — ВНЕ границ функции ---
  0b95c:  .word 0x20000efa  ; RAM
  0b960:  .word 0x20000efc  ; RAM
  0b964:  .word 0x20000ef9  ; RAM
```
