# func_0x01fe0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001fe0) | `0x00001fe0` |
| размер кода | 200 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000000 — RAM (r1)
- 0x20000a77 — RAM (r0)
- 0x20000a78 — RAM (r1)
- 0x20000a79 — RAM (r0)
- 0x20000dd8 — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x40010c18 — периферия (r1)

## Вызовы (callees)

- 0x0207e (b, вне списка функций)
- 0x020a6 (b, вне списка функций)
- 0x029d4 (bl, вне списка функций)
- `func_0x02a5c` (0x00002a5c, bl)
- `func_0x0af94` (0x0000af94, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01cea` (bl @0x00001cec)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0202c..0x0206a` (62 Б); цели из: 0x01ff8
- `0x0206a..0x0207e` (20 Б); цели из: 0x02062
- `0x0207e..0x0208a` (12 Б); цели из: 0x02068, 0x02070
- `0x0208a..0x020a6` (28 Б); цели из: 0x01fe8
- `0x020a6..0x020a8` (2 Б); цели из: 0x0202a, 0x02032, 0x0203a, 0x02088

## Дизассембляция

```asm
  01fe0:  push {r3, lr}                     
  01fe2:  bl #0x29d4                        -> 0x029d4 (вне списка функций)
  01fe6:  cmp r0, #0                        
  01fe8:  beq #0x208a                       
  01fea:  ldr r0, [pc, #0xbc]               -> RAM
  01fec:  ldrb r0, [r0]                     
  01fee:  adds r0, r0, #1                   
  01ff0:  uxtb r0, r0                       
  01ff2:  ldr r1, [pc, #0xb4]               -> RAM
  01ff4:  strb r0, [r1]                     
  01ff6:  cmp r0, #5                        
  01ff8:  blt #0x202c                       
  01ffa:  movs r0, #0                       
  01ffc:  strb r0, [r1]                     
  01ffe:  ldr r0, [pc, #0xac]               -> RAM
  02000:  bl #0xaf94                        -> func_0x0af94
  02004:  mov.w r0, #0x1f4                  
  02008:  str r0, [sp]                      
  0200a:  nop                               
  0200c:  ldr r0, [sp]                      
  0200e:  subs r1, r0, #1                   
  02010:  str r1, [sp]                      
  02012:  cmp r0, #0                        
  02014:  bne #0x200c                       
  02016:  movs r0, #1                       
  02018:  ldr r1, [pc, #0x94]               -> RAM
  0201a:  strb r0, [r1]                     
  0201c:  ldr r0, [pc, #0x94]               -> RAM
  0201e:  ldrb r0, [r0, #3]                 
  02020:  bic r0, r0, #4                    
  02024:  adds r0, r0, #4                   
  02026:  ldr r1, [pc, #0x8c]               -> RAM
  02028:  strb r0, [r1, #3]                 
  0202a:  b #0x20a6                         -> 0x020a6 (вне списка функций)
  0202c:  ldr r0, [pc, #0x80]               -> RAM
  0202e:  ldrb r0, [r0]                     
  02030:  cmp r0, #1                        
  02032:  bne #0x20a6                       
  02034:  ldr r0, [pc, #0x70]               -> RAM
  02036:  ldrb r0, [r0]                     
  02038:  cmp r0, #2                        
  0203a:  ble #0x20a6                       
  0203c:  movs r0, #2                       
  0203e:  ldr r1, [pc, #0x78]               -> периферия
  02040:  str r0, [r1]                      
  02042:  mov.w r0, #0x1f4                  
  02046:  str r0, [sp]                      
  02048:  nop                               
  0204a:  ldr r0, [sp]                      
  0204c:  subs r1, r0, #1                   
  0204e:  str r1, [sp]                      
  02050:  cmp r0, #0                        
  02052:  bne #0x204a                       
  02054:  movs r0, #2                       
  02056:  ldr r1, [pc, #0x60]               -> периферия
  02058:  adds r1, #0x10                    
  0205a:  str r0, [r1]                      
  0205c:  ldr r0, [pc, #0x5c]               -> RAM
  0205e:  ldrb r0, [r0]                     
  02060:  cmp r0, #3                        
  02062:  bge #0x206a                       
  02064:  bl #0x2a5c                        -> func_0x02a5c
  02068:  b #0x207e                         -> 0x0207e (вне списка функций)
  0206a:  ldr r0, [pc, #0x50]               -> RAM
  0206c:  ldrb r0, [r0]                     
  0206e:  cmp r0, #4                        
  02070:  blt #0x207e                       
  02072:  movs r0, #1                       
  02074:  ldr r1, [pc, #0x48]               -> RAM
  02076:  strb r0, [r1]                     
  02078:  movs r0, #0                       
  0207a:  ldr r1, [pc, #0x40]               -> RAM
  0207c:  strb r0, [r1]                     
  0207e:  ldr r0, [pc, #0x3c]               -> RAM
  02080:  ldrb r0, [r0]                     
  02082:  adds r0, r0, #1                   
  02084:  ldr r1, [pc, #0x34]               -> RAM
  02086:  strb r0, [r1]                     
  02088:  b #0x20a6                         -> 0x020a6 (вне списка функций)
  0208a:  movs r0, #0                       
  0208c:  ldr r1, [pc, #0x2c]               -> RAM
  0208e:  strb r0, [r1]                     
  02090:  ldr r1, [pc, #0x1c]               -> RAM
  02092:  strb r0, [r1]                     
  02094:  ldr r0, [pc, #0x1c]               -> RAM
  02096:  ldrb r0, [r0, #3]                 
  02098:  bic r0, r0, #4                    
  0209c:  ldr r1, [pc, #0x14]               -> RAM
  0209e:  strb r0, [r1, #3]                 
  020a0:  movs r0, #0                       
  020a2:  ldr r1, [pc, #4]                  -> RAM
  020a4:  strb r0, [r1]                     
  020a6:  pop {r3, pc}                      
  ; --- literal-пул @0x020a8 (7 слов) — ВНЕ границ функции ---
  020a8:  .word 0x20000a77  ; RAM
  020ac:  .word 0x20000dd8  ; RAM
  020b0:  .word 0x20000a78  ; RAM
  020b4:  .word 0x20000f70  ; RAM
  020b8:  .word 0x40010c18  ; периферия
  020bc:  .word 0x20000a79  ; RAM
  020c0:  .word 0x20000000  ; RAM
```
