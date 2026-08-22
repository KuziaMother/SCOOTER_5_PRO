# func_0x0e2cc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e2cc) | `0x0000e2cc` |
| размер кода | 44 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019f50 — flash-mirror @0x19f50 (r0)

## Вызовы (callees)

- `func_0x16d8e` (0x00016d8e, bl)

## Кто вызывает (callers / xrefs)

- `func_0x069e4` (bl @0x00006b50)
- `func_0x069e4` (bl @0x00006be8)


## Дизассембляция

```asm
  0e2cc:  push {r1, r2, r3, r4, r5, r6, r7, lr}
  0e2ce:  mov r4, r0                        
  0e2d0:  mov r5, r1                        
  0e2d2:  mov r6, r2                        
  0e2d4:  mov r7, r3                        
  0e2d6:  movs r2, #0xc                     
  0e2d8:  ldr r0, [pc, #0x1c]               -> flash-mirror @0x19f50
  0e2da:  addw r1, r0, #0x59f               
  0e2de:  strd r0, r2, [sp, #4]             
  0e2e2:  str r1, [sp]                      
  0e2e4:  subs r0, r4, r5                   
  0e2e6:  subw r3, r1, #0x5cf               
  0e2ea:  subw r2, r1, #0x5ff               
  0e2ee:  mov r1, r6                        
  0e2f0:  bl #0x16d8e                       -> func_0x16d8e
  0e2f4:  strb r0, [r7]                     
  0e2f6:  pop {r1, r2, r3, r4, r5, r6, r7, pc}
  ; --- literal-пул @0x0e2f8 (1 слов) — ВНЕ границ функции ---
  0e2f8:  .word 0x08019f50  ; flash-mirror @0x19f50
```
