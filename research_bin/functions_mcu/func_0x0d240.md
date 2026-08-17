# func_0x0d240

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d240) | `0x0000d240` |
| размер кода | 82 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000c9c — RAM (r0)

## Вызовы (callees)

- `func_0x08380` (0x00008380, bl)
- `func_0x08a50` (0x00008a50, bl)
- 0x0d28e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0c420` (bl @0x0000c424)
- `func_0x0c420` (bl @0x0000c43c)


## Дизассембляция

```asm
  0d240:  push {r3, r4, r5, lr}             
  0d242:  movs r4, #0                       
  0d244:  movs r5, #0                       
  0d246:  movs r2, #8                       
  0d248:  mov.w r1, #0x30000                
  0d24c:  ldr r0, [pc, #0x44]               -> RAM
  0d24e:  bl #0x8380                        -> func_0x08380
  0d252:  mov r4, r0                        
  0d254:  cbnz r4, #0xd274                  
  0d256:  movs r0, #0x64                    
  0d258:  str r0, [sp]                      
  0d25a:  nop                               
  0d25c:  ldr r0, [sp]                      
  0d25e:  subs r1, r0, #1                   
  0d260:  str r1, [sp]                      
  0d262:  cmp r0, #0                        
  0d264:  bne #0xd25c                       
  0d266:  movs r2, #8                       
  0d268:  mov.w r1, #0x30000                
  0d26c:  ldr r0, [pc, #0x24]               -> RAM
  0d26e:  bl #0x8380                        -> func_0x08380
  0d272:  mov r4, r0                        
  0d274:  cmp r4, #1                        
  0d276:  bne #0xd28e                       
  0d278:  movs r1, #4                       
  0d27a:  ldr r0, [pc, #0x18]               -> RAM
  0d27c:  bl #0x8a50                        -> func_0x08a50
  0d280:  mov r5, r0                        
  0d282:  ldr r0, [pc, #0x10]               -> RAM
  0d284:  ldr r0, [r0, #4]                  
  0d286:  cmp r0, r5                        
  0d288:  bne #0xd28c                       
  0d28a:  b #0xd28e                         -> 0x0d28e (вне списка функций)
  0d28c:  movs r4, #0                       
  0d28e:  mov r0, r4                        
  0d290:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x0d294 (1 слов) — ВНЕ границ функции ---
  0d294:  .word 0x20000c9c  ; RAM
```
