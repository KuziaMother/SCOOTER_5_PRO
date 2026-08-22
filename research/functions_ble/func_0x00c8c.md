# func_0x00c8c

| | |
|---|---|
| offset в файле | `0x00c8c` |
| vaddr (база 0x01800000) | `0x01800c8c` |
 | размер кода | 92 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x01802a28 (bl, вне списка функций)
- 0x01802bea (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x00ce8` (bl @0x01800d08)

## Дизассембляция

```asm
  01800c8c:  push {r4, r5, r6, lr}             
  01800c8e:  mov r4, r0                        
  01800c90:  ldrh.w r0, [r0, #3]               
  01800c94:  movs r5, #0                       
  01800c96:  cmp.w r0, #0x1000                 
  01800c9a:  bhs #0x1800ca8                    
  01800c9c:  bl #0x1802bea                     -> 0x02bea (вне списка функций)
  01800ca0:  cbz r0, #0x1800ca8                
  01800ca2:  ldr r2, [r0]                      
  01800ca4:  lsls r1, r2, #7                   
  01800ca6:  bmi #0x1800cac                    
  01800ca8:  movs r0, #2                       
  01800caa:  pop {r4, r5, r6, pc}              
  01800cac:  ldrb r1, [r0, #0xc]               
  01800cae:  lsls r1, r1, #0x1e                
  01800cb0:  bmi #0x1800cb6                    
  01800cb2:  movs r0, #0xc                     
  01800cb4:  pop {r4, r5, r6, pc}              
  01800cb6:  ldrh.w r1, [r4, #5]               
  01800cba:  strh.w r1, [r0, #0x13c]           
  01800cbe:  ldrh r3, [r0, #0x2c]              
  01800cc0:  ldrh r0, [r0, #0x30]              
  01800cc2:  add.w r1, r1, r1, lsl #2          
  01800cc6:  adds r0, r0, #1                   
  01800cc8:  add.w r0, r0, r0, lsl #2          
  01800ccc:  lsls r0, r0, #1                   
  01800cce:  muls r3, r0, r3                   
  01800cd0:  asrs r0, r3, #3                   
  01800cd2:  cmp.w r0, r1, lsl #1              
  01800cd6:  ble #0x1800cdc                    
  01800cd8:  movs r0, #0x12                    
  01800cda:  pop {r4, r5, r6, pc}              
  01800cdc:  ubfx r0, r2, #0x10, #8            
  01800ce0:  bl #0x1802a28                     -> 0x02a28 (вне списка функций)
  01800ce4:  mov r0, r5                        
  01800ce6:  pop {r4, r5, r6, pc}              
```
