# func_0x08bb6

| | |
|---|---|
| offset в файле | `0x08bb6` |
| vaddr (база 0x01800000) | `0x01808bb6` |
 | размер кода | 68 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x01808bee (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01808bb6:  push {r4, r5, lr}                 
  01808bb8:  mls r0, r1, r0, r3                
  01808bbc:  mov.w r5, #0x4000000              
  01808bc0:  lsls r4, r5, #1                   
  01808bc2:  uxth r0, r0                       
  01808bc4:  cmp r3, r2                        
  01808bc6:  bhs #0x1808bd6                    
  01808bc8:  subs r2, r2, r3                   
  01808bca:  cmp r2, r5                        
  01808bcc:  blo #0x1808bf8                    
  01808bce:  subs r0, r0, r1                   
  01808bd0:  bic r0, r0, #0xf8000000           
  01808bd4:  b #0x1808bee                      -> 0x08bee (вне списка функций)
  01808bd6:  cmp r2, r3                        
  01808bd8:  bhs #0x1808bf8                    
  01808bda:  subs r2, r3, r2                   
  01808bdc:  cmp r2, r5                        
  01808bde:  blo #0x1808bf8                    
  01808be0:  udiv r2, r4, r1                   
  01808be4:  mls r2, r1, r2, r4                
  01808be8:  subs r2, r1, r2                   
  01808bea:  uxth r2, r2                       
  01808bec:  add r0, r2                        
  01808bee:  udiv r2, r0, r1                   
  01808bf2:  mls r0, r1, r2, r0                
  01808bf6:  uxth r0, r0                       
  01808bf8:  pop {r4, r5, pc}                  
```
