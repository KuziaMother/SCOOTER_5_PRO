# func_0x129b4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800129b4) | `0x000129b4` |
| размер кода | 46 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b58 — RAM (r0)

## Вызовы (callees)

- `func_0x04c84` (0x00004c84, bl)
- 0x12470 (bl, вне списка функций)
- 0x12a46 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Дизассембляция

```asm
  129b4:  push {r4, lr}                     
  129b6:  mov r4, r0                        
  129b8:  movs r1, #0xa                     
  129ba:  movs r0, #1                       
  129bc:  bl #0x4c84                        -> func_0x04c84
  129c0:  bl #0x12470                       -> 0x12470 (вне списка функций)
  129c4:  ldr r0, [pc, #0x98]               -> RAM
  129c6:  ldrb r0, [r0]                     
  129c8:  cmp r0, #0xa                      
  129ca:  bhs #0x129da                      
  129cc:  tbb [pc, r0]                      
  129d0:  lsrs r1, r1, #0x18                
  129d2:  adds r3, r2, r0                   
  129d4:  movs r2, #0x1d                    
  129d6:  cmp r4, #0x27                     
  129d8:  adds r6, #0x31                    
  129da:  movs r0, #0                       
  129dc:  ldr r1, [pc, #0x80]               -> RAM
  129de:  strb r0, [r1]                     
  129e0:  b #0x12a46                        -> 0x12a46 (вне списка функций)
  ; --- literal-пул @0x12a60 (1 слов) — ВНЕ границ функции ---
  12a60:  .word 0x20000b58  ; RAM
```
