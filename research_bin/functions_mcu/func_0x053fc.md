# func_0x053fc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800053fc) | `0x000053fc` |
| размер кода | 68 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200007d5 — RAM (r1)

## Вызовы (callees)

- 0x05422 (b, вне списка функций)
- `func_0x0583c` (0x0000583c, bl)
- `func_0x05dd8` (0x00005dd8, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  053fc:  push {r2, r3, r4, r5, r6, lr}     
  053fe:  mov r5, r0                        
  05400:  movs r0, #0                       
  05402:  str r0, [sp, #4]                  
  05404:  mov r4, r5                        
  05406:  ldrb r0, [r4, #2]                 
  05408:  ldr r1, [pc, #0x34]               -> RAM
  0540a:  bl #0x583c                        -> func_0x0583c
  0540e:  mov r6, r0                        
  05410:  ldr r0, [pc, #0x2c]               -> RAM
  05412:  ldrb r0, [r0]                     
  05414:  cbz r0, #0x5420                   
  05416:  ldrb r0, [r4, #3]                 
  05418:  ldr r1, [r6]                      
  0541a:  ldrb r1, [r1, #8]                 
  0541c:  cmp r0, r1                        
  0541e:  ble #0x5424                       
  05420:  movs r0, #0                       
  05422:  pop {r2, r3, r4, r5, r6, pc}      
  05424:  ldr r0, [r6]                      
  05426:  ldrb r0, [r0, #8]                 
  05428:  strb r0, [r4, #4]                 
  0542a:  ldrb r0, [r4, #4]                 
  0542c:  str r0, [sp, #4]                  
  0542e:  str r6, [sp]                      
  05430:  ldrb r1, [r4]                     
  05432:  adds r3, r4, #5                   
  05434:  add r2, sp, #4                    
  05436:  movs r0, #0                       
  05438:  bl #0x5dd8                        -> func_0x05dd8
  0543c:  movs r0, #1                       
  0543e:  b #0x5422                         -> 0x05422 (вне списка функций)
  ; --- literal-пул @0x05440 (1 слов) — ВНЕ границ функции ---
  05440:  .word 0x200007d5  ; RAM
```
