# func_0x0ee48

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ee48) | `0x0000ee48` |
| размер кода | 298 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20002ffa — RAM (r0)

## Вызовы (callees)

- 0x0ee8e (b, вне списка функций)
- 0x0eeca (b, вне списка функций)
- 0x0ef18 (b, вне списка функций)
- 0x0ef6e (b, вне списка функций)
- `func_0x170e0` (0x000170e0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x07494` (bl @0x00007882)
- `func_0x07494` (bl @0x0000789c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0ee64..0x0ee80` (28 Б); цели из: 0x0ee60
- `0x0ee80..0x0ee88` (8 Б); цели из: 0x0ee7c
- `0x0ee88..0x0ee8e` (6 Б); цели из: 0x0ee68
- `0x0ee8e..0x0eea0` (18 Б); цели из: 0x0ee86
- `0x0eea0..0x0eeb4` (20 Б); цели из: 0x0ee9a
- `0x0eeb4..0x0eec4` (16 Б); цели из: 0x0eeac
- `0x0eec4..0x0eeca` (6 Б); цели из: 0x0eebc
- `0x0eeca..0x0eee8` (30 Б); цели из: 0x0eeb2, 0x0eec2
- `0x0eee8..0x0eef6` (14 Б); цели из: 0x0eee2
- `0x0eef6..0x0ef04` (14 Б); цели из: 0x0eef0
- `0x0ef04..0x0ef0a` (6 Б); цели из: 0x0ef00
- `0x0ef0a..0x0ef16` (12 Б); цели из: 0x0ef06
- `0x0ef16..0x0ef18` (2 Б); цели из: 0x0eea4
- `0x0ef18..0x0ef3e` (38 Б); цели из: 0x0ef14
- `0x0ef3e..0x0ef5c` (30 Б); цели из: 0x0ef26, 0x0ef34
- `0x0ef5c..0x0ef68` (12 Б); цели из: 0x0ef44, 0x0ef50
- `0x0ef68..0x0ef6e` (6 Б); цели из: 0x0ef1e
- `0x0ef6e..0x0ef72` (4 Б); цели из: 0x0ef3c, 0x0ef5a, 0x0ef66

## Дизассембляция

```asm
  0ee48:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  0ee4c:  mov r5, r0                        
  0ee4e:  mov r7, r1                        
  0ee50:  mov r8, r2                        
  0ee52:  ldrh r0, [r5]                     
  0ee54:  sub.w r6, r0, #0xf                
  0ee58:  ldrh r0, [r5]                     
  0ee5a:  subs r0, #0xf                     
  0ee5c:  ldrh r1, [r5]                     
  0ee5e:  cmp r0, r1                        
  0ee60:  bls #0xee64                       
  0ee62:  movs r6, #0                       
  0ee64:  ldrh r0, [r7]                     
  0ee66:  cmp r0, r6                        
  0ee68:  bge #0xee88                       
  0ee6a:  ldr r0, [pc, #0x108]              -> RAM
  0ee6c:  ldrsb.w r0, [r0, #0x14]           
  0ee70:  adds r4, r0, #1                   
  0ee72:  ldr r0, [pc, #0x100]              -> RAM
  0ee74:  ldrsb.w r0, [r0, #0x14]           
  0ee78:  adds r0, r0, #1                   
  0ee7a:  cmp r0, #0x7f                     
  0ee7c:  ble #0xee80                       
  0ee7e:  movs r4, #0x7f                    
  0ee80:  sxtb r0, r4                       
  0ee82:  ldr r1, [pc, #0xf0]               -> RAM
  0ee84:  strb r0, [r1, #0x14]              
  0ee86:  b #0xee8e                         -> 0x0ee8e (вне списка функций)
  0ee88:  movs r0, #0                       
  0ee8a:  ldr r1, [pc, #0xe8]               -> RAM
  0ee8c:  strb r0, [r1, #0x14]              
  0ee8e:  ldrh r0, [r5]                     
  0ee90:  adds r6, r0, #1                   
  0ee92:  ldrh r0, [r5]                     
  0ee94:  adds r0, r0, #1                   
  0ee96:  cmp.w r0, #0x10000                
  0ee9a:  blo #0xeea0                       
  0ee9c:  movw r6, #0xffff                  
  0eea0:  ldrh r0, [r7]                     
  0eea2:  cmp r0, r6                        
  0eea4:  blt #0xef16                       
  0eea6:  ldr r0, [pc, #0xcc]               -> RAM
  0eea8:  ldr r0, [r0]                      
  0eeaa:  cmp r0, #0                        
  0eeac:  blt #0xeeb4                       
  0eeae:  ldr r0, [pc, #0xc4]               -> RAM
  0eeb0:  ldr r6, [r0]                      
  0eeb2:  b #0xeeca                         -> 0x0eeca (вне списка функций)
  0eeb4:  ldr r0, [pc, #0xbc]               -> RAM
  0eeb6:  ldr r0, [r0]                      
  0eeb8:  cmp.w r0, #-0x80000000            
  0eebc:  bne #0xeec4                       
  0eebe:  mov.w r6, #-0x80000000            
  0eec2:  b #0xeeca                         -> 0x0eeca (вне списка функций)
  0eec4:  ldr r0, [pc, #0xac]               -> RAM
  0eec6:  ldr r0, [r0]                      
  0eec8:  rsbs r6, r0, #0                   
  0eeca:  mov.w r0, #0x3e8                  
  0eece:  udiv sb, r6, r0                   
  0eed2:  add.w r0, sb, sb, lsl #1          
  0eed6:  rsb r0, r0, sb, lsl #7            
  0eeda:  sub.w r6, r6, r0, lsl #3          
  0eede:  cmp.w r6, #0x1f4                  
  0eee2:  blo #0xeee8                       
  0eee4:  add.w sb, sb, #1                  
  0eee8:  mov r4, sb                        
  0eeea:  ldr r0, [pc, #0x88]               -> RAM
  0eeec:  ldr r0, [r0]                      
  0eeee:  cmp r0, #0                        
  0eef0:  bge #0xeef6                       
  0eef2:  rsb.w r4, sb, #0                  
  0eef6:  ldrh r0, [r7]                     
  0eef8:  ldrh r1, [r5]                     
  0eefa:  subs r6, r0, r1                   
  0eefc:  ldrh r0, [r7]                     
  0eefe:  cmp r0, r6                        
  0ef00:  bhs #0xef04                       
  0ef02:  movs r6, #0                       
  0ef04:  cmp r4, #8                        
  0ef06:  bge #0xef0a                       
  0ef08:  movs r4, #8                       
  0ef0a:  mov r1, r6                        
  0ef0c:  mov r0, r4                        
  0ef0e:  bl #0x170e0                       -> func_0x170e0
  0ef12:  mov r4, r0                        
  0ef14:  b #0xef18                         -> 0x0ef18 (вне списка функций)
  0ef16:  movs r4, #0                       
  0ef18:  ldr r0, [pc, #0x58]               -> RAM
  0ef1a:  ldr r0, [r0]                      
  0ef1c:  cmp r0, r4                        
  0ef1e:  ble #0xef68                       
  0ef20:  ldr r0, [pc, #0x50]               -> RAM
  0ef22:  ldr r0, [r0]                      
  0ef24:  cmp r0, #0                        
  0ef26:  blt #0xef3e                       
  0ef28:  ldr r0, [pc, #0x48]               -> RAM
  0ef2a:  ldr r0, [r0]                      
  0ef2c:  mvn r1, #0x80000000               
  0ef30:  subs r0, r0, r1                   
  0ef32:  cmp r0, r4                        
  0ef34:  ble #0xef3e                       
  0ef36:  mov r0, r1                        
  0ef38:  str.w r0, [r8]                    
  0ef3c:  b #0xef6e                         -> 0x0ef6e (вне списка функций)
  0ef3e:  ldr r0, [pc, #0x34]               -> RAM
  0ef40:  ldr r0, [r0]                      
  0ef42:  cmp r0, #0                        
  0ef44:  bge #0xef5c                       
  0ef46:  ldr r0, [pc, #0x2c]               -> RAM
  0ef48:  ldr r0, [r0]                      
  0ef4a:  add.w r0, r0, #-0x80000000        
  0ef4e:  cmp r0, r4                        
  0ef50:  bge #0xef5c                       
  0ef52:  mov.w r0, #-0x80000000            
  0ef56:  str.w r0, [r8]                    
  0ef5a:  b #0xef6e                         -> 0x0ef6e (вне списка функций)
  0ef5c:  ldr r0, [pc, #0x14]               -> RAM
  0ef5e:  ldr r0, [r0]                      
  0ef60:  subs r0, r0, r4                   
  0ef62:  str.w r0, [r8]                    
  0ef66:  b #0xef6e                         -> 0x0ef6e (вне списка функций)
  0ef68:  movs r0, #0                       
  0ef6a:  str.w r0, [r8]                    
  0ef6e:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
  ; --- literal-пул @0x0ef74 (1 слов) — ВНЕ границ функции ---
  0ef74:  .word 0x20002ffa  ; RAM
```
