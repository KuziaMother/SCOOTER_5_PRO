# func_0x051d8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800051d8) | `0x000051d8` |
| размер кода | 106 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000044 — RAM (r2)
- 0x20000f10 — RAM (r2)
- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)
- 0x20000fc7 — RAM (r0)
- 0x20000fd3 — RAM (r1)
- 0x20000fe7 — RAM (r0)
- 0x20001004 — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- 0x0521e (b, вне списка функций)
- 0x05230 (b, вне списка функций)
- `func_0x09aa4` (0x00009aa4, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001df6)


## Дизассембляция

```asm
  051d8:  push {r4, lr}                     
  051da:  movs r1, #0x25                    
  051dc:  ldr r0, [pc, #0x64]               -> RAM
  051de:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  051e2:  movs r1, #0x26                    
  051e4:  ldr r0, [pc, #0x60]               -> RAM
  051e6:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  051ea:  ldr r0, [pc, #0x60]               -> RAM
  051ec:  movs r1, #0                       
  051ee:  str r1, [r0]                      
  051f0:  str r1, [r0, #4]                  
  051f2:  str r1, [r0, #8]                  
  051f4:  ldr r0, [pc, #0x58]               -> RAM
  051f6:  str r1, [r0]                      
  051f8:  str r1, [r0, #4]                  
  051fa:  str r1, [r0, #8]                  
  051fc:  movs r1, #0x54                    
  051fe:  ldr r0, [pc, #0x54]               -> RAM
  05200:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  05204:  movs r1, #0x1d                    
  05206:  ldr r0, [pc, #0x50]               -> RAM
  05208:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0520c:  movs r0, #0                       
  0520e:  b #0x521e                         -> 0x0521e (вне списка функций)
  05210:  mov.w r1, #0xe10                  
  05214:  ldr r2, [pc, #0x44]               -> RAM
  05216:  strh.w r1, [r2, r0, lsl #1]       
  0521a:  adds r1, r0, #1                   
  0521c:  uxtb r0, r1                       
  0521e:  cmp r0, #0xd                      
  05220:  blt #0x5210                       
  05222:  movs r0, #0                       
  05224:  b #0x5230                         -> 0x05230 (вне списка функций)
  05226:  movs r1, #0x19                    
  05228:  ldr r2, [pc, #0x34]               -> RAM
  0522a:  strb r1, [r2, r0]                 
  0522c:  adds r1, r0, #1                   
  0522e:  uxtb r0, r1                       
  05230:  cmp r0, #2                        
  05232:  blt #0x5226                       
  05234:  bl #0x9aa4                        -> func_0x09aa4
  05238:  movw r0, #0x2710                  
  0523c:  ldr r1, [pc, #0x24]               -> RAM
  0523e:  str r0, [r1, #4]                  
  05240:  pop {r4, pc}                      
  ; --- literal-пул @0x05244 (9 слов) — ВНЕ границ функции ---
  05244:  .word 0x20000f70  ; RAM
  05248:  .word 0x20000f95  ; RAM
  0524c:  .word 0x20000fbb  ; RAM
  05250:  .word 0x20000fc7  ; RAM
  05254:  .word 0x20001004  ; RAM
  05258:  .word 0x20000fe7  ; RAM
  0525c:  .word 0x20000f10  ; RAM
  05260:  .word 0x20000044  ; RAM
  05264:  .word 0x20000fd3  ; RAM
```
