# func_0x02a94

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080002a94) | `0x00002a94` |
| размер кода | 132 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a7a8 — flash-mirror @0x1a7a8 (r0)
- 0x0801a7d0 — flash-mirror @0x1a7d0 (r2)
- 0x0801a808 — flash-mirror @0x1a808 (r2)
- 0x0801a824 — flash-mirror @0x1a824 (r0)
- 0x200016ad — RAM (r0)

## Вызовы (callees)

- `func_0x0307c` (0x0000307c, bl)
- 0x03220 (bl, вне списка функций)
- 0x03278 (bl, вне списка функций)
- `func_0x0332c` (0x0000332c, bl)
- `func_0x04f38` (0x00004f38, bl)
- `func_0x08588` (0x00008588, bl)
- `func_0x0c624` (0x0000c624, bl)
- `func_0x12fe0` (0x00012fe0, bl)
- 0x130c8 (bl, вне списка функций)
- 0x130e0 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03034` (bl @0x0000304c)
- `func_0x0c20c` (bl @0x0000c282)


## Дизассембляция

```asm
  02a94:  push {lr}                         
  02a96:  sub sp, #0x14                     
  02a98:  movs r1, #1                       
  02a9a:  mov r0, r1                        
  02a9c:  bl #0xc624                        -> func_0x0c624
  02aa0:  movs r1, #7                       
  02aa2:  movs r0, #1                       
  02aa4:  bl #0x8588                        -> func_0x08588
  02aa8:  movs r1, #2                       
  02aaa:  ldr r0, [pc, #0x6c]               -> flash-mirror @0x1a7a8
  02aac:  bl #0x332c                        -> func_0x0332c
  02ab0:  ldr r0, [pc, #0x68]               -> flash-mirror @0x1a824
  02ab2:  ldr r0, [r0]                      
  02ab4:  str r0, [sp, #0x10]               
  02ab6:  bl #0x307c                        -> func_0x0307c
  02aba:  ldr r2, [pc, #0x64]               -> flash-mirror @0x1a7d0
  02abc:  adds r2, #0x10                    
  02abe:  ldm r2, {r0, r1, r2}              
  02ac0:  stm.w sp, {r0, r1, r2}            
  02ac4:  ldr r0, [pc, #0x58]               -> flash-mirror @0x1a7d0
  02ac6:  ldm r0, {r0, r1, r2, r3}          
  02ac8:  bl #0x3278                        -> 0x03278 (вне списка функций)
  02acc:  movs r1, #0x96                    
  02ace:  ldr r0, [pc, #0x54]               -> RAM
  02ad0:  ldr r2, [pc, #0x54]               -> flash-mirror @0x1a808
  02ad2:  strd r0, r1, [sp, #0xc]           
  02ad6:  adds r2, #0x10                    
  02ad8:  ldm r2, {r0, r1, r2}              
  02ada:  stm.w sp, {r0, r1, r2}            
  02ade:  ldr r0, [pc, #0x48]               -> flash-mirror @0x1a808
  02ae0:  ldm r0, {r0, r1, r2, r3}          
  02ae2:  bl #0x3220                        -> 0x03220 (вне списка функций)
  02ae6:  ldr r1, [pc, #0x38]               -> flash-mirror @0x1a7d0
  02ae8:  movs r2, #1                       
  02aea:  ldr r0, [r1, #8]                  
  02aec:  movs r1, #0xc0                    
  02aee:  bl #0x130e0                       -> 0x130e0 (вне списка функций)
  02af2:  ldr r1, [pc, #0x2c]               -> flash-mirror @0x1a7d0
  02af4:  movs r2, #1                       
  02af6:  ldr r0, [r1, #8]                  
  02af8:  movw r1, #0x424                   
  02afc:  bl #0x12fe0                       -> func_0x12fe0
  02b00:  ldr r1, [pc, #0x24]               -> flash-mirror @0x1a808
  02b02:  ldr r0, [r1, #0x10]               
  02b04:  movs r1, #1                       
  02b06:  bl #0x4f38                        -> func_0x04f38
  02b0a:  ldr r1, [pc, #0x14]               -> flash-mirror @0x1a7d0
  02b0c:  ldr r0, [r1, #8]                  
  02b0e:  movs r1, #1                       
  02b10:  bl #0x130c8                       -> 0x130c8 (вне списка функций)
  02b14:  add sp, #0x14                     
  02b16:  pop {pc}                          
  ; --- literal-пул @0x02b18 (5 слов) — ВНЕ границ функции ---
  02b18:  .word 0x0801a7a8  ; flash-mirror @0x1a7a8
  02b1c:  .word 0x0801a824  ; flash-mirror @0x1a824
  02b20:  .word 0x0801a7d0  ; flash-mirror @0x1a7d0
  02b24:  .word 0x200016ad  ; RAM
  02b28:  .word 0x0801a808  ; flash-mirror @0x1a808
```
