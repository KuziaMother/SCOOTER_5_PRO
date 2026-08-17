# func_0x04c84

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080004c84) | `0x00004c84` |
| размер кода | 48 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000b4c — RAM (r0)
- 0x2000164c — RAM (r0)

## Вызовы (callees)

- `func_0x02d1c` (0x00002d1c, bl)
- `func_0x02d34` (0x00002d34, bl)
- 0x04cae (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x09a44` (bl @0x00009a76)
- `func_0x09a44` (bl @0x00009a7e)
- `func_0x09a44` (bl @0x00009a86)
- `func_0x09a44` (bl @0x00009a8e)
- `func_0x128e4` (bl @0x000128ec)
- `func_0x129b4` (bl @0x000129bc)
- `func_0x12a64` (bl @0x00012a6c)
- `func_0x12a78` (bl @0x00012a82)


## Дизассембляция

```asm
  04c84:  push {r4, r5, r6, lr}             
  04c86:  mov r5, r0                        
  04c88:  mov r6, r1                        
  04c8a:  cmp r5, #6                        
  04c8c:  bge #0x4cb2                       
  04c8e:  ldr r0, [pc, #0x24]               -> RAM
  04c90:  add.w r4, r0, r5, lsl #4          
  04c94:  bl #0x2d1c                        -> func_0x02d1c
  04c98:  ldr r0, [pc, #0x1c]               -> RAM
  04c9a:  ldr r0, [r0]                      
  04c9c:  add r0, r6                        
  04c9e:  str r0, [r4, #4]                  
  04ca0:  movs r0, #1                       
  04ca2:  strb r0, [r4]                     
  04ca4:  cbnz r6, #0x4caa                  
  04ca6:  strb r0, [r4, #1]                 
  04ca8:  b #0x4cae                         -> 0x04cae (вне списка функций)
  04caa:  movs r0, #0                       
  04cac:  strb r0, [r4, #1]                 
  04cae:  bl #0x2d34                        -> func_0x02d34
  04cb2:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x04cb4 (2 слов) — ВНЕ границ функции ---
  04cb4:  .word 0x2000164c  ; RAM
  04cb8:  .word 0x20000b4c  ; RAM
```
