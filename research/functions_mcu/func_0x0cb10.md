# func_0x0cb10

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cb10) | `0x0000cb10` |
| размер кода | 42 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40002824 — периферия (r2)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x14958` (bl @0x00014962)
- `func_0x14958` (bl @0x0001496e)
- `func_0x14958` (bl @0x0001497a)
- `func_0x14958` (bl @0x00014986)
- `func_0x14958` (bl @0x00014992)
- `func_0x14958` (bl @0x0001499e)


## Дизассембляция

```asm
  0cb10:  movs r1, #0xca                    
  0cb12:  ldr r2, [pc, #0x28]               -> периферия
  0cb14:  str r1, [r2]                      
  0cb16:  movs r1, #0x53                    
  0cb18:  str r1, [r2]                      
  0cb1a:  ldr r1, [pc, #0x20]               -> периферия
  0cb1c:  subs r1, #0x1c                    
  0cb1e:  ldr r1, [r1]                      
  0cb20:  bic r1, r1, #7                    
  0cb24:  ldr r2, [pc, #0x14]               -> периферия
  0cb26:  subs r2, #0x1c                    
  0cb28:  str r1, [r2]                      
  0cb2a:  mov r1, r2                        
  0cb2c:  ldr r1, [r1]                      
  0cb2e:  orrs r1, r0                       
  0cb30:  str r1, [r2]                      
  0cb32:  movs r1, #0xff                    
  0cb34:  ldr r2, [pc, #4]                  -> периферия
  0cb36:  str r1, [r2]                      
  0cb38:  bx lr                             
  ; --- literal-пул @0x0cb3c (1 слов) — ВНЕ границ функции ---
  0cb3c:  .word 0x40002824  ; периферия
```
