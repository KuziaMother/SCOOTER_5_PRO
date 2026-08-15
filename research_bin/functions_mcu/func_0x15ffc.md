# func_0x15ffc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015ffc) | `0x00015ffc` |
| размер кода | 56 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b8c — RAM (r0)
- 0x20000c7e — RAM (r1)
- 0x20000c80 — RAM (r0)

## Вызовы (callees)

- `func_0x15a1c` (0x00015a1c, bl)
- 0x16032 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x158f8` (bl @0x00015902)


## Дизассембляция

```asm
  15ffc:  push {r4, lr}                     
  15ffe:  mov r4, r0                        
  16000:  cbz r4, #0x16006                  
  16002:  ldr r0, [pc, #0x30]               -> RAM
  16004:  str r4, [r0]                      
  16006:  ldr r0, [pc, #0x30]               -> RAM
  16008:  ldrb r0, [r0]                     
  1600a:  cmp r0, #1                        
  1600c:  bne #0x1602c                      
  1600e:  ldr r0, [pc, #0x24]               -> RAM
  16010:  ldr r0, [r0]                      
  16012:  cbnz r0, #0x16020                 
  16014:  movs r0, #0                       
  16016:  ldr r1, [pc, #0x20]               -> RAM
  16018:  strb r0, [r1]                     
  1601a:  bl #0x15a1c                       -> func_0x15a1c
  1601e:  b #0x16032                        -> 0x16032 (вне списка функций)
  16020:  ldr r0, [pc, #0x10]               -> RAM
  16022:  ldr r0, [r0]                      
  16024:  subs r0, r0, #1                   
  16026:  ldr r1, [pc, #0xc]                -> RAM
  16028:  str r0, [r1]                      
  1602a:  b #0x16032                        -> 0x16032 (вне списка функций)
  1602c:  movs r0, #0                       
  1602e:  ldr r1, [pc, #0xc]                -> RAM
  16030:  strb r0, [r1]                     
  16032:  pop {r4, pc}                      
  ; --- literal-пул @0x16034 (3 слов) — ВНЕ границ функции ---
  16034:  .word 0x20000c80  ; RAM
  16038:  .word 0x20000b8c  ; RAM
  1603c:  .word 0x20000c7e  ; RAM
```
