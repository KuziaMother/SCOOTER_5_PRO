# func_0x15c94

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080015c94) | `0x00015c94` |
| размер кода | 66 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801aa9a — flash-mirror @0x1aa9a (r1)
- 0x20001fac — RAM (r0)

## Вызовы (callees)

- 0x011ec (bl, вне списка функций)
- 0x15cb8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x04a4c` (bl @0x00004a7c)


## Дизассембляция

```asm
  15c94:  push {r4, r5, r6, lr}             
  15c96:  mov r5, r0                        
  15c98:  mov r6, r1                        
  15c9a:  movs r4, #0                       
  15c9c:  nop                               
  15c9e:  b #0x15cb8                        -> 0x15cb8 (вне списка функций)
  15ca0:  ldr r0, [pc, #0x34]               -> RAM
  15ca2:  ldrb r0, [r0, #3]                 
  15ca4:  add.w r1, r0, r0, lsl #3          
  15ca8:  add.w r0, r1, r0, lsl #4          
  15cac:  ldr r1, [pc, #0x2c]               -> flash-mirror @0x1aa9a
  15cae:  add.w r0, r1, r0, lsl #1          
  15cb2:  ldrb r0, [r0, r4]                 
  15cb4:  strb r0, [r5, r4]                 
  15cb6:  adds r4, r4, #1                   
  15cb8:  ldr r1, [pc, #0x1c]               -> RAM
  15cba:  ldrb r1, [r1, #3]                 
  15cbc:  add.w r2, r1, r1, lsl #3          
  15cc0:  add.w r1, r2, r1, lsl #4          
  15cc4:  ldr r2, [pc, #0x14]               -> flash-mirror @0x1aa9a
  15cc6:  add.w r0, r2, r1, lsl #1          
  15cca:  bl #0x11ec                        -> 0x011ec (вне списка функций)
  15cce:  cmp r0, r4                        
  15cd0:  bhi #0x15ca0                      
  15cd2:  strb r4, [r6]                     
  15cd4:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x15cd8 (2 слов) — ВНЕ границ функции ---
  15cd8:  .word 0x20001fac  ; RAM
  15cdc:  .word 0x0801aa9a  ; flash-mirror @0x1aa9a
```
