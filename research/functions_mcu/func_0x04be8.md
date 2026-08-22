# func_0x04be8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004be8) | `0x00004be8` |
| размер кода | 36 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b4c — RAM (r3)
- 0x2000164c — RAM (r0)

## Вызовы (callees)

- 0x04c06 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x09a44` (bl @0x00009a46)


## Дизассембляция

```asm
  04be8:  movs r2, #0                       
  04bea:  ldr r3, [pc, #0x20]               -> RAM
  04bec:  str r2, [r3]                      
  04bee:  ldr r0, [pc, #0x20]               -> RAM
  04bf0:  movs r1, #0                       
  04bf2:  b #0x4c06                         -> 0x04c06 (вне списка функций)
  04bf4:  movs r2, #0                       
  04bf6:  strb r2, [r0]                     
  04bf8:  subs r2, r2, #1                   
  04bfa:  str r2, [r0, #4]                  
  04bfc:  movs r2, #0                       
  04bfe:  strb r2, [r0, #1]                 
  04c00:  adds r0, #0x10                    
  04c02:  adds r2, r1, #1                   
  04c04:  uxtb r1, r2                       
  04c06:  cmp r1, #6                        
  04c08:  blt #0x4bf4                       
  04c0a:  bx lr                             
  ; --- literal-пул @0x04c0c (2 слов) — ВНЕ границ функции ---
  04c0c:  .word 0x20000b4c  ; RAM
  04c10:  .word 0x2000164c  ; RAM
```
