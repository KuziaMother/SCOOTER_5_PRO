# func_0x0f40c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f40c) | `0x0000f40c` |
| размер кода | 116 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019d8e — flash-mirror @0x19d8e (r1)
- 0x20000a2a — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r0)

## Вызовы (callees)

- 0x0f438 (b, вне списка функций)
- 0x0f480 (b, вне списка функций)
- 0x0f4d8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11978` (bl @0x0001197e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0f42e..0x0f438` (10 Б); цели из: 0x0f420
- `0x0f438..0x0f478` (64 Б); цели из: 0x0f42c
- `0x0f478..0x0f480` (8 Б); цели из: 0x0f43e, 0x0f44a

## Дизассембляция

```asm
  0f40c:  ldr r0, [pc, #0x198]              -> RAM
  0f40e:  ldrb r0, [r0, #2]                 
  0f410:  ubfx r0, r0, #4, #1               
  0f414:  cbnz r0, #0xf476                  
  0f416:  ldr r0, [pc, #0x194]              -> RAM
  0f418:  ldrh r0, [r0, #8]                 
  0f41a:  ldr r1, [pc, #0x190]              -> RAM
  0f41c:  ldrh r1, [r1, #6]                 
  0f41e:  cmp r0, r1                        
  0f420:  ble #0xf42e                       
  0f422:  ldr r0, [pc, #0x188]              -> RAM
  0f424:  ldrh r0, [r0, #8]                 
  0f426:  ldr r1, [pc, #0x184]              -> RAM
  0f428:  ldrh r1, [r1, #6]                 
  0f42a:  subs r0, r0, r1                   
  0f42c:  b #0xf438                         -> 0x0f438 (вне списка функций)
  0f42e:  ldr r0, [pc, #0x17c]              -> RAM
  0f430:  ldrh r0, [r0, #6]                 
  0f432:  ldr r1, [pc, #0x178]              -> RAM
  0f434:  ldrh r1, [r1, #8]                 
  0f436:  subs r0, r0, r1                   
  0f438:  ldr r1, [pc, #0x174]              -> flash-mirror @0x19d8e
  0f43a:  ldrh r1, [r1, #0x12]              
  0f43c:  cmp r0, r1                        
  0f43e:  blt #0xf478                       
  0f440:  ldr r0, [pc, #0x168]              -> RAM
  0f442:  ldrh r0, [r0, #6]                 
  0f444:  movw r1, #0xc1c                   
  0f448:  cmp r0, r1                        
  0f44a:  ble #0xf478                       
  0f44c:  ldr r0, [pc, #0x164]              -> RAM
  0f44e:  ldrh r0, [r0]                     
  0f450:  adds r0, r0, #1                   
  0f452:  ldr r1, [pc, #0x160]              -> RAM
  0f454:  strh r0, [r1]                     
  0f456:  ldr r0, [pc, #0x158]              -> flash-mirror @0x19d8e
  0f458:  ldrh r0, [r0, #0x16]              
  0f45a:  ldrh r1, [r1]                     
  0f45c:  cmp r0, r1                        
  0f45e:  bgt #0xf4d8                       
  0f460:  ldr r0, [pc, #0x144]              -> RAM
  0f462:  ldrb r0, [r0, #2]                 
  0f464:  bic r0, r0, #0x10                 
  0f468:  adds r0, #0x10                    
  0f46a:  ldr r1, [pc, #0x13c]              -> RAM
  0f46c:  strb r0, [r1, #2]                 
  0f46e:  movs r0, #0                       
  0f470:  ldr r1, [pc, #0x140]              -> RAM
  0f472:  strh r0, [r1]                     
  0f474:  b #0xf4d8                         -> 0x0f4d8 (вне списка функций)
  0f476:  b #0xf480                         -> 0x0f480 (вне списка функций)
  0f478:  movs r0, #0                       
  0f47a:  ldr r1, [pc, #0x138]              -> RAM
  0f47c:  strh r0, [r1]                     
  0f47e:  b #0xf4d8                         -> 0x0f4d8 (вне списка функций)
  ; --- literal-пул @0x0f5a8 (4 слов) — ВНЕ границ функции ---
  0f5a8:  .word 0x20000f70  ; RAM
  0f5ac:  .word 0x20000f95  ; RAM
  0f5b0:  .word 0x08019d8e  ; flash-mirror @0x19d8e
  0f5b4:  .word 0x20000a2a  ; RAM
```
