# func_0x11d98

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080011d98) | `0x00011d98` |
| размер кода | 58 Б |
| регион | код D (0x11894 tbb-машина, 0x11cb4 OTA-init) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000002e — RAM (r0)
- 0x20000031 — RAM (r0)
- 0x20000033 — RAM (r0)
- 0x20000036 — RAM (r1)
- 0x20000f70 — RAM (r1)

## Вызовы (callees)

- 0x11dc2 (b, вне списка функций)
- `func_0x14ed0` (0x00014ed0, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x11db0..0x11dbc` (12 Б); цели из: 0x11da6
- `0x11dbc..0x11dc2` (6 Б); цели из: 0x11dae
- `0x11dc2..0x11dd2` (16 Б); цели из: 0x11dba

## Дизассембляция

```asm
  11d98:  push {r4, lr}                     
  11d9a:  ldr r0, [pc, #0x38]               -> RAM
  11d9c:  ldrb r0, [r0]                     
  11d9e:  cbz r0, #0x11db0                  
  11da0:  ldr r0, [pc, #0x30]               -> RAM
  11da2:  ldrb r0, [r0]                     
  11da4:  cmp r0, #4                        
  11da6:  beq #0x11db0                      
  11da8:  ldr r0, [pc, #0x28]               -> RAM
  11daa:  ldrb r0, [r0]                     
  11dac:  cmp r0, #1                        
  11dae:  bne #0x11dbc                      
  11db0:  movs r0, #1                       
  11db2:  ldr r1, [pc, #0x24]               -> RAM
  11db4:  strb r0, [r1]                     
  11db6:  bl #0x14ed0                       -> func_0x14ed0
  11dba:  b #0x11dc2                        -> 0x11dc2 (вне списка функций)
  11dbc:  movs r0, #0                       
  11dbe:  ldr r1, [pc, #0x18]               -> RAM
  11dc0:  strb r0, [r1]                     
  11dc2:  ldr r0, [pc, #0x18]               -> RAM
  11dc4:  ldrb r0, [r0]                     
  11dc6:  ldr r1, [pc, #0x18]               -> RAM
  11dc8:  strb r0, [r1, #6]                 
  11dca:  ldr r0, [pc, #0x18]               -> RAM
  11dcc:  ldrb r0, [r0]                     
  11dce:  strb r0, [r1, #5]                 
  11dd0:  pop {r4, pc}                      
  ; --- literal-пул @0x11dd4 (5 слов) — ВНЕ границ функции ---
  11dd4:  .word 0x2000002e  ; RAM
  11dd8:  .word 0x20000036  ; RAM
  11ddc:  .word 0x20000031  ; RAM
  11de0:  .word 0x20000f70  ; RAM
  11de4:  .word 0x20000033  ; RAM
```
