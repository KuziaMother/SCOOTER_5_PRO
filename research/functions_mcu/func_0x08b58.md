# func_0x08b58

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008b58) | `0x00008b58` |
| размер кода | 50 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000005e — RAM (r1)
- 0x200000a6 — RAM (r1)
- 0x20000fc7 — RAM (r1)

## Вызовы (callees)

- `func_0x0170c` (0x0000170c, bl)
- `func_0x12804` (0x00012804, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01984` (bl @0x000019e0)


## Дизассембляция

```asm
  08b58:  push {r4, lr}                     
  08b5a:  movs r0, #1                       
  08b5c:  bl #0x170c                        -> func_0x0170c
  08b60:  ldr r1, [pc, #0x28]               -> RAM
  08b62:  strh r0, [r1]                     
  08b64:  ldrh r1, [r1]                     
  08b66:  movw r2, #0xce4                   
  08b6a:  mul r4, r1, r2                    
  08b6e:  asrs r1, r4, #0x1f                
  08b70:  add.w r1, r4, r1, lsr #20         
  08b74:  ubfx r0, r1, #0xc, #0x10          
  08b78:  bl #0x12804                       -> func_0x12804
  08b7c:  ldr r1, [pc, #0x10]               -> RAM
  08b7e:  ldrb r1, [r1]                     
  08b80:  add r0, r1                        
  08b82:  sxtb r0, r0                       
  08b84:  ldr r1, [pc, #0xc]                -> RAM
  08b86:  strb r0, [r1, #8]                 
  08b88:  pop {r4, pc}                      
  ; --- literal-пул @0x08b8c (3 слов) — ВНЕ границ функции ---
  08b8c:  .word 0x2000005e  ; RAM
  08b90:  .word 0x200000a6  ; RAM
  08b94:  .word 0x20000fc7  ; RAM
```
