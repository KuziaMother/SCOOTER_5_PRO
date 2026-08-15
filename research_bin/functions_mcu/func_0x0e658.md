# func_0x0e658

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e658) | `0x0000e658` |
| размер кода | 136 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000035 — RAM (r0)
- 0x20000a49 — RAM (r0)
- 0x20000a62 — RAM (r0)

## Вызовы (callees)

- `func_0x063b8` (0x000063b8, bl)
- `func_0x06618` (0x00006618, bl)
- `func_0x06838` (0x00006838, bl)
- `func_0x069e4` (0x000069e4, bl)
- `func_0x06e50` (0x00006e50, bl)
- `func_0x0799c` (0x0000799c, bl)
- `func_0x07a30` (0x00007a30, bl)
- 0x0e6c6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0e670..0x0e692` (34 Б); цели из: 0x0e666
- `0x0e692..0x0e6c6` (52 Б); цели из: 0x0e682
- `0x0e6c6..0x0e6de` (24 Б); цели из: 0x0e698, 0x0e69e, 0x0e6a4, 0x0e6aa…
- `0x0e6de..0x0e6e0` (2 Б); цели из: 0x0e66e, 0x0e676, 0x0e6d8

## Дизассембляция

```asm
  0e658:  push {r4, lr}                     
  0e65a:  ldr r0, [pc, #0x84]               -> RAM
  0e65c:  ldrb r0, [r0]                     
  0e65e:  cbz r0, #0xe670                   
  0e660:  ldr r0, [pc, #0x7c]               -> RAM
  0e662:  ldrb r0, [r0]                     
  0e664:  cmp r0, #1                        
  0e666:  beq #0xe670                       
  0e668:  ldr r0, [pc, #0x74]               -> RAM
  0e66a:  ldrb r0, [r0]                     
  0e66c:  cmp r0, #2                        
  0e66e:  bne #0xe6de                       
  0e670:  ldr r0, [pc, #0x70]               -> RAM
  0e672:  ldrb r0, [r0]                     
  0e674:  cmp r0, #1                        
  0e676:  bne #0xe6de                       
  0e678:  bl #0x6618                        -> func_0x06618
  0e67c:  ldr r0, [pc, #0x68]               -> RAM
  0e67e:  ldrb r0, [r0]                     
  0e680:  cmp r0, #0xa                      
  0e682:  bhs #0xe692                       
  0e684:  tbb [pc, r0]                      
  0e688:  lsrs r1, r1, #0x10                
  0e68a:  asrs r7, r1, #8                   
  0e68c:  adds r5, r2, r0                   
  0e68e:  adds r3, r3, #0                   
  0e690:  subs r5, r3, #0                   
  0e692:  movs r0, #0                       
  0e694:  ldr r1, [pc, #0x50]               -> RAM
  0e696:  strb r0, [r1]                     
  0e698:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e69a:  bl #0x6e50                        -> func_0x06e50
  0e69e:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6a0:  bl #0x63b8                        -> func_0x063b8
  0e6a4:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6a6:  bl #0x799c                        -> func_0x0799c
  0e6aa:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6ac:  bl #0x7a30                        -> func_0x07a30
  0e6b0:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6b2:  bl #0x69e4                        -> func_0x069e4
  0e6b6:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6b8:  bl #0x6838                        -> func_0x06838
  0e6bc:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6be:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6c0:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6c2:  b #0xe6c6                         -> 0x0e6c6 (вне списка функций)
  0e6c4:  nop                               
  0e6c6:  nop                               
  0e6c8:  ldr r0, [pc, #0x1c]               -> RAM
  0e6ca:  ldrb r0, [r0]                     
  0e6cc:  adds r0, r0, #1                   
  0e6ce:  ldr r1, [pc, #0x18]               -> RAM
  0e6d0:  strb r0, [r1]                     
  0e6d2:  mov r0, r1                        
  0e6d4:  ldrb r0, [r0]                     
  0e6d6:  cmp r0, #0xa                      
  0e6d8:  blt #0xe6de                       
  0e6da:  movs r0, #0                       
  0e6dc:  strb r0, [r1]                     
  0e6de:  pop {r4, pc}                      
  ; --- literal-пул @0x0e6e0 (3 слов) — ВНЕ границ функции ---
  0e6e0:  .word 0x20000035  ; RAM
  0e6e4:  .word 0x20000a49  ; RAM
  0e6e8:  .word 0x20000a62  ; RAM
```
