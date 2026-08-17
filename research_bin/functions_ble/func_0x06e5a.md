# func_0x06e5a

| | |
|---|---|
| offset в файле | `0x06e5a` |
| vaddr (база 0x01800000) | `0x01806e5a` |
 | размер кода | 140 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002007b8 — RAM (r1)
- 0x00202044 — RAM (r0)
- 0x00206840 — RAM (r2)
- 0x40051000 — периферия (r6)

## Вызовы (callees)

- 0x01806edc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01806e5a:  push.w {r4, r5, r6, r7, r8, lr}   
  01806e5e:  sub.w r0, r1, #8                  
  01806e62:  uxtb r7, r0                       
  01806e64:  ldr r0, [pc, #0x19c]              (RAM)
  01806e66:  mov r4, r1                        
  01806e68:  add.w r1, r0, r4, lsl #2          
  01806e6c:  ldr r6, [pc, #0x198]              (периферия)
  01806e6e:  ldr.w r5, [r1, #0x210]            
  01806e72:  ldr r1, [r5]                      
  01806e74:  ubfx r1, r1, #0x1b, #2            
  01806e78:  add r0, r1                        
  01806e7a:  ldrb.w r0, [r0, #0x1f6]           
  01806e7e:  cmp r0, r4                        
  01806e80:  bne #0x1806eb0                    
  01806e82:  ldr r1, [pc, #0x190]              (RAM)
  01806e84:  mov r0, r4                        
  01806e86:  ldr r1, [r1]                      
  01806e88:  blx r1                            
  01806e8a:  ldrh.w r1, [r5, #0xac]            
  01806e8e:  subs r2, r1, #2                   
  01806e90:  uxth r2, r2                       
  01806e92:  cmp r2, r0                        
  01806e94:  beq #0x1806e9e                    
  01806e96:  subs r1, r1, #1                   
  01806e98:  uxth r1, r1                       
  01806e9a:  cmp r1, r0                        
  01806e9c:  bne #0x1806eb0                    
  01806e9e:  ldrh r0, [r6, #0x22]              
  01806ea0:  lsrs r1, r0, #8                   
  01806ea2:  beq #0x1806eb0                    
  01806ea4:  ldr r2, [pc, #0x164]              (RAM)
  01806ea6:  lsrs r1, r0, #8                   
  01806ea8:  adds r2, r2, #3                   
  01806eaa:  uxtb r0, r0                       
  01806eac:  strb r1, [r2, r7]                 
  01806eae:  strh r0, [r6, #0x22]              
  01806eb0:  cmp r4, #8                        
  01806eb2:  bhs #0x1806ee0                    
  01806eb4:  ldrh.w r0, [r6, #0x100]           
  01806eb8:  movs r1, #1                       
  01806eba:  ldr r2, [pc, #0x150]              (RAM)
  01806ebc:  lsls r1, r4                       
  01806ebe:  subs r2, #8                       
  01806ec0:  ldrb r2, [r2]                     
  01806ec2:  tst r1, r2                        
  01806ec4:  lsl.w r1, r0, #0x17               
  01806ec8:  beq #0x1806ed4                    
  01806eca:  cmp r1, #0                        
  01806ecc:  blt #0x1806ee0                    
  01806ece:  orr r0, r0, #0x100                
  01806ed2:  b #0x1806edc                      -> 0x06edc (вне списка функций)
  01806ed4:  cmp r1, #0                        
  01806ed6:  bge #0x1806ee0                    
  01806ed8:  bic r0, r0, #0x100                
  01806edc:  strh.w r0, [r6, #0x100]           
  01806ee0:  movs r0, #0                       
  01806ee2:  pop.w {r4, r5, r6, r7, r8, pc}    
  ; --- literal-пул @0x07004 (3 слов) — ВНЕ границ функции ---
  07004:  .word 0x00202044  ; RAM
  07008:  .word 0x40051000  ; периферия
  0700c:  .word 0x00206840  ; RAM
  ; --- literal-пул @0x07014 (1 слов) — ВНЕ границ функции ---
  07014:  .word 0x002007b8  ; RAM
```
