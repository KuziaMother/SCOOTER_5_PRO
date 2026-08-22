# func_0x08a50

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080008a50) | `0x00008a50` |
| размер кода | 54 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x08019584 — flash-mirror @0x19584 (r0)
- 0x08019684 — flash-mirror @0x19684 (r0)

## Вызовы (callees)

- 0x08a72 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03da0` (bl @0x00003dc4)
- `func_0x05330` (bl @0x00005398)
- `func_0x0bd50` (bl @0x0000be26)
- `func_0x0c420` (bl @0x0000c444)
- `func_0x0cf60` (bl @0x0000cf94)
- `func_0x0cfb8` (bl @0x0000cff0)
- `func_0x0d00c` (bl @0x0000d03a)
- `func_0x0d00c` (bl @0x0000d0ac)
- `func_0x0d00c` (bl @0x0000d0d8)
- `func_0x0d00c` (bl @0x0000d136)
- `func_0x0d00c` (bl @0x0000d158)
- `func_0x0d00c` (bl @0x0000d1a6)
- `func_0x0d00c` (bl @0x0000d206)
- `func_0x0d240` (bl @0x0000d27c)
- `func_0x0d39c` (bl @0x0000d3cc)
- `func_0x0d39c` (bl @0x0000d446)
- `func_0x0d46c` (bl @0x0000d49c)
- `func_0x0d46c` (bl @0x0000d4fe)
- `func_0x0d534` (bl @0x0000d5a0)
- `func_0x0d5d4` (bl @0x0000d63a)
- `func_0x0d670` (bl @0x0000d6b2)
- `func_0x0d938` (bl @0x0000dcf4)
- `func_0x0f038` (bl @0x0000f06c)
- `func_0x0f14c` (bl @0x0000f1b6)
- `func_0x11674` (bl @0x000116d0)
- `func_0x11724` (bl @0x0001177e)
- `func_0x117d4` (bl @0x0001182e)
- `func_0x13b60` (bl @0x00013b9c)
- `func_0x147ac` (bl @0x000147bc)
- `func_0x156ac` (bl @0x000156e2)
- `func_0x1570c` (bl @0x0001571c)
- `func_0x15790` (bl @0x000157a0)


## Дизассембляция

```asm
  08a50:  push {r4, r5, r6, r7, lr}         
  08a52:  mov r2, r0                        
  08a54:  movs r3, #0xff                    
  08a56:  movs r5, #0xff                    
  08a58:  b #0x8a72                         -> 0x08a72 (вне списка функций)
  08a5a:  ldrb r0, [r2], #1                 
  08a5e:  eor.w r4, r0, r3                  
  08a62:  ldr r0, [pc, #0x24]               -> flash-mirror @0x19584
  08a64:  ldrb r0, [r0, r4]                 
  08a66:  eor.w r3, r0, r5                  
  08a6a:  ldr r0, [pc, #0x20]               -> flash-mirror @0x19684
  08a6c:  ldrb r5, [r0, r4]                 
  08a6e:  subs r0, r1, #1                   
  08a70:  uxth r1, r0                       
  08a72:  cmp r1, #0                        
  08a74:  bne #0x8a5a                       
  08a76:  mov r6, r3                        
  08a78:  movw r0, #0xffff                  
  08a7c:  and.w r6, r0, r6, lsl #8          
  08a80:  orr.w r0, r6, r5                  
  08a84:  pop {r4, r5, r6, r7, pc}          
  ; --- literal-пул @0x08a88 (2 слов) — ВНЕ границ функции ---
  08a88:  .word 0x08019584  ; flash-mirror @0x19584
  08a8c:  .word 0x08019684  ; flash-mirror @0x19684
```
