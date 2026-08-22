# func_0x0bb14

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000bb14) | `0x0000bb14` |
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
  0bb14:  push.w {r0, r1, r2, r3, r4, r5, r6, r7, r8, sb, lr}
  0bb18:  sub sp, #0x2c                     
  0bb1a:  mov r7, r0                        
  0bb1c:  mov r6, r2                        
  0bb1e:  mov r8, r3                        
  0bb20:  ldrd sb, r4, [sp, #0x58]          
  0bb24:  movs r5, #0                       
  0bb26:  ldr r0, [r4]                      
  0bb28:  cbnz r0, #0xbb34                  
  0bb2a:  movs r5, #1                       
  0bb2c:  mov r0, r5                        
  0bb2e:  add sp, #0x3c                     
  0bb30:  pop.w {r4, r5, r6, r7, r8, sb, pc}
```
