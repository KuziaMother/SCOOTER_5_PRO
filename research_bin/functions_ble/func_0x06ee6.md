# func_0x06ee6

| | |
|---|---|
| offset в файле | `0x06ee6` |
| vaddr (база 0x01800000) | `0x01806ee6` |
 | размер кода | 66 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00206840 — RAM (r4)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x06f28` (bl @0x01806f92)

## Дизассембляция

```asm
  01806ee6:  push {r4, r5, lr}                 
  01806ee8:  movs r2, #1                       
  01806eea:  ldr r4, [pc, #0x120]              (RAM)
  01806eec:  lsls r2, r0                       
  01806eee:  subs r4, #8                       
  01806ef0:  ldr r1, [r4, #0x10]               
  01806ef2:  tst r2, r1                        
  01806ef4:  bne #0x1806f26                    
  01806ef6:  add.w r1, r4, #0x24               
  01806efa:  ldrb r3, [r1, #7]                 
  01806efc:  ldrb r5, [r1, #4]                 
  01806efe:  cmp r3, r5                        
  01806f00:  beq #0x1806f20                    
  01806f02:  ldrb r5, [r1, #6]                 
  01806f04:  ldr r3, [r1]                      
  01806f06:  str.w r0, [r3, r5, lsl #2]        
  01806f0a:  ldrb r0, [r1, #6]                 
  01806f0c:  ldrb r3, [r1, #4]                 
  01806f0e:  adds r0, r0, #1                   
  01806f10:  udiv r5, r0, r3                   
  01806f14:  mls r0, r3, r5, r0                
  01806f18:  strb r0, [r1, #6]                 
  01806f1a:  ldrb r0, [r1, #7]                 
  01806f1c:  adds r0, r0, #1                   
  01806f1e:  strb r0, [r1, #7]                 
  01806f20:  ldr r0, [r4, #0x10]               
  01806f22:  orrs r2, r0                       
  01806f24:  str r2, [r4, #0x10]               
  01806f26:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x0700c (1 слов) — ВНЕ границ функции ---
  0700c:  .word 0x00206840  ; RAM
```
