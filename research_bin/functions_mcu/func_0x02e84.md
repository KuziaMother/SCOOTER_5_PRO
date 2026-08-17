# func_0x02e84

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002e84) | `0x00002e84` |
| размер кода | 54 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b71 — RAM (r0)

## Вызовы (callees)

- `func_0x09874` (0x00009874, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  02e84:  push.w {r3, r4, r5, r6, r7, r8, sb, lr}
  02e88:  mov r4, r0                        
  02e8a:  mov r8, r1                        
  02e8c:  mov r5, r2                        
  02e8e:  mov r6, r3                        
  02e90:  ldr.w sb, [sp, #0x20]             
  02e94:  mov r7, r6                        
  02e96:  mov.w r1, #0x20000                
  02e9a:  mov r0, r4                        
  02e9c:  bl #0x9874                        -> func_0x09874
  02ea0:  cbz r0, #0x2eac                   
  02ea2:  ldr r0, [pc, #0x180]              -> RAM
  02ea4:  ldrb r0, [r0]                     
  02ea6:  adds r0, r0, #1                   
  02ea8:  ldr r1, [pc, #0x178]              -> RAM
  02eaa:  strb r0, [r1]                     
  02eac:  mov.w r0, #0x1000                 
  02eb0:  str r0, [sp]                      
  02eb2:  cbnz r4, #0x2eba                  
  02eb4:  movs r0, #1                       
  02eb6:  pop.w {r3, r4, r5, r6, r7, r8, sb, pc}
  ; --- literal-пул @0x03024 (1 слов) — ВНЕ границ функции ---
  03024:  .word 0x20000b71  ; RAM
```
