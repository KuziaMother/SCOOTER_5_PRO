# func_0x0befc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000befc) | `0x0000befc` |
| размер кода | 74 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200007c4 — RAM (r4)

## Вызовы (callees)

- 0x0bf3e (b, вне списка функций)
- 0x0bf42 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0bcc0` (bl @0x0000bcfc)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0bf3a..0x0bf3e` (4 Б); цели из: 0x0bf16, 0x0bf2c
- `0x0bf3e..0x0bf42` (4 Б); цели из: 0x0bf0a
- `0x0bf42..0x0bf46` (4 Б); цели из: 0x0bf38

## Дизассембляция

```asm
  0befc:  push {r4, r5, lr}                 
  0befe:  mov r2, r0                        
  0bf00:  mov r3, r1                        
  0bf02:  movs r0, #0                       
  0bf04:  movs r4, #0                       
  0bf06:  strb r4, [r3]                     
  0bf08:  movs r1, #0                       
  0bf0a:  b #0xbf3e                         -> 0x0bf3e (вне списка функций)
  0bf0c:  ldr r4, [pc, #0x38]               -> RAM
  0bf0e:  add.w r4, r4, r1, lsl #3          
  0bf12:  ldrb r4, [r4, #4]                 
  0bf14:  cmp r4, r2                        
  0bf16:  bgt #0xbf3a                       
  0bf18:  ldr r4, [pc, #0x2c]               -> RAM
  0bf1a:  add.w r4, r4, r1, lsl #3          
  0bf1e:  ldrb r4, [r4, #4]                 
  0bf20:  ldr r5, [pc, #0x24]               -> RAM
  0bf22:  ldr.w r5, [r5, r1, lsl #3]        
  0bf26:  ldrb r5, [r5, #8]                 
  0bf28:  add r4, r5                        
  0bf2a:  cmp r4, r2                        
  0bf2c:  ble #0xbf3a                       
  0bf2e:  movs r4, #1                       
  0bf30:  strb r4, [r3]                     
  0bf32:  ldr r4, [pc, #0x14]               -> RAM
  0bf34:  add.w r0, r4, r1, lsl #3          
  0bf38:  b #0xbf42                         -> 0x0bf42 (вне списка функций)
  0bf3a:  adds r4, r1, #1                   
  0bf3c:  uxth r1, r4                       
  0bf3e:  cmp r1, #2                        
  0bf40:  blo #0xbf0c                       
  0bf42:  nop                               
  0bf44:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x0bf48 (1 слов) — ВНЕ границ функции ---
  0bf48:  .word 0x200007c4  ; RAM
```
