# func_0x0e3ec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e3ec) | `0x0000e3ec` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019fac — flash-mirror @0x19fac (r2)

## Вызовы (callees)

- `func_0x16aa2` (0x00016aa2, bl)

## Кто вызывает (callers / xrefs)

- `func_0x063b8` (bl @0x00006504)
- `func_0x063b8` (bl @0x00006514)
- `func_0x06fc0` (bl @0x00006fd6)
- `func_0x06fc0` (bl @0x00006fe6)


## Дизассембляция

```asm
  0e3ec:  push {r4, r5, r6, lr}             
  0e3ee:  mov r5, r0                        
  0e3f0:  mov r4, r1                        
  0e3f2:  movs r3, #0x15                    
  0e3f4:  ldr r2, [pc, #0xc]                -> flash-mirror @0x19fac
  0e3f6:  add.w r1, r2, #0x8a               
  0e3fa:  mov r0, r5                        
  0e3fc:  bl #0x16aa2                       -> func_0x16aa2
  0e400:  strh r0, [r4]                     
  0e402:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x0e404 (1 слов) — ВНЕ границ функции ---
  0e404:  .word 0x08019fac  ; flash-mirror @0x19fac
```
