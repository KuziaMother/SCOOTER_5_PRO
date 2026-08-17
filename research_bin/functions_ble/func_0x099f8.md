# func_0x099f8

| | |
|---|---|
| offset в файле | `0x099f8` |
| vaddr (база 0x01800000) | `0x018099f8` |
 | размер кода | 170 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00009e01 — прочее (r1)
- 0x0000a315 — прочее (r1)
- 0x0000a359 — прочее (r1)
- 0x0000a39d — прочее (r1)
- 0x0000a4cd — прочее (r1)
- 0x00206464 — RAM (r1)
- 0x20201f00 — RAM (r7)

## Вызовы (callees)

- 0x01647fa4 (bl, вне списка функций)
- 0x017f416e (bl, вне списка функций)
- 0x017f41ec (bl, вне списка функций)
- 0x017f41f8 (bl, вне списка функций)
- 0x017f4200 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  018099f8:  push {r4, r5, r6, r7, lr}         
  018099fa:  sub sp, #0x64                     
  018099fc:  movs r2, #0x18                    
  018099fe:  ldr r1, [pc, #0xf0]               (RAM)
  01809a00:  add r0, sp, #0x4c                 
  01809a02:  bl #0x1647fa4                     
  01809a06:  ldr r1, [pc, #0xe8]               (RAM)
  01809a08:  movs r2, #0x44                    
  01809a0a:  adds r1, #0x18                    
  01809a0c:  add r0, sp, #8                    
  01809a0e:  bl #0x1647fa4                     
  01809a12:  ldr r1, [pc, #0xe0]               
  01809a14:  movw r0, #0xfffe                  
  01809a18:  ldr r2, [sp, #0x14]               
  01809a1a:  ands r1, r0                       
  01809a1c:  bfi r2, r1, #0, #0x18             
  01809a20:  ldr r1, [pc, #0xd4]               
  01809a22:  str r2, [sp, #0x14]               
  01809a24:  ldr r2, [sp, #0x1c]               
  01809a26:  ands r1, r0                       
  01809a28:  bfi r2, r1, #0, #0x18             
  01809a2c:  ldr r1, [pc, #0xcc]               
  01809a2e:  str r2, [sp, #0x1c]               
  01809a30:  ldr r2, [sp, #0x24]               
  01809a32:  ands r1, r0                       
  01809a34:  bfi r2, r1, #0, #0x18             
  01809a38:  ldr r1, [pc, #0xc4]               
  01809a3a:  str r2, [sp, #0x24]               
  01809a3c:  ldr r2, [sp, #0x2c]               
  01809a3e:  ands r1, r0                       
  01809a40:  bfi r2, r1, #0, #0x18             
  01809a44:  ldr r1, [pc, #0xbc]               
  01809a46:  str r2, [sp, #0x2c]               
  01809a48:  ands r1, r0                       
  01809a4a:  ldr r0, [sp, #0x34]               
  01809a4c:  bfi r0, r1, #0, #0x18             
  01809a50:  str r0, [sp, #0x34]               
  01809a52:  bl #0x17f41ec                     
  01809a56:  movs r4, #0                       
  01809a58:  ldr r7, [pc, #0xac]               (RAM)
  01809a5a:  movs r5, #1                       
  01809a5c:  add r6, sp, #8                    
  01809a5e:  ldr r1, [sp, #8]                  
  01809a60:  lsl.w r0, r5, r4                  
  01809a64:  tst.w r0, r1, lsr #24             
  01809a68:  beq #0x1809a8e                    
  01809a6a:  add.w r1, r6, r4, lsl #3          
  01809a6e:  ldr r0, [r1, #4]                  
  01809a70:  lsrs r2, r0, #0x18                
  01809a72:  beq #0x1809a76                    
  01809a74:  movs r2, #1                       
  01809a76:  uxtb r3, r4                       
  01809a78:  strd r3, r2, [sp]                 
  01809a7c:  ldr r3, [r1, #8]                  
  01809a7e:  add r1, sp, #0x4c                 
  01809a80:  ldr.w r2, [r1, r4, lsl #2]        
  01809a84:  bic r1, r0, #0xff000000           
  01809a88:  mov r0, r7                        
  01809a8a:  bl #0x17f416e                     
  01809a8e:  adds r4, r4, #1                   
  01809a90:  cmp r4, #6                        
  01809a92:  blt #0x1809a5e                    
  01809a94:  mov r0, r7                        
  01809a96:  bl #0x17f4200                     
  01809a9a:  bl #0x17f41f8                     
  01809a9e:  add sp, #0x64                     
  01809aa0:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x09af0 (7 слов) — ВНЕ границ функции ---
  09af0:  .word 0x00206464  ; RAM
  09af4:  .word 0x00009e01
  09af8:  .word 0x0000a315
  09afc:  .word 0x0000a39d
  09b00:  .word 0x0000a359
  09b04:  .word 0x0000a4cd
  09b08:  .word 0x20201f00  ; RAM
```
