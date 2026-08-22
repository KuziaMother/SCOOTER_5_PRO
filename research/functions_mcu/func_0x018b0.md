# func_0x018b0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800018b0) | `0x000018b0` |
| размер кода | 66 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0xfff0feff — прочее (r4)
- 0xfff1f7fd — прочее (r4)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x018fc` (bl @0x0000191e)


## Дизассембляция

```asm
  018b0:  push {r4, r5, lr}                 
  018b2:  mov r2, r0                        
  018b4:  movs r0, #0                       
  018b6:  movs r3, #0                       
  018b8:  ldr r0, [r2, #4]                  
  018ba:  ldr r4, [pc, #0x38]               
  018bc:  ands r0, r4                       
  018be:  ldrb r4, [r1]                     
  018c0:  orr.w r0, r0, r4, lsl #8          
  018c4:  str r0, [r2, #4]                  
  018c6:  ldr r0, [r2, #8]                  
  018c8:  ldr r4, [pc, #0x2c]               
  018ca:  ands r0, r4                       
  018cc:  ldrd r5, r4, [r1, #4]             
  018d0:  orrs r4, r5                       
  018d2:  ldrb r5, [r1, #1]                 
  018d4:  orr.w r4, r4, r5, lsl #1          
  018d8:  orrs r0, r4                       
  018da:  str r0, [r2, #8]                  
  018dc:  ldr r0, [r2, #0x2c]               
  018de:  bic r0, r0, #0xf00000             
  018e2:  ldrb r4, [r1, #0xc]               
  018e4:  subs r4, r4, #1                   
  018e6:  uxtb r4, r4                       
  018e8:  orrs r3, r4                       
  018ea:  orr.w r0, r0, r3, lsl #20         
  018ee:  str r0, [r2, #0x2c]               
  018f0:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x018f4 (2 слов) — ВНЕ границ функции ---
  018f4:  .word 0xfff0feff
  018f8:  .word 0xfff1f7fd
```
