# func_0x0f14c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f14c) | `0x0000f14c` |
| размер кода | 156 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001384 — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x08a50` (0x00008a50, bl)
- `func_0x0ab0c` (0x0000ab0c, bl)
- 0x0accc (bl, вне списка функций)
- 0x0f16e (b, вне списка функций)
- 0x0f172 (b, вне списка функций)
- 0x0f1d8 (b, вне списка функций)
- 0x0f1e0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e6ec` (bl @0x0000e6f8)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0f16a..0x0f16e` (4 Б); цели из: 0x0f166
- `0x0f16e..0x0f172` (4 Б); цели из: 0x0f15c
- `0x0f172..0x0f1e0` (110 Б); цели из: 0x0f168
- `0x0f1e0..0x0f1e8` (8 Б); цели из: 0x0f1c0

## Дизассембляция

```asm
  0f14c:  push {r4, lr}                     
  0f14e:  sub sp, #0x50                     
  0f150:  movs r4, #0                       
  0f152:  movs r1, #0x30                    
  0f154:  add r0, sp, #0x20                 
  0f156:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0f15a:  nop                               
  0f15c:  b #0xf16e                         -> 0x0f16e (вне списка функций)
  0f15e:  add r0, sp, #0x20                 
  0f160:  bl #0xab0c                        -> func_0x0ab0c
  0f164:  cmp r0, #1                        
  0f166:  bne #0xf16a                       
  0f168:  b #0xf172                         -> 0x0f172 (вне списка функций)
  0f16a:  adds r0, r4, #1                   
  0f16c:  uxtb r4, r0                       
  0f16e:  cmp r4, #3                        
  0f170:  blt #0xf15e                       
  0f172:  nop                               
  0f174:  ldr r0, [pc, #0x70]               -> RAM
  0f176:  ldr.w r0, [r0, #0x2f]             
  0f17a:  str r0, [sp, #0x28]               
  0f17c:  ldr r0, [pc, #0x68]               -> RAM
  0f17e:  ldr.w r0, [r0, #0x17]             
  0f182:  str r0, [sp, #0x20]               
  0f184:  ldr r0, [pc, #0x60]               -> RAM
  0f186:  ldr.w r0, [r0, #0x1b]             
  0f18a:  str r0, [sp, #0x24]               
  0f18c:  ldr r0, [pc, #0x58]               -> RAM
  0f18e:  ldr.w r0, [r0, #0x46]             
  0f192:  str r0, [sp, #0x2c]               
  0f194:  ldr r0, [pc, #0x50]               -> RAM
  0f196:  ldrh.w r0, [r0, #0x2d]            
  0f19a:  strh.w r0, [sp, #0x30]            
  0f19e:  ldr r0, [pc, #0x48]               -> RAM
  0f1a0:  ldrh.w r0, [r0, #0x41]            
  0f1a4:  strh.w r0, [sp, #0x32]            
  0f1a8:  ldr r0, [pc, #0x3c]               -> RAM
  0f1aa:  ldrb.w r0, [r0, #0x43]            
  0f1ae:  strh.w r0, [sp, #0x34]            
  0f1b2:  movs r1, #0x16                    
  0f1b4:  add r0, sp, #0x20                 
  0f1b6:  bl #0x8a50                        -> func_0x08a50
  0f1ba:  strh.w r0, [sp, #0x36]            
  0f1be:  movs r4, #0                       
  0f1c0:  b #0xf1e0                         -> 0x0f1e0 (вне списка функций)
  0f1c2:  movs r2, #0x20                    
  0f1c4:  add r1, sp, #0x30                 
  0f1c6:  mov r0, sp                        
  0f1c8:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0f1cc:  add r0, sp, #0x20                 
  0f1ce:  ldm r0, {r0, r1, r2, r3}          
  0f1d0:  bl #0xaccc                        -> 0x0accc (вне списка функций)
  0f1d4:  cbz r0, #0xf1dc                   
  0f1d6:  movs r0, #1                       
  0f1d8:  add sp, #0x50                     
  0f1da:  pop {r4, pc}                      
  0f1dc:  adds r0, r4, #1                   
  0f1de:  uxtb r4, r0                       
  0f1e0:  cmp r4, #3                        
  0f1e2:  blt #0xf1c2                       
  0f1e4:  movs r0, #0                       
  0f1e6:  b #0xf1d8                         -> 0x0f1d8 (вне списка функций)
  ; --- literal-пул @0x0f1e8 (1 слов) — ВНЕ границ функции ---
  0f1e8:  .word 0x20001384  ; RAM
```
