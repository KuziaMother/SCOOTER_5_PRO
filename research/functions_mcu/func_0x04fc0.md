# func_0x04fc0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004fc0) | `0x00004fc0` |
| размер кода | 52 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b76 — RAM (r0)
- 0x20001743 — RAM (r0)
- 0x40020000 — периферия (r1)

## Вызовы (callees)

- `func_0x04e38` (0x00004e38, bl)
- `func_0x04f58` (0x00004f58, bl)

## Кто вызывает (callers / xrefs)

- `func_0x04e30` (bl @0x00004e32)


## Дизассембляция

```asm
  04fc0:  push {r4, lr}                     
  04fc2:  ldr r1, [pc, #0x30]               -> периферия
  04fc4:  lsls r0, r1, #8                   
  04fc6:  bl #0x4f58                        -> func_0x04f58
  04fca:  cbz r0, #0x4ff2                   
  04fcc:  ldr r1, [pc, #0x24]               -> периферия
  04fce:  lsls r0, r1, #8                   
  04fd0:  bl #0x4e38                        -> func_0x04e38
  04fd4:  ldr r0, [pc, #0x20]               -> RAM
  04fd6:  ldrb r0, [r0]                     
  04fd8:  ldr r1, [pc, #0x1c]               -> RAM
  04fda:  ldrb r2, [r1, #1]                 
  04fdc:  movs r1, #1                       
  04fde:  lsls r1, r2                       
  04fe0:  bics r0, r1                       
  04fe2:  ldr r1, [pc, #0x14]               -> RAM
  04fe4:  strb r0, [r1]                     
  04fe6:  ldr r0, [pc, #0x14]               -> RAM
  04fe8:  ldrb r0, [r0]                     
  04fea:  bic r0, r0, #1                    
  04fee:  ldr r1, [pc, #0xc]                -> RAM
  04ff0:  strb r0, [r1]                     
  04ff2:  pop {r4, pc}                      
  ; --- literal-пул @0x04ff4 (3 слов) — ВНЕ границ функции ---
  04ff4:  .word 0x40020000  ; периферия
  04ff8:  .word 0x20001743  ; RAM
  04ffc:  .word 0x20000b76  ; RAM
```
