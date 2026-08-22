# func_0x02e0c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002e0c) | `0x00002e0c` |
| размер кода | 16 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x02d70` (bl @0x00002dc6)


## Дизассембляция

```asm
  02e0c:  push {r0, r1, r2, r3, r4, r5, r6, lr}
  02e0e:  mov r5, r0                        
  02e10:  mov r4, r1                        
  02e12:  cbz r5, #0x2e16                   
  02e14:  cbnz r4, #0x2e1c                  
  02e16:  movs r0, #1                       
  02e18:  add sp, #0x10                     
  02e1a:  pop {r4, r5, r6, pc}              
```
