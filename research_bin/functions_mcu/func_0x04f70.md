# func_0x04f70

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004f70) | `0x00004f70` |
| размер кода | 60 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x01670` (bl @0x000016a8)
- `func_0x03222` (bl @0x0000325a)


## Дизассембляция

```asm
  04f70:  push {r4, lr}                     
  04f72:  movs r2, #0                       
  04f74:  ldr r2, [r0]                      
  04f76:  movw r3, #0x7ff0                  
  04f7a:  bics r2, r3                       
  04f7c:  ldr r4, [r1, #0x20]               
  04f7e:  ldr r3, [r1, #8]                  
  04f80:  orrs r3, r4                       
  04f82:  ldr r4, [r1, #0x10]               
  04f84:  orrs r3, r4                       
  04f86:  ldr r4, [r1, #0x14]               
  04f88:  orrs r3, r4                       
  04f8a:  ldr r4, [r1, #0x18]               
  04f8c:  orrs r3, r4                       
  04f8e:  ldr r4, [r1, #0x1c]               
  04f90:  orrs r3, r4                       
  04f92:  ldr r4, [r1, #0x24]               
  04f94:  orrs r3, r4                       
  04f96:  ldr r4, [r1, #0x28]               
  04f98:  orrs r3, r4                       
  04f9a:  orrs r2, r3                       
  04f9c:  str r2, [r0]                      
  04f9e:  ldr r3, [r1, #0xc]                
  04fa0:  str r3, [r0, #4]                  
  04fa2:  ldr r3, [r1]                      
  04fa4:  str r3, [r0, #8]                  
  04fa6:  ldr r3, [r1, #4]                  
  04fa8:  str r3, [r0, #0xc]                
  04faa:  pop {r4, pc}                      
```
