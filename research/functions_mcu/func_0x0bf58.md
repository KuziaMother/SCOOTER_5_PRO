# func_0x0bf58

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000bf58) | `0x0000bf58` |
| размер кода | 184 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x0c016 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x048f8` (bl @0x0000491a)
- `func_0x05274` (bl @0x00005298)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0bfa0..0x0bfaa` (10 Б); цели из: 0x0bf98
- `0x0bfaa..0x0bfb4` (10 Б); цели из: 0x0bfa2
- `0x0bfb4..0x0bfc0` (12 Б); цели из: 0x0bfac
- `0x0bfc0..0x0bff4` (52 Б); цели из: 0x0bf6c
- `0x0bff4..0x0bffe` (10 Б); цели из: 0x0bfec
- `0x0bffe..0x0c008` (10 Б); цели из: 0x0bff6
- `0x0c008..0x0c010` (8 Б); цели из: 0x0c000

## Дизассембляция

```asm
  0bf58:  push.w {r4, r5, r6, r7, r8, lr}   
  0bf5c:  mov r4, r0                        
  0bf5e:  mov r5, r1                        
  0bf60:  mov r7, r2                        
  0bf62:  movs r6, #0                       
  0bf64:  mov r8, r6                        
  0bf66:  cbnz r4, #0xbf6a                  
  0bf68:  movs r6, #0xff                    
  0bf6a:  cmp r7, #1                        
  0bf6c:  bne #0xbfc0                       
  0bf6e:  ldrb r0, [r4]                     
  0bf70:  ubfx r0, r0, #1, #1               
  0bf74:  lsls r0, r0, #3                   
  0bf76:  ldrb r1, [r4]                     
  0bf78:  and r1, r1, #1                    
  0bf7c:  orr.w r0, r0, r1, lsl #2          
  0bf80:  ldrb r1, [r4]                     
  0bf82:  ubfx r1, r1, #3, #1               
  0bf86:  orr.w r0, r0, r1, lsl #1          
  0bf8a:  ldrb r1, [r4]                     
  0bf8c:  ubfx r1, r1, #2, #1               
  0bf90:  orrs r0, r1                       
  0bf92:  mvns r0, r0                       
  0bf94:  uxtb r6, r0                       
  0bf96:  cmp r5, #3                        
  0bf98:  bne #0xbfa0                       
  0bf9a:  and r6, r6, #0xf7                 
  0bf9e:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0bfa0:  cmp r5, #2                        
  0bfa2:  bne #0xbfaa                       
  0bfa4:  and r6, r6, #0xfb                 
  0bfa8:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0bfaa:  cmp r5, #1                        
  0bfac:  bne #0xbfb4                       
  0bfae:  and r6, r6, #0xfd                 
  0bfb2:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0bfb4:  cbnz r5, #0xbfbc                  
  0bfb6:  and r6, r6, #0xfe                 
  0bfba:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0bfbc:  movs r6, #0xff                    
  0bfbe:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0bfc0:  cbnz r7, #0xc014                  
  0bfc2:  ldrb r0, [r4]                     
  0bfc4:  ubfx r0, r0, #1, #1               
  0bfc8:  lsls r0, r0, #3                   
  0bfca:  ldrb r1, [r4]                     
  0bfcc:  and r1, r1, #1                    
  0bfd0:  orr.w r0, r0, r1, lsl #2          
  0bfd4:  ldrb r1, [r4]                     
  0bfd6:  ubfx r1, r1, #3, #1               
  0bfda:  orr.w r0, r0, r1, lsl #1          
  0bfde:  ldrb r1, [r4]                     
  0bfe0:  ubfx r1, r1, #2, #1               
  0bfe4:  orrs r0, r1                       
  0bfe6:  mvns r0, r0                       
  0bfe8:  uxtb r6, r0                       
  0bfea:  cmp r5, #3                        
  0bfec:  bne #0xbff4                       
  0bfee:  orr r6, r6, #8                    
  0bff2:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0bff4:  cmp r5, #2                        
  0bff6:  bne #0xbffe                       
  0bff8:  orr r6, r6, #4                    
  0bffc:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0bffe:  cmp r5, #1                        
  0c000:  bne #0xc008                       
  0c002:  orr r6, r6, #2                    
  0c006:  b #0xc016                         -> 0x0c016 (вне списка функций)
  0c008:  cbnz r5, #0xc010                  
  0c00a:  orr r6, r6, #1                    
  0c00e:  b #0xc016                         -> 0x0c016 (вне списка функций)
```
