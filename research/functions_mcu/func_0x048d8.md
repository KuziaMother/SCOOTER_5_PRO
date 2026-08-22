# func_0x048d8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800048d8) | `0x000048d8` |
| размер кода | 32 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x048ee (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  048d8:  push {r4, lr}                     
  048da:  mov r2, r0                        
  048dc:  mov r3, r1                        
  048de:  movs r0, #0                       
  048e0:  movs r1, #0                       
  048e2:  b #0x48ee                         -> 0x048ee (вне списка функций)
  048e4:  ldrb r4, [r2, r1]                 
  048e6:  add r4, r0                        
  048e8:  uxtb r0, r4                       
  048ea:  adds r4, r1, #1                   
  048ec:  uxtb r1, r4                       
  048ee:  cmp r1, r3                        
  048f0:  blt #0x48e4                       
  048f2:  mvns r4, r0                       
  048f4:  uxtb r0, r4                       
  048f6:  pop {r4, pc}                      
```
