# func_0x083e4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800083e4) | `0x000083e4` |
| размер кода | 74 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40010800 — периферия (r0)

## Вызовы (callees)

- 0x087da (bl, вне списка функций)
- `func_0x087de` (0x000087de, bl)
- `func_0x10870` (0x00010870, bl)

## Кто вызывает (callers / xrefs)

- `func_0x082b8` (bl @0x000082c4)


## Дизассембляция

```asm
  083e4:  push.w {r4, r5, r6, r7, r8, lr}   
  083e8:  movs r4, #0                       
  083ea:  movs r5, #0                       
  083ec:  movs r6, #0                       
  083ee:  movs r7, #0                       
  083f0:  movs r1, #0x10                    
  083f2:  ldr r0, [pc, #0x3c]               -> периферия
  083f4:  bl #0x87da                        -> 0x087da (вне списка функций)
  083f8:  movs r0, #0x9f                    
  083fa:  bl #0x10870                       -> func_0x10870
  083fe:  movs r0, #0xff                    
  08400:  bl #0x10870                       -> func_0x10870
  08404:  mov r5, r0                        
  08406:  movs r0, #0xff                    
  08408:  bl #0x10870                       -> func_0x10870
  0840c:  mov r6, r0                        
  0840e:  movs r0, #0xff                    
  08410:  bl #0x10870                       -> func_0x10870
  08414:  mov r7, r0                        
  08416:  movs r1, #0x10                    
  08418:  ldr r0, [pc, #0x14]               -> периферия
  0841a:  bl #0x87de                        -> func_0x087de
  0841e:  lsls r0, r5, #0x10                
  08420:  orr.w r0, r0, r6, lsl #8          
  08424:  orr.w r4, r0, r7                  
  08428:  mov r0, r4                        
  0842a:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x08430 (1 слов) — ВНЕ границ функции ---
  08430:  .word 0x40010800  ; периферия
```
