# func_0x1bd88

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001bd88) | `0x0001bd88` |
| размер кода | 118 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00002328 — данные @0x02328 (r1)
- 0x00003ce4 — данные @0x03ce4 (r2)
- 0x0000dfff — данные @0x0dfff (r2)
- 0x20000382 — RAM (r0)
- 0x20000384 — RAM (r0)
- 0x20000386 — RAM (r0)
- 0x40012c40 — периферия (r3)

## Вызовы (callees)

- 0x1bddc (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a938` (bl @0x0001b610)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x1bdbe..0x1bdc6` (8 Б); цели из: 0x1bdb8
- `0x1bdc6..0x1bdca` (4 Б); цели из: 0x1bdc0
- `0x1bdca..0x1bdd2` (8 Б); цели из: 0x1bdb4
- `0x1bdd2..0x1bdda` (8 Б); цели из: 0x1bdcc
- `0x1bdda..0x1bddc` (2 Б); цели из: 0x1bdd4
- `0x1bddc..0x1bdfc` (32 Б); цели из: 0x1bdbc, 0x1bdc4, 0x1bdc8, 0x1bdd0…
- `0x1bdfc..0x1bdfe` (2 Б); цели из: 0x1bd90

## Дизассембляция

```asm
  1bd88:  push {r4, r5, lr}                 
  1bd8a:  ldr r3, [pc, #0x74]               -> периферия
  1bd8c:  ldr r2, [r3, #0x14]               
  1bd8e:  lsls r2, r2, #0x10                
  1bd90:  bpl #0x1bdfc                      
  1bd92:  movs r4, #0                       
  1bd94:  ldrsh r4, [r1, r4]                
  1bd96:  ldr r2, [pc, #0x6c]               -> данные @0x03ce4
  1bd98:  muls r4, r2, r4                   
  1bd9a:  movs r2, #2                       
  1bd9c:  ldrsh r2, [r1, r2]                
  1bd9e:  ldr r1, [pc, #0x68]               -> данные @0x02328
  1bda0:  muls r2, r1, r2                   
  1bda2:  adds r1, r2, r4                   
  1bda4:  lsrs r5, r1, #0x1f                
  1bda6:  adds r1, r5, r1                   
  1bda8:  subs r4, r2, r4                   
  1bdaa:  lsrs r5, r4, #0x1f                
  1bdac:  adds r4, r5, r4                   
  1bdae:  asrs r1, r1, #1                   
  1bdb0:  asrs r4, r4, #1                   
  1bdb2:  cmp r1, #0                        
  1bdb4:  bge #0x1bdca                      
  1bdb6:  cmp r4, #0                        
  1bdb8:  bge #0x1bdbe                      
  1bdba:  movs r1, #5                       
  1bdbc:  b #0x1bddc                        -> 0x1bddc (вне списка функций)
  1bdbe:  cmp r2, #0                        
  1bdc0:  bgt #0x1bdc6                      
  1bdc2:  movs r1, #4                       
  1bdc4:  b #0x1bddc                        -> 0x1bddc (вне списка функций)
  1bdc6:  movs r1, #3                       
  1bdc8:  b #0x1bddc                        -> 0x1bddc (вне списка функций)
  1bdca:  cmp r4, #0                        
  1bdcc:  blt #0x1bdd2                      
  1bdce:  movs r1, #2                       
  1bdd0:  b #0x1bddc                        -> 0x1bddc (вне списка функций)
  1bdd2:  cmp r2, #0                        
  1bdd4:  bgt #0x1bdda                      
  1bdd6:  movs r1, #6                       
  1bdd8:  b #0x1bddc                        -> 0x1bddc (вне списка функций)
  1bdda:  movs r1, #1                       
  1bddc:  strh r1, [r0, #2]                 
  1bdde:  ldr r0, [pc, #0x20]               -> периферия
  1bde0:  subs r0, #0x40                    
  1bde2:  ldr r1, [r0, #0x30]               
  1bde4:  ldr r2, [pc, #0x24]               -> данные @0x0dfff
  1bde6:  ands r1, r2                       
  1bde8:  str r1, [r0, #0x30]               
  1bdea:  ldr r0, [pc, #0x24]               -> RAM
  1bdec:  ldrh r0, [r0]                     
  1bdee:  str r0, [r3, #4]                  
  1bdf0:  ldr r0, [pc, #0x20]               -> RAM
  1bdf2:  ldrh r0, [r0]                     
  1bdf4:  str r0, [r3, #8]                  
  1bdf6:  ldr r0, [pc, #0x20]               -> RAM
  1bdf8:  ldrh r0, [r0]                     
  1bdfa:  str r0, [r3, #0xc]                
  1bdfc:  pop {r4, r5, pc}                  
  ; --- literal-пул @0x1be00 (7 слов) — ВНЕ границ функции ---
  1be00:  .word 0x40012c40  ; периферия
  1be04:  .word 0x00003ce4  ; данные @0x03ce4
  1be08:  .word 0x00002328  ; данные @0x02328
  1be0c:  .word 0x0000dfff  ; данные @0x0dfff
  1be10:  .word 0x20000386  ; RAM
  1be14:  .word 0x20000384  ; RAM
  1be18:  .word 0x20000382  ; RAM
```
