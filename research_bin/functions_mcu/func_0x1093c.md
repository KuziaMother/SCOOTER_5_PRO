# func_0x1093c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001093c) | `0x0001093c` |
| размер кода | 118 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000004a — RAM (r0)
- 0x20000060 — RAM (r0)
- 0x2000008c — RAM (r0)
- 0x20000fc7 — RAM (r1)

## Вызовы (callees)

- 0x109b0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x128c8` (bl @0x000128d4)


## Дизассембляция

```asm
  1093c:  ldr r0, [pc, #0x74]               -> RAM
  1093e:  ldrb r0, [r0]                     
  10940:  ldr r1, [pc, #0x74]               -> RAM
  10942:  strb r0, [r1]                     
  10944:  ldr r0, [pc, #0x6c]               -> RAM
  10946:  ldrb r0, [r0, #1]                 
  10948:  strb r0, [r1, #1]                 
  1094a:  ldr r0, [pc, #0x68]               -> RAM
  1094c:  ldrb r0, [r0, #2]                 
  1094e:  strb r0, [r1, #2]                 
  10950:  ldr r0, [pc, #0x60]               -> RAM
  10952:  ldrb r0, [r0, #3]                 
  10954:  strb r0, [r1, #3]                 
  10956:  ldr r0, [pc, #0x5c]               -> RAM
  10958:  ldrb r0, [r0, #4]                 
  1095a:  strb r0, [r1, #4]                 
  1095c:  mov r0, r1                        
  1095e:  ldrb r0, [r0, #6]                 
  10960:  ubfx r0, r0, #6, #1               
  10964:  cbnz r0, #0x109aa                 
  10966:  mov r0, r1                        
  10968:  ldrsb.w r0, [r0, #2]              
  1096c:  ldrsb.w r1, [r1, #5]              
  10970:  cmp r0, r1                        
  10972:  ble #0x109a2                      
  10974:  ldr r0, [pc, #0x44]               -> RAM
  10976:  ldrb r0, [r0]                     
  10978:  adds r0, r0, #1                   
  1097a:  ldr r1, [pc, #0x40]               -> RAM
  1097c:  strb r0, [r1]                     
  1097e:  mov r0, r1                        
  10980:  ldrb r0, [r0]                     
  10982:  cmp r0, #0xa                      
  10984:  ble #0x109b0                      
  10986:  ldr r0, [pc, #0x30]               -> RAM
  10988:  ldrb r0, [r0, #2]                 
  1098a:  ldr r1, [pc, #0x2c]               -> RAM
  1098c:  strb r0, [r1, #5]                 
  1098e:  ldr r0, [pc, #0x30]               -> RAM
  10990:  ldr r0, [r0]                      
  10992:  orr r0, r0, #0x1000               
  10996:  ldr r1, [pc, #0x28]               -> RAM
  10998:  str r0, [r1]                      
  1099a:  movs r0, #0                       
  1099c:  ldr r1, [pc, #0x1c]               -> RAM
  1099e:  strb r0, [r1]                     
  109a0:  b #0x109b0                        -> 0x109b0 (вне списка функций)
  109a2:  movs r0, #0                       
  109a4:  ldr r1, [pc, #0x14]               -> RAM
  109a6:  strb r0, [r1]                     
  109a8:  b #0x109b0                        -> 0x109b0 (вне списка функций)
  109aa:  movs r0, #0                       
  109ac:  ldr r1, [pc, #0xc]                -> RAM
  109ae:  strb r0, [r1]                     
  109b0:  bx lr                             
  ; --- literal-пул @0x109b4 (4 слов) — ВНЕ границ функции ---
  109b4:  .word 0x2000004a  ; RAM
  109b8:  .word 0x20000fc7  ; RAM
  109bc:  .word 0x20000060  ; RAM
  109c0:  .word 0x2000008c  ; RAM
```
