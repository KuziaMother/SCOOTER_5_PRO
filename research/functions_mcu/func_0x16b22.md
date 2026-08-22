# func_0x16b22

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080016b22) | `0x00016b22` |
| размер кода | 178 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x161ea` (0x000161ea, bl)
- 0x16b5a (b, вне списка функций)
- 0x16b60 (b, вне списка функций)
- 0x16b8e (b, вне списка функций)
- 0x16bce (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x070d8` (bl @0x00007268)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x16b3a..0x16b58` (30 Б); цели из: 0x16b32
- `0x16b58..0x16b5a` (2 Б); цели из: 0x16b52
- `0x16b5a..0x16b60` (6 Б); цели из: 0x16b56
- `0x16b60..0x16b86` (38 Б); цели из: 0x16b4a
- `0x16b86..0x16b8e` (8 Б); цели из: 0x16b40
- `0x16b8e..0x16bb6` (40 Б); цели из: 0x16b38, 0x16b84
- `0x16bb6..0x16bce` (24 Б); цели из: 0x16b9a
- `0x16bce..0x16bd4` (6 Б); цели из: 0x16bb4

## Дизассембляция

```asm
  16b22:  push.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  16b26:  mov r8, r0                        
  16b28:  mov r6, r1                        
  16b2a:  mov r7, r2                        
  16b2c:  mov sb, r3                        
  16b2e:  ldr r0, [r6]                      
  16b30:  cmp r0, r8                        
  16b32:  blo #0x16b3a                      
  16b34:  movs r4, #0                       
  16b36:  movs r5, #0                       
  16b38:  b #0x16b8e                        -> 0x16b8e (вне списка функций)
  16b3a:  ldr.w r0, [r6, sb, lsl #2]        
  16b3e:  cmp r0, r8                        
  16b40:  bls #0x16b86                      
  16b42:  lsr.w r5, sb, #1                  
  16b46:  movs r4, #0                       
  16b48:  mov fp, sb                        
  16b4a:  b #0x16b60                        -> 0x16b60 (вне списка функций)
  16b4c:  ldr.w r0, [r6, r5, lsl #2]        
  16b50:  cmp r0, r8                        
  16b52:  bls #0x16b58                      
  16b54:  mov fp, r5                        
  16b56:  b #0x16b5a                        -> 0x16b5a (вне списка функций)
  16b58:  mov r4, r5                        
  16b5a:  add.w r0, fp, r4                  
  16b5e:  lsrs r5, r0, #1                   
  16b60:  sub.w r0, fp, r4                  
  16b64:  cmp r0, #1                        
  16b66:  bhi #0x16b4c                      
  16b68:  adds r2, r4, #1                   
  16b6a:  ldr.w r2, [r6, r2, lsl #2]        
  16b6e:  ldr.w r3, [r6, r4, lsl #2]        
  16b72:  subs r1, r2, r3                   
  16b74:  ldr.w r2, [r6, r4, lsl #2]        
  16b78:  sub.w r0, r8, r2                  
  16b7c:  movs r2, #0x10                    
  16b7e:  bl #0x161ea                       -> func_0x161ea
  16b82:  mov r5, r0                        
  16b84:  b #0x16b8e                        -> 0x16b8e (вне списка функций)
  16b86:  sub.w r4, sb, #1                  
  16b8a:  mov.w r5, #0x10000                
  16b8e:  adds r0, r4, #1                   
  16b90:  ldrh.w sl, [r7, r0, lsl #1]       
  16b94:  ldrh.w r0, [r7, r4, lsl #1]       
  16b98:  cmp r0, sl                        
  16b9a:  bgt #0x16bb6                      
  16b9c:  ldrh.w r1, [r7, r4, lsl #1]       
  16ba0:  ldrh.w r0, [r7, r4, lsl #1]       
  16ba4:  sub.w r0, sl, r0                  
  16ba8:  uxth r0, r0                       
  16baa:  muls r0, r5, r0                   
  16bac:  add.w r0, r1, r0, lsr #16         
  16bb0:  uxth r0, r0                       
  16bb2:  str r0, [sp]                      
  16bb4:  b #0x16bce                        -> 0x16bce (вне списка функций)
  16bb6:  ldrh.w r1, [r7, r4, lsl #1]       
  16bba:  ldrh.w r0, [r7, r4, lsl #1]       
  16bbe:  sub.w r0, r0, sl                  
  16bc2:  uxth r0, r0                       
  16bc4:  muls r0, r5, r0                   
  16bc6:  sub.w r0, r1, r0, lsr #16         
  16bca:  uxth r0, r0                       
  16bcc:  str r0, [sp]                      
  16bce:  ldr r0, [sp]                      
  16bd0:  pop.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
```
