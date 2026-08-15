# func_0x1bb1c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001bb1c) | `0x0001bb1c` |
| размер кода | 562 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00001555 — данные @0x01555 (r6)
- 0x00002aab — данные @0x02aab (r2)
- 0x00005555 — данные @0x05555 (r2)
- 0x00006aab — данные @0x06aab (r3)
- 0x00007fff — данные @0x07fff (r2)
- 0x0000a63a — данные @0x0a63a (r5)
- 0x0000ffff — данные @0x0ffff (r5)
- 0x200000ac — RAM (r1)
- 0x20000100 — RAM (r3)
- 0x2000023e — RAM (r3)
- 0x20000268 — RAM (r4)
- 0x20000380 — RAM (r5)
- 0x40023c00 — периферия (r3)
- 0x425b81c3 — периферия (r5)
- 0xffffc000 — прочее (r3)

## Вызовы (callees)

- 0x1bb38 (b, вне списка функций)
- 0x1bb4e (b, вне списка функций)
- 0x1bb74 (b, вне списка функций)
- 0x1bc1a (b, вне списка функций)
- 0x1bc70 (b, вне списка функций)
- 0x1bc7c (b, вне списка функций)
- 0x1bc82 (b, вне списка функций)
- 0x1bc92 (b, вне списка функций)
- 0x1bcb2 (b, вне списка функций)
- 0x1bcbc (b, вне списка функций)
- 0x1bd28 (b, вне списка функций)
- 0x1bd48 (b, вне списка функций)
- 0x21b52 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a41c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1bb36..0x1bb38` (2 Б); цели из: 0x1bb2a
- `0x1bb38..0x1bb4a` (18 Б); цели из: 0x1bb34
- `0x1bb4a..0x1bb4e` (4 Б); цели из: 0x1bb42
- `0x1bb4e..0x1bb6e` (32 Б); цели из: 0x1bb48
- `0x1bb6e..0x1bb74` (6 Б); цели из: 0x1bb66
- `0x1bb74..0x1bbdc` (104 Б); цели из: 0x1bb6c
- `0x1bbdc..0x1bc3e` (98 Б); цели из: 0x1bbca
- `0x1bc3e..0x1bc7c` (62 Б); цели из: 0x1bb56
- `0x1bc7c..0x1bc82` (6 Б); цели из: 0x1bc3e
- `0x1bc82..0x1bc92` (16 Б); цели из: 0x1bc3c, 0x1bc46, 0x1bc54, 0x1bc5c…
- `0x1bc92..0x1bca4` (18 Б); цели из: 0x1bbf6, 0x1bc08, 0x1bc10, 0x1bc1c…
- `0x1bca4..0x1bcae` (10 Б); цели из: 0x1bc9e
- `0x1bcae..0x1bcb2` (4 Б); цели из: 0x1bc8e
- `0x1bcb2..0x1bcba` (8 Б); цели из: 0x1bc90
- `0x1bcba..0x1bcbc` (2 Б); цели из: 0x1bcaa
- `0x1bcbc..0x1bcf0` (52 Б); цели из: 0x1bca2, 0x1bcac, 0x1bcb0, 0x1bcb8
- `0x1bcf0..0x1bcfc` (12 Б); цели из: 0x1bcec
- `0x1bcfc..0x1bd3c` (64 Б); цели из: 0x1bcf8
- `0x1bd3c..0x1bd48` (12 Б); цели из: 0x1bd0a, 0x1bd10
- `0x1bd48..0x1bd4e` (6 Б); цели из: 0x1bd2a

## Дизассембляция

```asm
  1bb1c:  push {r4, r5, r6, r7, lr}         
  1bb1e:  ldrh r1, [r0, #0xc]               
  1bb20:  movs r4, #0x7d                    
  1bb22:  lsls r4, r4, #4                   
  1bb24:  ldr r3, [pc, #0x228]              -> RAM
  1bb26:  movs r2, #0                       
  1bb28:  cmp r1, r4                        
  1bb2a:  bhs #0x1bb36                      
  1bb2c:  adds r1, r1, #1                   
  1bb2e:  strh r1, [r0, #0xc]               
  1bb30:  movs r1, #1                       
  1bb32:  strb r1, [r3]                     
  1bb34:  b #0x1bb38                        -> 0x1bb38 (вне списка функций)
  1bb36:  strb r2, [r3]                     
  1bb38:  ldr r1, [pc, #0x218]              -> RAM
  1bb3a:  movs r4, #0x7d                    
  1bb3c:  ldrh r3, [r1, #0x32]              
  1bb3e:  lsls r4, r4, #6                   
  1bb40:  cmp r3, r4                        
  1bb42:  bhs #0x1bb4a                      
  1bb44:  adds r3, r3, #1                   
  1bb46:  strh r3, [r1, #0x32]              
  1bb48:  b #0x1bb4e                        -> 0x1bb4e (вне списка функций)
  1bb4a:  strh r2, [r1, #0x34]              
  1bb4c:  strh r2, [r1, #0x32]              
  1bb4e:  ldr r4, [pc, #0x208]              -> RAM
  1bb50:  ldrb r3, [r0, #0x14]              
  1bb52:  ldrb r4, [r4]                     
  1bb54:  cmp r3, r4                        
  1bb56:  beq #0x1bc3e                      
  1bb58:  ldrh r5, [r1, #0x34]              
  1bb5a:  adds r5, r5, #1                   
  1bb5c:  strh r5, [r1, #0x34]              
  1bb5e:  ldr r5, [pc, #0x1fc]              -> данные @0x0a63a
  1bb60:  ldrb r3, [r5, r3]                 
  1bb62:  ldr r5, [pc, #0x1fc]              -> RAM
  1bb64:  cmp r3, r4                        
  1bb66:  beq #0x1bb6e                      
  1bb68:  strb r2, [r0, #0xa]               
  1bb6a:  strb r2, [r5]                     
  1bb6c:  b #0x1bb74                        -> 0x1bb74 (вне списка функций)
  1bb6e:  movs r3, #1                       
  1bb70:  strb r3, [r0, #0xa]               
  1bb72:  strb r3, [r5]                     
  1bb74:  ldr r3, [pc, #0x1dc]              -> RAM
  1bb76:  strb r4, [r0, #0x14]              
  1bb78:  ldrh r5, [r0, #0xc]               
  1bb7a:  lsls r6, r4, #1                   
  1bb7c:  adds r3, #0x44                    
  1bb7e:  strh r5, [r3, r6]                 
  1bb80:  movs r5, #2                       
  1bb82:  movs r6, #4                       
  1bb84:  ldrsh r5, [r3, r5]                
  1bb86:  ldrsh r6, [r3, r6]                
  1bb88:  movs r7, #8                       
  1bb8a:  adds r5, r5, r6                   
  1bb8c:  movs r6, #6                       
  1bb8e:  ldrsh r6, [r3, r6]                
  1bb90:  ldrsh r7, [r3, r7]                
  1bb92:  adds r6, r6, r7                   
  1bb94:  adds r5, r5, r6                   
  1bb96:  movs r6, #0xa                     
  1bb98:  ldrsh r6, [r3, r6]                
  1bb9a:  adds r5, r5, r6                   
  1bb9c:  movs r6, #0xc                     
  1bb9e:  ldrsh r6, [r3, r6]                
  1bba0:  adds r3, r5, r6                   
  1bba2:  str r3, [r0, #4]                  
  1bba4:  ldr r3, [pc, #0x1bc]              -> периферия
  1bba6:  ldr r5, [r3, #0x10]               
  1bba8:  movs r6, #1                       
  1bbaa:  orrs r5, r6                       
  1bbac:  str r5, [r3, #0x10]               
  1bbae:  ldr r5, [pc, #0x1b8]              -> данные @0x0ffff
  1bbb0:  str r5, [r3]                      
  1bbb2:  ldr r5, [r0, #4]                  
  1bbb4:  str r5, [r3, #4]                  
  1bbb6:  ldr r3, [r3, #8]                  
  1bbb8:  strh r3, [r0, #8]                 
  1bbba:  strh r2, [r0, #0xc]               
  1bbbc:  ldr r5, [pc, #0x194]              -> RAM
  1bbbe:  ldrb r3, [r0, #0xa]               
  1bbc0:  movs r7, #1                       
  1bbc2:  ldr r6, [pc, #0x1a8]              -> данные @0x01555
  1bbc4:  lsls r7, r7, #0xe                 
  1bbc6:  ldrb r5, [r5, #4]                 
  1bbc8:  cmp r3, #0                        
  1bbca:  beq #0x1bbdc                      
  1bbcc:  movs r3, r4                       
  1bbce:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1bbd2:  strb r7, [r0, r4]                 
  1bbd4:  mov r7, r6                        
  1bbd6:  str r3, [r7, r4]                  
  1bbd8:  ldr r3, [pc, #0xc0]               
  1bbda:  lsls r5, r2, #1                   
  1bbdc:  movs r3, r4                       
  1bbde:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1bbe2:  ldr r5, [pc, #0x1c]               -> периферия
  1bbe4:  adds r3, r1, r0                   
  1bbe6:  movs r3, #0xe                     
  1bbe8:  subs r5, r0, #0                   
  1bbea:  lsls r5, r1, #1                   
  1bbec:  strh r6, [r0, #0xe]               
  1bbee:  strh r7, [r0, #0x10]              
  1bbf0:  strh r6, [r0, #0x12]              
  1bbf2:  movs r3, #1                       
  1bbf4:  strb r3, [r1, #4]                 
  1bbf6:  b #0x1bc92                        -> 0x1bc92 (вне списка функций)
  1bbf8:  strh r7, [r0, #0xe]               
  1bbfa:  ldr r3, [pc, #0x174]              -> данные @0x06aab
  1bbfc:  b #0x1bc1a                        -> 0x1bc1a (вне списка функций)
  1bbfe:  ldr r3, [pc, #0x170]              -> данные @0x06aab
  1bc00:  strh r3, [r0, #0xe]               
  1bc02:  rsbs r3, r3, #0                   
  1bc04:  strh r3, [r0, #0x10]              
  1bc06:  cmp r5, #1                        
  1bc08:  bne #0x1bc92                      
  1bc0a:  ldr r3, [pc, #0x168]              -> RAM
  1bc0c:  strb r2, [r1, #4]                 
  1bc0e:  strh r2, [r3]                     
  1bc10:  b #0x1bc92                        -> 0x1bc92 (вне списка функций)
  1bc12:  ldr r3, [pc, #0x15c]              -> данные @0x06aab
  1bc14:  rsbs r3, r3, #0                   
  1bc16:  strh r3, [r0, #0xe]               
  1bc18:  ldr r3, [pc, #0x15c]              
  1bc1a:  strh r3, [r0, #0x10]              
  1bc1c:  b #0x1bc92                        -> 0x1bc92 (вне списка функций)
  1bc1e:  ldr r3, [pc, #0x158]              
  1bc20:  strh r3, [r0, #0xe]               
  1bc22:  ldr r3, [pc, #0x148]              -> данные @0x01555
  1bc24:  rsbs r3, r3, #0                   
  1bc26:  b #0x1bc1a                        -> 0x1bc1a (вне списка функций)
  1bc28:  ldr r3, [pc, #0x140]              -> данные @0x01555
  1bc2a:  rsbs r3, r3, #0                   
  1bc2c:  strh r3, [r0, #0xe]               
  1bc2e:  strh r6, [r0, #0x10]              
  1bc30:  b #0x1bc92                        -> 0x1bc92 (вне списка функций)
  1bc32:  strh r7, [r0, #0xe]               
  1bc34:  strh r6, [r0, #0x10]              
  1bc36:  strh r7, [r0, #0x12]              
  1bc38:  movs r3, #1                       
  1bc3a:  strb r3, [r1, #4]                 
  1bc3c:  b #0x1bc82                        -> 0x1bc82 (вне списка функций)
  1bc3e:  b #0x1bc7c                        -> 0x1bc7c (вне списка функций)
  1bc40:  ldr r3, [pc, #0x12c]              -> данные @0x06aab
  1bc42:  strh r3, [r0, #0xe]               
  1bc44:  strh r7, [r0, #0x10]              
  1bc46:  b #0x1bc82                        -> 0x1bc82 (вне списка функций)
  1bc48:  ldr r3, [pc, #0x124]              -> данные @0x06aab
  1bc4a:  rsbs r3, r3, #0                   
  1bc4c:  strh r3, [r0, #0xe]               
  1bc4e:  rsbs r3, r3, #0                   
  1bc50:  strh r3, [r0, #0x10]              
  1bc52:  cmp r5, #1                        
  1bc54:  bne #0x1bc82                      
  1bc56:  ldr r3, [pc, #0x11c]              -> RAM
  1bc58:  strb r2, [r1, #4]                 
  1bc5a:  strh r2, [r3]                     
  1bc5c:  b #0x1bc82                        -> 0x1bc82 (вне списка функций)
  1bc5e:  ldr r3, [pc, #0x118]              
  1bc60:  strh r3, [r0, #0xe]               
  1bc62:  ldr r3, [pc, #0x10c]              -> данные @0x06aab
  1bc64:  rsbs r3, r3, #0                   
  1bc66:  b #0x1bc70                        -> 0x1bc70 (вне списка функций)
  1bc68:  ldr r3, [pc, #0x100]              -> данные @0x01555
  1bc6a:  rsbs r3, r3, #0                   
  1bc6c:  strh r3, [r0, #0xe]               
  1bc6e:  ldr r3, [pc, #0x108]              
  1bc70:  strh r3, [r0, #0x10]              
  1bc72:  b #0x1bc82                        -> 0x1bc82 (вне списка функций)
  1bc74:  ldr r3, [pc, #0xf4]               -> данные @0x01555
  1bc76:  strh r6, [r0, #0xe]               
  1bc78:  rsbs r3, r3, #0                   
  1bc7a:  b #0x1bc70                        -> 0x1bc70 (вне списка функций)
  1bc7c:  ldrb r3, [r0, #0xa]               
  1bc7e:  cmp r3, #0                        
  1bc80:  beq #0x1bc92                      
  1bc82:  ldrh r3, [r0, #0xe]               
  1bc84:  ldrh r5, [r0, #8]                 
  1bc86:  subs r3, r3, r5                   
  1bc88:  sxth r3, r3                       
  1bc8a:  strh r3, [r0, #0xe]               
  1bc8c:  cmp r4, #3                        
  1bc8e:  beq #0x1bcae                      
  1bc90:  b #0x1bcb2                        -> 0x1bcb2 (вне списка функций)
  1bc92:  ldrh r3, [r0, #0xe]               
  1bc94:  ldrh r5, [r0, #8]                 
  1bc96:  adds r3, r3, r5                   
  1bc98:  sxth r3, r3                       
  1bc9a:  strh r3, [r0, #0xe]               
  1bc9c:  cmp r4, #3                        
  1bc9e:  bne #0x1bca4                      
  1bca0:  cmp r3, #0                        
  1bca2:  bge #0x1bcbc                      
  1bca4:  movs r5, #0x10                    
  1bca6:  ldrsh r5, [r0, r5]                
  1bca8:  cmp r3, r5                        
  1bcaa:  bgt #0x1bcba                      
  1bcac:  b #0x1bcbc                        -> 0x1bcbc (вне списка функций)
  1bcae:  cmp r3, #0                        
  1bcb0:  ble #0x1bcbc                      
  1bcb2:  movs r5, #0x10                    
  1bcb4:  ldrsh r5, [r0, r5]                
  1bcb6:  cmp r3, r5                        
  1bcb8:  bge #0x1bcbc                      
  1bcba:  strh r5, [r0, #0xe]               
  1bcbc:  movs r6, #0x1e                    
  1bcbe:  ldrsh r6, [r1, r6]                
  1bcc0:  strh r6, [r1, #0x20]              
  1bcc2:  movs r5, #0x1c                    
  1bcc4:  ldrh r3, [r1, #0x1a]              
  1bcc6:  ldrsh r5, [r1, r5]                
  1bcc8:  subs r3, r3, r5                   
  1bcca:  sxth r3, r3                       
  1bccc:  strh r3, [r1, #0x1e]              
  1bcce:  ldrh r7, [r1, #0x24]              
  1bcd0:  subs r6, r3, r6                   
  1bcd2:  asrs r6, r7                       
  1bcd4:  ldrh r7, [r1, #0x22]              
  1bcd6:  muls r6, r7, r6                   
  1bcd8:  ldrh r7, [r1, #0x28]              
  1bcda:  asrs r3, r7                       
  1bcdc:  ldrh r7, [r1, #0x26]              
  1bcde:  muls r3, r7, r3                   
  1bce0:  adds r3, r6, r3                   
  1bce2:  sxth r6, r3                       
  1bce4:  strh r6, [r1, #0x2c]              
  1bce6:  movs r3, #0x2e                    
  1bce8:  ldrsh r3, [r1, r3]                
  1bcea:  cmp r6, r3                        
  1bcec:  ble #0x1bcf0                      
  1bcee:  strh r3, [r1, #0x2c]              
  1bcf0:  movs r6, #0x2c                    
  1bcf2:  ldrsh r6, [r1, r6]                
  1bcf4:  rsbs r3, r3, #0                   
  1bcf6:  cmp r6, r3                        
  1bcf8:  bge #0x1bcfc                      
  1bcfa:  strh r3, [r1, #0x2c]              
  1bcfc:  ldrh r3, [r1, #0x2a]              
  1bcfe:  ldrh r6, [r1, #0x2c]              
  1bd00:  adds r3, r3, r6                   
  1bd02:  sxth r3, r3                       
  1bd04:  strh r3, [r1, #0x2a]              
  1bd06:  ldrb r6, [r1]                     
  1bd08:  cmp r6, #0                        
  1bd0a:  beq #0x1bd3c                      
  1bd0c:  ldrb r6, [r1, #2]                 
  1bd0e:  cmp r6, #5                        
  1bd10:  bhs #0x1bd3c                      
  1bd12:  movs r3, r4                       
  1bd14:  bl #0x21b52                       -> 0x21b52 (вне списка функций)
  1bd18:  adds r7, r0, r0                   
  1bd1a:  lsrs r7, r0, #0x10                
  1bd1c:  lsrs r2, r1, #0x20                
  1bd1e:  lsrs r5, r0, #0x1c                
  1bd20:  movs r0, r3                       
  1bd22:  ldr r2, [pc, #0x58]               -> данные @0x02aab
  1bd24:  b #0x1bd28                        -> 0x1bd28 (вне списка функций)
  1bd26:  ldr r2, [pc, #0x58]               -> данные @0x05555
  1bd28:  strh r2, [r1, #0x1c]              
  1bd2a:  b #0x1bd48                        -> 0x1bd48 (вне списка функций)
  1bd2c:  ldr r2, [pc, #0x54]               -> данные @0x07fff
  1bd2e:  b #0x1bd28                        -> 0x1bd28 (вне списка функций)
  1bd30:  ldr r2, [pc, #0x4c]               -> данные @0x05555
  1bd32:  rsbs r2, r2, #0                   
  1bd34:  b #0x1bd28                        -> 0x1bd28 (вне списка функций)
  1bd36:  ldr r2, [pc, #0x44]               -> данные @0x02aab
  1bd38:  rsbs r2, r2, #0                   
  1bd3a:  b #0x1bd28                        -> 0x1bd28 (вне списка функций)
  1bd3c:  ldrh r2, [r0, #8]                 
  1bd3e:  adds r3, r5, r3                   
  1bd40:  adds r2, r2, r3                   
  1bd42:  strh r2, [r1, #0x1c]              
  1bd44:  ldrh r2, [r0, #0xe]               
  1bd46:  strh r2, [r1, #0x1a]              
  1bd48:  ldrh r1, [r1, #0x1c]              
  1bd4a:  strh r1, [r0]                     
  1bd4c:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1bc00 (1 слов) ---
  1bc00:  .word 0x425b81c3  ; периферия
  ; --- literal-пул @0x1bd50 (14 слов) — ВНЕ границ функции ---
  1bd50:  .word 0x20000100  ; RAM
  1bd54:  .word 0x200000ac  ; RAM
  1bd58:  .word 0x20000268  ; RAM
  1bd5c:  .word 0x0000a63a  ; данные @0x0a63a
  1bd60:  .word 0x20000380  ; RAM
  1bd64:  .word 0x40023c00  ; периферия
  1bd68:  .word 0x0000ffff  ; данные @0x0ffff
  1bd6c:  .word 0x00001555  ; данные @0x01555
  1bd70:  .word 0x00006aab  ; данные @0x06aab
  1bd74:  .word 0x2000023e  ; RAM
  1bd78:  .word 0xffffc000
  1bd7c:  .word 0x00002aab  ; данные @0x02aab
  1bd80:  .word 0x00005555  ; данные @0x05555
  1bd84:  .word 0x00007fff  ; данные @0x07fff
```
