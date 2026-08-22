# func_0x12b50

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080012b50) | `0x00012b50` |
| размер кода | 190 Б |
| регион | код E (UART init/драйвер: 0x12d90/0x1302c) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801a808 — flash-mirror @0x1a808 (r1)
- 0x20000b78 — RAM (r1)
- 0x200016ad — RAM (r1)
- 0x2000190d — RAM (r0)
- 0x40013800 — периферия (r0)

## Вызовы (callees)

- 0x011a4 (bl, вне списка функций)
- `func_0x04f38` (0x00004f38, bl)
- `func_0x04f50` (0x00004f50, bl)
- `func_0x04fba` (0x00004fba, bl)
- `func_0x130f2` (0x000130f2, bl)

## Кто вызывает (callers / xrefs)

- `func_0x12fd0` (bl @0x00012fd2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x12baa..0x12bf2` (72 Б); цели из: 0x12ba6
- `0x12bf2..0x12c0c` (26 Б); цели из: 0x12b8c, 0x12b98
- `0x12c0c..0x12c0e` (2 Б); цели из: 0x12b62

## Дизассембляция

```asm
  12b50:  push {r4, r5, r6, lr}             
  12b52:  movs r5, #0                       
  12b54:  movs r4, #0                       
  12b56:  movw r1, #0x424                   
  12b5a:  ldr r0, [pc, #0xb4]               -> периферия
  12b5c:  bl #0x130f2                       -> func_0x130f2
  12b60:  cmp r0, #0                        
  12b62:  beq #0x12c0c                      
  12b64:  ldr r0, [pc, #0xa8]               -> периферия
  12b66:  ldrh r0, [r0]                     
  12b68:  uxtb r4, r0                       
  12b6a:  ldr r0, [pc, #0xa4]               -> периферия
  12b6c:  adds r0, r0, #4                   
  12b6e:  ldrh r0, [r0]                     
  12b70:  uxtb r4, r0                       
  12b72:  ldr r1, [pc, #0xa0]               -> flash-mirror @0x1a808
  12b74:  ldr r0, [r1, #0x10]               
  12b76:  movs r1, #0                       
  12b78:  bl #0x4f38                        -> func_0x04f38
  12b7c:  ldr r1, [pc, #0x94]               -> flash-mirror @0x1a808
  12b7e:  ldr r0, [r1, #0x10]               
  12b80:  bl #0x4f50                        -> func_0x04f50
  12b84:  rsb.w r0, r0, #0x96               
  12b88:  uxth r5, r0                       
  12b8a:  cmp r5, #0                        
  12b8c:  ble #0x12bf2                      
  12b8e:  ldr r0, [pc, #0x88]               -> RAM
  12b90:  ldrb r0, [r0]                     
  12b92:  and r0, r0, #7                    
  12b96:  cmp r0, #7                        
  12b98:  bge #0x12bf2                      
  12b9a:  ldr r0, [pc, #0x7c]               -> RAM
  12b9c:  ldrb r4, [r0, #1]                 
  12b9e:  nop                               
  12ba0:  adds r0, r4, #1                   
  12ba2:  uxtb r4, r0                       
  12ba4:  cmp r4, #3                        
  12ba6:  blt #0x12baa                      
  12ba8:  movs r4, #0                       
  12baa:  ldr r0, [pc, #0x6c]               -> RAM
  12bac:  ldrb r0, [r0]                     
  12bae:  movs r1, #1                       
  12bb0:  lsls r1, r4                       
  12bb2:  ands r0, r1                       
  12bb4:  cmp r0, #0                        
  12bb6:  bne #0x12ba0                      
  12bb8:  ldr r0, [pc, #0x5c]               -> RAM
  12bba:  ldrb r0, [r0]                     
  12bbc:  movs r1, #1                       
  12bbe:  lsls r1, r4                       
  12bc0:  orrs r0, r1                       
  12bc2:  ldr r1, [pc, #0x54]               -> RAM
  12bc4:  strb r0, [r1]                     
  12bc6:  add.w r1, r4, r4, lsl #1          
  12bca:  add.w r2, r1, r4, lsl #4          
  12bce:  ldr r1, [pc, #0x48]               -> RAM
  12bd0:  adds r1, r1, #2                   
  12bd2:  add.w r1, r1, r2, lsl #3          
  12bd6:  adds r0, r1, #2                   
  12bd8:  mov r2, r5                        
  12bda:  ldr r1, [pc, #0x40]               -> RAM
  12bdc:  bl #0x11a4                        -> 0x011a4 (вне списка функций)
  12be0:  add.w r0, r4, r4, lsl #1          
  12be4:  add.w r1, r0, r4, lsl #4          
  12be8:  ldr r0, [pc, #0x2c]               -> RAM
  12bea:  adds r0, r0, #2                   
  12bec:  add.w r0, r0, r1, lsl #3          
  12bf0:  strh r5, [r0]                     
  12bf2:  ldr r1, [pc, #0x20]               -> flash-mirror @0x1a808
  12bf4:  ldr r0, [r1, #0x10]               
  12bf6:  movs r1, #0x96                    
  12bf8:  bl #0x4fba                        -> func_0x04fba
  12bfc:  ldr r1, [pc, #0x14]               -> flash-mirror @0x1a808
  12bfe:  ldr r0, [r1, #0x10]               
  12c00:  movs r1, #1                       
  12c02:  bl #0x4f38                        -> func_0x04f38
  12c06:  movs r0, #0                       
  12c08:  ldr r1, [pc, #0x14]               -> RAM
  12c0a:  strh r0, [r1]                     
  12c0c:  pop {r4, r5, r6, pc}              
  ; --- literal-пул @0x12c10 (5 слов) — ВНЕ границ функции ---
  12c10:  .word 0x40013800  ; периферия
  12c14:  .word 0x0801a808  ; flash-mirror @0x1a808
  12c18:  .word 0x2000190d  ; RAM
  12c1c:  .word 0x200016ad  ; RAM
  12c20:  .word 0x20000b78  ; RAM
```
