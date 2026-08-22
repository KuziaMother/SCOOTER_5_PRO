# func_0x10ba0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080010ba0) | `0x00010ba0` |
| размер кода | 160 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00f42400 — прочее (r4)

## Вызовы (callees)

- `func_0x0c4cc` (0x0000c4cc, bl)
- `func_0x0c8a4` (0x0000c8a4, bl)
- 0x10bf0 (b, вне списка функций)
- 0x10bfa (b, вне списка функций)
- 0x10c52 (b, вне списка функций)
- 0x10e10 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x030e0` (bl @0x000030f2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x10bc8..0x10be0` (24 Б); цели из: 0x10bbe
- `0x10be0..0x10be6` (6 Б); цели из: 0x10bce
- `0x10be6..0x10bf0` (10 Б); цели из: 0x10bd2
- `0x10bf0..0x10bfa` (10 Б); цели из: 0x10bd8
- `0x10bfa..0x10c0e` (20 Б); цели из: 0x10bd6, 0x10bde, 0x10be4, 0x10bee
- `0x10c0e..0x10c20` (18 Б); цели из: 0x10c00
- `0x10c20..0x10c40` (32 Б); цели из: 0x10c12

## Дизассембляция

```asm
  10ba0:  push.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  10ba4:  movs r0, #0                       
  10ba6:  str r0, [sp]                      
  10ba8:  mov sl, r0                        
  10baa:  ldr r4, [pc, #0x128]              
  10bac:  mov.w r0, #0x10000                
  10bb0:  bl #0xc4cc                        -> func_0x0c4cc
  10bb4:  bl #0xc8a4                        -> func_0x0c8a4
  10bb8:  mov fp, r0                        
  10bba:  cmp.w fp, #1                      
  10bbe:  beq #0x10bc8                      
  10bc0:  bl #0x10e10                       -> 0x10e10 (вне списка функций)
  10bc4:  pop.w {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  10bc8:  movs r0, #1                       
  10bca:  cbz r0, #0x10bda                  
  10bcc:  cmp r0, #1                        
  10bce:  beq #0x10be0                      
  10bd0:  cmp r0, #2                        
  10bd2:  beq #0x10be6                      
  10bd4:  cmp r0, #3                        
  10bd6:  bne #0x10bfa                      
  10bd8:  b #0x10bf0                        -> 0x10bf0 (вне списка функций)
  10bda:  movs r7, #0                       
  10bdc:  mov r8, r7                        
  10bde:  b #0x10bfa                        -> 0x10bfa (вне списка функций)
  10be0:  movs r7, #0                       
  10be2:  mov r8, r7                        
  10be4:  b #0x10bfa                        -> 0x10bfa (вне списка функций)
  10be6:  mov.w r7, #0x400                  
  10bea:  mov.w r8, #0                      
  10bee:  b #0x10bfa                        -> 0x10bfa (вне списка функций)
  10bf0:  mov.w r7, #0x400                  
  10bf4:  mov.w r8, #0                      
  10bf8:  nop                               
  10bfa:  nop                               
  10bfc:  ldr r0, [pc, #0xd4]               
  10bfe:  cmp r4, r0                        
  10c00:  bls #0x10c0e                      
  10c02:  mov.w r5, #0x30000                
  10c06:  movs r6, #0                       
  10c08:  movs r0, #2                       
  10c0a:  str r0, [sp]                      
  10c0c:  b #0x10c52                        -> 0x10c52 (вне списка функций)
  10c0e:  ldr r0, [pc, #0xc4]               
  10c10:  cmp r4, r0                        
  10c12:  bne #0x10c20                      
  10c14:  mov.w r5, #0x30000                
  10c18:  movs r6, #0                       
  10c1a:  movs r0, #0                       
  10c1c:  str r0, [sp]                      
  10c1e:  b #0x10c52                        -> 0x10c52 (вне списка функций)
  10c20:  ldr r0, [pc, #0xb0]               
  10c22:  udiv r1, r0, r4                   
  10c26:  mls r0, r4, r1, r0                
  10c2a:  cbnz r0, #0x10c40                 
  10c2c:  mov.w r5, #0x10000                
  10c30:  ldr r0, [pc, #0xa0]               
  10c32:  udiv r6, r0, r4                   
  10c36:  subs r0, r6, #2                   
  10c38:  lsls r6, r0, #0x12                
  10c3a:  movs r0, #0                       
  10c3c:  str r0, [sp]                      
  10c3e:  b #0x10c52                        -> 0x10c52 (вне списка функций)
  ; --- literal-пул @0x10cd4 (1 слов) — ВНЕ границ функции ---
  10cd4:  .word 0x00f42400
```
