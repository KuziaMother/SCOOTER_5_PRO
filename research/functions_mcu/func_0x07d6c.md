# func_0x07d6c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007d6c) | `0x00007d6c` |
| размер кода | 148 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08003000 — flash-mirror @0x03000 (r1)
- 0x0801ffff — flash-mirror @0x1ffff (r2)

## Вызовы (callees)

- `func_0x01218` (0x00001218, bl)
- 0x0123a (bl, вне списка функций)
- 0x07db0 (b, вне списка функций)
- `func_0x07e70` (0x00007e70, bl)
- `func_0x16040` (0x00016040, bl)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x07dae..0x07dba` (12 Б); цели из: 0x07d90, 0x07da6
- `0x07dba..0x07dc2` (8 Б); цели из: 0x07dac
- `0x07dc2..0x07e00` (62 Б); цели из: 0x07dbc

## Дизассембляция

```asm
  07d6c:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  07d70:  vpush {d8, d9}                    
  07d74:  sub sp, #0xc                      
  07d76:  mov r5, r0                        
  07d78:  mov r6, r1                        
  07d7a:  mov r4, r2                        
  07d7c:  mov.w r8, #0                      
  07d80:  movs r0, #0                       
  07d82:  str r0, [sp, #8]                  
  07d84:  movs r7, #0                       
  07d86:  mov sb, r0                        
  07d88:  str r0, [sp, #4]                  
  07d8a:  cbz r4, #0x7dae                   
  07d8c:  cmp.w r4, #0x800                  
  07d90:  bgt #0x7dae                       
  07d92:  asrs r1, r4, #0x1f                
  07d94:  add.w r1, r4, r1, lsr #30         
  07d98:  asrs r1, r1, #2                   
  07d9a:  sub.w r1, r4, r1, lsl #2          
  07d9e:  cbnz r1, #0x7dae                  
  07da0:  adds r1, r6, r4                   
  07da2:  ldr r2, [pc, #0xc4]               -> flash-mirror @0x1ffff
  07da4:  cmp r1, r2                        
  07da6:  bhs #0x7dae                       
  07da8:  ldr r1, [pc, #0xc0]               -> flash-mirror @0x03000
  07daa:  cmp r6, r1                        
  07dac:  bhs #0x7dba                       
  07dae:  movs r0, #0                       
  07db0:  add sp, #0xc                      
  07db2:  vpop {d8, d9}                     
  07db6:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
  07dba:  cmp r5, r6                        
  07dbc:  bne #0x7dc2                       
  07dbe:  movs r0, #1                       
  07dc0:  b #0x7db0                         -> 0x07db0 (вне списка функций)
  07dc2:  asrs r1, r4, #0x1f                
  07dc4:  add.w r1, r4, r1, lsr #21         
  07dc8:  asrs r0, r1, #0xb                 
  07dca:  bl #0x1218                        -> func_0x01218
  07dce:  vmov d9, r0, r1                   
  07dd2:  vmov.f32 s0, s18                  
  07dd6:  vmov.f32 s1, s19                  
  07dda:  bl #0x16040                       -> func_0x16040
  07dde:  vmov.f32 s16, s0                  
  07de2:  vmov.f32 s17, s1                  
  07de6:  vmov r0, r1, d8                   
  07dea:  bl #0x123a                        -> 0x0123a (вне списка функций)
  07dee:  uxth.w fp, r0                     
  07df2:  mov r1, fp                        
  07df4:  mov r0, r6                        
  07df6:  bl #0x7e70                        -> func_0x07e70
  07dfa:  cbnz r0, #0x7e00                  
  07dfc:  movs r0, #0                       
  07dfe:  b #0x7db0                         -> 0x07db0 (вне списка функций)
  ; --- literal-пул @0x07e68 (2 слов) — ВНЕ границ функции ---
  07e68:  .word 0x0801ffff  ; flash-mirror @0x1ffff
  07e6c:  .word 0x08003000  ; flash-mirror @0x03000
```
