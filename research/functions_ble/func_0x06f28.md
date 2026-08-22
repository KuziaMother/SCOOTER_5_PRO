# func_0x06f28

| | |
|---|---|
| offset в файле | `0x06f28` |
| vaddr (база 0x01800000) | `0x01806f28` |
 | размер кода | 280 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00201ce4 — RAM (r0)
- 0x00202044 — RAM (fp)
- 0x0020672e — RAM (r0)
- 0x00206840 — RAM (sl)
- 0x21600002 — прочее (r0)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x01620956 (bl, вне списка функций)
- 0x01806cac (b, вне списка функций)
- `func_0x06dca` (0x01806dca, bl)
- `func_0x06ee6` (0x01806ee6, bl)
- 0x01806fba (b, вне списка функций)
- 0x01807020 (b, вне списка функций)
- 0x0180935c (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01806f28:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, lr}
  01806f2c:  ldr.w fp, [pc, #0xd4]             (RAM)
  01806f30:  mov r4, r0                        
  01806f32:  add.w sb, fp, r4, lsl #2          
  01806f36:  ldr.w sl, [pc, #0xd4]             (RAM)
  01806f3a:  ldr.w r5, [sb, #0x210]            
  01806f3e:  mov.w r6, #1                      
  01806f42:  sub.w sl, sl, #8                  
  01806f46:  ldrb.w r0, [r5, #0x8f]            
  01806f4a:  lsls r0, r0, #0x1a                
  01806f4c:  lsl.w r6, r6, r4                  
  01806f50:  bpl #0x1806fc0                    
  01806f52:  ldrb r0, [r5, #0xc]               
  01806f54:  lsls r0, r0, #0x1a                
  01806f56:  bpl #0x1806fc0                    
  01806f58:  ldr r0, [pc, #0xbc]               (RAM)
  01806f5a:  ldr.w r0, [r0, r4, lsl #2]        
  01806f5e:  ldrb r0, [r0, #7]                 
  01806f60:  cbnz r0, #0x1806fc0               
  01806f62:  ldr r0, [pc, #0xb8]               (RAM)
  01806f64:  ldrb r0, [r0, r4]                 
  01806f66:  cmp r0, #0xff                     
  01806f68:  beq #0x1806fc0                    
  01806f6a:  ldr r1, [r5]                      
  01806f6c:  lsls r1, r1, #7                   
  01806f6e:  bmi #0x1806f7e                    
  01806f70:  movs r2, #0                       
  01806f72:  movw r1, #0x43f                   
  01806f76:  ldr r0, [pc, #0x98]               
  01806f78:  bl #0x15f5b92                     
  01806f7c:  b #0x1806fba                      -> 0x06fba (вне списка функций)
  01806f7e:  movs r7, #0                       
  01806f80:  mov r8, r0                        
  01806f82:  bfi r7, r4, #0, #8                
  01806f86:  bfi r7, r8, #8, #8                
  01806f8a:  bl #0x180935c                     -> 0x0935c (вне списка функций)
  01806f8e:  mov ip, r0                        
  01806f90:  mov r0, r7                        
  01806f92:  bl #0x1806ee6                     -> func_0x06ee6
  01806f96:  cmp.w ip, #0                      
  01806f9a:  beq #0x1806fba                    
  01806f9c:  ldr.w r0, [sb, #0x210]            
  01806fa0:  ldr r0, [r0]                      
  01806fa2:  lsls r0, r0, #5                   
  01806fa4:  bpl #0x1806fb2                    
  01806fa6:  ldrb.w r2, [sl]                   
  01806faa:  orr.w r0, r6, r2                  
  01806fae:  strb.w r0, [sl]                   
  01806fb2:  mov r1, r8                        
  01806fb4:  mov r0, r4                        
  01806fb6:  bl #0x1620956                     
  01806fba:  ldr r0, [pc, #0x60]               (RAM)
  01806fbc:  movs r1, #0xff                    
  01806fbe:  strb r1, [r0, r4]                 
  01806fc0:  ldrh.w r0, [sl, #6]               
  01806fc4:  tst r6, r0                        
  01806fc6:  bne #0x1806fd8                    
  01806fc8:  ldrb r1, [r5, #0xd]               
  01806fca:  lsls r3, r1, #0x1d                
  01806fcc:  bpl #0x1806fd8                    
  01806fce:  lsls r1, r1, #0x1f                
  01806fd0:  bne #0x1806fd8                    
  01806fd2:  orrs r0, r6                       
  01806fd4:  strh.w r0, [sl, #6]               
  01806fd8:  ldr r0, [r5]                      
  01806fda:  lsls r1, r0, #5                   
  01806fdc:  bmi #0x180703c                    
  01806fde:  ldr r3, [pc, #0x3c]               (RAM)
  01806fe0:  subs r3, r3, #2                   
  01806fe2:  ldrh r1, [r3]                     
  01806fe4:  tst r6, r1                        
  01806fe6:  bne #0x1806ff6                    
  01806fe8:  ldrb r2, [r5, #0xd]               
  01806fea:  lsls r7, r2, #0x1d                
  01806fec:  bpl #0x1806ff6                    
  01806fee:  lsls r2, r2, #0x1f                
  01806ff0:  bne #0x1806ff6                    
  01806ff2:  orrs r6, r1                       
  01806ff4:  strh r6, [r3]                     
  01806ff6:  sub.w r1, r4, #8                  
  01806ffa:  uxth r1, r1                       
  01806ffc:  ldr r2, [pc, #0xc]                (RAM)
  01806ffe:  b #0x1807020                      -> 0x07020 (вне списка функций)
  01807000:  cmp r2, #0xd4                     
  01807002:  movs r0, r4                       
  01807004:  movs r0, #0x44                    
  01807006:  movs r0, r4                       
  01807008:  asrs r0, r0, #0x20                
  0180700a:  ands r5, r0                       
  0180700c:  ldr r0, [r0, #4]                  
  0180700e:  movs r0, r4                       
  01807010:  movs r2, r0                       
  01807012:  movs r1, #0x60                    
  01807014:  lsls r0, r7, #0x1e                
  01807016:  movs r0, r4                       
  01807018:  adds r4, r4, #3                   
  0180701a:  movs r0, r4                       
  0180701c:  str r6, [r5, #0x70]               
  0180701e:  movs r0, r4                       
  01807020:  ldrb r1, [r2, r1]                 
  01807022:  cbz r1, #0x180703c                
  01807024:  ubfx r1, r0, #0x1b, #2            
  01807028:  add.w r0, r1, fp                  
  0180702c:  ldrb.w r0, [r0, #0x1f6]           
  01807030:  cmp r0, #0xb                      
  01807032:  bne #0x180703c                    
  01807034:  mov r1, r5                        
  01807036:  mov r0, r4                        
  01807038:  bl #0x1806dca                     -> func_0x06dca
  0180703c:  movs r0, #0                       
  0180703e:  b #0x1806cac                      -> 0x06cac (вне списка функций)
  ; --- literal-пул @0x07004 (1 слов) ---
  07004:  .word 0x00202044  ; RAM
  ; --- literal-пул @0x0700c (2 слов) ---
  0700c:  .word 0x00206840  ; RAM
  07010:  .word 0x21600002
  ; --- literal-пул @0x07018 (2 слов) ---
  07018:  .word 0x00201ce4  ; RAM
  0701c:  .word 0x0020672e  ; RAM
```
