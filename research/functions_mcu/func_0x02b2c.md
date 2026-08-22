# func_0x02b2c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002b2c) | `0x00002b2c` |
| размер кода | 124 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a827 — flash-mirror @0x1a827 (r0)
- 0x0801a878 — flash-mirror @0x1a878 (r2)
- 0x0801a8b0 — flash-mirror @0x1a8b0 (r2)
- 0x0801a8cc — flash-mirror @0x1a8cc (r0)
- 0x20001ad8 — RAM (r0)

## Вызовы (callees)

- `func_0x0307c` (0x0000307c, bl)
- 0x03220 (bl, вне списка функций)
- 0x03278 (bl, вне списка функций)
- `func_0x0332c` (0x0000332c, bl)
- `func_0x04f38` (0x00004f38, bl)
- `func_0x0c624` (0x0000c624, bl)
- `func_0x12fe0` (0x00012fe0, bl)
- 0x130c8 (bl, вне списка функций)
- 0x130e0 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03f00` (bl @0x00003f50)


## Дизассембляция

```asm
  02b2c:  push {lr}                         
  02b2e:  sub sp, #0x14                     
  02b30:  movs r1, #1                       
  02b32:  mov r0, r1                        
  02b34:  bl #0xc624                        -> func_0x0c624
  02b38:  movs r1, #2                       
  02b3a:  ldr r0, [pc, #0x6c]               -> flash-mirror @0x1a827
  02b3c:  bl #0x332c                        -> func_0x0332c
  02b40:  ldr r0, [pc, #0x68]               -> flash-mirror @0x1a8cc
  02b42:  ldr r0, [r0]                      
  02b44:  str r0, [sp, #0x10]               
  02b46:  bl #0x307c                        -> func_0x0307c
  02b4a:  ldr r2, [pc, #0x64]               -> flash-mirror @0x1a878
  02b4c:  adds r2, #0x10                    
  02b4e:  ldm r2, {r0, r1, r2}              
  02b50:  stm.w sp, {r0, r1, r2}            
  02b54:  ldr r0, [pc, #0x58]               -> flash-mirror @0x1a878
  02b56:  ldm r0, {r0, r1, r2, r3}          
  02b58:  bl #0x3278                        -> 0x03278 (вне списка функций)
  02b5c:  movs r1, #0x96                    
  02b5e:  ldr r0, [pc, #0x54]               -> RAM
  02b60:  ldr r2, [pc, #0x54]               -> flash-mirror @0x1a8b0
  02b62:  strd r0, r1, [sp, #0xc]           
  02b66:  adds r2, #0x10                    
  02b68:  ldm r2, {r0, r1, r2}              
  02b6a:  stm.w sp, {r0, r1, r2}            
  02b6e:  ldr r0, [pc, #0x48]               -> flash-mirror @0x1a8b0
  02b70:  ldm r0, {r0, r1, r2, r3}          
  02b72:  bl #0x3220                        -> 0x03220 (вне списка функций)
  02b76:  ldr r1, [pc, #0x38]               -> flash-mirror @0x1a878
  02b78:  movs r2, #1                       
  02b7a:  ldr r0, [r1, #8]                  
  02b7c:  movs r1, #0xc0                    
  02b7e:  bl #0x130e0                       -> 0x130e0 (вне списка функций)
  02b82:  ldr r1, [pc, #0x2c]               -> flash-mirror @0x1a878
  02b84:  movs r2, #1                       
  02b86:  ldr r0, [r1, #8]                  
  02b88:  movw r1, #0x424                   
  02b8c:  bl #0x12fe0                       -> func_0x12fe0
  02b90:  ldr r1, [pc, #0x24]               -> flash-mirror @0x1a8b0
  02b92:  ldr r0, [r1, #0x10]               
  02b94:  movs r1, #1                       
  02b96:  bl #0x4f38                        -> func_0x04f38
  02b9a:  ldr r1, [pc, #0x14]               -> flash-mirror @0x1a878
  02b9c:  ldr r0, [r1, #8]                  
  02b9e:  movs r1, #1                       
  02ba0:  bl #0x130c8                       -> 0x130c8 (вне списка функций)
  02ba4:  add sp, #0x14                     
  02ba6:  pop {pc}                          
  ; --- literal-пул @0x02ba8 (5 слов) — ВНЕ границ функции ---
  02ba8:  .word 0x0801a827  ; flash-mirror @0x1a827
  02bac:  .word 0x0801a8cc  ; flash-mirror @0x1a8cc
  02bb0:  .word 0x0801a878  ; flash-mirror @0x1a878
  02bb4:  .word 0x20001ad8  ; RAM
  02bb8:  .word 0x0801a8b0  ; flash-mirror @0x1a8b0
```
