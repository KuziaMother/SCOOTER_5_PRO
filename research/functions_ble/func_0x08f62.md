# func_0x08f62

| | |
|---|---|
| offset в файле | `0x08f62` |
| vaddr (база 0x01800000) | `0x01808f62` |
 | размер кода | 258 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200ae1 — RAM (r0)
- 0x00202000 — RAM (r3)
- 0x00202a08 — RAM (r1)
- 0x00202ab0 — RAM (r0)
- 0x00fa1b59 — прочее (r0)
- 0x21600002 — прочее (r7)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x015f5fa4 (bl, вне списка функций)
- 0x0161f5fe (bl, вне списка функций)
- 0x0162e97e (bl, вне списка функций)
- 0x0162ee0c (bl, вне списка функций)
- 0x01808fa8 (b, вне списка функций)
- 0x01808ff2 (b, вне списка функций)
- 0x0180901a (b, вне списка функций)
- 0x0180902e (b, вне списка функций)
- 0x01809060 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01808f62:  push.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01808f66:  mov r5, r1                        
  01808f68:  mov sl, r3                        
  01808f6a:  mov r8, r0                        
  01808f6c:  mov r1, r0                        
  01808f6e:  mov fp, r2                        
  01808f70:  ldrh r0, [r0]                     
  01808f72:  ldr r3, [pc, #0x2e8]              (RAM)
  01808f74:  movs r2, #3                       
  01808f76:  add.w r2, r2, r0, lsr #8          
  01808f7a:  bic r2, r2, #1                    
  01808f7e:  ldrb r3, [r3]                     
  01808f80:  ldrd sb, r6, [sp, #0x30]          
  01808f84:  adds r2, r2, #6                   
  01808f86:  add.w r4, r2, r3, lsl #1          
  01808f8a:  cmp r4, r5                        
  01808f8c:  bls #0x1808fac                    
  01808f8e:  lsrs r1, r0, #8                   
  01808f90:  and r3, r0, #0xf                  
  01808f94:  stm.w sp, {r1, r4, r5}            
  01808f98:  ldr r0, [pc, #0x2c4]              
  01808f9a:  movs r2, #4                       
  01808f9c:  movw r1, #0xc8f                   
  01808fa0:  adds r0, #0x7d                    
  01808fa2:  bl #0x15f5fa4                     
  01808fa6:  mov r0, r5                        
  01808fa8:  pop.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
  01808fac:  movs r2, #0x22                    
  01808fae:  cmp.w r2, r0, lsr #8              
  01808fb2:  beq #0x1808fcc                    
  01808fb4:  lsrs r1, r0, #8                   
  01808fb6:  and r3, r0, #0xf                  
  01808fba:  ldr r0, [pc, #0x2a4]              
  01808fbc:  str r1, [sp]                      
  01808fbe:  movs r2, #2                       
  01808fc0:  mov.w r1, #0xc90                  
  01808fc4:  adds r0, #0x85                    
  01808fc6:  bl #0x15f5fa4                     
  01808fca:  b #0x1809060                      -> 0x09060 (вне списка функций)
  01808fcc:  ldrh r3, [r1, #0x18]              
  01808fce:  ldrh r2, [r1, #0x1a]              
  01808fd0:  ldrh r0, [r1, #0x1c]              
  01808fd2:  subs r1, r3, #6                   
  01808fd4:  movw r7, #0xc7b                   
  01808fd8:  cmp r1, r7                        
  01808fda:  bhs #0x1808fec                    
  01808fdc:  cmp.w r0, #0xc80                  
  01808fe0:  bhi #0x1808fec                    
  01808fe2:  cmp r0, #0xa                      
  01808fe4:  blo #0x1808fec                    
  01808fe6:  cmp.w r2, #0x1f4                  
  01808fea:  blo #0x1808ff0                    
  01808fec:  movs r1, #1                       
  01808fee:  b #0x1808ff2                      -> 0x08ff2 (вне списка функций)
  01808ff0:  movs r1, #0                       
  01808ff2:  ldr r7, [pc, #0x280]              
  01808ff4:  cbz r1, #0x1809008                
  01808ff6:  strd r0, r2, [sp]                 
  01808ffa:  movs r2, #3                       
  01808ffc:  movw r1, #0x44d                   
  01809000:  mov r0, r7                        
  01809002:  bl #0x15f5b92                     
  01809006:  b #0x1809060                      -> 0x09060 (вне списка функций)
  01809008:  cbz r6, #0x180900e                
  0180900a:  mov r0, sb                        
  0180900c:  b #0x180901a                      -> 0x0901a (вне списка функций)
  0180900e:  ldr r0, [pc, #0x268]              (RAM)
  01809010:  ldrh r0, [r0]                     
  01809012:  lsls r1, r0, #0x1d                
  01809014:  bpl #0x180902a                    
  01809016:  ubfx r0, r0, #3, #8               
  0180901a:  bl #0x162ee0c                     
  0180901e:  bl #0x162e97e                     
  01809022:  ldr r0, [r0, #0x1c]               
  01809024:  ubfx r3, r0, #0x12, #2            
  01809028:  b #0x180902e                      -> 0x0902e (вне списка функций)
  0180902a:  ldr r0, [pc, #0x250]              (RAM)
  0180902c:  ldrb r3, [r0]                     
  0180902e:  cmp r3, #3                        
  01809030:  bhi #0x1809054                    
  01809032:  ldr r1, [pc, #0x24c]              (RAM)
  01809034:  rsb r0, r3, r3, lsl #3            
  01809038:  add r0, r1                        
  0180903a:  ldrb r0, [r0, #3]                 
  0180903c:  ubfx r0, r0, #1, #1               
  01809040:  cbz r0, #0x1809054                
  01809042:  strd sb, r6, [sp]                 
  01809046:  mov r3, sl                        
  01809048:  mov r2, fp                        
  0180904a:  mov r1, r5                        
  0180904c:  mov r0, r8                        
  0180904e:  bl #0x161f5fe                     
  01809052:  b #0x1808fa8                      -> 0x08fa8 (вне списка функций)
  01809054:  movs r2, #1                       
  01809056:  movw r1, #0x44e                   
  0180905a:  mov r0, r7                        
  0180905c:  bl #0x15f5b92                     
  01809060:  mov r0, r4                        
  01809062:  b #0x1808fa8                      -> 0x08fa8 (вне списка функций)
  ; --- literal-пул @0x0925c (2 слов) — ВНЕ границ функции ---
  0925c:  .word 0x00202000  ; RAM
  09260:  .word 0x00fa1b59
  ; --- literal-пул @0x09274 (4 слов) — ВНЕ границ функции ---
  09274:  .word 0x21600002
  09278:  .word 0x00202ab0  ; RAM
  0927c:  .word 0x00200ae1  ; RAM
  09280:  .word 0x00202a08  ; RAM
```
