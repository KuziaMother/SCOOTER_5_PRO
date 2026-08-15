# func_0x0f1ec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000f1ec) | `0x0000f1ec` |
| размер кода | 78 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019d8e — flash-mirror @0x19d8e (r1)
- 0x20000a22 — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x20000f95 — RAM (r0)

## Вызовы (callees)

- 0x0f278 (b, вне списка функций)
- `func_0x156ac` (0x000156ac, bl)

## Кто вызывает (callers / xrefs)

- `func_0x11978` (bl @0x0001197a)


## Дизассембляция

```asm
  0f1ec:  push {r4, lr}                     
  0f1ee:  ldr r0, [pc, #0x8c]               -> RAM
  0f1f0:  ldrb r0, [r0, #2]                 
  0f1f2:  ubfx r0, r0, #1, #1               
  0f1f6:  cbnz r0, #0xf23a                  
  0f1f8:  ldr r0, [pc, #0x84]               -> RAM
  0f1fa:  ldrh r0, [r0, #6]                 
  0f1fc:  ldr r1, [pc, #0x84]               -> flash-mirror @0x19d8e
  0f1fe:  ldrh r1, [r1, #0xa]               
  0f200:  cmp r0, r1                        
  0f202:  bgt #0xf232                       
  0f204:  ldr r0, [pc, #0x80]               -> RAM
  0f206:  ldrh r0, [r0]                     
  0f208:  adds r0, r0, #1                   
  0f20a:  ldr r1, [pc, #0x7c]               -> RAM
  0f20c:  strh r0, [r1]                     
  0f20e:  ldr r0, [pc, #0x74]               -> flash-mirror @0x19d8e
  0f210:  ldrh r0, [r0, #0xe]               
  0f212:  ldrh r1, [r1]                     
  0f214:  cmp r0, r1                        
  0f216:  bgt #0xf278                       
  0f218:  ldr r0, [pc, #0x60]               -> RAM
  0f21a:  ldrb r0, [r0, #2]                 
  0f21c:  bic r0, r0, #2                    
  0f220:  adds r0, r0, #2                   
  0f222:  ldr r1, [pc, #0x58]               -> RAM
  0f224:  strb r0, [r1, #2]                 
  0f226:  movs r0, #0                       
  0f228:  ldr r1, [pc, #0x5c]               -> RAM
  0f22a:  strh r0, [r1]                     
  0f22c:  bl #0x156ac                       -> func_0x156ac
  0f230:  b #0xf278                         -> 0x0f278 (вне списка функций)
  0f232:  movs r0, #0                       
  0f234:  ldr r1, [pc, #0x50]               -> RAM
  0f236:  strh r0, [r1]                     
  0f238:  b #0xf278                         -> 0x0f278 (вне списка функций)
  ; --- literal-пул @0x0f27c (4 слов) — ВНЕ границ функции ---
  0f27c:  .word 0x20000f70  ; RAM
  0f280:  .word 0x20000f95  ; RAM
  0f284:  .word 0x08019d8e  ; flash-mirror @0x19d8e
  0f288:  .word 0x20000a22  ; RAM
```
