# func_0x08a90

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008a90) | `0x00008a90` |
| размер кода | 94 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0cc1c` (0x0000cc1c, bl)
- `func_0x0ccbc` (0x0000ccbc, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03970` (bl @0x00003974)
- `func_0x08938` (bl @0x0000894a)
- `func_0x0c984` (bl @0x0000c98a)
- `func_0x0d00c` (bl @0x0000d06a)
- `func_0x0d534` (bl @0x0000d55e)
- `func_0x0d5d4` (bl @0x0000d5fe)
- `func_0x0d878` (bl @0x0000d87c)
- `func_0x0d938` (bl @0x0000d958)
- `func_0x0d938` (bl @0x0000db2e)
- `func_0x139fc` (bl @0x00013a0a)
- `func_0x13c78` (bl @0x00013c82)
- `func_0x14f50` (bl @0x0001507a)


## Дизассембляция

```asm
  08a90:  push {r0, r1, r2, r3, r4, lr}     
  08a92:  mov r4, r0                        
  08a94:  add r1, sp, #0xc                  
  08a96:  movs r0, #0                       
  08a98:  bl #0xcc1c                        -> func_0x0cc1c
  08a9c:  add r1, sp, #8                    
  08a9e:  movs r0, #0                       
  08aa0:  bl #0xccbc                        -> func_0x0ccbc
  08aa4:  ldrb.w r0, [sp, #8]               
  08aa8:  strb.w r0, [sp, #2]               
  08aac:  ldrb.w r0, [sp, #9]               
  08ab0:  strb.w r0, [sp, #1]               
  08ab4:  ldrb.w r0, [sp, #0xa]             
  08ab8:  strb.w r0, [sp]                   
  08abc:  ldrb.w r0, [sp, #0xd]             
  08ac0:  strb.w r0, [sp, #4]               
  08ac4:  ldrb.w r0, [sp, #0xc]             
  08ac8:  strb.w r0, [sp, #6]               
  08acc:  ldrb.w r0, [sp, #0xe]             
  08ad0:  strb.w r0, [sp, #3]               
  08ad4:  ldrb.w r0, [sp, #0xf]             
  08ad8:  strb.w r0, [sp, #5]               
  08adc:  ldr r0, [sp]                      
  08ade:  str r0, [r4]                      
  08ae0:  ldrh.w r0, [sp, #4]               
  08ae4:  strh r0, [r4, #4]                 
  08ae6:  ldrb.w r0, [sp, #6]               
  08aea:  strb r0, [r4, #6]                 
  08aec:  pop {r0, r1, r2, r3, r4, pc}      
```
