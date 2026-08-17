# func_0x048f8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800048f8) | `0x000048f8` |
| размер кода | 142 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a66 — RAM (r0)
- 0x20000f70 — RAM (r0)
- 0x2000164b — RAM (r0)

## Вызовы (callees)

- `func_0x01bdc` (0x00001bdc, bl)
- `func_0x01c60` (0x00001c60, bl)
- 0x04960 (b, вне списка функций)
- 0x09400 (bl, вне списка функций)
- `func_0x0bf58` (0x0000bf58, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0c098` (bl @0x0000c0a6)


## Дизассембляция

```asm
  048f8:  push {r3, r4, r5, lr}             
  048fa:  movs r4, #1                       
  048fc:  ldr r0, [pc, #0x88]               -> RAM
  048fe:  ldrb r0, [r0]                     
  04900:  cmp r0, #1                        
  04902:  bne #0x4934                       
  04904:  ldr r0, [pc, #0x84]               -> RAM
  04906:  ldrb r0, [r0, #1]                 
  04908:  ubfx r0, r0, #1, #1               
  0490c:  cbnz r0, #0x4934                  
  0490e:  bl #0x9400                        -> 0x09400 (вне списка функций)
  04912:  cbnz r0, #0x4960                  
  04914:  movs r2, #1                       
  04916:  movs r1, #2                       
  04918:  ldr r0, [pc, #0x74]               -> RAM
  0491a:  bl #0xbf58                        -> func_0x0bf58
  0491e:  ands r4, r0                       
  04920:  mov.w r0, #0x1f4                  
  04924:  str r0, [sp]                      
  04926:  nop                               
  04928:  ldr r0, [sp]                      
  0492a:  subs r1, r0, #1                   
  0492c:  str r1, [sp]                      
  0492e:  cmp r0, #0                        
  04930:  bne #0x4928                       
  04932:  b #0x4960                         -> 0x04960 (вне списка функций)
  04934:  ldr r0, [pc, #0x50]               -> RAM
  04936:  ldrb r0, [r0]                     
  04938:  cbnz r0, #0x4960                  
  0493a:  ldr r0, [pc, #0x50]               -> RAM
  0493c:  ldrb r0, [r0, #1]                 
  0493e:  ubfx r0, r0, #1, #1               
  04942:  cbz r0, #0x4960                   
  04944:  movs r0, #0x94                    
  04946:  bl #0x1bdc                        -> func_0x01bdc
  0494a:  ands r4, r0                       
  0494c:  mov.w r0, #0x1f4                  
  04950:  str r0, [sp]                      
  04952:  nop                               
  04954:  ldr r0, [sp]                      
  04956:  subs r1, r0, #1                   
  04958:  str r1, [sp]                      
  0495a:  cmp r0, #0                        
  0495c:  bne #0x4954                       
  0495e:  nop                               
  04960:  movs r3, #1                       
  04962:  ldr r2, [pc, #0x2c]               -> RAM
  04964:  movs r1, #0x7f                    
  04966:  movs r0, #8                       
  04968:  bl #0x1c60                        -> func_0x01c60
  0496c:  ands r4, r0                       
  0496e:  ldr r0, [pc, #0x20]               -> RAM
  04970:  subs r0, #0x54                    
  04972:  ldrb.w r0, [r0, #0x54]            
  04976:  ldr r1, [pc, #0x14]               -> RAM
  04978:  ldrb r1, [r1, #1]                 
  0497a:  bfi r1, r0, #1, #1                
  0497e:  ldr r0, [pc, #0xc]                -> RAM
  04980:  strb r1, [r0, #1]                 
  04982:  mov r0, r4                        
  04984:  pop {r3, r4, r5, pc}              
  ; --- literal-пул @0x04988 (3 слов) — ВНЕ границ функции ---
  04988:  .word 0x20000a66  ; RAM
  0498c:  .word 0x20000f70  ; RAM
  04990:  .word 0x2000164b  ; RAM
```
