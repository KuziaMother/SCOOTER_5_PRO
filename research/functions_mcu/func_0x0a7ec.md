# func_0x0a7ec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000a7ec) | `0x0000a7ec` |
| размер кода | 184 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000002e — RAM (r0)
- 0x20000106 — RAM (r1)
- 0x20000114 — RAM (r0)
- 0x20000115 — RAM (r1)
- 0x200009c2 — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r1)
- 0x200015f7 — RAM (r0)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)
- 0x0a826 (b, вне списка функций)
- 0x0a8a2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1238c` (bl @0x000123a4)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0a824..0x0a826` (2 Б); цели из: 0x0a81e
- `0x0a826..0x0a850` (42 Б); цели из: 0x0a822
- `0x0a850..0x0a858` (8 Б); цели из: 0x0a844
- `0x0a858..0x0a872` (26 Б); цели из: 0x0a832
- `0x0a872..0x0a88c` (26 Б); цели из: 0x0a868
- `0x0a88c..0x0a8a2` (22 Б); цели из: 0x0a7fe, 0x0a806
- `0x0a8a2..0x0a8a4` (2 Б); цели из: 0x0a856, 0x0a878, 0x0a88a

## Дизассембляция

```asm
  0a7ec:  push {r4, lr}                     
  0a7ee:  movs r4, #0                       
  0a7f0:  ldr r0, [pc, #0xb0]               -> RAM
  0a7f2:  ldrh r0, [r0, #0x36]              
  0a7f4:  ldr r1, [pc, #0xb0]               -> RAM
  0a7f6:  strh r0, [r1, #0x24]              
  0a7f8:  ldr r0, [pc, #0xb0]               -> RAM
  0a7fa:  ldrb r0, [r0]                     
  0a7fc:  cmp r0, #0                        
  0a7fe:  bne #0xa88c                       
  0a800:  ldr r0, [pc, #0xac]               -> RAM
  0a802:  ldrb r0, [r0]                     
  0a804:  cmp r0, #3                        
  0a806:  blt #0xa88c                       
  0a808:  movs r0, #0x9e                    
  0a80a:  bl #0x1bdc                        -> func_0x01bdc
  0a80e:  ldr r0, [pc, #0x94]               -> RAM
  0a810:  ldrh r0, [r0, #0x36]              
  0a812:  add.w r0, r0, r0, lsl #2          
  0a816:  mov.w r1, #0xfa0                  
  0a81a:  cmp.w r1, r0, lsl #1              
  0a81e:  ble #0xa824                       
  0a820:  movs r4, #1                       
  0a822:  b #0xa826                         -> 0x0a826 (вне списка функций)
  0a824:  movs r4, #0                       
  0a826:  ldr r0, [pc, #0x8c]               -> RAM
  0a828:  ldrb r0, [r0, #1]                 
  0a82a:  and r0, r0, #1                    
  0a82e:  cbnz r0, #0xa87a                  
  0a830:  cmp r4, #1                        
  0a832:  bne #0xa858                       
  0a834:  ldr r0, [pc, #0x80]               -> RAM
  0a836:  ldrb r0, [r0]                     
  0a838:  adds r0, r0, #1                   
  0a83a:  ldr r1, [pc, #0x7c]               -> RAM
  0a83c:  strb r0, [r1]                     
  0a83e:  mov r0, r1                        
  0a840:  ldrb r0, [r0]                     
  0a842:  cmp r0, #0xa                      
  0a844:  ble #0xa850                       
  0a846:  movs r0, #0                       
  0a848:  strb r0, [r1]                     
  0a84a:  movs r0, #1                       
  0a84c:  ldr r1, [pc, #0x6c]               -> RAM
  0a84e:  strb r0, [r1]                     
  0a850:  movs r0, #0                       
  0a852:  ldr r1, [pc, #0x6c]               -> RAM
  0a854:  strb r0, [r1]                     
  0a856:  b #0xa8a2                         -> 0x0a8a2 (вне списка функций)
  0a858:  ldr r0, [pc, #0x64]               -> RAM
  0a85a:  ldrb r0, [r0]                     
  0a85c:  adds r0, r0, #1                   
  0a85e:  ldr r1, [pc, #0x60]               -> RAM
  0a860:  strb r0, [r1]                     
  0a862:  mov r0, r1                        
  0a864:  ldrb r0, [r0]                     
  0a866:  cmp r0, #0xa                      
  0a868:  ble #0xa872                       
  0a86a:  movs r0, #0                       
  0a86c:  strb r0, [r1]                     
  0a86e:  ldr r1, [pc, #0x4c]               -> RAM
  0a870:  strb r0, [r1]                     
  0a872:  movs r0, #0                       
  0a874:  ldr r1, [pc, #0x40]               -> RAM
  0a876:  strb r0, [r1]                     
  0a878:  b #0xa8a2                         -> 0x0a8a2 (вне списка функций)
  0a87a:  movs r0, #0                       
  0a87c:  ldr r1, [pc, #0x38]               -> RAM
  0a87e:  strb r0, [r1]                     
  0a880:  ldr r1, [pc, #0x3c]               -> RAM
  0a882:  strb r0, [r1]                     
  0a884:  movs r0, #2                       
  0a886:  ldr r1, [pc, #0x34]               -> RAM
  0a888:  strb r0, [r1]                     
  0a88a:  b #0xa8a2                         -> 0x0a8a2 (вне списка функций)
  0a88c:  movs r0, #0x9f                    
  0a88e:  bl #0x1bdc                        -> func_0x01bdc
  0a892:  movs r0, #0                       
  0a894:  ldr r1, [pc, #0x20]               -> RAM
  0a896:  strb r0, [r1]                     
  0a898:  ldr r1, [pc, #0x24]               -> RAM
  0a89a:  strb r0, [r1]                     
  0a89c:  movs r0, #2                       
  0a89e:  ldr r1, [pc, #0x1c]               -> RAM
  0a8a0:  strb r0, [r1]                     
  0a8a2:  pop {r4, pc}                      
  ; --- literal-пул @0x0a8a4 (8 слов) — ВНЕ границ функции ---
  0a8a4:  .word 0x200015f7  ; RAM
  0a8a8:  .word 0x20000f95  ; RAM
  0a8ac:  .word 0x2000002e  ; RAM
  0a8b0:  .word 0x200009c2  ; RAM
  0a8b4:  .word 0x20000f70  ; RAM
  0a8b8:  .word 0x20000114  ; RAM
  0a8bc:  .word 0x20000106  ; RAM
  0a8c0:  .word 0x20000115  ; RAM
```
