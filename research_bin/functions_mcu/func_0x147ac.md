# func_0x147ac

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800147ac) | `0x000147ac` |
| размер кода | 78 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200030cf — RAM (r0)

## Вызовы (callees)

- `func_0x082f0` (0x000082f0, bl)
- `func_0x084a0` (0x000084a0, bl)
- `func_0x08a50` (0x00008a50, bl)

## Кто вызывает (callers / xrefs)

- `func_0x14802` (bl @0x00014916)


## Дизассембляция

```asm
  147ac:  push {r3, r4, r5, lr}             
  147ae:  movs r4, #0                       
  147b0:  mov.w r0, #0x40000                
  147b4:  bl #0x82f0                        -> func_0x082f0
  147b8:  movs r1, #0xa                     
  147ba:  ldr r0, [pc, #0x40]               -> RAM
  147bc:  bl #0x8a50                        -> func_0x08a50
  147c0:  ldr r1, [pc, #0x38]               -> RAM
  147c2:  str.w r0, [r1, #0xa]              
  147c6:  movs r2, #0xe                     
  147c8:  mov.w r1, #0x40000                
  147cc:  ldr r0, [pc, #0x2c]               -> RAM
  147ce:  bl #0x84a0                        -> func_0x084a0
  147d2:  mov r4, r0                        
  147d4:  cbnz r4, #0x147f6                 
  147d6:  mov.w r0, #0x3e8                  
  147da:  str r0, [sp]                      
  147dc:  nop                               
  147de:  ldr r0, [sp]                      
  147e0:  subs r1, r0, #1                   
  147e2:  str r1, [sp]                      
  147e4:  cmp r0, #0                        
  147e6:  bne #0x147de                      
  147e8:  movs r2, #0xe                     
  147ea:  mov.w r1, #0x40000                
  147ee:  ldr r0, [pc, #0xc]                -> RAM
  147f0:  bl #0x84a0                        -> func_0x084a0
  147f4:  mov r4, r0                        
  147f6:  mov r0, r4                        
  147f8:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x147fc (1 слов) — ВНЕ границ функции ---
  147fc:  .word 0x200030cf  ; RAM
```
