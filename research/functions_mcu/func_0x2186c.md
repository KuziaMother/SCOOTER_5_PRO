# func_0x2186c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08002186c) | `0x0002186c` |
| размер кода | 370 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x200002b0 — RAM (r5)
- 0x200002b2 — RAM (r0)
- 0x200002b3 — RAM (r0)
- 0x200002b4 — RAM (r4)
- 0x200002b5 — RAM (r0)
- 0x200002b6 — RAM (r6)
- 0x200002b7 — RAM (r0)
- 0x200002b8 — RAM (r1)
- 0x200002b9 — RAM (r1)
- 0x200002ba — RAM (r1)

## Вызовы (callees)

- 0x19968 (bl, вне списка функций)
- 0x21922 (b, вне списка функций)
- 0x21972 (b, вне списка функций)
- 0x21992 (b, вне списка функций)
- 0x2199a (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x1dfd8` (bl @0x0001dfe6)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x218ee..0x21904` (22 Б); цели из: 0x218d6
- `0x21904..0x2192c` (40 Б); цели из: 0x21900
- `0x2192c..0x2193c` (16 Б); цели из: 0x21906
- `0x2193c..0x21956` (26 Б); цели из: 0x2192e
- `0x21956..0x21958` (2 Б); цели из: 0x21878, 0x2188a, 0x2189a, 0x218da…
- `0x21958..0x2195e` (6 Б); цели из: 0x2193a, 0x21948
- `0x2195e..0x21964` (6 Б); цели из: 0x2190c, 0x21910, 0x21914, 0x21918
- `0x21964..0x21972` (14 Б); цели из: 0x218ea
- `0x21972..0x2199a` (40 Б); цели из: 0x218ec, 0x2196e
- `0x2199a..0x219a2` (8 Б); цели из: 0x2192a
- `0x219a2..0x219b2` (16 Б); цели из: 0x21976
- `0x219b2..0x219ce` (28 Б); цели из: 0x219a4
- `0x219ce..0x219d6` (8 Б); цели из: 0x219b0, 0x219be
- `0x219d6..0x219de` (8 Б); цели из: 0x2197a, 0x2197e, 0x21982, 0x21986

## Дизассембляция

```asm
  2186c:  push {r3, r4, r5, r6, r7, lr}     
  2186e:  ldr r1, [pc, #0x170]              -> RAM
  21870:  movs r2, #0x7d                    
  21872:  ldrh r0, [r1]                     
  21874:  lsls r2, r2, #3                   
  21876:  cmp r0, r2                        
  21878:  blo #0x21956                      
  2187a:  movs r0, #0                       
  2187c:  strh r0, [r1]                     
  2187e:  ldr r1, [pc, #0x164]              -> RAM
  21880:  ldrb r2, [r1]                     
  21882:  adds r2, r2, #1                   
  21884:  uxtb r2, r2                       
  21886:  strb r2, [r1]                     
  21888:  cmp r2, #0x3c                     
  2188a:  blo #0x21956                      
  2188c:  strb r0, [r1]                     
  2188e:  ldr r1, [pc, #0x158]              -> RAM
  21890:  ldrb r2, [r1]                     
  21892:  adds r2, r2, #1                   
  21894:  uxtb r2, r2                       
  21896:  strb r2, [r1]                     
  21898:  cmp r2, #0x3c                     
  2189a:  blo #0x21956                      
  2189c:  strb r0, [r1]                     
  2189e:  ldr r0, [pc, #0x14c]              -> RAM
  218a0:  ldr r4, [pc, #0x150]              -> RAM
  218a2:  ldrb r1, [r0]                     
  218a4:  ldr r5, [pc, #0x158]              -> RAM
  218a6:  adds r1, r1, #1                   
  218a8:  uxtb r6, r1                       
  218aa:  strb r6, [r0]                     
  218ac:  ldr r0, [pc, #0x140]              -> RAM
  218ae:  ldrh r7, [r5]                     
  218b0:  ldrb r3, [r0]                     
  218b2:  ldrb r0, [r4]                     
  218b4:  adds r5, r7, #1                   
  218b6:  adds r0, r0, #1                   
  218b8:  uxtb r0, r0                       
  218ba:  mov ip, r0                        
  218bc:  ldr r0, [pc, #0x138]              -> RAM
  218be:  uxth r5, r5                       
  218c0:  ldrb r0, [r0]                     
  218c2:  mov lr, r5                        
  218c4:  adds r0, r0, #1                   
  218c6:  uxtb r1, r0                       
  218c8:  ldr r0, [pc, #0x130]              -> RAM
  218ca:  movs r5, #1                       
  218cc:  ldrb r0, [r0]                     
  218ce:  adds r2, r0, #1                   
  218d0:  cmp r3, #1                        
  218d2:  ldr r3, [pc, #0x118]              -> RAM
  218d4:  uxtb r2, r2                       
  218d6:  beq #0x218ee                      
  218d8:  cmp r6, #0xc                      
  218da:  blo #0x21956                      
  218dc:  movs r6, #0                       
  218de:  strb r6, [r3]                     
  218e0:  ldr r6, [pc, #0x120]              -> RAM
  218e2:  ldrb r3, [r6]                     
  218e4:  adds r3, r3, #1                   
  218e6:  ands r3, r5                       
  218e8:  strb r3, [r6]                     
  218ea:  beq #0x21964                      
  218ec:  b #0x21972                        -> 0x21972 (вне списка функций)
  218ee:  cmp r6, #0x18                     
  218f0:  blo #0x21956                      
  218f2:  movs r6, #0                       
  218f4:  strb r6, [r3]                     
  218f6:  mov r6, ip                        
  218f8:  ldr r3, [pc, #0xfc]               -> RAM
  218fa:  strb r6, [r4]                     
  218fc:  strb r1, [r3]                     
  218fe:  cmp r1, #7                        
  21900:  bls #0x21904                      
  21902:  strb r5, [r3]                     
  21904:  cmp r0, #2                        
  21906:  beq #0x2192c                      
  21908:  ldr r1, [pc, #0xf0]               -> RAM
  2190a:  cmp r0, #4                        
  2190c:  beq #0x2195e                      
  2190e:  cmp r0, #6                        
  21910:  beq #0x2195e                      
  21912:  cmp r0, #9                        
  21914:  beq #0x2195e                      
  21916:  cmp r0, #0xb                      
  21918:  beq #0x2195e                      
  2191a:  cmp r6, #0x1f                     
  2191c:  bls #0x21922                      
  2191e:  strb r5, [r4]                     
  21920:  strb r2, [r1]                     
  21922:  ldrb r0, [r1]                     
  21924:  cmp r0, #0xc                      
  21926:  bls #0x21956                      
  21928:  strb r5, [r1]                     
  2192a:  b #0x2199a                        -> 0x2199a (вне списка функций)
  2192c:  lsls r0, r7, #0x1e                
  2192e:  bne #0x2193c                      
  21930:  movs r1, #0x64                    
  21932:  mov r0, r7                        
  21934:  bl #0x19968                       -> 0x19968 (вне списка функций)
  21938:  cmp r1, #0                        
  2193a:  bne #0x21958                      
  2193c:  movs r1, #0xff                    
  2193e:  adds r1, #0x91                    
  21940:  mov r0, r7                        
  21942:  bl #0x19968                       -> 0x19968 (вне списка функций)
  21946:  cmp r1, #0                        
  21948:  beq #0x21958                      
  2194a:  cmp r6, #0x1c                     
  2194c:  bls #0x21956                      
  2194e:  ldr r0, [pc, #0xac]               -> RAM
  21950:  strb r5, [r4]                     
  21952:  movs r1, #3                       
  21954:  strb r1, [r0]                     
  21956:  pop {r3, r4, r5, r6, r7, pc}      
  21958:  cmp r6, #0x1d                     
  2195a:  bhi #0x2194e                      
  2195c:  pop {r3, r4, r5, r6, r7, pc}      
  2195e:  cmp r6, #0x1e                     
  21960:  bhi #0x2191e                      
  21962:  b #0x21922                        -> 0x21922 (вне списка функций)
  21964:  mov r3, ip                        
  21966:  strb r3, [r4]                     
  21968:  ldr r3, [pc, #0x8c]               -> RAM
  2196a:  cmp r1, #7                        
  2196c:  strb r1, [r3]                     
  2196e:  bls #0x21972                      
  21970:  strb r5, [r3]                     
  21972:  ldr r6, [pc, #0x88]               -> RAM
  21974:  cmp r0, #2                        
  21976:  beq #0x219a2                      
  21978:  cmp r0, #4                        
  2197a:  beq #0x219d6                      
  2197c:  cmp r0, #6                        
  2197e:  beq #0x219d6                      
  21980:  cmp r0, #9                        
  21982:  beq #0x219d6                      
  21984:  cmp r0, #0xb                      
  21986:  beq #0x219d6                      
  21988:  ldrb r0, [r4]                     
  2198a:  cmp r0, #0x1f                     
  2198c:  bls #0x21992                      
  2198e:  strb r5, [r4]                     
  21990:  strb r2, [r6]                     
  21992:  ldrb r0, [r6]                     
  21994:  cmp r0, #0xc                      
  21996:  bls #0x2195c                      
  21998:  strb r5, [r6]                     
  2199a:  ldr r0, [pc, #0x64]               -> RAM
  2199c:  mov r1, lr                        
  2199e:  strh r1, [r0]                     
  219a0:  pop {r3, r4, r5, r6, r7, pc}      
  219a2:  lsls r0, r7, #0x1e                
  219a4:  bne #0x219b2                      
  219a6:  movs r1, #0x64                    
  219a8:  mov r0, r7                        
  219aa:  bl #0x19968                       -> 0x19968 (вне списка функций)
  219ae:  cmp r1, #0                        
  219b0:  bne #0x219ce                      
  219b2:  movs r1, #0xff                    
  219b4:  adds r1, #0x91                    
  219b6:  mov r0, r7                        
  219b8:  bl #0x19968                       -> 0x19968 (вне списка функций)
  219bc:  cmp r1, #0                        
  219be:  beq #0x219ce                      
  219c0:  ldrb r0, [r4]                     
  219c2:  cmp r0, #0x1c                     
  219c4:  bls #0x219a0                      
  219c6:  strb r5, [r4]                     
  219c8:  movs r0, #3                       
  219ca:  strb r0, [r6]                     
  219cc:  pop {r3, r4, r5, r6, r7, pc}      
  219ce:  ldrb r0, [r4]                     
  219d0:  cmp r0, #0x1d                     
  219d2:  bhi #0x219c6                      
  219d4:  pop {r3, r4, r5, r6, r7, pc}      
  219d6:  ldrb r0, [r4]                     
  219d8:  cmp r0, #0x1e                     
  219da:  bhi #0x2198e                      
  219dc:  b #0x21992                        -> 0x21992 (вне списка функций)
  ; --- literal-пул @0x219e0 (10 слов) — ВНЕ границ функции ---
  219e0:  .word 0x200002ba  ; RAM
  219e4:  .word 0x200002b9  ; RAM
  219e8:  .word 0x200002b8  ; RAM
  219ec:  .word 0x200002b7  ; RAM
  219f0:  .word 0x200002b5  ; RAM
  219f4:  .word 0x200002b4  ; RAM
  219f8:  .word 0x200002b3  ; RAM
  219fc:  .word 0x200002b2  ; RAM
  21a00:  .word 0x200002b0  ; RAM
  21a04:  .word 0x200002b6  ; RAM
```
