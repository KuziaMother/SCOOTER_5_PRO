# func_0x10cdc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080010cdc) | `0x00010cdc` |
| размер кода | 152 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00f42400 — прочее (r4)

## Вызовы (callees)

- `func_0x0c518` (0x0000c518, bl)
- `func_0x0c8dc` (0x0000c8dc, bl)
- 0x10d2a (b, вне списка функций)
- 0x10d34 (b, вне списка функций)
- 0x10d84 (b, вне списка функций)
- 0x10e10 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x030e0` (bl @0x000030ec)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x10d02..0x10d1a` (24 Б); цели из: 0x10cf8
- `0x10d1a..0x10d20` (6 Б); цели из: 0x10d08
- `0x10d20..0x10d2a` (10 Б); цели из: 0x10d0c
- `0x10d2a..0x10d34` (10 Б); цели из: 0x10d12
- `0x10d34..0x10d46` (18 Б); цели из: 0x10d10, 0x10d18, 0x10d1e, 0x10d28
- `0x10d46..0x10d56` (16 Б); цели из: 0x10d3a
- `0x10d56..0x10d74` (30 Б); цели из: 0x10d4a

## Дизассембляция

```asm
  10cdc:  push.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  10ce0:  movs r0, #0                       
  10ce2:  str r0, [sp]                      
  10ce4:  mov sl, r0                        
  10ce6:  ldr r4, [pc, #0x120]              
  10ce8:  movs r0, #1                       
  10cea:  bl #0xc518                        -> func_0x0c518
  10cee:  bl #0xc8dc                        -> func_0x0c8dc
  10cf2:  mov fp, r0                        
  10cf4:  cmp.w fp, #1                      
  10cf8:  beq #0x10d02                      
  10cfa:  bl #0x10e10                       -> 0x10e10 (вне списка функций)
  10cfe:  pop.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  10d02:  movs r0, #1                       
  10d04:  cbz r0, #0x10d14                  
  10d06:  cmp r0, #1                        
  10d08:  beq #0x10d1a                      
  10d0a:  cmp r0, #2                        
  10d0c:  beq #0x10d20                      
  10d0e:  cmp r0, #3                        
  10d10:  bne #0x10d34                      
  10d12:  b #0x10d2a                        -> 0x10d2a (вне списка функций)
  10d14:  movs r7, #0                       
  10d16:  mov r8, r7                        
  10d18:  b #0x10d34                        -> 0x10d34 (вне списка функций)
  10d1a:  movs r7, #0                       
  10d1c:  mov r8, r7                        
  10d1e:  b #0x10d34                        -> 0x10d34 (вне списка функций)
  10d20:  mov.w r7, #0x400                  
  10d24:  mov.w r8, #0                      
  10d28:  b #0x10d34                        -> 0x10d34 (вне списка функций)
  10d2a:  mov.w r7, #0x400                  
  10d2e:  mov.w r8, #0                      
  10d32:  nop                               
  10d34:  nop                               
  10d36:  ldr r0, [pc, #0xd0]               
  10d38:  cmp r4, r0                        
  10d3a:  bls #0x10d46                      
  10d3c:  movs r5, #1                       
  10d3e:  movs r6, #0                       
  10d40:  movs r0, #2                       
  10d42:  str r0, [sp]                      
  10d44:  b #0x10d84                        -> 0x10d84 (вне списка функций)
  10d46:  ldr r0, [pc, #0xc0]               
  10d48:  cmp r4, r0                        
  10d4a:  bne #0x10d56                      
  10d4c:  movs r5, #1                       
  10d4e:  movs r6, #0                       
  10d50:  movs r0, #0                       
  10d52:  str r0, [sp]                      
  10d54:  b #0x10d84                        -> 0x10d84 (вне списка функций)
  10d56:  ldr r0, [pc, #0xb0]               
  10d58:  udiv r1, r0, r4                   
  10d5c:  mls r0, r4, r1, r0                
  10d60:  cbnz r0, #0x10d74                 
  10d62:  movs r5, #0                       
  10d64:  ldr r0, [pc, #0xa0]               
  10d66:  udiv r6, r0, r4                   
  10d6a:  subs r0, r6, #2                   
  10d6c:  lsls r6, r0, #0x12                
  10d6e:  movs r0, #0                       
  10d70:  str r0, [sp]                      
  10d72:  b #0x10d84                        -> 0x10d84 (вне списка функций)
  ; --- literal-пул @0x10e08 (1 слов) — ВНЕ границ функции ---
  10e08:  .word 0x00f42400
```
