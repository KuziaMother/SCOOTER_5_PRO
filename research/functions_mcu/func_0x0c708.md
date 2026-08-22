# func_0x0c708

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c708) | `0x0000c708` |
| размер кода | 86 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x007a1200 — прочее (r7)
- 0x083c0000 — прочее (ip)
- 0x40021000 — периферия (r7)

## Вызовы (callees)

- 0x0c74a (b, вне списка функций)
- 0x0c77e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03600` (bl @0x0000360c)
- `func_0x098c8` (bl @0x000098e6)
- `func_0x13148` (bl @0x00013198)


## Дизассембляция

```asm
  0c708:  push {r4, r5, r6, r7, lr}         
  0c70a:  movs r1, #0                       
  0c70c:  nop                               
  0c70e:  movs r3, #0                       
  0c710:  movs r6, #0                       
  0c712:  movs r4, #0                       
  0c714:  movs r5, #0                       
  0c716:  ldr r7, [pc, #0x120]              -> периферия
  0c718:  ldr r7, [r7, #4]                  
  0c71a:  ldr.w ip, [pc, #0x120]            
  0c71e:  and.w r3, r7, ip                  
  0c722:  ldr r7, [pc, #0x114]              -> периферия
  0c724:  ldr r7, [r7, #4]                  
  0c726:  and r6, r7, #0x10000              
  0c72a:  ldr r7, [pc, #0x10c]              -> периферия
  0c72c:  ldr r7, [r7, #0x24]               
  0c72e:  ubfx r5, r7, #4, #3               
  0c732:  and r7, r3, #0x8000000            
  0c736:  cbnz r7, #0xc740                  
  0c738:  movs r7, #2                       
  0c73a:  add.w r3, r7, r3, lsr #18         
  0c73e:  b #0xc74a                         -> 0x0c74a (вне списка функций)
  0c740:  mov.w r7, #0x1f0                  
  0c744:  rsb r7, r7, r3, lsr #18           
  0c748:  adds r3, r7, #1                   
  0c74a:  cbnz r6, #0xc766                  
  0c74c:  ldr r7, [pc, #0xe8]               -> периферия
  0c74e:  ldr r7, [r7, #0x40]               
  0c750:  and r7, r7, #1                    
  0c754:  cbz r7, #0xc75e                   
  0c756:  ldr r7, [pc, #0xe8]               
  0c758:  mul r2, r3, r7                    
  0c75c:  b #0xc77e                         -> 0x0c77e (вне списка функций)
  ; --- literal-пул @0x0c838 (3 слов) — ВНЕ границ функции ---
  0c838:  .word 0x40021000  ; периферия
  0c83c:  .word 0x083c0000
  0c840:  .word 0x007a1200
```
