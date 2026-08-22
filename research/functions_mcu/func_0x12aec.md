# func_0x12aec

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012aec) | `0x00012aec` |
| размер кода | 96 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000f95 — RAM (r1)

## Вызовы (callees)

- `func_0x0cee0` (0x0000cee0, bl)
- 0x12b3c (b, вне списка функций)
- 0x12b44 (b, вне списка функций)
- `func_0x155ac` (0x000155ac, bl)

## Кто вызывает (callers / xrefs)

- `func_0x03b2a` (bl @0x00003b30)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x12b24..0x12b3e` (26 Б); цели из: 0x12b16
- `0x12b3e..0x12b44` (6 Б); цели из: 0x12b22
- `0x12b44..0x12b4c` (8 Б); цели из: 0x12af4

## Дизассембляция

```asm
  12aec:  push {r3, r4, r5, lr}             
  12aee:  movs r0, #0                       
  12af0:  str r0, [sp]                      
  12af2:  movs r4, #0                       
  12af4:  b #0x12b44                        -> 0x12b44 (вне списка функций)
  12af6:  movs r3, #2                       
  12af8:  mov r2, sp                        
  12afa:  movw r1, #0x91a2                  
  12afe:  movs r0, #8                       
  12b00:  bl #0xcee0                        -> func_0x0cee0
  12b04:  cbz r0, #0x12b40                  
  12b06:  ldrh.w r0, [sp]                   
  12b0a:  ldr r1, [pc, #0x40]               -> RAM
  12b0c:  strh r0, [r1, #0x1a]              
  12b0e:  ldrh.w r0, [sp]                   
  12b12:  cmp.w r0, #0x7d00                 
  12b16:  blt #0x12b24                      
  12b18:  ldrh.w r0, [sp]                   
  12b1c:  movw r1, #0x8ca0                  
  12b20:  cmp r0, r1                        
  12b22:  ble #0x12b3e                      
  12b24:  movw r0, #0x84d0                  
  12b28:  str r0, [sp]                      
  12b2a:  movs r3, #2                       
  12b2c:  ldrh.w r2, [sp]                   
  12b30:  movw r1, #0x91a2                  
  12b34:  movs r0, #8                       
  12b36:  bl #0x155ac                       -> func_0x155ac
  12b3a:  cbz r0, #0x12b40                  
  12b3c:  pop {r3, r4, r5, pc}              
  12b3e:  b #0x12b3c                        -> 0x12b3c (вне списка функций)
  12b40:  adds r0, r4, #1                   
  12b42:  uxtb r4, r0                       
  12b44:  cmp r4, #3                        
  12b46:  blt #0x12af6                      
  12b48:  nop                               
  12b4a:  b #0x12b3c                        -> 0x12b3c (вне списка функций)
  ; --- literal-пул @0x12b4c (1 слов) — ВНЕ границ функции ---
  12b4c:  .word 0x20000f95  ; RAM
```
