# func_0x1395c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001395c) | `0x0001395c` |
| размер кода | 36 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000cac — RAM (r0)
- 0x20000cb2 — RAM (r1)

## Вызовы (callees)

- `func_0x08af0` (0x00008af0, bl)
- 0x139a0 (b, вне списка функций)
- `func_0x13c78` (0x00013c78, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  1395c:  push {r3, lr}                     
  1395e:  movs r0, #0                       
  13960:  str r0, [sp]                      
  13962:  ldr r0, [pc, #0x40]               -> RAM
  13964:  ldrb r0, [r0]                     
  13966:  cbz r0, #0x139a0                  
  13968:  bl #0x8af0                        -> func_0x08af0
  1396c:  cbz r0, #0x13980                  
  1396e:  movs r0, #0                       
  13970:  ldr r1, [pc, #0x34]               -> RAM
  13972:  strb r0, [r1]                     
  13974:  ldr r1, [pc, #0x2c]               -> RAM
  13976:  strb r0, [r1]                     
  13978:  mov r0, sp                        
  1397a:  bl #0x13c78                       -> func_0x13c78
  1397e:  b #0x139a0                        -> 0x139a0 (вне списка функций)
  ; --- literal-пул @0x139a4 (2 слов) — ВНЕ границ функции ---
  139a4:  .word 0x20000cac  ; RAM
  139a8:  .word 0x20000cb2  ; RAM
```
