# func_0x0a960

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000a960) | `0x0000a960` |
| размер кода | 170 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0801f000 — flash-mirror @0x1f000 (r1)
- 0x0801f7ff — flash-mirror @0x1f7ff (r2)
- 0x0801ffff — flash-mirror @0x1ffff (r2)

## Вызовы (callees)

- `func_0x062d4` (0x000062d4, bl)
- `func_0x06304` (0x00006304, bl)
- `func_0x06378` (0x00006378, bl)
- 0x0a9b0 (b, вне списка функций)
- 0x0a9f8 (b, вне списка функций)
- 0x0a9fc (b, вне списка функций)
- 0x0aa00 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x0acce` (bl @0x0000ad4e)
- `func_0x0acce` (bl @0x0000ad5a)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0a99e..0x0a9ae` (16 Б); цели из: 0x0a996
- `0x0a9ae..0x0a9b4` (6 Б); цели из: 0x0a980, 0x0a9a4
- `0x0a9b4..0x0a9f2` (62 Б); цели из: 0x0a99c, 0x0a9ac
- `0x0a9f2..0x0a9f8` (6 Б); цели из: 0x0a9e6
- `0x0a9f8..0x0a9fc` (4 Б); цели из: 0x0a9f0
- `0x0a9fc..0x0aa00` (4 Б); цели из: 0x0a9ba
- `0x0aa00..0x0aa0a` (10 Б); цели из: 0x0a9f6

## Дизассембляция

```asm
  0a960:  push.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, lr}
  0a964:  mov r5, r0                        
  0a966:  mov r6, r1                        
  0a968:  mov r4, r2                        
  0a96a:  mov.w r8, #0                      
  0a96e:  mov sb, r8                        
  0a970:  mov sl, r8                        
  0a972:  mov fp, r8                        
  0a974:  movs r7, #0                       
  0a976:  mov sb, r5                        
  0a978:  cbz r6, #0xa9ae                   
  0a97a:  cbz r4, #0xa9ae                   
  0a97c:  cmp.w r4, #0x800                  
  0a980:  bgt #0xa9ae                       
  0a982:  asrs r1, r4, #0x1f                
  0a984:  add.w r1, r4, r1, lsr #30         
  0a988:  asrs r1, r1, #2                   
  0a98a:  sub.w r1, r4, r1, lsl #2          
  0a98e:  cbnz r1, #0xa9ae                  
  0a990:  adds r1, r5, r4                   
  0a992:  ldr r2, [pc, #0x78]               -> flash-mirror @0x1f7ff
  0a994:  cmp r1, r2                        
  0a996:  bhs #0xa99e                       
  0a998:  ldr r1, [pc, #0x74]               -> flash-mirror @0x1f000
  0a99a:  cmp r5, r1                        
  0a99c:  bhs #0xa9b4                       
  0a99e:  adds r1, r5, r4                   
  0a9a0:  ldr r2, [pc, #0x70]               -> flash-mirror @0x1ffff
  0a9a2:  cmp r1, r2                        
  0a9a4:  bhs #0xa9ae                       
  0a9a6:  ldr r1, [pc, #0x64]               -> flash-mirror @0x1f7ff
  0a9a8:  adds r1, r1, #1                   
  0a9aa:  cmp r5, r1                        
  0a9ac:  bhs #0xa9b4                       
  0a9ae:  movs r0, #0                       
  0a9b0:  pop.w {r4, r5, r6, r7, r8, sb, sl, fp, ip, pc}
  0a9b4:  bl #0x6378                        -> func_0x06378
  0a9b8:  movs r7, #0                       
  0a9ba:  b #0xa9fc                         -> 0x0a9fc (вне списка функций)
  0a9bc:  adds r0, r7, #3                   
  0a9be:  ldrb.w r8, [r6, r0]               
  0a9c2:  adds r0, r7, #2                   
  0a9c4:  ldrb r0, [r6, r0]                 
  0a9c6:  add.w r8, r0, r8, lsl #8          
  0a9ca:  adds r0, r7, #1                   
  0a9cc:  ldrb r0, [r6, r0]                 
  0a9ce:  add.w r8, r0, r8, lsl #8          
  0a9d2:  ldrb r0, [r6, r7]                 
  0a9d4:  add.w r8, r0, r8, lsl #8          
  0a9d8:  mov r1, r8                        
  0a9da:  mov r0, sb                        
  0a9dc:  bl #0x6304                        -> func_0x06304
  0a9e0:  mov sl, r0                        
  0a9e2:  cmp.w sl, #6                      
  0a9e6:  bne #0xa9f2                       
  0a9e8:  add.w sb, sb, #4                  
  0a9ec:  mov.w fp, #1                      
  0a9f0:  b #0xa9f8                         -> 0x0a9f8 (вне списка функций)
  0a9f2:  mov.w fp, #0                      
  0a9f6:  b #0xaa00                         -> 0x0aa00 (вне списка функций)
  0a9f8:  adds r0, r7, #4                   
  0a9fa:  uxtb r7, r0                       
  0a9fc:  cmp r7, r4                        
  0a9fe:  blt #0xa9bc                       
  0aa00:  nop                               
  0aa02:  bl #0x62d4                        -> func_0x062d4
  0aa06:  mov r0, fp                        
  0aa08:  b #0xa9b0                         -> 0x0a9b0 (вне списка функций)
  ; --- literal-пул @0x0aa0c (3 слов) — ВНЕ границ функции ---
  0aa0c:  .word 0x0801f7ff  ; flash-mirror @0x1f7ff
  0aa10:  .word 0x0801f000  ; flash-mirror @0x1f000
  0aa14:  .word 0x0801ffff  ; flash-mirror @0x1ffff
```
