# func_0x0eddc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000eddc) | `0x0000eddc` |
| размер кода | 98 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00025e20 — прочее (r1)
- 0x2000304c — RAM (r0)

## Вызовы (callees)

- `func_0x0cfb8` (0x0000cfb8, bl)
- `func_0x1570c` (0x0001570c, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01df4` (bl @0x00001e06)


## Дизассембляция

```asm
  0eddc:  push {r3, lr}                     
  0edde:  bl #0xcfb8                        -> func_0x0cfb8
  0ede2:  cbnz r0, #0xedfa                  
  0ede4:  mov.w r0, #0x3e8                  
  0ede8:  str r0, [sp]                      
  0edea:  nop                               
  0edec:  ldr r0, [sp]                      
  0edee:  subs r1, r0, #1                   
  0edf0:  str r1, [sp]                      
  0edf2:  cmp r0, #0                        
  0edf4:  bne #0xedec                       
  0edf6:  bl #0xcfb8                        -> func_0x0cfb8
  0edfa:  ldr r0, [pc, #0x44]               -> RAM
  0edfc:  ldr r0, [r0]                      
  0edfe:  cmp.w r0, #0x1f4                  
  0ee02:  bhi #0xee2a                       
  0ee04:  ldr r0, [pc, #0x38]               -> RAM
  0ee06:  ldr r0, [r0, #4]                  
  0ee08:  cmp.w r0, #0x21000                
  0ee0c:  blo #0xee2a                       
  0ee0e:  ldr r0, [pc, #0x30]               -> RAM
  0ee10:  ldr r0, [r0, #4]                  
  0ee12:  ldr r1, [pc, #0x30]               
  0ee14:  cmp r0, r1                        
  0ee16:  bhi #0xee2a                       
  0ee18:  ldr r0, [pc, #0x24]               -> RAM
  0ee1a:  ldr r0, [r0, #8]                  
  0ee1c:  cmp.w r0, #0x21000                
  0ee20:  blo #0xee2a                       
  0ee22:  ldr r0, [pc, #0x1c]               -> RAM
  0ee24:  ldr r0, [r0, #8]                  
  0ee26:  cmp r0, r1                        
  0ee28:  bls #0xee3c                       
  0ee2a:  movs r0, #0                       
  0ee2c:  ldr r1, [pc, #0x10]               -> RAM
  0ee2e:  str r0, [r1]                      
  0ee30:  mov.w r0, #0x21000                
  0ee34:  str r0, [r1, #4]                  
  0ee36:  str r0, [r1, #8]                  
  0ee38:  bl #0x1570c                       -> func_0x1570c
  0ee3c:  pop {r3, pc}                      
  ; --- literal-пул @0x0ee40 (2 слов) — ВНЕ границ функции ---
  0ee40:  .word 0x2000304c  ; RAM
  0ee44:  .word 0x00025e20
```
