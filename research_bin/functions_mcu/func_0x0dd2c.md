# func_0x0dd2c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000dd2c) | `0x0000dd2c` |
| размер кода | 84 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x0dd72 (b, вне списка функций)
- 0x0dd7c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03f00` (bl @0x0000414e)
- `func_0x03f00` (bl @0x00004178)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0dd40..0x0dd48` (8 Б); цели из: 0x0dd3a
- `0x0dd48..0x0dd66` (30 Б); цели из: 0x0dd42
- `0x0dd66..0x0dd72` (12 Б); цели из: 0x0dd5a
- `0x0dd72..0x0dd78` (6 Б); цели из: 0x0dd64
- `0x0dd78..0x0dd7c` (4 Б); цели из: 0x0dd74
- `0x0dd7c..0x0dd80` (4 Б); цели из: 0x0dd3e, 0x0dd46

## Дизассембляция

```asm
  0dd2c:  push.w {r4, r5, r6, r7, r8, sb, lr}
  0dd30:  mov r4, r0                        
  0dd32:  mov r6, r4                        
  0dd34:  mla r7, r1, r2, r4                
  0dd38:  cmp r3, r6                        
  0dd3a:  bhs #0xdd40                       
  0dd3c:  mov r0, r6                        
  0dd3e:  b #0xdd7c                         -> 0x0dd7c (вне списка функций)
  0dd40:  cmp r3, r7                        
  0dd42:  bls #0xdd48                       
  0dd44:  mov r0, r7                        
  0dd46:  b #0xdd7c                         -> 0x0dd7c (вне списка функций)
  0dd48:  sub.w r8, r3, r4                  
  0dd4c:  udiv sb, r8, r1                   
  0dd50:  mls ip, r1, sb, r8                
  0dd54:  lsl.w r8, ip, #1                  
  0dd58:  cmp r8, r1                        
  0dd5a:  bhi #0xdd66                       
  0dd5c:  sub.w r8, r3, r4                  
  0dd60:  udiv r5, r8, r1                   
  0dd64:  b #0xdd72                         -> 0x0dd72 (вне списка функций)
  0dd66:  sub.w r8, r3, r4                  
  0dd6a:  udiv r8, r8, r1                   
  0dd6e:  add.w r5, r8, #1                  
  0dd72:  cmp r5, r2                        
  0dd74:  bls #0xdd78                       
  0dd76:  mov r5, r2                        
  0dd78:  mla r0, r1, r5, r4                
  0dd7c:  pop.w {r4, r5, r6, r7, r8, sb, pc}
```
