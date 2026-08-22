# func_0x02d34

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002d34) | `0x00002d34` |
| размер кода | 36 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b5c — RAM (r0)

## Вызовы (callees)

- 0x02d56 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04bc0` (bl @0x00004bdc)
- `func_0x04c84` (bl @0x00004cae)
- `func_0x04cbc` (bl @0x00004d10)
- `func_0x04cbc` (bl @0x00004d1c)
- `func_0x04cbc` (bl @0x00004d2e)


## Дизассембляция

```asm
  02d34:  ldr r0, [pc, #0x20]               -> RAM
  02d36:  ldrh r0, [r0]                     
  02d38:  cmp r0, #1                        
  02d3a:  beq #0x2d42                       
  02d3c:  ldr r0, [pc, #0x18]               -> RAM
  02d3e:  ldrh r0, [r0]                     
  02d40:  cbnz r0, #0x2d4c                  
  02d42:  cpsie i                           
  02d44:  movs r0, #0                       
  02d46:  ldr r1, [pc, #0x10]               -> RAM
  02d48:  strh r0, [r1]                     
  02d4a:  b #0x2d56                         -> 0x02d56 (вне списка функций)
  02d4c:  ldr r0, [pc, #8]                  -> RAM
  02d4e:  ldrh r0, [r0]                     
  02d50:  subs r0, r0, #1                   
  02d52:  ldr r1, [pc, #4]                  -> RAM
  02d54:  strh r0, [r1]                     
  02d56:  bx lr                             
  ; --- literal-пул @0x02d58 (1 слов) — ВНЕ границ функции ---
  02d58:  .word 0x20000b5c  ; RAM
```
