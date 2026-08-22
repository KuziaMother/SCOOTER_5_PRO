# func_0x020d8

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800020d8) | `0x000020d8` |
| размер кода | 76 Б |
| регион | код A |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a71 — RAM (r0)
- 0x20000a7a — RAM (r0)
- 0x20000dd8 — RAM (r0)

## Вызовы (callees)

- 0x0212a (b, вне списка функций)
- `func_0x02a5c` (0x00002a5c, bl)
- `func_0x0af94` (0x0000af94, bl)

## Кто вызывает (callers / xrefs)

- `func_0x01cea` (bl @0x00001cf0)


## Дизассембляция

```asm
  020d8:  push {r3, lr}                     
  020da:  ldr r0, [pc, #0x50]               -> RAM
  020dc:  ldrb r0, [r0]                     
  020de:  ubfx r0, r0, #3, #1               
  020e2:  cbz r0, #0x2124                   
  020e4:  ldr r0, [pc, #0x48]               -> RAM
  020e6:  ldrb r0, [r0]                     
  020e8:  adds r0, r0, #1                   
  020ea:  uxtb r0, r0                       
  020ec:  ldr r1, [pc, #0x40]               -> RAM
  020ee:  strb r0, [r1]                     
  020f0:  cmp r0, #5                        
  020f2:  blt #0x212a                       
  020f4:  movs r0, #0                       
  020f6:  strb r0, [r1]                     
  020f8:  ldr r0, [pc, #0x38]               -> RAM
  020fa:  bl #0xaf94                        -> func_0x0af94
  020fe:  mov.w r0, #0x1f4                  
  02102:  str r0, [sp]                      
  02104:  nop                               
  02106:  ldr r0, [sp]                      
  02108:  subs r1, r0, #1                   
  0210a:  str r1, [sp]                      
  0210c:  cmp r0, #0                        
  0210e:  bne #0x2106                       
  02110:  bl #0x2a5c                        -> func_0x02a5c
  02114:  cbz r0, #0x212a                   
  02116:  ldr r0, [pc, #0x14]               -> RAM
  02118:  ldrb r0, [r0]                     
  0211a:  bic r0, r0, #8                    
  0211e:  ldr r1, [pc, #0xc]                -> RAM
  02120:  strb r0, [r1]                     
  02122:  b #0x212a                         -> 0x0212a (вне списка функций)
  ; --- literal-пул @0x0212c (3 слов) — ВНЕ границ функции ---
  0212c:  .word 0x20000a71  ; RAM
  02130:  .word 0x20000a7a  ; RAM
  02134:  .word 0x20000dd8  ; RAM
```
