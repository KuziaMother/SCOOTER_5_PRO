# func_0x09a44

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080009a44) | `0x00009a44` |
| размер кода | 80 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x080148e5 — flash-mirror @0x148e5 (r1)
- 0x080149b5 — flash-mirror @0x149b5 (r1)
- 0x08014a65 — flash-mirror @0x14a65 (r1)
- 0x08014a79 — flash-mirror @0x14a79 (r1)

## Вызовы (callees)

- `func_0x04bc0` (0x00004bc0, bl)
- `func_0x04be8` (0x00004be8, bl)
- `func_0x04c84` (0x00004c84, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  09a44:  push {r4, lr}                     
  09a46:  bl #0x4be8                        -> func_0x04be8
  09a4a:  movs r2, #0                       
  09a4c:  ldr r1, [pc, #0x44]               -> flash-mirror @0x14a65
  09a4e:  mov r0, r2                        
  09a50:  bl #0x4bc0                        -> func_0x04bc0
  09a54:  movs r2, #0                       
  09a56:  ldr r1, [pc, #0x40]               -> flash-mirror @0x149b5
  09a58:  movs r0, #1                       
  09a5a:  bl #0x4bc0                        -> func_0x04bc0
  09a5e:  movs r2, #0                       
  09a60:  ldr r1, [pc, #0x38]               -> flash-mirror @0x148e5
  09a62:  movs r0, #3                       
  09a64:  bl #0x4bc0                        -> func_0x04bc0
  09a68:  movs r2, #0                       
  09a6a:  ldr r1, [pc, #0x34]               -> flash-mirror @0x14a79
  09a6c:  movs r0, #4                       
  09a6e:  bl #0x4bc0                        -> func_0x04bc0
  09a72:  movs r1, #4                       
  09a74:  movs r0, #0                       
  09a76:  bl #0x4c84                        -> func_0x04c84
  09a7a:  movs r1, #4                       
  09a7c:  movs r0, #1                       
  09a7e:  bl #0x4c84                        -> func_0x04c84
  09a82:  movs r1, #4                       
  09a84:  movs r0, #3                       
  09a86:  bl #0x4c84                        -> func_0x04c84
  09a8a:  movs r1, #4                       
  09a8c:  mov r0, r1                        
  09a8e:  bl #0x4c84                        -> func_0x04c84
  09a92:  pop {r4, pc}                      
  ; --- literal-пул @0x09a94 (4 слов) — ВНЕ границ функции ---
  09a94:  .word 0x08014a65  ; flash-mirror @0x14a65
  09a98:  .word 0x080149b5  ; flash-mirror @0x149b5
  09a9c:  .word 0x080148e5  ; flash-mirror @0x148e5
  09aa0:  .word 0x08014a79  ; flash-mirror @0x14a79
```
