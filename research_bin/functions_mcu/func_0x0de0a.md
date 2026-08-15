# func_0x0de0a

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000de0a) | `0x0000de0a` |
| размер кода | 196 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200009b5 — RAM (r3)
- 0x200009b8 — RAM (r0)
- 0x20000fe7 — RAM (r1)
- 0x20001222 — RAM (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x01ac8` (0x00001ac8, bl)
- 0x0de88 (b, вне списка функций)
- 0x0de8c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0de7c..0x0de88` (12 Б); цели из: 0x0de70
- `0x0de88..0x0de8c` (4 Б); цели из: 0x0de62
- `0x0de8c..0x0de8e` (2 Б); цели из: 0x0de7a
- `0x0de8e..0x0deb6` (40 Б); цели из: 0x0de5e
- `0x0deb6..0x0debe` (8 Б); цели из: 0x0deb0
- `0x0debe..0x0deca` (12 Б); цели из: 0x0deb4
- `0x0deca..0x0dece` (4 Б); цели из: 0x0dec0

## Дизассембляция

```asm
  0de0a:  push {r0, r1, r2, r3, r4, r5, r6, lr}
  0de0c:  movs r5, #0                       
  0de0e:  movs r6, #0                       
  0de10:  movs r0, #0                       
  0de12:  str r0, [sp]                      
  0de14:  str r0, [sp, #4]                  
  0de16:  str r0, [sp, #8]                  
  0de18:  str r0, [sp, #0xc]                
  0de1a:  ldrb.w r6, [sp, #0x21]            
  0de1e:  movs r2, #0x10                    
  0de20:  ldr r1, [pc, #0x74]               -> RAM
  0de22:  mov r0, sp                        
  0de24:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0de28:  ldr r0, [pc, #0x70]               -> RAM
  0de2a:  ldr r0, [r0]                      
  0de2c:  lsrs r0, r0, #0x18                
  0de2e:  strb.w r0, [sp, #0xc]             
  0de32:  ldr r0, [pc, #0x68]               -> RAM
  0de34:  ldr r0, [r0]                      
  0de36:  lsrs r0, r0, #0x10                
  0de38:  strb.w r0, [sp, #0xd]             
  0de3c:  ldr r0, [pc, #0x5c]               -> RAM
  0de3e:  ldrh r0, [r0]                     
  0de40:  lsrs r0, r0, #8                   
  0de42:  strb.w r0, [sp, #0xe]             
  0de46:  ldr r0, [pc, #0x54]               -> RAM
  0de48:  ldrb r0, [r0]                     
  0de4a:  strb.w r0, [sp, #0xf]             
  0de4e:  movs r1, #0x10                    
  0de50:  mov r0, sp                        
  0de52:  bl #0x1ac8                        -> func_0x01ac8
  0de56:  movs r0, #0                       
  0de58:  ldr r1, [pc, #0x44]               -> RAM
  0de5a:  strb r0, [r1, #0xa]               
  0de5c:  cmp r6, #0x1d                     
  0de5e:  bne #0xde8e                       
  0de60:  movs r4, #0                       
  0de62:  b #0xde88                         -> 0x0de88 (вне списка функций)
  0de64:  ldrb.w r1, [sp, r4]               
  0de68:  add.w r0, sp, #0x23               
  0de6c:  ldrb r0, [r0, r4]                 
  0de6e:  cmp r1, r0                        
  0de70:  beq #0xde7c                       
  0de72:  movs r5, #0                       
  0de74:  movs r0, #2                       
  0de76:  ldr r1, [pc, #0x28]               -> RAM
  0de78:  strb r0, [r1, #0xa]               
  0de7a:  b #0xde8c                         -> 0x0de8c (вне списка функций)
  0de7c:  movs r5, #1                       
  0de7e:  movs r0, #1                       
  0de80:  ldr r1, [pc, #0x1c]               -> RAM
  0de82:  strb r0, [r1, #0xa]               
  0de84:  adds r0, r4, #1                   
  0de86:  uxtb r4, r0                       
  0de88:  cmp r4, #0x10                     
  0de8a:  blt #0xde64                       
  0de8c:  nop                               
  0de8e:  mov r0, r5                        
  0de90:  add sp, #0x10                     
  0de92:  pop {r4, r5, r6}                  
  0de94:  ldr pc, [sp], #0x14               
  0de98:  asrs r2, r4, #8                   
  0de9a:  movs r0, #0                       
  0de9c:  lsrs r0, r7, #6                   
  0de9e:  movs r0, #0                       
  0dea0:  lsrs r7, r4, #0x1f                
  0dea2:  movs r0, #0                       
  0dea4:  push {r0, r1, r2, r3}             
  0dea6:  movs r0, #0                       
  0dea8:  movs r1, #0                       
  0deaa:  ldrb.w r1, [sp, #1]               
  0deae:  cmp r1, #9                        
  0deb0:  beq #0xdeb6                       
  0deb2:  cmp r1, #0xb                      
  0deb4:  bne #0xdebe                       
  0deb6:  movs r0, #1                       
  0deb8:  movs r2, #3                       
  0deba:  ldr r3, [pc, #0x14]               -> RAM
  0debc:  strb r2, [r3]                     
  0debe:  cmp r1, #0xa                      
  0dec0:  bne #0xdeca                       
  0dec2:  movs r0, #1                       
  0dec4:  movs r2, #3                       
  0dec6:  ldr r3, [pc, #8]                  -> RAM
  0dec8:  strb r2, [r3]                     
  0deca:  add sp, #0x10                     
  0decc:  bx lr                             
  ; --- literal-пул @0x0de98 (3 слов) ---
  0de98:  .word 0x20001222  ; RAM
  0de9c:  .word 0x200009b8  ; RAM
  0dea0:  .word 0x20000fe7  ; RAM
  ; --- literal-пул @0x0ded0 (1 слов) — ВНЕ границ функции ---
  0ded0:  .word 0x200009b5  ; RAM
```
