# func_0x0a8c4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000a8c4) | `0x0000a8c4` |
| размер кода | 66 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801c800 — flash-mirror @0x1c800 (r7)
- 0x0801d000 — flash-mirror @0x1d000 (r7)

## Вызовы (callees)

- `func_0x07fd4` (0x00007fd4, bl)
- 0x0a8e0 (b, вне списка функций)
- 0x0a8f2 (b, вне списка функций)
- 0x0a8fe (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0abf0` (bl @0x0000ac06)
- `func_0x0abf0` (bl @0x0000ac0e)
- `func_0x0acce` (bl @0x0000adac)
- `func_0x0ad9e` (bl @0x0000adac)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0a8de..0x0a8e0` (2 Б); цели из: 0x0a8d8
- `0x0a8e0..0x0a8f6` (22 Б); цели из: 0x0a8d4, 0x0a8dc
- `0x0a8f6..0x0a8fe` (8 Б); цели из: 0x0a8ee
- `0x0a8fe..0x0a906` (8 Б); цели из: 0x0a8e2

## Дизассембляция

```asm
  0a8c4:  push.w {r4, r5, r6, r7, r8, lr}   
  0a8c8:  mov r5, r0                        
  0a8ca:  movs r6, #0                       
  0a8cc:  movs r4, #0                       
  0a8ce:  movs r7, #0                       
  0a8d0:  cbnz r5, #0xa8d6                  
  0a8d2:  ldr r7, [pc, #0x34]               -> flash-mirror @0x1c800
  0a8d4:  b #0xa8e0                         -> 0x0a8e0 (вне списка функций)
  0a8d6:  cmp r5, #1                        
  0a8d8:  bne #0xa8de                       
  0a8da:  ldr r7, [pc, #0x30]               -> flash-mirror @0x1d000
  0a8dc:  b #0xa8e0                         -> 0x0a8e0 (вне списка функций)
  0a8de:  ldr r7, [pc, #0x28]               -> flash-mirror @0x1c800
  0a8e0:  movs r4, #0                       
  0a8e2:  b #0xa8fe                         -> 0x0a8fe (вне списка функций)
  0a8e4:  add.w r0, r7, r4, lsl #5          
  0a8e8:  bl #0x7fd4                        -> func_0x07fd4
  0a8ec:  cmp r0, #0xaa                     
  0a8ee:  beq #0xa8f6                       
  0a8f0:  mov r0, r6                        
  0a8f2:  pop.w {r4, r5, r6, r7, r8, pc}    
  0a8f6:  adds r0, r6, #1                   
  0a8f8:  uxtb r6, r0                       
  0a8fa:  adds r0, r4, #1                   
  0a8fc:  uxtb r4, r0                       
  0a8fe:  cmp r4, #0x40                     
  0a900:  blo #0xa8e4                       
  0a902:  mov r0, r6                        
  0a904:  b #0xa8f2                         -> 0x0a8f2 (вне списка функций)
  ; --- literal-пул @0x0a908 (2 слов) — ВНЕ границ функции ---
  0a908:  .word 0x0801c800  ; flash-mirror @0x1c800
  0a90c:  .word 0x0801d000  ; flash-mirror @0x1d000
```
