# func_0x0ab0c

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000ab0c) | `0x0000ab0c` |
| размер кода | 46 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- (нет)

## Вызовы (callees)

- 0x011d6 (bl, вне списка функций)
- `func_0x0a910` (0x0000a910, bl)

## Кто вызывает (callers / xrefs)

- `func_0x05330` (bl @0x0000534c)
- `func_0x05330` (bl @0x000053ba)
- `func_0x0d00c` (bl @0x0000d01a)
- `func_0x0d46c` (bl @0x0000d47e)
- `func_0x0d534` (bl @0x0000d548)
- `func_0x0d5d4` (bl @0x0000d5e8)
- `func_0x0d670` (bl @0x0000d696)
- `func_0x0f038` (bl @0x0000f04e)
- `func_0x0f14c` (bl @0x0000f160)
- `func_0x11674` (bl @0x0001168a)
- `func_0x11674` (bl @0x000116f2)
- `func_0x11724` (bl @0x0001173c)
- `func_0x11724` (bl @0x000117a0)
- `func_0x117d4` (bl @0x000117ec)
- `func_0x117d4` (bl @0x00011850)
- `func_0x156ac` (bl @0x000156bc)


## Дизассембляция

```asm
  0ab0c:  push {r4, r5, r6, r7, lr}         
  0ab0e:  sub sp, #0x3c                     
  0ab10:  mov r7, r0                        
  0ab12:  movs r6, #0                       
  0ab14:  movs r4, #0                       
  0ab16:  movs r5, #0                       
  0ab18:  movs r1, #0x38                    
  0ab1a:  add r0, sp, #4                    
  0ab1c:  bl #0x11d6                        -> 0x011d6 (вне списка функций)
  0ab20:  movs r0, #0                       
  0ab22:  bl #0xa910                        -> func_0x0a910
  0ab26:  mov r6, r0                        
  0ab28:  movs r0, #1                       
  0ab2a:  bl #0xa910                        -> func_0x0a910
  0ab2e:  mov r4, r0                        
  0ab30:  cbnz r6, #0xab8e                  
  0ab32:  cbnz r4, #0xab3a                  
  0ab34:  movs r0, #0                       
  0ab36:  add sp, #0x3c                     
  0ab38:  pop {r4, r5, r6, r7, pc}          
```
