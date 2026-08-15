# func_0x09dce

| | |
|---|---|
| offset в файле | `0x09dce` |
| vaddr (база 0x01800000) | `0x01809dce` |
 | размер кода | 250 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005ec — RAM (r3)

## Вызовы (callees)

- 0x01619118 (bl, вне списка функций)
- 0x01809df8 (b, вне списка функций)
- 0x01809e0c (b, вне списка функций)
- 0x01809e36 (b, вне списка функций)
- 0x01809e7e (b, вне списка функций)
- 0x01809ea0 (b, вне списка функций)
- 0x01809ebc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x09ec8` (bl @0x01809eea)
- `func_0x09f4c` (bl @0x01809f6e)

## Дизассембляция

```asm
  01809dce:  push.w {r0, r1, r2, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01809dd2:  mov sb, r0                        
  01809dd4:  adr r0, #0x170                    
  01809dd6:  movs r5, #3                       
  01809dd8:  sub sp, #8                        
  01809dda:  movs r1, #0                       
  01809ddc:  ldr r0, [r0]                      
  01809dde:  mov r6, r2                        
  01809de0:  mov sl, r1                        
  01809de2:  mov r4, r1                        
  01809de4:  str r0, [sp]                      
  01809de6:  b #0x1809ebc                      -> 0x09ebc (вне списка функций)
  01809de8:  cbz r4, #0x1809e04                
  01809dea:  ldrb.w r0, [sb, r5]               
  01809dee:  and r2, r0, #3                    
  01809df2:  add.w r0, r2, sl                  
  01809df6:  uxtb r3, r0                       
  01809df8:  and r2, r3, #0x7f                 
  01809dfc:  cmp r4, #0x14                     
  01809dfe:  bhs #0x1809e0a                    
  01809e00:  movs r7, #3                       
  01809e02:  b #0x1809e0c                      -> 0x09e0c (вне списка функций)
  01809e04:  ldrb.w r3, [sb]                   
  01809e08:  b #0x1809df8                      -> 0x09df8 (вне списка функций)
  01809e0a:  movs r7, #1                       
  01809e0c:  movs r0, #0                       
  01809e0e:  mov sl, sp                        
  01809e10:  b #0x1809e36                      -> 0x09e36 (вне списка функций)
  01809e12:  lsl.w ip, r0, #1                  
  01809e16:  ldrb.w r8, [sb, r5]               
  01809e1a:  add.w ip, ip, #2                  
  01809e1e:  lsr.w r8, r8, ip                  
  01809e22:  and ip, r8, #3                    
  01809e26:  add r1, ip                        
  01809e28:  ldrb.w ip, [sl, r0]               
  01809e2c:  lsl.w ip, r1, ip                  
  01809e30:  orr.w r2, ip, r2                  
  01809e34:  adds r0, r0, #1                   
  01809e36:  cmp r0, r7                        
  01809e38:  blo #0x1809e12                    
  01809e3a:  lsrs r0, r2, #0x10                
  01809e3c:  add.w sl, r3, r1                  
  01809e40:  uxth r3, r2                       
  01809e42:  str r0, [sp, #4]                  
  01809e44:  cmp r4, #0x14                     
  01809e46:  bhs #0x1809e6c                    
  01809e48:  movs r1, #5                       
  01809e4a:  udiv r2, r4, r1                   
  01809e4e:  add r2, r6                        
  01809e50:  adds r2, #0x14                    
  01809e52:  and fp, r2, #0xff                 
  01809e56:  udiv r2, r4, r1                   
  01809e5a:  mls r1, r1, r2, r4                
  01809e5e:  adds r0, r6, r4                   
  01809e60:  add.w r7, r1, r1, lsl #1          
  01809e64:  adds r1, r7, #2                   
  01809e66:  uxtb r0, r0                       
  01809e68:  uxtb r1, r1                       
  01809e6a:  b #0x1809e7e                      -> 0x09e7e (вне списка функций)
  01809e6c:  add.w r1, r6, #0x19               
  01809e70:  add.w r0, r6, #0x18               
  01809e74:  and fp, r1, #0xff                 
  01809e78:  movs r7, #0                       
  01809e7a:  uxtb r0, r0                       
  01809e7c:  movs r1, #2                       
  01809e7e:  mov r8, r1                        
  01809e80:  mov r2, r3                        
  01809e82:  movs r1, #0                       
  01809e84:  bl #0x1619118                     
  01809e88:  mov r0, r7                        
  01809e8a:  mov r3, r8                        
  01809e8c:  movs r1, #0                       
  01809e8e:  mov.w ip, #1                      
  01809e92:  b #0x1809ea0                      -> 0x09ea0 (вне списка функций)
  01809e94:  lsl.w r2, ip, r0                  
  01809e98:  orrs r2, r1                       
  01809e9a:  adds r0, r0, #1                   
  01809e9c:  uxth r1, r2                       
  01809e9e:  uxtb r0, r0                       
  01809ea0:  cmp r0, r3                        
  01809ea2:  bls #0x1809e94                    
  01809ea4:  ldr r0, [sp, #4]                  
  01809ea6:  ldr r3, [pc, #0x78]               (RAM)
  01809ea8:  lsls r0, r7                       
  01809eaa:  uxth r2, r0                       
  01809eac:  ldr r3, [r3]                      
  01809eae:  mov r0, fp                        
  01809eb0:  blx r3                            
  01809eb2:  adds r5, r5, #1                   
  01809eb4:  movs r1, #0                       
  01809eb6:  adds r4, r4, #1                   
  01809eb8:  uxtb r5, r5                       
  01809eba:  uxtb r4, r4                       
  01809ebc:  ldr r0, [sp, #0xc]                
  01809ebe:  cmp r4, r0                        
  01809ec0:  blo #0x1809de8                    
  01809ec2:  add sp, #0x14                     
  01809ec4:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x09f20 (1 слов) — ВНЕ границ функции ---
  09f20:  .word 0x002005ec  ; RAM
```
