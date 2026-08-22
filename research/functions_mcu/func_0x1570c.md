# func_0x1570c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001570c) | `0x0001570c` |
| размер кода | 72 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x2000304c — RAM (r0)

## Вызовы (callees)

- `func_0x082f0` (0x000082f0, bl)
- `func_0x084a0` (0x000084a0, bl)
- `func_0x08a50` (0x00008a50, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0eddc` (bl @0x0000ee38)
- `func_0x157e0` (bl @0x000158e2)


## Дизассембляция

```asm
  1570c:  push {r3, r4, r5, lr}             
  1570e:  movs r4, #0                       
  15710:  mov.w r0, #0x20000                
  15714:  bl #0x82f0                        -> func_0x082f0
  15718:  movs r1, #0xc                     
  1571a:  ldr r0, [pc, #0x38]               -> RAM
  1571c:  bl #0x8a50                        -> func_0x08a50
  15720:  ldr r1, [pc, #0x30]               -> RAM
  15722:  str r0, [r1, #0xc]                
  15724:  movs r2, #0x10                    
  15726:  lsls r1, r2, #0xd                 
  15728:  ldr r0, [pc, #0x28]               -> RAM
  1572a:  bl #0x84a0                        -> func_0x084a0
  1572e:  mov r4, r0                        
  15730:  cbnz r4, #0x15750                 
  15732:  mov.w r0, #0x3e8                  
  15736:  str r0, [sp]                      
  15738:  nop                               
  1573a:  ldr r0, [sp]                      
  1573c:  subs r1, r0, #1                   
  1573e:  str r1, [sp]                      
  15740:  cmp r0, #0                        
  15742:  bne #0x1573a                      
  15744:  movs r2, #0x10                    
  15746:  lsls r1, r2, #0xd                 
  15748:  ldr r0, [pc, #8]                  -> RAM
  1574a:  bl #0x84a0                        -> func_0x084a0
  1574e:  mov r4, r0                        
  15750:  mov r0, r4                        
  15752:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x15754 (1 слов) — ВНЕ границ функции ---
  15754:  .word 0x2000304c  ; RAM
```
