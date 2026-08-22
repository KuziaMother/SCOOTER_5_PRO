# func_0x07ac0

| | |
|---|---|
| offset в файле | `0x07ac0` |
| vaddr (база 0x01800000) | `0x01807ac0` |
 | размер кода | 272 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0020092e — RAM (lr)
- 0x00201df8 — RAM (ip)
- 0x00202044 — RAM (r5)

## Вызовы (callees)

- 0x01807b86 (b, вне списка функций)
- 0x01807b8a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01807ac0:  push {r4, r5, r6, r7, lr}         
  01807ac2:  ldrb r2, [r0, #5]                 
  01807ac4:  ldrb r1, [r0, #4]                 
  01807ac6:  lsrs r3, r2, #5                   
  01807ac8:  bne #0x1807b5e                    
  01807aca:  ldr r5, [pc, #0x1f8]              (RAM)
  01807acc:  cmp r1, #1                        
  01807ace:  bne #0x1807ae8                    
  01807ad0:  movs r1, #0                       
  01807ad2:  mov r3, r1                        
  01807ad4:  add.w r4, r5, r1, lsl #4          
  01807ad8:  adds r1, r1, #1                   
  01807ada:  uxtb r1, r1                       
  01807adc:  strh.w r3, [r4, #0x2b6]           
  01807ae0:  cmp r1, #0xe                      
  01807ae2:  blo #0x1807ad4                    
  01807ae4:  cmp r2, #0                        
  01807ae6:  beq #0x1807bcc                    
  01807ae8:  lsls r1, r2, #0x1f                
  01807aea:  mov.w r6, #0x400                  
  01807aee:  beq #0x1807b1c                    
  01807af0:  ldrb r3, [r0, #6]                 
  01807af2:  cmp r3, #0xa                      
  01807af4:  bls #0x1807af8                    
  01807af6:  movs r3, #0xa                     
  01807af8:  movs r1, #0                       
  01807afa:  add.w r3, r3, r3, lsl #2          
  01807afe:  lsls r4, r3, #1                   
  01807b00:  add.w r3, r5, r1, lsl #4          
  01807b04:  ldrsh.w r7, [r3, #0x2b4]          
  01807b08:  cmp r7, r6                        
  01807b0a:  beq #0x1807b10                    
  01807b0c:  strh.w r4, [r3, #0x2b4]           
  01807b10:  adds r1, r1, #1                   
  01807b12:  strh.w r4, [r3, #0x2b6]           
  01807b16:  cmp r1, #0xb                      
  01807b18:  blt #0x1807b00                    
  01807b1a:  b #0x1807b8a                      -> 0x07b8a (вне списка функций)
  01807b1c:  lsls r1, r2, #0x1e                
  01807b1e:  bpl #0x1807b8a                    
  01807b20:  ldrb r7, [r0, #0xa]               
  01807b22:  ldrb r3, [r0, #2]                 
  01807b24:  add.w r1, r7, r7, lsl #1          
  01807b28:  adds r1, #8                       
  01807b2a:  cmp r3, r1                        
  01807b2c:  bne #0x1807b5e                    
  01807b2e:  movs r1, #0                       
  01807b30:  b #0x1807b86                      -> 0x07b86 (вне списка функций)
  01807b32:  ldr.w ip, [pc, #0x1b8]            (RAM)
  01807b36:  ldr.w lr, [pc, #0x1b8]            (RAM)
  01807b3a:  add.w r3, r1, r1, lsl #1          
  01807b3e:  add r3, r0                        
  01807b40:  ldrb.w ip, [ip]                   
  01807b44:  ldrb.w lr, [lr]                   
  01807b48:  ldrb r4, [r3, #0xb]               
  01807b4a:  add ip, lr                        
  01807b4c:  sub.w r4, r4, ip                  
  01807b50:  subs r4, r4, #2                   
  01807b52:  ldrb r3, [r3, #0xd]               
  01807b54:  uxtb r4, r4                       
  01807b56:  cmp r4, #0xb                      
  01807b58:  bhs #0x1807b5e                    
  01807b5a:  cmp r3, #0xa                      
  01807b5c:  bls #0x1807b62                    
  01807b5e:  movs r0, #0x12                    
  01807b60:  pop {r4, r5, r6, r7, pc}          
  01807b62:  add.w r4, r5, r4, lsl #4          
  01807b66:  ldrsh.w ip, [r4, #0x2b4]          
  01807b6a:  cmp ip, r6                        
  01807b6c:  beq #0x1807b7a                    
  01807b6e:  add.w ip, r3, r3, lsl #2          
  01807b72:  lsl.w ip, ip, #1                  
  01807b76:  strh.w ip, [r4, #0x2b4]           
  01807b7a:  add.w r3, r3, r3, lsl #2          
  01807b7e:  lsls r3, r3, #1                   
  01807b80:  strh.w r3, [r4, #0x2b6]           
  01807b84:  adds r1, r1, #1                   
  01807b86:  cmp r1, r7                        
  01807b88:  blt #0x1807b32                    
  01807b8a:  lsls r1, r2, #0x1d                
  01807b8c:  bpl #0x1807ba0                    
  01807b8e:  ldrb r1, [r0, #7]                 
  01807b90:  cmp r1, #0xa                      
  01807b92:  bls #0x1807b96                    
  01807b94:  movs r1, #0xa                     
  01807b96:  add.w r1, r1, r1, lsl #2          
  01807b9a:  lsls r1, r1, #1                   
  01807b9c:  strh.w r1, [r5, #0x366]           
  01807ba0:  lsls r1, r2, #0x1c                
  01807ba2:  bpl #0x1807bb6                    
  01807ba4:  ldrb r1, [r0, #8]                 
  01807ba6:  cmp r1, #0xa                      
  01807ba8:  bls #0x1807bac                    
  01807baa:  movs r1, #0xa                     
  01807bac:  add.w r1, r1, r1, lsl #2          
  01807bb0:  lsls r1, r1, #1                   
  01807bb2:  strh.w r1, [r5, #0x376]           
  01807bb6:  lsls r1, r2, #0x1b                
  01807bb8:  bpl #0x1807bcc                    
  01807bba:  ldrb r0, [r0, #9]                 
  01807bbc:  cmp r0, #0xa                      
  01807bbe:  bls #0x1807bc2                    
  01807bc0:  movs r0, #0xa                     
  01807bc2:  add.w r0, r0, r0, lsl #2          
  01807bc6:  lsls r0, r0, #1                   
  01807bc8:  strh.w r0, [r5, #0x386]           
  01807bcc:  movs r0, #0                       
  01807bce:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x07cc4 (1 слов) — ВНЕ границ функции ---
  07cc4:  .word 0x00202044  ; RAM
  ; --- literal-пул @0x07cec (2 слов) — ВНЕ границ функции ---
  07cec:  .word 0x00201df8  ; RAM
  07cf0:  .word 0x0020092e  ; RAM
```
