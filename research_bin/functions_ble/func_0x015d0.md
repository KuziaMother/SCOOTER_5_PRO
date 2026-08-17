# func_0x015d0

| | |
|---|---|
| offset в файле | `0x015d0` |
| vaddr (база 0x01800000) | `0x018015d0` |
 | размер кода | 562 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200769 — RAM (r2)
- 0x0020076a — RAM (r1)
- 0x002007a8 — RAM (r1)
- 0x002009e8 — RAM (r1)
- 0x00201cb8 — RAM (r1)
- 0x00201e20 — RAM (r0)
- 0x00206838 — RAM (r0)
- 0x0021b2d1 — RAM (r0)

## Вызовы (callees)

- 0x018017f0 (b, вне списка функций)
- 0x01802964 (bl, вне списка функций)
- 0x01802ca8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  018015d0:  push {r4, lr}                     
  018015d2:  mov.w r2, #-1                     
  018015d6:  movs r1, #0x38                    
  018015d8:  adds r0, #0x78                    
  018015da:  bl #0x1802ca8                     -> 0x02ca8 (вне списка функций)
  018015de:  bl #0x1802964                     -> 0x02964 (вне списка функций)
  018015e2:  ldr r0, [pc, #0x54]               (RAM)
  018015e4:  movs r1, #0xc9                    
  018015e6:  adds r0, #0x58                    
  018015e8:  ldr r2, [pc, #0x1fc]              (RAM)
  018015ea:  strb r1, [r0]                     
  018015ec:  movs r1, #0xdc                    
  018015ee:  strb r1, [r0, #1]                 
  018015f0:  movs r1, #0xe1                    
  018015f2:  strb r1, [r0, #2]                 
  018015f4:  movs r1, #0xeb                    
  018015f6:  strb r1, [r0, #3]                 
  018015f8:  movs r1, #0xef                    
  018015fa:  strb r1, [r0, #4]                 
  018015fc:  movs r1, #0xf1                    
  018015fe:  strb r1, [r0, #5]                 
  01801600:  movs r1, #0xf6                    
  01801602:  strb r1, [r0, #6]                 
  01801604:  movs r1, #0xfb                    
  01801606:  strb r1, [r0, #7]                 
  01801608:  movs r1, #0xfe                    
  0180160a:  strb r1, [r0, #8]                 
  0180160c:  movs r1, #2                       
  0180160e:  strb r1, [r0, #9]                 
  01801610:  movs r1, #3                       
  01801612:  strb r1, [r0, #0xa]               
  01801614:  movs r1, #5                       
  01801616:  strb r1, [r0, #0xb]               
  01801618:  movs r1, #6                       
  0180161a:  strb r1, [r0, #0xc]               
  0180161c:  movs r1, #7                       
  0180161e:  strb r1, [r0, #0xd]               
  01801620:  movs r1, #8                       
  01801622:  strb r1, [r0, #0xe]               
  01801624:  movs r1, #9                       
  01801626:  strb r1, [r0, #0xf]               
  01801628:  ldr r0, [pc, #0x20]               (RAM)
  0180162a:  ldrb r0, [r0, #6]                 
  0180162c:  lsrs r1, r0, #4                   
  0180162e:  strb r1, [r2]                     
  01801630:  ldr r1, [pc, #0x1b8]              (RAM)
  01801632:  strb r0, [r1]                     
  01801634:  movs r0, #0xa                     
  01801636:  b #0x18017f0                      -> 0x017f0 (вне списка функций)
  01801638:  ldr r0, [r7]                      
  0180163a:  movs r0, r4                       
  0180163c:  movs r0, #0x44                    
  0180163e:  movs r0, r4                       
  01801640:  movs r1, #0x6a                    
  01801642:  lsls r2, r7, #3                   
  01801644:  lsls r4, r7, #0x16                
  01801646:  movs r0, r4                       
  01801648:  lsrs r0, r2, #5                   
  0180164a:  movs r0, r4                       
  0180164c:  subs r0, r4, #0                   
  0180164e:  movs r0, r4                       
  01801650:  lsls r4, r5, #0x17                
  01801652:  movs r0, r4                       
  01801654:  subs r4, r1, #1                   
  01801656:  movs r0, r4                       
  01801658:  subs r4, r5, #2                   
  0180165a:  movs r0, r4                       
  0180165c:  ldrh r7, [r1, #0x28]              
  0180165e:  movs r1, r4                       
  01801660:  lsls r0, r5, #0x17                
  01801662:  movs r0, r4                       
  01801664:  lsls r4, r0, #0x18                
  01801666:  movs r0, r4                       
  01801668:  ldrh r7, [r5, #4]                 
  0180166a:  movs r1, r4                       
  0180166c:  adds r0, r6, #2                   
  0180166e:  movs r0, r4                       
  01801670:  ldrh r3, [r5, #0x16]              
  01801672:  movs r1, r4                       
  01801674:  lsrs r0, r5, #0x20                
  01801676:  movs r0, r4                       
  01801678:  ldrh r7, [r3, #0x32]              
  0180167a:  movs r1, r4                       
  0180167c:  adds r0, r0, #3                   
  0180167e:  movs r0, r4                       
  01801680:  ldrh r5, [r5, #0x38]              
  01801682:  movs r1, r4                       
  01801684:  adds r4, r3, #3                   
  01801686:  movs r0, r4                       
  01801688:  str r3, [sp, #0xb4]               
  0180168a:  movs r1, r4                       
  0180168c:  adds r0, r2, #3                   
  0180168e:  movs r0, r4                       
  01801690:  str r4, [sp, #0x38c]              
  01801692:  movs r1, r4                       
  01801694:  lsrs r0, r3, #0xb                 
  01801696:  movs r0, r4                       
  01801698:  str r5, [sp, #0x244]              
  0180169a:  movs r1, r4                       
  0180169c:  lsls r4, r6, #0x1d                
  0180169e:  movs r0, r4                       
  018016a0:  str r6, [sp, #0xe4]               
  018016a2:  movs r1, r4                       
  018016a4:  adds r4, r3, #2                   
  018016a6:  movs r0, r4                       
  018016a8:  ldr r2, [sp, #0x34]               
  018016aa:  movs r1, r4                       
  018016ac:  adds r4, r6, #2                   
  018016ae:  movs r0, r4                       
  018016b0:  str r7, [sp, #0x244]              
  018016b2:  movs r1, r4                       
  018016b4:  lsrs r4, r5, #0x20                
  018016b6:  movs r0, r4                       
  018016b8:  str r7, [sp, #0x1cc]              
  018016ba:  movs r1, r4                       
  018016bc:  lsls r4, r6, #0x1f                
  018016be:  movs r0, r4                       
  018016c0:  ldr r0, [sp, #0x54]               
  018016c2:  movs r1, r4                       
  018016c4:  lsrs r4, r6, #0x20                
  018016c6:  movs r0, r4                       
  018016c8:  ldr r0, [sp, #0x304]              
  018016ca:  movs r1, r4                       
  018016cc:  lsrs r0, r4, #0x20                
  018016ce:  movs r0, r4                       
  018016d0:  lsrs r0, r3, #2                   
  018016d2:  movs r0, r4                       
  018016d4:  lsrs r0, r5, #8                   
  018016d6:  movs r0, r4                       
  018016d8:  ldr r4, [sp, #0xa4]               
  018016da:  movs r1, r4                       
  018016dc:  subs r0, r1, r7                   
  018016de:  movs r0, r4                       
  018016e0:  ldr r4, [sp, #0xcc]               
  018016e2:  movs r1, r4                       
  018016e4:  lsls r4, r4, #0x16                
  018016e6:  movs r0, r4                       
  018016e8:  lsls r4, r5, #0x1e                
  018016ea:  movs r0, r4                       
  018016ec:  ldr r4, [sp, #0x1a4]              
  018016ee:  movs r1, r4                       
  018016f0:  asrs r4, r7, #0x1d                
  018016f2:  movs r0, r4                       
  018016f4:  ldr r4, [sp, #0x204]              
  018016f6:  movs r1, r4                       
  018016f8:  lsls r4, r0, #0x1f                
  018016fa:  movs r0, r4                       
  018016fc:  ldr r4, [sp, #0x2ac]              
  018016fe:  movs r1, r4                       
  01801700:  lsls r4, r1, #0x1f                
  01801702:  movs r0, r4                       
  01801704:  ldr r5, [sp, #0x144]              
  01801706:  movs r1, r4                       
  01801708:  lsrs r4, r1, #4                   
  0180170a:  movs r0, r4                       
  0180170c:  adr r4, #0x21c                    
  0180170e:  movs r1, r4                       
  01801710:  asrs r4, r3, #0x1d                
  01801712:  movs r0, r4                       
  01801714:  ldr r5, [sp, #0x314]              
  01801716:  movs r1, r4                       
  01801718:  lsls r4, r4, #0x17                
  0180171a:  movs r0, r4                       
  0180171c:  lsls r4, r4, #0x1f                
  0180171e:  movs r0, r4                       
  01801720:  str r0, [sp, #0x3d4]              
  01801722:  movs r1, r4                       
  01801724:  ldr r5, [sp, #0x3bc]              
  01801726:  movs r1, r4                       
  01801728:  lsls r0, r6, #0x1f                
  0180172a:  movs r0, r4                       
  0180172c:  str r6, [sp, #0xa4]               
  0180172e:  movs r1, r4                       
  01801730:  lsrs r4, r4, #4                   
  01801732:  movs r0, r4                       
  01801734:  ldr r1, [sp, #0x14]               
  01801736:  movs r1, r4                       
  01801738:  adds r4, r1, #3                   
  0180173a:  movs r0, r4                       
  0180173c:  adr r1, #0x334                    
  0180173e:  movs r1, r4                       
  01801740:  adr r2, #0x2c                     
  01801742:  movs r1, r4                       
  01801744:  adds r0, r4, #2                   
  01801746:  movs r0, r4                       
  01801748:  adr r4, #0x24c                    
  0180174a:  movs r1, r4                       
  0180174c:  adds r0, r4, r6                   
  0180174e:  movs r0, r4                       
  01801750:  lsrs r4, r1, #0x20                
  01801752:  movs r0, r4                       
  01801754:  adr r4, #0x3e4                    
  01801756:  movs r1, r4                       
  01801758:  cmp r2, #0x48                     
  0180175a:  movs r0, r4                       
  0180175c:  adr r5, #0x234                    
  0180175e:  movs r1, r4                       
  01801760:  cmp r2, #0x5c                     
  01801762:  movs r0, r4                       
  01801764:  add r1, sp, #0x1fc                
  01801766:  movs r1, r4                       
  01801768:  adds r4, r5, #2                   
  0180176a:  movs r0, r4                       
  0180176c:  add r0, sp, #0x36c                
  0180176e:  movs r1, r4                       
  01801770:  cmp r2, #0x44                     
  01801772:  movs r0, r4                       
  01801774:  add r1, sp, #0x2ec                
  01801776:  movs r1, r4                       
  01801778:  cmp r2, #0x50                     
  0180177a:  movs r0, r4                       
  0180177c:  add r1, sp, #0x32c                
  0180177e:  movs r1, r4                       
  01801780:  lsls r0, r1, #0x1f                
  01801782:  movs r0, r4                       
  01801784:  add r2, sp, #0x1dc                
  01801786:  movs r1, r4                       
  01801788:  lsls r0, r4, #0x1f                
  0180178a:  movs r0, r4                       
  0180178c:  lsrs r0, r3, #0xc                 
  0180178e:  movs r0, r4                       
  01801790:  add r3, sp, #0x3fc                
  01801792:  movs r1, r4                       
  01801794:  lsrs r0, r4, #0xc                 
  01801796:  movs r0, r4                       
  01801798:  lsrs r4, r1, #0xc                 
  0180179a:  movs r0, r4                       
  0180179c:  lsrs r0, r0, #0xc                 
  0180179e:  movs r0, r4                       
  018017a0:  add r6, sp, #0x2ec                
  018017a2:  movs r1, r4                       
  018017a4:  movs r0, #0x18                    
  018017a6:  movs r0, r4                       
  018017a8:  add r7, sp, #0x19c                
  018017aa:  movs r1, r4                       
  018017ac:  lsls r4, r0, #0x1e                
  018017ae:  movs r0, r4                       
  018017b0:  add r3, sp, #0x1c4                
  018017b2:  movs r1, r4                       
  018017b4:  lsrs r4, r0, #8                   
  018017b6:  movs r0, r4                       
  018017b8:  add sp, #0x1a4                    
  018017ba:  movs r1, r4                       
  018017bc:  lsls r0, r6, #0x1e                
  018017be:  movs r0, r4                       
  018017c0:  lsrs r4, r5, #8                   
  018017c2:  movs r0, r4                       
  018017c4:  sub sp, #0x74                     
  018017c6:  movs r1, r4                       
  018017c8:  cmp r2, #0x7c                     
  018017ca:  movs r0, r4                       
  018017cc:  sub sp, #0x1b4                    
  018017ce:  movs r1, r4                       
  018017d0:  lsrs r0, r1, #5                   
  018017d2:  movs r0, r4                       
  018017d4:  cbz r7, #0x18017da                
  018017d6:  movs r1, r4                       
  018017d8:  cbz r3, #0x18017f4                
  018017da:  movs r1, r4                       
  018017dc:  cmp r2, #0x30                     
  018017de:  movs r0, r4                       
  018017e0:  cbz r3, #0x1801806                
  018017e2:  movs r1, r4                       
  018017e4:  adds r4, r6, r6                   
  018017e6:  movs r0, r4                       
  018017e8:  lsls r1, r5, #0x1d                
  018017ea:  movs r0, r4                       
  018017ec:  lsls r0, r5, #0x1e                
  018017ee:  movs r0, r4                       
  018017f0:  ldr r1, [pc, #0x10]               (RAM)
  018017f2:  strb r0, [r1, #3]                 
  018017f4:  ldr r1, [pc, #0x10]               (RAM)
  018017f6:  movs r0, #0xb                     
  018017f8:  strb r0, [r1]                     
  018017fa:  ldr r1, [pc, #0x14]               (RAM)
  018017fc:  ldr r0, [pc, #0xc]                (RAM)
  018017fe:  str r0, [r1]                      
  01801800:  pop {r4, pc}                      
  ; --- literal-пул @0x01638 (1 слов) ---
  01638:  .word 0x00206838  ; RAM
  ; --- literal-пул @0x0164c (1 слов) ---
  0164c:  .word 0x00201e20  ; RAM
  ; --- literal-пул @0x017e8 (2 слов) ---
  017e8:  .word 0x00200769  ; RAM
  017ec:  .word 0x002007a8  ; RAM
  ; --- literal-пул @0x01804 (4 слов) — ВНЕ границ функции ---
  01804:  .word 0x002009e8  ; RAM
  01808:  .word 0x0020076a  ; RAM
  0180c:  .word 0x0021b2d1  ; RAM
  01810:  .word 0x00201cb8  ; RAM
```
