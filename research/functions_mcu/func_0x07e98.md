# func_0x07e98

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007e98) | `0x00007e98` |
| размер кода | 52 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08003000 — flash-mirror @0x03000 (r0)
- 0x0801ffff — flash-mirror @0x1ffff (r0)

## Вызовы (callees)

- `func_0x06230` (0x00006230, bl)
- `func_0x062d4` (0x000062d4, bl)
- `func_0x06378` (0x00006378, bl)
- 0x07eb0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x07e70` (bl @0x00007e7e)
- `func_0x080ac` (bl @0x000080f6)
- `func_0x0acce` (bl @0x0000ad20)
- `func_0x0acce` (bl @0x0000ad74)
- `func_0x0acce` (bl @0x0000ad7a)
- `func_0x0acce` (bl @0x0000ade8)
- `func_0x0acce` (bl @0x0000ae3c)
- `func_0x0acce` (bl @0x0000ae42)
- `func_0x0ad9e` (bl @0x0000ade8)
- `func_0x0ad9e` (bl @0x0000ae3c)
- `func_0x0ad9e` (bl @0x0000ae42)
- `func_0x0ddc4` (bl @0x0000dddc)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x07eae..0x07eb2` (4 Б); цели из: 0x07ea6
- `0x07eb2..0x07ec4` (18 Б); цели из: 0x07eac
- `0x07ec4..0x07ecc` (8 Б); цели из: 0x07ebe

## Дизассембляция

```asm
  07e98:  push {r4, lr}                     
  07e9a:  mov r4, r0                        
  07e9c:  ubfx r0, r4, #0, #0xb             
  07ea0:  cbnz r0, #0x7eae                  
  07ea2:  ldr r0, [pc, #0x28]               -> flash-mirror @0x1ffff
  07ea4:  cmp r4, r0                        
  07ea6:  bhs #0x7eae                       
  07ea8:  ldr r0, [pc, #0x24]               -> flash-mirror @0x03000
  07eaa:  cmp r4, r0                        
  07eac:  bhs #0x7eb2                       
  07eae:  movs r0, #0                       
  07eb0:  pop {r4, pc}                      
  07eb2:  bl #0x6378                        -> func_0x06378
  07eb6:  mov r0, r4                        
  07eb8:  bl #0x6230                        -> func_0x06230
  07ebc:  cmp r0, #6                        
  07ebe:  beq #0x7ec4                       
  07ec0:  movs r0, #0                       
  07ec2:  b #0x7eb0                         -> 0x07eb0 (вне списка функций)
  07ec4:  bl #0x62d4                        -> func_0x062d4
  07ec8:  movs r0, #1                       
  07eca:  b #0x7eb0                         -> 0x07eb0 (вне списка функций)
  ; --- literal-пул @0x07ecc (2 слов) — ВНЕ границ функции ---
  07ecc:  .word 0x0801ffff  ; flash-mirror @0x1ffff
  07ed0:  .word 0x08003000  ; flash-mirror @0x03000
```
