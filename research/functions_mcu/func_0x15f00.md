# func_0x15f00

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015f00) | `0x00015f00` |
| размер кода | 116 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000c7f — RAM (r0)
- 0x20001f10 — RAM (r0)
- 0x20001fac — RAM (r0)

## Вызовы (callees)

- `func_0x15a1c` (0x00015a1c, bl)
- 0x15f24 (b, вне списка функций)
- 0x15fa6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x15b84` (bl @0x00015c1c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x15f14..0x15f26` (18 Б); цели из: 0x15f08
- `0x15f26..0x15f3c` (22 Б); цели из: 0x15f1a
- `0x15f3c..0x15f60` (36 Б); цели из: 0x15f30
- `0x15f60..0x15f74` (20 Б); цели из: 0x15f54

## Дизассембляция

```asm
  15f00:  push {r4, lr}                     
  15f02:  ldr r0, [pc, #0xb8]               -> RAM
  15f04:  ldrb r0, [r0, #1]                 
  15f06:  cmp r0, #1                        
  15f08:  bne #0x15f14                      
  15f0a:  ldr r0, [pc, #0xb4]               -> RAM
  15f0c:  ldrh r0, [r0, #0xc]               
  15f0e:  cbnz r0, #0x15f14                 
  15f10:  bl #0x15a1c                       -> func_0x15a1c
  15f14:  ldr r0, [pc, #0xac]               -> RAM
  15f16:  ldrb r0, [r0]                     
  15f18:  cmp r0, #1                        
  15f1a:  bne #0x15f26                      
  15f1c:  movs r0, #7                       
  15f1e:  ldr r1, [pc, #0xa0]               -> RAM
  15f20:  strb r0, [r1, #3]                 
  15f22:  movs r0, #0                       
  15f24:  pop {r4, pc}                      
  15f26:  ldr r0, [pc, #0x94]               -> RAM
  15f28:  ldrb r0, [r0, #1]                 
  15f2a:  ldr r1, [pc, #0x94]               -> RAM
  15f2c:  ldrh r1, [r1, #8]                 
  15f2e:  cmp r0, r1                        
  15f30:  bne #0x15f3c                      
  15f32:  movs r0, #2                       
  15f34:  ldr r1, [pc, #0x88]               -> RAM
  15f36:  strb r0, [r1, #3]                 
  15f38:  movs r0, #0                       
  15f3a:  b #0x15f24                        -> 0x15f24 (вне списка функций)
  15f3c:  ldr r1, [pc, #0x80]               -> RAM
  15f3e:  ldrh r0, [r1, #6]                 
  15f40:  ldr r1, [pc, #0x78]               -> RAM
  15f42:  ldrb r2, [r1, #1]                 
  15f44:  asrs r1, r0, #0x1f                
  15f46:  add.w r1, r0, r1, lsr #28         
  15f4a:  asrs r1, r1, #4                   
  15f4c:  sub.w r1, r0, r1, lsl #4          
  15f50:  adds r1, r1, #1                   
  15f52:  cmp r2, r1                        
  15f54:  beq #0x15f60                      
  15f56:  movs r0, #3                       
  15f58:  ldr r1, [pc, #0x64]               -> RAM
  15f5a:  strb r0, [r1, #3]                 
  15f5c:  movs r0, #0                       
  15f5e:  b #0x15f24                        -> 0x15f24 (вне списка функций)
  15f60:  ldr r0, [pc, #0x58]               -> RAM
  15f62:  ldrb r0, [r0, #1]                 
  15f64:  ldr r1, [pc, #0x58]               -> RAM
  15f66:  strh r0, [r1, #6]                 
  15f68:  mov r0, r1                        
  15f6a:  ldrh r0, [r0, #0xc]               
  15f6c:  cbnz r0, #0x15f74                 
  15f6e:  movs r0, #1                       
  15f70:  strb r0, [r1]                     
  15f72:  b #0x15fa6                        -> 0x15fa6 (вне списка функций)
  ; --- literal-пул @0x15fbc (3 слов) — ВНЕ границ функции ---
  15fbc:  .word 0x20001f10  ; RAM
  15fc0:  .word 0x20001fac  ; RAM
  15fc4:  .word 0x20000c7f  ; RAM
```
