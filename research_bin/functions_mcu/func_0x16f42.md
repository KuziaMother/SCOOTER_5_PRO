# func_0x16f42

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080016f42) | `0x00016f42` |
| размер кода | 156 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x16f84 (b, вне списка функций)
- 0x16f88 (b, вне списка функций)
- 0x16f92 (b, вне списка функций)
- 0x16fc2 (b, вне списка функций)
- 0x16fc6 (b, вне списка функций)
- 0x16fd0 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x069e4` (bl @0x00006c82)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x16f62..0x16f82` (32 Б); цели из: 0x16f5c
- `0x16f82..0x16f84` (2 Б); цели из: 0x16f7c
- `0x16f84..0x16f88` (4 Б); цели из: 0x16f80
- `0x16f88..0x16f90` (8 Б); цели из: 0x16f74
- `0x16f90..0x16f92` (2 Б); цели из: 0x16f6a
- `0x16f92..0x16fa0` (14 Б); цели из: 0x16f60, 0x16f8e
- `0x16fa0..0x16fc0` (32 Б); цели из: 0x16f9a
- `0x16fc0..0x16fc2` (2 Б); цели из: 0x16fba
- `0x16fc2..0x16fc6` (4 Б); цели из: 0x16fbe
- `0x16fc6..0x16fce` (8 Б); цели из: 0x16fb2
- `0x16fce..0x16fd0` (2 Б); цели из: 0x16fa8
- `0x16fd0..0x16fde` (14 Б); цели из: 0x16f9e, 0x16fcc

## Дизассембляция

```asm
  16f42:  push.w {r2, r3, r4, r5, r6, r7, r8, sb, lr}
  16f46:  mov r5, r0                        
  16f48:  mov r6, r1                        
  16f4a:  mov ip, r2                        
  16f4c:  mov r7, r3                        
  16f4e:  ldrd r4, sb, [sp, #0x28]          
  16f52:  ldr.w r8, [sp, #0x24]             
  16f56:  ldr.w r0, [ip]                    
  16f5a:  cmp r0, r5                        
  16f5c:  blt #0x16f62                      
  16f5e:  movs r1, #0                       
  16f60:  b #0x16f92                        -> 0x16f92 (вне списка функций)
  16f62:  ldr r0, [r4]                      
  16f64:  ldr.w r0, [ip, r0, lsl #2]        
  16f68:  cmp r0, r5                        
  16f6a:  ble #0x16f90                      
  16f6c:  ldr r0, [r4]                      
  16f6e:  lsrs r2, r0, #1                   
  16f70:  movs r1, #0                       
  16f72:  ldr r3, [r4]                      
  16f74:  b #0x16f88                        -> 0x16f88 (вне списка функций)
  16f76:  ldr.w r0, [ip, r2, lsl #2]        
  16f7a:  cmp r0, r5                        
  16f7c:  ble #0x16f82                      
  16f7e:  mov r3, r2                        
  16f80:  b #0x16f84                        -> 0x16f84 (вне списка функций)
  16f82:  mov r1, r2                        
  16f84:  adds r0, r3, r1                   
  16f86:  lsrs r2, r0, #1                   
  16f88:  subs r0, r3, r1                   
  16f8a:  cmp r0, #1                        
  16f8c:  bhi #0x16f76                      
  16f8e:  b #0x16f92                        -> 0x16f92 (вне списка функций)
  16f90:  ldr r1, [r4]                      
  16f92:  str r1, [sp]                      
  16f94:  ldrsh.w r0, [r7]                  
  16f98:  cmp r0, r6                        
  16f9a:  blt #0x16fa0                      
  16f9c:  movs r1, #0                       
  16f9e:  b #0x16fd0                        -> 0x16fd0 (вне списка функций)
  16fa0:  ldr r0, [r4, #4]                  
  16fa2:  ldrsh.w r0, [r7, r0, lsl #1]      
  16fa6:  cmp r0, r6                        
  16fa8:  ble #0x16fce                      
  16faa:  ldr r0, [r4, #4]                  
  16fac:  lsrs r2, r0, #1                   
  16fae:  movs r1, #0                       
  16fb0:  ldr r3, [r4, #4]                  
  16fb2:  b #0x16fc6                        -> 0x16fc6 (вне списка функций)
  16fb4:  ldrsh.w r0, [r7, r2, lsl #1]      
  16fb8:  cmp r0, r6                        
  16fba:  ble #0x16fc0                      
  16fbc:  mov r3, r2                        
  16fbe:  b #0x16fc2                        -> 0x16fc2 (вне списка функций)
  16fc0:  mov r1, r2                        
  16fc2:  adds r0, r3, r1                   
  16fc4:  lsrs r2, r0, #1                   
  16fc6:  subs r0, r3, r1                   
  16fc8:  cmp r0, #1                        
  16fca:  bhi #0x16fb4                      
  16fcc:  b #0x16fd0                        -> 0x16fd0 (вне списка функций)
  16fce:  ldr r1, [r4, #4]                  
  16fd0:  ldr r0, [sp]                      
  16fd2:  mla r0, r1, sb, r0                
  16fd6:  ldrb.w r0, [r8, r0]               
  16fda:  pop.w {r2, r3, r4, r5, r6, r7, r8, sb, pc}
```
