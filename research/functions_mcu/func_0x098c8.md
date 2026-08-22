# func_0x098c8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800098c8) | `0x000098c8` |
| размер кода | 222 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x000186a0 — данные @0x186a0 (r1)
- 0x000f4240 — прочее (r0)
- 0x007a1200 — прочее (r8)

## Вызовы (callees)

- 0x09958 (b, вне списка функций)
- 0x0997c (b, вне списка функций)
- `func_0x0c708` (0x0000c708, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0b09a` (bl @0x0000b0e6)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x09922..0x0992c` (10 Б); цели из: 0x0991e
- `0x0992c..0x09944` (24 Б); цели из: 0x09910
- `0x09944..0x09958` (20 Б); цели из: 0x09934
- `0x09958..0x0997c` (36 Б); цели из: 0x09942
- `0x0997c..0x099a6` (42 Б); цели из: 0x0992a

## Дизассембляция

```asm
  098c8:  push.w {r4, r5, r6, r7, r8, sb, lr}
  098cc:  sub sp, #0x1c                     
  098ce:  mov r4, r0                        
  098d0:  mov r5, r1                        
  098d2:  movs r6, #0                       
  098d4:  mov sb, r6                        
  098d6:  movs r7, #4                       
  098d8:  ldr.w r8, [pc, #0xcc]             
  098dc:  ldrh r6, [r4, #4]                 
  098de:  movw r0, #0xffc0                  
  098e2:  ands r6, r0                       
  098e4:  add r0, sp, #4                    
  098e6:  bl #0xc708                        -> func_0x0c708
  098ea:  ldr.w r8, [sp, #0xc]              
  098ee:  ldr r0, [pc, #0xbc]               
  098f0:  udiv r0, r8, r0                   
  098f4:  uxth.w sb, r0                     
  098f8:  orr.w r6, r6, sb                  
  098fc:  strh r6, [r4, #4]                 
  098fe:  ldrh r0, [r4]                     
  09900:  movw r1, #0xfffe                  
  09904:  ands r0, r1                       
  09906:  strh r0, [r4]                     
  09908:  movs r6, #0                       
  0990a:  ldr r1, [pc, #0xa4]               -> данные @0x186a0
  0990c:  ldr r0, [r5]                      
  0990e:  cmp r0, r1                        
  09910:  bhi #0x992c                       
  09912:  ldr r0, [r5]                      
  09914:  lsls r0, r0, #1                   
  09916:  udiv r0, r8, r0                   
  0991a:  uxth r7, r0                       
  0991c:  cmp r7, #4                        
  0991e:  bge #0x9922                       
  09920:  movs r7, #4                       
  09922:  orrs r6, r7                       
  09924:  add.w r0, sb, #1                  
  09928:  strh r0, [r4, #0x20]              
  0992a:  b #0x997c                         -> 0x0997c (вне списка функций)
  0992c:  ldrh r0, [r5, #6]                 
  0992e:  movw r1, #0xbfff                  
  09932:  cmp r0, r1                        
  09934:  bne #0x9944                       
  09936:  ldr r0, [r5]                      
  09938:  add.w r0, r0, r0, lsl #1          
  0993c:  udiv r0, r8, r0                   
  09940:  uxth r7, r0                       
  09942:  b #0x9958                         -> 0x09958 (вне списка функций)
  09944:  ldr r0, [r5]                      
  09946:  add.w r1, r0, r0, lsl #3          
  0994a:  add.w r0, r1, r0, lsl #4          
  0994e:  udiv r0, r8, r0                   
  09952:  uxth r7, r0                       
  09954:  orr r7, r7, #0x4000               
  09958:  ubfx r0, r7, #0, #0xc             
  0995c:  cbnz r0, #0x9962                  
  0995e:  orr r7, r7, #1                    
  09962:  orr r0, r7, #0x8000               
  09966:  orrs r6, r0                       
  09968:  mov.w r0, #0x12c                  
  0996c:  mul r0, sb, r0                    
  09970:  mov.w r1, #0x3e8                  
  09974:  sdiv r0, r0, r1                   
  09978:  adds r0, r0, #1                   
  0997a:  strh r0, [r4, #0x20]              
  0997c:  strh r6, [r4, #0x1c]              
  0997e:  ldrh r0, [r4]                     
  09980:  orr r0, r0, #1                    
  09984:  strh r0, [r4]                     
  09986:  ldrh r6, [r4]                     
  09988:  movw r0, #0xfbf5                  
  0998c:  ands r6, r0                       
  0998e:  ldrh r0, [r5, #4]                 
  09990:  ldrh r1, [r5, #0xa]               
  09992:  orrs r0, r1                       
  09994:  orrs r6, r0                       
  09996:  strh r6, [r4]                     
  09998:  ldrh r0, [r5, #0xc]               
  0999a:  ldrh r1, [r5, #8]                 
  0999c:  orrs r0, r1                       
  0999e:  strh r0, [r4, #8]                 
  099a0:  add sp, #0x1c                     
  099a2:  pop.w {r4, r5, r6, r7, r8, sb, pc}
  ; --- literal-пул @0x099a8 (3 слов) — ВНЕ границ функции ---
  099a8:  .word 0x007a1200
  099ac:  .word 0x000f4240
  099b0:  .word 0x000186a0  ; данные @0x186a0
```
