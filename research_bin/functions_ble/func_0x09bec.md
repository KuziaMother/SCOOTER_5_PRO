# func_0x09bec

| | |
|---|---|
| offset в файле | `0x09bec` |
| vaddr (база 0x01800000) | `0x01809bec` |
 | размер кода | 190 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00206524 — RAM (r1)
- 0x00206958 — RAM (r3)

## Вызовы (callees)

- 0x01647fa4 (bl, вне списка функций)
- `func_0x09baa` (0x01809baa, bl)
- 0x01809c24 (b, вне списка функций)
- 0x01809c5c (b, вне списка функций)
- 0x01809c9c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x09caa` (bl @0x01809cb2)
- `func_0x09caa` (bl @0x01809ccc)
- `func_0x09caa` (bl @0x01809ce4)
- `func_0x09caa` (bl @0x01809cfa)

## Дизассембляция

```asm
  01809bec:  push {r4, r5, lr}                 
  01809bee:  ldr r3, [pc, #0x314]              (RAM)
  01809bf0:  mov r2, r0                        
  01809bf2:  vpush {d8}                        
  01809bf6:  movs r5, #1                       
  01809bf8:  ldr r3, [r3, #4]                  
  01809bfa:  lsls r5, r2                       
  01809bfc:  sub sp, #0x44                     
  01809bfe:  ldrh.w r4, [r3, #1]               
  01809c02:  vmov.f32 s1, #1.000000e+00        
  01809c06:  tst r4, r5                        
  01809c08:  bne #0x1809c28                    
  01809c0a:  ldrb r4, [r3]                     
  01809c0c:  cbz r4, #0x1809c28                
  01809c0e:  cmp r2, #0xb                      
  01809c10:  beq #0x1809c6a                    
  01809c12:  add r3, r2                        
  01809c14:  ldrb.w r3, [r3, #0x4d]            
  01809c18:  vmov s0, r3                       
  01809c1c:  vcvt.f32.u32 s0, s0               
  01809c20:  vldr s2, [pc, #0x2f0]             
  01809c24:  vdiv.f32 s1, s0, s2               
  01809c28:  vmov s0, r1                       
  01809c2c:  vcvt.f32.u32 s2, s0               
  01809c30:  vldr s3, [pc, #0x2e4]             
  01809c34:  cmp r2, #9                        
  01809c36:  vdiv.f32 s0, s2, s3               
  01809c3a:  vdiv.f32 s16, s0, s1              
  01809c3e:  beq #0x1809c7c                    
  01809c40:  cmp r2, #0xa                      
  01809c42:  beq #0x1809c8e                    
  01809c44:  cmp r2, #0xb                      
  01809c46:  beq #0x1809c96                    
  01809c48:  cmp r0, #0xc                      
  01809c4a:  bne #0x1809c62                    
  01809c4c:  movs r2, #0x40                    
  01809c4e:  ldr r1, [pc, #0x2cc]              (RAM)
  01809c50:  mov r0, sp                        
  01809c52:  bl #0x1647fa4                     
  01809c56:  vmov.f32 s0, s16                  
  01809c5a:  movs r1, #0x10                    
  01809c5c:  mov r0, sp                        
  01809c5e:  bl #0x1809baa                     -> func_0x09baa
  01809c62:  add sp, #0x44                     
  01809c64:  vpop {d8}                         
  01809c68:  pop {r4, r5, pc}                  
  01809c6a:  ldrb.w r3, [r3, #0x58]            
  01809c6e:  vmov.f32 s2, #1.000000e+01        
  01809c72:  vmov s0, r3                       
  01809c76:  vcvt.f32.u32 s0, s0               
  01809c7a:  b #0x1809c24                      -> 0x09c24 (вне списка функций)
  01809c7c:  ldr r0, [pc, #0x29c]              (RAM)
  01809c7e:  vmov.f32 s0, s16                  
  01809c82:  subs r0, #0x50                    
  01809c84:  ldm r0, {r0, r1, r2, r3}          
  01809c86:  stm.w sp, {r0, r1, r2, r3}        
  01809c8a:  movs r1, #4                       
  01809c8c:  b #0x1809c5c                      -> 0x09c5c (вне списка функций)
  01809c8e:  ldr r1, [pc, #0x28c]              (RAM)
  01809c90:  movs r2, #0x20                    
  01809c92:  subs r1, #0x40                    
  01809c94:  b #0x1809c9c                      -> 0x09c9c (вне списка функций)
  01809c96:  ldr r1, [pc, #0x284]              (RAM)
  01809c98:  movs r2, #0x20                    
  01809c9a:  subs r1, #0x20                    
  01809c9c:  mov r0, sp                        
  01809c9e:  bl #0x1647fa4                     
  01809ca2:  vmov.f32 s0, s16                  
  01809ca6:  movs r1, #8                       
  01809ca8:  b #0x1809c5c                      -> 0x09c5c (вне списка функций)
  ; --- literal-пул @0x09f04 (1 слов) — ВНЕ границ функции ---
  09f04:  .word 0x00206958  ; RAM
  ; --- literal-пул @0x09f1c (1 слов) — ВНЕ границ функции ---
  09f1c:  .word 0x00206524  ; RAM
```
