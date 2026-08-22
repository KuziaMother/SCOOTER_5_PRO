# func_0x07fdc

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007fdc) | `0x00007fdc` |
| размер кода | 56 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08884` (bl @0x00008900)
- `func_0x0c368` (bl @0x0000c3a2)
- `func_0x0c368` (bl @0x0000c3b4)
- `func_0x0c368` (bl @0x0000c3e6)
- `func_0x0c368` (bl @0x0000c3f6)


## Дизассембляция

```asm
  07fdc:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  07fe0:  subw sp, sp, #0x804               
  07fe4:  mov r4, r0                        
  07fe6:  mov r5, r1                        
  07fe8:  mov r6, r2                        
  07fea:  mov r7, r3                        
  07fec:  mov.w r1, #0x800                  
  07ff0:  add r0, sp, #4                    
  07ff2:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  07ff6:  mov.w fp, #0                      
  07ffa:  mov sl, fp                        
  07ffc:  mov r8, sl                        
  07ffe:  mov sb, r8                        
  08000:  adds r0, r4, r6                   
  08002:  cmp.w r0, #0x800                  
  08006:  bgt #0x800a                       
  08008:  cbnz r5, #0x8014                  
  0800a:  movs r0, #0                       
  0800c:  addw sp, sp, #0x804               
  08010:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
```
