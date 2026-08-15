# func_0x0c02c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000c02c) | `0x0000c02c` |
| размер кода | 92 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000a65 — RAM (r1)
- 0x20000a66 — RAM (r1)
- 0x20000a68 — RAM (r0)
- 0x20000f70 — RAM (r0)

## Вызовы (callees)

- 0x0c086 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0c098` (bl @0x0000c0aa)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0c04c..0x0c074` (40 Б); цели из: 0x0c03a
- `0x0c074..0x0c086` (18 Б); цели из: 0x0c04a
- `0x0c086..0x0c088` (2 Б); цели из: 0x0c05c, 0x0c072

## Дизассембляция

```asm
  0c02c:  ldr r0, [pc, #0x58]               -> RAM
  0c02e:  ldrb r0, [r0, #1]                 
  0c030:  and r0, r0, #1                    
  0c034:  ldr r1, [pc, #0x54]               -> RAM
  0c036:  ldrb r1, [r1]                     
  0c038:  cmp r0, r1                        
  0c03a:  bne #0xc04c                       
  0c03c:  ldr r0, [pc, #0x48]               -> RAM
  0c03e:  ldrb r0, [r0, #1]                 
  0c040:  ubfx r0, r0, #1, #1               
  0c044:  ldr r1, [pc, #0x48]               -> RAM
  0c046:  ldrb r1, [r1]                     
  0c048:  cmp r0, r1                        
  0c04a:  beq #0xc074                       
  0c04c:  ldr r0, [pc, #0x44]               -> RAM
  0c04e:  ldrh r0, [r0]                     
  0c050:  adds r0, r0, #1                   
  0c052:  ldr r1, [pc, #0x40]               -> RAM
  0c054:  strh r0, [r1]                     
  0c056:  mov r0, r1                        
  0c058:  ldrh r0, [r0]                     
  0c05a:  cmp r0, #0x32                     
  0c05c:  blt #0xc086                       
  0c05e:  ldr r0, [pc, #0x28]               -> RAM
  0c060:  ldrb r0, [r0, #3]                 
  0c062:  bic r0, r0, #8                    
  0c066:  adds r0, #8                       
  0c068:  ldr r1, [pc, #0x1c]               -> RAM
  0c06a:  strb r0, [r1, #3]                 
  0c06c:  movs r0, #0x32                    
  0c06e:  ldr r1, [pc, #0x24]               -> RAM
  0c070:  strh r0, [r1]                     
  0c072:  b #0xc086                         -> 0x0c086 (вне списка функций)
  0c074:  movs r0, #0                       
  0c076:  ldr r1, [pc, #0x1c]               -> RAM
  0c078:  strh r0, [r1]                     
  0c07a:  ldr r0, [pc, #0xc]                -> RAM
  0c07c:  ldrb r0, [r0, #3]                 
  0c07e:  bic r0, r0, #8                    
  0c082:  ldr r1, [pc, #4]                  -> RAM
  0c084:  strb r0, [r1, #3]                 
  0c086:  bx lr                             
  ; --- literal-пул @0x0c088 (4 слов) — ВНЕ границ функции ---
  0c088:  .word 0x20000f70  ; RAM
  0c08c:  .word 0x20000a65  ; RAM
  0c090:  .word 0x20000a66  ; RAM
  0c094:  .word 0x20000a68  ; RAM
```
