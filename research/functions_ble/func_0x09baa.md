# func_0x09baa

| | |
|---|---|
| offset в файле | `0x09baa` |
| vaddr (база 0x01800000) | `0x01809baa` |
 | размер кода | 66 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x01809be6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x09bec` (bl @0x01809c5e)

## Дизассембляция

```asm
  01809baa:  push {r4, lr}                     
  01809bac:  mov r3, r0                        
  01809bae:  vldr s2, [pc, #0x364]             
  01809bb2:  movs r0, #0                       
  01809bb4:  mov r2, r0                        
  01809bb6:  b #0x1809be6                      -> 0x09be6 (вне списка функций)
  01809bb8:  add.w r4, r3, r2, lsl #2          
  01809bbc:  vldr s1, [r4]                     
  01809bc0:  vsub.f32 s1, s0, s1               
  01809bc4:  vcmpe.f32 s1, #0                  
  01809bc8:  vmrs apsr_nzcv, fpscr             
  01809bcc:  bge #0x1809bd2                    
  01809bce:  vneg.f32 s1, s1                   
  01809bd2:  vcmpe.f32 s1, s2                  
  01809bd6:  vmrs apsr_nzcv, fpscr             
  01809bda:  bhs #0x1809be2                    
  01809bdc:  vmov.f32 s2, s1                   
  01809be0:  uxtb r0, r2                       
  01809be2:  adds r2, r2, #1                   
  01809be4:  sxtb r2, r2                       
  01809be6:  cmp r2, r1                        
  01809be8:  blt #0x1809bb8                    
  01809bea:  pop {r4, pc}                      
```
