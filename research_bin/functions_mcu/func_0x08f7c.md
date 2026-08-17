# func_0x08f7c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008f7c) | `0x00008f7c` |
| размер кода | 198 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000dd8 — RAM (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x03c7c` (0x00003c7c, bl)
- 0x08fa8 (b, вне списка функций)
- 0x09030 (b, вне списка функций)
- 0x09034 (b, вне списка функций)
- 0x0903e (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0214c` (bl @0x00002164)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x08fae..0x0902c` (126 Б); цели из: 0x08fa4
- `0x0902c..0x09030` (4 Б); цели из: 0x09026
- `0x09030..0x09034` (4 Б); цели из: 0x09010
- `0x09034..0x0903e` (10 Б); цели из: 0x08ff2
- `0x0903e..0x09042` (4 Б); цели из: 0x09038

## Дизассембляция

```asm
  08f7c:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  08f80:  sub sp, #0x54                     
  08f82:  mov fp, r0                        
  08f84:  mov r5, r1                        
  08f86:  mov r6, r2                        
  08f88:  mov r8, r3                        
  08f8a:  ldr.w sl, [sp, #0x78]             
  08f8e:  movs r7, #0                       
  08f90:  movs r4, #0                       
  08f92:  mov sb, r4                        
  08f94:  movs r1, #0x48                    
  08f96:  add r0, sp, #0xc                  
  08f98:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  08f9c:  lsl.w r0, sl, #0x19               
  08fa0:  lsrs r7, r0, #0x18                
  08fa2:  cmp r7, #0x46                     
  08fa4:  ble #0x8fae                       
  08fa6:  movs r0, #0                       
  08fa8:  add sp, #0x54                     
  08faa:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
  08fae:  movw r0, #0xffff                  
  08fb2:  and.w r5, r0, r5, lsl #1          
  08fb6:  uxtb r0, r5                       
  08fb8:  movs r1, #0                       
  08fba:  bl #0x3c7c                        -> func_0x03c7c
  08fbe:  mov sb, r0                        
  08fc0:  mov r1, sb                        
  08fc2:  mov r0, r6                        
  08fc4:  bl #0x3c7c                        -> func_0x03c7c
  08fc8:  mov sb, r0                        
  08fca:  uxtb r1, r5                       
  08fcc:  orr r0, r1, #1                    
  08fd0:  mov r1, sb                        
  08fd2:  bl #0x3c7c                        -> func_0x03c7c
  08fd6:  mov sb, r0                        
  08fd8:  ldr r0, [pc, #0x68]               -> RAM
  08fda:  strd r7, r0, [sp]                 
  08fde:  uxtb r0, r5                       
  08fe0:  ldr r1, [pc, #0x60]               -> RAM
  08fe2:  add r3, sp, #0xc                  
  08fe4:  movs r2, #1                       
  08fe6:  ldr.w ip, [r1, #0x118]            
  08fea:  mov r1, r6                        
  08fec:  blx ip                            
  08fee:  cbnz r0, #0x903a                  
  08ff0:  movs r4, #0                       
  08ff2:  b #0x9034                         -> 0x09034 (вне списка функций)
  08ff4:  mov r0, r4                        
  08ff6:  add.w r1, r4, r0, lsr #31         
  08ffa:  asrs r1, r1, #1                   
  08ffc:  sub.w r1, r4, r1, lsl #1          
  09000:  cbnz r1, #0x9012                  
  09002:  add r1, sp, #0xc                  
  09004:  ldrb r1, [r1, r4]                 
  09006:  add.w r2, r4, r0, lsr #31         
  0900a:  asrs r2, r2, #1                   
  0900c:  strb.w r1, [r8, r2]               
  09010:  b #0x9030                         -> 0x09030 (вне списка функций)
  09012:  subs r1, r4, #1                   
  09014:  add r2, sp, #0xc                  
  09016:  ldrb r0, [r2, r1]                 
  09018:  mov r1, sb                        
  0901a:  bl #0x3c7c                        -> func_0x03c7c
  0901e:  mov sb, r0                        
  09020:  add r0, sp, #0xc                  
  09022:  ldrb r0, [r0, r4]                 
  09024:  cmp r0, sb                        
  09026:  beq #0x902c                       
  09028:  movs r0, #0                       
  0902a:  b #0x8fa8                         -> 0x08fa8 (вне списка функций)
  0902c:  mov.w sb, #0                      
  09030:  adds r0, r4, #1                   
  09032:  uxtb r4, r0                       
  09034:  cmp r4, r7                        
  09036:  blt #0x8ff4                       
  09038:  b #0x903e                         -> 0x0903e (вне списка функций)
  0903a:  movs r0, #0                       
  0903c:  b #0x8fa8                         -> 0x08fa8 (вне списка функций)
  0903e:  movs r0, #1                       
  09040:  b #0x8fa8                         -> 0x08fa8 (вне списка функций)
  ; --- literal-пул @0x09044 (1 слов) — ВНЕ границ функции ---
  09044:  .word 0x20000dd8  ; RAM
```
