# func_0x09aa4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080009aa4) | `0x00009aa4` |
| размер кода | 86 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20001344 — RAM (r1)
- 0x20001359 — RAM (r1)
- 0x20001384 — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x051d8` (bl @0x00005234)


## Дизассембляция

```asm
  09aa4:  push {r4, lr}                     
  09aa6:  movs r0, #0                       
  09aa8:  ldr r1, [pc, #0x50]               -> RAM
  09aaa:  str r0, [r1]                      
  09aac:  str r0, [r1, #4]                  
  09aae:  str r0, [r1, #8]                  
  09ab0:  str r0, [r1, #0xc]                
  09ab2:  strh r0, [r1, #0x10]              
  09ab4:  strb r0, [r1, #0x12]              
  09ab6:  strh.w r0, [r1, #0x13]            
  09aba:  ldr r1, [pc, #0x44]               -> RAM
  09abc:  strb r0, [r1]                     
  09abe:  strh.w r0, [r1, #1]               
  09ac2:  strh.w r0, [r1, #3]               
  09ac6:  strh.w r0, [r1, #5]               
  09aca:  strb r0, [r1, #7]                 
  09acc:  str r0, [r1, #8]                  
  09ace:  str r0, [r1, #0xc]                
  09ad0:  strb r0, [r1, #0x10]              
  09ad2:  str.w r0, [r1, #0x11]             
  09ad6:  strh.w r0, [r1, #0x15]            
  09ada:  strb r0, [r1, #0x17]              
  09adc:  strh r0, [r1, #0x18]              
  09ade:  strb r0, [r1, #0x1a]              
  09ae0:  str.w r0, [r1, #0x1b]             
  09ae4:  strb r0, [r1, #0x1f]              
  09ae6:  str r0, [r1, #0x20]               
  09ae8:  strb.w r0, [r1, #0x24]            
  09aec:  strh.w r0, [r1, #0x25]            
  09af0:  movs r1, #0x4a                    
  09af2:  ldr r0, [pc, #0x10]               -> RAM
  09af4:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  09af8:  pop {r4, pc}                      
  ; --- literal-пул @0x09afc (3 слов) — ВНЕ границ функции ---
  09afc:  .word 0x20001344  ; RAM
  09b00:  .word 0x20001359  ; RAM
  09b04:  .word 0x20001384  ; RAM
```
