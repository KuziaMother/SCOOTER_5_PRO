# func_0x0d878

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000d878) | `0x0000d878` |
| размер кода | 190 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- `func_0x082f0` (0x000082f0, bl)
- `func_0x084a0` (0x000084a0, bl)
- `func_0x087f8` (0x000087f8, bl)
- `func_0x08a90` (0x00008a90, bl)
- 0x0d8fe (b, вне списка функций)
- 0x0d902 (b, вне списка функций)
- 0x0d92e (b, вне списка функций)
- 0x0d932 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03740` (bl @0x00003762)
- `func_0x05448` (bl @0x000054d0)
- `func_0x0bf4c` (bl @0x0000bf4e)
- `func_0x11de8` (bl @0x00011ef6)
- `func_0x11de8` (bl @0x00012048)
- `func_0x15ce0` (bl @0x00015cfa)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0d8fe..0x0d902` (4 Б); цели из: 0x0d8d6
- `0x0d902..0x0d92e` (44 Б); цели из: 0x0d8f8
- `0x0d92e..0x0d932` (4 Б); цели из: 0x0d906
- `0x0d932..0x0d936` (4 Б); цели из: 0x0d928

## Дизассембляция

```asm
  0d878:  push {r0, r1, r2, r3, r4, lr}     
  0d87a:  mov r0, sp                        
  0d87c:  bl #0x8a90                        -> func_0x08a90
  0d880:  ldr r0, [sp]                      
  0d882:  str r0, [sp, #8]                  
  0d884:  ldrh.w r0, [sp, #4]               
  0d888:  strh.w r0, [sp, #0xc]             
  0d88c:  ldrb.w r0, [sp, #6]               
  0d890:  strb.w r0, [sp, #0xe]             
  0d894:  movs r1, #7                       
  0d896:  add r0, sp, #8                    
  0d898:  bl #0x87f8                        -> func_0x087f8
  0d89c:  strb.w r0, [sp, #0xf]             
  0d8a0:  mov.w r0, #0x50000                
  0d8a4:  bl #0x82f0                        -> func_0x082f0
  0d8a8:  mov.w r0, #0x3e8                  
  0d8ac:  str r0, [sp, #4]                  
  0d8ae:  nop                               
  0d8b0:  ldr r0, [sp, #4]                  
  0d8b2:  subs r1, r0, #1                   
  0d8b4:  str r1, [sp, #4]                  
  0d8b6:  cmp r0, #0                        
  0d8b8:  bne #0xd8b0                       
  0d8ba:  mov.w r0, #0x51000                
  0d8be:  bl #0x82f0                        -> func_0x082f0
  0d8c2:  mov.w r0, #0x3e8                  
  0d8c6:  str r0, [sp, #4]                  
  0d8c8:  nop                               
  0d8ca:  ldr r0, [sp, #4]                  
  0d8cc:  subs r1, r0, #1                   
  0d8ce:  str r1, [sp, #4]                  
  0d8d0:  cmp r0, #0                        
  0d8d2:  bne #0xd8ca                       
  0d8d4:  movs r4, #0                       
  0d8d6:  b #0xd8fe                         -> 0x0d8fe (вне списка функций)
  0d8d8:  mov.w r0, #0x3e8                  
  0d8dc:  str r0, [sp, #4]                  
  0d8de:  nop                               
  0d8e0:  ldr r0, [sp, #4]                  
  0d8e2:  subs r1, r0, #1                   
  0d8e4:  str r1, [sp, #4]                  
  0d8e6:  cmp r0, #0                        
  0d8e8:  bne #0xd8e0                       
  0d8ea:  movs r2, #8                       
  0d8ec:  mov.w r1, #0x50000                
  0d8f0:  add r0, sp, #8                    
  0d8f2:  bl #0x84a0                        -> func_0x084a0
  0d8f6:  cbz r0, #0xd8fa                   
  0d8f8:  b #0xd902                         -> 0x0d902 (вне списка функций)
  0d8fa:  adds r0, r4, #1                   
  0d8fc:  uxtb r4, r0                       
  0d8fe:  cmp r4, #3                        
  0d900:  blt #0xd8d8                       
  0d902:  nop                               
  0d904:  movs r4, #0                       
  0d906:  b #0xd92e                         -> 0x0d92e (вне списка функций)
  0d908:  mov.w r0, #0x3e8                  
  0d90c:  str r0, [sp, #4]                  
  0d90e:  nop                               
  0d910:  ldr r0, [sp, #4]                  
  0d912:  subs r1, r0, #1                   
  0d914:  str r1, [sp, #4]                  
  0d916:  cmp r0, #0                        
  0d918:  bne #0xd910                       
  0d91a:  movs r2, #8                       
  0d91c:  mov.w r1, #0x51000                
  0d920:  add r0, sp, #8                    
  0d922:  bl #0x84a0                        -> func_0x084a0
  0d926:  cbz r0, #0xd92a                   
  0d928:  b #0xd932                         -> 0x0d932 (вне списка функций)
  0d92a:  adds r0, r4, #1                   
  0d92c:  uxtb r4, r0                       
  0d92e:  cmp r4, #3                        
  0d930:  blt #0xd908                       
  0d932:  nop                               
  0d934:  pop {r0, r1, r2, r3, r4, pc}      
```
