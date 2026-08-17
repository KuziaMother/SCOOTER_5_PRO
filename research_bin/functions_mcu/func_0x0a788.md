# func_0x0a788

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000a788) | `0x0000a788` |
| размер кода | 96 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f95 — RAM (r1)

## Вызовы (callees)

- 0x0a7d8 (b, вне списка функций)
- 0x0a7e0 (b, вне списка функций)
- `func_0x0cee0` (0x0000cee0, bl)
- `func_0x155ac` (0x000155ac, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03b2a` (bl @0x00003b34)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0a7c0..0x0a7da` (26 Б); цели из: 0x0a7b2
- `0x0a7da..0x0a7e0` (6 Б); цели из: 0x0a7be
- `0x0a7e0..0x0a7e8` (8 Б); цели из: 0x0a790

## Дизассембляция

```asm
  0a788:  push {r3, r4, r5, lr}             
  0a78a:  movs r0, #0                       
  0a78c:  str r0, [sp]                      
  0a78e:  movs r4, #0                       
  0a790:  b #0xa7e0                         -> 0x0a7e0 (вне списка функций)
  0a792:  movs r3, #2                       
  0a794:  mov r2, sp                        
  0a796:  movw r1, #0x91a4                  
  0a79a:  movs r0, #8                       
  0a79c:  bl #0xcee0                        -> func_0x0cee0
  0a7a0:  cbz r0, #0xa7dc                   
  0a7a2:  ldrh.w r0, [sp]                   
  0a7a6:  ldr r1, [pc, #0x40]               -> RAM
  0a7a8:  strh r0, [r1, #0x1c]              
  0a7aa:  ldrh.w r0, [sp]                   
  0a7ae:  cmp.w r0, #0x7d00                 
  0a7b2:  blt #0xa7c0                       
  0a7b4:  ldrh.w r0, [sp]                   
  0a7b8:  movw r1, #0x8ca0                  
  0a7bc:  cmp r0, r1                        
  0a7be:  ble #0xa7da                       
  0a7c0:  movw r0, #0x84d0                  
  0a7c4:  str r0, [sp]                      
  0a7c6:  movs r3, #2                       
  0a7c8:  ldrh.w r2, [sp]                   
  0a7cc:  movw r1, #0x91a4                  
  0a7d0:  movs r0, #8                       
  0a7d2:  bl #0x155ac                       -> func_0x155ac
  0a7d6:  cbz r0, #0xa7dc                   
  0a7d8:  pop {r3, r4, r5, pc}              
  0a7da:  b #0xa7d8                         -> 0x0a7d8 (вне списка функций)
  0a7dc:  adds r0, r4, #1                   
  0a7de:  uxtb r4, r0                       
  0a7e0:  cmp r4, #3                        
  0a7e2:  blt #0xa792                       
  0a7e4:  nop                               
  0a7e6:  b #0xa7d8                         -> 0x0a7d8 (вне списка функций)
  ; --- literal-пул @0x0a7e8 (1 слов) — ВНЕ границ функции ---
  0a7e8:  .word 0x20000f95  ; RAM
```
