# func_0x05a68

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x080005a68) | `0x00005a68` |
| размер кода | 32 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- (нет)

## Кто вызывает (callers / xrefs)

- `func_0x05dd8` (bl @0x00005e8a)
- `func_0x05dd8` (bl @0x00005eb8)


## Дизассембляция

```asm
  05a68:  push.w {r4, r5, r6, r7, r8, sb, sl, lr}
  05a6c:  mov r5, r0                        
  05a6e:  mov r6, r1                        
  05a70:  mov r8, r2                        
  05a72:  mov r7, r3                        
  05a74:  movs r4, #0                       
  05a76:  mov sb, r4                        
  05a78:  sdiv r0, r7, r8                   
  05a7c:  mls r0, r8, r0, r7                
  05a80:  cbz r0, #0x5a88                   
  05a82:  movs r0, #0                       
  05a84:  pop.w {r4, r5, r6, r7, r8, sb, sl, pc}
```
