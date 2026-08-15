# func_0x0c304

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c304) | `0x0000c304` |
| размер кода | 96 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f95 — RAM (r1)

## Вызовы (callees)

- 0x0c354 (b, вне списка функций)
- 0x0c35c (b, вне списка функций)
- `func_0x0cee0` (0x0000cee0, bl)
- `func_0x155ac` (0x000155ac, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03b2a` (bl @0x00003b2c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0c33c..0x0c356` (26 Б); цели из: 0x0c32e
- `0x0c356..0x0c35c` (6 Б); цели из: 0x0c33a
- `0x0c35c..0x0c364` (8 Б); цели из: 0x0c30c

## Дизассембляция

```asm
  0c304:  push {r3, r4, r5, lr}             
  0c306:  movs r0, #0                       
  0c308:  str r0, [sp]                      
  0c30a:  movs r4, #0                       
  0c30c:  b #0xc35c                         -> 0x0c35c (вне списка функций)
  0c30e:  movs r3, #2                       
  0c310:  mov r2, sp                        
  0c312:  movw r1, #0x91a0                  
  0c316:  movs r0, #8                       
  0c318:  bl #0xcee0                        -> func_0x0cee0
  0c31c:  cbz r0, #0xc358                   
  0c31e:  ldrh.w r0, [sp]                   
  0c322:  ldr r1, [pc, #0x40]               -> RAM
  0c324:  strh r0, [r1, #0x18]              
  0c326:  ldrh.w r0, [sp]                   
  0c32a:  cmp.w r0, #0x7d00                 
  0c32e:  blt #0xc33c                       
  0c330:  ldrh.w r0, [sp]                   
  0c334:  movw r1, #0x8ca0                  
  0c338:  cmp r0, r1                        
  0c33a:  ble #0xc356                       
  0c33c:  movw r0, #0x84d0                  
  0c340:  str r0, [sp]                      
  0c342:  movs r3, #2                       
  0c344:  ldrh.w r2, [sp]                   
  0c348:  movw r1, #0x91a0                  
  0c34c:  movs r0, #8                       
  0c34e:  bl #0x155ac                       -> func_0x155ac
  0c352:  cbz r0, #0xc358                   
  0c354:  pop {r3, r4, r5, pc}              
  0c356:  b #0xc354                         -> 0x0c354 (вне списка функций)
  0c358:  adds r0, r4, #1                   
  0c35a:  uxtb r4, r0                       
  0c35c:  cmp r4, #3                        
  0c35e:  blt #0xc30e                       
  0c360:  nop                               
  0c362:  b #0xc354                         -> 0x0c354 (вне списка функций)
  ; --- literal-пул @0x0c364 (1 слов) — ВНЕ границ функции ---
  0c364:  .word 0x20000f95  ; RAM
```
