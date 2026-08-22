# func_0x105c4

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x0800105c4) | `0x000105c4` |
| размер кода | 194 Б |
| регион | код C |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019daa — flash-mirror @0x19daa (r1)
- 0x20000080 — RAM (r0)
- 0x200009f8 — RAM (r0)
- 0x200009fa — RAM (r1)
- 0x20000f95 — RAM (r0)
- 0x20000fbb — RAM (r0)

## Вызовы (callees)

- 0x1061e (b, вне списка функций)
- 0x10684 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x11998` (bl @0x000119a2)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x105d4..0x10618` (68 Б); цели из: 0x105ca
- `0x10618..0x1061e` (6 Б); цели из: 0x105e8
- `0x1061e..0x1064a` (44 Б); цели из: 0x105d2, 0x105fc, 0x10616
- `0x1064a..0x1067e` (52 Б); цели из: 0x10634
- `0x1067e..0x10684` (6 Б); цели из: 0x10654
- `0x10684..0x10686` (2 Б); цели из: 0x10648, 0x10668, 0x1067c

## Дизассембляция

```asm
  105c4:  ldr r0, [pc, #0xc0]               -> RAM
  105c6:  ldrb r0, [r0]                     
  105c8:  cmp r0, #1                        
  105ca:  beq #0x105d4                      
  105cc:  ldr r0, [pc, #0xb8]               -> RAM
  105ce:  ldrb r0, [r0]                     
  105d0:  cmp r0, #2                        
  105d2:  bne #0x1061e                      
  105d4:  ldr r0, [pc, #0xb4]               -> RAM
  105d6:  ldrb r0, [r0, #0xc]               
  105d8:  ubfx r0, r0, #6, #1               
  105dc:  cbnz r0, #0x1061e                 
  105de:  ldr r0, [pc, #0xac]               -> RAM
  105e0:  ldrh r0, [r0, #4]                 
  105e2:  ldr r1, [pc, #0xac]               -> flash-mirror @0x19daa
  105e4:  ldrh r1, [r1, #0x32]              
  105e6:  cmp r0, r1                        
  105e8:  bgt #0x10618                      
  105ea:  ldr r0, [pc, #0xa8]               -> RAM
  105ec:  ldrh r0, [r0]                     
  105ee:  adds r0, r0, #1                   
  105f0:  ldr r1, [pc, #0xa0]               -> RAM
  105f2:  strh r0, [r1]                     
  105f4:  ldr r0, [pc, #0x98]               -> flash-mirror @0x19daa
  105f6:  ldrh r0, [r0, #0x36]              
  105f8:  ldrh r1, [r1]                     
  105fa:  cmp r0, r1                        
  105fc:  bgt #0x1061e                      
  105fe:  ldr r0, [pc, #0x8c]               -> RAM
  10600:  ldrb r0, [r0, #0xc]               
  10602:  bic r0, r0, #0x40                 
  10606:  adds r0, #0x40                    
  10608:  ldr r1, [pc, #0x80]               -> RAM
  1060a:  strb r0, [r1, #0xc]               
  1060c:  movs r0, #0                       
  1060e:  ldr r1, [pc, #0x84]               -> RAM
  10610:  strh r0, [r1]                     
  10612:  ldr r1, [pc, #0x84]               -> RAM
  10614:  strh r0, [r1]                     
  10616:  b #0x1061e                        -> 0x1061e (вне списка функций)
  10618:  movs r0, #0                       
  1061a:  ldr r1, [pc, #0x78]               -> RAM
  1061c:  strh r0, [r1]                     
  1061e:  ldr r0, [pc, #0x6c]               -> RAM
  10620:  ldrb r0, [r0, #0xc]               
  10622:  ubfx r0, r0, #6, #1               
  10626:  cbz r0, #0x1067c                  
  10628:  ldr r0, [pc, #0x5c]               -> RAM
  1062a:  ldrb r0, [r0]                     
  1062c:  cbnz r0, #0x1064a                 
  1062e:  ldr r0, [pc, #0x6c]               -> RAM
  10630:  ldr r0, [r0, #4]                  
  10632:  cmp r0, #0x64                     
  10634:  blo #0x1064a                      
  10636:  ldr r0, [pc, #0x54]               -> RAM
  10638:  ldrb r0, [r0, #0xc]               
  1063a:  bic r0, r0, #0x40                 
  1063e:  ldr r1, [pc, #0x4c]               -> RAM
  10640:  strb r0, [r1, #0xc]               
  10642:  movs r0, #0                       
  10644:  ldr r1, [pc, #0x50]               -> RAM
  10646:  strh r0, [r1]                     
  10648:  b #0x10684                        -> 0x10684 (вне списка функций)
  1064a:  ldr r0, [pc, #0x40]               -> RAM
  1064c:  ldrh r0, [r0, #4]                 
  1064e:  ldr r1, [pc, #0x40]               -> flash-mirror @0x19daa
  10650:  ldrh r1, [r1, #0x34]              
  10652:  cmp r0, r1                        
  10654:  blt #0x1067e                      
  10656:  ldr r0, [pc, #0x40]               -> RAM
  10658:  ldrh r0, [r0]                     
  1065a:  adds r0, r0, #1                   
  1065c:  ldr r1, [pc, #0x38]               -> RAM
  1065e:  strh r0, [r1]                     
  10660:  ldr r0, [pc, #0x2c]               -> flash-mirror @0x19daa
  10662:  ldrh r0, [r0, #0x38]              
  10664:  ldrh r1, [r1]                     
  10666:  cmp r0, r1                        
  10668:  bgt #0x10684                      
  1066a:  ldr r0, [pc, #0x20]               -> RAM
  1066c:  ldrb r0, [r0, #0xc]               
  1066e:  bic r0, r0, #0x40                 
  10672:  ldr r1, [pc, #0x18]               -> RAM
  10674:  strb r0, [r1, #0xc]               
  10676:  movs r0, #0                       
  10678:  ldr r1, [pc, #0x1c]               -> RAM
  1067a:  strh r0, [r1]                     
  1067c:  b #0x10684                        -> 0x10684 (вне списка функций)
  1067e:  movs r0, #0                       
  10680:  ldr r1, [pc, #0x14]               -> RAM
  10682:  strh r0, [r1]                     
  10684:  bx lr                             
  ; --- literal-пул @0x10688 (6 слов) — ВНЕ границ функции ---
  10688:  .word 0x20000080  ; RAM
  1068c:  .word 0x20000f95  ; RAM
  10690:  .word 0x08019daa  ; flash-mirror @0x19daa
  10694:  .word 0x200009f8  ; RAM
  10698:  .word 0x200009fa  ; RAM
  1069c:  .word 0x20000fbb  ; RAM
```
