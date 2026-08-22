# func_0x03c7c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080003c7c) | `0x00003c7c` |
| размер кода | 46 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x03ca0 (b, вне списка функций)
- 0x03ca4 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08f7c` (bl @0x00008fba)
- `func_0x08f7c` (bl @0x00008fc4)
- `func_0x08f7c` (bl @0x00008fd2)
- `func_0x08f7c` (bl @0x0000901a)
- `func_0x15640` (bl @0x0001565a)
- `func_0x15640` (bl @0x00015666)
- `func_0x15640` (bl @0x0001567c)
- `func_0x15640` (bl @0x00015694)


## Дизассембляция

```asm
  03c7c:  push {r4, lr}                     
  03c7e:  mov r2, r0                        
  03c80:  movs r3, #0                       
  03c82:  mov r0, r1                        
  03c84:  nop                               
  03c86:  eors r0, r2                       
  03c88:  nop                               
  03c8a:  b #0x3ca4                         -> 0x03ca4 (вне списка функций)
  03c8c:  and r4, r0, #0x80                 
  03c90:  cbz r4, #0x3c9c                   
  03c92:  lsls r4, r0, #0x19                
  03c94:  lsrs r0, r4, #0x18                
  03c96:  eor r0, r0, #7                    
  03c9a:  b #0x3ca0                         -> 0x03ca0 (вне списка функций)
  03c9c:  lsls r4, r0, #0x19                
  03c9e:  lsrs r0, r4, #0x18                
  03ca0:  adds r4, r3, #1                   
  03ca2:  uxtb r3, r4                       
  03ca4:  cmp r3, #8                        
  03ca6:  blt #0x3c8c                       
  03ca8:  pop {r4, pc}                      
```
