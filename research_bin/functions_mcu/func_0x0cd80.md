# func_0x0cd80

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cd80) | `0x0000cd80` |
| размер кода | 136 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40002824 — периферия (r1)

## Вызовы (callees)

- `func_0x0c9a8` (0x0000c9a8, bl)
- `func_0x0c9be` (0x0000c9be, bl)
- `func_0x0cbb8` (0x0000cbb8, bl)
- 0x0cdb8 (b, вне списка функций)
- 0x0cdf4 (b, вне списка функций)
- 0x0ce32 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x031dc` (bl @0x000031fa)
- `func_0x10a5c` (bl @0x00010a84)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0cda2..0x0cdb8` (22 Б); цели из: 0x0cd96
- `0x0cdb8..0x0cdf4` (60 Б); цели из: 0x0cda4
- `0x0cdf4..0x0ce08` (20 Б); цели из: 0x0cdce

## Дизассембляция

```asm
  0cd80:  push.w {r4, r5, r6, r7, r8, lr}   
  0cd84:  mov r5, r0                        
  0cd86:  mov r4, r1                        
  0cd88:  movs r6, #0                       
  0cd8a:  movs r7, #0                       
  0cd8c:  cbnz r5, #0xcda2                  
  0cd8e:  ldrb r0, [r4, #1]                 
  0cd90:  and r0, r0, #0x10                 
  0cd94:  cmp r0, #0x10                     
  0cd96:  bne #0xcda2                       
  0cd98:  ldrb r0, [r4, #1]                 
  0cd9a:  bic r0, r0, #0x10                 
  0cd9e:  adds r0, #0xa                     
  0cda0:  strb r0, [r4, #1]                 
  0cda2:  cbnz r5, #0xcda6                  
  0cda4:  b #0xcdb8                         -> 0x0cdb8 (вне списка функций)
  0cda6:  ldrb r0, [r4, #1]                 
  0cda8:  bl #0xc9a8                        -> func_0x0c9a8
  0cdac:  mov r6, r0                        
  0cdae:  ldrb r0, [r4, #2]                 
  0cdb0:  bl #0xc9a8                        -> func_0x0c9a8
  0cdb4:  mov r6, r0                        
  0cdb6:  nop                               
  0cdb8:  cbz r5, #0xcdd0                   
  0cdba:  ldrb r0, [r4, #3]                 
  0cdbc:  lsls r0, r0, #0x10                
  0cdbe:  ldrb r1, [r4, #1]                 
  0cdc0:  orr.w r0, r0, r1, lsl #8          
  0cdc4:  ldrb r1, [r4, #2]                 
  0cdc6:  orrs r0, r1                       
  0cdc8:  ldrb r1, [r4]                     
  0cdca:  orr.w r6, r0, r1, lsl #13         
  0cdce:  b #0xcdf4                         -> 0x0cdf4 (вне списка функций)
  0cdd0:  ldrb r0, [r4, #3]                 
  0cdd2:  bl #0xc9be                        -> func_0x0c9be
  0cdd6:  lsl.w r8, r0, #0x10               
  0cdda:  ldrb r0, [r4, #1]                 
  0cddc:  bl #0xc9be                        -> func_0x0c9be
  0cde0:  orr.w r8, r8, r0, lsl #8          
  0cde4:  ldrb r0, [r4, #2]                 
  0cde6:  bl #0xc9be                        -> func_0x0c9be
  0cdea:  orr.w r8, r8, r0                  
  0cdee:  ldrb r0, [r4]                     
  0cdf0:  orr.w r6, r8, r0, lsl #13         
  0cdf4:  movs r0, #0xca                    
  0cdf6:  ldr r1, [pc, #0x4c]               -> периферия
  0cdf8:  str r0, [r1]                      
  0cdfa:  movs r0, #0x53                    
  0cdfc:  str r0, [r1]                      
  0cdfe:  bl #0xcbb8                        -> func_0x0cbb8
  0ce02:  cbnz r0, #0xce08                  
  0ce04:  movs r7, #0                       
  0ce06:  b #0xce32                         -> 0x0ce32 (вне списка функций)
  ; --- literal-пул @0x0ce44 (1 слов) — ВНЕ границ функции ---
  0ce44:  .word 0x40002824  ; периферия
```
