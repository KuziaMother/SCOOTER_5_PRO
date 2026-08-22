# func_0x0d670

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d670) | `0x0000d670` |
| размер кода | 110 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f64 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x08938` (0x00008938, bl)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x0ab0c` (0x0000ab0c, bl)
- 0x0accc (bl, вне списка функций)
- 0x0d6a4 (b, вне списка функций)
- 0x0d6a8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04508` (bl @0x00004538)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d6a0..0x0d6a4` (4 Б); цели из: 0x0d69c
- `0x0d6a4..0x0d6a8` (4 Б); цели из: 0x0d692
- `0x0d6a8..0x0d6da` (50 Б); цели из: 0x0d69e
- `0x0d6da..0x0d6de` (4 Б); цели из: 0x0d68e

## Дизассембляция

```asm
  0d670:  push {r4, r5, lr}                 
  0d672:  sub sp, #0x54                     
  0d674:  movs r4, #0                       
  0d676:  movs r1, #0x30                    
  0d678:  add r0, sp, #0x24                 
  0d67a:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0d67e:  movs r5, #0                       
  0d680:  bl #0x8938                        -> func_0x08938
  0d684:  mov r4, r0                        
  0d686:  ldr r0, [pc, #0x58]               -> RAM
  0d688:  ldr.w r0, [r0, #6]                
  0d68c:  cmp r0, r4                        
  0d68e:  bhs #0xd6da                       
  0d690:  nop                               
  0d692:  b #0xd6a4                         -> 0x0d6a4 (вне списка функций)
  0d694:  add r0, sp, #0x24                 
  0d696:  bl #0xab0c                        -> func_0x0ab0c
  0d69a:  cmp r0, #1                        
  0d69c:  bne #0xd6a0                       
  0d69e:  b #0xd6a8                         -> 0x0d6a8 (вне списка функций)
  0d6a0:  adds r0, r5, #1                   
  0d6a2:  uxtb r5, r0                       
  0d6a4:  cmp r5, #3                        
  0d6a6:  blt #0xd694                       
  0d6a8:  nop                               
  0d6aa:  str.w r4, [sp, #0x42]             
  0d6ae:  movs r1, #0xa                     
  0d6b0:  add r0, sp, #0x3c                 
  0d6b2:  bl #0x8a50                        -> func_0x08a50
  0d6b6:  add r1, sp, #0x24                 
  0d6b8:  strh r0, [r1, #0x22]              
  0d6ba:  movs r2, #0x20                    
  0d6bc:  add r1, sp, #0x34                 
  0d6be:  mov r0, sp                        
  0d6c0:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0d6c4:  add r0, sp, #0x24                 
  0d6c6:  ldm r0, {r0, r1, r2, r3}          
  0d6c8:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  0d6cc:  ldr r0, [pc, #0x10]               -> RAM
  0d6ce:  ldr r1, [sp, #0x3c]               
  0d6d0:  str r1, [r0]                      
  0d6d2:  ldr r1, [sp, #0x40]               
  0d6d4:  str r1, [r0, #4]                  
  0d6d6:  ldr r1, [sp, #0x44]               
  0d6d8:  str r1, [r0, #8]                  
  0d6da:  add sp, #0x54                     
  0d6dc:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x0d6e0 (1 слов) — ВНЕ границ функции ---
  0d6e0:  .word 0x20000f64  ; RAM
```
