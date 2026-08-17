# func_0x02d5c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002d5c) | `0x00002d5c` |
| размер кода | 16 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a550 — flash-mirror @0x1a550 (r0)

## Вызовы (callees)

- `func_0x0332c` (0x0000332c, bl)
- `func_0x03588` (0x00003588, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03034` (bl @0x00003042)
- `func_0x05dbc` (bl @0x00005dc6)


## Дизассембляция

```asm
  02d5c:  push {r4, lr}                     
  02d5e:  bl #0x3588                        -> func_0x03588
  02d62:  movs r1, #0x1a                    
  02d64:  ldr r0, [pc, #4]                  -> flash-mirror @0x1a550
  02d66:  bl #0x332c                        -> func_0x0332c
  02d6a:  pop {r4, pc}                      
  ; --- literal-пул @0x02d6c (1 слов) — ВНЕ границ функции ---
  02d6c:  .word 0x0801a550  ; flash-mirror @0x1a550
```
