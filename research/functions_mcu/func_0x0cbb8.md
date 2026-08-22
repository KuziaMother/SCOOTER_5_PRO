# func_0x0cbb8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cbb8) | `0x0000cbb8` |
| размер кода | 68 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x4000280c — периферия (r2)

## Вызовы (callees)

- 0x0cc02 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0ca3c` (bl @0x0000cac2)
- `func_0x0cd0c` (bl @0x0000cd1e)
- `func_0x0cd80` (bl @0x0000cdfe)


## Дизассембляция

```asm
  0cbb8:  push {r3, lr}                     
  0cbba:  movs r2, #0                       
  0cbbc:  str r2, [sp]                      
  0cbbe:  movs r0, #0                       
  0cbc0:  movs r1, #0                       
  0cbc2:  ldr r2, [pc, #0x40]               -> периферия
  0cbc4:  ldr r2, [r2]                      
  0cbc6:  and r2, r2, #0x40                 
  0cbca:  cbnz r2, #0xcc00                  
  0cbcc:  movs r2, #0x80                    
  0cbce:  ldr r3, [pc, #0x34]               -> периферия
  0cbd0:  str r2, [r3]                      
  0cbd2:  nop                               
  0cbd4:  ldr r2, [pc, #0x2c]               -> периферия
  0cbd6:  ldr r2, [r2]                      
  0cbd8:  and r1, r2, #0x40                 
  0cbdc:  ldr r2, [sp]                      
  0cbde:  adds r2, r2, #1                   
  0cbe0:  str r2, [sp]                      
  0cbe2:  ldr r2, [sp]                      
  0cbe4:  cmp.w r2, #0x2000                 
  0cbe8:  beq #0xcbee                       
  0cbea:  cmp r1, #0                        
  0cbec:  beq #0xcbd4                       
  0cbee:  ldr r2, [pc, #0x14]               -> периферия
  0cbf0:  ldr r2, [r2]                      
  0cbf2:  and r2, r2, #0x40                 
  0cbf6:  cbz r2, #0xcbfc                   
  0cbf8:  movs r0, #1                       
  0cbfa:  b #0xcc02                         -> 0x0cc02 (вне списка функций)
  ; --- literal-пул @0x0cc04 (1 слов) — ВНЕ границ функции ---
  0cc04:  .word 0x4000280c  ; периферия
```
