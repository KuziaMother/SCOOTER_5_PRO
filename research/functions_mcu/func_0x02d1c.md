# func_0x02d1c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002d1c) | `0x00002d1c` |
| размер кода | 20 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b5c — RAM (r0)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x04bc0` (bl @0x00004bce)
- `func_0x04c84` (bl @0x00004c94)
- `func_0x04cbc` (bl @0x00004cd2)
- `func_0x04cbc` (bl @0x00004d18)


## Дизассембляция

```asm
  02d1c:  ldr r0, [pc, #0x10]               -> RAM
  02d1e:  ldrh r0, [r0]                     
  02d20:  cbnz r0, #0x2d24                  
  02d22:  cpsid i                           
  02d24:  ldr r0, [pc, #8]                  -> RAM
  02d26:  ldrh r0, [r0]                     
  02d28:  adds r0, r0, #1                   
  02d2a:  ldr r1, [pc, #4]                  -> RAM
  02d2c:  strh r0, [r1]                     
  02d2e:  bx lr                             
  ; --- literal-пул @0x02d30 (1 слов) — ВНЕ границ функции ---
  02d30:  .word 0x20000b5c  ; RAM
```
