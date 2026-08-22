# func_0x03c4c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003c4c) | `0x00003c4c` |
| размер кода | 42 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019784 — flash-mirror @0x19784 (r5)

## Вызовы (callees)

- 0x03c70 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03838` (bl @0x000038a0)
- `func_0x038ec` (bl @0x0000391e)


## Дизассембляция

```asm
  03c4c:  push {r4, r5, lr}                 
  03c4e:  mov r2, r0                        
  03c50:  mov r3, r1                        
  03c52:  movs r1, #0                       
  03c54:  movs r0, #0                       
  03c56:  nop                               
  03c58:  b #0x3c70                         -> 0x03c70 (вне списка функций)
  03c5a:  ldrb r4, [r2, r1]                 
  03c5c:  eor.w r4, r4, r0, asr #8          
  03c60:  ldr r5, [pc, #0x14]               -> flash-mirror @0x19784
  03c62:  ldrh.w r4, [r5, r4, lsl #1]       
  03c66:  eor.w r4, r4, r0, lsl #8          
  03c6a:  uxth r0, r4                       
  03c6c:  adds r4, r1, #1                   
  03c6e:  uxtb r1, r4                       
  03c70:  cmp r1, r3                        
  03c72:  blt #0x3c5a                       
  03c74:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x03c78 (1 слов) — ВНЕ границ функции ---
  03c78:  .word 0x08019784  ; flash-mirror @0x19784
```
