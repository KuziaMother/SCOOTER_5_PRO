# func_0x08a72

| | |
|---|---|
| offset в файле | `0x08a72` |
| vaddr (база 0x01800000) | `0x01808a72` |
 | размер кода | 250 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00201c54 — RAM (r0)
- 0x00202044 — RAM (r0)
- 0x21600002 — прочее (r0)
- 0x40051000 — периферия (r1)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x0161484c (bl, вне списка функций)
- 0x01614866 (bl, вне списка функций)
- 0x016158b2 (bl, вне списка функций)
- 0x01620876 (bl, вне списка функций)
- `func_0x067a8` (0x018067a8, bl)
- 0x01808a90 (b, вне списка функций)
- 0x01808ae4 (b, вне списка функций)
- 0x01808b1c (b, вне списка функций)
- 0x01808b3a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01808a72:  push.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01808a76:  mov r7, r0                        
  01808a78:  movs r0, #0                       
  01808a7a:  bfi r0, r7, #0, #8                
  01808a7e:  mov sl, r0                        
  01808a80:  bl #0x161484c                     
  01808a84:  mov fp, r0                        
  01808a86:  ldr r0, [pc, #0x3a0]              (RAM)
  01808a88:  ldrb r0, [r0, #7]                 
  01808a8a:  cbz r0, #0x1808adc                
  01808a8c:  mov.w ip, #0                      
  01808a90:  mov r1, sl                        
  01808a92:  movs r0, #0                       
  01808a94:  bl #0x18067a8                     -> func_0x067a8
  01808a98:  cmp.w ip, #0                      
  01808a9c:  beq #0x1808b40                    
  01808a9e:  ldr r0, [pc, #0x384]              (RAM)
  01808aa0:  add.w r0, r0, r7, lsl #2          
  01808aa4:  ldr.w sb, [r0, #0x210]            
  01808aa8:  ldr.w r0, [sb]                    
  01808aac:  lsls r0, r0, #5                   
  01808aae:  bmi #0x1808b3a                    
  01808ab0:  sub.w r0, r7, #8                  
  01808ab4:  uxtb r0, r0                       
  01808ab6:  movw r1, #0x232                   
  01808aba:  add.w r6, r1, r0, lsl #1          
  01808abe:  adds r1, r1, #6                   
  01808ac0:  add.w r5, r1, r0, lsl #1          
  01808ac4:  bl #0x16158b2                     
  01808ac8:  ldr r1, [pc, #0x360]              (периферия)
  01808aca:  ubfx r4, r0, #1, #0x12            
  01808ace:  adds r2, r6, r1                   
  01808ad0:  ldrh r0, [r2]                     
  01808ad2:  add.w ip, r5, r1                  
  01808ad6:  ldrh.w r3, [ip]                   
  01808ada:  b #0x1808ae4                      -> 0x08ae4 (вне списка функций)
  01808adc:  mov.w ip, #1                      
  01808ae0:  b #0x1808a90                      -> 0x08a90 (вне списка функций)
  01808ae2:  mov r0, r1                        
  01808ae4:  ldrh r1, [r2]                     
  01808ae6:  cmp r1, r0                        
  01808ae8:  bne #0x1808ae2                    
  01808aea:  ubfx r1, r3, #0xa, #4             
  01808aee:  mov r6, r0                        
  01808af0:  bfi r6, r1, #0xe, #0x12           
  01808af4:  subs r5, r6, r4                   
  01808af6:  lsr.w r8, r0, #0xe                
  01808afa:  cmp.w r8, #1                      
  01808afe:  beq #0x1808b08                    
  01808b00:  cmp.w r8, #3                      
  01808b04:  beq #0x1808b10                    
  01808b06:  b #0x1808b3a                      -> 0x08b3a (вне списка функций)
  01808b08:  tst.w r5, #0x20000                
  01808b0c:  bne #0x1808b20                    
  01808b0e:  b #0x1808b3a                      -> 0x08b3a (вне списка функций)
  01808b10:  cmp r5, #0                        
  01808b12:  ble #0x1808b18                    
  01808b14:  mov r1, r5                        
  01808b16:  b #0x1808b1c                      -> 0x08b1c (вне списка функций)
  01808b18:  mvns r1, r5                       
  01808b1a:  adds r1, r1, #1                   
  01808b1c:  cmp r1, #1                        
  01808b1e:  ble #0x1808b3a                    
  01808b20:  adds r4, r4, #2                   
  01808b22:  lsrs r1, r4, #0xe                 
  01808b24:  bfi r0, r4, #0, #0xe              
  01808b28:  bfi r3, r1, #0xa, #4              
  01808b2c:  bic r0, r0, #0xc000               
  01808b30:  strh.w r3, [ip]                   
  01808b34:  add.w r0, r0, #0x4000             
  01808b38:  strh r0, [r2]                     
  01808b3a:  mov r0, r7                        
  01808b3c:  bl #0x1620876                     
  01808b40:  mov r0, fp                        
  01808b42:  bl #0x1614866                     
  01808b46:  ldr.w r0, [sb]                    
  01808b4a:  lsls r0, r0, #5                   
  01808b4c:  bmi #0x1808b62                    
  01808b4e:  strd r4, r6, [sp]                 
  01808b52:  mov r3, r8                        
  01808b54:  movs r2, #4                       
  01808b56:  movw r1, #0x45b                   
  01808b5a:  ldr r0, [pc, #0x2d4]              
  01808b5c:  str r5, [sp, #8]                  
  01808b5e:  bl #0x15f5b92                     
  01808b62:  pop.w {r1, r2, r3, r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01808b66:  movs r0, #2                       
  01808b68:  b.w #0x162dad8                    
  ; --- literal-пул @0x08e24 (4 слов) — ВНЕ границ функции ---
  08e24:  .word 0x00202044  ; RAM
  08e28:  .word 0x00201c54  ; RAM
  08e2c:  .word 0x40051000  ; периферия
  08e30:  .word 0x21600002
```
