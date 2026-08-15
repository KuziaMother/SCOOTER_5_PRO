# func_0x1dea4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001dea4) | `0x0001dea4` |
| размер кода | 186 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0000a8e4 — данные @0x0a8e4 (r1)
- 0x20000328 — RAM (r2)
- 0x20000329 — RAM (r0)
- 0x2000032a — RAM (r0)
- 0x2000032b — RAM (r0)
- 0x2000032c — RAM (r0)
- 0x2000032d — RAM (r0)
- 0x200003c8 — RAM (r0)
- 0x2000080c — RAM (r0)

## Вызовы (callees)

- `func_0x19a68` (0x00019a68, bl)
- 0x1df0a (b, вне списка функций)
- 0x1df5a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1c838` (bl @0x0001c9c0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1dedc..0x1df0e` (50 Б); цели из: 0x1ded0
- `0x1df0e..0x1df44` (54 Б); цели из: 0x1dee0
- `0x1df44..0x1df48` (4 Б); цели из: 0x1df3a
- `0x1df48..0x1df4c` (4 Б); цели из: 0x1df28
- `0x1df4c..0x1df50` (4 Б); цели из: 0x1df2c
- `0x1df50..0x1df54` (4 Б); цели из: 0x1df30
- `0x1df54..0x1df58` (4 Б); цели из: 0x1df34
- `0x1df58..0x1df5a` (2 Б); цели из: 0x1df3e
- `0x1df5a..0x1df5e` (4 Б); цели из: 0x1df4a, 0x1df4e, 0x1df52, 0x1df56

## Дизассембляция

```asm
  1dea4:  push {r0, r1, r2, r4, r5, r6, r7, lr}
  1dea6:  sub sp, #0x28                     
  1dea8:  movs r2, #0x24                    
  1deaa:  ldr r1, [pc, #0xb4]               -> данные @0x0a8e4
  1deac:  mov r0, sp                        
  1deae:  bl #0x19a68                       -> func_0x19a68
  1deb2:  movs r7, #0                       
  1deb4:  ldr r0, [pc, #0xac]               -> RAM
  1deb6:  movs r1, #1                       
  1deb8:  strb r7, [r0, #4]                 
  1deba:  strb r7, [r0, #3]                 
  1debc:  ldrb r2, [r0, #4]                 
  1debe:  mov r3, sp                        
  1dec0:  lsls r4, r2, #2                   
  1dec2:  adds r4, r2, r4                   
  1dec4:  adds r4, r4, r3                   
  1dec6:  ldrb r3, [r0, #3]                 
  1dec8:  ldr r5, [sp, #0x28]               
  1deca:  ldrb r6, [r4, r3]                 
  1decc:  ldrb r5, [r5, r3]                 
  1dece:  cmp r5, r6                        
  1ded0:  bne #0x1dedc                      
  1ded2:  adds r3, r3, #1                   
  1ded4:  uxtb r3, r3                       
  1ded6:  strb r3, [r0, #3]                 
  1ded8:  cmp r3, #5                        
  1deda:  blo #0x1dec6                      
  1dedc:  uxtb r3, r3                       
  1dede:  cmp r3, #5                        
  1dee0:  beq #0x1df0e                      
  1dee2:  adds r2, r2, #1                   
  1dee4:  uxtb r2, r2                       
  1dee6:  strb r2, [r0, #4]                 
  1dee8:  cmp r2, #7                        
  1deea:  blo #0x1deba                      
  1deec:  ldrb r2, [r0, #2]                 
  1deee:  cmp r2, #0xff                     
  1def0:  bne #0x1df0a                      
  1def2:  strb r7, [r0, #2]                 
  1def4:  ldr r0, [pc, #0x70]               -> RAM
  1def6:  strb r1, [r0]                     
  1def8:  ldr r0, [pc, #0x70]               -> RAM
  1defa:  ldrh r1, [r0, #2]                 
  1defc:  ldr r0, [sp, #0x2c]               
  1defe:  strh r1, [r0]                     
  1df00:  ldr r0, [pc, #0x68]               -> RAM
  1df02:  adds r0, #0xe                     
  1df04:  ldrh r1, [r0, #2]                 
  1df06:  ldr r0, [sp, #0x30]               
  1df08:  strh r1, [r0]                     
  1df0a:  add sp, #0x34                     
  1df0c:  pop {r4, r5, r6, r7, pc}          
  1df0e:  uxtb r3, r2                       
  1df10:  ldr r4, [pc, #0x58]               -> RAM
  1df12:  strb r3, [r0, #2]                 
  1df14:  lsls r2, r2, #1                   
  1df16:  ldrh r5, [r4, r2]                 
  1df18:  ldr r4, [sp, #0x2c]               
  1df1a:  strh r5, [r4]                     
  1df1c:  ldr r4, [pc, #0x4c]               -> RAM
  1df1e:  adds r4, #0xe                     
  1df20:  ldrh r4, [r4, r2]                 
  1df22:  ldr r2, [sp, #0x30]               
  1df24:  cmp r3, #0                        
  1df26:  strh r4, [r2]                     
  1df28:  beq #0x1df48                      
  1df2a:  cmp r3, #1                        
  1df2c:  beq #0x1df4c                      
  1df2e:  cmp r3, #2                        
  1df30:  beq #0x1df50                      
  1df32:  cmp r3, #3                        
  1df34:  beq #0x1df54                      
  1df36:  ldr r2, [pc, #0x38]               -> RAM
  1df38:  cmp r3, #4                        
  1df3a:  beq #0x1df44                      
  1df3c:  cmp r3, #5                        
  1df3e:  beq #0x1df58                      
  1df40:  cmp r3, #6                        
  1df42:  bne #0x1deec                      
  1df44:  strb r1, [r2]                     
  1df46:  b #0x1df0a                        -> 0x1df0a (вне списка функций)
  1df48:  ldr r0, [pc, #0x28]               -> RAM
  1df4a:  b #0x1df5a                        -> 0x1df5a (вне списка функций)
  1df4c:  ldr r0, [pc, #0x18]               -> RAM
  1df4e:  b #0x1df5a                        -> 0x1df5a (вне списка функций)
  1df50:  ldr r0, [pc, #0x24]               -> RAM
  1df52:  b #0x1df5a                        -> 0x1df5a (вне списка функций)
  1df54:  ldr r0, [pc, #0x24]               -> RAM
  1df56:  b #0x1df5a                        -> 0x1df5a (вне списка функций)
  1df58:  ldr r0, [pc, #0x24]               -> RAM
  1df5a:  strb r1, [r0]                     
  1df5c:  b #0x1df0a                        -> 0x1df0a (вне списка функций)
  ; --- literal-пул @0x1df60 (9 слов) — ВНЕ границ функции ---
  1df60:  .word 0x0000a8e4  ; данные @0x0a8e4
  1df64:  .word 0x200003c8  ; RAM
  1df68:  .word 0x2000032d  ; RAM
  1df6c:  .word 0x2000080c  ; RAM
  1df70:  .word 0x20000328  ; RAM
  1df74:  .word 0x2000032c  ; RAM
  1df78:  .word 0x2000032b  ; RAM
  1df7c:  .word 0x20000329  ; RAM
  1df80:  .word 0x2000032a  ; RAM
```
