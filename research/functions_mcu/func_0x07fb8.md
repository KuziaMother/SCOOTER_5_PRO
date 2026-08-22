# func_0x07fb8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007fb8) | `0x00007fb8` |
| размер кода | 28 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x07fcc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x057a0` (bl @0x000057b4)
- `func_0x15df4` (bl @0x00015e98)


## Дизассембляция

```asm
  07fb8:  push {r4, lr}                     
  07fba:  mov r3, r0                        
  07fbc:  mov r4, r1                        
  07fbe:  movs r1, #0                       
  07fc0:  nop                               
  07fc2:  b #0x7fcc                         -> 0x07fcc (вне списка функций)
  07fc4:  ldrb r0, [r3, r1]                 
  07fc6:  strb r0, [r4, r1]                 
  07fc8:  adds r0, r1, #1                   
  07fca:  uxth r1, r0                       
  07fcc:  cmp r1, r2                        
  07fce:  blt #0x7fc4                       
  07fd0:  movs r0, #1                       
  07fd2:  pop {r4, pc}                      
```
