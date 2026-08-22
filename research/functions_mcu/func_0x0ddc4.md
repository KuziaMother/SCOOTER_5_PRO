# func_0x0ddc4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ddc4) | `0x0000ddc4` |
| размер кода | 58 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801d800 — flash-mirror @0x1d800 (r0)
- 0x2000124e — RAM (r0)

## Вызовы (callees)

- `func_0x07e98` (0x00007e98, bl)
- 0x0dd80 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0bf4c` (bl @0x0000bf52)


## Дизассембляция

```asm
  0ddc4:  push {r4, lr}                     
  0ddc6:  ldr r0, [pc, #0x38]               -> RAM
  0ddc8:  ldrh r0, [r0, #0x12]              
  0ddca:  cmp r0, #0xe0                     
  0ddcc:  bne #0xdde4                       
  0ddce:  ldr r0, [pc, #0x30]               -> RAM
  0ddd0:  ldrh r0, [r0, #0x14]              
  0ddd2:  movw r1, #0x5aa5                  
  0ddd6:  cmp r0, r1                        
  0ddd8:  bne #0xdde4                       
  0ddda:  ldr r0, [pc, #0x28]               -> flash-mirror @0x1d800
  0dddc:  bl #0x7e98                        -> func_0x07e98
  0dde0:  bl #0xdd80                        -> 0x0dd80 (вне списка функций)
  0dde4:  ldr r0, [pc, #0x18]               -> RAM
  0dde6:  ldrh r0, [r0, #0x12]              
  0dde8:  cmp r0, #0xe2                     
  0ddea:  bne #0xddfc                       
  0ddec:  ldr r0, [pc, #0x10]               -> RAM
  0ddee:  ldrh r0, [r0, #0x14]              
  0ddf0:  movw r1, #0x5aa5                  
  0ddf4:  cmp r0, r1                        
  0ddf6:  bne #0xddfc                       
  0ddf8:  bl #0xdd80                        -> 0x0dd80 (вне списка функций)
  0ddfc:  pop {r4, pc}                      
  ; --- literal-пул @0x0de00 (2 слов) — ВНЕ границ функции ---
  0de00:  .word 0x2000124e  ; RAM
  0de04:  .word 0x0801d800  ; flash-mirror @0x1d800
```
