# func_0x029e8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800029e8) | `0x000029e8` |
| размер кода | 104 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000ac8 — RAM (r1)
- 0x20000adc — RAM (r0)
- 0x20000b48 — RAM (r1)

## Вызовы (callees)

- `func_0x01e94` (0x00001e94, bl)
- 0x023c4 (bl, вне списка функций)
- 0x02a44 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x01dec` (bl @0x00001dee)


## Дизассембляция

```asm
  029e8:  push {r4, lr}                     
  029ea:  ldr r0, [pc, #0x64]               -> RAM
  029ec:  ldr r1, [pc, #0x64]               -> RAM
  029ee:  ldr r1, [r1]                      
  029f0:  ldr.w r0, [r0, r1, lsl #2]        
  029f4:  cbnz r0, #0x2a04                  
  029f6:  movs r0, #0                       
  029f8:  ldr r1, [pc, #0x58]               -> RAM
  029fa:  str r0, [r1]                      
  029fc:  bl #0x23c4                        -> 0x023c4 (вне списка функций)
  02a00:  bl #0x1e94                        -> func_0x01e94
  02a04:  ldr r0, [pc, #0x48]               -> RAM
  02a06:  ldr r1, [pc, #0x4c]               -> RAM
  02a08:  ldr r1, [r1]                      
  02a0a:  ldr.w r0, [r0, r1, lsl #2]        
  02a0e:  cbz r0, #0x2a44                   
  02a10:  ldr r1, [pc, #0x3c]               -> RAM
  02a12:  ldr r2, [pc, #0x40]               -> RAM
  02a14:  ldr r2, [r2]                      
  02a16:  ldr.w r0, [r1, r2, lsl #2]        
  02a1a:  blx r0                            
  02a1c:  cbz r0, #0x2a32                   
  02a1e:  ldr r0, [pc, #0x34]               -> RAM
  02a20:  ldrb r1, [r0]                     
  02a22:  movs r0, #1                       
  02a24:  lsls r0, r1                       
  02a26:  ldr r1, [pc, #0x30]               -> RAM
  02a28:  ldr r1, [r1]                      
  02a2a:  bics r1, r0                       
  02a2c:  ldr r0, [pc, #0x28]               -> RAM
  02a2e:  str r1, [r0]                      
  02a30:  b #0x2a44                         -> 0x02a44 (вне списка функций)
  02a32:  ldr r0, [pc, #0x20]               -> RAM
  02a34:  ldrb r1, [r0]                     
  02a36:  movs r0, #1                       
  02a38:  lsls r0, r1                       
  02a3a:  ldr r1, [pc, #0x1c]               -> RAM
  02a3c:  ldr r1, [r1]                      
  02a3e:  orrs r0, r1                       
  02a40:  ldr r1, [pc, #0x14]               -> RAM
  02a42:  str r0, [r1]                      
  02a44:  ldr r0, [pc, #0xc]                -> RAM
  02a46:  ldr r0, [r0]                      
  02a48:  adds r0, r0, #1                   
  02a4a:  ldr r1, [pc, #8]                  -> RAM
  02a4c:  str r0, [r1]                      
  02a4e:  pop {r4, pc}                      
  ; --- literal-пул @0x02a50 (3 слов) — ВНЕ границ функции ---
  02a50:  .word 0x20000adc  ; RAM
  02a54:  .word 0x20000b48  ; RAM
  02a58:  .word 0x20000ac8  ; RAM
```
