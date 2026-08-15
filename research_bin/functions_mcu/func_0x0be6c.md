# func_0x0be6c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000be6c) | `0x0000be6c` |
| размер кода | 104 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x0bec0 (b, вне списка функций)
- 0x0bed8 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0be96..0x0beac` (22 Б); цели из: 0x0be8a
- `0x0beac..0x0bec0` (20 Б); цели из: 0x0be8e
- `0x0bec0..0x0bed4` (20 Б); цели из: 0x0be94

## Дизассембляция

```asm
  0be6c:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  0be70:  mov r6, r0                        
  0be72:  mov r4, r1                        
  0be74:  mov r8, r2                        
  0be76:  mov.w sb, #0                      
  0be7a:  movs r7, #0                       
  0be7c:  mov r5, r6                        
  0be7e:  ldrb r0, [r5]                     
  0be80:  strb r0, [r4]                     
  0be82:  ldrb r0, [r5, #1]                 
  0be84:  strb r0, [r4, #1]                 
  0be86:  ldrb r0, [r5, #1]                 
  0be88:  cmp r0, #3                        
  0be8a:  beq #0xbe96                       
  0be8c:  cmp r0, #6                        
  0be8e:  beq #0xbeac                       
  0be90:  cmp r0, #0x10                     
  0be92:  bne #0xbed4                       
  0be94:  b #0xbec0                         -> 0x0bec0 (вне списка функций)
  0be96:  ldrb r0, [r5, #6]                 
  0be98:  strb r0, [r4, #2]                 
  0be9a:  ldrb r2, [r5, #6]                 
  0be9c:  adds r1, r5, #7                   
  0be9e:  adds r0, r4, #3                   
  0bea0:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0bea4:  ldrb r0, [r5, #6]                 
  0bea6:  adds r0, r0, #3                   
  0bea8:  uxtb r7, r0                       
  0beaa:  b #0xbed8                         -> 0x0bed8 (вне списка функций)
  0beac:  ldrb r0, [r5, #2]                 
  0beae:  strb r0, [r4, #2]                 
  0beb0:  ldrb r0, [r5, #3]                 
  0beb2:  strb r0, [r4, #3]                 
  0beb4:  ldrb r0, [r5, #7]                 
  0beb6:  strb r0, [r4, #4]                 
  0beb8:  ldrb r0, [r5, #8]                 
  0beba:  strb r0, [r4, #5]                 
  0bebc:  movs r7, #6                       
  0bebe:  b #0xbed8                         -> 0x0bed8 (вне списка функций)
  0bec0:  ldrb r0, [r5, #2]                 
  0bec2:  strb r0, [r4, #2]                 
  0bec4:  ldrb r0, [r5, #3]                 
  0bec6:  strb r0, [r4, #3]                 
  0bec8:  ldrb r0, [r5, #4]                 
  0beca:  strb r0, [r4, #4]                 
  0becc:  ldrb r0, [r5, #5]                 
  0bece:  strb r0, [r4, #5]                 
  0bed0:  movs r7, #6                       
  0bed2:  b #0xbed8                         -> 0x0bed8 (вне списка функций)
```
