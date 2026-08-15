# func_0x16aa2

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080016aa2) | `0x00016aa2` |
| размер кода | 128 Б |
| регион | код G |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x16ad4 (b, вне списка функций)
- 0x16ad8 (b, вне списка функций)
- 0x16b06 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0e3ec` (bl @0x0000e3fc)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x16ab6..0x16ad2` (28 Б); цели из: 0x16aae
- `0x16ad2..0x16ad4` (2 Б); цели из: 0x16acc
- `0x16ad4..0x16ad8` (4 Б); цели из: 0x16ad0
- `0x16ad8..0x16b00` (40 Б); цели из: 0x16ac4
- `0x16b00..0x16b06` (6 Б); цели из: 0x16abc
- `0x16b06..0x16b22` (28 Б); цели из: 0x16ab4, 0x16afe

## Дизассембляция

```asm
  16aa2:  push {r4, r5, r6, r7, lr}         
  16aa4:  mov r5, r0                        
  16aa6:  mov r4, r1                        
  16aa8:  mov r6, r2                        
  16aaa:  ldrh r0, [r4]                     
  16aac:  cmp r0, r5                        
  16aae:  blt #0x16ab6                      
  16ab0:  movs r1, #0                       
  16ab2:  movs r2, #0                       
  16ab4:  b #0x16b06                        -> 0x16b06 (вне списка функций)
  16ab6:  ldrh.w r0, [r4, r3, lsl #1]       
  16aba:  cmp r0, r5                        
  16abc:  ble #0x16b00                      
  16abe:  lsrs r2, r3, #1                   
  16ac0:  movs r1, #0                       
  16ac2:  mov r7, r3                        
  16ac4:  b #0x16ad8                        -> 0x16ad8 (вне списка функций)
  16ac6:  ldrh.w r0, [r4, r2, lsl #1]       
  16aca:  cmp r0, r5                        
  16acc:  ble #0x16ad2                      
  16ace:  mov r7, r2                        
  16ad0:  b #0x16ad4                        -> 0x16ad4 (вне списка функций)
  16ad2:  mov r1, r2                        
  16ad4:  adds r0, r7, r1                   
  16ad6:  lsrs r2, r0, #1                   
  16ad8:  subs r0, r7, r1                   
  16ada:  cmp r0, #1                        
  16adc:  bhi #0x16ac6                      
  16ade:  adds r0, r1, #1                   
  16ae0:  ldrh.w r0, [r4, r0, lsl #1]       
  16ae4:  ldrh.w ip, [r4, r1, lsl #1]       
  16ae8:  sub.w r0, r0, ip                  
  16aec:  uxth r0, r0                       
  16aee:  ldrh.w ip, [r4, r1, lsl #1]       
  16af2:  sub.w ip, r5, ip                  
  16af6:  lsl.w ip, ip, #0x10               
  16afa:  udiv r2, ip, r0                   
  16afe:  b #0x16b06                        -> 0x16b06 (вне списка функций)
  16b00:  subs r1, r3, #1                   
  16b02:  mov.w r2, #0x10000                
  16b06:  adds r0, r1, #1                   
  16b08:  ldrsh.w r0, [r6, r0, lsl #1]      
  16b0c:  ldrsh.w ip, [r6, r1, lsl #1]      
  16b10:  sub.w r0, r0, ip                  
  16b14:  muls r0, r2, r0                   
  16b16:  ldrh.w ip, [r6, r1, lsl #1]       
  16b1a:  add.w r0, ip, r0, asr #16         
  16b1e:  sxth r0, r0                       
  16b20:  pop {r4, r5, r6, r7, pc}          
```
