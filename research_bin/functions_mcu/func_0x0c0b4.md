# func_0x0c0b4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c0b4) | `0x0000c0b4` |
| размер кода | 78 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xe000e400 — Cortex-M (NVIC/SCB/SysTick) (r4)
- 0xe000ed0c — Cortex-M (NVIC/SCB/SysTick) (r4)

## Вызовы (callees)

- 0x0c116 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0307c` (bl @0x000030a0)
- `func_0x0332c` (bl @0x000034d4)
- `func_0x058b0` (bl @0x000058f0)
- `func_0x0bc5c` (bl @0x0000bc7e)


## Дизассембляция

```asm
  0c0b4:  push {r4, r5, r6, lr}             
  0c0b6:  movs r1, #0                       
  0c0b8:  movs r3, #0                       
  0c0ba:  movs r2, #0xf                     
  0c0bc:  ldrb r4, [r0, #3]                 
  0c0be:  cbz r4, #0xc102                   
  0c0c0:  ldr r4, [pc, #0x54]               -> Cortex-M (NVIC/SCB/SysTick)
  0c0c2:  ldr r4, [r4]                      
  0c0c4:  and r4, r4, #0x700                
  0c0c8:  rsb.w r4, r4, #0x700              
  0c0cc:  lsrs r1, r4, #8                   
  0c0ce:  rsb.w r3, r1, #4                  
  0c0d2:  lsrs r2, r1                       
  0c0d4:  ldrb r4, [r0, #1]                 
  0c0d6:  lsl.w r1, r4, r3                  
  0c0da:  ldrb r4, [r0, #2]                 
  0c0dc:  ands r4, r2                       
  0c0de:  orrs r1, r4                       
  0c0e0:  lsls r1, r1, #4                   
  0c0e2:  ldr r4, [pc, #0x38]               -> Cortex-M (NVIC/SCB/SysTick)
  0c0e4:  ldrb r6, [r0]                     
  0c0e6:  strb r1, [r4, r6]                 
  0c0e8:  ldrb r4, [r0]                     
  0c0ea:  and r5, r4, #0x1f                 
  0c0ee:  movs r4, #1                       
  0c0f0:  lsls r4, r5                       
  0c0f2:  ldrb r5, [r0]                     
  0c0f4:  asrs r5, r5, #5                   
  0c0f6:  lsls r5, r5, #2                   
  0c0f8:  add.w r5, r5, #-0x1fff2000        
  0c0fc:  str.w r4, [r5, #0x100]            
  0c100:  b #0xc116                         -> 0x0c116 (вне списка функций)
  ; --- literal-пул @0x0c118 (2 слов) — ВНЕ границ функции ---
  0c118:  .word 0xe000ed0c  ; Cortex-M (NVIC/SCB/SysTick)
  0c11c:  .word 0xe000e400  ; Cortex-M (NVIC/SCB/SysTick)
```
