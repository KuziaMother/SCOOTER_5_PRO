# func_0x0f038

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f038) | `0x0000f038` |
| размер кода | 262 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000059 — RAM (r1)
- 0x2000005a — RAM (r1)
- 0x20001359 — RAM (r1)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x0ab0c` (0x0000ab0c, bl)
- 0x0f05e (b, вне списка функций)
- 0x0f062 (b, вне списка функций)
- 0x0f0a2 (b, вне списка функций)
- 0x0f0be (b, вне списка функций)
- 0x0f100 (b, вне списка функций)
- 0x0f112 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11894` (bl @0x000118c2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0f05a..0x0f05e` (4 Б); цели из: 0x0f056
- `0x0f05e..0x0f062` (4 Б); цели из: 0x0f04a
- `0x0f062..0x0f09a` (56 Б); цели из: 0x0f058
- `0x0f09a..0x0f0a2` (8 Б); цели из: 0x0f08e
- `0x0f0a2..0x0f0b6` (20 Б); цели из: 0x0f098
- `0x0f0b6..0x0f0be` (8 Б); цели из: 0x0f0aa
- `0x0f0be..0x0f0e6` (40 Б); цели из: 0x0f0b4
- `0x0f0e6..0x0f0f4` (14 Б); цели из: 0x0f0da
- `0x0f0f4..0x0f100` (12 Б); цели из: 0x0f0e4
- `0x0f100..0x0f116` (22 Б); цели из: 0x0f0f2
- `0x0f116..0x0f13e` (40 Б); цели из: 0x0f066, 0x0f076

## Дизассембляция

```asm
  0f038:  push {r4, r5, lr}                 
  0f03a:  sub sp, #0x34                     
  0f03c:  movs r5, #0                       
  0f03e:  movs r1, #0x30                    
  0f040:  add r0, sp, #4                    
  0f042:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0f046:  movs r4, #0                       
  0f048:  nop                               
  0f04a:  b #0xf05e                         -> 0x0f05e (вне списка функций)
  0f04c:  add r0, sp, #4                    
  0f04e:  bl #0xab0c                        -> func_0x0ab0c
  0f052:  mov r4, r0                        
  0f054:  cmp r4, #1                        
  0f056:  bne #0xf05a                       
  0f058:  b #0xf062                         -> 0x0f062 (вне списка функций)
  0f05a:  adds r0, r5, #1                   
  0f05c:  uxtb r5, r0                       
  0f05e:  cmp r5, #3                        
  0f060:  blt #0xf04c                       
  0f062:  nop                               
  0f064:  cmp r4, #1                        
  0f066:  bne #0xf116                       
  0f068:  movs r1, #0x16                    
  0f06a:  add r0, sp, #4                    
  0f06c:  bl #0x8a50                        -> func_0x08a50
  0f070:  ldrh.w r1, [sp, #0x1a]            
  0f074:  cmp r0, r1                        
  0f076:  bne #0xf116                       
  0f078:  ldr r1, [pc, #0xc4]               -> RAM
  0f07a:  ldr r0, [sp, #4]                  
  0f07c:  str r0, [r1, #8]                  
  0f07e:  ldr r0, [sp, #8]                  
  0f080:  str r0, [r1, #0xc]                
  0f082:  movs r0, #0                       
  0f084:  strb r0, [r1, #7]                 
  0f086:  movw r1, #0xea60                  
  0f08a:  ldr r0, [sp, #0xc]                
  0f08c:  cmp r0, r1                        
  0f08e:  blo #0xf09a                       
  0f090:  movs r0, #0                       
  0f092:  ldr r1, [pc, #0xac]               -> RAM
  0f094:  str.w r0, [r1, #0x11]             
  0f098:  b #0xf0a2                         -> 0x0f0a2 (вне списка функций)
  0f09a:  ldr r1, [pc, #0xa4]               -> RAM
  0f09c:  ldr r0, [sp, #0xc]                
  0f09e:  str.w r0, [r1, #0x11]             
  0f0a2:  movw r1, #0xea60                  
  0f0a6:  ldr r0, [sp, #0xc]                
  0f0a8:  cmp r0, r1                        
  0f0aa:  blo #0xf0b6                       
  0f0ac:  movs r0, #0                       
  0f0ae:  ldr r1, [pc, #0x90]               -> RAM
  0f0b0:  str.w r0, [r1, #0x11]             
  0f0b4:  b #0xf0be                         -> 0x0f0be (вне списка функций)
  0f0b6:  ldr r1, [pc, #0x88]               -> RAM
  0f0b8:  ldr r0, [sp, #0xc]                
  0f0ba:  str.w r0, [r1, #0x11]             
  0f0be:  ldr r1, [pc, #0x80]               -> RAM
  0f0c0:  ldr r0, [sp, #0x10]               
  0f0c2:  str.w r0, [r1, #0x27]             
  0f0c6:  ldrh.w r0, [sp, #0x14]            
  0f0ca:  strh.w r0, [r1, #0x15]            
  0f0ce:  movs r0, #0                       
  0f0d0:  strb r0, [r1, #0x10]              
  0f0d2:  ldrh.w r0, [sp, #0x16]            
  0f0d6:  cmp.w r0, #0x3e8                  
  0f0da:  bgt #0xf0e6                       
  0f0dc:  ldrh.w r0, [sp, #0x16]            
  0f0e0:  cmp.w r0, #0x12c                  
  0f0e4:  bge #0xf0f4                       
  0f0e6:  mov.w r0, #0x3e8                  
  0f0ea:  ldr r1, [pc, #0x54]               -> RAM
  0f0ec:  strh r0, [r1, #0x18]              
  0f0ee:  movs r0, #1                       
  0f0f0:  strb r0, [r1, #0x17]              
  0f0f2:  b #0xf100                         -> 0x0f100 (вне списка функций)
  0f0f4:  ldrh.w r0, [sp, #0x16]            
  0f0f8:  ldr r1, [pc, #0x44]               -> RAM
  0f0fa:  strh r0, [r1, #0x18]              
  0f0fc:  movs r0, #0                       
  0f0fe:  strb r0, [r1, #0x17]              
  0f100:  ldrh.w r0, [sp, #0x18]            
  0f104:  ldr r1, [pc, #0x38]               -> RAM
  0f106:  strb r0, [r1, #0x1a]              
  0f108:  movs r0, #1                       
  0f10a:  ldr r1, [pc, #0x38]               -> RAM
  0f10c:  strb r0, [r1]                     
  0f10e:  ldr r1, [pc, #0x38]               -> RAM
  0f110:  strb r0, [r1]                     
  0f112:  add sp, #0x34                     
  0f114:  pop {r4, r5, pc}                  
  0f116:  movs r0, #0                       
  0f118:  ldr r1, [pc, #0x24]               -> RAM
  0f11a:  str r0, [r1, #8]                  
  0f11c:  str r0, [r1, #0xc]                
  0f11e:  movs r0, #1                       
  0f120:  strb r0, [r1, #7]                 
  0f122:  movs r0, #0                       
  0f124:  str.w r0, [r1, #0x11]             
  0f128:  strh.w r0, [r1, #0x15]            
  0f12c:  movs r0, #1                       
  0f12e:  strb r0, [r1, #0x10]              
  0f130:  movs r0, #0                       
  0f132:  strh r0, [r1, #0x18]              
  0f134:  strb r0, [r1, #0x1a]              
  0f136:  movs r0, #1                       
  0f138:  strb r0, [r1, #0x17]              
  0f13a:  movs r0, #0                       
  0f13c:  b #0xf112                         -> 0x0f112 (вне списка функций)
  ; --- literal-пул @0x0f140 (3 слов) — ВНЕ границ функции ---
  0f140:  .word 0x20001359  ; RAM
  0f144:  .word 0x20000059  ; RAM
  0f148:  .word 0x2000005a  ; RAM
```
