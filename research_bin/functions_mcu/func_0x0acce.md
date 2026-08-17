# func_0x0acce

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000acce) | `0x0000acce` |
| размер кода | 458 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801c800 — flash-mirror @0x1c800 (r0)
- 0x0801d000 — flash-mirror @0x1d000 (r0)
- 0x0801f000 — flash-mirror @0x1f000 (r1)
- 0x0801f800 — flash-mirror @0x1f800 (r1)
- 0x2000007c — RAM (r0)
- 0x2000007d — RAM (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- 0x011d6 (bl, вне списка функций)
- `func_0x07e98` (0x00007e98, bl)
- `func_0x080ac` (0x000080ac, bl)
- `func_0x097ca` (0x000097ca, bl)
- `func_0x09874` (0x00009874, bl)
- `func_0x0a8c4` (0x0000a8c4, bl)
- `func_0x0a910` (0x0000a910, bl)
- `func_0x0a960` (0x0000a960, bl)
- `func_0x0aa18` (0x0000aa18, bl)
- `func_0x0aad0` (0x0000aad0, bl)
- 0x0ad5e (b, вне списка функций)
- 0x0ad86 (b, вне списка функций)
- 0x0ae26 (b, вне списка функций)
- 0x0ae4e (b, вне списка функций)
- 0x0ae80 (b, вне списка функций)
- 0x0ae86 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в коде образа)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0ad48..0x0ad5e` (22 Б); цели из: 0x0ad2e
- `0x0ad5e..0x0ad86` (40 Б); цели из: 0x0ad46
- `0x0ad86..0x0ae10` (138 Б); цели из: 0x0ad70, 0x0ad7e
- `0x0ae10..0x0ae26` (22 Б); цели из: 0x0adf6
- `0x0ae26..0x0ae4e` (40 Б); цели из: 0x0ae0e
- `0x0ae4e..0x0ae60` (18 Б); цели из: 0x0ae38, 0x0ae46
- `0x0ae60..0x0ae86` (38 Б); цели из: 0x0ae5c
- `0x0ae86..0x0ae98` (18 Б); цели из: 0x0ae74, 0x0ae7c

## Дизассембляция

```asm
  0acce:  push {r4, r5, r6, r7, lr}         
  0acd0:  sub sp, #0x3c                     
  0acd2:  movs r4, #0                       
  0acd4:  movs r5, #0                       
  0acd6:  movs r7, #0                       
  0acd8:  movs r6, #0                       
  0acda:  movs r0, #0                       
  0acdc:  bl #0xa910                        -> func_0x0a910
  0ace0:  mov r4, r0                        
  0ace2:  rsb r0, r4, r4, lsl #3            
  0ace6:  ldr r1, [pc, #0xa8]               -> flash-mirror @0x1f000
  0ace8:  add.w r5, r1, r0, lsl #3          
  0acec:  rsb r0, r4, r4, lsl #3            
  0acf0:  ldr r1, [pc, #0xa0]               -> flash-mirror @0x1f800
  0acf2:  add.w r7, r1, r0, lsl #3          
  0acf6:  movs r1, #0x38                    
  0acf8:  add r0, sp, #4                    
  0acfa:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0acfe:  movs r0, #0xaa                    
  0ad00:  str r0, [sp, #4]                  
  0ad02:  movs r2, #0x30                    
  0ad04:  add r1, sp, #0x50                 
  0ad06:  add r0, sp, #8                    
  0ad08:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0ad0c:  movs r1, #0x34                    
  0ad0e:  add r0, sp, #4                    
  0ad10:  bl #0xaad0                        -> func_0x0aad0
  0ad14:  ldr r1, [sp, #0x38]               
  0ad16:  bfi r1, r0, #0x10, #0x10          
  0ad1a:  str r1, [sp, #0x38]               
  0ad1c:  cbnz r4, #0xad24                  
  0ad1e:  ldr r0, [pc, #0x70]               -> flash-mirror @0x1f000
  0ad20:  bl #0x7e98                        -> func_0x07e98
  0ad24:  add.w r0, r5, #0x38               
  0ad28:  ldr r1, [pc, #0x68]               -> flash-mirror @0x1f800
  0ad2a:  subs r1, r1, #1                   
  0ad2c:  cmp r0, r1                        
  0ad2e:  blo #0xad48                       
  0ad30:  movs r2, #0x38                    
  0ad32:  add r1, sp, #4                    
  0ad34:  ldr r0, [pc, #0x58]               -> flash-mirror @0x1f000
  0ad36:  bl #0x80ac                        -> func_0x080ac
  0ad3a:  mov r6, r0                        
  0ad3c:  movs r2, #0x38                    
  0ad3e:  add r1, sp, #4                    
  0ad40:  ldr r0, [pc, #0x50]               -> flash-mirror @0x1f800
  0ad42:  bl #0x80ac                        -> func_0x080ac
  0ad46:  b #0xad5e                         -> 0x0ad5e (вне списка функций)
  0ad48:  movs r2, #0x38                    
  0ad4a:  add r1, sp, #4                    
  0ad4c:  mov r0, r5                        
  0ad4e:  bl #0xa960                        -> func_0x0a960
  0ad52:  mov r6, r0                        
  0ad54:  movs r2, #0x38                    
  0ad56:  add r1, sp, #4                    
  0ad58:  mov r0, r7                        
  0ad5a:  bl #0xa960                        -> func_0x0a960
  0ad5e:  cbnz r6, #0xad80                  
  0ad60:  ldr r0, [pc, #0x34]               -> RAM
  0ad62:  ldrb r0, [r0]                     
  0ad64:  adds r0, r0, #1                   
  0ad66:  ldr r1, [pc, #0x30]               -> RAM
  0ad68:  strb r0, [r1]                     
  0ad6a:  mov r0, r1                        
  0ad6c:  ldrb r0, [r0]                     
  0ad6e:  cmp r0, #3                        
  0ad70:  ble #0xad86                       
  0ad72:  ldr r0, [pc, #0x1c]               -> flash-mirror @0x1f000
  0ad74:  bl #0x7e98                        -> func_0x07e98
  0ad78:  ldr r0, [pc, #0x18]               -> flash-mirror @0x1f800
  0ad7a:  bl #0x7e98                        -> func_0x07e98
  0ad7e:  b #0xad86                         -> 0x0ad86 (вне списка функций)
  0ad80:  movs r0, #0                       
  0ad82:  ldr r1, [pc, #0x14]               -> RAM
  0ad84:  strb r0, [r1]                     
  0ad86:  mov r0, r6                        
  0ad88:  add sp, #0x3c                     
  0ad8a:  pop {r4, r5, r6, r7}              
  0ad8c:  ldr pc, [sp], #0x14               
  0ad90:  and r8, r0, #1                    
  0ad94:  .byte 0x00, 0xf8                  
  0ad96:  lsrs r1, r0, #0x20                
  0ad98:  lsls r4, r7, #1                   
  0ad9a:  movs r0, #0                       
  0ad9c:  push {r0, r1, r2, r3}             
  0ad9e:  push {r4, r5, r6, r7, lr}         
  0ada0:  sub sp, #0x24                     
  0ada2:  movs r4, #0                       
  0ada4:  movs r5, #0                       
  0ada6:  movs r7, #0                       
  0ada8:  movs r6, #0                       
  0adaa:  movs r0, #0                       
  0adac:  bl #0xa8c4                        -> func_0x0a8c4
  0adb0:  mov r4, r0                        
  0adb2:  ldr r0, [pc, #0xa4]               -> flash-mirror @0x1c800
  0adb4:  add.w r5, r0, r4, lsl #5          
  0adb8:  ldr r0, [pc, #0xa0]               -> flash-mirror @0x1d000
  0adba:  add.w r7, r0, r4, lsl #5          
  0adbe:  movs r1, #0x20                    
  0adc0:  add r0, sp, #4                    
  0adc2:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0adc6:  movs r0, #0xaa                    
  0adc8:  str r0, [sp, #4]                  
  0adca:  movs r2, #0x18                    
  0adcc:  add r1, sp, #0x38                 
  0adce:  add r0, sp, #8                    
  0add0:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  0add4:  movs r1, #0x1c                    
  0add6:  add r0, sp, #4                    
  0add8:  bl #0xaad0                        -> func_0x0aad0
  0addc:  ldr r1, [sp, #0x20]               
  0adde:  bfi r1, r0, #0x10, #0x10          
  0ade2:  str r1, [sp, #0x20]               
  0ade4:  cbnz r4, #0xadec                  
  0ade6:  ldr r0, [pc, #0x70]               -> flash-mirror @0x1c800
  0ade8:  bl #0x7e98                        -> func_0x07e98
  0adec:  add.w r0, r5, #0x20               
  0adf0:  ldr r1, [pc, #0x68]               -> flash-mirror @0x1d000
  0adf2:  subs r1, r1, #1                   
  0adf4:  cmp r0, r1                        
  0adf6:  blo #0xae10                       
  0adf8:  movs r2, #0x20                    
  0adfa:  add r1, sp, #4                    
  0adfc:  ldr r0, [pc, #0x58]               -> flash-mirror @0x1c800
  0adfe:  bl #0x80ac                        -> func_0x080ac
  0ae02:  mov r6, r0                        
  0ae04:  movs r2, #0x20                    
  0ae06:  add r1, sp, #4                    
  0ae08:  ldr r0, [pc, #0x50]               -> flash-mirror @0x1d000
  0ae0a:  bl #0x80ac                        -> func_0x080ac
  0ae0e:  b #0xae26                         -> 0x0ae26 (вне списка функций)
  0ae10:  movs r2, #0x20                    
  0ae12:  add r1, sp, #4                    
  0ae14:  mov r0, r5                        
  0ae16:  bl #0xaa18                        -> func_0x0aa18
  0ae1a:  mov r6, r0                        
  0ae1c:  movs r2, #0x20                    
  0ae1e:  add r1, sp, #4                    
  0ae20:  mov r0, r7                        
  0ae22:  bl #0xaa18                        -> func_0x0aa18
  0ae26:  cbnz r6, #0xae48                  
  0ae28:  ldr r0, [pc, #0x34]               -> RAM
  0ae2a:  ldrb r0, [r0]                     
  0ae2c:  adds r0, r0, #1                   
  0ae2e:  ldr r1, [pc, #0x30]               -> RAM
  0ae30:  strb r0, [r1]                     
  0ae32:  mov r0, r1                        
  0ae34:  ldrb r0, [r0]                     
  0ae36:  cmp r0, #3                        
  0ae38:  ble #0xae4e                       
  0ae3a:  ldr r0, [pc, #0x1c]               -> flash-mirror @0x1c800
  0ae3c:  bl #0x7e98                        -> func_0x07e98
  0ae40:  ldr r0, [pc, #0x18]               -> flash-mirror @0x1d000
  0ae42:  bl #0x7e98                        -> func_0x07e98
  0ae46:  b #0xae4e                         -> 0x0ae4e (вне списка функций)
  0ae48:  movs r0, #0                       
  0ae4a:  ldr r1, [pc, #0x14]               -> RAM
  0ae4c:  strb r0, [r1]                     
  0ae4e:  mov r0, r6                        
  0ae50:  add sp, #0x24                     
  0ae52:  pop {r4, r5, r6, r7}              
  0ae54:  ldr pc, [sp], #0x14               
  0ae58:  .byte 0x00, 0xc8                  
  0ae5a:  lsrs r1, r0, #0x20                
  0ae5c:  beq #0xae60                       
  0ae5e:  lsrs r1, r0, #0x20                
  0ae60:  lsls r5, r7, #1                   
  0ae62:  movs r0, #0                       
  0ae64:  push {r0, r1, r2, r3}             
  0ae66:  push {r4, lr}                     
  0ae68:  movs r1, #1                       
  0ae6a:  ldr r0, [sp, #8]                  
  0ae6c:  bl #0x97ca                        -> func_0x097ca
  0ae70:  mov.w r4, #0x10000                
  0ae74:  b #0xae86                         -> 0x0ae86 (вне списка функций)
  0ae76:  subs r0, r4, #0                   
  0ae78:  sub.w r4, r4, #1                  
  0ae7c:  bne #0xae86                       
  0ae7e:  movs r0, #2                       
  0ae80:  pop {r4}                          
  0ae82:  ldr pc, [sp], #0x14               
  0ae86:  mov.w r1, #0x20000                
  0ae8a:  ldr r0, [sp, #8]                  
  0ae8c:  bl #0x9874                        -> func_0x09874
  0ae90:  cmp r0, #0                        
  0ae92:  bne #0xae76                       
  0ae94:  nop                               
  0ae96:  b #0xae80                         -> 0x0ae80 (вне списка функций)
  ; --- literal-пул @0x0ad90 (3 слов) ---
  0ad90:  .word 0x0801f000  ; flash-mirror @0x1f000
  0ad94:  .word 0x0801f800  ; flash-mirror @0x1f800
  0ad98:  .word 0x2000007c  ; RAM
  ; --- literal-пул @0x0ae58 (3 слов) ---
  0ae58:  .word 0x0801c800  ; flash-mirror @0x1c800
  0ae5c:  .word 0x0801d000  ; flash-mirror @0x1d000
  0ae60:  .word 0x2000007d  ; RAM
```
