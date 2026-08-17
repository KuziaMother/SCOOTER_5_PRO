# func_0x0ea64

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ea64) | `0x0000ea64` |
| размер кода | 504 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00018448 — данные @0x18448 (r1)
- 0x000186a0 — данные @0x186a0 (r0)
- 0x2000128b — RAM (r1)
- 0x200012ba — RAM (r0)
- 0xffff3cb0 — прочее (r0)

## Вызовы (callees)

- `func_0x08d90` (0x00008d90, bl)
- 0x0eaac (b, вне списка функций)
- 0x0eb0c (b, вне списка функций)
- 0x0eb62 (b, вне списка функций)
- 0x0ebc6 (b, вне списка функций)
- 0x0ebce (b, вне списка функций)
- 0x0ebf4 (b, вне списка функций)
- 0x0ec36 (b, вне списка функций)
- 0x0ec58 (b, вне списка функций)
- 0x10e5c (bl, вне списка функций)
- 0x1654c (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x063b8` (bl @0x00006486)
- `func_0x063b8` (bl @0x000064a6)
- `func_0x063b8` (bl @0x0000656e)
- `func_0x063b8` (bl @0x000065a0)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0ea86..0x0eaa4` (30 Б); цели из: 0x0ea70, 0x0ea7e
- `0x0eaa4..0x0eaac` (8 Б); цели из: 0x0ea8c, 0x0ea9c
- `0x0eaac..0x0eaca` (30 Б); цели из: 0x0ea84, 0x0eaa2
- `0x0eaca..0x0eae6` (28 Б); цели из: 0x0eab4, 0x0eaba
- `0x0eae6..0x0eb04` (30 Б); цели из: 0x0ead0, 0x0eade
- `0x0eb04..0x0eb0c` (8 Б); цели из: 0x0eaec, 0x0eafc
- `0x0eb0c..0x0eb20` (20 Б); цели из: 0x0eae4, 0x0eb02
- `0x0eb20..0x0eb3c` (28 Б); цели из: 0x0eb10
- `0x0eb3c..0x0eb5a` (30 Б); цели из: 0x0eb26, 0x0eb34
- `0x0eb5a..0x0eb62` (8 Б); цели из: 0x0eb42, 0x0eb52
- `0x0eb62..0x0eb76` (20 Б); цели из: 0x0eb3a, 0x0eb58
- `0x0eb76..0x0eb96` (32 Б); цели из: 0x0eb66
- `0x0eb96..0x0ebb8` (34 Б); цели из: 0x0eb7c, 0x0eb8a
- `0x0ebb8..0x0ebc6` (14 Б); цели из: 0x0eb9c, 0x0ebac
- `0x0ebc6..0x0ebce` (8 Б); цели из: 0x0eb94, 0x0ebb6
- `0x0ebce..0x0ebe6` (24 Б); цели из: 0x0eac8, 0x0eb1e, 0x0eb74
- `0x0ebe6..0x0ebee` (8 Б); цели из: 0x0ebde
- `0x0ebee..0x0ebf4` (6 Б); цели из: 0x0ebd4
- `0x0ebf4..0x0ec0a` (22 Б); цели из: 0x0ebe4, 0x0ebec
- `0x0ec0a..0x0ec10` (6 Б); цели из: 0x0ec04
- `0x0ec10..0x0ec28` (24 Б); цели из: 0x0ebf6
- `0x0ec28..0x0ec30` (8 Б); цели из: 0x0ec20
- `0x0ec30..0x0ec36` (6 Б); цели из: 0x0ec16
- `0x0ec36..0x0ec4c` (22 Б); цели из: 0x0ec26, 0x0ec2e
- `0x0ec4c..0x0ec52` (6 Б); цели из: 0x0ec48
- `0x0ec52..0x0ec58` (6 Б); цели из: 0x0ec38
- `0x0ec58..0x0ec5c` (4 Б); цели из: 0x0ec0e, 0x0ec50

## Дизассембляция

```asm
  0ea64:  push.w {r4, r5, r6, r7, r8, lr}   
  0ea68:  mov r4, r0                        
  0ea6a:  bl #0x8d90                        -> func_0x08d90
  0ea6e:  cmp r0, #0                        
  0ea70:  bge #0xea86                       
  0ea72:  bl #0x8d90                        -> func_0x08d90
  0ea76:  rsb.w r0, r0, #-0x80000000        
  0ea7a:  ldr r1, [r4]                      
  0ea7c:  cmp r0, r1                        
  0ea7e:  ble #0xea86                       
  0ea80:  mov.w r5, #-0x80000000            
  0ea84:  b #0xeaac                         -> 0x0eaac (вне списка функций)
  0ea86:  bl #0x8d90                        -> func_0x08d90
  0ea8a:  cmp r0, #0                        
  0ea8c:  ble #0xeaa4                       
  0ea8e:  bl #0x8d90                        -> func_0x08d90
  0ea92:  mvn r1, #0x80000000               
  0ea96:  subs r0, r1, r0                   
  0ea98:  ldr r1, [r4]                      
  0ea9a:  cmp r0, r1                        
  0ea9c:  bge #0xeaa4                       
  0ea9e:  mvn r5, #0x80000000               
  0eaa2:  b #0xeaac                         -> 0x0eaac (вне списка функций)
  0eaa4:  bl #0x8d90                        -> func_0x08d90
  0eaa8:  ldr r1, [r4]                      
  0eaaa:  adds r5, r0, r1                   
  0eaac:  bl #0x8d90                        -> func_0x08d90
  0eab0:  ldr r1, [pc, #0x1a8]              -> данные @0x18448
  0eab2:  cmp r0, r1                        
  0eab4:  bgt #0xeaca                       
  0eab6:  mov r0, r1                        
  0eab8:  cmp r5, r0                        
  0eaba:  ble #0xeaca                       
  0eabc:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  0eac0:  bl #0x8d90                        -> func_0x08d90
  0eac4:  ldr r1, [pc, #0x198]              -> RAM
  0eac6:  str r0, [r1, #0x18]               
  0eac8:  b #0xebce                         -> 0x0ebce (вне списка функций)
  0eaca:  bl #0x8d90                        -> func_0x08d90
  0eace:  cmp r0, #0                        
  0ead0:  bge #0xeae6                       
  0ead2:  bl #0x8d90                        -> func_0x08d90
  0ead6:  rsb.w r0, r0, #-0x80000000        
  0eada:  ldr r1, [r4]                      
  0eadc:  cmp r0, r1                        
  0eade:  ble #0xeae6                       
  0eae0:  mov.w r5, #-0x80000000            
  0eae4:  b #0xeb0c                         -> 0x0eb0c (вне списка функций)
  0eae6:  bl #0x8d90                        -> func_0x08d90
  0eaea:  cmp r0, #0                        
  0eaec:  ble #0xeb04                       
  0eaee:  bl #0x8d90                        -> func_0x08d90
  0eaf2:  mvn r1, #0x80000000               
  0eaf6:  subs r0, r1, r0                   
  0eaf8:  ldr r1, [r4]                      
  0eafa:  cmp r0, r1                        
  0eafc:  bge #0xeb04                       
  0eafe:  mvn r5, #0x80000000               
  0eb02:  b #0xeb0c                         -> 0x0eb0c (вне списка функций)
  0eb04:  bl #0x8d90                        -> func_0x08d90
  0eb08:  ldr r1, [r4]                      
  0eb0a:  adds r5, r0, r1                   
  0eb0c:  ldr r0, [pc, #0x154]              
  0eb0e:  cmp r5, r0                        
  0eb10:  bge #0xeb20                       
  0eb12:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  0eb16:  bl #0x8d90                        -> func_0x08d90
  0eb1a:  ldr r1, [pc, #0x144]              -> RAM
  0eb1c:  str r0, [r1, #0x18]               
  0eb1e:  b #0xebce                         -> 0x0ebce (вне списка функций)
  0eb20:  bl #0x8d90                        -> func_0x08d90
  0eb24:  cmp r0, #0                        
  0eb26:  bge #0xeb3c                       
  0eb28:  bl #0x8d90                        -> func_0x08d90
  0eb2c:  rsb.w r0, r0, #-0x80000000        
  0eb30:  ldr r1, [r4]                      
  0eb32:  cmp r0, r1                        
  0eb34:  ble #0xeb3c                       
  0eb36:  mov.w r5, #-0x80000000            
  0eb3a:  b #0xeb62                         -> 0x0eb62 (вне списка функций)
  0eb3c:  bl #0x8d90                        -> func_0x08d90
  0eb40:  cmp r0, #0                        
  0eb42:  ble #0xeb5a                       
  0eb44:  bl #0x8d90                        -> func_0x08d90
  0eb48:  mvn r1, #0x80000000               
  0eb4c:  subs r0, r1, r0                   
  0eb4e:  ldr r1, [r4]                      
  0eb50:  cmp r0, r1                        
  0eb52:  bge #0xeb5a                       
  0eb54:  mvn r5, #0x80000000               
  0eb58:  b #0xeb62                         -> 0x0eb62 (вне списка функций)
  0eb5a:  bl #0x8d90                        -> func_0x08d90
  0eb5e:  ldr r1, [r4]                      
  0eb60:  adds r5, r0, r1                   
  0eb62:  ldr r0, [pc, #0x104]              -> данные @0x186a0
  0eb64:  cmp r5, r0                        
  0eb66:  blt #0xeb76                       
  0eb68:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  0eb6c:  bl #0x8d90                        -> func_0x08d90
  0eb70:  ldr r1, [pc, #0xec]               -> RAM
  0eb72:  str r0, [r1, #0x18]               
  0eb74:  b #0xebce                         -> 0x0ebce (вне списка функций)
  0eb76:  bl #0x8d90                        -> func_0x08d90
  0eb7a:  cmp r0, #0                        
  0eb7c:  bge #0xeb96                       
  0eb7e:  bl #0x8d90                        -> func_0x08d90
  0eb82:  rsb.w r0, r0, #-0x80000000        
  0eb86:  ldr r1, [r4]                      
  0eb88:  cmp r0, r1                        
  0eb8a:  ble #0xeb96                       
  0eb8c:  mov.w r0, #-0x80000000            
  0eb90:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  0eb94:  b #0xebc6                         -> 0x0ebc6 (вне списка функций)
  0eb96:  bl #0x8d90                        -> func_0x08d90
  0eb9a:  cmp r0, #0                        
  0eb9c:  ble #0xebb8                       
  0eb9e:  bl #0x8d90                        -> func_0x08d90
  0eba2:  mvn r1, #0x80000000               
  0eba6:  subs r0, r1, r0                   
  0eba8:  ldr r1, [r4]                      
  0ebaa:  cmp r0, r1                        
  0ebac:  bge #0xebb8                       
  0ebae:  mvn r0, #0x80000000               
  0ebb2:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  0ebb6:  b #0xebc6                         -> 0x0ebc6 (вне списка функций)
  0ebb8:  bl #0x8d90                        -> func_0x08d90
  0ebbc:  ldr r1, [r4]                      
  0ebbe:  adds r7, r0, r1                   
  0ebc0:  mov r0, r7                        
  0ebc2:  bl #0x10e5c                       -> 0x10e5c (вне списка функций)
  0ebc6:  bl #0x8d90                        -> func_0x08d90
  0ebca:  ldr r1, [pc, #0x94]               -> RAM
  0ebcc:  str r0, [r1, #0x18]               
  0ebce:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ebd2:  cmp r0, #0                        
  0ebd4:  bge #0xebee                       
  0ebd6:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ebda:  cmp.w r0, #-0x80000000            
  0ebde:  bgt #0xebe6                       
  0ebe0:  mvn r5, #0x80000000               
  0ebe4:  b #0xebf4                         -> 0x0ebf4 (вне списка функций)
  0ebe6:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ebea:  rsbs r5, r0, #0                   
  0ebec:  b #0xebf4                         -> 0x0ebf4 (вне списка функций)
  0ebee:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ebf2:  mov r5, r0                        
  0ebf4:  cmp r5, #0x64                     
  0ebf6:  bge #0xec10                       
  0ebf8:  ldr r0, [pc, #0x70]               -> RAM
  0ebfa:  ldr r0, [r0, #0x44]               
  0ebfc:  adds r6, r0, #1                   
  0ebfe:  ldr r0, [pc, #0x6c]               -> RAM
  0ec00:  ldr r0, [r0, #0x44]               
  0ec02:  cmp r0, r6                        
  0ec04:  bls #0xec0a                       
  0ec06:  mov.w r6, #-1                     
  0ec0a:  ldr r0, [pc, #0x60]               -> RAM
  0ec0c:  str r6, [r0, #0x44]               
  0ec0e:  b #0xec58                         -> 0x0ec58 (вне списка функций)
  0ec10:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ec14:  cmp r0, #0                        
  0ec16:  bge #0xec30                       
  0ec18:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ec1c:  cmp.w r0, #-0x80000000            
  0ec20:  bgt #0xec28                       
  0ec22:  mvn r5, #0x80000000               
  0ec26:  b #0xec36                         -> 0x0ec36 (вне списка функций)
  0ec28:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ec2c:  rsbs r5, r0, #0                   
  0ec2e:  b #0xec36                         -> 0x0ec36 (вне списка функций)
  0ec30:  bl #0x1654c                       -> 0x1654c (вне списка функций)
  0ec34:  mov r5, r0                        
  0ec36:  cmp r5, #0xc8                     
  0ec38:  bge #0xec52                       
  0ec3a:  ldr r0, [pc, #0x30]               -> RAM
  0ec3c:  ldr r0, [r0, #0x44]               
  0ec3e:  sub.w r6, r0, #0x64               
  0ec42:  ldr r0, [pc, #0x28]               -> RAM
  0ec44:  ldr r0, [r0, #0x44]               
  0ec46:  cmp r0, r6                        
  0ec48:  bhs #0xec4c                       
  0ec4a:  movs r6, #0                       
  0ec4c:  ldr r0, [pc, #0x1c]               -> RAM
  0ec4e:  str r6, [r0, #0x44]               
  0ec50:  b #0xec58                         -> 0x0ec58 (вне списка функций)
  0ec52:  movs r0, #0                       
  0ec54:  ldr r1, [pc, #0x14]               -> RAM
  0ec56:  str r0, [r1, #0x44]               
  0ec58:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x0ec5c (5 слов) — ВНЕ границ функции ---
  0ec5c:  .word 0x00018448  ; данные @0x18448
  0ec60:  .word 0x2000128b  ; RAM
  0ec64:  .word 0xffff3cb0
  0ec68:  .word 0x000186a0  ; данные @0x186a0
  0ec6c:  .word 0x200012ba  ; RAM
```
