# func_0x080ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800080ac) | `0x000080ac` |
| размер кода | 84 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08003000 — flash-mirror @0x03000 (r1)
- 0x0801ffff — flash-mirror @0x1ffff (r2)

## Вызовы (callees)

- `func_0x07e98` (0x00007e98, bl)
- 0x080f0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0acce` (bl @0x0000ad36)
- `func_0x0acce` (bl @0x0000ad42)
- `func_0x0acce` (bl @0x0000adfe)
- `func_0x0acce` (bl @0x0000ae0a)
- `func_0x0ad9e` (bl @0x0000adfe)
- `func_0x0ad9e` (bl @0x0000ae0a)
- `func_0x15df4` (bl @0x00015ec2)


## Дизассембляция

```asm
  080ac:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, lr}
  080b0:  mov r7, r0                        
  080b2:  mov r5, r1                        
  080b4:  mov r4, r2                        
  080b6:  mov.w r8, #0                      
  080ba:  mov sb, r8                        
  080bc:  mov sl, r8                        
  080be:  mov fp, r8                        
  080c0:  movs r6, #0                       
  080c2:  ubfx r1, r7, #0, #0xb             
  080c6:  cbnz r1, #0x80ee                  
  080c8:  cbz r5, #0x80ee                   
  080ca:  cbz r4, #0x80ee                   
  080cc:  cmp.w r4, #0x800                  
  080d0:  bgt #0x80ee                       
  080d2:  asrs r1, r4, #0x1f                
  080d4:  add.w r1, r4, r1, lsr #30         
  080d8:  asrs r1, r1, #2                   
  080da:  sub.w r1, r4, r1, lsl #2          
  080de:  cbnz r1, #0x80ee                  
  080e0:  adds r1, r7, r4                   
  080e2:  ldr r2, [pc, #0x74]               -> flash-mirror @0x1ffff
  080e4:  cmp r1, r2                        
  080e6:  bhs #0x80ee                       
  080e8:  ldr r1, [pc, #0x70]               -> flash-mirror @0x03000
  080ea:  cmp r7, r1                        
  080ec:  bhs #0x80f4                       
  080ee:  movs r0, #0                       
  080f0:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, pc}
  080f4:  mov r0, r7                        
  080f6:  bl #0x7e98                        -> func_0x07e98
  080fa:  cbnz r0, #0x8100                  
  080fc:  movs r0, #0                       
  080fe:  b #0x80f0                         -> 0x080f0 (вне списка функций)
  ; --- literal-пул @0x08158 (2 слов) — ВНЕ границ функции ---
  08158:  .word 0x0801ffff  ; flash-mirror @0x1ffff
  0815c:  .word 0x08003000  ; flash-mirror @0x03000
```
