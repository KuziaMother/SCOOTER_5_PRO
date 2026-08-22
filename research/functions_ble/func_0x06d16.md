# func_0x06d16

| | |
|---|---|
| offset в файле | `0x06d16` |
| vaddr (база 0x01800000) | `0x01806d16` |
 | размер кода | 180 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00202044 — RAM (r1)
- 0x00206840 — RAM (r1)
- 0x21600002 — прочее (r0)
- 0x40051000 — периферия (fp)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x0161fdc0 (bl, вне списка функций)
- 0x0161fdde (bl, вне списка функций)
- 0x01806d92 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0778c` (bl @0x018077f8)

## Дизассембляция

```asm
  01806d16:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  01806d1a:  ldr r1, [pc, #0x2e8]              (RAM)
  01806d1c:  mov sl, r0                        
  01806d1e:  add.w r0, r1, sl, lsl #2          
  01806d22:  sub sp, #0x14                     
  01806d24:  ldr.w r4, [r0, #0x210]            
  01806d28:  movs r1, #0x14                    
  01806d2a:  mov r0, sl                        
  01806d2c:  adds r4, #0x9c                    
  01806d2e:  bl #0x161fdc0                     
  01806d32:  ldrb r2, [r4, #0x14]              
  01806d34:  ubfx r1, r0, #0xa, #0x10          
  01806d38:  lsls r7, r2, #1                   
  01806d3a:  ldrh r2, [r4, #4]                 
  01806d3c:  mov r8, r1                        
  01806d3e:  lsls r6, r2, #1                   
  01806d40:  sub.w r2, sl, #8                  
  01806d44:  uxtb r5, r2                       
  01806d46:  subs r2, r6, r7                   
  01806d48:  subs r2, r2, #2                   
  01806d4a:  sub.w r2, r1, r2, lsr #1          
  01806d4e:  cmp r2, #0                        
  01806d50:  ble #0x1806d5a                    
  01806d52:  sub.w r1, r8, r2                  
  01806d56:  bfi r0, r1, #0xa, #0x10           
  01806d5a:  ldr.w fp, [pc, #0x2ac]            (периферия)
  01806d5e:  ldrh.w r4, [fp, #0x24e]           
  01806d62:  ldr r1, [pc, #0x2a8]              (RAM)
  01806d64:  ubfx r2, r4, #0xa, #3             
  01806d68:  strb r2, [r1, r5]                 
  01806d6a:  ubfx r2, r0, #0xa, #0x10          
  01806d6e:  adds r1, r2, #2                   
  01806d70:  uxth r1, r1                       
  01806d72:  cmp r1, #7                        
  01806d74:  bls #0x1806d84                    
  01806d76:  subs r1, r2, r1                   
  01806d78:  adds r1, r1, #7                   
  01806d7a:  bfi r0, r1, #0xa, #0x10           
  01806d7e:  orr r4, r4, #0x1c00               
  01806d82:  b #0x1806d92                      -> 0x06d92 (вне списка функций)
  01806d84:  ubfx r2, r4, #0xa, #3             
  01806d88:  cmp r2, r1                        
  01806d8a:  blo #0x1806d8e                    
  01806d8c:  mov r1, r2                        
  01806d8e:  bfi r4, r1, #0xa, #3              
  01806d92:  mov sb, r0                        
  01806d94:  mov r2, sb                        
  01806d96:  movs r1, #0x14                    
  01806d98:  mov r0, sl                        
  01806d9a:  bl #0x161fdde                     
  01806d9e:  strh.w r4, [fp, #0x24e]           
  01806da2:  ubfx r0, sb, #0xa, #0x10          
  01806da6:  strd r0, r7, [sp, #8]             
  01806daa:  ubfx r0, r4, #0xa, #3             
  01806dae:  strd r0, r8, [sp]                 
  01806db2:  ldr r0, [pc, #0x258]              (RAM)
  01806db4:  str r6, [sp, #0x10]               
  01806db6:  movs r2, #6                       
  01806db8:  ldrb r3, [r0, r5]                 
  01806dba:  movw r1, #0x439                   
  01806dbe:  ldr r0, [pc, #0x250]              
  01806dc0:  bl #0x15f5b92                     
  01806dc4:  add sp, #0x14                     
  01806dc6:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
  ; --- literal-пул @0x07004 (4 слов) — ВНЕ границ функции ---
  07004:  .word 0x00202044  ; RAM
  07008:  .word 0x40051000  ; периферия
  0700c:  .word 0x00206840  ; RAM
  07010:  .word 0x21600002
```
