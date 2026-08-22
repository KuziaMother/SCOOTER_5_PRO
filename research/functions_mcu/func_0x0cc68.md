# func_0x0cc68

| | |
|---|---|
| offset = vaddr (база 0x0; mirror 0x08000cc68) | `0x0000cc68` |
| размер кода | 76 Б |
| регион | код B (FLASH-OTA: 0x06230/0x06304) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x40002840 — периферия (r5)

## Вызовы (callees)

- 0x0cca0 (b, вне списка функций)
- 0x0ccb6 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- `func_0x03168` (bl @0x0000316e)


## Внутренние блоки (цели b/b.w/cbz внутри функции; заголовки циклов исключены)

- `0x0cc86..0x0cc96` (16 Б); цели из: 0x0cc78, 0x0cc7e
- `0x0cc96..0x0cca0` (10 Б); цели из: 0x0cc84
- `0x0cca0..0x0ccb4` (20 Б); цели из: 0x0cc90, 0x0cc94

## Дизассембляция

```asm
  0cc68:  push {r4, r5, lr}                 
  0cc6a:  mov r1, r0                        
  0cc6c:  movs r0, #0                       
  0cc6e:  movs r2, #0                       
  0cc70:  movs r3, #0                       
  0cc72:  movs r4, #0                       
  0cc74:  cmp.w r1, #0x20000                
  0cc78:  beq #0xcc86                       
  0cc7a:  cmp.w r1, #0x40000                
  0cc7e:  beq #0xcc86                       
  0cc80:  cmp.w r1, #0x80000                
  0cc84:  bne #0xcc96                       
  0cc86:  ldr r5, [pc, #0x30]               -> периферия
  0cc88:  ldr r5, [r5]                      
  0cc8a:  ubfx r4, r5, #0x10, #8            
  0cc8e:  cmp r4, #0                        
  0cc90:  ble #0xcca0                       
  0cc92:  movs r3, #1                       
  0cc94:  b #0xcca0                         -> 0x0cca0 (вне списка функций)
  0cc96:  ldr r5, [pc, #0x20]               -> периферия
  0cc98:  subs r5, #0x38                    
  0cc9a:  ldr r5, [r5]                      
  0cc9c:  and.w r3, r5, r1                  
  0cca0:  ldr r5, [pc, #0x14]               -> периферия
  0cca2:  subs r5, #0x34                    
  0cca4:  ldr r5, [r5]                      
  0cca6:  and.w r2, r5, r1, lsr #4          
  0ccaa:  cbz r3, #0xccb4                   
  0ccac:  uxth r5, r2                       
  0ccae:  cbz r5, #0xccb4                   
  0ccb0:  movs r0, #1                       
  0ccb2:  b #0xccb6                         -> 0x0ccb6 (вне списка функций)
  ; --- literal-пул @0x0ccb8 (1 слов) — ВНЕ границ функции ---
  0ccb8:  .word 0x40002840  ; периферия
```
