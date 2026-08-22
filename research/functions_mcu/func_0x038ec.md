# func_0x038ec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800038ec) | `0x000038ec` |
| размер кода | 84 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x03c4c` (0x00003c4c, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  038ec:  push.w {r4, r5, r6, r7, r8, lr}   
  038f0:  mov r4, r0                        
  038f2:  mov r6, r1                        
  038f4:  mov r7, r2                        
  038f6:  mov.w r8, #0                      
  038fa:  mov r5, r4                        
  038fc:  ldrb r0, [r5]                     
  038fe:  strb r0, [r6]                     
  03900:  ldrb r0, [r5, #1]                 
  03902:  strb r0, [r6, #1]                 
  03904:  ldrb r0, [r5, #2]                 
  03906:  strb r0, [r6, #2]                 
  03908:  ldrb r0, [r5, #3]                 
  0390a:  strb r0, [r6, #3]                 
  0390c:  ldrb r2, [r5, #3]                 
  0390e:  adds r1, r5, #4                   
  03910:  adds r0, r6, #4                   
  03912:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  03916:  ldrb r0, [r5, #3]                 
  03918:  adds r0, r0, #4                   
  0391a:  uxtb r1, r0                       
  0391c:  mov r0, r6                        
  0391e:  bl #0x3c4c                        -> func_0x03c4c
  03922:  mov r8, r0                        
  03924:  asr.w r1, r8, #8                  
  03928:  ldrb r0, [r5, #3]                 
  0392a:  adds r0, r0, #4                   
  0392c:  strb r1, [r6, r0]                 
  0392e:  ldrb r0, [r5, #3]                 
  03930:  adds r0, r0, #5                   
  03932:  strb.w r8, [r6, r0]               
  03936:  ldrb r0, [r5, #3]                 
  03938:  adds r0, r0, #6                   
  0393a:  strb r0, [r7]                     
  0393c:  pop.w {r4, r5, r6, r7, r8, pc}    
```
