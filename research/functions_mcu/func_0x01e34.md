# func_0x01e34

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080001e34) | `0x00001e34` |
| размер кода | 30 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x01e4a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x054dc` (bl @0x00005590)
- `func_0x056bc` (bl @0x0000574e)


## Дизассембляция

```asm
  01e34:  push {r4, lr}                     
  01e36:  mov r2, r0                        
  01e38:  mov r3, r1                        
  01e3a:  movs r1, #0                       
  01e3c:  movs r4, #0                       
  01e3e:  nop                               
  01e40:  b #0x1e4a                         -> 0x01e4a (вне списка функций)
  01e42:  ldrb r0, [r2, r1]                 
  01e44:  add r0, r4                        
  01e46:  uxtb r4, r0                       
  01e48:  adds r1, r1, #1                   
  01e4a:  cmp r1, r3                        
  01e4c:  blt #0x1e42                       
  01e4e:  uxtb r0, r4                       
  01e50:  pop {r4, pc}                      
```
