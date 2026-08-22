# func_0x0d33c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d33c) | `0x0000d33c` |
| размер кода | 84 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a67 — RAM (r0)
- 0x20000f70 — RAM (r1)
- 0x2000164b — RAM (r2)

## Вызовы (callees)

- `func_0x01c60` (0x00001c60, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0c098` (bl @0x0000c09e)


## Дизассембляция

```asm
  0d33c:  push {r4, lr}                     
  0d33e:  ldr r0, [pc, #0x50]               -> RAM
  0d340:  ldrb r0, [r0]                     
  0d342:  adds r0, r0, #1                   
  0d344:  ldr r1, [pc, #0x48]               -> RAM
  0d346:  strb r0, [r1]                     
  0d348:  mov r0, r1                        
  0d34a:  ldrb r0, [r0]                     
  0d34c:  cmp r0, #5                        
  0d34e:  ble #0xd38e                       
  0d350:  movs r3, #1                       
  0d352:  ldr r2, [pc, #0x40]               -> RAM
  0d354:  movs r1, #0x7f                    
  0d356:  movs r0, #8                       
  0d358:  bl #0x1c60                        -> func_0x01c60
  0d35c:  cbz r0, #0xd388                   
  0d35e:  ldr r0, [pc, #0x34]               -> RAM
  0d360:  subs r0, #0x54                    
  0d362:  ldrb.w r0, [r0, #0x54]            
  0d366:  ldr r1, [pc, #0x30]               -> RAM
  0d368:  ldrb r1, [r1, #1]                 
  0d36a:  bfi r1, r0, #1, #1                
  0d36e:  ldr r0, [pc, #0x28]               -> RAM
  0d370:  strb r1, [r0, #1]                 
  0d372:  ldr r0, [pc, #0x20]               -> RAM
  0d374:  subs r0, #0x54                    
  0d376:  ldrb.w r0, [r0, #0x54]            
  0d37a:  lsrs r1, r0, #2                   
  0d37c:  ldr r0, [pc, #0x18]               -> RAM
  0d37e:  ldrb r0, [r0, #1]                 
  0d380:  bfi r0, r1, #0, #1                
  0d384:  ldr r1, [pc, #0x10]               -> RAM
  0d386:  strb r0, [r1, #1]                 
  0d388:  movs r0, #0                       
  0d38a:  ldr r1, [pc, #4]                  -> RAM
  0d38c:  strb r0, [r1]                     
  0d38e:  pop {r4, pc}                      
  ; --- literal-пул @0x0d390 (3 слов) — ВНЕ границ функции ---
  0d390:  .word 0x20000a67  ; RAM
  0d394:  .word 0x2000164b  ; RAM
  0d398:  .word 0x20000f70  ; RAM
```
