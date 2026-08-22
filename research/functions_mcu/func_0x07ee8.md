# func_0x07ee8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080007ee8) | `0x00007ee8` |
| размер кода | 58 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x08884` (bl @0x0000889c)
- `func_0x08884` (bl @0x000088d4)


## Дизассембляция

```asm
  07ee8:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, lr}
  07eec:  subw sp, sp, #0x804               
  07ef0:  mov r4, r0                        
  07ef2:  mov r5, r1                        
  07ef4:  mov r6, r2                        
  07ef6:  mov r7, r3                        
  07ef8:  mov.w r1, #0x800                  
  07efc:  add r0, sp, #4                    
  07efe:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  07f02:  movs r0, #0                       
  07f04:  str r0, [sp]                      
  07f06:  mov sb, r0                        
  07f08:  mov r8, r0                        
  07f0a:  mov sl, r0                        
  07f0c:  mov fp, r0                        
  07f0e:  adds r0, r4, r6                   
  07f10:  cmp.w r0, #0x800                  
  07f14:  bgt #0x7f18                       
  07f16:  cbnz r5, #0x7f22                  
  07f18:  movs r0, #0                       
  07f1a:  addw sp, sp, #0x804               
  07f1e:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, pc}
```
