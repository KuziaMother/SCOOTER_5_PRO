# func_0x0ca3c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ca3c) | `0x0000ca3c` |
| размер кода | 144 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40002808 — периферия (r0)

## Вызовы (callees)

- `func_0x0c9a8` (0x0000c9a8, bl)
- `func_0x0c9be` (0x0000c9be, bl)
- 0x0ca5c (b, вне списка функций)
- 0x0ca78 (b, вне списка функций)
- 0x0ca7a (b, вне списка функций)
- 0x0cab6 (b, вне списка функций)
- 0x0caf4 (b, вне списка функций)
- `func_0x0cbb8` (0x0000cbb8, bl)

## Кто вызывает (callers / xrefs)

- `func_0x031dc` (bl @0x00003218)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0ca5c..0x0ca78` (28 Б); цели из: 0x0ca54
- `0x0ca78..0x0ca7a` (2 Б); цели из: 0x0ca70
- `0x0ca7a..0x0cab6` (60 Б); цели из: 0x0ca5c
- `0x0cab6..0x0cacc` (22 Б); цели из: 0x0ca90

## Дизассембляция

```asm
  0ca3c:  push.w {r4, r5, r6, r7, r8, lr}   
  0ca40:  mov r5, r0                        
  0ca42:  mov r4, r1                        
  0ca44:  movs r6, #0                       
  0ca46:  movs r7, #0                       
  0ca48:  cbnz r5, #0xca5e                  
  0ca4a:  ldr r0, [pc, #0xbc]               -> периферия
  0ca4c:  ldr r0, [r0]                      
  0ca4e:  and r0, r0, #0x40                 
  0ca52:  cbz r0, #0xca56                   
  0ca54:  b #0xca5c                         -> 0x0ca5c (вне списка функций)
  0ca56:  movs r0, #0                       
  0ca58:  strb r0, [r4, #3]                 
  0ca5a:  nop                               
  0ca5c:  b #0xca7a                         -> 0x0ca7a (вне списка функций)
  0ca5e:  ldr r0, [pc, #0xa8]               -> периферия
  0ca60:  ldr r0, [r0]                      
  0ca62:  and r0, r0, #0x40                 
  0ca66:  cbz r0, #0xca72                   
  0ca68:  ldrb r0, [r4]                     
  0ca6a:  bl #0xc9a8                        -> func_0x0c9a8
  0ca6e:  mov r6, r0                        
  0ca70:  b #0xca78                         -> 0x0ca78 (вне списка функций)
  0ca72:  movs r0, #0                       
  0ca74:  strb r0, [r4, #3]                 
  0ca76:  nop                               
  0ca78:  nop                               
  0ca7a:  cbz r5, #0xca92                   
  0ca7c:  ldrb r0, [r4]                     
  0ca7e:  lsls r0, r0, #0x10                
  0ca80:  ldrb r1, [r4, #1]                 
  0ca82:  orr.w r0, r0, r1, lsl #8          
  0ca86:  ldrb r1, [r4, #2]                 
  0ca88:  orrs r0, r1                       
  0ca8a:  ldrb r1, [r4, #3]                 
  0ca8c:  orr.w r6, r0, r1, lsl #16         
  0ca90:  b #0xcab6                         -> 0x0cab6 (вне списка функций)
  0ca92:  ldrb r0, [r4]                     
  0ca94:  bl #0xc9be                        -> func_0x0c9be
  0ca98:  lsl.w r8, r0, #0x10               
  0ca9c:  ldrb r0, [r4, #1]                 
  0ca9e:  bl #0xc9be                        -> func_0x0c9be
  0caa2:  orr.w r8, r8, r0, lsl #8          
  0caa6:  ldrb r0, [r4, #2]                 
  0caa8:  bl #0xc9be                        -> func_0x0c9be
  0caac:  orr.w r8, r8, r0                  
  0cab0:  ldrb r0, [r4, #3]                 
  0cab2:  orr.w r6, r8, r0, lsl #16         
  0cab6:  movs r0, #0xca                    
  0cab8:  ldr r1, [pc, #0x4c]               -> периферия
  0caba:  adds r1, #0x1c                    
  0cabc:  str r0, [r1]                      
  0cabe:  movs r0, #0x53                    
  0cac0:  str r0, [r1]                      
  0cac2:  bl #0xcbb8                        -> func_0x0cbb8
  0cac6:  cbnz r0, #0xcacc                  
  0cac8:  movs r7, #0                       
  0caca:  b #0xcaf4                         -> 0x0caf4 (вне списка функций)
  ; --- literal-пул @0x0cb08 (1 слов) — ВНЕ границ функции ---
  0cb08:  .word 0x40002808  ; периферия
```
