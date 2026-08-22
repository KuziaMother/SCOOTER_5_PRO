# func_0x14ed0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080014ed0) | `0x00014ed0` |
| размер кода | 110 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000031 — RAM (r0)
- 0x20000042 — RAM (r1)
- 0x20000080 — RAM (r0)
- 0x20000107 — RAM (r0)

## Вызовы (callees)

- `func_0x08e14` (0x00008e14, bl)
- 0x14ef4 (b, вне списка функций)
- 0x14f30 (b, вне списка функций)
- 0x14f3a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11d98` (bl @0x00011db6)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x14ef2..0x14ef4` (2 Б); цели из: 0x14ee4
- `0x14ef4..0x14f08` (20 Б); цели из: 0x14edc
- `0x14f08..0x14f30` (40 Б); цели из: 0x14efa
- `0x14f30..0x14f32` (2 Б); цели из: 0x14f06, 0x14f1e, 0x14f28
- `0x14f32..0x14f3a` (8 Б); цели из: 0x14eda
- `0x14f3a..0x14f3e` (4 Б); цели из: 0x14ef2, 0x14f30

## Дизассембляция

```asm
  14ed0:  push {r4, lr}                     
  14ed2:  ldr r0, [pc, #0x6c]               -> RAM
  14ed4:  ldrb r0, [r0]                     
  14ed6:  cbz r0, #0x14ede                  
  14ed8:  cmp r0, #1                        
  14eda:  bne #0x14f32                      
  14edc:  b #0x14ef4                        -> 0x14ef4 (вне списка функций)
  14ede:  ldr r0, [pc, #0x64]               -> RAM
  14ee0:  ldrb r0, [r0]                     
  14ee2:  cmp r0, #1                        
  14ee4:  bne #0x14ef2                      
  14ee6:  ldr r0, [pc, #0x60]               -> RAM
  14ee8:  ldrb r0, [r0]                     
  14eea:  cbnz r0, #0x14ef2                 
  14eec:  movs r0, #1                       
  14eee:  ldr r1, [pc, #0x50]               -> RAM
  14ef0:  strb r0, [r1]                     
  14ef2:  b #0x14f3a                        -> 0x14f3a (вне списка функций)
  14ef4:  bl #0x8e14                        -> func_0x08e14
  14ef8:  cmp r0, #1                        
  14efa:  bne #0x14f08                      
  14efc:  movs r0, #0                       
  14efe:  ldr r1, [pc, #0x40]               -> RAM
  14f00:  strb r0, [r1]                     
  14f02:  ldr r1, [pc, #0x48]               -> RAM
  14f04:  strb r0, [r1]                     
  14f06:  b #0x14f30                        -> 0x14f30 (вне списка функций)
  14f08:  ldr r0, [pc, #0x3c]               -> RAM
  14f0a:  ldrb r0, [r0]                     
  14f0c:  cbz r0, #0x14f2a                  
  14f0e:  ldr r0, [pc, #0x3c]               -> RAM
  14f10:  ldrb r0, [r0]                     
  14f12:  adds r0, r0, #1                   
  14f14:  ldr r1, [pc, #0x34]               -> RAM
  14f16:  strb r0, [r1]                     
  14f18:  mov r0, r1                        
  14f1a:  ldrb r0, [r0]                     
  14f1c:  cmp r0, #0x32                     
  14f1e:  ble #0x14f30                      
  14f20:  movs r0, #0                       
  14f22:  strb r0, [r1]                     
  14f24:  ldr r1, [pc, #0x18]               -> RAM
  14f26:  strb r0, [r1]                     
  14f28:  b #0x14f30                        -> 0x14f30 (вне списка функций)
  14f2a:  movs r0, #0                       
  14f2c:  ldr r1, [pc, #0x1c]               -> RAM
  14f2e:  strb r0, [r1]                     
  14f30:  b #0x14f3a                        -> 0x14f3a (вне списка функций)
  14f32:  movs r0, #0                       
  14f34:  ldr r1, [pc, #8]                  -> RAM
  14f36:  strb r0, [r1]                     
  14f38:  nop                               
  14f3a:  nop                               
  14f3c:  pop {r4, pc}                      
  ; --- literal-пул @0x14f40 (4 слов) — ВНЕ границ функции ---
  14f40:  .word 0x20000031  ; RAM
  14f44:  .word 0x20000107  ; RAM
  14f48:  .word 0x20000080  ; RAM
  14f4c:  .word 0x20000042  ; RAM
```
