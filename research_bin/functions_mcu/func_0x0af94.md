# func_0x0af94

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000af94) | `0x0000af94` |
| размер кода | 250 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f00 — RAM (r0)
- 0x200030f6 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x097e2` (0x000097e2, bl)
- 0x0ae98 (bl, вне списка функций)
- 0x0aecc (bl, вне списка функций)
- 0x0afe2 (b, вне списка функций)
- 0x0b08a (b, вне списка функций)
- 0x0b098 (bl, вне списка функций)
- 0x0b0f8 (bl, вне списка функций)
- 0x0b300 (bl, вне списка функций)
- `func_0x0bc5c` (0x0000bc5c, bl)
- `func_0x0c464` (0x0000c464, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01fe0` (bl @0x00002000)
- `func_0x020d8` (bl @0x000020fa)
- `func_0x03034` (bl @0x00003048)
- `func_0x05cd0` (bl @0x00005d86)
- `func_0x0b302` (bl @0x0000b464)
- `func_0x0b384` (bl @0x0000b464)
- `func_0x0c20c` (bl @0x0000c224)
- `func_0x0c20c` (bl @0x0000c258)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0afcc..0x0afe2` (22 Б); цели из: 0x0afb4
- `0x0afe2..0x0b038` (86 Б); цели из: 0x0afca
- `0x0b038..0x0b084` (76 Б); цели из: 0x0b00e
- `0x0b084..0x0b08a` (6 Б); цели из: 0x0b06c, 0x0b07a
- `0x0b08a..0x0b08e` (4 Б); цели из: 0x0b082

## Дизассембляция

```asm
  0af94:  push {r4, r5, lr}                 
  0af96:  sub sp, #0x24                     
  0af98:  mov r4, r0                        
  0af9a:  movs r5, #0                       
  0af9c:  movs r2, #0x24                    
  0af9e:  add.w r1, r4, #0x10               
  0afa2:  mov r0, sp                        
  0afa4:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0afa8:  ldm.w r4, {r0, r1, r2, r3}        
  0afac:  bl #0xae98                        -> 0x0ae98 (вне списка функций)
  0afb0:  ldrb r0, [r4, #0x13]              
  0afb2:  cmp r0, #2                        
  0afb4:  beq #0xafcc                       
  0afb6:  movs r2, #0x24                    
  0afb8:  add.w r1, r4, #0x10               
  0afbc:  mov r0, sp                        
  0afbe:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0afc2:  ldm.w r4, {r0, r1, r2, r3}        
  0afc6:  bl #0xb300                        -> 0x0b300 (вне списка функций)
  0afca:  b #0xafe2                         -> 0x0afe2 (вне списка функций)
  0afcc:  movw r1, #0x848                   
  0afd0:  ldr r0, [pc, #0xbc]               -> RAM
  0afd2:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0afd6:  movs r3, #0x14                    
  0afd8:  movs r2, #0x6a                    
  0afda:  ldr r1, [pc, #0xb4]               -> RAM
  0afdc:  ldr r0, [pc, #0xb4]               -> RAM
  0afde:  bl #0xc464                        -> func_0x0c464
  0afe2:  movs r2, #0x24                    
  0afe4:  add.w r1, r4, #0x10               
  0afe8:  mov r0, sp                        
  0afea:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0afee:  ldm.w r4, {r0, r1, r2, r3}        
  0aff2:  bl #0xae98                        -> 0x0ae98 (вне списка функций)
  0aff6:  movs r2, #0x24                    
  0aff8:  add.w r1, r4, #0x10               
  0affc:  mov r0, sp                        
  0affe:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0b002:  ldm.w r4, {r0, r1, r2, r3}        
  0b006:  bl #0xb0f8                        -> 0x0b0f8 (вне списка функций)
  0b00a:  ldrb r0, [r4, #0x13]              
  0b00c:  cmp r0, #1                        
  0b00e:  beq #0xb038                       
  0b010:  ldrsb.w r0, [r4, #0x18]           
  0b014:  movs r3, #1                       
  0b016:  ldrd r1, r2, [r4, #0x1c]          
  0b01a:  bl #0xbc5c                        -> func_0x0bc5c
  0b01e:  ldrsb.w r0, [r4, #0x24]           
  0b022:  movs r3, #1                       
  0b024:  ldrd r1, r2, [r4, #0x28]          
  0b028:  bl #0xbc5c                        -> func_0x0bc5c
  0b02c:  movs r2, #1                       
  0b02e:  mov.w r1, #0x700                  
  0b032:  ldr r0, [r4]                      
  0b034:  bl #0x97e2                        -> func_0x097e2
  0b038:  movs r2, #0x24                    
  0b03a:  add.w r1, r4, #0x10               
  0b03e:  mov r0, sp                        
  0b040:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0b044:  ldm.w r4, {r0, r1, r2, r3}        
  0b048:  bl #0xaecc                        -> 0x0aecc (вне списка функций)
  0b04c:  movs r2, #0x24                    
  0b04e:  add.w r1, r4, #0x10               
  0b052:  mov r0, sp                        
  0b054:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0b058:  ldm.w r4, {r0, r1, r2, r3}        
  0b05c:  bl #0xb098                        -> 0x0b098 (вне списка функций)
  0b060:  mov.w r5, #0x700                  
  0b064:  ldr r0, [r4]                      
  0b066:  ldrh r0, [r0, #4]                 
  0b068:  ands r0, r5                       
  0b06a:  cmp r0, r5                        
  0b06c:  bne #0xb084                       
  0b06e:  ldr r0, [r4]                      
  0b070:  ldrh r0, [r0]                     
  0b072:  movw r1, #0x401                   
  0b076:  ands r0, r1                       
  0b078:  cmp r0, r1                        
  0b07a:  bne #0xb084                       
  0b07c:  movs r0, #1                       
  0b07e:  strb.w r0, [r4, #0x10c]           
  0b082:  b #0xb08a                         -> 0x0b08a (вне списка функций)
  0b084:  movs r0, #0                       
  0b086:  strb.w r0, [r4, #0x10c]           
  0b08a:  add sp, #0x24                     
  0b08c:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x0b090 (2 слов) — ВНЕ границ функции ---
  0b090:  .word 0x200030f6  ; RAM
  0b094:  .word 0x20000f00  ; RAM
```
