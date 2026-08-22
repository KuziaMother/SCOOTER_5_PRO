# func_0x1d640

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08001d640) | `0x0001d640` |
| размер кода | 348 Б |
| регион | код I (USART3-протокол 0x1e480/0x1e9e0/0x1f600/0x1f6b4, HAL_UART_Transmit 0x23188, мотор TIM1 0x22a48-0x22fac, ADC 0x1a31c/0x1e298) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x0000045b — данные @0x0045b (r0)
- 0x000008ca — данные @0x008ca (r0)
- 0x40012c00 — периферия (r4)
- 0x48000400 — периферия (r4)

## Вызовы (callees)

- 0x19a9a (bl, вне списка функций)
- `func_0x22000` (0x00022000, bl)
- `func_0x22a48` (0x00022a48, bl)
- 0x22b00 (bl, вне списка функций)
- `func_0x22c70` (0x00022c70, bl)
- `func_0x23040` (0x00023040, bl)
- `func_0x23544` (0x00023544, bl)

## Кто вызывает (callers / xrefs)

- `func_0x1bf48` (bl @0x0001bf4a)


## Дизассембляция

```asm
  1d640:  push {r4, r5, r6, r7, lr}         
  1d642:  sub sp, #0x64                     
  1d644:  movs r5, #0                       
  1d646:  movs r1, #2                       
  1d648:  str r5, [sp, #0x3c]               
  1d64a:  add r0, sp, #0x20                 
  1d64c:  str r5, [sp, #0x40]               
  1d64e:  strb r1, [r0, #0x1c]              
  1d650:  strb r5, [r0, #0x1e]              
  1d652:  strb r5, [r0, #0x1d]              
  1d654:  add r0, sp, #0x40                 
  1d656:  strb r5, [r0]                     
  1d658:  strb r5, [r0, #1]                 
  1d65a:  add r0, sp, #0x20                 
  1d65c:  strb r5, [r0, #0x1f]              
  1d65e:  movs r6, #6                       
  1d660:  add r0, sp, #0x40                 
  1d662:  movs r4, #9                       
  1d664:  strb r6, [r0, #2]                 
  1d666:  lsls r7, r1, #7                   
  1d668:  lsls r4, r4, #0x1b                
  1d66a:  add r2, sp, #0x3c                 
  1d66c:  mov r1, r7                        
  1d66e:  mov r0, r4                        
  1d670:  bl #0x22000                       -> func_0x22000
  1d674:  add r2, sp, #0x3c                 
  1d676:  lsls r1, r7, #1                   
  1d678:  mov r0, r4                        
  1d67a:  bl #0x22000                       -> func_0x22000
  1d67e:  add r2, sp, #0x3c                 
  1d680:  lsls r1, r7, #2                   
  1d682:  mov r0, r4                        
  1d684:  bl #0x22000                       -> func_0x22000
  1d688:  ldr r4, [pc, #0x110]              -> периферия
  1d68a:  add r2, sp, #0x3c                 
  1d68c:  lsls r1, r7, #5                   
  1d68e:  mov r0, r4                        
  1d690:  bl #0x22000                       -> func_0x22000
  1d694:  add r2, sp, #0x3c                 
  1d696:  lsls r1, r7, #6                   
  1d698:  mov r0, r4                        
  1d69a:  bl #0x22000                       -> func_0x22000
  1d69e:  add r2, sp, #0x3c                 
  1d6a0:  lsls r1, r4, #5                   
  1d6a2:  mov r0, r4                        
  1d6a4:  bl #0x22000                       -> func_0x22000
  1d6a8:  add r2, sp, #0x3c                 
  1d6aa:  lsls r1, r7, #4                   
  1d6ac:  mov r0, r4                        
  1d6ae:  bl #0x22000                       -> func_0x22000
  1d6b2:  movs r1, #0x3c                    
  1d6b4:  mov r0, sp                        
  1d6b6:  bl #0x19a9a                       -> 0x19a9a (вне списка функций)
  1d6ba:  ldr r4, [pc, #0xe4]               -> периферия
  1d6bc:  movs r1, #3                       
  1d6be:  mov r0, sp                        
  1d6c0:  str r5, [sp, #4]                  
  1d6c2:  str r4, [sp]                      
  1d6c4:  strb r1, [r0, #8]                 
  1d6c6:  ldr r0, [pc, #0xdc]               -> данные @0x008ca
  1d6c8:  str r0, [sp, #0xc]                
  1d6ca:  mov r0, sp                        
  1d6cc:  strb r5, [r0, #0x10]              
  1d6ce:  str r5, [sp, #0x14]               
  1d6d0:  bl #0x22b00                       -> 0x22b00 (вне списка функций)
  1d6d4:  mov r0, sp                        
  1d6d6:  bl #0x22a48                       -> func_0x22a48
  1d6da:  str r5, [sp, #0x44]               
  1d6dc:  str r5, [sp, #0x4c]               
  1d6de:  add r0, sp, #0x40                 
  1d6e0:  str r5, [sp, #0x50]               
  1d6e2:  strb r6, [r0, #4]                 
  1d6e4:  ldr r0, [pc, #0xc0]               -> данные @0x0045b
  1d6e6:  str r0, [sp, #0x48]               
  1d6e8:  movs r6, #1                       
  1d6ea:  add r0, sp, #0x40                 
  1d6ec:  strb r6, [r0, #0xd]               
  1d6ee:  strb r5, [r0, #0xc]               
  1d6f0:  strb r5, [r0, #0xf]               
  1d6f2:  strb r6, [r0, #0x10]              
  1d6f4:  movs r2, #0                       
  1d6f6:  add r1, sp, #0x44                 
  1d6f8:  mov r0, sp                        
  1d6fa:  bl #0x23040                       -> func_0x23040
  1d6fe:  movs r2, #1                       
  1d700:  add r1, sp, #0x44                 
  1d702:  mov r0, sp                        
  1d704:  bl #0x23040                       -> func_0x23040
  1d708:  movs r2, #2                       
  1d70a:  add r1, sp, #0x44                 
  1d70c:  mov r0, sp                        
  1d70e:  bl #0x23040                       -> func_0x23040
  1d712:  movs r2, #4                       
  1d714:  add r1, sp, #0x44                 
  1d716:  mov r0, sp                        
  1d718:  bl #0x23040                       -> func_0x23040
  1d71c:  ldr r0, [r4, #0x30]               
  1d71e:  orrs r0, r6                       
  1d720:  str r0, [r4, #0x30]               
  1d722:  ldr r0, [r4, #0x30]               
  1d724:  movs r1, #0x10                    
  1d726:  orrs r0, r1                       
  1d728:  str r0, [r4, #0x30]               
  1d72a:  ldr r0, [r4, #0x30]               
  1d72c:  orrs r0, r7                       
  1d72e:  str r0, [r4, #0x30]               
  1d730:  ldr r0, [r4, #0x30]               
  1d732:  lsls r1, r1, #8                   
  1d734:  orrs r0, r1                       
  1d736:  str r0, [r4, #0x30]               
  1d738:  ldr r0, [r4, #0x30]               
  1d73a:  movs r1, #4                       
  1d73c:  orrs r0, r1                       
  1d73e:  str r0, [r4, #0x30]               
  1d740:  ldr r0, [r4, #0x30]               
  1d742:  movs r1, #0x40                    
  1d744:  orrs r0, r1                       
  1d746:  str r0, [r4, #0x30]               
  1d748:  ldr r0, [r4, #0x30]               
  1d74a:  lsls r1, r1, #4                   
  1d74c:  orrs r0, r1                       
  1d74e:  str r0, [r4, #0x30]               
  1d750:  str r5, [sp, #0x54]               
  1d752:  add r0, sp, #0x40                 
  1d754:  str r5, [sp, #0x5c]               
  1d756:  strb r6, [r0, #0x14]              
  1d758:  strb r6, [r0, #0x15]              
  1d75a:  strb r6, [r0, #0x16]              
  1d75c:  movs r0, #0x24                    
  1d75e:  str r0, [sp, #0x58]               
  1d760:  add r0, sp, #0x40                 
  1d762:  strb r6, [r0, #0x1c]              
  1d764:  strb r5, [r0, #0x1d]              
  1d766:  strb r5, [r0, #0x1e]              
  1d768:  add r1, sp, #0x54                 
  1d76a:  mov r0, sp                        
  1d76c:  bl #0x22c70                       -> func_0x22c70
  1d770:  ldr r0, [r4, #0xc]                
  1d772:  movs r1, #0x80                    
  1d774:  orrs r0, r1                       
  1d776:  str r0, [r4, #0xc]                
  1d778:  movs r2, #1                       
  1d77a:  movs r1, #0                       
  1d77c:  movs r0, #0xd                     
  1d77e:  bl #0x23544                       -> func_0x23544
  1d782:  ldr r0, [pc, #0x1c]               -> периферия
  1d784:  adds r0, #0x40                    
  1d786:  str r5, [r0, #4]                  
  1d788:  str r5, [r0, #8]                  
  1d78a:  str r5, [r0, #0xc]                
  1d78c:  ldr r1, [pc, #0x14]               -> данные @0x008ca
  1d78e:  subs r1, r1, #1                   
  1d790:  str r1, [r0, #0x10]               
  1d792:  ldr r0, [r4]                      
  1d794:  orrs r0, r6                       
  1d796:  str r0, [r4]                      
  1d798:  add sp, #0x64                     
  1d79a:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x1d79c (4 слов) — ВНЕ границ функции ---
  1d79c:  .word 0x48000400  ; периферия
  1d7a0:  .word 0x40012c00  ; периферия
  1d7a4:  .word 0x000008ca  ; данные @0x008ca
  1d7a8:  .word 0x0000045b  ; данные @0x0045b
```
