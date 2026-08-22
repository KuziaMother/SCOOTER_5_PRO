# func_0x0307c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000307c) | `0x0000307c` |
| размер кода | 42 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x0c0b4` (0x0000c0b4, bl)

## Кто вызывает (callers / xrefs)

- `func_0x02a94` (bl @0x00002ab6)
- `func_0x02b2c` (bl @0x00002b46)
- `func_0x03222` (bl @0x000032e0)
- `func_0x0327a` (bl @0x000032e0)
- `func_0x032a0` (bl @0x000032e0)


## Дизассембляция

```asm
  0307c:  push {r0, lr}                     
  0307e:  sub sp, #8                        
  03080:  ldrb.w r0, [sp, #8]               
  03084:  strb.w r0, [sp, #4]               
  03088:  ldrb.w r0, [sp, #9]               
  0308c:  strb.w r0, [sp, #5]               
  03090:  ldrb.w r0, [sp, #0xa]             
  03094:  strb.w r0, [sp, #6]               
  03098:  movs r0, #1                       
  0309a:  strb.w r0, [sp, #7]               
  0309e:  add r0, sp, #4                    
  030a0:  bl #0xc0b4                        -> func_0x0c0b4
  030a4:  pop {r1, r2, r3, pc}              
```
