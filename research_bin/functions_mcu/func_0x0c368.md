# func_0x0c368

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c368) | `0x0000c368` |
| размер кода | 172 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000082 — RAM (r0)
- 0x20000088 — RAM (r0)
- 0x20001004 — RAM (r1)

## Вызовы (callees)

- `func_0x07fdc` (0x00007fdc, bl)
- `func_0x08884` (0x00008884, bl)
- `func_0x09a18` (0x00009a18, bl)
- 0x0c40e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e16)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0c384..0x0c3ba` (54 Б); цели из: 0x0c37c
- `0x0c3ba..0x0c3ca` (16 Б); цели из: 0x0c3aa
- `0x0c3ca..0x0c400` (54 Б); цели из: 0x0c3bc
- `0x0c400..0x0c40e` (14 Б); цели из: 0x0c3dc
- `0x0c40e..0x0c414` (6 Б); цели из: 0x0c38e, 0x0c3ec, 0x0c3fe, 0x0c406

## Дизассембляция

```asm
  0c368:  push {r4, lr}                     
  0c36a:  movs r4, #0                       
  0c36c:  ldr r0, [pc, #0xa4]               -> RAM
  0c36e:  ldrb r0, [r0]                     
  0c370:  cbnz r0, #0xc376                  
  0c372:  bl #0x8884                        -> func_0x08884
  0c376:  ldr r0, [pc, #0xa0]               -> RAM
  0c378:  ldrh r0, [r0]                     
  0c37a:  cmp r0, #0x7f                     
  0c37c:  ble #0xc384                       
  0c37e:  movs r0, #0                       
  0c380:  ldr r1, [pc, #0x94]               -> RAM
  0c382:  strh r0, [r1]                     
  0c384:  ldr r0, [pc, #0x8c]               -> RAM
  0c386:  ldrb r0, [r0]                     
  0c388:  and r0, r0, #0x7f                 
  0c38c:  cmp r0, #0                        
  0c38e:  beq #0xc40e                       
  0c390:  ldr r0, [pc, #0x80]               -> RAM
  0c392:  ldrb r0, [r0]                     
  0c394:  ubfx r0, r0, #4, #1               
  0c398:  cbz r0, #0xc3d6                   
  0c39a:  movs r3, #1                       
  0c39c:  movs r2, #0x54                    
  0c39e:  ldr r1, [pc, #0x7c]               -> RAM
  0c3a0:  movs r0, #4                       
  0c3a2:  bl #0x7fdc                        -> func_0x07fdc
  0c3a6:  mov r4, r0                        
  0c3a8:  cmp r4, #1                        
  0c3aa:  bne #0xc3ba                       
  0c3ac:  movs r3, #2                       
  0c3ae:  movs r2, #0x54                    
  0c3b0:  ldr r1, [pc, #0x68]               -> RAM
  0c3b2:  movs r0, #4                       
  0c3b4:  bl #0x7fdc                        -> func_0x07fdc
  0c3b8:  mov r4, r0                        
  0c3ba:  cmp r4, #1                        
  0c3bc:  bne #0xc3ca                       
  0c3be:  ldr r0, [pc, #0x58]               -> RAM
  0c3c0:  ldrh r0, [r0]                     
  0c3c2:  orr r0, r0, #0x10                 
  0c3c6:  ldr r1, [pc, #0x50]               -> RAM
  0c3c8:  strh r0, [r1]                     
  0c3ca:  ldr r0, [pc, #0x48]               -> RAM
  0c3cc:  ldrb r0, [r0]                     
  0c3ce:  bic r0, r0, #0x10                 
  0c3d2:  ldr r1, [pc, #0x40]               -> RAM
  0c3d4:  strb r0, [r1]                     
  0c3d6:  ldr r0, [pc, #0x40]               -> RAM
  0c3d8:  ldrh r0, [r0]                     
  0c3da:  cmp r0, #0x7f                     
  0c3dc:  bne #0xc400                       
  0c3de:  movs r3, #1                       
  0c3e0:  movs r2, #2                       
  0c3e2:  ldr r1, [pc, #0x34]               -> RAM
  0c3e4:  movs r0, #0                       
  0c3e6:  bl #0x7fdc                        -> func_0x07fdc
  0c3ea:  cmp r0, #1                        
  0c3ec:  bne #0xc40e                       
  0c3ee:  movs r3, #2                       
  0c3f0:  mov r2, r3                        
  0c3f2:  ldr r1, [pc, #0x24]               -> RAM
  0c3f4:  movs r0, #0                       
  0c3f6:  bl #0x7fdc                        -> func_0x07fdc
  0c3fa:  bl #0x8884                        -> func_0x08884
  0c3fe:  b #0xc40e                         -> 0x0c40e (вне списка функций)
  0c400:  ldr r0, [pc, #0x14]               -> RAM
  0c402:  ldrh r0, [r0]                     
  0c404:  cmp r0, #0x7f                     
  0c406:  ble #0xc40e                       
  0c408:  movs r0, #0                       
  0c40a:  ldr r1, [pc, #0xc]                -> RAM
  0c40c:  strh r0, [r1]                     
  0c40e:  bl #0x9a18                        -> func_0x09a18
  0c412:  pop {r4, pc}                      
  ; --- literal-пул @0x0c414 (3 слов) — ВНЕ границ функции ---
  0c414:  .word 0x20000088  ; RAM
  0c418:  .word 0x20000082  ; RAM
  0c41c:  .word 0x20001004  ; RAM
```
