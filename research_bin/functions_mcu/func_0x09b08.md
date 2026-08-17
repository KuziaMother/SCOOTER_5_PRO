# func_0x09b08

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080009b08) | `0x00009b08` |
| размер кода | 54 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a71 — RAM (r0)

## Вызовы (callees)

- `func_0x02a5c` (0x00002a5c, bl)
- 0x09b0e (b, вне списка функций)
- 0x09b20 (b, вне списка функций)
- 0x09b3c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e26)


## Дизассембляция

```asm
  09b08:  push {r4, lr}                     
  09b0a:  movs r4, #0                       
  09b0c:  b #0x9b3c                         -> 0x09b3c (вне списка функций)
  09b0e:  bl #0x2a5c                        -> func_0x02a5c
  09b12:  cbz r0, #0x9b22                   
  09b14:  ldr r0, [pc, #0x28]               -> RAM
  09b16:  ldrb r0, [r0]                     
  09b18:  bic r0, r0, #8                    
  09b1c:  ldr r1, [pc, #0x20]               -> RAM
  09b1e:  strb r0, [r1]                     
  09b20:  pop {r4, pc}                      
  09b22:  ldr r0, [pc, #0x1c]               -> RAM
  09b24:  ldrb r0, [r0]                     
  09b26:  bic r0, r0, #8                    
  09b2a:  adds r0, #8                       
  09b2c:  ldr r1, [pc, #0x10]               -> RAM
  09b2e:  strb r0, [r1]                     
  09b30:  adds r0, r4, #1                   
  09b32:  uxtb r0, r0                       
  09b34:  mov r4, r0                        
  09b36:  cmp r0, #2                        
  09b38:  blt #0x9b3c                       
  09b3a:  b #0x9b20                         -> 0x09b20 (вне списка функций)
  09b3c:  b #0x9b0e                         -> 0x09b0e (вне списка функций)
  ; --- literal-пул @0x09b40 (1 слов) — ВНЕ границ функции ---
  09b40:  .word 0x20000a71  ; RAM
```
