# func_0x15a1c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015a1c) | `0x00015a1c` |
| размер кода | 58 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000c7f — RAM (r1)
- 0x20001fac — RAM (r1)

## Вызовы (callees)

- `func_0x15758` (0x00015758, bl)

## Кто вызывает (callers / xrefs)

- `func_0x15f00` (bl @0x00015f10)
- `func_0x15ffc` (bl @0x0001601a)


## Дизассембляция

```asm
  15a1c:  push {r4, lr}                     
  15a1e:  movs r0, #0                       
  15a20:  ldr r1, [pc, #0x34]               -> RAM
  15a22:  strb r0, [r1, #3]                 
  15a24:  strh r0, [r1, #6]                 
  15a26:  strh r0, [r1, #8]                 
  15a28:  movs r0, #0xff                    
  15a2a:  strh r0, [r1, #0xa]               
  15a2c:  movs r0, #0                       
  15a2e:  strh r0, [r1, #4]                 
  15a30:  str r0, [r1, #0x10]               
  15a32:  strh r0, [r1, #0x14]              
  15a34:  str r0, [r1, #0x18]               
  15a36:  strh r0, [r1, #0x1c]              
  15a38:  add.w r0, r1, #0x1e               
  15a3c:  movs r1, #0                       
  15a3e:  str r1, [r0]                      
  15a40:  str r1, [r0, #4]                  
  15a42:  strh r1, [r0, #8]                 
  15a44:  movs r0, #0                       
  15a46:  ldr r1, [pc, #0x10]               -> RAM
  15a48:  strh r0, [r1, #0xc]               
  15a4a:  strh r0, [r1, #0xe]               
  15a4c:  ldr r1, [pc, #0xc]                -> RAM
  15a4e:  strb r0, [r1]                     
  15a50:  bl #0x15758                       -> func_0x15758
  15a54:  pop {r4, pc}                      
  ; --- literal-пул @0x15a58 (2 слов) — ВНЕ границ функции ---
  15a58:  .word 0x20001fac  ; RAM
  15a5c:  .word 0x20000c7f  ; RAM
```
