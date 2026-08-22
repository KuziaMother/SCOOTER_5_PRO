# func_0x098ae

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800098ae) | `0x000098ae` |
| размер кода | 26 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  098ae:  push {r4, lr}                     
  098b0:  mov r1, r0                        
  098b2:  movs r0, #0                       
  098b4:  movs r3, #0                       
  098b6:  movs r2, #0                       
  098b8:  ldrh r3, [r1, #0x14]              
  098ba:  ldrh r2, [r1, #0x18]              
  098bc:  lsls r2, r2, #0x10                
  098be:  orr.w r4, r3, r2                  
  098c2:  bic r0, r4, #0xff000000           
  098c6:  pop {r4, pc}                      
```
