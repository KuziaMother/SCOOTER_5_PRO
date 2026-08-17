# func_0x0280c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000280c) | `0x0000280c` |
| размер кода | 88 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40005800 — периферия (r0)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- 0x02846 (b, вне списка функций)
- `func_0x09048` (0x00009048, bl)

## Кто вызывает (callers / xrefs)

- `func_0x0c158` (bl @0x0000c1a4)
- `func_0x0c158` (bl @0x0000c1d0)


## Дизассембляция

```asm
  0280c:  push.w {r4, r5, r6, r7, r8, sb, lr}
  02810:  sub sp, #0x1c                     
  02812:  mov sb, r0                        
  02814:  mov r7, r1                        
  02816:  mov r5, r2                        
  02818:  mov r6, r3                        
  0281a:  ldr.w r8, [sp, #0x38]             
  0281e:  movs r1, #0x14                    
  02820:  add r0, sp, #8                    
  02822:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  02826:  movs r0, #0                       
  02828:  str r0, [sp, #4]                  
  0282a:  movs r4, #0                       
  0282c:  uxtb r0, r5                       
  0282e:  strb.w r0, [sp, #8]               
  02832:  lsrs r0, r5, #8                   
  02834:  strb.w r0, [sp, #9]               
  02838:  b #0x2846                         -> 0x02846 (вне списка функций)
  0283a:  ldrb r1, [r6, r4]                 
  0283c:  add r2, sp, #8                    
  0283e:  adds r0, r4, #2                   
  02840:  strb r1, [r2, r0]                 
  02842:  adds r0, r4, #1                   
  02844:  uxtb r4, r0                       
  02846:  cmp r4, #0xf                      
  02848:  blt #0x283a                       
  0284a:  movs r0, #0x11                    
  0284c:  add r3, sp, #8                    
  0284e:  movs r2, #0x3e                    
  02850:  mov r1, r7                        
  02852:  str r0, [sp]                      
  02854:  ldr r0, [pc, #0x178]              -> периферия
  02856:  bl #0x9048                        -> func_0x09048
  0285a:  cbnz r0, #0x2864                  
  0285c:  movs r0, #0                       
  0285e:  add sp, #0x1c                     
  02860:  pop.w {r4, r5, r6, r7, r8, sb, pc}
  ; --- literal-пул @0x029d0 (1 слов) — ВНЕ границ функции ---
  029d0:  .word 0x40005800  ; периферия
```
