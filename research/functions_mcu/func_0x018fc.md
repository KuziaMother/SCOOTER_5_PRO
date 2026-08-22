# func_0x018fc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800018fc) | `0x000018fc` |
| размер кода | 60 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a8d0 — flash-mirror @0x1a8d0 (r0)
- 0x40020800 — периферия (r0)

## Вызовы (callees)

- `func_0x015aa` (0x000015aa, bl)
- `func_0x018b0` (0x000018b0, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0175c` (bl @0x00001772)


## Дизассембляция

```asm
  018fc:  push {r0, r1, r2, r3, r4, lr}     
  018fe:  mov r4, r0                        
  01900:  movs r0, #1                       
  01902:  strb.w r0, [sp]                   
  01906:  strb.w r0, [sp, #1]               
  0190a:  mov.w r0, #0xe0000                
  0190e:  str r0, [sp, #4]                  
  01910:  movs r0, #0                       
  01912:  str r0, [sp, #8]                  
  01914:  movs r0, #2                       
  01916:  strb.w r0, [sp, #0xc]             
  0191a:  mov r1, sp                        
  0191c:  ldr r0, [pc, #0x18]               -> периферия
  0191e:  bl #0x18b0                        -> func_0x018b0
  01922:  adds r0, r4, #1                   
  01924:  uxtb r2, r0                       
  01926:  ldr r0, [pc, #0x14]               -> flash-mirror @0x1a8d0
  01928:  add.w r0, r0, r4, lsl #3          
  0192c:  ldrb r1, [r0, #6]                 
  0192e:  movs r3, #7                       
  01930:  ldr r0, [pc, #4]                  -> периферия
  01932:  bl #0x15aa                        -> func_0x015aa
  01936:  pop {r0, r1, r2, r3, r4, pc}      
  ; --- literal-пул @0x01938 (2 слов) — ВНЕ границ функции ---
  01938:  .word 0x40020800  ; периферия
  0193c:  .word 0x0801a8d0  ; flash-mirror @0x1a8d0
```
