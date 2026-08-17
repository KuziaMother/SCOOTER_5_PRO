# func_0x216e4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800216e4) | `0x000216e4` |
| размер кода | 256 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x20000170 — RAM (r1)
- 0x200001e0 — RAM (r4)
- 0x200002c9 — RAM (r1)
- 0x200002ca — RAM (r0)
- 0x20000358 — RAM (r0)
- 0x20000360 — RAM (r4)
- 0x200010b5 — RAM (r1)
- 0x40004c00 — периферия (r0)

## Вызовы (callees)

- `func_0x211ec` (0x000211ec, bl)
- 0x21772 (b, вне списка функций)
- 0x217ca (b, вне списка функций)
- 0x217ce (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1a31c` (bl @0x0001a51c)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x21780..0x217ca` (74 Б); цели из: 0x21726
- `0x217ca..0x217d2` (8 Б); цели из: 0x21778, 0x2177e
- `0x217d2..0x217d6` (4 Б); цели из: 0x216f2, 0x2172a, 0x2174a, 0x2178c…
- `0x217d6..0x217e4` (14 Б); цели из: 0x2175c, 0x2179e

## Дизассембляция

```asm
  216e4:  push {r4, r5, r6, r7, lr}         
  216e6:  ldr r0, [pc, #0xfc]               -> RAM
  216e8:  ldr r1, [pc, #0xfc]               -> RAM
  216ea:  ldrb r0, [r0]                     
  216ec:  ldrb r1, [r1]                     
  216ee:  sub sp, #0x2c                     
  216f0:  cmp r0, r1                        
  216f2:  beq #0x217d2                      
  216f4:  ldr r0, [pc, #0xf4]               -> RAM
  216f6:  movs r5, #0                       
  216f8:  ldrb r4, [r0]                     
  216fa:  ldr r0, [pc, #0xe8]               -> RAM
  216fc:  ldrb r0, [r0]                     
  216fe:  adds r1, r0, #1                   
  21700:  uxtb r1, r1                       
  21702:  mov lr, r1                        
  21704:  movs r1, #0x96                    
  21706:  muls r0, r1, r0                   
  21708:  ldr r1, [pc, #0xe4]               -> RAM
  2170a:  mov ip, r0                        
  2170c:  adds r0, r0, r1                   
  2170e:  ldr r1, [pc, #0xe4]               -> RAM
  21710:  str r0, [sp, #0x20]               
  21712:  ldr r0, [r1, #0x48]               
  21714:  ldr r3, [r1, #0x4c]               
  21716:  mov r1, r0                        
  21718:  mov r2, r3                        
  2171a:  adds r0, r0, #1                   
  2171c:  adcs r3, r5                       
  2171e:  str r3, [sp, #4]                  
  21720:  ldr r3, [pc, #0xd0]               -> RAM
  21722:  cmp r4, #1                        
  21724:  ldrb r3, [r3, #0x19]              
  21726:  beq #0x21780                      
  21728:  cmp r4, #0                        
  2172a:  bne #0x217d2                      
  2172c:  ldr r4, [pc, #0xc8]               -> RAM
  2172e:  ldr r7, [pc, #0xc4]               -> RAM
  21730:  ldr r5, [r4]                      
  21732:  ldr r4, [r4, #4]                  
  21734:  str r5, [sp, #0x18]               
  21736:  str r4, [sp, #0x1c]               
  21738:  ldr r6, [r7, #0x40]               
  2173a:  ldr r7, [r7, #0x44]               
  2173c:  subs r6, r5, r6                   
  2173e:  sbcs r4, r7                       
  21740:  movs r7, #0xff                    
  21742:  adds r7, #0xb1                    
  21744:  movs r5, #0                       
  21746:  subs r6, r7, r6                   
  21748:  sbcs r5, r4                       
  2174a:  bhs #0x217d2                      
  2174c:  ldr r4, [pc, #0xa0]               -> RAM
  2174e:  mov r5, ip                        
  21750:  ldrb r5, [r4, r5]                 
  21752:  ldr r4, [pc, #0xa0]               -> RAM
  21754:  ldr r6, [pc, #0x8c]               -> RAM
  21756:  strb r5, [r4, #0x18]              
  21758:  adds r5, r5, #1                   
  2175a:  cmp r3, r5                        
  2175c:  blo #0x217d6                      
  2175e:  movs r0, #1                       
  21760:  strb r0, [r4, #0x19]              
  21762:  movs r0, #0xb                     
  21764:  movs r1, #0                       
  21766:  str r1, [r4, #0x4c]               
  21768:  str r0, [r4, #0x48]               
  2176a:  ldr r1, [sp, #0x1c]               
  2176c:  ldr r0, [sp, #0x18]               
  2176e:  str r1, [r4, #0x44]               
  21770:  str r0, [r4, #0x40]               
  21772:  mov r0, lr                        
  21774:  strb r0, [r6]                     
  21776:  cmp r0, #8                        
  21778:  blo #0x217ca                      
  2177a:  movs r0, #0                       
  2177c:  strb r0, [r6]                     
  2177e:  b #0x217ca                        -> 0x217ca (вне списка функций)
  21780:  ldr r4, [pc, #0x78]               -> RAM
  21782:  movs r7, #0x50                    
  21784:  ldm r4!, {r5, r6}                 
  21786:  movs r4, #0                       
  21788:  subs r5, r7, r5                   
  2178a:  sbcs r4, r6                       
  2178c:  bhs #0x217d2                      
  2178e:  ldr r4, [pc, #0x60]               -> RAM
  21790:  mov r5, ip                        
  21792:  ldrb r5, [r4, r5]                 
  21794:  ldr r4, [pc, #0x5c]               -> RAM
  21796:  ldr r6, [pc, #0x4c]               -> RAM
  21798:  strb r5, [r4, #0x18]              
  2179a:  adds r5, r5, #1                   
  2179c:  cmp r3, r5                        
  2179e:  blo #0x217d6                      
  217a0:  movs r0, #1                       
  217a2:  strb r0, [r4, #0x19]              
  217a4:  movs r0, #0xb                     
  217a6:  movs r1, #0                       
  217a8:  str r1, [r4, #0x4c]               
  217aa:  str r0, [r4, #0x48]               
  217ac:  ldr r0, [pc, #0x4c]               -> RAM
  217ae:  mov r2, r1                        
  217b0:  stm r0!, {r1, r2}                 
  217b2:  b #0x21772                        -> 0x21772 (вне списка функций)
  217b4:  ldr r0, [pc, #0x48]               -> периферия
  217b6:  ldr r0, [r0, #0x28]               
  217b8:  lsls r0, r0, #0x11                
  217ba:  bmi #0x217d2                      
  217bc:  ldr r0, [sp, #0x20]               
  217be:  ldrb r0, [r0, r3]                 
  217c0:  bl #0x211ec                       -> func_0x211ec
  217c4:  ldrb r0, [r4, #0x19]              
  217c6:  adds r0, r0, #1                   
  217c8:  strb r0, [r4, #0x19]              
  217ca:  movs r0, #0                       
  217cc:  mov r1, r0                        
  217ce:  str r1, [r4, #0x4c]               
  217d0:  str r0, [r4, #0x48]               
  217d2:  add sp, #0x2c                     
  217d4:  pop {r4, r5, r6, r7, pc}          
  217d6:  movs r6, #8                       
  217d8:  movs r5, #0                       
  217da:  subs r1, r6, r1                   
  217dc:  sbcs r5, r2                       
  217de:  blo #0x217b4                      
  217e0:  ldr r1, [sp, #4]                  
  217e2:  b #0x217ce                        -> 0x217ce (вне списка функций)
  ; --- literal-пул @0x217e4 (8 слов) — ВНЕ границ функции ---
  217e4:  .word 0x200002ca  ; RAM
  217e8:  .word 0x200002c9  ; RAM
  217ec:  .word 0x20000358  ; RAM
  217f0:  .word 0x200010b5  ; RAM
  217f4:  .word 0x20000170  ; RAM
  217f8:  .word 0x200001e0  ; RAM
  217fc:  .word 0x20000360  ; RAM
  21800:  .word 0x40004c00  ; периферия
```
