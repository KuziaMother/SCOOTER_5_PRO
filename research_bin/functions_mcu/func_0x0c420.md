# func_0x0c420

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c420) | `0x0000c420` |
| размер кода | 60 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200000a6 — RAM (r1)
- 0x20000c9c — RAM (r0)

## Вызовы (callees)

- `func_0x08a50` (0x00008a50, bl)
- `func_0x0d240` (0x0000d240, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e0a)


## Дизассембляция

```asm
  0c420:  push {r3, r4, r5, lr}             
  0c422:  movs r4, #0                       
  0c424:  bl #0xd240                        -> func_0x0d240
  0c428:  cbnz r0, #0xc440                  
  0c42a:  mov.w r0, #0x3e8                  
  0c42e:  str r0, [sp]                      
  0c430:  nop                               
  0c432:  ldr r0, [sp]                      
  0c434:  subs r1, r0, #1                   
  0c436:  str r1, [sp]                      
  0c438:  cmp r0, #0                        
  0c43a:  bne #0xc432                       
  0c43c:  bl #0xd240                        -> func_0x0d240
  0c440:  movs r1, #4                       
  0c442:  ldr r0, [pc, #0x18]               -> RAM
  0c444:  bl #0x8a50                        -> func_0x08a50
  0c448:  mov r4, r0                        
  0c44a:  ldr r0, [pc, #0x10]               -> RAM
  0c44c:  ldr r0, [r0, #4]                  
  0c44e:  cmp r0, r4                        
  0c450:  bne #0xc45a                       
  0c452:  ldr r0, [pc, #8]                  -> RAM
  0c454:  ldrb r0, [r0]                     
  0c456:  ldr r1, [pc, #8]                  -> RAM
  0c458:  strb r0, [r1]                     
  0c45a:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x0c45c (2 слов) — ВНЕ границ функции ---
  0c45c:  .word 0x20000c9c  ; RAM
  0c460:  .word 0x200000a6  ; RAM
```
