# func_0x0aad0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000aad0) | `0x0000aad0` |
| размер кода | 58 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x0ab04 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0acce` (bl @0x0000ad10)
- `func_0x0acce` (bl @0x0000add8)
- `func_0x0ad9e` (bl @0x0000add8)


## Дизассембляция

```asm
  0aad0:  push {r4, r5, lr}                 
  0aad2:  mov r2, r0                        
  0aad4:  mov r3, r1                        
  0aad6:  movs r0, #0                       
  0aad8:  movs r1, #0                       
  0aada:  nop                               
  0aadc:  b #0xab04                         -> 0x0ab04 (вне списка функций)
  0aade:  asrs r4, r0, #8                   
  0aae0:  orr.w r4, r4, r0, lsl #8          
  0aae4:  uxth r0, r4                       
  0aae6:  ldrb r4, [r2, r1]                 
  0aae8:  eors r0, r4                       
  0aaea:  ubfx r4, r0, #4, #4               
  0aaee:  eors r0, r4                       
  0aaf0:  movw r5, #0xffff                  
  0aaf4:  and.w r4, r5, r0, lsl #12         
  0aaf8:  eors r0, r4                       
  0aafa:  lsls r4, r0, #0x18                
  0aafc:  lsrs r4, r4, #0x14                
  0aafe:  eor.w r0, r0, r4, lsl #1          
  0ab02:  adds r1, r1, #1                   
  0ab04:  cmp r1, r3                        
  0ab06:  blo #0xaade                       
  0ab08:  pop {r4, r5, pc}                  
```
