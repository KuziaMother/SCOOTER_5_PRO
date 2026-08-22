# func_0x057f8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800057f8) | `0x000057f8` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000cb3 — RAM (r0)

## Вызовы (callees)

- `func_0x13bb8` (0x00013bb8, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  057f8:  push {r4, lr}                     
  057fa:  ldr r0, [pc, #0x18]               -> RAM
  057fc:  ldrb r0, [r0, #1]                 
  057fe:  ldr r1, [pc, #0x14]               -> RAM
  05800:  ldrb r1, [r1]                     
  05802:  add.w r0, r0, r1, lsl #8          
  05806:  uxth r4, r0                       
  05808:  mov r1, r4                        
  0580a:  movs r0, #1                       
  0580c:  bl #0x13bb8                       -> func_0x13bb8
  05810:  pop {r4, pc}                      
  ; --- literal-пул @0x05814 (1 слов) — ВНЕ границ функции ---
  05814:  .word 0x20000cb3  ; RAM
```
