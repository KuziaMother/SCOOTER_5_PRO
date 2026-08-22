# func_0x08d24

| | |
|---|---|
| offset в файле | `0x08d24` |
| vaddr (база 0x01800000) | `0x01808d24` |
 | размер кода | 124 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00206739 — RAM (ip)
- 0x21600002 — прочее (r6)

## Вызовы (callees)

- 0x015f5b92 (bl, вне списка функций)
- 0x01808bae (b, вне списка функций)
- 0x01808d46 (b, вне списка функций)
- 0x01808d9c (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08da0` (bl @0x01808dbe)

## Дизассембляция

```asm
  01808d24:  push.w {r0, r1, r2, r3, r4, r5, r6, r7, r8, lr}
  01808d28:  ldr r6, [pc, #0x104]              
  01808d2a:  ldr r5, [sp, #0x28]               
  01808d2c:  movw r7, #0x44c                   
  01808d30:  cmp r0, r1                        
  01808d32:  bls #0x1808d4a                    
  01808d34:  stm.w sp, {r1, r2, r3, r5}        
  01808d38:  mov r3, r0                        
  01808d3a:  movs r2, #5                       
  01808d3c:  mov r1, r7                        
  01808d3e:  mov r0, r6                        
  01808d40:  bl #0x15f5b92                     
  01808d44:  movs r0, #1                       
  01808d46:  add sp, #0x10                     
  01808d48:  b #0x1808bae                      -> 0x08bae (вне списка функций)
  01808d4a:  movs r4, #0                       
  01808d4c:  ldr.w ip, [pc, #0x104]            (RAM)
  01808d50:  cmp r2, #9                        
  01808d52:  bhs #0x1808d98                    
  01808d54:  tbb [pc, r2]                      
  01808d58:  subs r5, r0, r4                   
  01808d5a:  subs r5, r0, r4                   
  01808d5c:  subs r5, r0, r4                   
  01808d5e:  lsls r5, r0, #0x14                
  01808d60:  movs r5, r0                       
  01808d62:  ldrb.w ip, [ip, r2]               
  01808d66:  cmp ip, r3                        
  01808d68:  bhi #0x1808d7a                    
  01808d6a:  ldr.w ip, [pc, #0xe8]             (RAM)
  01808d6e:  add.w ip, ip, #9                  
  01808d72:  ldrb.w ip, [ip, r2]               
  01808d76:  cmp ip, r3                        
  01808d78:  bhs #0x1808d9c                    
  01808d7a:  stm.w sp, {r1, r2, r3, r5}        
  01808d7e:  mov r3, r0                        
  01808d80:  movs r4, #1                       
  01808d82:  movs r2, #5                       
  01808d84:  mov r1, r7                        
  01808d86:  mov r0, r6                        
  01808d88:  bl #0x15f5b92                     
  01808d8c:  b #0x1808d9c                      -> 0x08d9c (вне списка функций)
  01808d8e:  ldrb.w ip, [ip, r2]               
  01808d92:  cmp ip, r3                        
  01808d94:  bne #0x1808d7a                    
  01808d96:  b #0x1808d9c                      -> 0x08d9c (вне списка функций)
  01808d98:  cmp r3, #0                        
  01808d9a:  beq #0x1808d7a                    
  01808d9c:  mov r0, r4                        
  01808d9e:  b #0x1808d46                      -> 0x08d46 (вне списка функций)
  ; --- literal-пул @0x08e30 (1 слов) — ВНЕ границ функции ---
  08e30:  .word 0x21600002
  ; --- literal-пул @0x08e54 (1 слов) — ВНЕ границ функции ---
  08e54:  .word 0x00206739  ; RAM
```
