# func_0x08b10

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008b10) | `0x00008b10` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000044 — RAM (r1)
- 0x20000048 — RAM (r1)
- 0x2000005c — RAM (r1)
- 0x200000a6 — RAM (r1)

## Вызовы (callees)

- `func_0x0170c` (0x0000170c, bl)
- `func_0x12804` (0x00012804, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01984` (bl @0x000019e4)


## Дизассембляция

```asm
  08b10:  push {r4, lr}                     
  08b12:  movs r0, #0                       
  08b14:  bl #0x170c                        -> func_0x0170c
  08b18:  ldr r1, [pc, #0x2c]               -> RAM
  08b1a:  strh r0, [r1]                     
  08b1c:  ldrh r1, [r1]                     
  08b1e:  movw r2, #0xce4                   
  08b22:  mul r4, r1, r2                    
  08b26:  asrs r1, r4, #0x1f                
  08b28:  add.w r1, r4, r1, lsr #20         
  08b2c:  ubfx r0, r1, #0xc, #0x10          
  08b30:  bl #0x12804                       -> func_0x12804
  08b34:  ldr r1, [pc, #0x14]               -> RAM
  08b36:  ldrb r1, [r1]                     
  08b38:  add r0, r1                        
  08b3a:  sxtb r0, r0                       
  08b3c:  ldr r1, [pc, #0x10]               -> RAM
  08b3e:  strb r0, [r1, #1]                 
  08b40:  movs r0, #0                       
  08b42:  ldr r1, [pc, #0x10]               -> RAM
  08b44:  strh r0, [r1]                     
  08b46:  pop {r4, pc}                      
  ; --- literal-пул @0x08b48 (4 слов) — ВНЕ границ функции ---
  08b48:  .word 0x2000005c  ; RAM
  08b4c:  .word 0x200000a6  ; RAM
  08b50:  .word 0x20000044  ; RAM
  08b54:  .word 0x20000048  ; RAM
```
