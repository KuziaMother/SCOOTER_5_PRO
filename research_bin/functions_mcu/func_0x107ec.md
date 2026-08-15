# func_0x107ec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800107ec) | `0x000107ec` |
| размер кода | 126 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40010800 — периферия (r0)

## Вызовы (callees)

- `func_0x085c8` (0x000085c8, bl)
- `func_0x087b0` (0x000087b0, bl)
- `func_0x0c6a4` (0x0000c6a4, bl)

## Кто вызывает (callers / xrefs)

- `func_0x10788` (bl @0x0001078c)


## Дизассембляция

```asm
  107ec:  push {r0, r1, r2, r3, r4, lr}     
  107ee:  mov r0, sp                        
  107f0:  bl #0x87b0                        -> func_0x087b0
  107f4:  movs r1, #1                       
  107f6:  movs r0, #4                       
  107f8:  bl #0xc6a4                        -> func_0x0c6a4
  107fc:  movs r1, #1                       
  107fe:  movw r0, #0x1001                  
  10802:  bl #0xc6a4                        -> func_0x0c6a4
  10806:  movs r0, #0x20                    
  10808:  strh.w r0, [sp]                   
  1080c:  movs r0, #0                       
  1080e:  strb.w r0, [sp, #3]               
  10812:  movs r0, #2                       
  10814:  str r0, [sp, #8]                  
  10816:  movs r0, #0                       
  10818:  str r0, [sp, #0xc]                
  1081a:  mov r1, sp                        
  1081c:  ldr r0, [pc, #0x4c]               -> периферия
  1081e:  bl #0x85c8                        -> func_0x085c8
  10822:  movs r0, #0x80                    
  10824:  strh.w r0, [sp]                   
  10828:  movs r0, #0                       
  1082a:  strb.w r0, [sp, #3]               
  1082e:  movs r0, #2                       
  10830:  str r0, [sp, #8]                  
  10832:  mov r1, sp                        
  10834:  ldr r0, [pc, #0x34]               -> периферия
  10836:  bl #0x85c8                        -> func_0x085c8
  1083a:  movs r0, #0x40                    
  1083c:  strh.w r0, [sp]                   
  10840:  movs r0, #0                       
  10842:  strb.w r0, [sp, #3]               
  10846:  str r0, [sp, #8]                  
  10848:  mov r1, sp                        
  1084a:  ldr r0, [pc, #0x20]               -> периферия
  1084c:  bl #0x85c8                        -> func_0x085c8
  10850:  movs r0, #0x10                    
  10852:  strh.w r0, [sp]                   
  10856:  movs r0, #0                       
  10858:  strb.w r0, [sp, #3]               
  1085c:  movs r0, #1                       
  1085e:  str r0, [sp, #8]                  
  10860:  mov r1, sp                        
  10862:  ldr r0, [pc, #8]                  -> периферия
  10864:  bl #0x85c8                        -> func_0x085c8
  10868:  pop {r0, r1, r2, r3, r4, pc}      
  ; --- literal-пул @0x1086c (1 слов) — ВНЕ границ функции ---
  1086c:  .word 0x40010800  ; периферия
```
