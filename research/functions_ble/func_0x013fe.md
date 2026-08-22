# func_0x013fe

| | |
|---|---|
| offset в файле | `0x013fe` |
| vaddr (база 0x01800000) | `0x018013fe` |
 | размер кода | 464 Б |
| регион | заголовок + bootloader (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x002005a4 — RAM (r3)
- 0x002005e4 — RAM (r3)
- 0x002005e8 — RAM (r1)
- 0x00200604 — RAM (r0)
- 0x00200774 — RAM (r2)
- 0x00200784 — RAM (r2)
- 0x002007ac — RAM (r3)
- 0x002007b0 — RAM (r4)
- 0x002007c4 — RAM (r3)
- 0x002007c8 — RAM (r3)
- 0x002007cc — RAM (r3)
- 0x002007e0 — RAM (r3)
- 0x002007e4 — RAM (r3)
- 0x002007f0 — RAM (r3)
- 0x002007f4 — RAM (r2)
- 0x0020080c — RAM (r3)
- 0x00200820 — RAM (r2)
- 0x00200828 — RAM (r2)
- 0x0020082c — RAM (r2)
- 0x00200834 — RAM (r2)
- 0x00200898 — RAM (r1)
- 0x0020090c — RAM (r3)
- 0x00200924 — RAM (r3)
- 0x00200948 — RAM (r3)
- 0x00200a04 — RAM (r4)
- 0x00200a28 — RAM (r3)
- 0x00200a2c — RAM (r3)
- 0x00200ad8 — RAM (r2)
- 0x00200b00 — RAM (r3)
- 0x00200b0c — RAM (r3)
- 0x00200b18 — RAM (r3)
- 0x00200b20 — RAM (r3)
- 0x0020175c — RAM (r3)
- 0x0020177c — RAM (r3)
- 0x002019a0 — RAM (r3)
- 0x002019b4 — RAM (r1)
- 0x00201bc8 — RAM (r3)
- 0x00201c9c — RAM (r2)
- 0x00201ca0 — RAM (r3)
- 0x00201cac — RAM (r3)
- 0x00201cb0 — RAM (r2)
- 0x00201cb4 — RAM (r2)
- 0x00201cc0 — RAM (r2)
- 0x00201ccc — RAM (r3)
- 0x00201cd0 — RAM (r2)
- 0x00201cdc — RAM (r2)
- 0x00201e4c — RAM (r1)
- 0x00201eac — RAM (r1)
- 0x00202018 — RAM (r3)
- 0x00202a30 — RAM (r2)
- 0x00202a44 — RAM (r3)
- 0x00202a48 — RAM (r3)
- 0x00202a50 — RAM (r3)
- 0x00202a5c — RAM (r3)
- 0x00202a7c — RAM (r3)
- 0x002188af — RAM (r1)
- 0x00218aeb — RAM (r1)
- 0x00218d0f — RAM (r0)
- 0x00218e5f — RAM (r1)
- 0x00218f2d — RAM (r1)
- 0x002190f5 — RAM (r2)
- 0x0021932d — RAM (r1)
- 0x002194e3 — RAM (r1)
- 0x00219591 — RAM (r1)
- 0x00219629 — RAM (r2)
- 0x00219639 — RAM (r1)
- 0x00219773 — RAM (r1)
- 0x00219791 — RAM (r1)
- 0x00219815 — RAM (r1)
- 0x002198c1 — RAM (r1)
- 0x00219905 — RAM (r2)
- 0x00219a0d — RAM (r1)
- 0x00219c29 — RAM (r2)
- 0x00219c33 — RAM (r2)
- 0x00219c69 — RAM (r2)
- 0x00219c81 — RAM (r2)
- 0x00219cab — RAM (r2)
- 0x00219d51 — RAM (r2)
- 0x00219dc5 — RAM (r2)
- 0x00219def — RAM (r2)
- 0x0021a1cd — RAM (r2)
- 0x0021a20b — RAM (r2)
- 0x0021a487 — RAM (r2)
- 0x0021a493 — RAM (r2)
- 0x0021a4f9 — RAM (r2)
- 0x0021a58d — RAM (r2)
- 0x0021a8db — RAM (r2)
- 0x0021a97f — RAM (r2)
- 0x0021a9bb — RAM (r2)
- 0x0021a9cb — RAM (r2)
- 0x0021aa77 — RAM (r2)
- 0x0021ab71 — RAM (r3)
- 0x0021abff — RAM (r2)
- 0x0021aebb — RAM (r2)
- 0x0021af67 — RAM (r3)
- 0x0021b069 — RAM (r3)
- 0x0021b09d — RAM (r1)
- 0x0021b0ed — RAM (r1)
- 0x0021b10f — RAM (r1)
- 0x0021b163 — RAM (r1)
- 0x0021b18b — RAM (r1)

## Вызовы (callees)

- 0x01801fb8 (bl, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x027d6` (bl @0x01802834)

## Дизассембляция

```asm
  018013fe:  push {r4, lr}                     
  01801400:  bl #0x1801fb8                     -> 0x01fb8 (вне списка функций)
  01801404:  subw r0, pc, #0xad                
  01801408:  ldr r1, [pc, #0x248]              (RAM)
  0180140a:  str r0, [r1]                      
  0180140c:  subw r0, pc, #0x24f               
  01801410:  ldr r1, [pc, #0x244]              (RAM)
  01801412:  str r0, [r1]                      
  01801414:  ldr r1, [pc, #0x248]              (RAM)
  01801416:  ldr r0, [pc, #0x244]              (RAM)
  01801418:  str r0, [r1]                      
  0180141a:  subw r1, pc, #0x26f               
  0180141e:  ldr r0, [pc, #0x244]              (RAM)
  01801420:  str r1, [r0, #0x78]               
  01801422:  subw r1, pc, #0x28b               
  01801426:  ldr r2, [pc, #0x244]              (RAM)
  01801428:  str.w r1, [r0, #0xd0]             
  0180142c:  ldr r1, [pc, #0x238]              (RAM)
  0180142e:  str r1, [r2]                      
  01801430:  ldr r2, [pc, #0x240]              (RAM)
  01801432:  ldr r1, [pc, #0x23c]              (RAM)
  01801434:  str r1, [r2]                      
  01801436:  ldr r2, [pc, #0x244]              (RAM)
  01801438:  ldr r1, [pc, #0x23c]              (RAM)
  0180143a:  str r1, [r2]                      
  0180143c:  ldr r2, [pc, #0x244]              (RAM)
  0180143e:  ldr r1, [pc, #0x240]              (RAM)
  01801440:  str r1, [r2]                      
  01801442:  ldr r2, [pc, #0x248]              (RAM)
  01801444:  ldr r1, [pc, #0x240]              (RAM)
  01801446:  str r1, [r2]                      
  01801448:  ldr r2, [pc, #0x248]              (RAM)
  0180144a:  ldr r1, [pc, #0x244]              (RAM)
  0180144c:  str r1, [r2]                      
  0180144e:  ldr r2, [pc, #0x24c]              (RAM)
  01801450:  ldr r1, [pc, #0x244]              (RAM)
  01801452:  str r1, [r2]                      
  01801454:  ldr r2, [pc, #0x24c]              (RAM)
  01801456:  ldr r1, [pc, #0x248]              (RAM)
  01801458:  str r1, [r2]                      
  0180145a:  ldr r2, [pc, #0x250]              (RAM)
  0180145c:  ldr r1, [pc, #0x248]              (RAM)
  0180145e:  str r1, [r2]                      
  01801460:  ldr r2, [pc, #0x250]              (RAM)
  01801462:  ldr r1, [pc, #0x24c]              (RAM)
  01801464:  str r1, [r2]                      
  01801466:  ldr r2, [pc, #0x254]              (RAM)
  01801468:  ldr r1, [pc, #0x24c]              (RAM)
  0180146a:  str r1, [r2]                      
  0180146c:  ldr r2, [pc, #0x254]              (RAM)
  0180146e:  ldr r1, [pc, #0x250]              (RAM)
  01801470:  str r1, [r2]                      
  01801472:  ldr r2, [pc, #0x258]              (RAM)
  01801474:  ldr r1, [pc, #0x250]              (RAM)
  01801476:  str r1, [r2]                      
  01801478:  subw r2, pc, #0xf9b               
  0180147c:  ldr r1, [pc, #0x250]              (RAM)
  0180147e:  str r2, [r1, #0x4c]               
  01801480:  subw r2, pc, #0x327               
  01801484:  str r2, [r0, #0x1c]               
  01801486:  subw r2, pc, #0x517               
  0180148a:  str.w r2, [r0, #0xe0]             
  0180148e:  subw r2, pc, #0x72b               
  01801492:  str.w r2, [r0, #0xdc]             
  01801496:  subw r2, pc, #0xf97               
  0180149a:  ldr r3, [pc, #0x238]              (RAM)
  0180149c:  str r2, [r3]                      
  0180149e:  ldr r3, [pc, #0x23c]              (RAM)
  018014a0:  ldr r2, [pc, #0x234]              (RAM)
  018014a2:  str r2, [r3]                      
  018014a4:  ldr r3, [pc, #0x23c]              (RAM)
  018014a6:  ldr r2, [pc, #0x238]              (RAM)
  018014a8:  str r2, [r3]                      
  018014aa:  subw r2, pc, #0xf37               
  018014ae:  ldr r3, [pc, #0x238]              (RAM)
  018014b0:  str r2, [r3]                      
  018014b2:  ldr r3, [pc, #0x23c]              (RAM)
  018014b4:  ldr r2, [pc, #0x234]              (RAM)
  018014b6:  str r2, [r3]                      
  018014b8:  ldr r3, [pc, #0x23c]              (RAM)
  018014ba:  ldr r2, [pc, #0x238]              (RAM)
  018014bc:  str r2, [r3]                      
  018014be:  ldr r3, [pc, #0x240]              (RAM)
  018014c0:  ldr r2, [pc, #0x238]              (RAM)
  018014c2:  str r2, [r3]                      
  018014c4:  ldr r3, [pc, #0x240]              (RAM)
  018014c6:  ldr r2, [pc, #0x23c]              (RAM)
  018014c8:  str r2, [r3]                      
  018014ca:  subw r2, pc, #0xf39               
  018014ce:  ldr r3, [pc, #0x240]              (RAM)
  018014d0:  str r2, [r1, #0x48]               
  018014d2:  ldr r2, [pc, #0x238]              (RAM)
  018014d4:  str r2, [r3]                      
  018014d6:  ldr r3, [pc, #0x240]              (RAM)
  018014d8:  ldr r2, [pc, #0x238]              (RAM)
  018014da:  str r2, [r3]                      
  018014dc:  subw r2, pc, #0xee7               
  018014e0:  ldr r3, [pc, #0x238]              (RAM)
  018014e2:  str r2, [r3]                      
  018014e4:  ldr r2, [pc, #0x238]              (RAM)
  018014e6:  ldr r3, [pc, #0x240]              (RAM)
  018014e8:  str r2, [r0, #0x28]               
  018014ea:  ldr r2, [pc, #0x238]              (RAM)
  018014ec:  str r2, [r3]                      
  018014ee:  ldr r3, [pc, #0x240]              (RAM)
  018014f0:  ldr r2, [pc, #0x238]              (RAM)
  018014f2:  str r2, [r3]                      
  018014f4:  ldr r3, [pc, #0x240]              (RAM)
  018014f6:  ldr r2, [pc, #0x23c]              (RAM)
  018014f8:  str r2, [r3]                      
  018014fa:  ldr r2, [pc, #0x240]              (RAM)
  018014fc:  ldr r3, [pc, #0x244]              (RAM)
  018014fe:  str r2, [r1]                      
  01801500:  ldr r2, [pc, #0x23c]              (RAM)
  01801502:  str r2, [r3]                      
  01801504:  ldr r3, [pc, #0x244]              (RAM)
  01801506:  ldr r2, [pc, #0x240]              (RAM)
  01801508:  str r2, [r3]                      
  0180150a:  subw r2, pc, #0xecf               
  0180150e:  ldr r3, [pc, #0x240]              (RAM)
  01801510:  str r2, [r3]                      
  01801512:  ldr r3, [pc, #0x244]              (RAM)
  01801514:  ldr r2, [pc, #0x23c]              (RAM)
  01801516:  str r2, [r3]                      
  01801518:  ldr r3, [pc, #0x244]              (RAM)
  0180151a:  ldr r2, [pc, #0x240]              (RAM)
  0180151c:  str r2, [r3]                      
  0180151e:  subw r2, pc, #0xca5               
  01801522:  ldr r3, [pc, #0x244]              (RAM)
  01801524:  str.w r2, [r0, #0xd8]             
  01801528:  ldr r2, [pc, #0x238]              (RAM)
  0180152a:  str r2, [r3]                      
  0180152c:  ldr r3, [pc, #0x240]              (RAM)
  0180152e:  ldr r2, [pc, #0x23c]              (RAM)
  01801530:  str r2, [r3]                      
  01801532:  ldr r3, [pc, #0x244]              (RAM)
  01801534:  ldr r2, [pc, #0x23c]              (RAM)
  01801536:  str r2, [r3]                      
  01801538:  ldr r3, [pc, #0x244]              (RAM)
  0180153a:  ldr r2, [pc, #0x240]              (RAM)
  0180153c:  str r2, [r3]                      
  0180153e:  ldr r3, [pc, #0x248]              (RAM)
  01801540:  ldr r2, [pc, #0x240]              (RAM)
  01801542:  str r2, [r3]                      
  01801544:  subw r2, pc, #0xc53               
  01801548:  str.w r2, [r0, #0xf0]             
  0180154c:  subw r2, pc, #0xc15               
  01801550:  str.w r2, [r0, #0xf4]             
  01801554:  subw r2, pc, #0xbe1               
  01801558:  ldr r3, [pc, #0x230]              (RAM)
  0180155a:  str r2, [r3]                      
  0180155c:  ldr r3, [pc, #0x234]              (RAM)
  0180155e:  ldr r2, [pc, #0x230]              (RAM)
  01801560:  str r2, [r3]                      
  01801562:  subw r2, pc, #0xb51               
  01801566:  str r2, [r0, #0x38]               
  01801568:  subw r2, pc, #0xa87               
  0180156c:  ldr r3, [pc, #0x228]              (RAM)
  0180156e:  str r2, [r3]                      
  01801570:  subw r2, pc, #0x9f3               
  01801574:  ldr r3, [pc, #0x224]              (RAM)
  01801576:  ldr r4, [pc, #0x23c]              (RAM)
  01801578:  str r2, [r3]                      
  0180157a:  ldr r3, [pc, #0x228]              (RAM)
  0180157c:  ldr r2, [pc, #0x220]              (RAM)
  0180157e:  str r2, [r3]                      
  01801580:  ldr r2, [pc, #0x228]              (RAM)
  01801582:  ldr r3, [pc, #0x224]              (RAM)
  01801584:  str r3, [r2, #0x14]               
  01801586:  ldr r3, [pc, #0x228]              (RAM)
  01801588:  str r3, [r4]                      
  0180158a:  ldr r4, [pc, #0x230]              (RAM)
  0180158c:  ldr r3, [pc, #0x228]              (RAM)
  0180158e:  str r3, [r4]                      
  01801590:  subw r3, pc, #0x9bf               
  01801594:  str r3, [r1, #0x20]               
  01801596:  subw r3, pc, #0x98f               
  0180159a:  str r3, [r1, #0x38]               
  0180159c:  subw r1, pc, #0x963               
  018015a0:  ldr r3, [pc, #0x21c]              (RAM)
  018015a2:  str r1, [r3]                      
  018015a4:  ldr r3, [pc, #0x220]              (RAM)
  018015a6:  ldr r1, [pc, #0x21c]              (RAM)
  018015a8:  str r1, [r3]                      
  018015aa:  ldr r3, [pc, #0x224]              (RAM)
  018015ac:  ldr r1, [pc, #0x21c]              (RAM)
  018015ae:  str r1, [r3]                      
  018015b0:  ldr r1, [pc, #0x220]              (RAM)
  018015b2:  str r1, [r2, #0x1c]               
  018015b4:  ldr r2, [pc, #0x224]              (RAM)
  018015b6:  ldr r1, [pc, #0x220]              (RAM)
  018015b8:  str r1, [r2]                      
  018015ba:  subw r1, pc, #0xa1d               
  018015be:  str r1, [r0, #0x34]               
  018015c0:  ldr r1, [pc, #0x21c]              (RAM)
  018015c2:  str r1, [r0, #0x30]               
  018015c4:  subw r0, pc, #0x8df               
  018015c8:  ldr r1, [pc, #0x218]              (RAM)
  018015ca:  str r0, [r1]                      
  018015cc:  pop {r4, pc}                      
  ; --- literal-пул @0x01654 (101 слов) — ВНЕ границ функции ---
  01654:  .word 0x00201e4c  ; RAM
  01658:  .word 0x00201eac  ; RAM
  0165c:  .word 0x00218d0f  ; RAM
  01660:  .word 0x002005e8  ; RAM
  01664:  .word 0x00200604  ; RAM
  01668:  .word 0x002188af  ; RAM
  0166c:  .word 0x00201cb0  ; RAM
  01670:  .word 0x00218aeb  ; RAM
  01674:  .word 0x00200828  ; RAM
  01678:  .word 0x00218e5f  ; RAM
  0167c:  .word 0x00201cc0  ; RAM
  01680:  .word 0x00218f2d  ; RAM
  01684:  .word 0x00201cdc  ; RAM
  01688:  .word 0x0021932d  ; RAM
  0168c:  .word 0x00201cd0  ; RAM
  01690:  .word 0x002194e3  ; RAM
  01694:  .word 0x00200ad8  ; RAM
  01698:  .word 0x00219591  ; RAM
  0169c:  .word 0x00200774  ; RAM
  016a0:  .word 0x00219639  ; RAM
  016a4:  .word 0x00201c9c  ; RAM
  016a8:  .word 0x00219a0d  ; RAM
  016ac:  .word 0x00201cb4  ; RAM
  016b0:  .word 0x00219791  ; RAM
  016b4:  .word 0x0020082c  ; RAM
  016b8:  .word 0x00219773  ; RAM
  016bc:  .word 0x002007f4  ; RAM
  016c0:  .word 0x00219815  ; RAM
  016c4:  .word 0x00200834  ; RAM
  016c8:  .word 0x002198c1  ; RAM
  016cc:  .word 0x00200820  ; RAM
  016d0:  .word 0x00200898  ; RAM
  016d4:  .word 0x00200a28  ; RAM
  016d8:  .word 0x00219c29  ; RAM
  016dc:  .word 0x00201bc8  ; RAM
  016e0:  .word 0x00219c33  ; RAM
  016e4:  .word 0x002005a4  ; RAM
  016e8:  .word 0x002007ac  ; RAM
  016ec:  .word 0x00219c69  ; RAM
  016f0:  .word 0x0020177c  ; RAM
  016f4:  .word 0x00219c81  ; RAM
  016f8:  .word 0x002007c4  ; RAM
  016fc:  .word 0x00219cab  ; RAM
  01700:  .word 0x002007cc  ; RAM
  01704:  .word 0x00219d51  ; RAM
  01708:  .word 0x0020090c  ; RAM
  0170c:  .word 0x0021a487  ; RAM
  01710:  .word 0x0020175c  ; RAM
  01714:  .word 0x00219dc5  ; RAM
  01718:  .word 0x002005e4  ; RAM
  0171c:  .word 0x002007e4  ; RAM
  01720:  .word 0x002190f5  ; RAM
  01724:  .word 0x00219def  ; RAM
  01728:  .word 0x002007f0  ; RAM
  0172c:  .word 0x00219629  ; RAM
  01730:  .word 0x00200924  ; RAM
  01734:  .word 0x00219905  ; RAM
  01738:  .word 0x00201ccc  ; RAM
  0173c:  .word 0x0021a1cd  ; RAM
  01740:  .word 0x0021a20b  ; RAM
  01744:  .word 0x00201ca0  ; RAM
  01748:  .word 0x0021a493  ; RAM
  0174c:  .word 0x002019a0  ; RAM
  01750:  .word 0x0020080c  ; RAM
  01754:  .word 0x0021a4f9  ; RAM
  01758:  .word 0x00202a48  ; RAM
  0175c:  .word 0x0021a58d  ; RAM
  01760:  .word 0x00202a5c  ; RAM
  01764:  .word 0x0021a97f  ; RAM
  01768:  .word 0x00201cac  ; RAM
  0176c:  .word 0x0021a8db  ; RAM
  01770:  .word 0x00202a44  ; RAM
  01774:  .word 0x0021a9bb  ; RAM
  01778:  .word 0x00202a50  ; RAM
  0177c:  .word 0x0021a9cb  ; RAM
  01780:  .word 0x002007c8  ; RAM
  01784:  .word 0x0021aa77  ; RAM
  01788:  .word 0x002007e0  ; RAM
  0178c:  .word 0x00200b18  ; RAM
  01790:  .word 0x0021abff  ; RAM
  01794:  .word 0x00200b20  ; RAM
  01798:  .word 0x00200b0c  ; RAM
  0179c:  .word 0x00200b00  ; RAM
  017a0:  .word 0x0021aebb  ; RAM
  017a4:  .word 0x00202018  ; RAM
  017a8:  .word 0x0021af67  ; RAM
  017ac:  .word 0x00200784  ; RAM
  017b0:  .word 0x0021ab71  ; RAM
  017b4:  .word 0x00200a04  ; RAM
  017b8:  .word 0x0021b069  ; RAM
  017bc:  .word 0x002007b0  ; RAM
  017c0:  .word 0x00200a2c  ; RAM
  017c4:  .word 0x0021b09d  ; RAM
  017c8:  .word 0x00202a7c  ; RAM
  017cc:  .word 0x0021b0ed  ; RAM
  017d0:  .word 0x00200948  ; RAM
  017d4:  .word 0x0021b10f  ; RAM
  017d8:  .word 0x0021b163  ; RAM
  017dc:  .word 0x00202a30  ; RAM
  017e0:  .word 0x0021b18b  ; RAM
  017e4:  .word 0x002019b4  ; RAM
```
