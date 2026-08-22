# func_0x0bd50

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000bd50) | `0x0000bd50` |
| размер кода | 280 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001154 — RAM (r1)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- 0x0bda6 (b, вне списка функций)
- 0x0bde0 (b, вне списка функций)
- 0x0bdf0 (b, вне списка функций)
- 0x0be64 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0bd7c..0x0bd90` (20 Б); цели из: 0x0bd70
- `0x0bd90..0x0bda6` (22 Б); цели из: 0x0bd74
- `0x0bda6..0x0bdca` (36 Б); цели из: 0x0bd7a
- `0x0bdca..0x0bdda` (16 Б); цели из: 0x0bdc2
- `0x0bdda..0x0bde0` (6 Б); цели из: 0x0bd78
- `0x0bde0..0x0bdee` (14 Б); цели из: 0x0bd8e, 0x0bda4, 0x0bdc8, 0x0bdd8
- `0x0bdee..0x0bdf4` (6 Б); цели из: 0x0bde6
- `0x0bdf4..0x0be50` (92 Б); цели из: 0x0bdec
- `0x0be50..0x0be58` (8 Б); цели из: 0x0be3e, 0x0be46
- `0x0be58..0x0be5e` (6 Б); цели из: 0x0be2e, 0x0be36, 0x0be4e
- `0x0be5e..0x0be64` (6 Б); цели из: 0x0be56
- `0x0be64..0x0be68` (4 Б); цели из: 0x0be5c

## Дизассембляция

```asm
  0bd50:  push.w {r4, r5, r6, r7, r8, lr}   
  0bd54:  mov r4, r0                        
  0bd56:  mov r5, r1                        
  0bd58:  movs r7, #0                       
  0bd5a:  movs r6, #0                       
  0bd5c:  mov r8, r6                        
  0bd5e:  nop                               
  0bd60:  ldrb r0, [r4, #2]                 
  0bd62:  ldr r1, [pc, #0x104]              -> RAM
  0bd64:  strb r0, [r1]                     
  0bd66:  ldrb r0, [r4, #3]                 
  0bd68:  strb r0, [r1, #1]                 
  0bd6a:  mov r0, r1                        
  0bd6c:  ldrb r0, [r0, #1]                 
  0bd6e:  cmp r0, #3                        
  0bd70:  beq #0xbd7c                       
  0bd72:  cmp r0, #6                        
  0bd74:  beq #0xbd90                       
  0bd76:  cmp r0, #0x10                     
  0bd78:  bne #0xbdda                       
  0bd7a:  b #0xbda6                         -> 0x0bda6 (вне списка функций)
  0bd7c:  ldrb r0, [r4, #4]                 
  0bd7e:  ldr r1, [pc, #0xe8]               -> RAM
  0bd80:  strb r0, [r1, #2]                 
  0bd82:  ldrb r0, [r4, #5]                 
  0bd84:  strb r0, [r1, #3]                 
  0bd86:  ldrb r0, [r4, #6]                 
  0bd88:  strb r0, [r1, #4]                 
  0bd8a:  ldrb r0, [r4, #7]                 
  0bd8c:  strb r0, [r1, #5]                 
  0bd8e:  b #0xbde0                         -> 0x0bde0 (вне списка функций)
  0bd90:  ldrb r0, [r4, #4]                 
  0bd92:  ldr r1, [pc, #0xd4]               -> RAM
  0bd94:  strb r0, [r1, #2]                 
  0bd96:  ldrb r0, [r4, #5]                 
  0bd98:  strb r0, [r1, #3]                 
  0bd9a:  ldrb r0, [r4, #6]                 
  0bd9c:  strb r0, [r1, #7]                 
  0bd9e:  ldrb r1, [r4, #7]                 
  0bda0:  ldr r0, [pc, #0xc4]               -> RAM
  0bda2:  strb r1, [r0, #8]                 
  0bda4:  b #0xbde0                         -> 0x0bde0 (вне списка функций)
  0bda6:  ldrb r0, [r4, #4]                 
  0bda8:  ldr r1, [pc, #0xbc]               -> RAM
  0bdaa:  strb r0, [r1, #2]                 
  0bdac:  ldrb r0, [r4, #5]                 
  0bdae:  strb r0, [r1, #3]                 
  0bdb0:  ldrb r0, [r4, #6]                 
  0bdb2:  strb r0, [r1, #4]                 
  0bdb4:  ldrb r0, [r4, #7]                 
  0bdb6:  strb r0, [r1, #5]                 
  0bdb8:  ldrb r0, [r4, #8]                 
  0bdba:  strb r0, [r1, #6]                 
  0bdbc:  mov r0, r1                        
  0bdbe:  ldrb r0, [r0, #6]                 
  0bdc0:  cmp r0, #0x82                     
  0bdc2:  ble #0xbdca                       
  0bdc4:  mov.w r8, #0                      
  0bdc8:  b #0xbde0                         -> 0x0bde0 (вне списка функций)
  0bdca:  ldr r0, [pc, #0x9c]               -> RAM
  0bdcc:  ldrb r2, [r0, #6]                 
  0bdce:  add.w r1, r4, #9                  
  0bdd2:  adds r0, r0, #7                   
  0bdd4:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0bdd8:  b #0xbde0                         -> 0x0bde0 (вне списка функций)
  0bdda:  mov.w r8, #0                      
  0bdde:  nop                               
  0bde0:  nop                               
  0bde2:  ldrh r0, [r4]                     
  0bde4:  cmp r0, #8                        
  0bde6:  blt #0xbdee                       
  0bde8:  ldrh r0, [r4]                     
  0bdea:  cmp r0, #0x82                     
  0bdec:  ble #0xbdf4                       
  0bdee:  movs r0, #0                       
  0bdf0:  pop.w {r4, r5, r6, r7, r8, pc}    
  0bdf4:  ldrh r0, [r4]                     
  0bdf6:  subs r0, r0, #2                   
  0bdf8:  adds r1, r4, #2                   
  0bdfa:  ldrb r0, [r1, r0]                 
  0bdfc:  ldr r1, [pc, #0x68]               -> RAM
  0bdfe:  strb.w r0, [r1, #0x9d]            
  0be02:  ldrh r0, [r4]                     
  0be04:  subs r0, r0, #1                   
  0be06:  adds r1, r4, #2                   
  0be08:  ldrb r0, [r1, r0]                 
  0be0a:  ldr r1, [pc, #0x5c]               -> RAM
  0be0c:  strb.w r0, [r1, #0x9e]            
  0be10:  mov r0, r1                        
  0be12:  ldrb.w r6, [r0, #0x9d]            
  0be16:  ldrb.w r0, [r0, #0x9e]            
  0be1a:  orr.w r6, r0, r6, lsl #8          
  0be1e:  ldrh r0, [r4]                     
  0be20:  subs r0, r0, #2                   
  0be22:  uxth r1, r0                       
  0be24:  adds r0, r4, #2                   
  0be26:  bl #0x8a50                        -> func_0x08a50
  0be2a:  mov r7, r0                        
  0be2c:  cmp r7, r6                        
  0be2e:  bne #0xbe58                       
  0be30:  ldr r0, [pc, #0x34]               -> RAM
  0be32:  ldrb r0, [r0]                     
  0be34:  cmp r0, #0x6e                     
  0be36:  bne #0xbe58                       
  0be38:  ldr r0, [pc, #0x2c]               -> RAM
  0be3a:  ldrb r0, [r0, #1]                 
  0be3c:  cmp r0, #0x10                     
  0be3e:  beq #0xbe50                       
  0be40:  ldr r0, [pc, #0x24]               -> RAM
  0be42:  ldrb r0, [r0, #1]                 
  0be44:  cmp r0, #3                        
  0be46:  beq #0xbe50                       
  0be48:  ldr r0, [pc, #0x1c]               -> RAM
  0be4a:  ldrb r0, [r0, #1]                 
  0be4c:  cmp r0, #6                        
  0be4e:  bne #0xbe58                       
  0be50:  ldr r0, [pc, #0x14]               -> RAM
  0be52:  ldrb r0, [r0, #6]                 
  0be54:  cmp r0, #0x82                     
  0be56:  ble #0xbe5e                       
  0be58:  movs r5, #0                       
  0be5a:  mov r8, r5                        
  0be5c:  b #0xbe64                         -> 0x0be64 (вне списка функций)
  0be5e:  ldr r5, [pc, #8]                  -> RAM
  0be60:  mov.w r8, #1                      
  0be64:  mov r0, r8                        
  0be66:  b #0xbdf0                         -> 0x0bdf0 (вне списка функций)
  ; --- literal-пул @0x0be68 (1 слов) — ВНЕ границ функции ---
  0be68:  .word 0x20001154  ; RAM
```
