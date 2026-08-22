# func_0x0e160

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000e160) | `0x0000e160` |
| размер кода | 24 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019e98 — flash-mirror @0x19e98 (r2)

## Вызовы (callees)

- `func_0x16880` (0x00016880, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0799c` (bl @0x000079ac)
- `func_0x0e17c` (bl @0x0000e18a)


## Дизассембляция

```asm
  0e160:  push {r4, r5, r6, lr}             
  0e162:  mov r5, r0                        
  0e164:  mov r4, r1                        
  0e166:  movs r3, #6                       
  0e168:  ldr r2, [pc, #0xc]                -> flash-mirror @0x19e98
  0e16a:  add.w r1, r2, #0x140              
  0e16e:  mov r0, r5                        
  0e170:  bl #0x16880                       -> func_0x16880
  0e174:  str r0, [r4]                      
  0e176:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x0e178 (1 слов) — ВНЕ границ функции ---
  0e178:  .word 0x08019e98  ; flash-mirror @0x19e98
```
