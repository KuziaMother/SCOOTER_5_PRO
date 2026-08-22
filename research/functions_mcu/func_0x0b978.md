# func_0x0b978

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000b978) | `0x0000b978` |
| размер кода | 32 Б |
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
  0b978:  push.w {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, lr}
  0b97c:  sub sp, #0x2c                     
  0b97e:  mov r6, r0                        
  0b980:  mov r7, r2                        
  0b982:  mov r8, r3                        
  0b984:  ldrd sb, r4, [sp, #0x58]          
  0b988:  movs r5, #0                       
  0b98a:  ldr r0, [r4]                      
  0b98c:  cbnz r0, #0xb998                  
  0b98e:  movs r5, #1                       
  0b990:  mov r0, r5                        
  0b992:  add sp, #0x3c                     
  0b994:  pop.w {r4, r5, r6, r7, r8, sb, pc}
```
