# func_0x1ce38

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001ce38) | `0x0001ce38` |
| размер кода | 522 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00000bb8 — данные @0x00bb8 (r6)
- 0x00001770 — данные @0x01770 (r6)
- 0x20000216 — RAM (r6)
- 0x20000218 — RAM (r4)
- 0x20000268 — RAM (r3)
- 0x2000026a — RAM (r3)
- 0x2000026e — RAM (r6)
- 0x2000031a — RAM (r3)
- 0x200003c8 — RAM (r3)
- 0x2000169a — RAM (r0)
- 0x20001768 — RAM (r4)
- 0x40012c40 — периферия (r2)
- 0xffffd8f0 — прочее (r3)

## Вызовы (callees)

- 0x1ce60 (b, вне списка функций)
- 0x1cf0e (b, вне списка функций)
- 0x1cf36 (b, вне списка функций)
- 0x1cf50 (b, вне списка функций)
- 0x1cf52 (b, вне списка функций)
- 0x1cfaa (b, вне списка функций)
- 0x1cfac (b, вне списка функций)
- 0x1cfca (b, вне списка функций)
- 0x1cfe4 (b, вне списка функций)
- 0x1d002 (b, вне списка функций)
- 0x1d012 (b, вне списка функций)
- 0x21b52 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1b67c` (bl @0x0001b7c8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1ce68..0x1ce76` (14 Б); цели из: 0x1ce46
- `0x1ce76..0x1ce7e` (8 Б); цели из: 0x1ce70
- `0x1ce7e..0x1cf08` (138 Б); цели из: 0x1ce4c
- `0x1cf08..0x1cf0c` (4 Б); цели из: 0x1ce9e, 0x1cea2, 0x1ceb0, 0x1ceb4…
- `0x1cf0c..0x1cf0e` (2 Б); цели из: 0x1cea6, 0x1ceaa, 0x1ceb8, 0x1cebc…
- `0x1cf0e..0x1cf20` (18 Б); цели из: 0x1ceac, 0x1cebe, 0x1ced0, 0x1cee2…
- `0x1cf20..0x1cf32` (18 Б); цели из: 0x1cf18
- `0x1cf32..0x1cf36` (4 Б); цели из: 0x1cf26
- `0x1cf36..0x1cf3a` (4 Б); цели из: 0x1cf30
- `0x1cf3a..0x1cf4c` (18 Б); цели из: 0x1cf1c
- `0x1cf4c..0x1cf50` (4 Б); цели из: 0x1cf40
- `0x1cf50..0x1cf52` (2 Б); цели из: 0x1cf4a
- `0x1cf52..0x1cf6e` (28 Б); цели из: 0x1cf1e, 0x1cf38
- `0x1cf6e..0x1cf70` (2 Б); цели из: 0x1ce88
- `0x1cf70..0x1cf82` (18 Б); цели из: 0x1cf64
- `0x1cf82..0x1cf98` (22 Б); цели из: 0x1cf5c
- `0x1cf98..0x1cf9c` (4 Б); цели из: 0x1cf8e
- `0x1cf9c..0x1cfa0` (4 Б); цели из: 0x1cf72
- `0x1cfa0..0x1cfaa` (10 Б); цели из: 0x1cf9a
- `0x1cfaa..0x1cfac` (2 Б); цели из: 0x1cf6c, 0x1cf7e, 0x1cf96
- `0x1cfac..0x1cfae` (2 Б); цели из: 0x1cf6e
- `0x1cfae..0x1cfca` (28 Б); цели из: 0x1cf84
- `0x1cfca..0x1cfe4` (26 Б); цели из: 0x1cf80, 0x1cf9e, 0x1cfa8, 0x1cfac
- `0x1cfe4..0x1cfea` (6 Б); цели из: 0x1ce66, 0x1cfd6
- `0x1cfea..0x1d000` (22 Б); цели из: 0x1cfd0
- `0x1d000..0x1d002` (2 Б); цели из: 0x1cffa
- `0x1d002..0x1d00c` (10 Б); цели из: 0x1cffe
- `0x1d00c..0x1d012` (6 Б); цели из: 0x1d004
- `0x1d012..0x1d034` (34 Б); цели из: 0x1d00a
- `0x1d034..0x1d042` (14 Б); цели из: 0x1d016

## Дизассембляция

```asm
  1ce38:  push {r4, r5, r6, r7, lr}         
  1ce3a:  ldr r3, [pc, #0x208]              -> RAM
  1ce3c:  movs r2, #1                       
  1ce3e:  ldrb r5, [r3]                     
  1ce40:  movs r1, #0                       
  1ce42:  ldr r0, [pc, #0x204]              -> RAM
  1ce44:  cmp r5, #0                        
  1ce46:  beq #0x1ce68                      
  1ce48:  ldr r4, [pc, #0x200]              -> RAM
  1ce4a:  cmp r5, #1                        
  1ce4c:  beq #0x1ce7e                      
  1ce4e:  mov r2, r3                        
  1ce50:  strb r1, [r2]                     
  1ce52:  ldr r2, [pc, #0x1fc]              -> периферия
  1ce54:  strb r1, [r4]                     
  1ce56:  ldr r3, [r2, #0x14]               
  1ce58:  movs r4, #1                       
  1ce5a:  lsls r4, r4, #0xf                 
  1ce5c:  bics r3, r4                       
  1ce5e:  str r3, [r2, #0x14]               
  1ce60:  strh r1, [r0, #8]                 
  1ce62:  strh r1, [r0, #6]                 
  1ce64:  strh r1, [r0, #4]                 
  1ce66:  b #0x1cfe4                        -> 0x1cfe4 (вне списка функций)
  1ce68:  ldr r4, [pc, #0x1e8]              -> RAM
  1ce6a:  movs r5, #8                       
  1ce6c:  ldrsh r5, [r4, r5]                
  1ce6e:  cmp r5, #0x68                     
  1ce70:  bge #0x1ce76                      
  1ce72:  strb r2, [r3]                     
  1ce74:  pop {r4, r5, r6, r7, pc}          
  1ce76:  strb r1, [r3]                     
  1ce78:  ldr r3, [pc, #0x1dc]              -> RAM
  1ce7a:  strb r2, [r3]                     
  1ce7c:  b #0x1ce60                        -> 0x1ce60 (вне списка функций)
  1ce7e:  ldr r3, [pc, #0x1dc]              -> RAM
  1ce80:  ldrb r5, [r3, #0xa]               
  1ce82:  ldr r3, [pc, #0x1dc]              -> RAM
  1ce84:  ldrb r7, [r3]                     
  1ce86:  cmp r5, r7                        
  1ce88:  beq #0x1cf6e                      
  1ce8a:  movs r6, #2                       
  1ce8c:  movs r3, r7                       
  1ce8e:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1ce92:  subs r6, #7                       
  1ce94:  lsrs r2, r6, #0x18                
  1ce96:  movs r0, #5                       
  1ce98:  asrs r1, r5, #0x1c                
  1ce9a:  movs r6, r7                       
  1ce9c:  cmp r5, #1                        
  1ce9e:  beq #0x1cf08                      
  1cea0:  cmp r5, #5                        
  1cea2:  beq #0x1cf08                      
  1cea4:  cmp r5, #2                        
  1cea6:  beq #0x1cf0c                      
  1cea8:  cmp r5, #6                        
  1ceaa:  beq #0x1cf0c                      
  1ceac:  b #0x1cf0e                        -> 0x1cf0e (вне списка функций)
  1ceae:  cmp r5, #3                        
  1ceb0:  beq #0x1cf08                      
  1ceb2:  cmp r5, #1                        
  1ceb4:  beq #0x1cf08                      
  1ceb6:  cmp r5, #6                        
  1ceb8:  beq #0x1cf0c                      
  1ceba:  cmp r5, #4                        
  1cebc:  beq #0x1cf0c                      
  1cebe:  b #0x1cf0e                        -> 0x1cf0e (вне списка функций)
  1cec0:  cmp r5, #2                        
  1cec2:  beq #0x1cf08                      
  1cec4:  cmp r5, #3                        
  1cec6:  beq #0x1cf08                      
  1cec8:  cmp r5, #4                        
  1ceca:  beq #0x1cf0c                      
  1cecc:  cmp r5, #5                        
  1cece:  beq #0x1cf0c                      
  1ced0:  b #0x1cf0e                        -> 0x1cf0e (вне списка функций)
  1ced2:  cmp r5, #6                        
  1ced4:  beq #0x1cf08                      
  1ced6:  cmp r5, #2                        
  1ced8:  beq #0x1cf08                      
  1ceda:  cmp r5, #5                        
  1cedc:  beq #0x1cf0c                      
  1cede:  cmp r5, #1                        
  1cee0:  beq #0x1cf0c                      
  1cee2:  b #0x1cf0e                        -> 0x1cf0e (вне списка функций)
  1cee4:  cmp r5, #4                        
  1cee6:  beq #0x1cf08                      
  1cee8:  cmp r5, #6                        
  1ceea:  beq #0x1cf08                      
  1ceec:  cmp r5, #1                        
  1ceee:  beq #0x1cf0c                      
  1cef0:  cmp r5, #3                        
  1cef2:  beq #0x1cf0c                      
  1cef4:  b #0x1cf0e                        -> 0x1cf0e (вне списка функций)
  1cef6:  cmp r5, #5                        
  1cef8:  beq #0x1cf08                      
  1cefa:  cmp r5, #4                        
  1cefc:  beq #0x1cf08                      
  1cefe:  cmp r5, #3                        
  1cf00:  beq #0x1cf0c                      
  1cf02:  cmp r5, #2                        
  1cf04:  beq #0x1cf0c                      
  1cf06:  b #0x1cf0e                        -> 0x1cf0e (вне списка функций)
  1cf08:  strh r6, [r0, #0xa]               
  1cf0a:  b #0x1cf0e                        -> 0x1cf0e (вне списка функций)
  1cf0c:  strh r2, [r0, #0xa]               
  1cf0e:  ldr r3, [pc, #0x14c]              -> RAM
  1cf10:  strb r7, [r3, #0xa]               
  1cf12:  movs r3, #0xa                     
  1cf14:  ldrsh r3, [r0, r3]                
  1cf16:  cmp r3, #1                        
  1cf18:  beq #0x1cf20                      
  1cf1a:  cmp r3, #2                        
  1cf1c:  beq #0x1cf3a                      
  1cf1e:  b #0x1cf52                        -> 0x1cf52 (вне списка функций)
  1cf20:  movs r3, #2                       
  1cf22:  ldrsh r3, [r0, r3]                
  1cf24:  cmp r3, #2                        
  1cf26:  ble #0x1cf32                      
  1cf28:  ldrh r3, [r0, #4]                 
  1cf2a:  adds r3, r3, #1                   
  1cf2c:  strh r3, [r0, #4]                 
  1cf2e:  strh r1, [r0, #2]                 
  1cf30:  b #0x1cf36                        -> 0x1cf36 (вне списка функций)
  1cf32:  adds r3, r3, #1                   
  1cf34:  strh r3, [r0, #2]                 
  1cf36:  strh r1, [r0]                     
  1cf38:  b #0x1cf52                        -> 0x1cf52 (вне списка функций)
  1cf3a:  movs r3, #0                       
  1cf3c:  ldrsh r3, [r0, r3]                
  1cf3e:  cmp r3, #2                        
  1cf40:  ble #0x1cf4c                      
  1cf42:  ldrh r3, [r0, #6]                 
  1cf44:  adds r3, r3, #1                   
  1cf46:  strh r3, [r0, #6]                 
  1cf48:  strh r1, [r0]                     
  1cf4a:  b #0x1cf50                        -> 0x1cf50 (вне списка функций)
  1cf4c:  adds r3, r3, #1                   
  1cf4e:  strh r3, [r0]                     
  1cf50:  strh r1, [r0, #2]                 
  1cf52:  movs r5, #4                       
  1cf54:  movs r3, #6                       
  1cf56:  ldrsh r5, [r0, r5]                
  1cf58:  ldrsh r3, [r0, r3]                
  1cf5a:  cmp r5, r3                        
  1cf5c:  ble #0x1cf82                      
  1cf5e:  subs r5, r5, r3                   
  1cf60:  ldr r3, [pc, #0x100]              
  1cf62:  cmp r5, #0x14                     
  1cf64:  ble #0x1cf70                      
  1cf66:  movs r5, #0x14                    
  1cf68:  strh r5, [r0, #4]                 
  1cf6a:  strh r1, [r0, #6]                 
  1cf6c:  b #0x1cfaa                        -> 0x1cfaa (вне списка функций)
  1cf6e:  b #0x1cfac                        -> 0x1cfac (вне списка функций)
  1cf70:  cmp r5, #3                        
  1cf72:  blt #0x1cf9c                      
  1cf74:  lsls r5, r5, #9                   
  1cf76:  rsbs r5, r5, #0                   
  1cf78:  sxth r5, r5                       
  1cf7a:  strh r5, [r0, #8]                 
  1cf7c:  cmp r5, r3                        
  1cf7e:  blt #0x1cfaa                      
  1cf80:  b #0x1cfca                        -> 0x1cfca (вне списка функций)
  1cf82:  cmp r3, r5                        
  1cf84:  ble #0x1cfae                      
  1cf86:  subs r5, r3, r5                   
  1cf88:  ldr r3, [pc, #0xd8]               
  1cf8a:  rsbs r3, r3, #0                   
  1cf8c:  cmp r5, #0x14                     
  1cf8e:  ble #0x1cf98                      
  1cf90:  movs r5, #0xa                     
  1cf92:  strh r5, [r0, #6]                 
  1cf94:  strh r1, [r0, #4]                 
  1cf96:  b #0x1cfaa                        -> 0x1cfaa (вне списка функций)
  1cf98:  cmp r5, #3                        
  1cf9a:  bge #0x1cfa0                      
  1cf9c:  strh r1, [r0, #8]                 
  1cf9e:  b #0x1cfca                        -> 0x1cfca (вне списка функций)
  1cfa0:  lsls r5, r5, #9                   
  1cfa2:  sxth r5, r5                       
  1cfa4:  strh r5, [r0, #8]                 
  1cfa6:  cmp r5, r3                        
  1cfa8:  ble #0x1cfca                      
  1cfaa:  strh r3, [r0, #8]                 
  1cfac:  b #0x1cfca                        -> 0x1cfca (вне списка функций)
  1cfae:  strh r1, [r0, #6]                 
  1cfb0:  strh r1, [r0, #4]                 
  1cfb2:  strh r1, [r0, #8]                 
  1cfb4:  strb r1, [r0, #0xe]               
  1cfb6:  ldr r3, [pc, #0x8c]               -> RAM
  1cfb8:  strh r1, [r0, #0xc]               
  1cfba:  strb r1, [r3]                     
  1cfbc:  ldr r3, [pc, #0x90]               -> периферия
  1cfbe:  strb r1, [r4]                     
  1cfc0:  ldr r5, [r3, #0x14]               
  1cfc2:  movs r6, #1                       
  1cfc4:  lsls r6, r6, #0xf                 
  1cfc6:  bics r5, r6                       
  1cfc8:  str r5, [r3, #0x14]               
  1cfca:  ldr r3, [pc, #0x84]               -> периферия
  1cfcc:  ldr r5, [r3, #0x14]               
  1cfce:  lsls r5, r5, #0x10                
  1cfd0:  bmi #0x1cfea                      
  1cfd2:  ldrh r5, [r0, #8]                 
  1cfd4:  cmp r5, #0                        
  1cfd6:  beq #0x1cfe4                      
  1cfd8:  strb r2, [r4]                     
  1cfda:  ldr r2, [r3, #0x14]               
  1cfdc:  movs r4, #1                       
  1cfde:  lsls r4, r4, #0xf                 
  1cfe0:  orrs r2, r4                       
  1cfe2:  str r2, [r3, #0x14]               
  1cfe4:  strb r1, [r0, #0xe]               
  1cfe6:  strh r1, [r0, #0xc]               
  1cfe8:  pop {r4, r5, r6, r7, pc}          
  1cfea:  ldr r6, [pc, #0x7c]               -> RAM
  1cfec:  movs r5, #0                       
  1cfee:  ldrsh r5, [r6, r5]                
  1cff0:  ldr r6, [pc, #0x78]               -> RAM
  1cff2:  movs r7, #0                       
  1cff4:  ldrsh r7, [r6, r7]                
  1cff6:  cmp r5, r7                        
  1cff8:  ldrh r5, [r0, #0xc]               
  1cffa:  bge #0x1d000                      
  1cffc:  ldr r6, [pc, #0x70]               -> данные @0x00bb8
  1cffe:  b #0x1d002                        -> 0x1d002 (вне списка функций)
  1d000:  ldr r6, [pc, #0x70]               -> данные @0x01770
  1d002:  cmp r5, r6                        
  1d004:  blo #0x1d00c                      
  1d006:  strh r6, [r0, #0xc]               
  1d008:  strb r2, [r0, #0xe]               
  1d00a:  b #0x1d012                        -> 0x1d012 (вне списка функций)
  1d00c:  adds r5, r5, #1                   
  1d00e:  strh r5, [r0, #0xc]               
  1d010:  strb r1, [r0, #0xe]               
  1d012:  ldrh r2, [r0, #8]                 
  1d014:  cmp r2, #0                        
  1d016:  beq #0x1d034                      
  1d018:  ldrb r2, [r0, #0xe]               
  1d01a:  cmp r2, #1                        
  1d01c:  bne #0x1cfe8                      
  1d01e:  strh r1, [r0, #0xc]               
  1d020:  strb r1, [r0, #0xe]               
  1d022:  strh r1, [r0, #6]                 
  1d024:  strh r1, [r0, #4]                 
  1d026:  strh r1, [r0, #8]                 
  1d028:  strb r1, [r4]                     
  1d02a:  ldr r1, [r3, #0x14]               
  1d02c:  lsls r0, r2, #0xf                 
  1d02e:  bics r1, r0                       
  1d030:  str r1, [r3, #0x14]               
  1d032:  pop {r4, r5, r6, r7, pc}          
  1d034:  strb r1, [r4]                     
  1d036:  ldr r0, [r3, #0x14]               
  1d038:  movs r1, #1                       
  1d03a:  lsls r1, r1, #0xf                 
  1d03c:  bics r0, r1                       
  1d03e:  str r0, [r3, #0x14]               
  1d040:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1d044 (13 слов) — ВНЕ границ функции ---
  1d044:  .word 0x2000026a  ; RAM
  1d048:  .word 0x2000169a  ; RAM
  1d04c:  .word 0x20000218  ; RAM
  1d050:  .word 0x40012c40  ; периферия
  1d054:  .word 0x20001768  ; RAM
  1d058:  .word 0x2000031a  ; RAM
  1d05c:  .word 0x200003c8  ; RAM
  1d060:  .word 0x20000268  ; RAM
  1d064:  .word 0xffffd8f0
  1d068:  .word 0x2000026e  ; RAM
  1d06c:  .word 0x20000216  ; RAM
  1d070:  .word 0x00000bb8  ; данные @0x00bb8
  1d074:  .word 0x00001770  ; данные @0x01770
```
