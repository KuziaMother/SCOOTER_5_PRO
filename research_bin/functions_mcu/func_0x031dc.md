# func_0x031dc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800031dc) | `0x000031dc` |
| размер кода | 66 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0ca3c` (0x0000ca3c, bl)
- `func_0x0cd80` (0x0000cd80, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0ced0` (bl @0x0000ceda)


## Дизассембляция

```asm
  031dc:  push {r2, r3, r4, lr}             
  031de:  movs r0, #2                       
  031e0:  strb.w r0, [sp, #4]               
  031e4:  movs r0, #8                       
  031e6:  strb.w r0, [sp, #5]               
  031ea:  movs r0, #0x14                    
  031ec:  strb.w r0, [sp, #6]               
  031f0:  movs r0, #0x18                    
  031f2:  strb.w r0, [sp, #7]               
  031f6:  add r1, sp, #4                    
  031f8:  movs r0, #0                       
  031fa:  bl #0xcd80                        -> func_0x0cd80
  031fe:  movs r0, #0xd                     
  03200:  strb.w r0, [sp]                   
  03204:  movs r0, #1                       
  03206:  strb.w r0, [sp, #1]               
  0320a:  strb.w r0, [sp, #2]               
  0320e:  movs r0, #0x40                    
  03210:  strb.w r0, [sp, #3]               
  03214:  mov r1, sp                        
  03216:  movs r0, #0                       
  03218:  bl #0xca3c                        -> func_0x0ca3c
  0321c:  pop {r2, r3, r4, pc}              
```
