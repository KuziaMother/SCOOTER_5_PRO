# func_0x1bfa0

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001bfa0) | `0x0001bfa0` |
| размер кода | 150 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0000a907 — данные @0x0a907 (r4)
- 0x0000ab07 — данные @0x0ab07 (r4)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x1a5f2` (bl @0x0001a5f4)


## Дизассембляция

```asm
  1bfa0:  push {r3, r4, r5, r6, r7, lr}     
  1bfa2:  movs r2, #0                       
  1bfa4:  lsls r3, r2, #2                   
  1bfa6:  ldrb r4, [r1, r3]                 
  1bfa8:  strb r4, [r0, r3]                 
  1bfaa:  adds r4, r3, r1                   
  1bfac:  adds r3, r3, r0                   
  1bfae:  ldrb r5, [r4, #1]                 
  1bfb0:  strb r5, [r3, #1]                 
  1bfb2:  ldrb r5, [r4, #2]                 
  1bfb4:  strb r5, [r3, #2]                 
  1bfb6:  ldrb r4, [r4, #3]                 
  1bfb8:  adds r2, r2, #1                   
  1bfba:  strb r4, [r3, #3]                 
  1bfbc:  cmp r2, #4                        
  1bfbe:  blo #0x1bfa4                      
  1bfc0:  movs r2, #4                       
  1bfc2:  lsls r1, r2, #2                   
  1bfc4:  subs r5, r1, #4                   
  1bfc6:  ldrb r3, [r0, r5]                 
  1bfc8:  mov r4, sp                        
  1bfca:  strb r3, [r4]                     
  1bfcc:  adds r5, r0, r5                   
  1bfce:  ldrb r7, [r5, #1]                 
  1bfd0:  strb r7, [r4, #1]                 
  1bfd2:  ldrb r6, [r5, #2]                 
  1bfd4:  strb r6, [r4, #2]                 
  1bfd6:  ldrb r5, [r5, #3]                 
  1bfd8:  strb r5, [r4, #3]                 
  1bfda:  lsls r4, r2, #0x1e                
  1bfdc:  bne #0x1bffe                      
  1bfde:  ldr r4, [pc, #0x58]               -> данные @0x0a907
  1bfe0:  ldrb r7, [r4, r7]                 
  1bfe2:  mov ip, r7                        
  1bfe4:  ldrb r7, [r4, r6]                 
  1bfe6:  mov r6, sp                        
  1bfe8:  strb r7, [r6, #1]                 
  1bfea:  ldrb r5, [r4, r5]                 
  1bfec:  strb r5, [r6, #2]                 
  1bfee:  ldrb r3, [r4, r3]                 
  1bff0:  strb r3, [r6, #3]                 
  1bff2:  ldr r4, [pc, #0x48]               -> данные @0x0ab07
  1bff4:  lsrs r3, r2, #2                   
  1bff6:  ldrb r3, [r4, r3]                 
  1bff8:  mov r7, ip                        
  1bffa:  eors r7, r3                       
  1bffc:  strb r7, [r6]                     
  1bffe:  mov r3, r1                        
  1c000:  subs r3, #0x10                    
  1c002:  mov r4, sp                        
  1c004:  ldrb r5, [r0, r3]                 
  1c006:  ldrb r4, [r4]                     
  1c008:  adds r3, r0, r3                   
  1c00a:  eors r5, r4                       
  1c00c:  strb r5, [r0, r1]                 
  1c00e:  mov r4, sp                        
  1c010:  ldrb r5, [r3, #1]                 
  1c012:  ldrb r4, [r4, #1]                 
  1c014:  adds r1, r0, r1                   
  1c016:  eors r5, r4                       
  1c018:  strb r5, [r1, #1]                 
  1c01a:  mov r4, sp                        
  1c01c:  ldrb r5, [r3, #2]                 
  1c01e:  ldrb r4, [r4, #2]                 
  1c020:  adds r2, r2, #1                   
  1c022:  eors r5, r4                       
  1c024:  strb r5, [r1, #2]                 
  1c026:  mov r4, sp                        
  1c028:  ldrb r3, [r3, #3]                 
  1c02a:  ldrb r4, [r4, #3]                 
  1c02c:  eors r3, r4                       
  1c02e:  strb r3, [r1, #3]                 
  1c030:  cmp r2, #0x2c                     
  1c032:  blo #0x1bfc2                      
  1c034:  pop {r3, r4, r5, r6, r7, pc}      
  ; --- literal-пул @0x1c038 (2 слов) — ВНЕ границ функции ---
  1c038:  .word 0x0000a907  ; данные @0x0a907
  1c03c:  .word 0x0000ab07  ; данные @0x0ab07
```
