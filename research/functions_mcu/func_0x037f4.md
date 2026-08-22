# func_0x037f4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800037f4) | `0x000037f4` |
| размер кода | 64 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000304c — RAM (r1)

## Вызовы (callees)

- `func_0x084a0` (0x000084a0, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  037f4:  push {r3, r4, r5, lr}             
  037f6:  movs r4, #0                       
  037f8:  mov.w r0, #0x21000                
  037fc:  ldr r1, [pc, #0x34]               -> RAM
  037fe:  str r0, [r1, #4]                  
  03800:  str r0, [r1, #8]                  
  03802:  movs r0, #0                       
  03804:  str r0, [r1]                      
  03806:  movs r2, #0x10                    
  03808:  lsls r1, r2, #0xd                 
  0380a:  ldr r0, [pc, #0x28]               -> RAM
  0380c:  bl #0x84a0                        -> func_0x084a0
  03810:  mov r4, r0                        
  03812:  cbnz r4, #0x3832                  
  03814:  mov.w r0, #0x3e8                  
  03818:  str r0, [sp]                      
  0381a:  nop                               
  0381c:  ldr r0, [sp]                      
  0381e:  subs r1, r0, #1                   
  03820:  str r1, [sp]                      
  03822:  cmp r0, #0                        
  03824:  bne #0x381c                       
  03826:  movs r2, #0x10                    
  03828:  lsls r1, r2, #0xd                 
  0382a:  ldr r0, [pc, #8]                  -> RAM
  0382c:  bl #0x84a0                        -> func_0x084a0
  03830:  mov r4, r0                        
  03832:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x03834 (1 слов) — ВНЕ границ функции ---
  03834:  .word 0x2000304c  ; RAM
```
