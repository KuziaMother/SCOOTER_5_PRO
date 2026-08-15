# func_0x169f0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800169f0) | `0x000169f0` |
| размер кода | 178 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x161ea` (0x000161ea, bl)
- 0x16a28 (b, вне списка функций)
- 0x16a2e (b, вне списка функций)
- 0x16a5c (b, вне списка функций)
- 0x16a9c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e808` (bl @0x0000e9ac)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x16a08..0x16a26` (30 Б); цели из: 0x16a00
- `0x16a26..0x16a28` (2 Б); цели из: 0x16a20
- `0x16a28..0x16a2e` (6 Б); цели из: 0x16a24
- `0x16a2e..0x16a54` (38 Б); цели из: 0x16a18
- `0x16a54..0x16a5c` (8 Б); цели из: 0x16a0e
- `0x16a5c..0x16a84` (40 Б); цели из: 0x16a06, 0x16a52
- `0x16a84..0x16a9c` (24 Б); цели из: 0x16a68
- `0x16a9c..0x16aa2` (6 Б); цели из: 0x16a82

## Дизассембляция

```asm
  169f0:  push.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  169f4:  mov r8, r0                        
  169f6:  mov r6, r1                        
  169f8:  mov r7, r2                        
  169fa:  mov sb, r3                        
  169fc:  ldr r0, [r6]                      
  169fe:  cmp r0, r8                        
  16a00:  blt #0x16a08                      
  16a02:  movs r4, #0                       
  16a04:  movs r5, #0                       
  16a06:  b #0x16a5c                        -> 0x16a5c (вне списка функций)
  16a08:  ldr.w r0, [r6, sb, lsl #2]        
  16a0c:  cmp r0, r8                        
  16a0e:  ble #0x16a54                      
  16a10:  lsr.w r5, sb, #1                  
  16a14:  movs r4, #0                       
  16a16:  mov fp, sb                        
  16a18:  b #0x16a2e                        -> 0x16a2e (вне списка функций)
  16a1a:  ldr.w r0, [r6, r5, lsl #2]        
  16a1e:  cmp r0, r8                        
  16a20:  ble #0x16a26                      
  16a22:  mov fp, r5                        
  16a24:  b #0x16a28                        -> 0x16a28 (вне списка функций)
  16a26:  mov r4, r5                        
  16a28:  add.w r0, fp, r4                  
  16a2c:  lsrs r5, r0, #1                   
  16a2e:  sub.w r0, fp, r4                  
  16a32:  cmp r0, #1                        
  16a34:  bhi #0x16a1a                      
  16a36:  adds r2, r4, #1                   
  16a38:  ldr.w r2, [r6, r2, lsl #2]        
  16a3c:  ldr.w r3, [r6, r4, lsl #2]        
  16a40:  subs r1, r2, r3                   
  16a42:  ldr.w r2, [r6, r4, lsl #2]        
  16a46:  sub.w r0, r8, r2                  
  16a4a:  movs r2, #0x10                    
  16a4c:  bl #0x161ea                       -> func_0x161ea
  16a50:  mov r5, r0                        
  16a52:  b #0x16a5c                        -> 0x16a5c (вне списка функций)
  16a54:  sub.w r4, sb, #1                  
  16a58:  mov.w r5, #0x10000                
  16a5c:  adds r0, r4, #1                   
  16a5e:  ldrh.w sl, [r7, r0, lsl #1]       
  16a62:  ldrh.w r0, [r7, r4, lsl #1]       
  16a66:  cmp r0, sl                        
  16a68:  bgt #0x16a84                      
  16a6a:  ldrh.w r1, [r7, r4, lsl #1]       
  16a6e:  ldrh.w r0, [r7, r4, lsl #1]       
  16a72:  sub.w r0, sl, r0                  
  16a76:  uxth r0, r0                       
  16a78:  muls r0, r5, r0                   
  16a7a:  add.w r0, r1, r0, lsr #16         
  16a7e:  uxth r0, r0                       
  16a80:  str r0, [sp]                      
  16a82:  b #0x16a9c                        -> 0x16a9c (вне списка функций)
  16a84:  ldrh.w r1, [r7, r4, lsl #1]       
  16a88:  ldrh.w r0, [r7, r4, lsl #1]       
  16a8c:  sub.w r0, r0, sl                  
  16a90:  uxth r0, r0                       
  16a92:  muls r0, r5, r0                   
  16a94:  sub.w r0, r1, r0, lsr #16         
  16a98:  uxth r0, r0                       
  16a9a:  str r0, [sp]                      
  16a9c:  ldr r0, [sp]                      
  16a9e:  pop.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
```
