# func_0x1238c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001238c) | `0x0001238c` |
| размер кода | 48 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000035 — RAM (r0)

## Вызовы (callees)

- `func_0x0a7ec` (0x0000a7ec, bl)
- `func_0x0c098` (0x0000c098, bl)

## Кто вызывает (callers / xrefs)

- `func_0x128e4` (bl @0x000128f0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x123a4..0x123a8` (4 Б); цели из: 0x1239a
- `0x123a8..0x123ba` (18 Б); цели из: 0x123a2
- `0x123ba..0x123bc` (2 Б); цели из: 0x123b4

## Дизассембляция

```asm
  1238c:  push {r4, lr}                     
  1238e:  ldr r0, [pc, #0x2c]               -> RAM
  12390:  ldrb r0, [r0]                     
  12392:  cbz r0, #0x123a4                  
  12394:  ldr r0, [pc, #0x24]               -> RAM
  12396:  ldrb r0, [r0]                     
  12398:  cmp r0, #1                        
  1239a:  beq #0x123a4                      
  1239c:  ldr r0, [pc, #0x1c]               -> RAM
  1239e:  ldrb r0, [r0]                     
  123a0:  cmp r0, #2                        
  123a2:  bne #0x123a8                      
  123a4:  bl #0xa7ec                        -> func_0x0a7ec
  123a8:  ldr r0, [pc, #0x10]               -> RAM
  123aa:  ldrb r0, [r0]                     
  123ac:  cbz r0, #0x123b6                  
  123ae:  ldr r0, [pc, #0xc]                -> RAM
  123b0:  ldrb r0, [r0]                     
  123b2:  cmp r0, #1                        
  123b4:  bne #0x123ba                      
  123b6:  bl #0xc098                        -> func_0x0c098
  123ba:  pop {r4, pc}                      
  ; --- literal-пул @0x123bc (1 слов) — ВНЕ границ функции ---
  123bc:  .word 0x20000035  ; RAM
```
